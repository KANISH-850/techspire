from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.analytics import kpi, revenue, departments, alerts
from app.services.ai import get_ai_provider
from app.schemas import KPISummary, RevenueInsights, DepartmentList, AlertList, AIInsights

router = APIRouter()

@router.get("/kpis", response_model=KPISummary)
def get_kpis(
    start_date: str = Query(None),
    end_date: str = Query(None),
    department_id: int = Query(None),
    db: Session = Depends(get_db)
):
    return kpi.calculate_kpis(db, start_date, end_date, department_id)

@router.get("/revenue", response_model=RevenueInsights)
def get_revenue(
    start_date: str = Query(None),
    end_date: str = Query(None),
    department_id: int = Query(None),
    db: Session = Depends(get_db)
):
    return revenue.get_revenue_insights(db, start_date, end_date, department_id)

@router.get("/departments", response_model=DepartmentList)
def get_departments(
    start_date: str = Query(None),
    end_date: str = Query(None),
    db: Session = Depends(get_db)
):
    return departments.get_department_performance(db, start_date, end_date)

@router.get("/alerts", response_model=AlertList)
def get_alerts(db: Session = Depends(get_db)):
    return alerts.generate_alerts(db)

@router.get("/ai-insights", response_model=AIInsights)
def get_ai_insights(db: Session = Depends(get_db)):
    agg_data = {
        "kpis": kpi.calculate_kpis(db).dict(),
        "alerts": [alert.dict() for alert in alerts.generate_alerts(db).alerts],
        "departments": [dept.dict() for dept in departments.get_department_performance(db).departments]
    }
    provider = get_ai_provider()
    return provider.generate_insights(agg_data)
