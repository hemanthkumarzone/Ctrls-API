"""
Authentication schemas.
"""

from typing import Optional

from pydantic import BaseModel

from .base import BaseSchema
from .user import User


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str
    user: User


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None
    tenant_id: Optional[str] = None


class RefreshToken(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class UserRegister(BaseModel):
    """User registration schema (requires organization)."""
    email: str
    password: str
    org_slug: str
    org_admin_name: str
    role: str = "viewer"