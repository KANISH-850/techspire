from typing import List, Dict, Any

class Chunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Splits documents into smaller chunks of approximately `chunk_size` words.
        """
        chunks = []
        for doc in documents:
            text = doc["text"]
            metadata = doc["metadata"]
            
            # Simple word-based chunking
            words = text.split()
            
            if len(words) <= self.chunk_size:
                chunks.append({
                    "text": text,
                    "metadata": metadata
                })
                continue
                
            start = 0
            while start < len(words):
                end = start + self.chunk_size
                chunk_words = words[start:end]
                chunk_text = " ".join(chunk_words)
                
                chunks.append({
                    "text": chunk_text,
                    "metadata": metadata
                })
                
                # Move start forward, accounting for overlap
                start += (self.chunk_size - self.chunk_overlap)
                
        return chunks
