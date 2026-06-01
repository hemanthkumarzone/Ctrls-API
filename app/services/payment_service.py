"""
Payment service.
"""

from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Payment


class PaymentService:
    """Payment service."""

    def create_payment(
        self,
        db: Session,
        tenant_id: str,
        subscription_id: str,
        amount: Decimal,
        order_id: str,
    ):

        payment = Payment(
            tenant_id=tenant_id,
            subscription_id=subscription_id,
            amount=amount,
            payment_status="pending",
            razorpay_order_id=order_id,
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return payment

    def mark_payment_success(
        self,
        db: Session,
        payment: Payment,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ):

        payment.payment_status = "success"
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return payment


payment_service = PaymentService()