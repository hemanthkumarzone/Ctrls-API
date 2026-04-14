"""
Tenant management endpoints.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models import User
from app.services.tenant_service import TenantService

router = APIRouter()
tenant_service = TenantService()


@router.get("/", response_model=List[schemas.Tenant])
def read_tenants(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Retrieve tenants (owner only)."""
    if current_user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    tenants = tenant_service.get_tenants(db, skip=skip, limit=limit)
    return tenants


@router.post("/", response_model=schemas.Tenant)
def create_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_in: schemas.TenantCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Create new tenant (owner only)."""
    if current_user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    tenant = tenant_service.create_tenant(db, tenant_in)
    return tenant


@router.get("/{tenant_id}", response_model=schemas.Tenant)
def read_tenant(
    *,
    tenant_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Get tenant by ID."""
    tenant = tenant_service.get_tenant(db, tenant_id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    return tenant


@router.put("/{tenant_id}", response_model=schemas.Tenant)
def update_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: str,
    tenant_in: schemas.TenantUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Update tenant (owner only)."""
    if current_user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    tenant = tenant_service.update_tenant(db, tenant_id=tenant_id, tenant_in=tenant_in)
    return tenant


@router.delete("/{tenant_id}")
def delete_tenant(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Delete tenant (owner only)."""
    if current_user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    tenant_service.delete_tenant(db, tenant_id=tenant_id)
    return {"message": "Tenant deleted successfully"}