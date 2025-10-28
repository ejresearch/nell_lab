"""
HARV SHIPPED - Tutoring API
AI Socratic tutoring endpoints (from Harv)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import json

from ..app.database import get_db
from ..app.models import Module, Conversation, User
from ..app.auth import get_current_user, hash_password, authenticate_user, create_access_token

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ChatRequest(BaseModel):
    module_id: int
    message: str
    conversation_id: int | None = None


@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register new student."""
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=request.email,
        name=request.name,
        hashed_password=hash_password(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})

    return {
        "user_id": user.id,
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login student."""
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {
        "user_id": user.id,
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/modules")
async def list_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all available teaching modules."""
    modules = db.query(Module).filter(Module.is_published == True).order_by(Module.week_number).all()

    return {
        "total": len(modules),
        "modules": [
            {
                "id": m.id,
                "week_number": m.week_number,
                "title": m.title,
                "description": m.description,
                "grammar_focus": m.grammar_focus
            }
            for m in modules
        ]
    }


@router.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with AI tutor for a specific module.

    TODO: Integrate with actual LLM and memory system.
    """
    # TODO: Implement actual chat with memory system

    return {
        "reply": "AI tutor integration pending. This will use Harv's Socratic teaching method.",
        "conversation_id": request.conversation_id or 1
    }
