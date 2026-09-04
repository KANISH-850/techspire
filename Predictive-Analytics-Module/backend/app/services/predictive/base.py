import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from datetime import timedelta

class BaseForecaster:
    def __init__(self, data_file: str):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "predictive", data_file)
        self.model = LinearRegression()
        
    def load_data(self) -> pd.DataFrame:
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        df = pd.read_csv(self.data_path)
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values('date')
        
    def extract_features(self, df: pd.DataFrame):
        # Convert date to ordinal for simple linear regression over time
        df['day_index'] = (df['date'] - df['date'].min()).dt.days
        return df[['day_index']]
        
    def calculate_metrics(self, y_true, y_pred):
        if len(y_true) < 2:
            return {"mae": 0.0, "rmse": 0.0, "r2": 0.0}
        return {
            "mae": float(mean_absolute_error(y_true, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
            "r2": float(r2_score(y_true, y_pred))
        }
