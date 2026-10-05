import logging
from typing import List, Dict, Any
from app.core.config import settings
from rag.embeddings import Embeddings
from rag.vector_store import VectorStore

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self):
        self.embeddings = Embeddings()
        self.vector_store = VectorStore()
        
    def retrieve_relevant_documents(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        Retrieves the most relevant document chunks for a given query.
        """
        if top_k is None:
            top_k = settings.RAG_TOP_K
            
        try:
            # 1. Generate embedding for the query
            query_embedding = self.embeddings.get_embedding(query)
            
            # 2. Search ChromaDB
            results = self.vector_store.search(query_embedding, top_k=top_k)
            
            # Log debug info
            if settings.DEBUG:
                sources = [res["metadata"].get("source") for res in results]
                logger.info(f"[RAG] Query: {query}")
                logger.info(f"[RAG] Retrieved: {len(results)} chunks")
                logger.info(f"[RAG] Sources: {sources}")
                
            return results
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return []
