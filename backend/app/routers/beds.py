from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.models.bed import Bed
from app.schemas.department import BedResponse

router = APIRouter()

@router.get("", response_model=List[BedResponse])
def list_beds(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(Bed).offset(skip).limit(limit).all()

@router.get("/{bed_id}", response_model=BedResponse)
def get_bed(
    bed_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    b = db.query(Bed).filter(Bed.id == bed_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bed not found")
    return b
