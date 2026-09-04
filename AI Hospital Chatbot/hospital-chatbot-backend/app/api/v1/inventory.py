from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.analytics import inventory
from app.schemas import (
    LowStockResponse,
    ExpiringResponse,
    VendorAnalysis,
    ReorderSuggestion,
    PurchaseOrderCreate,
    PurchaseOrderResponse
)

router = APIRouter()

@router.get("/status")
def get_inventory_status(db: Session = Depends(get_db)):
    return inventory.get_inventory_status(db)

@router.get("/low-stock", response_model=LowStockResponse)
def get_low_stock(db: Session = Depends(get_db)):
    return inventory.get_low_stock(db)

@router.get("/expiring", response_model=ExpiringResponse)
def get_expiring(db: Session = Depends(get_db)):
    return inventory.get_expiring(db)

@router.get("/vendors", response_model=List[VendorAnalysis])
def get_vendors(db: Session = Depends(get_db)):
    return inventory.get_vendors(db)

@router.get("/reorder", response_model=List[ReorderSuggestion])
def get_reorder_suggestions(db: Session = Depends(get_db)):
    return inventory.get_reorder_suggestions(db)

@router.get("/recommendations")
def get_purchase_recommendations(db: Session = Depends(get_db)):
    return inventory.get_purchase_recommendations(db)

@router.post("/purchase-orders", response_model=PurchaseOrderResponse)
def create_purchase_order(request: PurchaseOrderCreate, db: Session = Depends(get_db)):
    return inventory.create_purchase_order(db, request.vendor_id, request.total_amount)
