from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ChatMessageRequest(BaseModel):
    conversation_id: str
    message: str

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"

class MessageResponseSchema(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: str
    session_id: Optional[str] = None
    title: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponseSchema] = []

    class Config:
        from_attributes = True

class ChatMessageResponse(BaseModel):
    conversation_id: str
    user_message: MessageResponseSchema
    assistant_message: MessageResponseSchema
