import sys
import os
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.predictive.base import BaseForecaster
from app.services.predictive.revenue_forecaster import RevenueForecaster
from app.services.predictive.admissions_forecaster import AdmissionsForecaster
from app.services.predictive.bed_occupancy_forecaster import BedOccupancyForecaster
from app.services.predictive.medicine_demand_forecaster import MedicineDemandForecaster
from app.services.predictive.inventory_forecaster import InventoryForecaster

def test_base_forecaster_train_evaluate_predict():
    forecaster = BaseForecaster()
    dates = pd.date_range(end=pd.Timestamp.now(), periods=20, freq='D')
    df = pd.DataFrame({'date': dates, 'value': np.linspace(10, 100, 20)})
    
    X = forecaster.extract_features(df)
    y = df['value']
    
    hist_preds, future_preds, metrics = forecaster.train_evaluate_predict(X, y, future_days=7)
    
    assert len(hist_preds) == 20
    assert len(future_preds) == 7
    assert "mae" in metrics
    assert "rmse" in metrics
    assert "r2" in metrics
    # Test non-negative constraint
    assert all(p >= 0 for p in future_preds)

@pytest.mark.asyncio
async def test_revenue_forecaster_data_source():
    forecaster = RevenueForecaster()
    res = await forecaster.forecast(days=14)
    assert "metric" in res
    assert res["metric"] == "revenue"
    assert "data_source" in res
    assert "data_quality" in res
    assert isinstance(res["forecast"], list)

@pytest.mark.asyncio
async def test_admissions_forecaster_data_source():
    forecaster = AdmissionsForecaster()
    res = await forecaster.forecast(days=14)
    assert "metric" in res
    assert res["metric"] == "admissions"
    assert "data_source" in res

@pytest.mark.asyncio
async def test_medicine_demand_forecaster():
    forecaster = MedicineDemandForecaster()
    res = await forecaster.forecast(days=30)
    assert isinstance(res, list)
    if len(res) > 0:
        assert "name" in res[0]
        assert "data_source" in res[0]

@pytest.mark.asyncio
async def test_inventory_forecaster():
    forecaster = InventoryForecaster()
    res = await forecaster.forecast()
    assert isinstance(res, list)
    if len(res) > 0:
        assert "risk_level" in res[0]
        assert "data_source" in res[0]
