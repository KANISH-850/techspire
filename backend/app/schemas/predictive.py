from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ForecastPoint(BaseModel):
    date: str
    value: float

class ForecastMetrics(BaseModel):
    mae: float
    rmse: float
    r2: float

class ForecastResponse(BaseModel):
    metric: str
    historical: List[ForecastPoint]
    forecast: List[ForecastPoint]
    trend: str
    metrics: ForecastMetrics
    explanation: str
    algorithm: str = "Scikit-learn LinearRegression"
    data_source: str = "POSTGRESQL_DB"
    data_quality: str = "HISTORICAL" # HISTORICAL, RECONSTRUCTED, RULE_BASED_SNAPSHOT

class MedicineForecastItem(BaseModel):
    name: str
    category: str
    historical_daily_avg: float
    projected_daily_demand: float
    predicted_30day_total: float
    trend: str
    recommendation: str
    data_source: str = "POSTGRESQL_DB"

class InventoryForecastItem(BaseModel):
    name: str
    category: str
    current_stock: int
    minimum_stock: int
    daily_consumption: float
    days_until_stockout: int
    risk_level: str # CRITICAL, HIGH, MODERATE, LOW
    recommended_reorder_qty: int
    data_source: str = "POSTGRESQL_DB"

class PredictiveSummaryResponse(BaseModel):
    revenue_trend: str
    admissions_trend: str
    bed_occupancy_peak: float
    data_source: str = "POSTGRESQL_DB"

