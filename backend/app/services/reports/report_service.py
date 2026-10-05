import uuid
import os
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models import Transaction, Patient, Admission, InventoryItem, PurchaseOrder, Department
from app.schemas.report import ReportGenerateRequest, ReportResponse, ReportHistoryItem
from app.services.reports.filter_engine import FilterEngine
from app.services.reports.pdf_exporter import PDFExporter
from app.services.reports.excel_exporter import ExcelExporter
from app.core.config import settings

_report_history: List[Dict[str, Any]] = []

class ReportService:
    @staticmethod
    async def generate_report(req: ReportGenerateRequest, db: Session) -> ReportResponse:
        report_id = f"REP-{uuid.uuid4().hex[:8].upper()}"
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        r_type = req.report_type.lower()
        title = req.title or f"Executive {r_type.title()} Report"

        metrics: Dict[str, Any] = {}
        data_records: List[Dict[str, Any]] = []
        summary = ""

        if r_type == "financial":
            txs = db.query(Transaction).all()
            formatted = [{
                "id": t.id,
                "department_id": t.department_id,
                "amount": t.amount,
                "transaction_type": t.transaction_type,
                "transaction_date": t.transaction_date.isoformat() if t.transaction_date else ""
            } for t in txs]

            filtered = FilterEngine.filter_by_date(formatted, "transaction_date", req.start_date, req.end_date)
            total_rev = sum(x["amount"] for x in filtered if x["transaction_type"] == "revenue")
            total_exp = sum(x["amount"] for x in filtered if x["transaction_type"] == "expense")
            net_income = total_rev - total_exp

            metrics = {
                "total_revenue": round(total_rev, 2),
                "total_expenses": round(total_exp, 2),
                "net_income": round(net_income, 2),
                "transaction_count": len(filtered)
            }
            data_records = filtered
            summary = f"Financial audit generated {len(filtered)} transactions totaling ${total_rev:,.2f} in revenue and ${total_exp:,.2f} in expenses."

        elif r_type in ["clinical", "operational"]:
            patients = db.query(Patient).all()
            formatted = [{
                "id": p.id,
                "name": p.name,
                "age": p.age,
                "gender": p.gender,
                "status": p.status,
                "satisfaction_score": p.satisfaction_score,
                "admission_date": p.admission_date.isoformat() if p.admission_date else ""
            } for p in patients]

            filtered = FilterEngine.filter_by_date(formatted, "admission_date", req.start_date, req.end_date)
            admitted_count = sum(1 for x in filtered if x["status"] == "Admitted")
            discharged_count = sum(1 for x in filtered if x["status"] == "Discharged")
            avg_sat = sum(x["satisfaction_score"] for x in filtered if x["satisfaction_score"]) / max(1, len(filtered))

            metrics = {
                "total_patients_analyzed": len(filtered),
                "currently_admitted": admitted_count,
                "discharged_patients": discharged_count,
                "avg_satisfaction": round(avg_sat, 2)
            }
            data_records = filtered
            summary = f"Clinical metrics evaluation covers {len(filtered)} patient records with an average satisfaction rating of {avg_sat:.1f}/10."

        elif r_type == "inventory":
            items = db.query(InventoryItem).all()
            formatted = [{
                "id": i.id,
                "name": i.name,
                "category": i.category,
                "current_stock": i.current_stock,
                "minimum_stock": i.minimum_stock,
                "unit_price": i.unit_price,
                "total_val": i.current_stock * i.unit_price
            } for i in items]

            total_val = sum(x["total_val"] for x in formatted)
            low_stock = sum(1 for x in formatted if x["current_stock"] <= x["minimum_stock"])

            metrics = {
                "total_inventory_items": len(formatted),
                "total_valuation": round(total_val, 2),
                "low_stock_items": low_stock
            }
            data_records = formatted
            summary = f"Inventory audit tracks {len(formatted)} SKUs with a total valuation of ${total_val:,.2f}. {low_stock} items require reorder."

        elif r_type == "procurement":
            pos = db.query(PurchaseOrder).all()
            formatted = [{
                "id": p.id,
                "vendor_id": p.vendor_id,
                "status": p.status,
                "total_amount": p.total_amount,
                "created_at": p.created_at.isoformat() if p.created_at else ""
            } for p in pos]

            total_spend = sum(x["total_amount"] for x in formatted)
            pending = sum(1 for x in formatted if x["status"] in ["Draft", "Pending"])

            metrics = {
                "total_purchase_orders": len(formatted),
                "total_spend": round(total_spend, 2),
                "pending_orders": pending
            }
            data_records = formatted
            summary = f"Procurement analysis summarizes {len(formatted)} purchase orders totaling ${total_spend:,.2f} in commitment."

        else:
            metrics = {"count": 0}
            summary = f"Custom report generated for {r_type}."

        storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "storage", "reports"))
        os.makedirs(storage_dir, exist_ok=True)

        pdf_path = os.path.join(storage_dir, f"{report_id}.pdf")
        excel_path = os.path.join(storage_dir, f"{report_id}.xlsx")

        report_payload = {
            "report_id": report_id,
            "report_type": r_type,
            "title": title,
            "generated_at": now_str,
            "executive_summary": summary,
            "metrics": metrics,
            "data": data_records
        }

        pdf_url = None
        excel_url = None

        if req.format.lower() in ["pdf", "all"]:
            PDFExporter.export(report_payload, pdf_path)
            pdf_url = f"{settings.API_V1_STR}/reports/{report_id}/pdf"

        if req.format.lower() in ["excel", "xlsx", "all"]:
            ExcelExporter.export(report_payload, excel_path)
            excel_url = f"{settings.API_V1_STR}/reports/{report_id}/excel"

        _report_history.append({
            "report_id": report_id,
            "report_type": r_type,
            "title": title,
            "generated_at": now_str,
            "pdf_available": os.path.exists(pdf_path),
            "excel_available": os.path.exists(excel_path)
        })

        return ReportResponse(
            report_id=report_id,
            report_type=r_type,
            title=title,
            generated_at=now_str,
            executive_summary=summary,
            metrics=metrics,
            data=data_records[:50], # Sample 50 records in API response
            pdf_url=pdf_url,
            excel_url=excel_url
        )

    @staticmethod
    def get_history() -> List[ReportHistoryItem]:
        return [ReportHistoryItem(**item) for item in reversed(_report_history)]
