from abc import ABC, abstractmethod
from typing import List, Dict, Iterator

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response from the AI provider."""
        pass

    def generate_stream(self, messages: List[Dict[str, str]]) -> Iterator[str]:
        """
        Optional method to return a generator for streaming responses.
        By default, it just yields the full response. Providers can override this.
        """
        yield self.generate_response(messages)
