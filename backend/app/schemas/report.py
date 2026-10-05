from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ReportGenerateRequest(BaseModel):
    report_type: str # financial, clinical, operational, inventory, procurement
    title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    department_id: Optional[int] = None
    format: str = "json" # json, pdf, excel

class ReportResponse(BaseModel):
    report_id: str
    report_type: str
    title: str
    generated_at: str
    executive_summary: str
    metrics: Dict[str, Any]
    data: List[Dict[str, Any]]
    pdf_url: Optional[str] = None
    excel_url: Optional[str] = None

class ReportHistoryItem(BaseModel):
    report_id: str
    report_type: str
    title: str
    generated_at: str
    pdf_available: bool
    excel_available: bool
