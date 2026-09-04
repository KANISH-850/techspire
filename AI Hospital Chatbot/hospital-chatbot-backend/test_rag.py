import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.retriever import Retriever

logging.basicConfig(level=logging.INFO)

def test_retrieval():
    retriever = Retriever()
    query = "What are the ICU visiting hours?"
    print(f"\nQuery:\n{query}\n")
    
    results = retriever.retrieve_relevant_documents(query)
    
    print("Retrieved documents:\n")
    for i, res in enumerate(results, 1):
        source = res['metadata'].get('source', 'Unknown')
        print(f"{i}. [Source: {source} | Distance: {res['distance']:.4f}]")
        print(f"{res['text']}\n")

if __name__ == "__main__":
    test_retrieval()
