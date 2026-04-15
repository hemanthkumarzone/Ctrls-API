"""
Authentication endpoints.
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.models import User
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    tenant_id: str | None = Query(None, description="Optional tenant ID for scoped login"),
) -> Any:
    """Login endpoint."""
    user = auth_service.authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password,
        tenant_id=tenant_id,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
        extra_claims={
            "tenant_id": user.tenant_id,
            "roles": [user.role],
        },
    )
    refresh_token = security.create_refresh_token(
        subject=user.id,
        extra_claims={"tenant_id": user.tenant_id},
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": schemas.User.from_orm(user),
    }


@router.post("/register", response_model=schemas.User)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """Register new user."""
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = auth_service.create_user(db, user_in)
    return user


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    token_in: schemas.RefreshToken,
    db: Session = Depends(deps.get_db),
) -> Any:
    """Refresh access token."""
    try:
        payload = security.verify_token(token_in.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            subject=user.id,
            expires_delta=access_token_expires,
            extra_claims={
                "tenant_id": user.tenant_id,
                "roles": [user.role],
            },
        )
        refresh_token = security.create_refresh_token(
            subject=user.id,
            extra_claims={"tenant_id": user.tenant_id},
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": schemas.User.from_orm(user),
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


@router.post("/logout", response_model=dict)
def logout(current_user: User = Depends(deps.get_current_user)) -> Any:
    """Logout endpoint - client should discard tokens."""
    return {"message": "Successfully logged out"}