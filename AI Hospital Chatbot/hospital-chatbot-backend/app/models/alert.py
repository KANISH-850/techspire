from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    severity = Column(String) # CRITICAL, HIGH, MEDIUM, LOW
    title = Column(String)
    description = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    metric = Column(String)
    value = Column(String)
    threshold = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active") # active, resolved

    department = relationship("Department", back_populates="alerts")
