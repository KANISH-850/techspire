import pandas as pd
from datetime import timedelta
from .base import BaseForecaster
from .ai_explanation import AIExplanationService

class BedOccupancyForecaster(BaseForecaster):
    def __init__(self):
        super().__init__("bed_occupancy.csv")
        
    async def forecast(self, days: int = 7) -> dict:
        df = self.load_data()
        
        # Taking max occupancy per day if there are multiple entries, or just using as is since it's one per day
        daily = df.groupby('date').agg({'total_beds': 'max', 'occupied_beds': 'max', 'occupancy_rate': 'max'}).reset_index()
        
        if len(daily) < 2:
            return {}
            
        X = self.extract_features(daily)
        y = daily['occupancy_rate']
        
        self.model.fit(X, y)
        metrics = self.calculate_metrics(y, self.model.predict(X))
        
        last_date = daily['date'].max()
        future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
        last_day_index = X['day_index'].max()
        future_X = pd.DataFrame({'day_index': [last_day_index + i + 1 for i in range(days)]})
        
        future_preds = self.model.predict(future_X)
        # Cap at 1.0 (100%) and floor at 0
        future_preds = [min(1.0, max(0.0, p)) for p in future_preds]
        
        trend_direction = "increasing" if future_preds[-1] > future_preds[0] else "decreasing"
        
        historical = [{"date": row['date'].strftime("%Y-%m-%d"), "value": float(row['occupancy_rate'])} for _, row in daily.tail(30).iterrows()]
        forecast = [{"date": date.strftime("%Y-%m-%d"), "value": float(pred)} for date, pred in zip(future_dates, future_preds)]
        
        peak_occupancy = max(future_preds)
        
        context = f"Projected peak occupancy in next {days} days is {peak_occupancy*100:.1f}%. Trend is {trend_direction}."
        if peak_occupancy > 0.90:
            fallback = f"Warning: Projected occupancy may exceed 90% during the next {days} days. Trend is {trend_direction}."
        else:
            fallback = f"Bed occupancy is stable, expected to peak around {peak_occupancy*100:.1f}% in the next {days} days."
            
        explanation = await AIExplanationService.get_explanation(context, fallback)
        
        return {
            "metric": "bed-occupancy",
            "historical": historical,
            "forecast": forecast,
            "trend": trend_direction,
            "metrics": metrics,
            "explanation": explanation
        }
