"""
Tenant service.
"""

from sqlalchemy.orm import Session

from app.models import Tenant
from app.repositories.tenant_repo import tenant_repo
from app.schemas.tenant import TenantCreate, TenantUpdate


class TenantService:
    """Tenant service."""

    def get_tenants(self, db: Session, skip: int = 0, limit: int = 100) -> list[Tenant]:
        """Get all tenants."""
        return tenant_repo.get_multi(db, skip=skip, limit=limit)

    def get_tenant(self, db: Session, tenant_id: str) -> Tenant | None:
        """Get tenant by ID."""
        return tenant_repo.get(db, tenant_id)

    def create_tenant(self, db: Session, tenant_in: TenantCreate) -> Tenant:
        """Create new tenant."""
        tenant_data = tenant_in.dict()
        return tenant_repo.create(db, obj_in=tenant_data)

    def update_tenant(self, db: Session, tenant_id: str, tenant_in: TenantUpdate) -> Tenant:
        """Update tenant."""
        tenant = self.get_tenant(db, tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        return tenant_repo.update(db, db_obj=tenant, obj_in=tenant_in)

    def delete_tenant(self, db: Session, tenant_id: str) -> None:
        """Delete tenant."""
        tenant_repo.remove(db, id=tenant_id)