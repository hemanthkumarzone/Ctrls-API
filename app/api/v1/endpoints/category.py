"""
Category endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from decimal import Decimal
from datetime import datetime

router = APIRouter()


@router.get("/")
async def get_categories(db: Session = Depends(deps.get_db)):
    """Get all cost categories."""
    return [
        {"name": "Compute", "value": Decimal("120000"), "change": Decimal("8.2")},
        {"name": "Storage", "value": Decimal("54000"), "change": Decimal("-3.1")},
        {"name": "Network", "value": Decimal("38000"), "change": Decimal("5.5")},
        {"name": "Kubernetes", "value": Decimal("47000"), "change": Decimal("12.3")},
        {"name": "Database", "value": Decimal("25750"), "change": Decimal("-2.1")},
    ]


@router.get("/{category_id}")
async def get_category(category_id: str, db: Session = Depends(deps.get_db)):
    """Get specific category."""
    categories = {
        "compute": {"name": "Compute", "value": Decimal("120000"), "change": Decimal("8.2")},
        "storage": {"name": "Storage", "value": Decimal("54000"), "change": Decimal("-3.1")},
        "network": {"name": "Network", "value": Decimal("38000"), "change": Decimal("5.5")},
        "kubernetes": {"name": "Kubernetes", "value": Decimal("47000"), "change": Decimal("12.3")},
        "database": {"name": "Database", "value": Decimal("25750"), "change": Decimal("-2.1")},
    }
    return categories.get(category_id.lower(), {})


@router.get("/{category_id}/trend")
async def get_category_trend(category_id: str, db: Session = Depends(deps.get_db)):
    """Get trend for category."""
    return [
        {"month": "Apr 2025", "value": Decimal("95000")},
        {"month": "May 2025", "value": Decimal("101000")},
        {"month": "Jun 2025", "value": Decimal("110000")},
        {"month": "Mar 2026", "value": Decimal("120000")},
    ]


@router.get("/{category_id}/services")
async def get_category_services(category_id: str, db: Session = Depends(deps.get_db)):
    """Get services within category."""
    return [
        {
            "name": "EC2 Instances",
            "provider": "AWS",
            "cost": Decimal("68500"),
            "usage": "1,240 vCPU-hours",
            "trend": Decimal("12.3"),
        },
        {
            "name": "GKE Clusters",
            "provider": "GCP",
            "cost": Decimal("34200"),
            "usage": "8 clusters",
            "trend": Decimal("22.1"),
        },
    ]


@router.get("/{category_id}/mom-change")
async def get_category_mom_change(category_id: str, db: Session = Depends(deps.get_db)):
    """Get month-over-month change for category."""
    return {"category": "Compute", "change": Decimal("8.2")}


@router.get("/{category_id}/export")
async def export_category(category_id: str, db: Session = Depends(deps.get_db)):
    """Export category data to CSV."""
    return {"download_url": f"/exports/{category_id}_export.csv"}
