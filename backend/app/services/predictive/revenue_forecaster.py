import pandas as pd
from datetime import timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.services.predictive.base import BaseForecaster
from app.services.predictive.ai_explanation import AIExplanationService
from app.models.transaction import Transaction

class RevenueForecaster(BaseForecaster):
    def __init__(self, db: Optional[Session] = None):
        super().__init__("revenue.csv", db=db)

    def load_data(self) -> Tuple[pd.DataFrame, str, str]:
        if self.db is not None:
            try:
                # Query transactions table in PostgreSQL
                query = (
                    self.db.query(
                        func.date(Transaction.transaction_date).label('date'),
                        func.sum(Transaction.amount).label('net_revenue')
                    )
                    .filter(Transaction.transaction_type == 'revenue')
                    .group_by(func.date(Transaction.transaction_date))
                    .order_by(func.date(Transaction.transaction_date))
                )
                results = query.all()
                if len(results) >= 3:
                    records = [{'date': pd.to_datetime(r.date), 'net_revenue': float(r.net_revenue or 0.0)} for r in results]
                    df = pd.DataFrame(records).sort_values('date')
                    return df, "POSTGRESQL_DB", "HISTORICAL"
            except Exception as e:
                pass

        # Fallback to CSV or synthetic
        return super().load_data()

    async def forecast(self, days: int = 30) -> dict:
        df, data_source, data_quality = self.load_data()
        daily_revenue = df.groupby('date')['net_revenue'].sum().reset_index()
        if len(daily_revenue) < 2:
            return {}

        X = self.extract_features(daily_revenue)
        y = daily_revenue['net_revenue']

        hist_preds, future_preds, metrics = self.train_evaluate_predict(X, y, future_days=days)

        last_date = daily_revenue['date'].max()
        future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
        trend_direction = "increasing" if future_preds[-1] > future_preds[0] else "decreasing"

        historical = [{"date": row['date'].strftime("%Y-%m-%d"), "value": float(row['net_revenue'])} for _, row in daily_revenue.tail(30).iterrows()]
        forecast = [{"date": date.strftime("%Y-%m-%d"), "value": float(pred)} for date, pred in zip(future_dates, future_preds)]

        avg_future = sum(future_preds) / len(future_preds) if len(future_preds) > 0 else 0
        avg_past = y.tail(days).mean() if len(y) > 0 else 0
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
            "explanation": explanation,
            "algorithm": "Scikit-learn LinearRegression",
            "data_source": data_source,
            "data_quality": data_quality
        }

