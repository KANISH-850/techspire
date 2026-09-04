import json
from openai import OpenAI
from typing import Dict, Any
from .base_provider import BaseAIProvider
from app.core.config import settings

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        kwargs = {"api_key": settings.OPENAI_API_KEY}
        if settings.OPENAI_BASE_URL:
            kwargs["base_url"] = settings.OPENAI_BASE_URL
        self.client = OpenAI(**kwargs)
        
        # Override model to force deepseek if using openrouter
        self.model = settings.OPENAI_MODEL if settings.OPENAI_MODEL else "deepseek/deepseek-chat"

    def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        You are an expert hospital management consultant AI.
        Analyze the following aggregated hospital analytics data and provide an executive summary, key insights, risks, and actionable recommendations.
        Do NOT invent any numerical values. Use ONLY the data provided.
        
        Data:
        {json.dumps(data, indent=2, default=str)}
        
        Return ONLY a valid JSON object with the exact following structure. Do not return markdown, just the JSON string:
        {{
            "executive_summary": "High-level summary of the hospital's performance based on the metrics provided.",
            "hospital_status": "Excellent" | "Stable" | "Warning" | "Critical",
            "key_insights": ["Insight 1", "Insight 2", "Insight 3"],
            "risks": [
                {{
                    "title": "Short title",
                    "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
                    "description": "Detailed description of the risk."
                }}
            ],
            "recommendations": [
                {{
                    "priority": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
                    "title": "Actionable recommendation title.",
                    "reason": "Why this is recommended based on data.",
                    "supporting_metric": "Specific data metric supporting this.",
                    "expected_impact": "What impact this will have."
                }}
            ]
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up potential markdown formatting block if AI ignores instruction
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
                
            parsed_json = json.loads(content)
            
            # Validate basic structure
            required_keys = ["executive_summary", "hospital_status", "key_insights", "risks", "recommendations"]
            for key in required_keys:
                if key not in parsed_json:
                    parsed_json[key] = [] if key in ["key_insights", "risks", "recommendations"] else "Missing data."
            
            return parsed_json

        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}, Raw content: {content}")
            return self._fallback_response("The AI returned malformed data. Please try again.")
        except Exception as e:
            print(f"AI API Error: {e}")
            return self._fallback_response(f"AI Insights are currently unavailable due to an error: {str(e)}")

    def _fallback_response(self, message: str) -> Dict[str, Any]:
        return {
            "executive_summary": message,
            "hospital_status": "Unknown",
            "key_insights": [],
            "risks": [],
            "recommendations": []
        }
