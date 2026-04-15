"""
Authentication service.
"""

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models import User
from app.repositories.user_repo import user_repo
from app.schemas.user import UserCreate


class AuthService:
    """Authentication service."""

    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str,
        tenant_id: str | None = None,
    ) -> User | None:
        """Authenticate user with email and password."""
        if tenant_id:
            user = user_repo.get_by_tenant_and_email(db, tenant_id=tenant_id, email=email)
        else:
            candidates = db.query(User).filter(User.email == email).all()
            if len(candidates) > 1:
                return None
            user = candidates[0] if candidates else None

        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """Create new user."""
        user_data = user_in.dict()
        user_data["password_hash"] = get_password_hash(user_in.password)
        del user_data["password"]
        return user_repo.create(db, obj_in=user_data)