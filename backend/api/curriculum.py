"""
HARV SHIPPED - Curriculum API
Steel2 curriculum generation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..app.database import get_db
from ..app.models import Module
from ..app.auth import get_current_user, require_admin, User

router = APIRouter()


class GenerateWeekRequest(BaseModel):
    week_number: int
    use_patterns: bool = False


@router.post("/generate")
async def generate_week(
    request: GenerateWeekRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Generate a single week of curriculum using Steel2."""
    # TODO: Integrate with Steel2 generator
    return {
        "status": "pending",
        "week": request.week_number,
        "message": "Steel2 generator integration pending"
    }


@router.get("/weeks")
async def list_weeks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all curriculum weeks/modules."""
    modules = db.query(Module).order_by(Module.week_number).all()
    return {
        "total": len(modules),
        "weeks": [
            {
                "week_number": m.week_number,
                "title": m.title,
                "grammar_focus": m.grammar_focus,
                "is_published": m.is_published,
                "quality_score": m.quality_score
            }
            for m in modules
        ]
    }


@router.get("/week/{week_number}")
async def get_week(
    week_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information for a specific week."""
    module = db.query(Module).filter(Module.week_number == week_number).first()

    if not module:
        raise HTTPException(status_code=404, detail="Week not found")

    return {
        "week_number": module.week_number,
        "title": module.title,
        "description": module.description,
        "grammar_focus": module.grammar_focus,
        "virtue": module.virtue,
        "faith_phrase": module.faith_phrase,
        "learning_objectives": module.learning_objectives,
        "system_prompt": module.system_prompt,
        "module_prompt": module.module_prompt,
        "is_published": module.is_published,
        "quality_score": module.quality_score
    }
