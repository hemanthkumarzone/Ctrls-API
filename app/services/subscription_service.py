"""
Subscription service.
"""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Subscription


class SubscriptionService:
    """Subscription service."""

    def create_trial_subscription(
        self,
        db: Session,
        tenant_id: str,
        plan_name: str,
        billing_cycle: str = "monthly",
    ):

        subscription = Subscription(
            tenant_id=tenant_id,
            plan_name=plan_name,
            billing_cycle=billing_cycle,
            status="trial",
            trial_start_date=datetime.utcnow(),
            trial_end_date=datetime.utcnow()
            + timedelta(days=14),
            auto_renew=False,
        )

        db.add(subscription)
        db.commit()
        db.refresh(subscription)

        return subscription

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
    def expire_trial_subscriptions(
        self,
        db: Session
    ):

        from datetime import datetime

        expired_subscriptions = (
            db.query(Subscription)
            .filter(
                Subscription.status == "trial",
                Subscription.trial_end_date < datetime.utcnow()
            )
           .all()
        )

        for subscription in expired_subscriptions:

            subscription.status = "expired"

            db.add(subscription)

        db.commit()

        return len(expired_subscriptions)
subscription_service = SubscriptionService()

