import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.models import Transaction, Admission, InventoryItem
from app.services.ai import get_ai_provider
from app.services.analytics.ml_forecaster import MLForecaster

def predict_revenue(db: Session, days_ahead: int = 30):
    # Fetch historical daily revenue from PostgreSQL transactions
    daily_rev = db.query(
        func.date(Transaction.transaction_date).label('date'),
        func.sum(Transaction.amount).label('total')
    ).filter(Transaction.transaction_type == 'revenue').group_by(func.date(Transaction.transaction_date)).order_by('date').all()
    
    if not daily_rev:
        return {
            "historical": [], 
            "forecast": [], 
            "ai_analysis": {},
            "model": "Linear Regression",
            "algorithm": "Scikit-Learn LinearRegression",
            "training_samples": 0,
            "data_source": "PostgreSQL transactions",
            "data_quality": "historical",
            "metrics": "insufficient historical data"
        }

    dates = [row.date for row in daily_rev]
    values = [float(row.total) for row in daily_rev]
    
    result = MLForecaster.train_and_forecast(
        dates=dates,
        values=values,
        days_ahead=days_ahead,
        data_source="PostgreSQL transactions",
        data_quality="historical",
        model_name="Linear Regression"
    )
    
    # Generate AI insights using LLM
    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Revenue",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in result["forecast"]]) / len(result["forecast"]) if result["forecast"] else 0
    })

    result["historical"] = result["historical"][-90:]
    result["ai_analysis"] = insights
    return result

def predict_admissions(db: Session, days_ahead: int = 30):
    # Fetch historical daily admissions from PostgreSQL admissions
    daily_adm = db.query(
        func.date(Admission.admission_date).label('date'),
        func.count(Admission.id).label('total')
    ).group_by(func.date(Admission.admission_date)).order_by('date').all()
    
    if not daily_adm:
        return {
            "historical": [], 
            "forecast": [], 
            "ai_analysis": {},
            "model": "Linear Regression",
            "algorithm": "Scikit-Learn LinearRegression",
            "training_samples": 0,
            "data_source": "PostgreSQL admissions",
            "data_quality": "historical",
            "metrics": "insufficient historical data"
        }

    dates = [row.date for row in daily_adm]
    values = [float(row.total) for row in daily_adm]
    
    result = MLForecaster.train_and_forecast(
        dates=dates,
        values=values,
        days_ahead=days_ahead,
        data_source="PostgreSQL admissions",
        data_quality="historical",
        model_name="Linear Regression"
    )

    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Patient Admissions",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in result["forecast"]]) / len(result["forecast"]) if result["forecast"] else 0
    })

    result["historical"] = result["historical"][-90:]
    result["ai_analysis"] = insights
    return result

def predict_beds(db: Session, days_ahead: int = 30):
    # Derive bed occupancy proxy using admissions over a 3-day rolling window
    daily_adm = db.query(
        func.date(Admission.admission_date).label('date'),
        func.count(Admission.id).label('total')
    ).group_by(func.date(Admission.admission_date)).order_by('date').all()
    
    if not daily_adm:
        return {
            "historical": [], 
            "forecast": [], 
            "ai_analysis": {},
            "model": "Linear Regression",
            "algorithm": "Scikit-Learn LinearRegression",
            "training_samples": 0,
            "data_source": "Admission & Bed records (3-day rolling window occupancy proxy)",
            "data_quality": "approximated",
            "metrics": "insufficient historical data"
        }

    dates = [row.date for row in daily_adm]
    values = []
    for i in range(len(dates)):
        val = sum([float(daily_adm[j].total) for j in range(max(0, i-3), i+1)])
        values.append(val)
        
    result = MLForecaster.train_and_forecast(
        dates=dates,
        values=values,
        days_ahead=days_ahead,
        data_source="Admission & Bed records (3-day rolling window occupancy proxy)",
        data_quality="approximated",
        model_name="Linear Regression"
    )

    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Bed Occupancy",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in result["forecast"]]) / len(result["forecast"]) if result["forecast"] else 0
    })

    result["historical"] = result["historical"][-90:]
    result["ai_analysis"] = insights
    return result

def predict_medicines(db: Session, days_ahead: int = 30):
    # Predict medicine demand based on historical admissions multiplied by baseline consumption
    items = db.query(InventoryItem).filter(InventoryItem.category == 'Medicine').all()
    total_daily_baseline = sum([i.daily_consumption for i in items]) if items else 100
    
    daily_adm = db.query(
        func.date(Admission.admission_date).label('date'),
        func.count(Admission.id).label('total')
    ).group_by(func.date(Admission.admission_date)).order_by('date').all()
    
    if not daily_adm:
        return {
            "historical": [], 
            "forecast": [], 
            "ai_analysis": {},
            "model": "Linear Regression",
            "algorithm": "Scikit-Learn LinearRegression",
            "training_samples": 0,
            "data_source": "Admissions & Medicine baseline consumption",
            "data_quality": "approximated",
            "metrics": "insufficient historical data"
        }

    dates = [row.date for row in daily_adm]
    values = [float(row.total) * total_daily_baseline * 0.1 for row in daily_adm]
    
    result = MLForecaster.train_and_forecast(
        dates=dates,
        values=values,
        days_ahead=days_ahead,
        data_source="Admissions & Medicine baseline consumption",
        data_quality="approximated",
        model_name="Linear Regression"
    )

    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Medicine Demand",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in result["forecast"]]) / len(result["forecast"]) if result["forecast"] else 0
    })

    result["historical"] = result["historical"][-90:]
    result["ai_analysis"] = insights
    return result

def predict_inventory(db: Session, days_ahead: int = 30):
    # Reconstruct historical inventory levels from current stock and daily consumption rates
    items = db.query(InventoryItem).all()
    current_total = sum([i.current_stock for i in items]) if items else 0
    daily_cons = sum([i.daily_consumption for i in items]) if items else 0
    
    today = datetime.now(timezone.utc).date()
    dates = [today - timedelta(days=i) for i in range(90, -1, -1)]
    
    values = []
    for i, d in enumerate(dates):
        val = current_total + (daily_cons * (90 - i))
        values.append(float(val))
        
    result = MLForecaster.train_and_forecast(
        dates=dates,
        values=values,
        days_ahead=days_ahead,
        data_source="Current inventory stock & daily consumption rates",
        data_quality="reconstructed",
        model_name="Linear Regression"
    )

    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Overall Inventory Stock",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in result["forecast"]]) / len(result["forecast"]) if result["forecast"] else 0
    })

    result["historical"] = result["historical"][-90:]
    result["ai_analysis"] = insights
    return result
