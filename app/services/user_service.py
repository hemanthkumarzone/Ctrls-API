"""
User service.
"""

from sqlalchemy.orm import Session

from app.models import User
from app.repositories.user_repo import user_repo
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """User service."""

    def get_users(
        self, db: Session, tenant_id: str, skip: int = 0, limit: int = 100
    ) -> list[User]:
        """Get users for a tenant."""
        return (
            db.query(User)
            .filter(User.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user(self, db: Session, user_id: str) -> User | None:
        """Get user by ID."""
        return user_repo.get(db, user_id)

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """Create new user."""
        user_data = user_in.dict()
        return user_repo.create(db, obj_in=user_data)

    def update_user(self, db: Session, user_id: str, user_in: UserUpdate) -> User:
        """Update user."""
        user = self.get_user(db, user_id)
        if not user:
            raise ValueError("User not found")
        return user_repo.update(db, db_obj=user, obj_in=user_in)

    def delete_user(self, db: Session, user_id: str) -> None:
        """Delete user."""
        user_repo.remove(db, id=user_id)