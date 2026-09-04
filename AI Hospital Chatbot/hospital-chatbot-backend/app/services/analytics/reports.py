import io
import pandas as pd
from datetime import datetime, timezone
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.widgets.markers import makeMarker
from sqlalchemy.orm import Session
from app.models import Transaction, Patient, Department, InventoryItem, PurchaseOrder, Vendor
from app.services.ai import get_ai_provider

def generate_financial_report(db: Session, format_type: str = "pdf", start_date: str = None, end_date: str = None):
    query = db.query(Transaction).order_by(Transaction.transaction_date.desc())
    if start_date:
        query = query.filter(Transaction.transaction_date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Transaction.transaction_date <= datetime.fromisoformat(end_date))
    transactions = query.limit(100).all()
    
    provider = get_ai_provider()
    summary = provider.generate_insights({"task": "Summarize financial data", "total_records": len(transactions), "module": "Financial Report"})
    exec_summary = summary.get("executive_summary", "Financial Report Generated")

    if format_type == "excel":
        output = io.BytesIO()
        data = [{"ID": t.id, "Date": t.transaction_date.strftime('%Y-%m-%d'), "Type": t.transaction_type, "Amount": t.amount, "Dept ID": t.department_id} for t in transactions]
        df = pd.DataFrame(data)
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Financial Report', index=False)
        output.seek(0)
        return output
        
    elif format_type == "pdf":
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("Hospital Financial Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Generated on: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Executive Summary", styles['Heading2']))
        elements.append(Paragraph(exec_summary, styles['Normal']))
        elements.append(Spacer(1, 20))
        
        if transactions:
            # Simple Chart (Revenue Trend)
            drawing = Drawing(400, 200)
            lp = LinePlot()
            lp.x = 50
            lp.y = 50
            lp.height = 125
            lp.width = 300
            
            # Group by date for chart (simple trend)
            revs = [t for t in transactions if t.transaction_type == 'revenue']
            revs.reverse() # chronological
            chart_data = [(i, float(t.amount)) for i, t in enumerate(revs[:20])]
            
            if chart_data:
                lp.data = [chart_data]
                lp.lines[0].strokeColor = colors.blue
                lp.lines[0].symbol = makeMarker('FilledCircle')
                drawing.add(lp)
                elements.append(drawing)
                elements.append(Spacer(1, 20))
        
        # Table
        data = [["ID", "Date", "Type", "Amount"]]
        for t in transactions[:30]: # Limit to 30 for PDF demo
            data.append([str(t.id), t.transaction_date.strftime('%Y-%m-%d'), t.transaction_type, f"${t.amount:.2f}"])
            
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        output.seek(0)
        return output

def generate_clinical_report(db: Session, format_type: str = "pdf", start_date: str = None, end_date: str = None):
    query = db.query(Patient).order_by(Patient.admission_date.desc())
    if start_date:
        query = query.filter(Patient.admission_date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Patient.admission_date <= datetime.fromisoformat(end_date))
    patients = query.limit(100).all()
    
    provider = get_ai_provider()
    summary = provider.generate_insights({"task": "Summarize clinical data", "total_patients": len(patients), "module": "Clinical Report"})
    exec_summary = summary.get("executive_summary", "Clinical Report Generated")

    if format_type == "excel":
        output = io.BytesIO()
        data = [{"ID": p.id, "Name": p.name, "Age": p.age, "Gender": p.gender, "Status": p.status, "Admitted": p.admission_date.strftime('%Y-%m-%d') if p.admission_date else ""} for p in patients]
        df = pd.DataFrame(data)
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Clinical Report', index=False)
        output.seek(0)
        return output
        
    elif format_type == "pdf":
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("Hospital Clinical Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Generated on: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Executive Summary", styles['Heading2']))
        elements.append(Paragraph(exec_summary, styles['Normal']))
        elements.append(Spacer(1, 20))
        
        data = [["ID", "Name", "Age", "Status"]]
        for p in patients[:30]:
            data.append([str(p.id), p.name, str(p.age), p.status])
            
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        output.seek(0)
        return output

def generate_inventory_report(db: Session, format_type: str = "pdf", start_date: str = None, end_date: str = None):
    # inventory is current status, dates are less relevant, but we can query standard
    items = db.query(InventoryItem).all()
    
    provider = get_ai_provider()
    summary = provider.generate_insights({"task": "Summarize inventory data", "total_items": len(items), "module": "Inventory Report"})
    exec_summary = summary.get("executive_summary", "Inventory Report Generated")

    if format_type == "excel":
        output = io.BytesIO()
        data = [{"ID": i.id, "Name": i.name, "Stock": i.current_stock, "Min": i.minimum_stock, "Price": i.unit_price} for i in items]
        df = pd.DataFrame(data)
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Inventory Report', index=False)
        output.seek(0)
        return output
        
    elif format_type == "pdf":
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("Hospital Inventory Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Generated on: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Executive Summary", styles['Heading2']))
        elements.append(Paragraph(exec_summary, styles['Normal']))
        elements.append(Spacer(1, 20))
        
        data = [["ID", "Name", "Stock", "Status"]]
        for i in items[:30]:
            status = "Low" if i.current_stock <= i.minimum_stock else "OK"
            data.append([str(i.id), i.name, str(i.current_stock), status])
            
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        output.seek(0)
        return output

def generate_procurement_report(db: Session, format_type: str = "pdf", start_date: str = None, end_date: str = None):
    query = db.query(PurchaseOrder).order_by(PurchaseOrder.order_date.desc())
    if start_date:
        query = query.filter(PurchaseOrder.order_date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(PurchaseOrder.order_date <= datetime.fromisoformat(end_date))
    orders = query.limit(100).all()
    
    provider = get_ai_provider()
    summary = provider.generate_insights({"task": "Summarize procurement data", "total_orders": len(orders), "module": "Procurement Report"})
    exec_summary = summary.get("executive_summary", "Procurement Report Generated")

    if format_type == "excel":
        output = io.BytesIO()
        data = [{"PO ID": o.id, "Date": o.order_date.strftime('%Y-%m-%d') if o.order_date else "", "Vendor ID": o.vendor_id, "Amount": o.total_amount, "Status": o.status} for o in orders]
        df = pd.DataFrame(data)
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Procurement Report', index=False)
        output.seek(0)
        return output
        
    elif format_type == "pdf":
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("Hospital Procurement Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Generated on: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Executive Summary", styles['Heading2']))
        elements.append(Paragraph(exec_summary, styles['Normal']))
        elements.append(Spacer(1, 20))
        
        data = [["PO ID", "Date", "Vendor ID", "Amount"]]
        for o in orders[:30]:
            data.append([str(o.id), o.order_date.strftime('%Y-%m-%d') if o.order_date else "", str(o.vendor_id), f"${o.total_amount:.2f}" if o.total_amount else "$0.00"])
            
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightpink),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        output.seek(0)
        return output
