import ollama

def test_ollama():
    print("Testing qwen3:4b LLM...")
    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": "Say 'Ollama is reachable' and nothing else."
            }
        ]
    )
    print("LLM Response:", response["message"]["content"])
    
    print("\nTesting nomic-embed-text...")
    embed_response = ollama.embeddings(
        model="nomic-embed-text",
        prompt="Hospital services"
    )
    embedding = embed_response.get("embedding", [])
    print(f"Embedding generated! Length: {len(embedding)}")

if __name__ == "__main__":
    test_ollama()
