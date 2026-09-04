import httpx
from report_config import settings

class AISummaryService:
    @staticmethod
    async def generate_summary(report_type: str, context: str, fallback_summary: str) -> str:
        if not settings.OLLAMA_ENABLED:
            return fallback_summary
            
        prompt = f"""You are an executive hospital analyst. Write a concise 2-3 sentence executive summary for a {report_type} report based strictly on these metrics. Do not calculate new numbers. Do not say 'Here is the summary' or use markdown.

{context}"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{settings.OLLAMA_HOST}/api/generate",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                if response.status_code == 200:
                    return response.json().get("response", fallback_summary).strip()
        except Exception:
            pass
            
        return fallback_summary
