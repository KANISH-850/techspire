from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from app.models import Transaction, Department
from app.schemas import RevenueInsights, MonthlyRevenue, DepartmentRevenue

def get_revenue_insights(db: Session, start_date: str = None, end_date: str = None, department_id: int = None) -> RevenueInsights:
    try:
        sd = datetime.fromisoformat(start_date) if start_date else None
        ed = datetime.fromisoformat(end_date) if end_date else datetime.now(timezone.utc)
    except ValueError:
        sd = None
        ed = datetime.now(timezone.utc)

    if sd is None:
        sd = ed - timedelta(days=180) # Last 6 months default

    # Base filters
    filters = [Transaction.transaction_type == 'revenue', Transaction.transaction_date.between(sd, ed)]
    if department_id:
        filters.append(Transaction.department_id == department_id)

    # Total Revenue
    total_revenue = db.query(func.sum(Transaction.amount)).filter(*filters).scalar() or 0.0

    # Monthly Revenue (last 6 months generally)
    # Using python to group by month for cross-platform SQLite/Postgres compatibility
    transactions = db.query(Transaction).filter(*filters).all()
    monthly_data = {}
    dept_data = {}
    
    for t in transactions:
        month_key = t.transaction_date.strftime("%Y-%m")
        monthly_data[month_key] = monthly_data.get(month_key, 0) + t.amount
        
        dept_id = t.department_id
        dept_data[dept_id] = dept_data.get(dept_id, 0) + t.amount

    monthly = [MonthlyRevenue(month=k, revenue=v) for k, v in sorted(monthly_data.items())]

    # Department Revenue
    departments = db.query(Department).all()
    dept_map = {d.id: d.name for d in departments}
    
    department_revenue = []
    for d_id, rev in dept_data.items():
        if d_id in dept_map:
            department_revenue.append(DepartmentRevenue(department=dept_map[d_id], revenue=rev))

    # Sort and find highest/lowest
    department_revenue.sort(key=lambda x: x.revenue, reverse=True)
    highest = department_revenue[0] if department_revenue else None
    lowest = department_revenue[-1] if department_revenue else None

    # Growth (calculate based on first half vs second half of the period)
    mid_point = sd + (ed - sd) / 2
    mid_point = mid_point.replace(tzinfo=None)
    first_half_rev = sum(t.amount for t in transactions if t.transaction_date < mid_point)
    second_half_rev = sum(t.amount for t in transactions if t.transaction_date >= mid_point)
    
    revenue_growth = 0.0
    if first_half_rev > 0:
        revenue_growth = ((second_half_rev - first_half_rev) / first_half_rev) * 100
    elif second_half_rev > 0:
        revenue_growth = 100.0

    return RevenueInsights(
        total_revenue=total_revenue,
        monthly=monthly,
        department_revenue=department_revenue,
        revenue_growth=round(revenue_growth, 2),
        highest_revenue_department=highest,
        lowest_revenue_department=lowest
    )
