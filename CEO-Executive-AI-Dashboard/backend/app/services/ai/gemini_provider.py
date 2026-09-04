import json
from google import genai
from typing import Dict, Any
from .base_provider import BaseAIProvider
from app.core.config import settings

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        You are an expert hospital management consultant AI.
        Analyze the following aggregated hospital analytics data and provide an executive summary, key insights, risks, and actionable recommendations.
        Do NOT invent any numerical values. Use ONLY the data provided.
        
        Data:
        {json.dumps(data, indent=2)}
        
        Return ONLY a valid JSON object with the following structure:
        {{
            "executive_summary": "High-level summary of the hospital's performance.",
            "hospital_status": "Excellent/Stable/Warning/Critical",
            "key_insights": ["Insight 1", "Insight 2", "Insight 3"],
            "risks": [
                {{
                    "title": "Short title",
                    "severity": "CRITICAL/HIGH/MEDIUM/LOW",
                    "description": "Detailed description of the risk."
                }}
            ],
            "recommendations": [
                {{
                    "priority": "CRITICAL/HIGH/MEDIUM/LOW",
                    "recommendation": "Actionable recommendation.",
                    "reason": "Why this is recommended based on data.",
                    "expected_impact": "What impact this will have."
                }}
            ]
        }}
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            text_resp = response.text.strip()
            if text_resp.startswith('```json'):
                text_resp = text_resp[7:-3]
            elif text_resp.startswith('```'):
                text_resp = text_resp[3:-3]
            return json.loads(text_resp)
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return {
                "executive_summary": "AI Insights are currently unavailable due to an error.",
                "hospital_status": "Unknown",
                "key_insights": [],
                "risks": [],
                "recommendations": []
            }
