from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import List
from app.schemas.reports import ReportGenerateRequest, ReportResponse, ReportHistoryItem
from app.modules.reports.services.report_service import ReportService
from report_config import settings
import os

router = APIRouter()

def check_enabled():
    if not settings.REPORT_BUILDER_ENABLED:
        raise HTTPException(status_code=503, detail="Report Builder Module is currently disabled.")

@router.get("/health")
async def health_check():
    check_enabled()
    return {
        "status": "online",
        "ollama_enabled": settings.OLLAMA_ENABLED,
        "version": "1.0.0"
    }

@router.get("/types")
async def get_report_types():
    check_enabled()
    return ["financial", "clinical", "operational", "inventory", "procurement"]

@router.post("/generate", response_model=ReportResponse)
async def generate_report(req: ReportGenerateRequest):
    check_enabled()
    try:
        response = await ReportService.generate_report(req)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history", response_model=List[ReportHistoryItem])
async def get_report_history():
    check_enabled()
    return ReportService.get_history()

@router.get("/{report_id}/pdf")
async def download_pdf(report_id: str):
    check_enabled()
    file_path = os.path.join(settings.REPORT_STORAGE_PATH, f"{report_id}.pdf")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF not found.")
    return FileResponse(file_path, media_type="application/pdf", filename=f"{report_id}.pdf")

@router.get("/{report_id}/excel")
async def download_excel(report_id: str):
    check_enabled()
    file_path = os.path.join(settings.REPORT_STORAGE_PATH, f"{report_id}.xlsx")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Excel not found.")
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"{report_id}.xlsx")
