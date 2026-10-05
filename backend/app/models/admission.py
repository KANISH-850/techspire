from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    admission_date = Column(DateTime)
    discharge_date = Column(DateTime, nullable=True)
    status = Column(String) # Admitted, Discharged

    patient = relationship("Patient", back_populates="admissions")
    department = relationship("Department", back_populates="admissions")
