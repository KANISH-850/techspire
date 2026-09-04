from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/predictive/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_revenue_forecast():
    response = client.get("/api/v1/predictive/revenue?days=7")
    assert response.status_code == 200
    data = response.json()
    assert data["metric"] == "revenue"
    assert "historical" in data
    assert "forecast" in data
    assert "trend" in data
    assert "metrics" in data
    assert "explanation" in data

def test_admissions_forecast():
    response = client.get("/api/v1/predictive/admissions?days=30")
    assert response.status_code == 200
    assert response.json()["metric"] == "admissions"

def test_bed_occupancy_forecast():
    response = client.get("/api/v1/predictive/bed-occupancy?days=7")
    assert response.status_code == 200
    assert response.json()["metric"] == "bed-occupancy"

def test_medicine_demand_forecast():
    response = client.get("/api/v1/predictive/medicine-demand")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_inventory_forecast():
    response = client.get("/api/v1/predictive/inventory")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_summary():
    response = client.get("/api/v1/predictive/summary")
    assert response.status_code == 200
    assert "revenue_trend" in response.json()
