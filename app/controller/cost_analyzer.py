"""Cost analyzer controller."""

from typing import Any

from fastapi import APIRouter, Query

cost_analyzer_controller = APIRouter(prefix="/cost-analyzer", tags=["Cost Analyzer"])


@cost_analyzer_controller.get("/services")
def get_services() -> list[dict[str, Any]]:
    return [
        {"name": "EC2 Instances", "provider": "AWS", "cost": 68500, "usage": "1,240 vCPU-hours", "trend": 12.3},
        {"name": "GKE Clusters", "provider": "GCP", "cost": 34200, "usage": "8 clusters", "trend": 22.1},
    ]


@cost_analyzer_controller.get("/services/filter")
def filter_services(
    provider: str | None = Query(None),
    minCost: int | None = Query(None),
) -> list[dict[str, Any]]:
    results = [
        {"name": "EC2 Instances", "provider": "AWS", "cost": 68500, "usage": "1,240 vCPU-hours", "trend": 12.3},
        {"name": "GKE Clusters", "provider": "GCP", "cost": 34200, "usage": "8 clusters", "trend": 22.1},
    ]
    if provider:
        results = [item for item in results if item["provider"] == provider]
    if minCost is not None:
        results = [item for item in results if item["cost"] >= minCost]
    return results


@cost_analyzer_controller.get("/services/{service_id}")
def get_service(service_id: str) -> dict[str, Any]:
    return {"name": "EC2 Instances", "provider": "AWS", "cost": 68500, "usage": "1,240 vCPU-hours", "trend": 12.3}


@cost_analyzer_controller.get("/cost-by-provider")
def get_cost_by_provider() -> list[dict[str, Any]]:
    return [
        {"provider": "AWS", "cost": 125700},
        {"provider": "GCP", "cost": 93400},
        {"provider": "Azure", "cost": 65650},
    ]


@cost_analyzer_controller.get("/cost-by-category")
def get_cost_by_category() -> list[dict[str, Any]]:
    return [
        {"name": "Compute", "value": 120000, "change": 8.2},
        {"name": "Storage", "value": 54000, "change": -3.1},
    ]


@cost_analyzer_controller.get("/usage-metrics")
def get_usage_metrics() -> list[dict[str, Any]]:
    return [{"name": "EC2 Instances", "usage": "1,240 vCPU-hours", "cost": 68500}]


@cost_analyzer_controller.get("/services/export")
def export_services() -> dict[str, Any]:
    return {"downloadUrl": "/exports/services_export.csv", "generatedAt": "2026-03-25T13:00:00.000Z"}


@cost_analyzer_controller.get("/provider-comparison")
def get_provider_comparison() -> list[dict[str, Any]]:
    return [
        {"provider": "AWS", "services": [{"name": "EC2 Instances", "cost": 68500}]},
        {"provider": "GCP", "services": [{"name": "GKE Clusters", "cost": 34200}]},
    ]
