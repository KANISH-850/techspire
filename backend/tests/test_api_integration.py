import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.core.config import settings

client = TestClient(app)

@pytest.fixture(scope="module")
def auth_headers():
    # Register test user or login admin
    username = "test_user_integration"
    password = "password123"
    email = "test_user_integration@hms.com"

    # Try register
    resp = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={"username": username, "email": email, "password": password}
    )
    if resp.status_code not in [201, 400]:
        pytest.fail(f"Failed user registration: {resp.text}")

    # Login
    login_resp = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": username, "password": password}
    )
    if login_resp.status_code != 200:
        # Fallback to admin login
        login_resp = client.post(
            f"{settings.API_V1_STR}/auth/login",
            json={"username": "admin", "password": "admin123"}
        )

    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_health_endpoints():
    res1 = client.get(f"{settings.API_V1_STR}/health")
    assert res1.status_code == 200
    assert res1.json()["status"] == "healthy"

    res2 = client.get(f"{settings.API_V1_STR}/health/ready")
    assert res2.status_code == 200
    assert res2.json()["status"] == "ready"

def test_unauthenticated_rejection():
    res = client.get(f"{settings.API_V1_STR}/dashboard/kpis")
    assert res.status_code == 401

def test_auth_me(auth_headers):
    res = client.get(f"{settings.API_V1_STR}/auth/me", headers=auth_headers)
    assert res.status_code == 200
    assert "username" in res.json()

def test_dashboard_endpoints(auth_headers):
    kpis = client.get(f"{settings.API_V1_STR}/dashboard/kpis", headers=auth_headers)
    assert kpis.status_code == 200
    data = kpis.json()
    assert "total_revenue" in data
    assert "total_patients" in data
    assert "total_admissions" in data

    rev = client.get(f"{settings.API_V1_STR}/dashboard/revenue", headers=auth_headers)
    assert rev.status_code == 200
    assert "total_revenue" in rev.json()

    depts = client.get(f"{settings.API_V1_STR}/dashboard/departments", headers=auth_headers)
    assert depts.status_code == 200
    assert "departments" in depts.json()

    alerts = client.get(f"{settings.API_V1_STR}/dashboard/alerts", headers=auth_headers)
    assert alerts.status_code == 200
    assert "alerts" in alerts.json()

    insights = client.get(f"{settings.API_V1_STR}/dashboard/ai-insights", headers=auth_headers)
    assert insights.status_code == 200
    assert "summary" in insights.json()

def test_predictive_endpoints(auth_headers):
    rev = client.get(f"{settings.API_V1_STR}/predictive/revenue?days=14", headers=auth_headers)
    assert rev.status_code == 200
    assert rev.json()["metric"] == "revenue"
    assert "metrics" in rev.json()
    assert "algorithm" in rev.json()

    adm = client.get(f"{settings.API_V1_STR}/predictive/admissions?days=14", headers=auth_headers)
    assert adm.status_code == 200
    assert adm.json()["metric"] == "admissions"

    beds = client.get(f"{settings.API_V1_STR}/predictive/beds?days=7", headers=auth_headers)
    assert beds.status_code == 200

    meds = client.get(f"{settings.API_V1_STR}/predictive/medicines", headers=auth_headers)
    assert meds.status_code == 200
    assert isinstance(meds.json(), list)

    inv = client.get(f"{settings.API_V1_STR}/predictive/inventory", headers=auth_headers)
    assert inv.status_code == 200
    assert isinstance(inv.json(), list)

    summary = client.get(f"{settings.API_V1_STR}/predictive/summary", headers=auth_headers)
    assert summary.status_code == 200
    assert "revenue_trend" in summary.json()

def test_report_endpoints(auth_headers):
    r_types = client.get(f"{settings.API_V1_STR}/reports/types", headers=auth_headers)
    assert r_types.status_code == 200
    assert "financial" in r_types.json()

    gen = client.post(
        f"{settings.API_V1_STR}/reports/generate",
        json={"report_type": "financial", "format": "all"},
        headers=auth_headers
    )
    assert gen.status_code == 200
    res_data = gen.json()
    assert "report_id" in res_data
    assert "executive_summary" in res_data

def test_inventory_endpoints(auth_headers):
    status_res = client.get(f"{settings.API_V1_STR}/inventory/status", headers=auth_headers)
    assert status_res.status_code == 200
    assert "total_items" in status_res.json()

    low_stock = client.get(f"{settings.API_V1_STR}/inventory/low-stock", headers=auth_headers)
    assert low_stock.status_code == 200
    assert isinstance(low_stock.json(), list)

    expiry = client.get(f"{settings.API_V1_STR}/inventory/expiry", headers=auth_headers)
    assert expiry.status_code == 200
    assert isinstance(expiry.json(), list)

    items = client.get(f"{settings.API_V1_STR}/inventory/items", headers=auth_headers)
    assert items.status_code == 200
    assert isinstance(items.json(), list)

def test_procurement_endpoints(auth_headers):
    vendors = client.get(f"{settings.API_V1_STR}/procurement/vendors", headers=auth_headers)
    assert vendors.status_code == 200
    assert isinstance(vendors.json(), list)

    recs = client.get(f"{settings.API_V1_STR}/procurement/ai-recommendations", headers=auth_headers)
    assert recs.status_code == 200
    assert "suggested_orders" in recs.json()

    pos = client.get(f"{settings.API_V1_STR}/procurement/purchase-orders", headers=auth_headers)
    assert pos.status_code == 200
    assert isinstance(pos.json(), list)

def test_domain_entity_endpoints(auth_headers):
    patients = client.get(f"{settings.API_V1_STR}/patients", headers=auth_headers)
    assert patients.status_code == 200

    appointments = client.get(f"{settings.API_V1_STR}/appointments", headers=auth_headers)
    assert appointments.status_code == 200

    admissions = client.get(f"{settings.API_V1_STR}/admissions", headers=auth_headers)
    assert admissions.status_code == 200

    beds = client.get(f"{settings.API_V1_STR}/beds", headers=auth_headers)
    assert beds.status_code == 200

def test_chatbot_endpoints(auth_headers):
    conv_create = client.post(
        f"{settings.API_V1_STR}/chatbot/conversations",
        json={"title": "Test Chat Conversation"},
        headers=auth_headers
    )
    assert conv_create.status_code == 200
    conv_id = conv_create.json()["id"]

    conv_get = client.get(f"{settings.API_V1_STR}/chatbot/conversations/{conv_id}", headers=auth_headers)
    assert conv_get.status_code == 200
    assert conv_get.json()["id"] == conv_id
