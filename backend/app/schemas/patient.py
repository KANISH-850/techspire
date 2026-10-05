from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.department import DepartmentResponse

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    department_id: Optional[int] = None
    status: str = "Outpatient"
    satisfaction_score: Optional[float] = None

class PatientCreate(PatientBase):
    pass

class AdmissionResponse(BaseModel):
    id: int
    patient_id: int
    department_id: int
    admission_date: datetime
    discharge_date: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    department_id: int
    appointment_date: datetime
    status: str

    class Config:
        from_attributes = True

class PatientResponse(PatientBase):
    id: int
    admission_date: Optional[datetime] = None
    discharge_date: Optional[datetime] = None
    department: Optional[DepartmentResponse] = None

    class Config:
        from_attributes = True
