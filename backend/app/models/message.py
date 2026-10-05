import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.conversation import Conversation

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"), index=True)
    role: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="sent")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")
