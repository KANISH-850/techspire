import pandas as pd
from datetime import timedelta
from .base import BaseForecaster
from .ai_explanation import AIExplanationService

class AdmissionsForecaster(BaseForecaster):
    def __init__(self):
        super().__init__("admissions.csv")
        
    async def forecast(self, days: int = 30) -> dict:
        df = self.load_data()
        
        daily_adm = df.groupby('date')[['admissions', 'emergency_admissions', 'inpatient', 'outpatient']].sum().reset_index()
        
        if len(daily_adm) < 2:
            return {}
            
        X = self.extract_features(daily_adm)
        y = daily_adm['admissions']
        
        self.model.fit(X, y)
        metrics = self.calculate_metrics(y, self.model.predict(X))
        
        last_date = daily_adm['date'].max()
        future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
        last_day_index = X['day_index'].max()
        future_X = pd.DataFrame({'day_index': [last_day_index + i + 1 for i in range(days)]})
        
        future_preds = self.model.predict(future_X)
        
        trend_direction = "increasing" if future_preds[-1] > future_preds[0] else "decreasing"
        
        historical = [{"date": row['date'].strftime("%Y-%m-%d"), "value": float(row['admissions'])} for _, row in daily_adm.tail(30).iterrows()]
        forecast = [{"date": date.strftime("%Y-%m-%d"), "value": float(pred)} for date, pred in zip(future_dates, future_preds)]
        
        avg_future = sum(future_preds) / len(future_preds)
        
        context = f"Projected {days}-day average admissions: {avg_future:.0f} per day. Trend is {trend_direction}."
        fallback = f"Patient admissions are {trend_direction}, with an expected average of {avg_future:.0f} patients per day over the next {days} days."
        
        explanation = await AIExplanationService.get_explanation(context, fallback)
        
        return {
            "metric": "admissions",
            "historical": historical,
            "forecast": forecast,
            "trend": trend_direction,
            "metrics": metrics,
            "explanation": explanation
        }
