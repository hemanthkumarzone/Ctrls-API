"""
Ingestion endpoints for metrics and inference events.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.services.ingest_service import ingest_service
from app.models import Agent

router = APIRouter()


@router.post("/metrics", status_code=status.HTTP_201_CREATED)
def ingest_metrics(
    payload: schemas.MetricBatch,
    db: Session = Depends(deps.get_db),
    current_agent: Agent = Depends(deps.get_current_agent),
) -> dict:
    """Ingest a batch of metric samples from an agent."""
    try:
        created = ingest_service.ingest_metrics(db, current_agent, payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    return {"created": created}


@router.post("/inference", status_code=status.HTTP_201_CREATED)
def ingest_inference(
    payload: schemas.InferenceBatch,
    db: Session = Depends(deps.get_db),
    current_agent: Agent = Depends(deps.get_current_agent),
) -> dict:
    """Ingest a batch of inference request events from an agent."""
    try:
        created = ingest_service.ingest_inference(db, current_agent, payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    return {"created": created}
