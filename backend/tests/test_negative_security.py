import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_invalid_login():
    res = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": "wronguser", "password": "wrongpassword"}
    )
    assert res.status_code == 401

def test_invalid_jwt_token():
    headers = {"Authorization": "Bearer invalid_garbage_token_12345"}
    res = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert res.status_code == 401

def test_missing_auth_header():
    res = client.get(f"{settings.API_V1_STR}/dashboard/kpis")
    assert res.status_code == 401

def test_nonexistent_patient_id():
    login_resp = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    if login_resp.status_code == 200:
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        res = client.get(f"{settings.API_V1_STR}/patients/9999999", headers=headers)
        assert res.status_code == 404

