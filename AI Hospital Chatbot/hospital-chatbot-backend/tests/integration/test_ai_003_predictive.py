from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predictive_revenue():
    response = client.get("/api/v1/predictive/revenue?days_ahead=30")
    assert response.status_code == 200
    data = response.json()
    assert "historical" in data
    assert "forecast" in data
    assert "ai_analysis" in data

def test_predictive_admissions():
    response = client.get("/api/v1/predictive/admissions?days_ahead=30")
    assert response.status_code == 200
    data = response.json()
    assert "historical" in data
    assert "forecast" in data
    assert "ai_analysis" in data
