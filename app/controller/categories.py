"""Categories controller."""

from typing import Any

from fastapi import APIRouter

categories_controller = APIRouter(prefix="/categories", tags=["Categories"])


@categories_controller.get("")
def get_categories() -> list[dict[str, Any]]:
    return [{"name": "Compute", "value": 120000, "change": 8.2}, {"name": "Storage", "value": 54000, "change": -3.1}]


@categories_controller.get("/{category_id}")
def get_category(category_id: str) -> dict[str, Any]:
    return {"name": "Compute", "value": 120000, "change": 8.2}


@categories_controller.get("/{category_id}/trend")
def get_category_trend(category_id: str) -> list[dict[str, Any]]:
    return [{"month": "Apr 2025", "value": 95000}, {"month": "Mar 2026", "value": 120000}]


@categories_controller.get("/{category_id}/services")
def get_category_services(category_id: str) -> list[dict[str, Any]]:
    return [{"name": "EC2 Instances", "provider": "AWS", "cost": 68500}]


@categories_controller.get("/{category_id}/mom-change")
def get_category_mom_change(category_id: str) -> dict[str, Any]:
    return {"category": "Compute", "change": 8.2}


@categories_controller.get("/{category_id}/export")
def export_category(category_id: str) -> dict[str, Any]:
    return {"downloadUrl": f"/exports/{category_id}_export.csv"}
