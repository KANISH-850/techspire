from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate executive insights based on aggregated dashboard analytics.
        Must return a dict with:
        - summary: str
        - key_observations: list[str]
        - recommendations: list[str]
        """
        pass
