"""
Budget endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas
from decimal import Decimal

router = APIRouter()


@router.get("/")
async def get_budgets(db: Session = Depends(deps.get_db)):
    """Get all budgets."""
    return [
        {
            "name": "Compute Budget",
            "limit": Decimal("130000"),
            "spent": Decimal("120000"),
            "forecast": Decimal("135000"),
            "status": "At Risk",
            "owner": "Platform Engineering",
        },
        {
            "name": "K8s Budget",
            "limit": Decimal("100000"),
            "spent": Decimal("95000"),
            "forecast": Decimal("102000"),
            "status": "At Risk",
            "owner": "DevOps",
        },
    ]


@router.get("/{budget_id}")
async def get_budget(budget_id: str, db: Session = Depends(deps.get_db)):
    """Get specific budget."""
    return {
        "name": "Compute Budget",
        "limit": Decimal("130000"),
        "spent": Decimal("120000"),
        "forecast": Decimal("135000"),
        "status": "At Risk",
        "owner": "Platform Engineering",
    }


@router.post("/create")
async def create_budget(
    budget: schemas.BudgetCreate, db: Session = Depends(deps.get_db)
):
    """Create budget."""
    return {
        "id": "bgt-1711361400000",
        "message": "Budget created.",
    }


@router.put("/{budget_id}/update")
async def update_budget(
    budget_id: str,
    budget_update: schemas.BudgetUpdate,
    db: Session = Depends(deps.get_db),
):
    """Update budget."""
    return {
        "name": "Compute Budget",
        "limit": budget_update.limit or Decimal("130000"),
        "updated": True,
    }


@router.delete("/{budget_id}")
async def delete_budget(budget_id: str, db: Session = Depends(deps.get_db)):
    """Delete budget."""
    return {"message": f"Budget {budget_id} deleted."}


@router.get("/status")
async def get_budget_status(db: Session = Depends(deps.get_db)):
    """Get budget status."""
    return [
        {
            "name": "Compute Budget",
            "status": "At Risk",
        },
        {
            "name": "K8s Budget",
            "status": "Exceeded",
        },
    ]


@router.get("/daily-burn-rate")
async def get_daily_burn_rate(db: Session = Depends(deps.get_db)):
    """Get daily burn rate."""
    return [
        {
            "name": "Compute Budget",
            "daily_burn_rate": "4000.00",
        },
        {
            "name": "K8s Budget",
            "daily_burn_rate": "3200.00",
        },
    ]


@router.post("/{budget_id}/alerts")
async def set_budget_alerts(
    budget_id: str,
    alert_settings: schemas.BudgetAlertSettings,
    db: Session = Depends(deps.get_db),
):
    """Set budget alert thresholds."""
    return {
        "message": f"Alert set for budget {budget_id}.",
    }
