from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from typing import List, Dict, Any, Optional
from app.models import InventoryItem
from app.schemas.inventory import (
    InventoryItemCreate, InventoryItemResponse, InventoryStatusResponse,
    LowStockItemResponse, ExpiryAlertResponse
)

class InventoryService:
    @staticmethod
    def get_status(db: Session) -> InventoryStatusResponse:
        total_items = db.query(func.count(InventoryItem.id)).scalar() or 0
        total_val = db.query(func.sum(InventoryItem.current_stock * InventoryItem.unit_price)).scalar() or 0.0

        items = db.query(InventoryItem).all()
        low_stock_count = sum(1 for i in items if i.current_stock <= i.minimum_stock)

        today = date.today()
        thirty_days = today + timedelta(days=30)
        expiring_count = sum(1 for i in items if i.expiry_date and today <= i.expiry_date <= thirty_days)

        return InventoryStatusResponse(
            total_items=total_items,
            total_value=round(total_val, 2),
            low_stock_count=low_stock_count,
            expiring_soon_count=expiring_count
        )

    @staticmethod
    def get_low_stock(db: Session) -> List[LowStockItemResponse]:
        items = db.query(InventoryItem).all()
        result = []
        for i in items:
            if i.current_stock <= i.minimum_stock:
                rec_qty = max(0, i.maximum_stock - i.current_stock)
                result.append(LowStockItemResponse(
                    id=i.id,
                    name=i.name,
                    category=i.category or "General",
                    current_stock=i.current_stock,
                    minimum_stock=i.minimum_stock,
                    daily_consumption=i.daily_consumption or 0.0,
                    reorder_recommended_qty=rec_qty
                ))
        return result

    @staticmethod
    def get_expiry_alerts(db: Session) -> List[ExpiryAlertResponse]:
        today = date.today()
        items = db.query(InventoryItem).filter(InventoryItem.expiry_date.isnot(None)).all()
        result = []
        for i in items:
            days_left = (i.expiry_date - today).days
            if days_left <= 60:
                result.append(ExpiryAlertResponse(
                    id=i.id,
                    name=i.name,
                    category=i.category or "General",
                    batch_number=i.batch_number,
                    current_stock=i.current_stock,
                    expiry_date=i.expiry_date.strftime("%Y-%m-%d"),
                    days_until_expiry=days_left
                ))
        result.sort(key=lambda x: x.days_until_expiry)
        return result

    @staticmethod
    def create_item(db: Session, item_in: InventoryItemCreate) -> InventoryItem:
        db_item = InventoryItem(**item_in.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


    @staticmethod
    def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[InventoryItem]:
        return db.query(InventoryItem).offset(skip).limit(limit).all()

    @staticmethod
    def get_item_by_id(db: Session, item_id: int) -> Optional[InventoryItem]:
        return db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
