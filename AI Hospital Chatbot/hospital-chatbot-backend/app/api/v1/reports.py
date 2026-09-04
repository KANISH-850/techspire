from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.analytics import reports

router = APIRouter()

@router.get("/templates")
def get_report_templates():
    return [
        {"id": "financial", "name": "Financial Summary", "description": "Revenue and expense analysis"},
        {"id": "clinical", "name": "Clinical Summary", "description": "Patient and admission statistics"},
        {"id": "inventory", "name": "Inventory Summary", "description": "Current stock and consumption"},
        {"id": "procurement", "name": "Procurement Summary", "description": "Vendor performance and purchase orders"}
    ]

@router.get("/generate")
def generate_report(
    type: str = Query(..., description="financial, clinical, inventory, or procurement"),
    format: str = Query("pdf", description="pdf or excel"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    if type == "financial":
        output = reports.generate_financial_report(db, format, start_date, end_date)
        filename = f"financial_report.{format}"
    elif type == "clinical":
        output = reports.generate_clinical_report(db, format, start_date, end_date)
        filename = f"clinical_report.{format}"
    elif type == "inventory":
        output = reports.generate_inventory_report(db, format, start_date, end_date)
        filename = f"inventory_report.{format}"
    elif type == "procurement":
        output = reports.generate_procurement_report(db, format, start_date, end_date)
        filename = f"procurement_report.{format}"
    else:
        return {"error": "Invalid report type"}

    media_type = "application/pdf" if format == "pdf" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    return StreamingResponse(
        output,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
