import os
import asyncio
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load env before importing anything
load_dotenv(override=True)

from app.services.ai.openai_provider import OpenAIProvider

def test_ai():
    print(f"API KEY: {os.getenv('OPENAI_API_KEY')[:5]}...")
    print(f"BASE URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"MODEL: {os.getenv('OPENAI_MODEL')}")

    provider = OpenAIProvider() 
    data = {
        "kpis": {"total_revenue": 50000, "bed_occupancy": 95},
        "alerts": [{"severity": "CRITICAL", "message": "High occupancy"}],
        "departments": []
    }
    
    print("Generating insights...")
    result = provider.generate_insights(data)
    print("Result:")
    import json
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_ai()
