from .base import BaseReportAnalytics
import pandas as pd

class ProcurementAnalytics(BaseReportAnalytics):
    def generate_kpis(self):
        if self.df.empty:
            return {"total_orders": 0, "total_value": 0, "pending_orders": 0}
            
        return {
            "total_orders": len(self.df),
            "total_value": round(self.df['purchase_value'].sum(), 2),
            "pending_orders": len(self.df[self.df['status'].str.lower() == 'pending'])
        }
        
    def generate_charts(self):
        if self.df.empty:
            return []
            
        vendor_vol = self.df.groupby('vendor')['purchase_value'].sum().reset_index()
        bar_data = [{"name": row['vendor'], "value": float(row['purchase_value'])} for _, row in vendor_vol.iterrows()]
        
        status_counts = self.df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        pie_data = [{"name": row['status'], "value": int(row['count'])} for _, row in status_counts.iterrows()]
        
        return [
            {"title": "Purchases by Vendor", "type": "bar", "data": bar_data},
            {"title": "Order Status Distribution", "type": "pie", "data": pie_data}
        ]
        
    def get_fallback_summary(self):
        kpis = self.generate_kpis()
        return f"Procurement activities generated {kpis['total_orders']} orders totaling ${kpis['total_value']:,}. Currently, {kpis['pending_orders']} orders remain in pending status."
