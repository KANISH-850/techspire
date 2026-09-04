from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "module": "AI-Procurement"}

def test_get_inventory_status():
    response = client.get("/api/v1/inventory/status")
    assert response.status_code == 200
    data = response.json()
    assert "total_items" in data
    assert "low_stock" in data
    assert "critical_stock" in data
    assert "expired" in data
    assert "expiring_soon" in data

def test_get_low_stock():
    response = client.get("/api/v1/inventory/low-stock")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "recommended_quantity" in data[0]
        assert "priority" in data[0]

def test_get_expiry():
    response = client.get("/api/v1/inventory/expiry")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "days_remaining" in data[0]
        assert "status" in data[0]

def test_get_vendors():
    response = client.get("/api/v1/inventory/vendors")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_ai_recommendations():
    # Since Ollama might not be running in the test environment, we expect our robust fallback mechanism to return a 200 OK.
    response = client.get("/api/v1/inventory/ai-recommendations")
    assert response.status_code == 200
    data = response.json()
    assert "executive_summary" in data
    assert "immediate_actions" in data
    assert "cost_optimization" in data

def test_create_and_update_purchase_order():
    # Get a vendor
    vendors_res = client.get("/api/v1/inventory/vendors")
    assert vendors_res.status_code == 200
    vendors = vendors_res.json()
    if not vendors:
        pytest.skip("No vendors seeded, skipping PO creation test")
    
    vendor_id = vendors[0]["id"]
    
    # Get an item
    status_res = client.get("/api/v1/inventory/low-stock")
    if not status_res.json():
        pytest.skip("No low stock items, skipping PO test")
    item_id = status_res.json()[0]["id"]
    
    # Create PO
    po_payload = {
        "vendor_id": vendor_id,
        "status": "Draft",
        "total_amount": 100.0,
        "items": [
            {
                "inventory_item_id": item_id,
                "quantity": 10,
                "unit_price": 10.0,
                "total_price": 100.0
            }
        ]
    }
    create_res = client.post("/api/v1/inventory/purchase-orders", json=po_payload)
    assert create_res.status_code == 200
    po_data = create_res.json()
    assert po_data["status"] == "Draft"
    assert po_data["vendor_id"] == vendor_id
    
    po_id = po_data["id"]
    
    # Update PO status
    update_res = client.patch(f"/api/v1/inventory/purchase-orders/{po_id}", json={"status": "Approved"})
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "Approved"
