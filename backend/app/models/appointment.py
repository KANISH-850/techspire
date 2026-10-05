from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    appointment_date = Column(DateTime)
    status = Column(String) # Scheduled, Completed, Cancelled

    patient = relationship("Patient", back_populates="appointments")
    department = relationship("Department", back_populates="appointments")
