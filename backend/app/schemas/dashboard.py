from pydantic import BaseModel
from typing import List, Optional

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

class MonthlyRevenue(BaseModel):
    month: str
    revenue: float

class DepartmentRevenue(BaseModel):
    department: str
    revenue: float

class RevenueInsights(BaseModel):
    total_revenue: float
    monthly: List[MonthlyRevenue]
    department_revenue: List[DepartmentRevenue]
    revenue_growth: float
    highest_revenue_department: Optional[DepartmentRevenue] = None
    lowest_revenue_department: Optional[DepartmentRevenue] = None

class DepartmentPerformance(BaseModel):
    id: int
    name: str
    patient_count: int
    admission_count: int
    discharge_count: int
    bed_occupancy_rate: float
    avg_satisfaction: float
    revenue: float

class DepartmentList(BaseModel):
    departments: List[DepartmentPerformance]

class AlertItem(BaseModel):
    id: int
    severity: str
    title: str
    description: str
    department_id: Optional[int] = None
    metric: Optional[str] = None
    value: Optional[str] = None
    threshold: Optional[str] = None
    created_at: str
    status: str

class AlertList(BaseModel):
    alerts: List[AlertItem]

class AIInsights(BaseModel):
    summary: str
    key_observations: List[str]
    recommendations: List[str]
