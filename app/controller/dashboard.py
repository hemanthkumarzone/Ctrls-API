"""Dashboard controller."""

from typing import Any

from fastapi import APIRouter

dashboard_controller = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@dashboard_controller.get("/summary")
def get_dashboard_summary() -> dict[str, Any]:
    return {
        "totalSpend": 284750.00,
        "monthOverMonthChange": 12.4,
        "forecastedSpend": 310000.00,
        "budgetLimit": 300000.00,
        "savingsOpportunity": 47200.00,
        "anomaliesDetected": 3,
    }


@dashboard_controller.get("/spend-trend")
def get_spend_trend() -> list[dict[str, Any]]:
    return [
        {"month": "Apr 2025", "compute": 95000, "storage": 48000, "network": 30000, "kubernetes": 35000, "database": 22000},
        {"month": "Mar 2026", "compute": 120000, "storage": 54000, "network": 38000, "kubernetes": 47000, "database": 25750},
    ]


@dashboard_controller.get("/cost-by-category")
def get_cost_by_category() -> list[dict[str, Any]]:
    return [
        {"name": "Compute", "value": 120000, "change": 8.2},
        {"name": "Storage", "value": 54000, "change": -3.1},
    ]


@dashboard_controller.get("/top-services")
def get_top_services() -> list[dict[str, Any]]:
    return [
        {"name": "EC2 Instances", "provider": "AWS", "cost": 68500, "usage": "1,240 vCPU-hours", "trend": 12.3},
    ]


@dashboard_controller.get("/recommendations-widget")
def get_recommendations_widget() -> list[dict[str, Any]]:
    return [
        {"id": "rec-1", "title": "Right-size EC2 instances in us-east-1", "category": "Compute", "impact": "High", "effort": "Low", "savings": 18500, "status": "open"},
        {"id": "rec-2", "title": "Resize GKE nodes", "category": "Kubernetes", "impact": "Medium", "effort": "Medium", "savings": 9200, "status": "open"},
        {"id": "rec-3", "title": "Archive unused snapshots", "category": "Storage", "impact": "Low", "effort": "Low", "savings": 4700, "status": "open"},
    ]


@dashboard_controller.get("/anomalies-widget")
def get_anomalies_widget() -> list[dict[str, Any]]:
    return [
        {"id": "anom-1", "service": "Lambda Functions", "detectedAt": "2026-03-12T14:32:00Z", "severity": "Critical", "spike": 340},
        {"id": "anom-2", "service": "S3 Storage", "detectedAt": "2026-03-18T10:10:00Z", "severity": "High", "spike": 120},
        {"id": "anom-3", "service": "RDS Instances", "detectedAt": "2026-03-20T09:22:00Z", "severity": "Medium", "spike": 65},
    ]


@dashboard_controller.get("/reports-widget")
def get_reports_widget() -> list[dict[str, Any]]:
    return [
        {"name": "Weekly Cost Summary", "frequency": "Weekly", "recipients": ["cfo@company.com"], "lastRun": "2026-03-10T08:00:00Z", "format": "PDF"},
    ]


@dashboard_controller.post("/refresh")
def refresh_dashboard() -> dict[str, Any]:
    return {"message": "Dashboard data refreshed.", "timestamp": "2026-03-25T13:00:00.000Z"}


@dashboard_controller.get("/sample")
def sample_dashboard():
    return {
        'data': [],
        'msg': "Dashboard data fetched successfully"
    }

