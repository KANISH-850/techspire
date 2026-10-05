from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.dashboard import (
    KPISummary, RevenueInsights, DepartmentList, AlertList, AIInsights
)
from app.services.dashboard.dashboard_service import DashboardService

router = APIRouter()

@router.get("/kpis", response_model=KPISummary)
def get_kpis(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    department_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return DashboardService.calculate_kpis(db, start_date, end_date, department_id)

@router.get("/revenue", response_model=RevenueInsights)
def get_revenue(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    department_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return DashboardService.get_revenue_insights(db, start_date, end_date, department_id)

@router.get("/departments", response_model=DepartmentList)
def get_departments(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return DashboardService.get_department_performance(db, start_date, end_date)

@router.get("/alerts", response_model=AlertList)
def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return DashboardService.get_alerts(db)

@router.get("/ai-insights", response_model=AIInsights)
def get_ai_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return DashboardService.get_ai_insights(db)
