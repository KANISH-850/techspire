from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.core.config import settings
from app.core.database import check_database_connection
from app.schemas.common import HealthResponse

router = APIRouter()

@router.get("", response_model=HealthResponse)
@router.get("/status", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        app=settings.APP_NAME,
        version=settings.APP_VERSION
    )

@router.get("/ready")
def readiness_check(db: Session = Depends(get_db)):
    db_ok = check_database_connection()
    return {
        "status": "ready" if db_ok else "degraded",
        "database": "healthy" if db_ok else "unhealthy",
        "app": settings.APP_NAME
    }
