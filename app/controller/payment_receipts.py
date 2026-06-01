"""Payment receipts controller."""

from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status
)

from sqlalchemy.orm import Session

from app.api.deps import (
    get_db,
    get_current_active_user
)

from app import schemas
from fastapi.responses import FileResponse
from app.repositories.payment_receipt_repo import (
    payment_receipt_repo
)
payment_receipts_controller = APIRouter(prefix="/payment-receipts", tags=["Payment Receipts"])


@payment_receipts_controller.get("")
def get_payment_receipts(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(
        get_current_active_user
    )
):

    receipts = (
        payment_receipt_repo.get_by_tenant(
            db,
            current_user.tenant_id
        )
    )

    return receipts

@payment_receipts_controller.get("/vendor/{vendor}")
def get_payment_receipts_by_vendor(
    vendor: str,
    db: Session = Depends(get_db)
):

    receipts = (
        payment_receipt_repo.get_by_vendor(
            db,
            vendor
        )
    )

    return receipts

@payment_receipts_controller.get("/{receipt_id}")
def get_payment_receipt(
    receipt_id: str,
    db: Session = Depends(get_db)
):

    receipt = (
        payment_receipt_repo.get_by_id(
            db,
            receipt_id
        )
    )

    if not receipt:
        return {
            "success": False,
            "message": "Receipt not found"
        }

    return receipt




@payment_receipts_controller.get(
    "/{receipt_id}/download"
)
def download_payment_receipt(
    receipt_id: str,
    db: Session = Depends(get_db)
):

    receipt = (
        payment_receipt_repo.get_by_id(
            db,
            receipt_id
        )
    )

    if not receipt:
        return {
            "success": False,
            "message": "Receipt not found"
        }

    return FileResponse(
        path=receipt.download_url,
        filename=f"{receipt.invoice_number}.pdf",
        media_type="application/pdf"
    )

@payment_receipts_controller.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_payment_receipt(file: UploadFile = File(...)) -> dict[str, Any]:
    return {"id": "rcpt-1711361400000", "message": "Receipt uploaded."}


@payment_receipts_controller.get("/summary")
def get_payment_receipts_summary(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(
        get_current_active_user
    )
):

    return (
        payment_receipt_repo.get_summary(
            db,
            current_user.tenant_id
        )
    )