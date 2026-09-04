from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.models import Department, Patient, Transaction, Bed
from app.schemas import DepartmentPerformance, DepartmentList

def get_department_performance(db: Session, start_date: str = None, end_date: str = None) -> DepartmentList:
    try:
        sd = datetime.fromisoformat(start_date) if start_date else None
        ed = datetime.fromisoformat(end_date) if end_date else datetime.now(timezone.utc)
    except ValueError:
        sd = None
        ed = datetime.now(timezone.utc)

    if sd is None:
        sd = ed - timedelta(days=30)

    departments = db.query(Department).all()
    results = []

    for dept in departments:
        # Patient Count
        pat_query = db.query(func.count(Patient.id)).filter(Patient.department_id == dept.id)
        if sd and ed:
            pat_query = pat_query.filter(Patient.admission_date.between(sd, ed))
        patient_count = pat_query.scalar() or 0

        # Revenue
        rev_query = db.query(func.sum(Transaction.amount)).filter(
            Transaction.department_id == dept.id, 
            Transaction.transaction_type == 'revenue'
        )
        if sd and ed:
            rev_query = rev_query.filter(Transaction.transaction_date.between(sd, ed))
        revenue = rev_query.scalar() or 0.0

        # Occupancy
        total_beds = db.query(func.count(Bed.id)).filter(Bed.department_id == dept.id).scalar() or 1
        occupied_beds = db.query(func.count(Bed.id)).filter(Bed.department_id == dept.id, Bed.status == 'Occupied').scalar() or 0
        occupancy = (occupied_beds / total_beds) * 100 if total_beds > 0 else 0.0

        # Satisfaction
        sat_query = db.query(func.avg(Patient.satisfaction_score)).filter(Patient.department_id == dept.id)
        if sd and ed:
            sat_query = sat_query.filter(Patient.admission_date.between(sd, ed))
        satisfaction = sat_query.scalar() or 0.0

        # Calculate true period-over-period revenue growth using database records
        prev_sd = sd - (ed - sd)
        prev_rev = db.query(func.sum(Transaction.amount)).filter(
            Transaction.department_id == dept.id,
            Transaction.transaction_type == 'revenue',
            Transaction.transaction_date.between(prev_sd, sd)
        ).scalar() or 0.0

        growth = 0.0
        if prev_rev > 0:
            growth = ((revenue - prev_rev) / prev_rev) * 100
        elif revenue > 0:
            growth = 100.0

        # Performance Score (Weighted metric)
        score = (satisfaction * 4) + (occupancy * 0.3) + (min(growth, 100) * 0.3)
        performance_score = round(min(score, 100.0), 1)

        # Alert Status
        alert_status = 'LOW'
        if occupancy > 95 or satisfaction < 6.0 or growth < -20:
            alert_status = 'CRITICAL'
        elif occupancy > 85 or satisfaction < 7.0 or growth < -10:
            alert_status = 'HIGH'
        elif occupancy > 75 or growth < 0:
            alert_status = 'MEDIUM'

        results.append(DepartmentPerformance(
            id=dept.id,
            name=dept.name,
            patient_count=patient_count,
            revenue=round(revenue, 2),
            occupancy=round(occupancy, 1),
            satisfaction=round(satisfaction, 1),
            performance_score=performance_score,
            growth=round(growth, 1),
            alert_status=alert_status
        ))

    # Sort by performance desc
    results.sort(key=lambda x: x.performance_score, reverse=True)
    return DepartmentList(departments=results)
