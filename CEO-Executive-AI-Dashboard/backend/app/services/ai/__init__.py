from .base_provider import BaseAIProvider
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider
from app.core.config import settings

def get_ai_provider() -> BaseAIProvider:
    if settings.OPENAI_API_KEY:
        return OpenAIProvider()
    elif settings.GEMINI_API_KEY:
        return GeminiProvider()
    else:
        # Fallback dummy provider if no keys are set
        class DummyProvider(BaseAIProvider):
            def generate_insights(self, data):
                return {
                    "executive_summary": "Please configure an AI provider API key in .env for insights.",
                    "hospital_status": "Unknown",
                    "key_insights": ["No API Key detected."],
                    "risks": [{"title": "No API Key", "severity": "MEDIUM", "description": "AI functionality is disabled without an API key."}],
                    "recommendations": [{"priority": "HIGH", "recommendation": "Add GEMINI_API_KEY or OPENAI_API_KEY to .env", "reason": "To enable AI insights.", "expected_impact": "Full AI functionality."}]
                }
        return DummyProvider()
