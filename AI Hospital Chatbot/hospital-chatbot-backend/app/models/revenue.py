from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    amount = Column(Float)
    transaction_type = Column(String) # 'revenue', 'expense'
    transaction_date = Column(DateTime, default=datetime.utcnow)

    department = relationship("Department", back_populates="transactions")

class HospitalExpense(Base):
    __tablename__ = "hospital_expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    expense_date = Column(DateTime, default=datetime.utcnow)
