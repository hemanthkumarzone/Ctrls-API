"""
Unit Economics endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from decimal import Decimal

router = APIRouter()


@router.get("/summary")
async def get_unit_economics_summary(db: Session = Depends(deps.get_db)):
    """Get unit economics summary."""
    return {
        "month": "Mar 2026",
        "cost_per_user": Decimal("2.78"),
        "cost_per_transaction": Decimal("0.0040"),
        "revenue": Decimal("1260000"),
        "margin": Decimal("71.8"),
    }


@router.get("/cost-per-user")
async def get_cost_per_user_trend(db: Session = Depends(deps.get_db)):
    """Get cost per user trend."""
    return [
        {"month": "Apr 2025", "value": Decimal("2.45")},
        {"month": "May 2025", "value": Decimal("2.52")},
        {"month": "Jun 2025", "value": Decimal("2.61")},
        {"month": "Mar 2026", "value": Decimal("2.78")},
    ]


@router.get("/cost-per-transaction")
async def get_cost_per_transaction_trend(db: Session = Depends(deps.get_db)):
    """Get cost per transaction trend."""
    return [
        {"month": "Apr 2025", "value": Decimal("0.0032")},
        {"month": "May 2025", "value": Decimal("0.0035")},
        {"month": "Jun 2025", "value": Decimal("0.0037")},
        {"month": "Mar 2026", "value": Decimal("0.0040")},
    ]


@router.get("/gross-margin")
async def get_gross_margin_trend(db: Session = Depends(deps.get_db)):
    """Get gross margin trend."""
    return [
        {"month": "Apr 2025", "margin": Decimal("74.2"), "revenue": Decimal("890000")},
        {"month": "May 2025", "margin": Decimal("73.5"), "revenue": Decimal("920000")},
        {"month": "Jun 2025", "margin": Decimal("72.8"), "revenue": Decimal("950000")},
        {"month": "Mar 2026", "margin": Decimal("71.8"), "revenue": Decimal("1260000")},
    ]


@router.get("/benchmark")
async def get_benchmark_comparison(db: Session = Depends(deps.get_db)):
    """Get benchmark comparison."""
    return {
        "industry": {
            "cost_per_user": Decimal("3.10"),
            "gross_margin": Decimal("72.0"),
        },
        "yours": {
            "cost_per_user": Decimal("2.78"),
            "gross_margin": Decimal("71.8"),
        },
    }


@router.get("/trends")
async def get_unit_economics_trends(db: Session = Depends(deps.get_db)):
    """Get full 12-month unit economics trend."""
    return [
        {
            "month": "Apr 2025",
            "cost_per_user": Decimal("2.45"),
            "cost_per_transaction": Decimal("0.0032"),
            "margin": Decimal("74.2"),
            "revenue": Decimal("890000"),
        },
        {
            "month": "May 2025",
            "cost_per_user": Decimal("2.52"),
            "cost_per_transaction": Decimal("0.0035"),
            "margin": Decimal("73.5"),
            "revenue": Decimal("920000"),
        },
    ]
