from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    current_stock = Column(Integer, default=0)
    minimum_stock = Column(Integer, default=0)
    maximum_stock = Column(Integer, default=0)
    daily_consumption = Column(Float, default=0.0)
    unit_price = Column(Float, default=0.0)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    expiry_date = Column(Date)

    vendor = relationship("Vendor", back_populates="inventory_items")

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_email = Column(String)
    delivery_time_days = Column(Integer)
    reliability_score = Column(Float)
    rating = Column(Float)

    inventory_items = relationship("InventoryItem", back_populates="vendor")
    purchase_orders = relationship("PurchaseOrder", back_populates="vendor")

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    order_date = Column(DateTime)
    total_amount = Column(Float)
    status = Column(String)

    vendor = relationship("Vendor", back_populates="purchase_orders")
