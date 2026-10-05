from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.procurement import (
    VendorCreate, VendorResponse, VendorAnalysisResponse,
    PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderResponse,
    AIProcurementRecommendation
)
from app.services.procurement.procurement_service import ProcurementService

router = APIRouter()

@router.get("/vendors", response_model=List[VendorAnalysisResponse])
def get_vendors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return ProcurementService.get_vendors(db)

@router.post("/vendors", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
def create_vendor(
    vendor_in: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return ProcurementService.create_vendor(db, vendor_in)

@router.get("/ai-recommendations", response_model=AIProcurementRecommendation)
@router.get("/recommendations", response_model=AIProcurementRecommendation)
async def get_ai_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await ProcurementService.get_ai_recommendations(db)

@router.get("/purchase-orders", response_model=List[PurchaseOrderResponse])
def list_purchase_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return ProcurementService.list_purchase_orders(db)

@router.post("/purchase-orders", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_order(
    po_in: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        return ProcurementService.create_purchase_order(db, po_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/purchase-orders/{po_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    po = ProcurementService.get_purchase_order(db, po_id)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return po

@router.patch("/purchase-orders/{po_id}", response_model=PurchaseOrderResponse)
def update_purchase_order_status(
    po_id: int,
    update: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        return ProcurementService.update_purchase_order_status(db, po_id, update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
