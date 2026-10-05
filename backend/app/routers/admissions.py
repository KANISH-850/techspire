from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.models.admission import Admission
from app.schemas.patient import AdmissionResponse

router = APIRouter()

@router.get("", response_model=List[AdmissionResponse])
def list_admissions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(Admission).offset(skip).limit(limit).all()

@router.get("/{admission_id}", response_model=AdmissionResponse)
def get_admission(
    admission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    adm = db.query(Admission).filter(Admission.id == admission_id).first()
    if not adm:
        raise HTTPException(status_code=404, detail="Admission record not found")
    return adm
