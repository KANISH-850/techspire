import os
import pandas as pd
from typing import Dict, Any

class ExcelExporter:
    @staticmethod
    def generate(report_id: str, report_data: Dict[str, Any], output_path: str) -> str:
        file_path = os.path.join(output_path, f"{report_id}.xlsx")
        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Sheet 1: Executive Summary & Metadata
            summary_df = pd.DataFrame([
                {"Field": "Report Type", "Value": report_data.get('report_type', '').upper()},
                {"Field": "Date Range", "Value": report_data.get('date_range', '')},
                {"Field": "Generated On", "Value": report_data.get('generated_date', '')},
                {"Field": "Executive Summary", "Value": report_data.get('summary', '')},
            ])
            summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Sheet 2: KPIs
            kpi_data = [{"Metric": k.replace('_', ' ').title(), "Value": v} for k, v in report_data.get('kpis', {}).items()]
            kpi_df = pd.DataFrame(kpi_data)
            if not kpi_df.empty:
                kpi_df.to_excel(writer, sheet_name='KPIs', index=False)
                
            # Sheet 3: Detailed Data
            tables = report_data.get('tables', {})
            for table_name, records in tables.items():
                if records:
                    df = pd.DataFrame(records)
                    sheet_name = (table_name[:28] + '..') if len(table_name) > 31 else table_name
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    
            # Set column widths (basic formatting via openpyxl)
            for sheetname in writer.sheets:
                worksheet = writer.sheets[sheetname]
                for col in worksheet.columns:
                    max_length = 0
                    column = col[0].column_letter
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2) * 1.2
                    # Cap width
                    if adjusted_width > 50:
                        adjusted_width = 50
                    worksheet.column_dimensions[column].width = adjusted_width
                    
        return file_path
