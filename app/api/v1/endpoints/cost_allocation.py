"""
Cost Allocation endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas
from decimal import Decimal

router = APIRouter()


@router.get("/teams")
async def get_teams(db: Session = Depends(deps.get_db)):
    """Get all teams with allocated costs."""
    return [
        {
            "name": "Platform Engineering",
            "department": "Engineering",
            "allocated": Decimal("85000"),
            "actual": Decimal("92400"),
            "variance": Decimal("8.7"),
            "services": 18,
        },
        {
            "name": "Data Science",
            "department": "Engineering",
            "allocated": Decimal("50000"),
            "actual": Decimal("48300"),
            "variance": Decimal("-3.4"),
            "services": 12,
        },
    ]


@router.get("/teams/{team_id}")
async def get_team(team_id: str, db: Session = Depends(deps.get_db)):
    """Get specific team."""
    return {
        "name": "Platform Engineering",
        "department": "Engineering",
        "allocated": Decimal("85000"),
        "actual": Decimal("92400"),
        "variance": Decimal("8.7"),
        "services": 18,
    }


@router.get("/teams/{team_id}/breakdown")
async def get_team_breakdown(team_id: str, db: Session = Depends(deps.get_db)):
    """Get cost breakdown for team."""
    return {
        "team": "Platform Engineering",
        "breakdown": {
            "compute": Decimal("46200"),
            "storage": Decimal("18480"),
            "network": Decimal("13860"),
            "kubernetes": Decimal("9240"),
            "database": Decimal("4620"),
        },
    }


@router.post("/rules/create")
async def create_allocation_rule(
    rule: schemas.CostAllocationRule, db: Session = Depends(deps.get_db)
):
    """Create cost allocation rule."""
    return {
        "id": "alloc-rule-1711361400000",
        "message": "Allocation rule created.",
    }


@router.put("/rules/{rule_id}/update")
async def update_allocation_rule(
    rule_id: str,
    rule_update: dict,
    db: Session = Depends(deps.get_db),
):
    """Update allocation rule."""
    return {
        "id": rule_id,
        "message": "Rule updated.",
    }


@router.get("/treemap")
async def get_treemap_data(db: Session = Depends(deps.get_db)):
    """Get treemap data for cost allocation visualization."""
    return [
        {
            "name": "Platform Engineering",
            "value": Decimal("92400"),
            "department": "Engineering",
        },
        {
            "name": "Data Science",
            "value": Decimal("48300"),
            "department": "Engineering",
        },
    ]


@router.get("/chargeback")
async def get_chargeback(db: Session = Depends(deps.get_db)):
    """Get chargeback by team."""
    return [
        {
            "team": "Platform Engineering",
            "chargeback": Decimal("92400"),
        },
        {
            "team": "Data Science",
            "chargeback": Decimal("48300"),
        },
    ]


@router.get("/variance-analysis")
async def get_variance_analysis(db: Session = Depends(deps.get_db)):
    """Get variance analysis."""
    return [
        {
            "team": "Platform Engineering",
            "allocated": Decimal("85000"),
            "actual": Decimal("92400"),
            "variance": Decimal("8.7"),
        },
        {
            "team": "Data Science",
            "allocated": Decimal("50000"),
            "actual": Decimal("48300"),
            "variance": Decimal("-3.4"),
        },
    ]
