from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

class VendorBase(BaseModel):
    id: int
    name: str
    contact_email: Optional[str] = None
    delivery_time_days: Optional[int] = None
    reliability_score: Optional[float] = None
    rating: Optional[float] = None
    
    class Config:
        from_attributes = True

class VendorAnalysis(VendorBase):
    purchase_orders_count: int
    total_purchase_value: float

class InventoryItemBase(BaseModel):
    id: int
    name: str
    category: str
    current_stock: int
    minimum_stock: int
    maximum_stock: int
    daily_consumption: float
    unit_price: float
    vendor_id: int
    expiry_date: Optional[date] = None
    
    class Config:
        from_attributes = True

class InventoryItemStatus(InventoryItemBase):
    status: str
    vendor_name: str

class LowStockItem(BaseModel):
    item: InventoryItemBase
    current_stock: int
    minimum_stock: int
    shortage: int
    recommended_reorder_quantity: int
    severity: str

class LowStockResponse(BaseModel):
    items: List[LowStockItem]

class ExpiringItem(BaseModel):
    item: InventoryItemBase
    expiry_date: date
    days_remaining: int
    severity: str

class ExpiringResponse(BaseModel):
    expired_items: List[ExpiringItem]
    expiring_soon_items: List[ExpiringItem]

class ReorderSuggestion(BaseModel):
    item: InventoryItemBase
    current_stock: int
    minimum_stock: int
    recommended_quantity: int
    reason: str

class PurchaseOrderCreate(BaseModel):
    vendor_id: int
    items: List[dict] # Not fully structured yet since PO doesn't have line items in schema, but total_amount is stored
    total_amount: float

class PurchaseOrderResponse(BaseModel):
    id: int
    vendor_id: int
    order_date: datetime
    total_amount: float
    status: str
    
    class Config:
        from_attributes = True
