from typing import List, Dict
from app.services.ai.base_provider import BaseAIProvider

class MockProvider(BaseAIProvider):
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        return "A hospital bill is an itemized record of the costs for services and materials you received at the hospital. This includes charges for your room, medical supplies, tests, and any procedures you had."
