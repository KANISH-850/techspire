from pydantic import BaseModel
from typing import List

class DepartmentPerformance(BaseModel):
    id: int
    name: str
    patient_count: int
    revenue: float
    occupancy: float
    satisfaction: float
    performance_score: float
    growth: float
    alert_status: str # CRITICAL, HIGH, MEDIUM, LOW

class DepartmentList(BaseModel):
    departments: List[DepartmentPerformance]
