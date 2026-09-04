import httpx
from predictive_config import settings

class AIExplanationService:
    @staticmethod
    async def get_explanation(context: str, fallback_explanation: str) -> str:
        """
        Uses Ollama to generate an explanation based on prediction context.
        If Ollama is disabled or unavailable, returns the deterministic fallback explanation.
        """
        if not settings.OLLAMA_ENABLED:
            return fallback_explanation
            
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    f"{settings.OLLAMA_HOST}/api/generate",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "prompt": f"You are a hospital data analyst. Briefly explain this forecast in 1-2 sentences. Do not mention that you are an AI. Do not recalculate numbers.\n\nContext:\n{context}",
                        "stream": False
                    }
                )
                if response.status_code == 200:
                    return response.json().get("response", fallback_explanation).strip()
        except Exception:
            # Fallback if Ollama is unreachable
            pass
            
        return fallback_explanation
