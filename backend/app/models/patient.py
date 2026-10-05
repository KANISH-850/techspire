from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    admission_date = Column(DateTime, nullable=True)
    discharge_date = Column(DateTime, nullable=True)
    status = Column(String) # Admitted, Discharged, Outpatient
    satisfaction_score = Column(Float, nullable=True) # 1.0 to 10.0

    department = relationship("Department", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    admissions = relationship("Admission", back_populates="patient", cascade="all, delete-orphan")
