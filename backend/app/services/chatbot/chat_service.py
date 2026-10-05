import logging
import string
import uuid
from typing import Generator
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.patient import Patient
from app.models.department import Department
from app.models.appointment import Appointment
from app.schemas.chatbot import ChatMessageRequest
from app.services.chatbot.prompt_service import prompt_service
from app.services.ai.factory import get_ai_provider

logger = logging.getLogger(__name__)

class ChatService:
    @staticmethod
    def process_message_stream(
        db: Session,
        request: ChatMessageRequest
    ) -> Generator[str, None, None]:
        # 1. Verify conversation
        conv = db.query(Conversation).filter(Conversation.id == request.conversation_id).first()
        if not conv:
            conv = Conversation(id=request.conversation_id, title="Hospital Inquiry")
            db.add(conv)
            db.commit()

        # 2. Save user message
        user_msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conv.id,
            role="user",
            content=request.message,
            status="sent"
        )
        db.add(user_msg)
        db.commit()

        # Update title if first message
        msg_count = db.query(Message).filter(Message.conversation_id == conv.id).count()
        if msg_count <= 1:
            conv.title = request.message[:30] + ("..." if len(request.message) > 30 else "")
            db.commit()

        # 3. Check for HMS Navigation Intents
        msg_lower = request.message.lower().strip()
        nav_routes = {
            "dashboard": ("/", "Executive Dashboard"),
            "predictive": ("/predictive-analytics", "Predictive AI Analytics"),
            "forecast": ("/predictive-analytics", "Predictive AI Analytics"),
            "report": ("/reports", "AI Report Builder"),
            "procurement": ("/procurement", "AI Procurement"),
            "inventory": ("/procurement", "AI Procurement & Inventory"),
            "chatbot": ("/chatbot", "AI Chatbot")
        }

        if any(k in msg_lower for k in ["open ", "show ", "go to ", "navigate ", "view "]):
            for keyword, (route, name) in nav_routes.items():
                if keyword in msg_lower:
                    nav_reply = f"Opening **{name}** module for you...\n\n[NAVIGATE:{route}]"
                    assistant_msg = Message(
                        id=str(uuid.uuid4()),
                        conversation_id=conv.id,
                        role="assistant",
                        content=nav_reply,
                        status="sent"
                    )
                    db.add(assistant_msg)
                    db.commit()

                    def nav_gen():
                        yield nav_reply

                    return nav_gen()

        # 4. Fetch DB patient/appointment context if applicable
        db_context = ""
        try:
            words = request.message.split()
            possible_names = []
            for i in range(len(words)):
                possible_names.append(words[i].strip(string.punctuation))
                if i < len(words) - 1:
                    possible_names.append(f"{words[i]} {words[i+1]}".strip(string.punctuation))

            possible_names = [n for n in possible_names if len(n) > 2]
            if possible_names:
                found_patient = db.query(Patient).filter(
                    or_(*[Patient.name.ilike(f"%{n}%") for n in possible_names])
                ).first()

                if found_patient:
                    dept_name = found_patient.department.name if found_patient.department else "General"
                    db_context += f"PATIENT RECORD FOUND:\nName: {found_patient.name}\nAge: {found_patient.age}\nGender: {found_patient.gender}\nStatus: {found_patient.status}\nDepartment: {dept_name}\n\n"

                    appts = db.query(Appointment).filter(Appointment.patient_id == found_patient.id).all()
                    if appts:
                        db_context += "APPOINTMENTS:\n"
                        for a in appts:
                            d_name = a.department.name if a.department else "General"
                            db_context += f"- Date: {a.appointment_date.strftime('%Y-%m-%d %H:%M')}, Dept: {d_name}, Status: {a.status}\n"
        except Exception as e:
            logger.error(f"Error building DB context: {e}")

        # 5. Fetch RAG context if retriever is available
        rag_context = ""
        try:
            from rag.retriever import Retriever
            retriever = Retriever()
            docs = retriever.retrieve_relevant_documents(request.message)
            rag_context = "\n\n".join([d.get("text", "") for d in docs])
        except Exception as e:
            logger.debug(f"RAG retriever not active or empty: {e}")

        full_context = (rag_context + "\n" + db_context).strip()
        system_prompt = prompt_service.get_system_prompt(full_context or "No specific patient or document context provided.")

        history_msgs = db.query(Message).filter(Message.conversation_id == conv.id).order_by(Message.timestamp.asc()).all()
        messages_payload = [{"role": "system", "content": system_prompt}]
        for m in history_msgs[-10:]:
            messages_payload.append({"role": m.role, "content": m.content})

        provider = get_ai_provider()

        def generate_stream():
            full_content = ""
            status = "sent"
            try:
                if hasattr(provider, "generate_stream"):
                    for chunk in provider.generate_stream(messages_payload):
                        full_content += chunk
                        yield chunk
                else:
                    response_text = provider.generate_insights({"message": request.message}).get("summary", "")
                    full_content = response_text
                    yield response_text
            except Exception as e:
                logger.error(f"Error streaming response: {e}")
                err_text = f"I am operating in fallback mode. Response completed. ({e})"
                full_content += err_text
                yield err_text
                status = "error"

            ai_msg = Message(
                id=str(uuid.uuid4()),
                conversation_id=conv.id,
                role="assistant",
                content=full_content or "No response generated.",
                status=status
            )
            db.add(ai_msg)
            db.commit()

        return generate_stream()

chat_service = ChatService()
