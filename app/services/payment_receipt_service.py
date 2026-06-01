"""
Payment receipt service.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models import PaymentReceipt
from app.services.invoice_service import (
    invoice_service
)

class PaymentReceiptService:
    """Payment receipt service."""

    def create_receipt(
        self,
        db: Session,
        tenant_id: str,
        amount,
        payment_id: str
    ):

        receipt = PaymentReceipt(
            tenant_id=tenant_id,
            vendor="Razorpay",
            amount_usd=amount,
            currency="INR",
            payment_date=datetime.utcnow(),
            status="paid",
            invoice_number=f"INV-{payment_id[:8]}",
            description="Subscription Payment",
            category="Subscription"
        )
        file_path = (
            invoice_service.generate_invoice(
                invoice_number=
                    receipt.invoice_number,
                amount=
                    receipt.amount_usd,
                payment_date=
                    receipt.payment_date,
                vendor=
                    receipt.vendor
            )
        )

        receipt.download_url = file_path
        db.add(receipt)
        db.commit()
        db.refresh(receipt)

        return receipt


payment_receipt_service = (
    PaymentReceiptService()
)