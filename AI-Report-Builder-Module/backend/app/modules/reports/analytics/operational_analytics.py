from .base import BaseReportAnalytics

class OperationalAnalytics(BaseReportAnalytics):
    def generate_kpis(self):
        if self.df.empty:
            return {"avg_bed_utilization": 0, "total_critical_alerts": 0, "avg_staff_on_duty": 0}
        return {
            "avg_bed_utilization": round((self.df['occupied_beds'].sum() / self.df['total_beds'].sum()) * 100, 1) if self.df['total_beds'].sum() > 0 else 0,
            "total_critical_alerts": int(self.df['critical_alerts'].sum()),
            "avg_staff_on_duty": int(self.df['staff_on_duty'].mean())
        }
        
    def generate_charts(self):
        if self.df.empty:
            return []
            
        self.df['month'] = self.df['date'].dt.to_period('M').astype(str)
        trend = self.df.groupby('month').agg({'occupied_beds': 'sum', 'total_beds': 'sum'}).reset_index()
        trend['utilization'] = (trend['occupied_beds'] / trend['total_beds']) * 100
        
        line_data = [{"month": row['month'], "utilization": round(float(row['utilization']), 1)} for _, row in trend.iterrows()]
        
        return [
            {"title": "Bed Utilization Trend (%)", "type": "line", "data": line_data}
        ]
        
    def get_fallback_summary(self):
        kpis = self.generate_kpis()
        return f"Operational metrics indicate an average bed utilization of {kpis['avg_bed_utilization']}%. There were {kpis['total_critical_alerts']} critical alerts logged across departments, with an average staff presence of {kpis['avg_staff_on_duty']} personnel on duty."
