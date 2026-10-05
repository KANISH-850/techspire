from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class InventoryItemBase(BaseModel):
    name: str
    category: str
    sku: Optional[str] = None
    batch_number: Optional[str] = None
    current_stock: int = 0
    minimum_stock: int = 10
    maximum_stock: int = 100
    daily_consumption: float = 0.0
    unit: Optional[str] = "Units"
    unit_price: float = 0.0
    expiry_date: Optional[date] = None
    vendor_id: Optional[int] = None

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemResponse(InventoryItemBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InventoryStatusResponse(BaseModel):
    total_items: int
    total_value: float
    low_stock_count: int
    expiring_soon_count: int

class LowStockItemResponse(BaseModel):
    id: int
    name: str
    category: str
    current_stock: int
    minimum_stock: int
    daily_consumption: float
    reorder_recommended_qty: int

class ExpiryAlertResponse(BaseModel):
    id: int
    name: str
    category: str
    batch_number: Optional[str] = None
    current_stock: int
    expiry_date: str
    days_until_expiry: int
