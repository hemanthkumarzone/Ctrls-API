"""
Tenant schemas.
"""

from typing import Dict, Optional

from pydantic import BaseModel

from .base import BaseSchema, TimestampMixin


class TenantBase(BaseSchema):
    """Base tenant schema."""
    name: str
    slug: str
    plan: str
    is_active: bool = True
    metadata_: Optional[Dict] = {}


class TenantCreate(BaseModel):
    """Tenant creation schema."""
    name: str
    slug: str
    plan: str = "starter"


class OrgAdminCreate(BaseModel):
    """Organization creation with admin user."""
    org_name: str
    org_slug: str
    org_plan: str = "starter"
    admin_email: str
    admin_password: str
    admin_name: str


class TenantUpdate(BaseModel):
    """Tenant update schema."""
    name: Optional[str] = None
    plan: Optional[str] = None
    is_active: Optional[bool] = None
    metadata_: Optional[Dict] = None


class Tenant(TenantBase, TimestampMixin):
    """Tenant response schema."""
    id: str