import os
import sys
import logging
import argparse

# Ensure we can import app modules when running as a script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.document_loader import DocumentLoader
from rag.chunker import Chunker
from rag.embeddings import Embeddings
from rag.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Ingest hospital documents into ChromaDB.")
    parser.add_argument("--data-dir", type=str, default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "documents"), help="Directory containing documents.")
    args = parser.parse_args()

    logger.info("Loading documents...")
    loader = DocumentLoader(data_dir=args.data_dir)
    documents = loader.load_documents()
    
    if not documents:
        logger.info("No documents found to ingest.")
        return
        
    logger.info(f"Found {len(documents)} documents.")
    
    chunker = Chunker(chunk_size=500, chunk_overlap=100)
    chunks = chunker.chunk_documents(documents)
    logger.info(f"Created {len(chunks)} chunks.")
    
    logger.info("Generating embeddings (this might take a while)...")
    embeddings_service = Embeddings()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embeddings_service.get_embeddings_batch(texts)
    
    logger.info("Storing chunks and embeddings in ChromaDB...")
    vector_store = VectorStore()
    vector_store.add_chunks(chunks, embeddings)
    
    logger.info("Ingestion completed successfully.")

if __name__ == "__main__":
    main()
