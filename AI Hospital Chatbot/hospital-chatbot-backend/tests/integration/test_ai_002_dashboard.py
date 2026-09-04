from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_kpis():
    response = client.get("/api/v1/dashboard/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "total_revenue" in data
    assert "total_patients" in data

def test_dashboard_revenue():
    response = client.get("/api/v1/dashboard/revenue")
    assert response.status_code == 200
    data = response.json()
    assert "monthly" in data

def test_dashboard_departments():
    response = client.get("/api/v1/dashboard/departments")
    assert response.status_code == 200
    data = response.json()
    assert "departments" in data
    assert isinstance(data["departments"], list)

def test_dashboard_alerts():
    response = client.get("/api/v1/dashboard/alerts")
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
