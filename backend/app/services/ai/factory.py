from app.core.config import settings
from app.services.ai.base_provider import BaseAIProvider
from app.services.ai.ollama_provider import OllamaProvider

def get_ai_provider() -> BaseAIProvider:
    provider_type = settings.AI_PROVIDER.lower()
    if provider_type == "ollama":
        return OllamaProvider()
    return OllamaProvider()
