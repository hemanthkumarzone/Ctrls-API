"""Budgets controller."""

from typing import Any

from fastapi import APIRouter, Body, status

budgets_controller = APIRouter(prefix="/budgets", tags=["Budgets"])


@budgets_controller.get("")
def get_budgets() -> list[dict[str, Any]]:
    return [{"name": "Compute Budget", "limit": 130000, "spent": 120000, "forecast": 135000, "status": "At Risk", "owner": "Platform Engineering"}]


@budgets_controller.get("/{budget_id}")
def get_budget(budget_id: str) -> dict[str, Any]:
    return {"id": budget_id, "name": "Compute Budget", "limit": 130000, "spent": 120000, "forecast": 135000, "status": "At Risk", "owner": "Platform Engineering"}


@budgets_controller.post("/create", status_code=status.HTTP_201_CREATED)
def create_budget(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return {"id": "bgt-1711361400000", "message": "Budget created."}


@budgets_controller.put("/{budget_id}/update")
def update_budget(budget_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return {"id": budget_id, "limit": payload.get("limit", 140000), "updated": True}


@budgets_controller.delete("/{budget_id}")
def delete_budget(budget_id: str) -> dict[str, Any]:
    return {"message": f"Budget {budget_id} deleted."}


@budgets_controller.get("/status")
def get_budget_status() -> list[dict[str, Any]]:
    return [{"name": "Compute Budget", "status": "At Risk"}, {"name": "K8s Budget", "status": "Exceeded"}]


@budgets_controller.get("/daily-burn-rate")
def get_budget_daily_burn_rate() -> list[dict[str, Any]]:
    return [{"name": "Compute Budget", "dailyBurnRate": "4000.00"}]


@budgets_controller.post("/{budget_id}/alerts", status_code=status.HTTP_201_CREATED)
def create_budget_alert(budget_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return {"message": f"Alert set for budget {budget_id}."}


@budgets_controller.get("/sample")
def sample_budgets():
    return {
        'data': [],
        'msg': "Budgets fetched successfully"
    }

