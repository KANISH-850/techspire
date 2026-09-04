import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_kpis():
    response = client.get("/api/v1/dashboard/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "total_revenue" in data
    assert "total_patients" in data
    assert "value" in data["total_revenue"]

def test_get_revenue():
    response = client.get("/api/v1/dashboard/revenue")
    assert response.status_code == 200
    data = response.json()
    assert "total_revenue" in data
    assert "monthly" in data

def test_get_departments():
    response = client.get("/api/v1/dashboard/departments")
    assert response.status_code == 200
    data = response.json()
    assert "departments" in data
    assert type(data["departments"]) is list

def test_get_alerts():
    response = client.get("/api/v1/dashboard/alerts")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert type(data["alerts"]) is list

# Note: test_get_ai_insights is skipped by default to prevent real API calls
# unless mocking is explicitly implemented.
@pytest.mark.skip(reason="Avoids external API call")
def test_get_ai_insights():
    response = client.get("/api/v1/dashboard/ai-insights")
    assert response.status_code == 200
    data = response.json()
    assert "executive_summary" in data
