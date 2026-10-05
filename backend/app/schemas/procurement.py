from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.inventory import InventoryItemResponse

class VendorBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    average_delivery_days: int = 5
    reliability_score: float = 100.0
    rating: float = 5.0

class VendorCreate(VendorBase):
    pass

class VendorResponse(VendorBase):
    id: int

    class Config:
        from_attributes = True

class VendorAnalysisResponse(VendorBase):
    id: int
    active_purchase_orders_count: int

class PurchaseOrderItemBase(BaseModel):
    inventory_item_id: int
    quantity: int
    unit_price: float
    total_price: float

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: int
    inventory_item: Optional[InventoryItemResponse] = None

    class Config:
        from_attributes = True

class PurchaseOrderCreate(BaseModel):
    vendor_id: int
    status: str = "Draft"
    total_amount: float
    expected_delivery_date: Optional[datetime] = None
    items: List[PurchaseOrderItemCreate]

class PurchaseOrderUpdate(BaseModel):
    status: str

class PurchaseOrderResponse(BaseModel):
    id: int
    vendor_id: int
    status: str
    total_amount: float
    created_at: Optional[datetime] = None
    expected_delivery_date: Optional[datetime] = None
    vendor: Optional[VendorResponse] = None
    items: List[PurchaseOrderItemResponse] = []

    class Config:
        from_attributes = True

class AIProcurementRecommendation(BaseModel):
    summary: str
    suggested_orders: List[dict]
    cost_optimization_tips: List[str]
