from fastapi.testclient import TestClient
from app.main import app
import httpx

client = TestClient(app)

def test_chatbot_flow():
    # 1. Create conversation
    response = client.post("/api/v1/chatbot/conversations", json={
        "title": "Test Chat",
        "session_id": "test_session",
        "status": "active"
    })
    assert response.status_code in [200, 201]
    data = response.json()
    assert "id" in data
    cid = data["id"]
    
    # 2. Patient lookup chat message
    response = client.post("/api/v1/chatbot/chat", json={
        "conversation_id": cid,
        "message": "What is the status of patient Emily Chen?"
    })
    assert response.status_code == 200
    assert len(response.text) > 0
