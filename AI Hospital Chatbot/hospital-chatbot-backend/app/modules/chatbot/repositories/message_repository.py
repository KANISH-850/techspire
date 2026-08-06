from typing import List

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.chatbot.models.message import Message
from app.modules.chatbot.repositories.base import CRUDBase


class MessageCreateInternal(BaseModel):
    conversation_id: str
    role: str
    content: str
    status: str = "sent"


class CRUDMessage(CRUDBase[Message, MessageCreateInternal, BaseModel]):
    def get_by_conversation(
        self, db: Session, *, conversation_id: str, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """
        Retrieve all messages for a specific conversation, ordered by timestamp.
        """
        stmt = (
            select(self.model)
            .where(self.model.conversation_id == conversation_id)
            .order_by(self.model.timestamp.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())


message_repo = CRUDMessage(Message)
