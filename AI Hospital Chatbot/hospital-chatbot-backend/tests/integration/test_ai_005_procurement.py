from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_inventory_status():
    response = client.get("/api/v1/inventory/status")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "low_stock_items" in data
    assert "all_items" in data
    assert "ai_recommendations" in data
