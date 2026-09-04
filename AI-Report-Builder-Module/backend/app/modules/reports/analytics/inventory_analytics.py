from .base import BaseReportAnalytics
import numpy as np

class InventoryAnalytics(BaseReportAnalytics):
    def generate_kpis(self):
        if self.df.empty:
            return {"total_stock_value": 0, "high_risk_items": 0, "expired_items": 0}
            
        # Get latest snapshot per item for KPIs
        latest = self.df.sort_values('date').groupby('item_name').last().reset_index()
        
        return {
            "total_stock_value": round(latest['stock_value'].sum(), 2),
            "high_risk_items": len(latest[latest['current_stock'] < 100]), # Mock risk threshold
            "expired_items": int(latest['expired'].sum())
        }
        
    def generate_charts(self):
        if self.df.empty:
            return []
            
        latest = self.df.sort_values('date').groupby('item_name').last().reset_index()
        bar_data = [{"name": row['item_name'], "stock": int(row['current_stock'])} for _, row in latest.iterrows()]
        
        return [
            {"title": "Current Stock Levels", "type": "bar", "data": bar_data}
        ]
        
    def get_fallback_summary(self):
        kpis = self.generate_kpis()
        return f"The current total inventory value is ${kpis['total_stock_value']:,}. There are {kpis['high_risk_items']} high-risk items requiring immediate reorder, and {kpis['expired_items']} expired units that need disposal."
