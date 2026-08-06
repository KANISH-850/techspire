from google import genai
from typing import List, Dict
from app.services.ai.base_provider import BaseAIProvider

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            system_instruction = None
            
            # Extract system instruction
            for msg in messages:
                if msg["role"] == "system":
                    system_instruction = msg["content"]
                    break
            
            formatted_contents = []
            if system_instruction:
                 formatted_contents.append(
                     {"role": "user", "parts": [{"text": f"System Instruction: {system_instruction}"}]}
                 )
                 formatted_contents.append(
                     {"role": "model", "parts": [{"text": "Understood. I will follow these instructions."}]}
                 )

            for msg in messages:
                if msg["role"] == "system":
                    continue
                role = "user" if msg["role"] == "user" else "model"
                if not formatted_contents or formatted_contents[-1]["role"] != role:
                    formatted_contents.append({"role": role, "parts": [{"text": msg["content"]}]})
                else:
                    formatted_contents[-1]["parts"][0]["text"] += f"\n\n{msg['content']}"
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=formatted_contents
            )
            
            return response.text or ""
        except Exception as e:
            raise Exception(f"Gemini API Error: {str(e)}")
