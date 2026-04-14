"""
Forecasting endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas
from decimal import Decimal

router = APIRouter()


@router.get("/forecast")
async def get_forecast(db: Session = Depends(deps.get_db)):
    """Get forecast scenarios."""
    return {
        "base": [
            {
                "month": "Apr 2026",
                "spend": Decimal("292000"),
                "lower": Decimal("285000"),
                "upper": Decimal("299000"),
            },
            {
                "month": "May 2026",
                "spend": Decimal("298000"),
                "lower": Decimal("290000"),
                "upper": Decimal("305000"),
            },
        ],
        "optimistic": [
            {
                "month": "Apr 2026",
                "spend": Decimal("278000"),
            },
        ],
        "pessimistic": [
            {
                "month": "Apr 2026",
                "spend": Decimal("308000"),
            },
        ],
    }


@router.get("/forecast/{scenario}")
async def get_forecast_scenario(
    scenario: str, db: Session = Depends(deps.get_db)
):
    """Get forecast for specific scenario."""
    scenarios = {
        "base": [
            {
                "month": "Apr 2026",
                "spend": Decimal("292000"),
                "lower": Decimal("285000"),
                "upper": Decimal("299000"),
            },
        ],
        "optimistic": [
            {
                "month": "Apr 2026",
                "spend": Decimal("278000"),
            },
        ],
        "pessimistic": [
            {
                "month": "Apr 2026",
                "spend": Decimal("308000"),
            },
        ],
    }
    return scenarios.get(scenario, [])


@router.post("/what-if")
async def what_if_analysis(
    analysis: schemas.WhatIfAssumptions, db: Session = Depends(deps.get_db)
):
    """Perform what-if analysis."""
    return {
        "scenario": "custom",
        "projected_spend": Decimal("295000"),
        "savings": Decimal("15000"),
    }


@router.get("/drivers")
async def get_cost_drivers(db: Session = Depends(deps.get_db)):
    """Get cost drivers for forecasting."""
    return [
        {
            "service": "GKE Clusters",
            "impact": Decimal("8200"),
            "direction": "up",
            "reason": "New ML workloads",
        },
        {
            "service": "Cost Optimization",
            "impact": Decimal("-5000"),
            "direction": "down",
            "reason": "Spot instance migration",
        },
    ]


@router.put("/drivers/{driver_id}/update")
async def update_cost_driver(
    driver_id: str,
    driver_update: schemas.CostDriverUpdate,
    db: Session = Depends(deps.get_db),
):
    """Update cost driver."""
    return {
        "id": driver_id,
        "message": "Driver updated.",
    }


@router.get("/accuracy")
async def get_forecast_accuracy(db: Session = Depends(deps.get_db)):
    """Get forecast model accuracy."""
    return {
        "mape": Decimal("4.2"),
        "rmse": Decimal("8900"),
        "last_evaluated": "2026-03-01",
    }


@router.get("/historical-accuracy")
async def get_historical_accuracy(db: Session = Depends(deps.get_db)):
    """Get historical forecast accuracy."""
    return [
        {
            "month": "Oct 2025",
            "spend": Decimal("262700"),
        },
        {
            "month": "Nov 2025",
            "spend": Decimal("273400"),
        },
        {
            "month": "Mar 2026",
            "spend": Decimal("284750"),
        },
    ]
