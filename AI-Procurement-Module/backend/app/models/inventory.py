from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.sql import func
from app.database import Base

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    sku = Column(String, unique=True, index=True)
    batch_number = Column(String)
    current_stock = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=10)
    maximum_stock = Column(Integer, default=100)
    unit = Column(String)
    unit_price = Column(Float, default=0.0)
    expiry_date = Column(Date, nullable=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
