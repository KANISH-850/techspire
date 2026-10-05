from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.predictive import (
    ForecastResponse, MedicineForecastItem, InventoryForecastItem, PredictiveSummaryResponse
)
from app.services.predictive.predictive_service import PredictiveService

router = APIRouter()

@router.get("/revenue", response_model=ForecastResponse)
async def get_revenue_forecast(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    res = await PredictiveService.get_revenue_forecast(days=days, db=db)
    if not res:
        raise HTTPException(status_code=404, detail="Not enough data for revenue forecast")
    return res

@router.get("/admissions", response_model=ForecastResponse)
async def get_admissions_forecast(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    res = await PredictiveService.get_admissions_forecast(days=days, db=db)
    if not res:
        raise HTTPException(status_code=404, detail="Not enough data for admissions forecast")
    return res

@router.get("/beds", response_model=ForecastResponse)
@router.get("/bed-occupancy", response_model=ForecastResponse)
async def get_bed_occupancy_forecast(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    res = await PredictiveService.get_bed_occupancy_forecast(days=days, db=db)
    if not res:
        raise HTTPException(status_code=404, detail="Not enough data for bed forecast")
    return res

@router.get("/medicines", response_model=List[MedicineForecastItem])
@router.get("/medicine-demand", response_model=List[MedicineForecastItem])
async def get_medicine_demand_forecast(
    days: int = Query(30, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await PredictiveService.get_medicine_demand_forecast(days=days, db=db)

@router.get("/inventory", response_model=List[InventoryForecastItem])
async def get_inventory_forecast(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await PredictiveService.get_inventory_forecast(db=db)

@router.get("/summary", response_model=PredictiveSummaryResponse)
async def get_predictive_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await PredictiveService.get_summary(db=db)

