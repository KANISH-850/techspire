from typing import List, Dict, Iterator, Any
import json
import ollama
from app.services.ai.base_provider import BaseAIProvider

class OllamaProvider(BaseAIProvider):
    def __init__(self, model: str = "qwen3:4b", host: str = "http://localhost:11434"):
        self.model = model
        self.client = ollama.Client(host=host)

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat(
            model=self.model,
            messages=messages,
            stream=False
        )
        return response["message"]["content"]
        
    def generate_stream(self, messages: List[Dict[str, str]]) -> Iterator[str]:
        stream = self.client.chat(
            model=self.model,
            messages=messages,
            stream=True
        )
        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                yield chunk["message"]["content"]

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
            content = self.generate_response([{"role": "user", "content": prompt}]).strip()
            
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
                
            parsed_json = json.loads(content)
            
            required_keys = ["executive_summary", "hospital_status", "key_insights", "risks", "recommendations"]
            for key in required_keys:
                if key not in parsed_json:
                    parsed_json[key] = [] if key in ["key_insights", "risks", "recommendations"] else "Missing data."
            
            return parsed_json

        except Exception as e:
            print(f"AI API Error: {e}")
            return {
                "executive_summary": "AI Insights unavailable. Check connection.",
                "hospital_status": "Unknown",
                "key_insights": [],
                "risks": [],
                "recommendations": []
            }
