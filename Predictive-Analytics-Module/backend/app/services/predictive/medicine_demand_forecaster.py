import pandas as pd
from datetime import timedelta
from .base import BaseForecaster
from .ai_explanation import AIExplanationService

class MedicineDemandForecaster(BaseForecaster):
    def __init__(self):
        super().__init__("medicine_demand.csv")
        
    async def forecast(self, days: int = 30) -> list:
        df = self.load_data()
        results = []
        
        for medicine in df['medicine_name'].unique():
            med_df = df[df['medicine_name'] == medicine]
            daily = med_df.groupby('date')['quantity_used'].sum().reset_index()
            
            if len(daily) < 2:
                continue
                
            X = self.extract_features(daily)
            y = daily['quantity_used']
            
            self.model.fit(X, y)
            metrics = self.calculate_metrics(y, self.model.predict(X))
            
            last_date = daily['date'].max()
            future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
            last_day_index = X['day_index'].max()
            future_X = pd.DataFrame({'day_index': [last_day_index + i + 1 for i in range(days)]})
            
            future_preds = self.model.predict(future_X)
            future_preds = [max(0.0, p) for p in future_preds]
            
            trend_direction = "increasing" if future_preds[-1] > future_preds[0] else "decreasing"
            
            historical = [{"date": row['date'].strftime("%Y-%m-%d"), "value": float(row['quantity_used'])} for _, row in daily.tail(30).iterrows()]
            forecast = [{"date": date.strftime("%Y-%m-%d"), "value": float(pred)} for date, pred in zip(future_dates, future_preds)]
            
            expected_demand = sum(future_preds)
            
            context = f"Demand for {medicine} over next {days} days is expected to be {expected_demand:.0f} units. Trend is {trend_direction}."
            fallback = f"Demand for {medicine} is {trend_direction}, with an estimated {expected_demand:.0f} units needed over the next {days} days."
            
            explanation = await AIExplanationService.get_explanation(context, fallback)
            
            results.append({
                "medicine": medicine,
                "historical": historical,
                "forecast": forecast,
                "expected_demand": float(expected_demand),
                "trend": trend_direction,
                "metrics": metrics,
                "explanation": explanation
            })
            
        return results
