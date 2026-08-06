from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.modules.chatbot.models.conversation import Conversation
from app.modules.chatbot.repositories.base import CRUDBase
from app.modules.chatbot.schemas.conversation import ConversationBase, ConversationCreate


class CRUDConversation(CRUDBase[Conversation, ConversationCreate, ConversationBase]):
    def get_by_user(
        self, db: Session, *, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """
        Retrieve all conversations for a specific user.
        """
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())

    def get_with_messages(self, db: Session, *, id: str) -> Optional[Conversation]:
        """
        Retrieve a conversation with all its associated messages preloaded.
        """
        stmt = (
            select(self.model)
            .options(selectinload(self.model.messages))
            .where(self.model.id == id)
        )
        return db.execute(stmt).scalar_one_or_none()


conversation_repo = CRUDConversation(Conversation)
