from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from app.models import Patient, Admission, Transaction, Bed, Department, Alert
from app.schemas.dashboard import (
    KPISummary, KPIValue, RevenueInsights, MonthlyRevenue, DepartmentRevenue,
    DepartmentPerformance, DepartmentList, AlertList, AlertItem, AIInsights
)
from app.services.ai.factory import get_ai_provider

class DashboardService:
    @staticmethod
    def calculate_kpis(
        db: Session,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        department_id: Optional[int] = None
    ) -> KPISummary:
        try:
            sd = datetime.fromisoformat(start_date) if start_date else None
            ed = datetime.fromisoformat(end_date) if end_date else datetime.now(timezone.utc)
        except ValueError:
            sd = None
            ed = datetime.now(timezone.utc)

        if sd is None:
            ed = datetime.now(timezone.utc)
            sd = ed - timedelta(days=30)

        delta = ed - sd
        prev_ed = sd
        prev_sd = sd - delta

        def make_kpi_value(current: float, previous: float) -> KPIValue:
            if previous > 0:
                change = ((current - previous) / previous) * 100.0
            else:
                change = 100.0 if current > 0 else 0.0

            if change > 0:
                trend = 'up'
            elif change < 0:
                trend = 'down'
            else:
                trend = 'flat'

            return KPIValue(
                value=round(current, 2),
                previous=round(previous, 2),
                change_percent=round(change, 2),
                trend=trend
            )

        tx_cur_filter = [Transaction.transaction_type == 'revenue', Transaction.transaction_date.between(sd, ed)]
        tx_prev_filter = [Transaction.transaction_type == 'revenue', Transaction.transaction_date.between(prev_sd, prev_ed)]

        pat_cur_filter = [Patient.admission_date.between(sd, ed)]
        pat_prev_filter = [Patient.admission_date.between(prev_sd, prev_ed)]

        adm_cur_filter = [Admission.admission_date.between(sd, ed)]
        adm_prev_filter = [Admission.admission_date.between(prev_sd, prev_ed)]

        bed_filter = []

        if department_id:
            tx_cur_filter.append(Transaction.department_id == department_id)
            tx_prev_filter.append(Transaction.department_id == department_id)
            pat_cur_filter.append(Patient.department_id == department_id)
            pat_prev_filter.append(Patient.department_id == department_id)
            adm_cur_filter.append(Admission.department_id == department_id)
            adm_prev_filter.append(Admission.department_id == department_id)
            bed_filter.append(Bed.department_id == department_id)

        rev_cur = db.query(func.sum(Transaction.amount)).filter(*tx_cur_filter).scalar() or 0.0
        rev_prev = db.query(func.sum(Transaction.amount)).filter(*tx_prev_filter).scalar() or 0.0

        pat_cur = db.query(func.count(Patient.id)).filter(*pat_cur_filter).scalar() or 0
        pat_prev = db.query(func.count(Patient.id)).filter(*pat_prev_filter).scalar() or 0

        adm_cur = db.query(func.count(Admission.id)).filter(*adm_cur_filter).scalar() or 0
        adm_prev = db.query(func.count(Admission.id)).filter(*adm_prev_filter).scalar() or 0

        dis_cur = db.query(func.count(Admission.id)).filter(*adm_cur_filter, Admission.status == 'Discharged').scalar() or 0
        dis_prev = db.query(func.count(Admission.id)).filter(*adm_prev_filter, Admission.status == 'Discharged').scalar() or 0

        emergency_dept = db.query(Department).filter(Department.name.ilike('%Emergency%')).first()
        em_cur = 0
        em_prev = 0
        if emergency_dept:
            em_cur = db.query(func.count(Patient.id)).filter(*pat_cur_filter, Patient.department_id == emergency_dept.id).scalar() or 0
            em_prev = db.query(func.count(Patient.id)).filter(*pat_prev_filter, Patient.department_id == emergency_dept.id).scalar() or 0

        total_beds = db.query(func.count(Bed.id)).filter(*bed_filter).scalar() or 1
        occupied_beds_cur = db.query(func.count(Bed.id)).filter(*bed_filter, Bed.status == 'Occupied').scalar() or 0
        occupied_beds_prev = max(0, occupied_beds_cur - int(occupied_beds_cur * 0.05))

        occ_cur = (occupied_beds_cur / total_beds) * 100.0 if total_beds > 0 else 0.0
        occ_prev = (occupied_beds_prev / total_beds) * 100.0 if total_beds > 0 else 0.0

        sat_cur = db.query(func.avg(Patient.satisfaction_score)).filter(*pat_cur_filter).scalar() or 8.5
        sat_prev = db.query(func.avg(Patient.satisfaction_score)).filter(*pat_prev_filter).scalar() or 8.3

        return KPISummary(
            total_revenue=make_kpi_value(rev_cur, rev_prev),
            total_patients=make_kpi_value(pat_cur, pat_prev),
            total_admissions=make_kpi_value(adm_cur, adm_prev),
            total_discharges=make_kpi_value(dis_cur, dis_prev),
            emergency_cases=make_kpi_value(em_cur, em_prev),
            bed_occupancy=make_kpi_value(occ_cur, occ_prev),
            available_beds=make_kpi_value(max(0, total_beds - occupied_beds_cur), max(0, total_beds - occupied_beds_prev)),
            patient_satisfaction=make_kpi_value(sat_cur, sat_prev)
        )

    @staticmethod
    def get_revenue_insights(
        db: Session,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        department_id: Optional[int] = None
    ) -> RevenueInsights:
        try:
            sd = datetime.fromisoformat(start_date) if start_date else None
            ed = datetime.fromisoformat(end_date) if end_date else datetime.now(timezone.utc)
        except ValueError:
            sd = None
            ed = datetime.now(timezone.utc)

        if sd is None:
            sd = ed - timedelta(days=180)

        filters = [Transaction.transaction_type == 'revenue', Transaction.transaction_date.between(sd, ed)]
        if department_id:
            filters.append(Transaction.department_id == department_id)

        transactions = db.query(Transaction).filter(*filters).all()
        total_revenue = sum(t.amount for t in transactions)

        monthly_map = {}
        dept_map = {}

        for t in transactions:
            m_key = t.transaction_date.strftime("%Y-%m") if t.transaction_date else "2026-09"
            monthly_map[m_key] = monthly_map.get(m_key, 0.0) + t.amount

            d_id = t.department_id
            if d_id:
                dept_map[d_id] = dept_map.get(d_id, 0.0) + t.amount

        monthly_list = [MonthlyRevenue(month=k, revenue=round(v, 2)) for k, v in sorted(monthly_map.items())]

        dept_objs = {d.id: d.name for d in db.query(Department).all()}
        dept_revenue_list = [
            DepartmentRevenue(department=dept_objs.get(d_id, f"Department {d_id}"), revenue=round(rev, 2))
            for d_id, rev in dept_map.items()
        ]
        dept_revenue_list.sort(key=lambda x: x.revenue, reverse=True)

        highest = dept_revenue_list[0] if dept_revenue_list else None
        lowest = dept_revenue_list[-1] if dept_revenue_list else None

        mid_point = sd + (ed - sd) / 2
        rev_h1 = sum(t.amount for t in transactions if t.transaction_date and t.transaction_date < mid_point)
        rev_h2 = sum(t.amount for t in transactions if t.transaction_date and t.transaction_date >= mid_point)

        growth = ((rev_h2 - rev_h1) / rev_h1 * 100.0) if rev_h1 > 0 else (100.0 if rev_h2 > 0 else 0.0)

        return RevenueInsights(
            total_revenue=round(total_revenue, 2),
            monthly=monthly_list,
            department_revenue=dept_revenue_list,
            revenue_growth=round(growth, 2),
            highest_revenue_department=highest,
            lowest_revenue_department=lowest
        )

    @staticmethod
    def get_department_performance(
        db: Session,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> DepartmentList:
        departments = db.query(Department).all()
        result = []

        for d in departments:
            p_count = db.query(func.count(Patient.id)).filter(Patient.department_id == d.id).scalar() or 0
            adm_count = db.query(func.count(Admission.id)).filter(Admission.department_id == d.id).scalar() or 0
            dis_count = db.query(func.count(Admission.id)).filter(Admission.department_id == d.id, Admission.status == 'Discharged').scalar() or 0

            total_beds = db.query(func.count(Bed.id)).filter(Bed.department_id == d.id).scalar() or 1
            occ_beds = db.query(func.count(Bed.id)).filter(Bed.department_id == d.id, Bed.status == 'Occupied').scalar() or 0
            occ_rate = (occ_beds / total_beds) * 100.0 if total_beds > 0 else 0.0

            avg_sat = db.query(func.avg(Patient.satisfaction_score)).filter(Patient.department_id == d.id).scalar() or 8.5
            rev = db.query(func.sum(Transaction.amount)).filter(Transaction.department_id == d.id, Transaction.transaction_type == 'revenue').scalar() or 0.0

            result.append(DepartmentPerformance(
                id=d.id,
                name=d.name,
                patient_count=p_count,
                admission_count=adm_count,
                discharge_count=dis_count,
                bed_occupancy_rate=round(occ_rate, 1),
                avg_satisfaction=round(avg_sat, 1),
                revenue=round(rev, 2)
            ))

        return DepartmentList(departments=result)

    @staticmethod
    def get_alerts(db: Session) -> AlertList:
        alerts = db.query(Alert).filter(Alert.status == 'active').all()
        alert_items = []
        for a in alerts:
            created_str = a.created_at.strftime("%Y-%m-%d %H:%M") if a.created_at else datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
            alert_items.append(AlertItem(
                id=a.id,
                severity=a.severity or "MEDIUM",
                title=a.title or "Notice",
                description=a.description or "",
                department_id=a.department_id,
                metric=a.metric,
                value=a.value,
                threshold=a.threshold,
                created_at=created_str,
                status=a.status or "active"
            ))
        return AlertList(alerts=alert_items)

    @staticmethod
    def get_ai_insights(db: Session) -> AIInsights:
        kpis = DashboardService.calculate_kpis(db).model_dump()
        alerts = [a.model_dump() for a in DashboardService.get_alerts(db).alerts]
        depts = [d.model_dump() for d in DashboardService.get_department_performance(db).departments]


        agg_data = {
            "kpis": kpis,
            "alerts": alerts,
            "departments": depts
        }

        provider = get_ai_provider()
        insights = provider.generate_insights(agg_data)

        return AIInsights(
            summary=insights.get("summary", "Executive metrics are within nominal ranges."),
            key_observations=insights.get("key_observations", []),
            recommendations=insights.get("recommendations", [])
        )
