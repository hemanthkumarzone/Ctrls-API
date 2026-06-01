from sqlalchemy.orm import Session

from app.models import PaymentReceipt
from app.repositories.base import BaseRepository


class PaymentReceiptRepository(
    BaseRepository[PaymentReceipt]
):

    def get_by_tenant(
        self,
        db: Session,
        tenant_id: str
    ):
        return (
            db.query(PaymentReceipt)
            .filter(
                PaymentReceipt.tenant_id
                == tenant_id
            )
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        receipt_id: str
    ):
        return (
            db.query(PaymentReceipt)
            .filter(
                PaymentReceipt.id
                == receipt_id
            )
            .first()
        )
    def get_by_vendor(
        self,
        db: Session,
        vendor: str
    ):
        return (
            db.query(PaymentReceipt)
            .filter(
                PaymentReceipt.vendor
                == vendor
            )
            .all()
        )
    def get_summary(
        self,
        db: Session,
        tenant_id: str
    ):
        receipts = (
            db.query(PaymentReceipt)
            .filter(
                PaymentReceipt.tenant_id
                == tenant_id
            )
            .all()
        )

        total = sum(
            receipt.amount_usd
            for receipt in receipts
        )

        paid = sum(
            1
            for receipt in receipts
            if receipt.status == "paid"
        )

        pending = sum(
            1
            for receipt in receipts
            if receipt.status == "pending"
        )

        return {
            "total": total,
            "paid": paid,
            "pending": pending
        }

payment_receipt_repo = (
    PaymentReceiptRepository(
        PaymentReceipt
    )
)

