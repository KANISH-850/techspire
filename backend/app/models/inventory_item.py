from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    sku = Column(String, unique=True, index=True, nullable=True)
    batch_number = Column(String, nullable=True)
    current_stock = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=10)
    maximum_stock = Column(Integer, default=100)
    daily_consumption = Column(Float, default=0.0)
    unit = Column(String, nullable=True)
    unit_price = Column(Float, default=0.0)
    expiry_date = Column(Date, nullable=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    vendor = relationship("Vendor", back_populates="inventory_items")
    purchase_order_items = relationship("PurchaseOrderItem", back_populates="inventory_item")
