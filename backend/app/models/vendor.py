from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_person = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    average_delivery_days = Column(Integer, default=5)
    reliability_score = Column(Float, default=100.0)
    rating = Column(Float, default=5.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    inventory_items = relationship("InventoryItem", back_populates="vendor")
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")
