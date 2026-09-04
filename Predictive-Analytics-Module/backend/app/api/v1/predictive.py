from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.schemas.predictive import ForecastResponse, InventoryForecastItem
from app.services.predictive.revenue_forecaster import RevenueForecaster
from app.services.predictive.admissions_forecaster import AdmissionsForecaster
from app.services.predictive.bed_occupancy_forecaster import BedOccupancyForecaster
from app.services.predictive.medicine_demand_forecaster import MedicineDemandForecaster
from app.services.predictive.inventory_forecaster import InventoryForecaster
from predictive_config import settings

router = APIRouter()

def check_enabled():
    if not settings.PREDICTIVE_ANALYTICS_ENABLED:
        raise HTTPException(status_code=503, detail="Predictive Analytics Module is currently disabled.")

@router.get("/health")
async def health_check():
    check_enabled()
    return {
        "status": "online",
        "model_type": settings.MODEL_TYPE,
        "ollama_enabled": settings.OLLAMA_ENABLED,
        "version": "1.0.0"
    }

@router.get("/revenue", response_model=ForecastResponse)
async def get_revenue_forecast(days: int = 30):
    check_enabled()
    forecaster = RevenueForecaster()
    result = await forecaster.forecast(days=days)
    if not result:
        raise HTTPException(status_code=404, detail="Not enough data to generate forecast.")
    return result

@router.get("/admissions", response_model=ForecastResponse)
async def get_admissions_forecast(days: int = 30):
    check_enabled()
    forecaster = AdmissionsForecaster()
    result = await forecaster.forecast(days=days)
    if not result:
        raise HTTPException(status_code=404, detail="Not enough data to generate forecast.")
    return result

@router.get("/bed-occupancy", response_model=ForecastResponse)
async def get_bed_occupancy_forecast(days: int = 7):
    check_enabled()
    forecaster = BedOccupancyForecaster()
    result = await forecaster.forecast(days=days)
    if not result:
        raise HTTPException(status_code=404, detail="Not enough data to generate forecast.")
    return result

@router.get("/medicine-demand", response_model=List[dict])
async def get_medicine_demand_forecast(days: int = 30):
    check_enabled()
    forecaster = MedicineDemandForecaster()
    result = await forecaster.forecast(days=days)
    return result

@router.get("/inventory", response_model=List[InventoryForecastItem])
async def get_inventory_forecast():
    check_enabled()
    forecaster = InventoryForecaster()
    result = await forecaster.forecast()
    return result

@router.get("/summary")
async def get_predictive_summary():
    check_enabled()
    # Lightweight aggregation for dashboard overview
    rev = RevenueForecaster()
    adm = AdmissionsForecaster()
    bed = BedOccupancyForecaster()
    
    rev_res = await rev.forecast(days=7)
    adm_res = await adm.forecast(days=7)
    bed_res = await bed.forecast(days=7)
    
    return {
        "revenue_trend": rev_res.get("trend", "unknown"),
        "admissions_trend": adm_res.get("trend", "unknown"),
        "bed_occupancy_peak": max([x["value"] for x in bed_res.get("forecast", [])]) if bed_res.get("forecast") else 0
    }
