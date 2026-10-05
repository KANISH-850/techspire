import os
import pandas as pd
import numpy as np
from datetime import timedelta
from typing import Optional, Tuple, Dict
from sqlalchemy.orm import Session
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class BaseForecaster:
    def __init__(self, data_file: str = "revenue.csv", db: Optional[Session] = None):
        self.db = db
        self.data_file = data_file
        
        # Fallback CSV data paths
        root_data = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "predictive", data_file)
        fallback_data = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "Predictive-Analytics-Module", "data", "predictive", data_file)
        
        if os.path.exists(root_data):
            self.data_path = root_data
        elif os.path.exists(fallback_data):
            self.data_path = fallback_data
        else:
            self.data_path = root_data

        self.model = LinearRegression()

    def load_data(self) -> Tuple[pd.DataFrame, str, str]:
        """
        Loads data. Child classes override to load from PostgreSQL DB.
        Returns (df, data_source, data_quality)
        """
        if os.path.exists(self.data_path):
            df = pd.read_csv(self.data_path)
            df['date'] = pd.to_datetime(df['date'])
            return df.sort_values('date'), "HISTORICAL_CSV", "HISTORICAL"
        
        # Synthetic fallback if CSV missing and DB unavailable
        dates = pd.date_range(end=pd.Timestamp.now(), periods=60, freq='D')
        df = pd.DataFrame({
            'date': dates,
            'net_revenue': np.random.normal(15000, 2000, 60),
            'admissions': np.random.poisson(15, 60),
            'occupied_beds': np.random.randint(40, 80, 60),
            'medicine': 'Aspirin 100mg',
            'daily_demand': np.random.randint(20, 50, 60),
            'item_name': 'Aspirin 100mg',
            'category': 'Medication',
            'current_stock': 150,
            'minimum_stock': 50,
            'daily_consumption': 25.0
        })
        return df, "SYNTHETIC_FALLBACK", "SYNTHETIC"

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df['day_index'] = (df['date'] - df['date'].min()).dt.days
        return df[['day_index']]

    def train_evaluate_predict(self, X: pd.DataFrame, y: pd.Series, future_days: int) -> Tuple[np.ndarray, np.ndarray, Dict[str, float]]:
        """
        Performs chronological 80/20 train/test split for evaluation,
        evaluates metrics on test set, then retrains on full dataset for future predictions.
        """
        n_samples = len(X)
        if n_samples < 4:
            # Fit on available data without split
            self.model.fit(X, y)
            y_pred_train = np.maximum(0, self.model.predict(X))
            metrics = self.calculate_metrics(y, y_pred_train)
        else:
            # Chronological 80/20 split for evaluation on holdout test set
            split_idx = int(n_samples * 0.8)
            X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
            y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

            self.model.fit(X_train, y_train)
            y_pred_test = np.maximum(0, self.model.predict(X_test))
            metrics = self.calculate_metrics(y_test, y_pred_test)

            # Retrain on full historical dataset for production future prediction
            self.model.fit(X, y)

        last_day_index = X['day_index'].max()
        future_X = pd.DataFrame({'day_index': [last_day_index + i + 1 for i in range(future_days)]})
        future_preds = np.maximum(0, self.model.predict(future_X))
        
        hist_preds = np.maximum(0, self.model.predict(X))
        return hist_preds, future_preds, metrics

    def calculate_metrics(self, y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
        if len(y_true) < 2:
            return {"mae": 0.0, "rmse": 0.0, "r2": 0.0}
        
        mae = float(mean_absolute_error(y_true, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
        r2 = float(r2_score(y_true, y_pred))
        return {
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "r2": round(r2, 3)
        }

