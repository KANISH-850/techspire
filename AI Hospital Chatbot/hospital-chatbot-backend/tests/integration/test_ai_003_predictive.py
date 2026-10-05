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
    assert data.get("model") == "Linear Regression"
    assert data.get("algorithm") == "Scikit-Learn LinearRegression"
    assert data.get("data_source") == "PostgreSQL transactions"
    assert data.get("data_quality") == "historical"
    assert "metrics" in data

def test_predictive_admissions():
    response = client.get("/api/v1/predictive/admissions?days_ahead=30")
    assert response.status_code == 200
    data = response.json()
    assert "historical" in data
    assert "forecast" in data
    assert "ai_analysis" in data
    assert data.get("model") == "Linear Regression"
    assert data.get("algorithm") == "Scikit-Learn LinearRegression"
    assert data.get("data_source") == "PostgreSQL admissions"
    assert data.get("data_quality") == "historical"
    assert "metrics" in data

def test_predictive_beds():
    response = client.get("/api/v1/predictive/beds?days_ahead=30")
    assert response.status_code == 200
    data = response.json()
    assert "historical" in data
    assert "forecast" in data
    assert "ai_analysis" in data
    assert data.get("model") == "Linear Regression"
    assert data.get("algorithm") == "Scikit-Learn LinearRegression"
    assert data.get("data_quality") == "approximated"
    assert "metrics" in data

def test_predictive_medicines():
    response = client.get("/api/v1/predictive/medicines?days_ahead=30")
    assert response.status_code == 200
    data = response.json()
    assert "historical" in data
    assert "forecast" in data
    assert "ai_analysis" in data
    assert data.get("model") == "Linear Regression"
    assert data.get("algorithm") == "Scikit-Learn LinearRegression"
    assert data.get("data_quality") == "approximated"
    assert "metrics" in data

def test_predictive_inventory():
    response = client.get("/api/v1/predictive/inventory?days_ahead=30")
    assert response.status_code == 200
    data = response.json()
    assert "historical" in data
    assert "forecast" in data
    assert "ai_analysis" in data
    assert data.get("model") == "Linear Regression"
    assert data.get("algorithm") == "Scikit-Learn LinearRegression"
    assert data.get("data_quality") == "reconstructed"
    assert "metrics" in data
