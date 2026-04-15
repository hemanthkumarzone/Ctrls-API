"""
Agent service for registration and heartbeat.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core import security
from app.models import Agent, User
from app.repositories.agent_repo import agent_repo
from app.schemas.agent import AgentCreate


class AgentService:
    """Agent service."""

    def register_agent(self, db: Session, current_user: User, agent_in: AgentCreate) -> tuple[Agent, str]:
        existing = agent_repo.get_by_tenant_and_name(
            db, current_user.tenant_id, agent_in.name
        )
        if existing:
            raise ValueError("Agent already exists")

        agent_data = agent_in.dict()
        agent_data["tenant_id"] = current_user.tenant_id
        agent = agent_repo.create(db, obj_in=agent_data)

        expires_delta = timedelta(minutes=settings.AGENT_TOKEN_EXPIRE_MINUTES)
        auth_token = security.create_access_token(
            subject=agent.id,
            expires_delta=expires_delta,
            extra_claims={
                "tenant_id": current_user.tenant_id,
                "type": "agent",
                "role": "agent",
            },
        )

        agent.auth_token_expires_at = datetime.utcnow() + expires_delta
        db.add(agent)
        db.commit()
        db.refresh(agent)

        return agent, auth_token

    def update_heartbeat(self, db: Session, agent: Agent) -> Agent:
        return agent_repo.update_last_seen(db, agent, datetime.utcnow())

    def get_agent(self, db: Session, agent_id: str) -> Agent | None:
        return agent_repo.get_by_id(db, agent_id)

    def list_agents(self, db: Session, tenant_id: str) -> list[Agent]:
        return agent_repo.get_by_tenant(db, tenant_id)


agent_service = AgentService()
