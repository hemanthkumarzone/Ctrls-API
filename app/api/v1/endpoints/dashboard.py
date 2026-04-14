"""
Dashboard endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas
from decimal import Decimal
from datetime import datetime

router = APIRouter()


@router.get("/summary", response_model=schemas.DashboardSummary)
async def get_dashboard_summary(db: Session = Depends(deps.get_db)):
    """Get dashboard summary."""
    return {
        "total_spend": Decimal("284750.00"),
        "month_over_month_change": Decimal("12.4"),
        "forecasted_spend": Decimal("310000.00"),
        "budget_limit": Decimal("300000.00"),
        "savings_opportunity": Decimal("47200.00"),
        "anomalies_detected": 3,
    }


@router.get("/spend-trend")
async def get_spend_trend(db: Session = Depends(deps.get_db)):
    """Get spend trend by category."""
    return [
        {
            "month": "Apr 2025",
            "compute": Decimal("95000"),
            "storage": Decimal("48000"),
            "network": Decimal("30000"),
            "kubernetes": Decimal("35000"),
            "database": Decimal("22000"),
        },
        {
            "month": "Mar 2026",
            "compute": Decimal("120000"),
            "storage": Decimal("54000"),
            "network": Decimal("38000"),
            "kubernetes": Decimal("47000"),
            "database": Decimal("25750"),
        },
    ]


@router.get("/cost-by-category")
async def get_cost_by_category(db: Session = Depends(deps.get_db)):
    """Get cost breakdown by category."""
    return [
        {"name": "Compute", "value": Decimal("120000"), "change": Decimal("8.2")},
        {"name": "Storage", "value": Decimal("54000"), "change": Decimal("-3.1")},
        {"name": "Network", "value": Decimal("38000"), "change": Decimal("5.5")},
        {"name": "Kubernetes", "value": Decimal("47000"), "change": Decimal("12.3")},
        {"name": "Database", "value": Decimal("25750"), "change": Decimal("-2.1")},
    ]


@router.get("/top-services")
async def get_top_services(db: Session = Depends(deps.get_db)):
    """Get top services by cost."""
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
    ]


@router.get("/recommendations-widget")
async def get_recommendations_widget(db: Session = Depends(deps.get_db)):
    """Get top recommendations for dashboard widget."""
    return [
        {
            "id": "rec-1",
            "title": "Right-size EC2 instances in us-east-1",
            "category": "Compute",
            "impact": "High",
            "effort": "Low",
            "savings": Decimal("18500"),
            "status": "open",
        },
        {
            "id": "rec-2",
            "title": "Delete unused RDS snapshots",
            "category": "Storage",
            "impact": "Medium",
            "effort": "Low",
            "savings": Decimal("5200"),
            "status": "open",
        },
        {
            "id": "rec-3",
            "title": "Migrate to spot instances",
            "category": "Compute",
            "impact": "High",
            "effort": "High",
            "savings": Decimal("28500"),
            "status": "open",
        },
    ]


@router.get("/anomalies-widget")
async def get_anomalies_widget(db: Session = Depends(deps.get_db)):
    """Get recent anomalies for dashboard widget."""
    return [
        {
            "id": "anom-1",
            "service": "Lambda Functions",
            "detected_at": datetime.now().isoformat(),
            "severity": "Critical",
            "spike": Decimal("340"),
        },
        {
            "id": "anom-2",
            "service": "S3 Transfer",
            "detected_at": datetime.now().isoformat(),
            "severity": "High",
            "spike": Decimal("125"),
        },
    ]


@router.get("/reports-widget")
async def get_reports_widget(db: Session = Depends(deps.get_db)):
    """Get reports for dashboard widget."""
    return [
        {
            "name": "Weekly Cost Summary",
            "frequency": "Weekly",
            "recipients": ["cfo@company.com"],
            "lastRun": "2026-03-10T08:00:00Z",
            "format": "PDF",
        },
        {
            "name": "Monthly K8s Report",
            "frequency": "Monthly",
            "recipients": ["devops@company.com"],
            "lastRun": "2026-03-01T08:00:00Z",
            "format": "CSV",
        },
    ]


@router.post("/refresh")
async def refresh_dashboard(db: Session = Depends(deps.get_db)):
    """Refresh dashboard cache."""
    return {
        "message": "Dashboard data refreshed.",
        "timestamp": datetime.now().isoformat() + "Z",
    }
