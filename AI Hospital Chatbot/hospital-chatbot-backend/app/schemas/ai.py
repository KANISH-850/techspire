from pydantic import BaseModel
from typing import List

class Risk(BaseModel):
    title: str
    severity: str
    description: str

class Recommendation(BaseModel):
    priority: str
    title: str
    reason: str
    supporting_metric: str
    expected_impact: str

class AIInsights(BaseModel):
    executive_summary: str
    hospital_status: str
    key_insights: List[str]
    risks: List[Risk]
    recommendations: List[Recommendation]
