"""
Main API router that includes all endpoint routers.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    health,
    jobs,
    cost,
    users,
    tenants,
    cloud_accounts,
    k8s,
    accelerators,
    agents,
    metrics,
    dashboard,
    cost_analyzer,
    category,
    recommendation,
    anomaly,
    report,
    virtual_tag,
    cost_allocation,
    unit_economics,
    forecasting,
    budget,
    payment_receipt,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(cloud_accounts.router, prefix="/cloud-accounts", tags=["cloud-accounts"])
api_router.include_router(k8s.router, prefix="/k8s", tags=["k8s"])
api_router.include_router(accelerators.router, prefix="/accelerators", tags=["accelerators"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(cost.router, prefix="/cost", tags=["cost"])

# New routers for FinOps modules
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(cost_analyzer.router, prefix="/cost-analyzer", tags=["cost_analyzer"])
api_router.include_router(category.router, prefix="/categories", tags=["categories"])
api_router.include_router(recommendation.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(anomaly.router, prefix="/anomalies", tags=["anomalies"])
api_router.include_router(report.router, prefix="/reports", tags=["reports"])
api_router.include_router(virtual_tag.router, prefix="/virtual-tags", tags=["virtual_tags"])
api_router.include_router(cost_allocation.router, prefix="/cost-allocation", tags=["cost_allocation"])
api_router.include_router(unit_economics.router, prefix="/unit-economics", tags=["unit_economics"])
api_router.include_router(forecasting.router, prefix="/forecasting", tags=["forecasting"])
api_router.include_router(budget.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(payment_receipt.router, prefix="/payment-receipts", tags=["payment_receipts"])