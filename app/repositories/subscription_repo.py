"""
Subscription repository.
"""

from sqlalchemy.orm import Session

from app.models import Subscription
from app.repositories.base import BaseRepository


class SubscriptionRepository(
    BaseRepository[Subscription]
):
    """Subscription repository."""

    def get_by_tenant(
        self,
        db: Session,
        tenant_id: str
    ):
        return (
            db.query(Subscription)
            .filter(
                Subscription.tenant_id
                == tenant_id
            )
            .first()
        )
    
    def activate_subscription(
        self,
        db: Session,
        subscription: Subscription
    ):

        subscription.status = "active"

        subscription.auto_renew = True

        db.add(subscription)

        db.commit()

        db.refresh(subscription)

        return subscription
    def cancel_subscription(
        self,
        db: Session,
        subscription: Subscription
    ):

        subscription.status = "cancelled"

        subscription.auto_renew = False

        db.add(subscription)

        db.commit()

        db.refresh(subscription)

        return subscription

subscription_repo = (
    SubscriptionRepository(
        Subscription
    )
)

