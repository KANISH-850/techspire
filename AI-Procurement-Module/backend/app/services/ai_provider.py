import httpx
import json
from app.database import settings

class AIProviderService:
    @staticmethod
    async def get_recommendations(inventory_context: dict):
        prompt = f"""
You are an expert Hospital Procurement AI Assistant.
Based on the following inventory data, generate an executive summary and procurement recommendations.
Return ONLY valid JSON in this exact structure:
{{
    "executive_summary": "Overall summary of the inventory health",
    "immediate_actions": ["List of immediate purchase actions"],
    "cost_optimization": ["List of cost saving suggestions"]
}}

Inventory Context:
{json.dumps(inventory_context, default=str)}
"""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{settings.OLLAMA_HOST}/api/generate",
                    json={
                        "model": settings.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    }
                )
                response.raise_for_status()
                data = response.json()
                return json.loads(data["response"])
        except Exception as e:
            # Deterministic Fallback if Ollama is unavailable
            return {
                "executive_summary": f"AI recommendations temporarily unavailable. Generated fallback based on rules. You have {len(inventory_context.get('low_stock', []))} low stock items and {len(inventory_context.get('expiry_alerts', []))} expiring items.",
                "immediate_actions": [f"Reorder {item['name']}" for item in inventory_context.get('low_stock', [])],
                "cost_optimization": ["Consolidate orders to reduce shipping costs", "Review vendor contracts for items ordered frequently"]
            }
