import pandas as pd
from datetime import timedelta
from .base import BaseForecaster
from .ai_explanation import AIExplanationService

class RevenueForecaster(BaseForecaster):
    def __init__(self):
        super().__init__("revenue.csv")
        
    async def forecast(self, days: int = 30) -> dict:
        df = self.load_data()
        
        # Aggregate daily net revenue across all departments
        daily_revenue = df.groupby('date')['net_revenue'].sum().reset_index()
        
        if len(daily_revenue) < 2:
            return {}
            
        X = self.extract_features(daily_revenue)
        y = daily_revenue['net_revenue']
        
        self.model.fit(X, y)
        
        # Calculate metrics on training data
        y_pred_train = self.model.predict(X)
        metrics = self.calculate_metrics(y, y_pred_train)
        
        # Forecast future
        last_date = daily_revenue['date'].max()
        future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
        last_day_index = X['day_index'].max()
        future_X = pd.DataFrame({'day_index': [last_day_index + i + 1 for i in range(days)]})
        
        future_preds = self.model.predict(future_X)
        
        trend_direction = "increasing" if future_preds[-1] > future_preds[0] else "decreasing"
        
        historical = [{"date": row['date'].strftime("%Y-%m-%d"), "value": float(row['net_revenue'])} for _, row in daily_revenue.tail(30).iterrows()]
        forecast = [{"date": date.strftime("%Y-%m-%d"), "value": float(pred)} for date, pred in zip(future_dates, future_preds)]
        
        avg_future = sum(future_preds) / len(future_preds)
        avg_past = y.tail(days).mean()
        pct_change = ((avg_future - avg_past) / avg_past * 100) if avg_past else 0
        
        context = f"Historical 30-day average net revenue: {avg_past:.2f}. Projected {days}-day average: {avg_future:.2f}. Trend is {trend_direction} with {abs(pct_change):.1f}% change."
        fallback = f"Revenue is projected to be {trend_direction} by approximately {abs(pct_change):.1f}% based on historical trends."
        
        explanation = await AIExplanationService.get_explanation(context, fallback)
        
        return {
            "metric": "revenue",
            "historical": historical,
            "forecast": forecast,
            "trend": trend_direction,
            "metrics": metrics,
            "explanation": explanation
        }
