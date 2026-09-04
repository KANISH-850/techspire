from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ReportGenerateRequest(BaseModel):
    report_type: str # financial, clinical, operational, inventory, procurement
    start_date: str
    end_date: str
    department: Optional[str] = "all"
    format: str # pdf, excel, preview

class ChartData(BaseModel):
    title: str
    type: str # line, bar, pie
    data: List[Dict[str, Any]]

class ReportResponse(BaseModel):
    report_id: str
    report_type: str
    format: str
    status: str
    download_url: Optional[str] = None
    summary: str
    kpis: Dict[str, Any]
    charts: List[ChartData]
    tables: Dict[str, List[Dict[str, Any]]]

class ReportHistoryItem(BaseModel):
    report_id: str
    report_type: str
    generated_date: str
    date_range: str
    format: str
    status: str
