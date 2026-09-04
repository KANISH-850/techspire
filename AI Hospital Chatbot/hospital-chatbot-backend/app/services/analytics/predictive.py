import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.models import Transaction, Admission, InventoryItem
from app.services.ai import get_ai_provider

def train_and_predict(dates, values, days_ahead=30):
    if len(dates) < 2:
        return []
    
    # Convert dates to ordinal for regression
    X = np.array([d.toordinal() for d in dates]).reshape(-1, 1)
    y = np.array(values)
    
    model = LinearRegression()
    model.fit(X, y)
    
    last_date = dates[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
    X_future = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
    
    predictions = model.predict(X_future)
    
    # Ensure no negative predictions if it doesn't make sense (like admissions)
    predictions = [max(0, p) for p in predictions]
    
    return [{"date": d.strftime('%Y-%m-%d'), "predicted_value": round(p, 2)} for d, p in zip(future_dates, predictions)]

def predict_revenue(db: Session, days_ahead: int = 30):
    # Fetch historical daily revenue
    daily_rev = db.query(
        func.date(Transaction.transaction_date).label('date'),
        func.sum(Transaction.amount).label('total')
    ).filter(Transaction.transaction_type == 'revenue').group_by(func.date(Transaction.transaction_date)).order_by('date').all()
    
    if not daily_rev:
        return {"historical": [], "forecast": [], "insights": {}}

    dates = [row.date for row in daily_rev]
    values = [float(row.total) for row in daily_rev]
    
    forecast = train_and_predict(dates, values, days_ahead)
    
    historical = [{"date": d.strftime('%Y-%m-%d'), "value": round(v, 2)} for d, v in zip(dates, values)]
    
    # Generate AI insights
    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Revenue",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in forecast]) / len(forecast) if forecast else 0
    })

    return {
        "historical": historical[-90:], # send last 90 days of historical
        "forecast": forecast,
        "ai_analysis": insights
    }

def predict_admissions(db: Session, days_ahead: int = 30):
    # Fetch historical daily admissions
    daily_adm = db.query(
        func.date(Admission.admission_date).label('date'),
        func.count(Admission.id).label('total')
    ).group_by(func.date(Admission.admission_date)).order_by('date').all()
    
    if not daily_adm:
        return {"historical": [], "forecast": [], "ai_analysis": {}}

    dates = [row.date for row in daily_adm]
    values = [int(row.total) for row in daily_adm]
    
    forecast = train_and_predict(dates, values, days_ahead)
    historical = [{"date": d.strftime('%Y-%m-%d'), "value": v} for d, v in zip(dates, values)]

    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Patient Admissions",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in forecast]) / len(forecast) if forecast else 0
    })

    return {
        "historical": historical[-90:],
        "forecast": forecast,
        "ai_analysis": insights
    }

def predict_beds(db: Session, days_ahead: int = 30):
    # Approximate historical bed occupancy using admissions
    daily_adm = db.query(
        func.date(Admission.admission_date).label('date'),
        func.count(Admission.id).label('total')
    ).group_by(func.date(Admission.admission_date)).order_by('date').all()
    
    if not daily_adm:
        return {"historical": [], "forecast": [], "ai_analysis": {}}

    # We assume bed occupancy is proportional to admissions (e.g. active admissions)
    # Since we lack daily snapshot of beds, we'll build a moving window of admissions over 3 days (average stay)
    dates = [row.date for row in daily_adm]
    values = []
    
    for i in range(len(dates)):
        # sum of admissions in last 3 days
        val = sum([int(daily_adm[j].total) for j in range(max(0, i-3), i+1)])
        values.append(val)
        
    forecast = train_and_predict(dates, values, days_ahead)
    historical = [{"date": d.strftime('%Y-%m-%d'), "value": v} for d, v in zip(dates, values)]

    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Bed Occupancy",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in forecast]) / len(forecast) if forecast else 0
    })

    return {
        "historical": historical[-90:],
        "forecast": forecast,
        "ai_analysis": insights
    }

def predict_medicines(db: Session, days_ahead: int = 30):
    # Predict medicine demand based on historical admissions multiplied by baseline consumption
    items = db.query(InventoryItem).filter(InventoryItem.category == 'Medicine').all()
    total_daily_baseline = sum([i.daily_consumption for i in items]) if items else 100
    
    daily_adm = db.query(
        func.date(Admission.admission_date).label('date'),
        func.count(Admission.id).label('total')
    ).group_by(func.date(Admission.admission_date)).order_by('date').all()
    
    if not daily_adm:
        return {"historical": [], "forecast": [], "ai_analysis": {}}

    dates = [row.date for row in daily_adm]
    # Assume medicine demand scales with admissions
    values = [int(row.total) * total_daily_baseline * 0.1 for row in daily_adm]
    
    forecast = train_and_predict(dates, values, days_ahead)
    historical = [{"date": d.strftime('%Y-%m-%d'), "value": round(v, 2)} for d, v in zip(dates, values)]

    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Medicine Demand",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in forecast]) / len(forecast) if forecast else 0
    })

    return {
        "historical": historical[-90:],
        "forecast": forecast,
        "ai_analysis": insights
    }

def predict_inventory(db: Session, days_ahead: int = 30):
    # Aggregate total inventory and simulate historical decrease
    items = db.query(InventoryItem).all()
    current_total = sum([i.current_stock for i in items]) if items else 0
    daily_cons = sum([i.daily_consumption for i in items]) if items else 0
    
    today = datetime.now(timezone.utc).date()
    dates = [today - timedelta(days=i) for i in range(90, -1, -1)]
    
    # Reconstruct historical inventory levels
    values = []
    for i, d in enumerate(dates):
        # as we go forward in time (from 90 days ago), stock decreases, but with some noise
        # assuming stock was replenished sometimes, but we model a linear trend for simplicity
        val = current_total + (daily_cons * (90 - i))
        values.append(val)
        
    forecast = train_and_predict(dates, values, days_ahead)
    historical = [{"date": d.strftime('%Y-%m-%d'), "value": round(v, 2)} for d, v in zip(dates, values)]

    provider = get_ai_provider()
    insights = provider.generate_insights({
        "metric": "Overall Inventory Stock",
        "last_30_days_avg": sum(values[-30:]) / min(len(values), 30),
        "predicted_next_30_days_avg": sum([f["predicted_value"] for f in forecast]) / len(forecast) if forecast else 0
    })

    return {
        "historical": historical[-90:],
        "forecast": forecast,
        "ai_analysis": insights
    }
