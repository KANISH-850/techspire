from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    budget = Column(Float, default=0.0)

    patients = relationship("Patient", back_populates="department")
    appointments = relationship("Appointment", back_populates="department")
    beds = relationship("Bed", back_populates="department")
    transactions = relationship("Transaction", back_populates="department")
    admissions = relationship("Admission", back_populates="department")
    alerts = relationship("Alert", back_populates="department")
