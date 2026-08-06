from datetime import datetime

from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    """
    Schema for incoming chat messages from the user.
    """
    conversation_id: str = Field(
        ..., description="The ID of the conversation to add the message to"
    )
    message: str = Field(
        ..., min_length=1, description="The content of the message sent by the user"
    )


class ChatMessageResponse(BaseModel):
    """
    Schema for the chatbot's response.
    """
    message_id: str = Field(..., description="The ID of the generated message")
    conversation_id: str = Field(..., description="The ID of the conversation")
    role: str = Field(..., description="Role of the sender (e.g., 'assistant')")
    content: str = Field(..., description="The actual response text")
    timestamp: datetime = Field(..., description="Time the message was generated")
