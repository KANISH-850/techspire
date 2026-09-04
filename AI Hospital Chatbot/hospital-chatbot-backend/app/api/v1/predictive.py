from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.analytics import predictive

router = APIRouter()

@router.get("/revenue")
def get_revenue_prediction(days_ahead: int = Query(30), db: Session = Depends(get_db)):
    return predictive.predict_revenue(db, days_ahead)

@router.get("/admissions")
def get_admissions_prediction(days_ahead: int = Query(30), db: Session = Depends(get_db)):
    return predictive.predict_admissions(db, days_ahead)

@router.get("/beds")
def get_beds_prediction(days_ahead: int = Query(30), db: Session = Depends(get_db)):
    return predictive.predict_beds(db, days_ahead)

@router.get("/medicines")
def get_medicines_prediction(days_ahead: int = Query(30), db: Session = Depends(get_db)):
    return predictive.predict_medicines(db, days_ahead)

@router.get("/inventory")
def get_inventory_prediction(days_ahead: int = Query(30), db: Session = Depends(get_db)):
    return predictive.predict_inventory(db, days_ahead)
