import logging
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIExplanationService:
    @staticmethod
    async def get_explanation(context: str, fallback: str) -> str:
        prompt = f"Analyze this hospital forecast context and provide a 2-sentence executive summary:\n{context}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                if resp.status_code == 200:
                    text = resp.json().get("response", "").strip()
                    if text:
                        return text
        except Exception as e:
            logger.debug(f"AI explanation call failed: {e}")

        return fallback
