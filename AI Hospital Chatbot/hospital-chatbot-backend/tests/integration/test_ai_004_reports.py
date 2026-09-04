from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_financial_report_pdf():
    response = client.get("/api/v1/reports/generate?type=financial&format=pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0

def test_clinical_report_excel():
    response = client.get("/api/v1/reports/generate?type=clinical&format=excel")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert len(response.content) > 0
