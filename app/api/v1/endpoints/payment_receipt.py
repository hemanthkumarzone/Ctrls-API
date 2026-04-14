"""
Payment Receipt endpoints.
"""

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas
from decimal import Decimal
from datetime import datetime

router = APIRouter()


@router.get("/")
async def get_payment_receipts(db: Session = Depends(deps.get_db)):
    """Get all payment receipts."""
    return [
        {
            "id": "rcpt-1",
            "vendor": "AWS",
            "amount": Decimal("68500"),
            "currency": "USD",
            "date": "2026-03-01T00:00:00Z",
            "status": "paid",
            "invoice_number": "INV-AWS-2026-03",
            "description": "AWS Monthly Bill - March 2026",
            "category": "Compute",
            "download_url": "/receipts/rcpt-1.pdf",
        },
        {
            "id": "rcpt-2",
            "vendor": "GCP",
            "amount": Decimal("45200"),
            "currency": "USD",
            "date": "2026-03-01T00:00:00Z",
            "status": "paid",
            "invoice_number": "INV-GCP-2026-03",
            "description": "GCP Monthly Bill - March 2026",
            "category": "Compute",
            "download_url": "/receipts/rcpt-2.pdf",
        },
    ]


@router.get("/{receipt_id}")
async def get_payment_receipt(
    receipt_id: str, db: Session = Depends(deps.get_db)
):
    """Get specific receipt."""
    return {
        "id": receipt_id,
        "vendor": "AWS",
        "amount": Decimal("68500"),
        "currency": "USD",
        "date": "2026-03-01T00:00:00Z",
        "status": "paid",
        "invoice_number": "INV-AWS-2026-03",
        "description": "AWS Monthly Bill - March 2026",
        "category": "Compute",
    }


@router.get("/vendor/{vendor}")
async def get_receipts_by_vendor(
    vendor: str, db: Session = Depends(deps.get_db)
):
    """Get receipts from specific vendor."""
    return [
        {
            "id": "rcpt-1",
            "vendor": vendor,
            "amount": Decimal("68500"),
            "currency": "USD",
            "date": "2026-03-01T00:00:00Z",
            "status": "paid",
        },
    ]


@router.get("/{receipt_id}/download")
async def download_receipt(receipt_id: str, db: Session = Depends(deps.get_db)):
    """Download receipt."""
    return {"download_url": f"/receipts/{receipt_id}.pdf"}


@router.post("/upload")
async def upload_receipt(
    file: UploadFile = File(...), db: Session = Depends(deps.get_db)
):
    """Upload receipt file."""
    return {
        "id": "rcpt-1711361400000",
        "message": "Receipt uploaded.",
    }


@router.get("/summary")
async def get_receipts_summary(db: Session = Depends(deps.get_db)):
    """Get payment receipts summary."""
    return {
        "total": Decimal("237700"),
        "paid": 4,
        "pending": 1,
    }
