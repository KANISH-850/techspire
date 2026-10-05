from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.models.conversation import Conversation
from app.schemas.chatbot import ChatMessageRequest, ConversationResponse, ConversationCreate
from app.services.chatbot.chat_service import chat_service

router = APIRouter()

@router.post("/chat/stream")
def chat_stream(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    gen = chat_service.process_message_stream(db, request)
    return StreamingResponse(gen, media_type="text/plain")

@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(Conversation).order_by(Conversation.updated_at.desc()).all()

@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    conv_in: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    conv = Conversation(title=conv_in.title or "New Chat")
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv
