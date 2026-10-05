import pandas as pd
from datetime import timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.services.predictive.base import BaseForecaster
from app.services.predictive.ai_explanation import AIExplanationService
from app.models.admission import Admission

class AdmissionsForecaster(BaseForecaster):
    def __init__(self, db: Optional[Session] = None):
        super().__init__("admissions.csv", db=db)

    def load_data(self) -> Tuple[pd.DataFrame, str, str]:
        if self.db is not None:
            try:
                # Query admissions table in PostgreSQL
                query = (
                    self.db.query(
                        func.date(Admission.admission_date).label('date'),
                        func.count(Admission.id).label('admissions')
                    )
                    .group_by(func.date(Admission.admission_date))
                    .order_by(func.date(Admission.admission_date))
                )
                results = query.all()
                if len(results) >= 3:
                    records = [{'date': pd.to_datetime(r.date), 'admissions': int(r.admissions or 0)} for r in results]
                    df = pd.DataFrame(records).sort_values('date')
                    return df, "POSTGRESQL_DB", "HISTORICAL"
            except Exception as e:
                pass

        return super().load_data()

    async def forecast(self, days: int = 30) -> dict:
        df, data_source, data_quality = self.load_data()
        daily_admissions = df.groupby('date')['admissions'].sum().reset_index()
        if len(daily_admissions) < 2:
            return {}

        X = self.extract_features(daily_admissions)
        y = daily_admissions['admissions']

        hist_preds, future_preds, metrics = self.train_evaluate_predict(X, y, future_days=days)

        last_date = daily_admissions['date'].max()
        future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
        trend_direction = "increasing" if future_preds[-1] > future_preds[0] else "decreasing"

        historical = [{"date": row['date'].strftime("%Y-%m-%d"), "value": float(row['admissions'])} for _, row in daily_admissions.tail(30).iterrows()]
        forecast = [{"date": date.strftime("%Y-%m-%d"), "value": float(max(0, pred))} for date, pred in zip(future_dates, future_preds)]

        avg_future = sum([f["value"] for f in forecast]) / len(forecast) if len(forecast) > 0 else 0
        avg_past = y.tail(days).mean() if len(y) > 0 else 0

        context = f"Historical daily admissions average: {avg_past:.1f}. Projected {days}-day average: {avg_future:.1f}. Trend is {trend_direction}."
        fallback = f"Patient admissions are predicted to remain {trend_direction} over the next {days} days."

        explanation = await AIExplanationService.get_explanation(context, fallback)

        return {
            "metric": "admissions",
            "historical": historical,
            "forecast": forecast,
            "trend": trend_direction,
            "metrics": metrics,
            "explanation": explanation,
            "algorithm": "Scikit-learn LinearRegression",
            "data_source": data_source,
            "data_quality": data_quality
        }

