from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# Message schemas
class MessageBase(BaseModel):
    role: str
    content: str
    status: str
    timestamp: datetime


class MessageResponse(MessageBase):
    id: str
    conversation_id: str

    model_config = ConfigDict(from_attributes=True)


# Conversation schemas
class ConversationBase(BaseModel):
    title: Optional[str] = None
    status: str = "active"


class ConversationCreate(ConversationBase):
    user_id: str


class ConversationResponse(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationWithMessages(ConversationResponse):
    messages: List[MessageResponse] = []
