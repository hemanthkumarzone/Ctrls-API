"""
AI FinOps Platform - FastAPI Application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.controller import (
    auth_controller,
    dashboard_controller,
    recommendations_controller,
    anomalies_controller,
    kubernetes_controller,
    cost_allocation_controller,
    unit_economics_controller,
    budgets_controller,
    virtual_tags_controller,
    reports_controller,
    forecasting_controller,
    tenant_controller,
    user_operations_controller,

)
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import ExceptionHandlerMiddleware, RequestLoggingMiddleware, TenantMiddleware
from app.db.session import engine
from app.models import Base
from fastapi.routing import APIRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    setup_logging()
    # Create tables if they don't exist (in production, use migrations)
    if settings.ENVIRONMENT == "development":
        Base.metadata.create_all(bind=engine)

    yield

    # Shutdown
    # Close connections, etc.


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI FinOps Platform API",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

# Custom middleware
app.add_middleware(TenantMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ExceptionHandlerMiddleware)

# Routers
# app.include_router(api_router, prefix=settings.API_V1_STR, )

def create_app():
    """Create and configure the FastAPI application"""
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        raise
    
    # Register all routers
    app.include_router(anomalies_controller)
    app.include_router(auth_controller)
    app.include_router(cost_allocation_controller)
    app.include_router(dashboard_controller)
    app.include_router(forecasting_controller)
    app.include_router(kubernetes_controller)
    app.include_router(recommendations_controller)
    app.include_router(reports_controller)
    app.include_router(tenant_controller)
    app.include_router(unit_economics_controller)
    app.include_router(budgets_controller)
    app.include_router(user_operations_controller)
    app.include_router(virtual_tags_controller)
   
    
    
    return app

create_app()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.VERSION}