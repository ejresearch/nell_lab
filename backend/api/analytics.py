"""
HARV SHIPPED - Analytics API
Student performance and system analytics
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..app.database import get_db
from ..app.models import User, Module, Conversation, UserProgress
from ..app.auth import get_current_user, require_admin

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overall dashboard metrics."""
    total_students = db.query(User).filter(User.is_admin == False).count()
    total_modules = db.query(Module).filter(Module.is_published == True).count()
    total_conversations = db.query(Conversation).count()
    completed_modules = db.query(UserProgress).filter(UserProgress.completed == True).count()

    return {
        "students": total_students,
        "modules": total_modules,
        "conversations": total_conversations,
        "completions": completed_modules
    }


@router.get("/module/{module_id}")
async def get_module_analytics(
    module_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get analytics for a specific module."""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        return {"error": "Module not found"}

    progress_records = db.query(UserProgress).filter(UserProgress.module_id == module_id).all()

    completed = sum(1 for p in progress_records if p.completed)
    completion_rate = completed / len(progress_records) if progress_records else 0

    return {
        "module_id": module_id,
        "title": module.title,
        "students_enrolled": len(progress_records),
        "completions": completed,
        "completion_rate": round(completion_rate, 3)
    }


@router.get("/student/{user_id}")
async def get_student_analytics(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get analytics for a specific student."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()

    return {
        "user_id": user_id,
        "name": user.name,
        "modules_completed": sum(1 for p in progress if p.completed),
        "total_modules": len(progress)
    }
