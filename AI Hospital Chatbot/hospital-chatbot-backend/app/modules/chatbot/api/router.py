from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import check_database_connection, get_db
from app.modules.chatbot.repositories.conversation_repository import conversation_repo
from app.modules.chatbot.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.modules.chatbot.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ConversationWithMessages,
)
from app.services.ai import BaseAIProvider
from app.services.ai import get_ai_provider
from app.modules.chatbot.services.chat_service import chat_service

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Check the health of the Chatbot API and its dependencies (e.g., Database).
    """
    db_status = check_database_connection()
    return {
        "status": "healthy" if db_status else "degraded",
        "database": "connected" if db_status else "disconnected",
    }


from app.dependencies.auth import get_current_user
from app.modules.chatbot.models.user import User
from app.modules.chatbot.schemas.conversation import ConversationBase

@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    conversation_in: ConversationBase, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new conversation for a user.
    """
    create_data = ConversationCreate(title=conversation_in.title, status=conversation_in.status, user_id=current_user.id)
    conversation = conversation_repo.create(db, obj_in=create_data)
    return conversation


from fastapi.responses import StreamingResponse

@router.post(
    "/chat", status_code=status.HTTP_200_OK
)
def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    ai_provider: BaseAIProvider = Depends(get_ai_provider),
    current_user: User = Depends(get_current_user)
):
    """
    Send a message to the AI chatbot within a specific conversation.
    Returns a stream of text.
    """
    try:
        # Verify conversation belongs to user
        conversation = conversation_repo.get(db, id=request.conversation_id)
        if not conversation or conversation.user_id != current_user.id:
            raise ValueError("Conversation not found or access denied")
            
        generator = chat_service.process_message_stream(
            db=db, request=request, ai_provider_instance=ai_provider
        )
        return StreamingResponse(generator, media_type="text/plain")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the message.",
        )


@router.get("/conversations", response_model=List[ConversationResponse])
def get_user_conversations(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all conversations for the current authenticated user.
    """
    conversations = conversation_repo.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
    conversation_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific conversation along with its full history of messages.
    """
    conversation = conversation_repo.get_with_messages(db, id=conversation_id)
    if not conversation or conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )
    return conversation


@router.delete(
    "/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_conversation(
    conversation_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific conversation and all its associated messages.
    """
    conversation = conversation_repo.get(db, id=conversation_id)
    if not conversation or conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )
    conversation_repo.remove(db, id=conversation_id)
    return None
