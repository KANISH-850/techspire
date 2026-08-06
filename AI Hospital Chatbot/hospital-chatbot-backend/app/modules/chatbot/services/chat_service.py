import logging
from sqlalchemy.orm import Session

from app.modules.chatbot.repositories.conversation_repository import conversation_repo
from app.modules.chatbot.repositories.message_repository import message_repo
from app.modules.chatbot.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.modules.chatbot.services.prompt_service import prompt_service

logger = logging.getLogger(__name__)


class ChatService:
    def process_message_stream(
        self,
        db: Session,
        request: ChatMessageRequest,
        ai_provider_instance
    ):
        """
        Processes a user's chat message and returns a generator that yields the AI's response chunks.
        Saves the complete message to the database once the stream is finished.
        """
        # 1. Verify conversation exists
        conversation = conversation_repo.get(db, id=request.conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {request.conversation_id} not found.")

        # 2. Save user message
        message_repo.create(
            db,
            obj_in={
                "conversation_id": request.conversation_id,
                "role": "user",
                "content": request.message,
                "status": "sent",
            },
        )

        # 3. Retrieve conversation history
        history_msgs = message_repo.get_by_conversation(
            db, conversation_id=request.conversation_id, limit=20
        )

        # 4. Construct payload for AI provider
        system_prompt = prompt_service.get_system_prompt()
        messages_payload = [{"role": "system", "content": system_prompt}]
        for msg in history_msgs:
            messages_payload.append({"role": msg.role, "content": msg.content})

        # 5. Get stream generator
        def generate():
            full_content = ""
            status = "sent"
            try:
                stream = ai_provider_instance.generate_stream(messages_payload)
                for chunk in stream:
                    full_content += chunk
                    yield chunk
            except Exception as e:
                logger.error(f"AI Provider error: {e}")
                error_msg = f"Vanakammm (Error: {e})"
                full_content += error_msg
                yield error_msg
                status = "error"
            
            # 6. Save AI response
            message_repo.create(
                db,
                obj_in={
                    "conversation_id": request.conversation_id,
                    "role": "assistant",
                    "content": full_content,
                    "status": status,
                },
            )

        return generate()


chat_service = ChatService()
