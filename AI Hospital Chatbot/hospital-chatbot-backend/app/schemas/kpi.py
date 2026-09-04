from pydantic import BaseModel
from typing import Optional

class KPIValue(BaseModel):
    value: float
    previous: float
    change_percent: float
    trend: str # 'up', 'down', 'flat'

class KPISummary(BaseModel):
    total_revenue: KPIValue
    total_patients: KPIValue
    total_admissions: KPIValue
    total_discharges: KPIValue
    emergency_cases: KPIValue
    bed_occupancy: KPIValue
    available_beds: KPIValue
    patient_satisfaction: KPIValue
