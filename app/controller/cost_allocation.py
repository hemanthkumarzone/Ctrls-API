"""Cost allocation controller."""

from typing import Any

from fastapi import APIRouter, Body

cost_allocation_controller = APIRouter(prefix="/cost-allocation", tags=["Cost Allocation"])


@cost_allocation_controller.get("/teams")
def get_cost_allocation_teams() -> list[dict[str, Any]]:
    return [{"name": "Platform Engineering", "department": "Engineering", "allocated": 85000, "actual": 92400, "variance": 8.7, "services": 18}]


@cost_allocation_controller.get("/teams/{team_id}")
def get_team(team_id: str) -> dict[str, Any]:
    return {"team": "Platform Engineering", "department": "Engineering", "allocated": 85000, "actual": 92400, "variance": 8.7, "services": 18}


@cost_allocation_controller.get("/teams/{team_id}/breakdown")
def get_team_breakdown(team_id: str) -> dict[str, Any]:
    return {"team": "Platform Engineering", "breakdown": {"compute": 46200, "storage": 18480, "network": 13860, "kubernetes": 9240, "database": 4620}}


@cost_allocation_controller.post("/rules/create")
def create_allocation_rule(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return {"id": "alloc-rule-1711361400000", "message": "Allocation rule created."}


@cost_allocation_controller.put("/rules/{rule_id}/update")
def update_allocation_rule(rule_id: str, payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    return {"id": rule_id, "message": "Rule updated."}


@cost_allocation_controller.get("/treemap")
def get_treemap() -> list[dict[str, Any]]:
    return [{"name": "Platform Engineering", "value": 92400, "department": "Engineering"}]


@cost_allocation_controller.get("/chargeback")
def get_chargeback() -> list[dict[str, Any]]:
    return [{"team": "Platform Engineering", "chargeback": 92400}]


@cost_allocation_controller.get("/variance-analysis")
def get_variance_analysis() -> list[dict[str, Any]]:
    return [{"team": "Platform Engineering", "allocated": 85000, "actual": 92400, "variance": 8.7}]


@cost_allocation_controller.get("/sample")
def sample_cost_allocation():
    return {
        'data': [],
        'msg': "Cost allocation fetched successfully"
    }

