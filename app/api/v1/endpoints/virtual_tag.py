"""
Virtual Tag endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app import schemas

router = APIRouter()


@router.get("/")
async def get_virtual_tags(db: Session = Depends(deps.get_db)):
    """Get all virtual tags."""
    return [
        {
            "provider": "AWS",
            "raw_key": "aws:createdBy",
            "raw_value": "team-platform",
            "normalized_key": "team",
            "normalized_value": "Platform Engineering",
        },
        {
            "provider": "GCP",
            "raw_key": "env",
            "raw_value": "staging",
            "normalized_key": "environment",
            "normalized_value": "Staging",
        },
    ]


@router.get("/coverage")
async def get_tag_coverage(db: Session = Depends(deps.get_db)):
    """Get tag coverage statistics."""
    return {
        "covered": 8,
        "total": 12,
        "percentage": 67,
    }


@router.post("/rules/create")
async def create_tag_rule(
    rule: schemas.TagRuleCreate, db: Session = Depends(deps.get_db)
):
    """Create tag rule."""
    return {
        "id": "rule-1711361400000",
        "message": "Tag rule created.",
    }


@router.put("/rules/{rule_id}/update")
async def update_tag_rule(
    rule_id: str,
    rule_update: schemas.TagRuleUpdate,
    db: Session = Depends(deps.get_db),
):
    """Update tag rule."""
    return {
        "id": rule_id,
        "message": "Rule updated.",
    }


@router.delete("/rules/{rule_id}")
async def delete_tag_rule(rule_id: str, db: Session = Depends(deps.get_db)):
    """Delete tag rule."""
    return {"message": f"Rule {rule_id} deleted."}


@router.get("/mappings")
async def get_tag_mappings(db: Session = Depends(deps.get_db)):
    """Get tag mappings."""
    return [
        {
            "from": "AWS:aws:createdBy=team-platform",
            "to": "team=Platform Engineering",
        },
        {
            "from": "GCP:labels.env=dev",
            "to": "environment=Development",
        },
    ]


@router.post("/mappings/create")
async def create_tag_mapping(
    mapping: schemas.TagMappingCreate, db: Session = Depends(deps.get_db)
):
    """Create tag mapping."""
    return {
        "id": "map-1711361400000",
        "message": "Tag mapping created.",
    }
