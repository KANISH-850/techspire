import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.report import ReportGenerateRequest, ReportResponse, ReportHistoryItem
from app.services.reports.report_service import ReportService

router = APIRouter()

@router.get("/types")
def get_report_types(current_user: User = Depends(get_current_active_user)):
    return ["financial", "clinical", "operational", "inventory", "procurement"]

@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    req: ReportGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        return await ReportService.generate_report(req, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history", response_model=List[ReportHistoryItem])
def get_report_history(current_user: User = Depends(get_current_active_user)):
    return ReportService.get_history()

@router.get("/{report_id}/pdf")
def download_pdf(
    report_id: str,
    current_user: User = Depends(get_current_active_user)
):
    storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage", "reports"))
    file_path = os.path.join(storage_dir, f"{report_id}.pdf")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF report file not found")
    return FileResponse(file_path, media_type="application/pdf", filename=f"{report_id}.pdf")

@router.get("/{report_id}/excel")
def download_excel(
    report_id: str,
    current_user: User = Depends(get_current_active_user)
):
    storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage", "reports"))
    file_path = os.path.join(storage_dir, f"{report_id}.xlsx")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Excel report file not found")
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"{report_id}.xlsx")
