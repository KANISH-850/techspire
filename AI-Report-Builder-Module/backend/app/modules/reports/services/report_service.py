import uuid
from datetime import datetime
from typing import Dict, Any
from app.schemas.reports import ReportGenerateRequest, ReportResponse, ChartData
from app.modules.reports.services.filter_engine import FilterEngine
from app.modules.reports.analytics.ai_summary import AISummaryService
from app.modules.reports.analytics.financial_analytics import FinancialAnalytics
from app.modules.reports.analytics.clinical_analytics import ClinicalAnalytics
from app.modules.reports.analytics.operational_analytics import OperationalAnalytics
from app.modules.reports.analytics.inventory_analytics import InventoryAnalytics
from app.modules.reports.analytics.procurement_analytics import ProcurementAnalytics
from app.modules.reports.exporters.pdf_exporter import PdfExporter
from app.modules.reports.exporters.excel_exporter import ExcelExporter
from report_config import settings
import json
import os

class ReportService:
    HISTORY_FILE = os.path.join(settings.REPORT_STORAGE_PATH, "history.json")
    
    @classmethod
    def _get_history(cls) -> list:
        if os.path.exists(cls.HISTORY_FILE):
            with open(cls.HISTORY_FILE, 'r') as f:
                return json.load(f)
        return []
        
    @classmethod
    def _save_history(cls, record: dict):
        history = cls._get_history()
        history.append(record)
        with open(cls.HISTORY_FILE, 'w') as f:
            json.dump(history, f)
            
    @classmethod
    async def generate_report(cls, req: ReportGenerateRequest) -> ReportResponse:
        report_id = str(uuid.uuid4())
        generated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_range_str = f"{req.start_date} to {req.end_date}"
        
        # 1. Apply Filters
        try:
            df = FilterEngine.apply_filters(req.report_type, req.start_date, req.end_date, req.department)
        except Exception as e:
            raise ValueError(f"Failed to apply filters: {str(e)}")
            
        # 2. Get Analytics Engine
        if req.report_type == "financial":
            analytics = FinancialAnalytics(df)
        elif req.report_type == "clinical":
            analytics = ClinicalAnalytics(df)
        elif req.report_type == "operational":
            analytics = OperationalAnalytics(df)
        elif req.report_type == "inventory":
            analytics = InventoryAnalytics(df)
        elif req.report_type == "procurement":
            analytics = ProcurementAnalytics(df)
        else:
            raise ValueError("Unsupported report type.")
            
        # 3. Calculate KPIs and Context
        kpis = analytics.generate_kpis()
        context = analytics.generate_context_for_llm()
        fallback_summary = analytics.get_fallback_summary()
        
        # 4. Generate Summary
        summary = await AISummaryService.generate_summary(req.report_type, context, fallback_summary)
        
        # 5. Get Charts & Tables
        charts = analytics.generate_charts()
        table_data = analytics.get_table_data()
        
        # Construct raw payload
        report_data = {
            "report_id": report_id,
            "report_type": req.report_type,
            "date_range": date_range_str,
            "generated_date": generated_date,
            "summary": summary,
            "kpis": kpis,
            "tables": {"Data": table_data}
        }
        
        # 6. Export if requested
        download_url = None
        if req.format == "pdf":
            PdfExporter.generate(report_id, report_data, settings.REPORT_STORAGE_PATH)
            download_url = f"/api/v1/reports/{report_id}/pdf"
        elif req.format == "excel":
            ExcelExporter.generate(report_id, report_data, settings.REPORT_STORAGE_PATH)
            download_url = f"/api/v1/reports/{report_id}/excel"
            
        # 7. Save History
        cls._save_history({
            "report_id": report_id,
            "report_type": req.report_type.title() + " Report",
            "generated_date": generated_date,
            "date_range": date_range_str,
            "format": req.format.upper(),
            "status": "Completed"
        })
        
        return ReportResponse(
            report_id=report_id,
            report_type=req.report_type,
            format=req.format,
            status="completed",
            download_url=download_url,
            summary=summary,
            kpis=kpis,
            charts=[ChartData(**c) for c in charts],
            tables={"Data": table_data[:100]} # Limit preview table to 100 rows
        )
        
    @classmethod
    def get_history(cls):
        return sorted(cls._get_history(), key=lambda x: x['generated_date'], reverse=True)
