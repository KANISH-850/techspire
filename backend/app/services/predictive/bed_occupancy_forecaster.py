import pandas as pd
from datetime import timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.services.predictive.base import BaseForecaster
from app.services.predictive.ai_explanation import AIExplanationService
from app.models.bed import Bed
from app.models.admission import Admission

class BedOccupancyForecaster(BaseForecaster):
    def __init__(self, db: Optional[Session] = None):
        super().__init__("bed_occupancy.csv", db=db)

    def load_data(self) -> Tuple[pd.DataFrame, str, str]:
        if self.db is not None:
            try:
                # Query admissions grouped by date for occupied bed historical trend
                query = (
                    self.db.query(
                        func.date(Admission.admission_date).label('date'),
                        func.count(Admission.id).label('occupied_beds')
                    )
                    .filter(Admission.status == 'Admitted')
                    .group_by(func.date(Admission.admission_date))
                    .order_by(func.date(Admission.admission_date))
                )
                results = query.all()
                if len(results) >= 3:
                    records = [{'date': pd.to_datetime(r.date), 'occupied_beds': int(r.occupied_beds or 0)} for r in results]
                    df = pd.DataFrame(records).sort_values('date')
                    return df, "POSTGRESQL_DB", "RECONSTRUCTED"
            except Exception as e:
                pass

        return super().load_data()

    async def forecast(self, days: int = 7) -> dict:
        df, data_source, data_quality = self.load_data()
        daily_beds = df.groupby('date')['occupied_beds'].sum().reset_index()
        if len(daily_beds) < 2:
            return {}

        X = self.extract_features(daily_beds)
        y = daily_beds['occupied_beds']

        hist_preds, future_preds, metrics = self.train_evaluate_predict(X, y, future_days=days)

        last_date = daily_beds['date'].max()
        future_dates = [last_date + timedelta(days=i+1) for i in range(days)]
        trend_direction = "increasing" if future_preds[-1] > future_preds[0] else "decreasing"

        historical = [{"date": row['date'].strftime("%Y-%m-%d"), "value": float(row['occupied_beds'])} for _, row in daily_beds.tail(30).iterrows()]
        forecast = [{"date": date.strftime("%Y-%m-%d"), "value": float(max(0, pred))} for date, pred in zip(future_dates, future_preds)]

        avg_future = sum([f["value"] for f in forecast]) / len(forecast) if len(forecast) > 0 else 0
        avg_past = y.tail(days).mean() if len(y) > 0 else 0
        peak_bed = max([f['value'] for f in forecast]) if len(forecast) > 0 else 0.0

        context = f"Historical occupied beds: {avg_past:.1f}. Projected {days}-day average: {avg_future:.1f}. Peak expected: {peak_bed:.0f} beds."
        fallback = f"Bed occupancy is expected to trend {trend_direction} over the next {days} days."

        explanation = await AIExplanationService.get_explanation(context, fallback)

        return {
            "metric": "bed_occupancy",
            "historical": historical,
            "forecast": forecast,
            "trend": trend_direction,
            "metrics": metrics,
            "explanation": explanation,
            "algorithm": "Scikit-learn LinearRegression",
            "data_source": data_source,
            "data_quality": data_quality
        }

