"""
Recommendation endpoints.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas
from decimal import Decimal

router = APIRouter()


@router.get("/")
async def get_recommendations(db: Session = Depends(deps.get_db)):
    """Get all recommendations."""
    return [
        {
            "id": "rec-1",
            "title": "Right-size EC2 instances in us-east-1",
            "category": "Compute",
            "impact": "High",
            "effort": "Low",
            "savings": Decimal("18500"),
            "status": "open",
            "steps": ["Identify underutilized instances", "Migrate to smaller types"],
        },
        {
            "id": "rec-2",
            "title": "Delete unused RDS snapshots",
            "category": "Storage",
            "impact": "Medium",
            "effort": "Low",
            "savings": Decimal("5200"),
            "status": "open",
            "steps": ["Identify old snapshots", "Delete snapshots"],
        },
    ]


@router.get("/{recommendation_id}")
async def get_recommendation(
    recommendation_id: str, db: Session = Depends(deps.get_db)
):
    """Get specific recommendation."""
    return {
        "id": recommendation_id,
        "title": "Right-size EC2 instances in us-east-1",
        "category": "Compute",
        "impact": "High",
        "effort": "Low",
        "savings": Decimal("18500"),
        "status": "open",
        "steps": ["Identify underutilized instances", "Migrate to smaller types"],
    }


@router.get("/filter")
async def filter_recommendations(
    category: str = Query(None),
    impact: str = Query(None),
    db: Session = Depends(deps.get_db),
):
    """Filter recommendations by category and impact."""
    recommendations = [
        {
            "id": "rec-1",
            "title": "Right-size EC2 instances in us-east-1",
            "category": "Compute",
            "impact": "High",
            "effort": "Low",
            "savings": Decimal("18500"),
            "status": "open",
        },
    ]
    if category:
        recommendations = [r for r in recommendations if r["category"] == category]
    if impact:
        recommendations = [r for r in recommendations if r["impact"] == impact]
    return recommendations


@router.get("/category/{category}")
async def get_recommendations_by_category(
    category: str, db: Session = Depends(deps.get_db)
):
    """Get recommendations filtered by category."""
    return [
        {
            "id": "rec-1",
            "title": "Right-size EC2 instances in us-east-1",
            "category": category,
            "impact": "High",
            "effort": "Low",
            "savings": Decimal("18500"),
            "status": "open",
        },
    ]


@router.put("/{recommendation_id}/status")
async def update_recommendation_status(
    recommendation_id: str,
    status_update: schemas.RecommendationUpdate,
    db: Session = Depends(deps.get_db),
):
    """Update recommendation status."""
    return {
        "id": recommendation_id,
        "status": status_update.status,
        "title": "Right-size EC2 instances in us-east-1",
        "category": "Compute",
        "impact": "High",
        "effort": "Low",
        "savings": Decimal("18500"),
    }


@router.post("/{recommendation_id}/apply")
async def apply_recommendation(
    recommendation_id: str, db: Session = Depends(deps.get_db)
):
    """Apply recommendation."""
    return {
        "message": "Recommendation applied successfully.",
        "steps": ["Step 1: Identify instances", "Step 2: Migrate instances"],
    }


@router.get("/{recommendation_id}/impact")
async def get_recommendation_impact(
    recommendation_id: str, db: Session = Depends(deps.get_db)
):
    """Get recommendation impact details."""
    return {
        "id": recommendation_id,
        "savings": Decimal("18500"),
        "impact": "High",
        "effort": "Low",
    }


@router.post("/{recommendation_id}/dismiss")
async def dismiss_recommendation(
    recommendation_id: str, db: Session = Depends(deps.get_db)
):
    """Dismiss recommendation."""
    return {"message": "Recommendation dismissed."}


@router.get("/savings-summary")
async def get_savings_summary(db: Session = Depends(deps.get_db)):
    """Get savings summary."""
    return {
        "total_savings": Decimal("49200"),
        "open": 4,
        "in_progress": 1,
        "done": 1,
    }
