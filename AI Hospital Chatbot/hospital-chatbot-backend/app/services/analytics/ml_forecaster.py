import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Union
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

class MLForecaster:
    """
    Standard Machine Learning Forecasting Engine using Scikit-Learn LinearRegression.
    Provides time-aware validation splits, evaluation diagnostics (R², MAE, RMSE),
    and structured forecast outputs with explicit data quality metadata.
    """

    @staticmethod
    def train_and_forecast(
        dates: List[Any],
        values: List[float],
        days_ahead: int = 30,
        data_source: str = "PostgreSQL",
        data_quality: str = "historical",
        model_name: str = "Linear Regression"
    ) -> Dict[str, Any]:
        """
        Train a LinearRegression model on time-series ordinal dates and return 
        historical values, future predictions, metrics, and metadata.
        """
        if len(dates) < 2:
            return {
                "historical": [],
                "forecast": [],
                "model": model_name,
                "algorithm": "Scikit-Learn LinearRegression",
                "training_samples": len(dates),
                "data_source": data_source,
                "data_quality": data_quality,
                "metrics": "insufficient historical data"
            }

        # Convert dates to ordinal for regression
        X = np.array([d.toordinal() for d in dates]).reshape(-1, 1)
        y = np.array(values, dtype=float)

        # Time-aware train/test evaluation (first 80% train, last 20% test)
        metrics: Union[Dict[str, float], str] = "insufficient historical data"
        if len(X) >= 10:
            split_idx = int(len(X) * 0.8)
            if split_idx <= len(X) - 2:
                X_train, X_test = X[:split_idx], X[split_idx:]
                y_train, y_test = y[:split_idx], y[split_idx:]

                val_model = LinearRegression()
                val_model.fit(X_train, y_train)
                y_pred_test = val_model.predict(X_test)

                try:
                    r2_val = float(r2_score(y_test, y_pred_test))
                except Exception:
                    r2_val = 0.0

                mae_val = float(mean_absolute_error(y_test, y_pred_test))
                rmse_val = float(np.sqrt(mean_squared_error(y_test, y_pred_test)))

                metrics = {
                    "r2": round(max(-1.0, min(1.0, r2_val)), 4),
                    "mae": round(mae_val, 2),
                    "rmse": round(rmse_val, 2)
                }

        # Fit final model on all available historical data
        final_model = LinearRegression()
        final_model.fit(X, y)

        # Generate future predictions
        last_date = dates[-1]
        future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
        X_future = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)

        raw_predictions = final_model.predict(X_future)
        predictions = [round(max(0.0, float(p)), 2) for p in raw_predictions]

        forecast_list = [
            {"date": d.strftime("%Y-%m-%d"), "predicted_value": p}
            for d, p in zip(future_dates, predictions)
        ]

        historical_list = [
            {"date": d.strftime("%Y-%m-%d"), "value": round(float(v), 2)}
            for d, v in zip(dates, values)
        ]

        return {
            "historical": historical_list,
            "forecast": forecast_list,
            "model": model_name,
            "algorithm": "Scikit-Learn LinearRegression",
            "training_samples": len(dates),
            "data_source": data_source,
            "data_quality": data_quality,
            "metrics": metrics
        }
