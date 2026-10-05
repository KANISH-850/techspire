from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.inventory import (
    InventoryItemCreate, InventoryItemResponse, InventoryStatusResponse,
    LowStockItemResponse, ExpiryAlertResponse
)
from app.services.inventory.inventory_service import InventoryService

router = APIRouter()

@router.get("/status", response_model=InventoryStatusResponse)
def get_inventory_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return InventoryService.get_status(db)

@router.get("/low-stock", response_model=List[LowStockItemResponse])
def get_low_stock(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return InventoryService.get_low_stock(db)

@router.get("/expiry", response_model=List[ExpiryAlertResponse])
def get_expiry(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return InventoryService.get_expiry_alerts(db)

@router.get("/items", response_model=List[InventoryItemResponse])
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return InventoryService.get_items(db, skip=skip, limit=limit)

@router.post("/items", response_model=InventoryItemResponse, status_code=201)
def create_item(
    item_in: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return InventoryService.create_item(db, item_in)

@router.get("/items/{item_id}", response_model=InventoryItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    item = InventoryService.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item
