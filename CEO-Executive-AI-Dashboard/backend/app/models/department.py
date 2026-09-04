from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

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

class Bed(Base):
    __tablename__ = "beds"
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    bed_number = Column(String)
    status = Column(String) # Occupied, Available, Maintenance

    department = relationship("Department", back_populates="beds")
