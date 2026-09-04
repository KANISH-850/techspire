from .base import BaseReportAnalytics

class FinancialAnalytics(BaseReportAnalytics):
    def generate_kpis(self):
        if self.df.empty:
            return {"total_revenue": 0, "total_expenses": 0, "net_revenue": 0}
        return {
            "total_revenue": round(self.df['revenue'].sum(), 2),
            "total_expenses": round(self.df['expense'].sum(), 2),
            "net_revenue": round(self.df['net_revenue'].sum(), 2),
            "highest_revenue_dept": self.df.groupby('department')['revenue'].sum().idxmax() if not self.df.empty else "N/A"
        }
        
    def generate_charts(self):
        if self.df.empty:
            return []
            
        # Revenue by department pie chart
        dept_rev = self.df.groupby('department')['revenue'].sum().reset_index()
        pie_data = [{"name": row['department'], "value": float(row['revenue'])} for _, row in dept_rev.iterrows()]
        
        # Monthly trend line chart
        self.df['month'] = self.df['date'].dt.to_period('M').astype(str)
        trend = self.df.groupby('month')[['revenue', 'expense']].sum().reset_index()
        line_data = [{"month": row['month'], "revenue": float(row['revenue']), "expense": float(row['expense'])} for _, row in trend.iterrows()]
        
        return [
            {"title": "Revenue by Department", "type": "pie", "data": pie_data},
            {"title": "Revenue vs Expense Trend", "type": "line", "data": line_data}
        ]
        
    def get_fallback_summary(self):
        kpis = self.generate_kpis()
        return f"During this period, total revenue was ${kpis['total_revenue']:,} against expenses of ${kpis['total_expenses']:,}, resulting in a net revenue of ${kpis['net_revenue']:,}. The highest performing department was {kpis['highest_revenue_dept']}."
