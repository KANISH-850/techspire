import ollama
import logging
from typing import List
from app.core.config import settings

logger = logging.getLogger(__name__)

class Embeddings:
    def __init__(self, model_name: str = None, host: str = None):
        self.model_name = model_name or settings.OLLAMA_EMBEDDING_MODEL
        self.host = host or settings.OLLAMA_BASE_URL
        self.client = ollama.Client(host=self.host)

    def get_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding for a single text string using Ollama.
        """
        try:
            response = self.client.embeddings(model=self.model_name, prompt=text)
            return response["embedding"]
        except Exception as e:
            logger.error(f"Failed to get embedding from Ollama: {e}")
            raise
            
    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of strings sequentially.
        Ollama doesn't natively support batch embeddings API efficiently in one call, 
        so we iterate over the texts.
        """
        embeddings = []
        for text in texts:
            embeddings.append(self.get_embedding(text))
        return embeddings
