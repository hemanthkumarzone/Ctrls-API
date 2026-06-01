"""
Authentication schemas.
"""

from typing import Optional

from pydantic import BaseModel, field_validator

from app.core.security import validate_password
from .base import BaseSchema
from .user import User

class LoginRequest(BaseModel):
    """Login request schema."""
    
    username: str
    email: str
    password: str


class Token(BaseModel):
    """Token response schema."""

    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    user: Optional[User] = None

    requires_2fa: Optional[bool] = False
    message: Optional[str] = None
    email: Optional[str] = None


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None
    tenant_id: Optional[str] = None


class RefreshToken(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


from pydantic import BaseModel, EmailStr, field_validator, model_validator

class UserRegister(BaseModel):
    username: str
    company_name: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        return validate_password(value)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    
class VerifyEmailRequest(BaseModel):
    email: EmailStr
    verification_code: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    verification_code: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    def validate_new_password(cls, value: str) -> str:
        return validate_password(value)

    @model_validator(mode="after")
    def passwords_match(self):

        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")

        return self


class ResendVerificationRequest(BaseModel):
    email: EmailStr