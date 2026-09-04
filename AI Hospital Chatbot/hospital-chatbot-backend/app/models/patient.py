from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    admission_date = Column(DateTime, nullable=True)
    discharge_date = Column(DateTime, nullable=True)
    status = Column(String) # Admitted, Discharged, Outpatient
    satisfaction_score = Column(Float, nullable=True) # 1.0 to 10.0

    department = relationship("Department", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    admissions = relationship("Admission", back_populates="patient")

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

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    appointment_date = Column(DateTime)
    status = Column(String) # Scheduled, Completed, Cancelled

    patient = relationship("Patient", back_populates="appointments")
    department = relationship("Department", back_populates="appointments")
