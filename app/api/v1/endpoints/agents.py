"""
AI agent management endpoints.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models import User
from app.services.agent_service import agent_service

router = APIRouter()


@router.post("/register", response_model=schemas.AgentWithToken)
def register_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_in: schemas.AgentCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Register a new agent for the current tenant."""
    if current_user.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    try:
        agent, token = agent_service.register_agent(db, current_user, agent_in)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    agent_payload = schemas.AgentWithToken.model_validate(agent)
    agent_payload.auth_token = token
    return agent_payload


@router.post("/{agent_id}/heartbeat", response_model=schemas.Agent)
def heartbeat_agent(
    agent_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Record an agent heartbeat."""
    agent = agent_service.get_agent(db, agent_id)
    if not agent or agent.tenant_id != current_user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )

    agent = agent_service.update_heartbeat(db, agent)
    return agent


@router.get("/", response_model=List[schemas.Agent])
def list_agents(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """List agents for the current tenant."""
    if current_user.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return agent_service.list_agents(db, current_user.tenant_id)
