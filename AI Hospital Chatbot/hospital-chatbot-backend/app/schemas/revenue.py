from pydantic import BaseModel
from typing import List, Optional

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
    highest_revenue_department: Optional[DepartmentRevenue]
    lowest_revenue_department: Optional[DepartmentRevenue]
