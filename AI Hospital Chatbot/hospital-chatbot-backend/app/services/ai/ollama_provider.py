from typing import List, Dict
from app.services.ai.base_provider import BaseAIProvider

class OllamaProvider(BaseAIProvider):
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        # Mock implementation for local Ollama
        user_message = messages[-1]["content"] if messages else ""
        return f"[Ollama] Responding to: {user_message}"
