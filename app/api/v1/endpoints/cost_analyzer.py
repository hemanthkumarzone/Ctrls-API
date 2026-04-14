"""
Cost Analyzer endpoints.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api import deps
from decimal import Decimal
from datetime import datetime

router = APIRouter()


@router.get("/services")
async def get_services(db: Session = Depends(deps.get_db)):
    """Get all services by cost."""
    return [
        {
            "name": "EC2 Instances",
            "provider": "AWS",
            "cost": Decimal("68500"),
            "usage": "1,240 vCPU-hours",
            "trend": Decimal("12.3"),
        },
        {
            "name": "RDS Database",
            "provider": "AWS",
            "cost": Decimal("42300"),
            "usage": "2.5 TB storage",
            "trend": Decimal("-1.2"),
        },
        {
            "name": "GKE Clusters",
            "provider": "GCP",
            "cost": Decimal("34200"),
            "usage": "8 clusters",
            "trend": Decimal("22.1"),
        },
        {
            "name": "Azure VMs",
            "provider": "Azure",
            "cost": Decimal("28400"),
            "usage": "512 vCPU-hours",
            "trend": Decimal("5.7"),
        },
    ]


@router.get("/services/filter")
async def filter_services(
    provider: str = Query(None),
    min_cost: Decimal = Query(None),
    db: Session = Depends(deps.get_db),
):
    """Filter services by provider and cost."""
    services = [
        {
            "name": "EC2 Instances",
            "provider": "AWS",
            "cost": Decimal("68500"),
            "usage": "1,240 vCPU-hours",
            "trend": Decimal("12.3"),
        },
        {
            "name": "RDS Database",
            "provider": "AWS",
            "cost": Decimal("42300"),
            "usage": "2.5 TB storage",
            "trend": Decimal("-1.2"),
        },
    ]
    if provider:
        services = [s for s in services if s["provider"] == provider]
    if min_cost:
        services = [s for s in services if s["cost"] >= min_cost]
    return services


@router.get("/services/{service_id}")
async def get_service(service_id: str, db: Session = Depends(deps.get_db)):
    """Get specific service details."""
    return {
        "name": "EC2 Instances",
        "provider": "AWS",
        "cost": Decimal("68500"),
        "usage": "1,240 vCPU-hours",
        "trend": Decimal("12.3"),
    }


@router.get("/cost-by-provider")
async def get_cost_by_provider(db: Session = Depends(deps.get_db)):
    """Get cost breakdown by cloud provider."""
    return [
        {"provider": "AWS", "cost": Decimal("125700")},
        {"provider": "GCP", "cost": Decimal("93400")},
        {"provider": "Azure", "cost": Decimal("65650")},
    ]


@router.get("/cost-by-category")
async def get_cost_by_category(db: Session = Depends(deps.get_db)):
    """Get cost by resource category."""
    return [
        {"name": "Compute", "value": Decimal("120000"), "change": Decimal("8.2")},
        {"name": "Storage", "value": Decimal("54000"), "change": Decimal("-3.1")},
        {"name": "Network", "value": Decimal("38000"), "change": Decimal("5.5")},
        {"name": "Kubernetes", "value": Decimal("47000"), "change": Decimal("12.3")},
        {"name": "Database", "value": Decimal("25750"), "change": Decimal("-2.1")},
    ]


@router.get("/usage-metrics")
async def get_usage_metrics(db: Session = Depends(deps.get_db)):
    """Get usage metrics for services."""
    return [
        {
            "name": "EC2 Instances",
            "usage": "1,240 vCPU-hours",
            "cost": Decimal("68500"),
        },
        {
            "name": "RDS Database",
            "usage": "2.5 TB storage",
            "cost": Decimal("42300"),
        },
    ]


@router.get("/services/export")
async def export_services(db: Session = Depends(deps.get_db)):
    """Export services to CSV."""
    return {
        "download_url": "/exports/services_export.csv",
        "generated_at": datetime.now().isoformat() + "Z",
    }


@router.get("/provider-comparison")
async def get_provider_comparison(db: Session = Depends(deps.get_db)):
    """Compare costs across providers."""
    return [
        {
            "provider": "AWS",
            "services": [
                {
                    "name": "EC2 Instances",
                    "cost": Decimal("68500"),
                }
            ],
        },
        {
            "provider": "GCP",
            "services": [
                {
                    "name": "GKE Clusters",
                    "cost": Decimal("34200"),
                }
            ],
        },
        {
            "provider": "Azure",
            "services": [
                {
                    "name": "Azure VMs",
                    "cost": Decimal("28400"),
                }
            ],
        },
    ]
