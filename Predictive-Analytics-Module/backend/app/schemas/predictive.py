from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ForecastMetrics(BaseModel):
    mae: float
    rmse: float
    r2: float

class ForecastResponse(BaseModel):
    metric: str
    historical: List[Dict[str, Any]]
    forecast: List[Dict[str, Any]]
    trend: str
    metrics: ForecastMetrics
    explanation: Optional[str] = None
    
class InventoryForecastItem(BaseModel):
    medicine: str
    current_stock: float
    daily_consumption: float
    days_until_stockout: int
    risk: str
    recommended_reorder: float
    explanation: Optional[str] = None
