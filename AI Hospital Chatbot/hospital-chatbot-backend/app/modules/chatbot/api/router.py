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



from app.modules.chatbot.schemas.conversation import ConversationBase

@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    conversation_in: ConversationBase, 
    db: Session = Depends(get_db)
):
    """
    Create a new anonymous conversation.
    """
    create_data = ConversationCreate(
        title=conversation_in.title, 
        status=conversation_in.status,
        session_id=conversation_in.session_id
    )
    conversation = conversation_repo.create(db, obj_in=create_data)
    return conversation


@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all conversations for an anonymous session.
    """
    return conversation_repo.get_by_session_id(db, session_id=session_id)

from fastapi.responses import StreamingResponse

@router.post(
    "/chat", status_code=status.HTTP_200_OK
)
def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db),
    ai_provider: BaseAIProvider = Depends(get_ai_provider)
):
    """
    Send a message to the AI chatbot within a specific conversation.
    Returns a stream of text.
    """
    try:
        # Verify conversation exists
        conversation = conversation_repo.get(db, id=request.conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
            
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


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
    conversation_id: str, 
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific conversation along with its full history of messages.
    """
    conversation = conversation_repo.get_with_messages(db, id=conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )
    return conversation

