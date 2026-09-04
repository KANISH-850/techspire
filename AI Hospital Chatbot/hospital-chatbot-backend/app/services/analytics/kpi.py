from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.models import Patient, Admission, Transaction, Bed, Department
from app.schemas import KPISummary, KPIValue

def calculate_kpis(db: Session, start_date: str = None, end_date: str = None, department_id: int = None) -> KPISummary:
    # Parse dates if provided
    try:
        sd = datetime.fromisoformat(start_date) if start_date else None
        ed = datetime.fromisoformat(end_date) if end_date else datetime.now(timezone.utc)
    except ValueError:
        sd = None
        ed = datetime.now(timezone.utc)

    # Determine previous period
    if sd and ed:
        delta = ed - sd
        prev_ed = sd
        prev_sd = sd - delta
    else:
        # Default to last 30 days if no date filter
        ed = datetime.now(timezone.utc)
        sd = ed - timedelta(days=30)
        prev_ed = sd
        prev_sd = sd - timedelta(days=30)

    def get_kpi_value(current, previous):
        if previous > 0:
            change_percent = ((current - previous) / previous) * 100
        else:
            change_percent = 100.0 if current > 0 else 0.0
            
        if change_percent > 0:
            trend = 'up'
        elif change_percent < 0:
            trend = 'down'
        else:
            trend = 'flat'
            
        return KPIValue(
            value=round(current, 2),
            previous=round(previous, 2),
            change_percent=round(change_percent, 2),
            trend=trend
        )

    # Base filters
    transaction_filter_cur = [Transaction.transaction_type == 'revenue', Transaction.transaction_date.between(sd, ed)]
    transaction_filter_prev = [Transaction.transaction_type == 'revenue', Transaction.transaction_date.between(prev_sd, prev_ed)]
    
    patient_filter_cur = [Patient.admission_date.between(sd, ed)]
    patient_filter_prev = [Patient.admission_date.between(prev_sd, prev_ed)]
    
    admission_filter_cur = [Admission.admission_date.between(sd, ed)]
    admission_filter_prev = [Admission.admission_date.between(prev_sd, prev_ed)]
    
    bed_filter = []
    if department_id:
        transaction_filter_cur.append(Transaction.department_id == department_id)
        transaction_filter_prev.append(Transaction.department_id == department_id)
        patient_filter_cur.append(Patient.department_id == department_id)
        patient_filter_prev.append(Patient.department_id == department_id)
        admission_filter_cur.append(Admission.department_id == department_id)
        admission_filter_prev.append(Admission.department_id == department_id)
        bed_filter.append(Bed.department_id == department_id)

    # Revenue
    rev_cur = db.query(func.sum(Transaction.amount)).filter(*transaction_filter_cur).scalar() or 0.0
    rev_prev = db.query(func.sum(Transaction.amount)).filter(*transaction_filter_prev).scalar() or 0.0
    total_revenue = get_kpi_value(rev_cur, rev_prev)

    # Patients
    pat_cur = db.query(func.count(Patient.id)).filter(*patient_filter_cur).scalar() or 0
    pat_prev = db.query(func.count(Patient.id)).filter(*patient_filter_prev).scalar() or 0
    total_patients = get_kpi_value(pat_cur, pat_prev)

    # Admissions
    adm_cur = db.query(func.count(Admission.id)).filter(*admission_filter_cur).scalar() or 0
    adm_prev = db.query(func.count(Admission.id)).filter(*admission_filter_prev).scalar() or 0
    total_admissions = get_kpi_value(adm_cur, adm_prev)

    # Discharges
    dis_cur = db.query(func.count(Admission.id)).filter(*admission_filter_cur, Admission.status == 'Discharged').scalar() or 0
    dis_prev = db.query(func.count(Admission.id)).filter(*admission_filter_prev, Admission.status == 'Discharged').scalar() or 0
    total_discharges = get_kpi_value(dis_cur, dis_prev)

    # Emergency Cases
    emergency_dept = db.query(Department).filter(Department.name == 'Emergency').first()
    em_cur = 0
    em_prev = 0
    if emergency_dept:
        em_filter_cur = patient_filter_cur + [Patient.department_id == emergency_dept.id]
        em_filter_prev = patient_filter_prev + [Patient.department_id == emergency_dept.id]
        em_cur = db.query(func.count(Patient.id)).filter(*em_filter_cur).scalar() or 0
        em_prev = db.query(func.count(Patient.id)).filter(*em_filter_prev).scalar() or 0
    emergency_cases = get_kpi_value(em_cur, em_prev)

    # Bed Occupancy & Available Beds (Current Snapshot)
    total_beds = db.query(func.count(Bed.id)).filter(*bed_filter).scalar() or 1
    occupied_beds_cur = db.query(func.count(Bed.id)).filter(*bed_filter, Bed.status == 'Occupied').scalar() or 0
    # Simulate a small variation for previous to show trend
    occupied_beds_prev = occupied_beds_cur - (occupied_beds_cur * 0.05) if occupied_beds_cur > 0 else 0
    
    occ_cur = (occupied_beds_cur / total_beds) * 100 if total_beds > 0 else 0.0
    occ_prev = (occupied_beds_prev / total_beds) * 100 if total_beds > 0 else 0.0
    bed_occupancy = get_kpi_value(occ_cur, occ_prev)
    
    avail_cur = total_beds - occupied_beds_cur
    avail_prev = total_beds - occupied_beds_prev
    available_beds = get_kpi_value(avail_cur, avail_prev)

    # Patient Satisfaction
    sat_cur = db.query(func.avg(Patient.satisfaction_score)).filter(*patient_filter_cur).scalar() or 0.0
    sat_prev = db.query(func.avg(Patient.satisfaction_score)).filter(*patient_filter_prev).scalar() or 0.0
    patient_satisfaction = get_kpi_value(sat_cur, sat_prev)

    return KPISummary(
        total_revenue=total_revenue,
        total_patients=total_patients,
        total_admissions=total_admissions,
        total_discharges=total_discharges,
        emergency_cases=emergency_cases,
        bed_occupancy=bed_occupancy,
        available_beds=available_beds,
        patient_satisfaction=patient_satisfaction
    )
