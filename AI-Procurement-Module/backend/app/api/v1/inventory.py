from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.inventory_analytics import InventoryAnalytics
from app.services.ai_provider import AIProviderService
from app import schemas
from app.models.purchase_order import PurchaseOrder, PurchaseOrderItem
from app.models.vendor import Vendor

router = APIRouter()

@router.get("/status")
def get_inventory_status(db: Session = Depends(get_db)):
    return InventoryAnalytics.get_status(db)

@router.get("/low-stock")
def get_low_stock(db: Session = Depends(get_db)):
    return InventoryAnalytics.get_low_stock(db)

@router.get("/expiry")
def get_expiry(db: Session = Depends(get_db)):
    return InventoryAnalytics.get_expiry_alerts(db)

@router.get("/vendors")
def get_vendors(db: Session = Depends(get_db)):
    return InventoryAnalytics.get_vendor_analysis(db)

@router.get("/ai-recommendations")
async def get_ai_recommendations(db: Session = Depends(get_db)):
    # Build context
    context = {
        "status": InventoryAnalytics.get_status(db),
        "low_stock": InventoryAnalytics.get_low_stock(db),
        "expiry_alerts": InventoryAnalytics.get_expiry_alerts(db)
    }
    return await AIProviderService.get_recommendations(context)

@router.post("/purchase-orders", response_model=schemas.PurchaseOrderResponse)
def create_purchase_order(po: schemas.PurchaseOrderCreate, db: Session = Depends(get_db)):
    # Validate vendor
    vendor = db.query(Vendor).filter(Vendor.id == po.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
        
    db_po = PurchaseOrder(
        vendor_id=po.vendor_id,
        status=po.status,
        total_amount=po.total_amount,
        expected_delivery_date=po.expected_delivery_date
    )
    db.add(db_po)
    db.commit()
    db.refresh(db_po)
    
    for item in po.items:
        db_item = PurchaseOrderItem(
            purchase_order_id=db_po.id,
            inventory_item_id=item.inventory_item_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.total_price
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_po)
    return db_po

@router.get("/purchase-orders", response_model=List[schemas.PurchaseOrderResponse])
def list_purchase_orders(db: Session = Depends(get_db)):
    return db.query(PurchaseOrder).all()

@router.get("/purchase-orders/{po_id}", response_model=schemas.PurchaseOrderResponse)
def get_purchase_order(po_id: int, db: Session = Depends(get_db)):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return po

@router.patch("/purchase-orders/{po_id}", response_model=schemas.PurchaseOrderResponse)
def update_purchase_order_status(po_id: int, update: schemas.PurchaseOrderUpdate, db: Session = Depends(get_db)):
    valid_statuses = ["Draft", "Pending", "Approved", "Ordered", "Received", "Cancelled"]
    if update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
        
    po.status = update.status
    db.commit()
    db.refresh(po)
    return po
