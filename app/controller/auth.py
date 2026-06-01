"""
Authentication controller.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.services.auth_service import AuthService
from app.repositories.tenant_repo import tenant_repo

auth_controller = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_controller.post(
    "/login",
    response_model=schemas.Token
)
def login(
    login_data: schemas.LoginRequest,
    db: Session = Depends(deps.get_db),
) -> schemas.Token:
    """Login endpoint."""

    token = AuthService.login(
        db,
        login_data.username,
        login_data.email,
        login_data.password,
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username, email, or password",
        )

    return token


@auth_controller.post("/logout")
def logout(
    current_user: schemas.User = Depends(
        deps.get_current_user
    ),
) -> dict:
    """Logout endpoint."""

    return {
        "message": "Successfully logged out"
    }


@auth_controller.post(
    "/refresh",
    response_model=schemas.Token
)
def refresh_token(
    refresh_token: schemas.RefreshToken,
    db: Session = Depends(deps.get_db),
) -> schemas.Token:
    """Refresh access token."""

    token = AuthService.refresh_access_token(
        db,
        refresh_token.refresh_token
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    return token


@auth_controller.post(
    "/register",
    response_model=schemas.User
)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_reg: schemas.UserRegister,
) -> schemas.User:
    """
    Register a new user in an organization.
    """

    try:

        user = AuthService.register_user(
            db,
            user_reg,
            tenant_repo
        )

        return user

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@auth_controller.post("/verify-email")
def verify_email(
    verify_data: schemas.VerifyEmailRequest,
    db: Session = Depends(deps.get_db),
):

    try:

        result = AuthService.verify_email(
            db=db,
            email=verify_data.email,
            verification_code=verify_data.verification_code
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@auth_controller.post("/forgot-password")
def forgot_password(
    forgot_data: schemas.ForgotPasswordRequest,
    db: Session = Depends(deps.get_db),
):

    try:

        result = AuthService.forgot_password(
            db=db,
            email=forgot_data.email
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@auth_controller.post("/reset-password")
def reset_password(
    reset_data: schemas.ResetPasswordRequest,
    db: Session = Depends(deps.get_db),
):

    try:

        result = AuthService.reset_password(
            db=db,
            email=reset_data.email,
            verification_code=reset_data.verification_code,
            new_password=reset_data.new_password
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@auth_controller.post("/resend-verification")
def resend_verification(
    resend_data: schemas.ResendVerificationRequest,
    db: Session = Depends(deps.get_db),
):

    try:

        result = AuthService.resend_verification(
            db=db,
            email=resend_data.email
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@auth_controller.post("/verify-login-otp")
def verify_login_otp(
    verify_data: schemas.VerifyEmailRequest,
    db: Session = Depends(deps.get_db),
):

    try:

        result = AuthService.verify_login_otp(
            db=db,
            email=verify_data.email,
            verification_code=verify_data.verification_code
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )