from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime

class VendorBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    average_delivery_days: int
    reliability_score: float
    rating: float

class VendorResponse(VendorBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class InventoryItemBase(BaseModel):
    name: str
    category: str
    sku: str
    batch_number: Optional[str] = None
    current_stock: int
    minimum_stock: int
    maximum_stock: int
    unit: str
    unit_price: float
    expiry_date: Optional[date] = None
    vendor_id: Optional[int] = None

class InventoryItemResponse(InventoryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    vendor: Optional[VendorResponse] = None
    model_config = ConfigDict(from_attributes=True)

class PurchaseOrderItemBase(BaseModel):
    inventory_item_id: int
    quantity: int
    unit_price: float
    total_price: float

class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    id: int
    inventory_item: Optional[InventoryItemResponse] = None
    model_config = ConfigDict(from_attributes=True)

class PurchaseOrderBase(BaseModel):
    vendor_id: int
    status: str
    total_amount: float
    expected_delivery_date: Optional[datetime] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemBase]

class PurchaseOrderUpdate(BaseModel):
    status: str

class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    created_at: datetime
    vendor: Optional[VendorResponse] = None
    model_config = ConfigDict(from_attributes=True)
