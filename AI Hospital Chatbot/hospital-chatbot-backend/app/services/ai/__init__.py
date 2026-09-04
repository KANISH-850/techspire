from app.core.config import settings
from app.services.ai.base_provider import BaseAIProvider
from app.services.ai.openai_provider import OpenAIProvider
from app.services.ai.gemini_provider import GeminiProvider
from app.services.ai.ollama_provider import OllamaProvider
from app.services.ai.mock_provider import MockProvider

def get_ai_provider() -> BaseAIProvider:
    provider = settings.AI_PROVIDER.lower() if settings.AI_PROVIDER else "openai"
    
    if provider == "openai":
        return OpenAIProvider(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            model=settings.OPENAI_MODEL
        )
    elif provider == "gemini":
        return GeminiProvider(api_key=settings.GEMINI_API_KEY)
    elif provider == "ollama":
        return OllamaProvider(
            model=settings.OLLAMA_MODEL,
            host=settings.OLLAMA_BASE_URL
        )
    elif provider == "mock":
        from app.services.ai.mock_provider import MockProvider
        return MockProvider()
    else:
        return OpenAIProvider(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            model=settings.OPENAI_MODEL
        )
