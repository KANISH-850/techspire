from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models import Alert, Department, Bed, Patient, Transaction
from app.schemas import AlertList, AlertBase

def generate_alerts(db: Session) -> AlertList:
    generated_alerts = []
    
    # 1. Fetch active alerts from DB (seeded)
    db_alerts = db.query(Alert).filter(Alert.status == 'active').order_by(Alert.created_at.desc()).limit(10).all()
    for a in db_alerts:
        dept_name = a.department.name if a.department else "Hospital"
        generated_alerts.append(AlertBase(
            severity=a.severity,
            title=a.title,
            description=a.description,
            department=dept_name,
            metric=a.metric,
            value=a.value,
            threshold=a.threshold,
            created_at=a.created_at,
            status=a.status,
            recommended_action=f"Review {a.metric} in {dept_name}."
        ))

    # 2. Generate rule-based alerts from current metrics
    departments = db.query(Department).all()
    
    for dept in departments:
        # Occupancy Alert
        total_beds = db.query(func.count(Bed.id)).filter(Bed.department_id == dept.id).scalar() or 1
        occupied_beds = db.query(func.count(Bed.id)).filter(Bed.department_id == dept.id, Bed.status == 'Occupied').scalar() or 0
        occupancy = (occupied_beds / total_beds) * 100 if total_beds > 0 else 0.0
        
        if occupancy > 90:
            generated_alerts.append(AlertBase(
                severity="CRITICAL" if occupancy > 95 else "HIGH",
                title=f"High Occupancy in {dept.name}",
                description=f"Bed occupancy is at {occupancy:.1f}%, which exceeds safe limits.",
                department=dept.name,
                metric="occupancy",
                value=f"{occupancy:.1f}%",
                threshold="90%",
                created_at=datetime.utcnow(),
                status="active",
                recommended_action="Prepare overflow beds or divert non-critical admissions."
            ))
            
        # Satisfaction Alert
        satisfaction = db.query(func.avg(Patient.satisfaction_score)).filter(Patient.department_id == dept.id).scalar() or 0.0
        if satisfaction > 0 and satisfaction < 6.5:
            generated_alerts.append(AlertBase(
                severity="HIGH",
                title=f"Low Patient Satisfaction in {dept.name}",
                description=f"Average satisfaction score has dropped to {satisfaction:.1f}.",
                department=dept.name,
                metric="satisfaction",
                value=f"{satisfaction:.1f}",
                threshold="6.5",
                created_at=datetime.utcnow(),
                status="active",
                recommended_action="Review patient feedback and adjust staffing/care protocols."
            ))

    # Avoid exact duplicates from DB and generated
    seen = set()
    unique_alerts = []
    for a in generated_alerts:
        key = (a.title, a.department)
        if key not in seen:
            seen.add(key)
            unique_alerts.append(a)

    # Sort by severity
    severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    unique_alerts.sort(key=lambda x: (severity_rank.get(x.severity, 4), x.created_at), reverse=False)

    return AlertList(alerts=unique_alerts)
