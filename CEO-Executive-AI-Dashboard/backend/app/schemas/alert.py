from pydantic import BaseModel
from typing import List
from datetime import datetime

class AlertBase(BaseModel):
    severity: str
    title: str
    description: str
    department: str
    metric: str
    value: str
    threshold: str
    created_at: datetime
    status: str
    recommended_action: str

class AlertList(BaseModel):
    alerts: List[AlertBase]
