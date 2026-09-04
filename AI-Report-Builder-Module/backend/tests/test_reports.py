from fastapi.testclient import TestClient
import pytest
import os
from app.main import app
from report_config import settings

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/reports/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_report_types():
    response = client.get("/api/v1/reports/types")
    assert response.status_code == 200
    assert "financial" in response.json()

@pytest.mark.parametrize("report_type", ["financial", "clinical", "operational", "inventory", "procurement"])
def test_generate_report_pdf(report_type):
    payload = {
        "report_type": report_type,
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "department": "all",
        "format": "pdf"
    }
    response = client.post("/api/v1/reports/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["report_type"] == report_type
    assert data["format"] == "pdf"
    assert "report_id" in data
    assert "download_url" in data
    assert "summary" in data
    assert "kpis" in data
    assert "charts" in data
    
    # Check if PDF exists
    pdf_path = os.path.join(settings.REPORT_STORAGE_PATH, f"{data['report_id']}.pdf")
    assert os.path.exists(pdf_path)

def test_generate_report_excel():
    payload = {
        "report_type": "financial",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "department": "all",
        "format": "excel"
    }
    response = client.post("/api/v1/reports/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    excel_path = os.path.join(settings.REPORT_STORAGE_PATH, f"{data['report_id']}.xlsx")
    assert os.path.exists(excel_path)

def test_report_history():
    response = client.get("/api/v1/reports/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_invalid_report_type():
    payload = {
        "report_type": "invalid_type",
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "department": "all",
        "format": "pdf"
    }
    response = client.post("/api/v1/reports/generate", json=payload)
    assert response.status_code == 400
