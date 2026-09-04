import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.vendor import Vendor
from app.models.inventory import InventoryItem
from app.models.purchase_order import PurchaseOrder, PurchaseOrderItem
from app import models

def seed():
    db = SessionLocal()
    
    # Check if seeded
    if db.query(Vendor).filter(Vendor.name == "MedSupply Co.").first():
        print("Database already seeded with procurement mock data.")
        db.close()
        return

    # Create Vendors
    v1 = Vendor(name="MedSupply Co.", contact_person="Alice Smith", email="alice@medsupply.com", average_delivery_days=3, reliability_score=98.5)
    v2 = Vendor(name="PharmaGlobal", contact_person="Bob Jones", email="bob@pharmaglobal.com", average_delivery_days=7, reliability_score=85.0)
    v3 = Vendor(name="SurgicalTools Ltd.", contact_person="Charlie Day", email="charlie@surgicaltools.com", average_delivery_days=5, reliability_score=92.0)
    
    db.add_all([v1, v2, v3])
    db.commit()
    
    today = datetime.date.today()
    
    # Create Inventory Items
    items = [
        # Normal
        InventoryItem(name="Surgical Masks", category="PPE", sku="PPE-001", current_stock=5000, minimum_stock=1000, maximum_stock=10000, unit="Box", unit_price=15.0, expiry_date=today + datetime.timedelta(days=365), vendor_id=v1.id),
        InventoryItem(name="IV Fluids", category="Emergency", sku="EMG-001", current_stock=800, minimum_stock=500, maximum_stock=2000, unit="Bag", unit_price=10.0, expiry_date=today + datetime.timedelta(days=180), vendor_id=v2.id),
        
        # Low Stock
        InventoryItem(name="Bandages", category="Surgical", sku="SUR-001", current_stock=150, minimum_stock=500, maximum_stock=2000, unit="Roll", unit_price=2.5, expiry_date=today + datetime.timedelta(days=700), vendor_id=v1.id),
        InventoryItem(name="Syringes (10ml)", category="Laboratory", sku="LAB-001", current_stock=250, minimum_stock=500, maximum_stock=5000, unit="Box", unit_price=25.0, expiry_date=today + datetime.timedelta(days=365), vendor_id=v3.id),
        
        # Critical Stock
        InventoryItem(name="Defibrillator Pads", category="Emergency", sku="EMG-002", current_stock=2, minimum_stock=20, maximum_stock=100, unit="Pair", unit_price=120.0, expiry_date=today + datetime.timedelta(days=400), vendor_id=v3.id),
        
        # Expiring Soon (7 days)
        InventoryItem(name="Amoxicillin", category="Medicine", sku="MED-001", current_stock=300, minimum_stock=100, maximum_stock=1000, unit="Bottle", unit_price=45.0, expiry_date=today + datetime.timedelta(days=5), vendor_id=v2.id),
        
        # Expiring Soon (30 days)
        InventoryItem(name="Insulin", category="Medicine", sku="MED-002", current_stock=150, minimum_stock=50, maximum_stock=500, unit="Vial", unit_price=85.0, expiry_date=today + datetime.timedelta(days=20), vendor_id=v2.id),
        
        # Expired
        InventoryItem(name="Paracetamol", category="Medicine", sku="MED-003", current_stock=400, minimum_stock=200, maximum_stock=2000, unit="Pack", unit_price=5.0, expiry_date=today - datetime.timedelta(days=10), vendor_id=v2.id)
    ]
    
    db.add_all(items)
    db.commit()
    
    # Create historical Purchase Orders
    po1 = PurchaseOrder(vendor_id=v1.id, status="Received", total_amount=1500.0, created_at=today - datetime.timedelta(days=30))
    po2 = PurchaseOrder(vendor_id=v2.id, status="Pending", total_amount=4500.0, created_at=today - datetime.timedelta(days=2))
    db.add_all([po1, po2])
    db.commit()
    
    # Purchase Order Items
    poi1 = PurchaseOrderItem(purchase_order_id=po1.id, inventory_item_id=items[0].id, quantity=100, unit_price=15.0, total_price=1500.0)
    poi2 = PurchaseOrderItem(purchase_order_id=po2.id, inventory_item_id=items[5].id, quantity=100, unit_price=45.0, total_price=4500.0)
    db.add_all([poi1, poi2])
    db.commit()
    
    print("Database seeded successfully with deterministic mock data.")
    db.close()

if __name__ == "__main__":
    seed()
