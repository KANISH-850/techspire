import os
import logging
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

logger = logging.getLogger(__name__)

class PDFExporter:
    @staticmethod
    def export(data: Dict[str, Any], output_path: str) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#0284c7'),
            spaceAfter=12
        )

        heading_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=10,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#334155')
        )

        elements = []

        # Title
        title_text = data.get("title", "Hospital Executive Report")
        elements.append(Paragraph(title_text, title_style))

        # Meta
        meta_text = f"Report ID: {data.get('report_id')} | Generated: {data.get('generated_at')} | Type: {data.get('report_type')}"
        elements.append(Paragraph(meta_text, body_style))
        elements.append(Spacer(1, 12))

        # Executive Summary
        elements.append(Paragraph("Executive Summary", heading_style))
        summary_text = data.get("executive_summary", "No summary provided.")
        elements.append(Paragraph(summary_text, body_style))
        elements.append(Spacer(1, 12))

        # Metrics Table
        metrics = data.get("metrics", {})
        if metrics:
            elements.append(Paragraph("Key Performance Metrics", heading_style))
            table_data = [["Metric", "Value"]]
            for k, v in metrics.items():
                table_data.append([str(k).replace('_', ' ').title(), str(v)])

            t = Table(table_data, colWidths=[200, 300])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 12))

        # Records Table
        records = data.get("data", [])
        if records and isinstance(records, list):
            elements.append(Paragraph("Report Records", heading_style))
            keys = list(records[0].keys())[:5]
            rec_table_data = [[str(k).replace('_', ' ').title() for k in keys]]
            for row in records[:20]:
                rec_table_data.append([str(row.get(k, '')) for k in keys])

            t_rec = Table(rec_table_data)
            t_rec.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ]))
            elements.append(t_rec)

        doc.build(elements)
        return output_path
