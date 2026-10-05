import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List
from sqlalchemy import DateTime, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.message import Message

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    session_id: Mapped[str] = mapped_column(String, index=True, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    messages: Mapped[List["Message"]] = relationship(back_populates="conversation", cascade="all, delete-orphan")
