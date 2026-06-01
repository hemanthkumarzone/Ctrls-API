"""
Payment repository.
"""

from sqlalchemy.orm import Session

from app.models import Payment
from app.repositories.base import BaseRepository


class PaymentRepository(
    BaseRepository[Payment]
):
    """Payment repository."""

    def get_by_order_id(
        self,
        db: Session,
        order_id: str
    ):
        return (
            db.query(Payment)
            .filter(
                Payment.razorpay_order_id
                == order_id
            )
            .first()
        )


payment_repo = (
    PaymentRepository(
        Payment
    )
)