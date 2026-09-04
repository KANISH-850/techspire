from .base import BaseReportAnalytics

class ClinicalAnalytics(BaseReportAnalytics):
    def generate_kpis(self):
        if self.df.empty:
            return {"total_admissions": 0, "total_discharges": 0, "emergency_cases": 0}
        return {
            "total_admissions": int(self.df['admissions'].sum()),
            "total_discharges": int(self.df['discharges'].sum()),
            "emergency_cases": int(self.df['emergency_cases'].sum()),
            "avg_daily_admissions": round(self.df['admissions'].mean(), 1) if not self.df.empty else 0
        }
        
    def generate_charts(self):
        if self.df.empty:
            return []
            
        dept_adm = self.df.groupby('department')['admissions'].sum().reset_index()
        bar_data = [{"name": row['department'], "admissions": int(row['admissions'])} for _, row in dept_adm.iterrows()]
        
        self.df['month'] = self.df['date'].dt.to_period('M').astype(str)
        trend = self.df.groupby('month')['admissions'].sum().reset_index()
        line_data = [{"month": row['month'], "admissions": int(row['admissions'])} for _, row in trend.iterrows()]
        
        return [
            {"title": "Admissions by Department", "type": "bar", "data": bar_data},
            {"title": "Admission Trend", "type": "line", "data": line_data}
        ]
        
    def get_fallback_summary(self):
        kpis = self.generate_kpis()
        return f"The hospital recorded {kpis['total_admissions']} admissions and {kpis['total_discharges']} discharges. Emergency cases accounted for {kpis['emergency_cases']} of the total patient flow. Average daily admissions stood at {kpis['avg_daily_admissions']}."
