import os
import chromadb
import logging
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, collection_name: str = "hospital_knowledge"):
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        
    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """
        Adds or updates chunks and their embeddings in ChromaDB.
        Generates a unique ID for each chunk based on its source and index.
        """
        if not chunks:
            return
            
        ids = []
        texts = []
        metadatas = []
        
        # Track counts to make unique IDs
        source_counts = {}
        
        for chunk in chunks:
            source = chunk["metadata"].get("source", "unknown")
            source_counts[source] = source_counts.get(source, 0) + 1
            
            chunk_id = f"{source}_{source_counts[source]:03d}"
            
            ids.append(chunk_id)
            texts.append(chunk["text"])
            metadatas.append(chunk["metadata"])
            
        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )
        logger.info(f"Upserted {len(chunks)} chunks into ChromaDB.")

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches the vector store for the most relevant chunks given a query embedding.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        retrieved = []
        if not results["documents"] or not results["documents"][0]:
            return retrieved
            
        for i in range(len(results["documents"][0])):
            retrieved.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
            })
            
        return retrieved
