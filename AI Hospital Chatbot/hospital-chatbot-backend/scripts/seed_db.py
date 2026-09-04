import sys
import os
from datetime import datetime, timedelta, timezone
import random

# Add backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import engine, SessionLocal
from app.core.database import Base
from app.models import Department, Patient, Appointment, Admission, Transaction, Bed, HospitalExpense, Alert, InventoryItem, Vendor, PurchaseOrder

from sqlalchemy import text

def reset_db():
    print("Dropping all existing tables...")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alerts CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS purchase_orders CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS inventory_items CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS vendors CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS billing CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS doctors CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS appointments CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS admissions CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS patients CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS transactions CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS beds CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS departments CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS hospital_expenses CASCADE;"))
        conn.commit()
    print("Creating tables based on current schema...")
    Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # Departments
        depts = [
            {"name": "Cardiology", "budget": 1200000.0, "beds": 40},
            {"name": "Neurology", "budget": 950000.0, "beds": 30},
            {"name": "Orthopedics", "budget": 1100000.0, "beds": 35},
            {"name": "Pediatrics", "budget": 800000.0, "beds": 25},
            {"name": "Emergency", "budget": 2000000.0, "beds": 50},
        ]
        
        department_objs = []
        for d in depts:
            dept = Department(name=d["name"], budget=d["budget"])
            db.add(dept)
            department_objs.append(dept)
        
        db.commit()
        
        # Reload to get IDs
        department_objs = db.query(Department).all()
        dept_map = {d.name: d for d in department_objs}
        
        print(f"Created {len(department_objs)} departments.")

        # Beds
        bed_objs = []
        for d in depts:
            dept = dept_map[d["name"]]
            prefix = d["name"][:4].upper()
            
            for i in range(1, d["beds"] + 1):
                status = random.choices(
                    ['Occupied', 'Available', 'Maintenance'],
                    weights=[0.75, 0.20, 0.05]
                )[0]
                
                bed = Bed(
                    department_id=dept.id,
                    bed_number=f"{prefix}-{i:03d}",
                    status=status
                )
                bed_objs.append(bed)
        
        db.add_all(bed_objs)
        db.commit()
        print(f"Created {len(bed_objs)} beds.")

        # Time range for realistic data (last 6 months)
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=180)
        
        # Patients, Admissions, Appointments, Transactions
        first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

        print("Generating patients, appointments, admissions, and transactions...")
        
        for i in range(600): # 600 total patients
            dept = random.choice(department_objs)
            admission_dt = start_date + timedelta(days=random.randint(0, 170))
            is_admitted = random.choice([True, False])
            discharge_dt = admission_dt + timedelta(days=random.randint(1, 14)) if (not is_admitted or random.random() > 0.3) else None
            status = 'Admitted' if discharge_dt is None else random.choice(['Discharged', 'Outpatient'])
            
            patient = Patient(
                name=f"{random.choice(first_names)} {random.choice(last_names)}",
                age=random.randint(1, 90),
                gender=random.choice(["Male", "Female"]),
                department_id=dept.id,
                admission_date=admission_dt,
                discharge_date=discharge_dt,
                status=status,
                satisfaction_score=round(random.uniform(5.0, 10.0), 1)
            )
            db.add(patient)
            db.commit() # commit to get patient ID
            
            # Appointments for this patient
            for _ in range(random.randint(1, 4)):
                appt_date = admission_dt + timedelta(days=random.randint(-30, 30))
                if appt_date > end_date:
                    appt_status = 'Scheduled'
                else:
                    appt_status = random.choices(['Completed', 'Cancelled', 'Scheduled'], weights=[0.8, 0.15, 0.05])[0]
                
                appt = Appointment(
                    patient_id=patient.id,
                    department_id=dept.id,
                    appointment_date=appt_date,
                    status=appt_status
                )
                db.add(appt)
            
            # Admission record if admitted
            if status in ['Admitted', 'Discharged']:
                adm = Admission(
                    patient_id=patient.id,
                    department_id=dept.id,
                    admission_date=admission_dt,
                    discharge_date=discharge_dt,
                    status=status
                )
                db.add(adm)
        
        db.commit()

        # Transactions (Revenue & Expenses)
        # Generate transactions distributed across the 6 months
        transactions = []
        expenses = []
        
        for i in range(180): # loop over each day
            current_day = start_date + timedelta(days=i)
            
            for dept in department_objs:
                # Daily Revenue for dept
                rev_amount = random.uniform(5000, 25000)
                # Boost revenue for Emergency and Cardiology
                if dept.name in ['Emergency', 'Cardiology']:
                    rev_amount *= 1.5
                    
                transactions.append(Transaction(
                    department_id=dept.id,
                    amount=rev_amount,
                    transaction_type='revenue',
                    transaction_date=current_day
                ))
                
                # Daily Expense for dept (indirect representation or general expense)
                exp_amount = rev_amount * random.uniform(0.4, 0.7) # 40-70% margin
                transactions.append(Transaction(
                    department_id=dept.id,
                    amount=exp_amount,
                    transaction_type='expense',
                    transaction_date=current_day
                ))

        # Hospital-wide general expenses
        for i in range(30):
            exp_date = start_date + timedelta(days=random.randint(0, 179))
            expenses.append(HospitalExpense(
                description=random.choice(["Equipment Maintenance", "Utility Bill", "Facility Upgrade", "Software License", "Marketing"]),
                amount=random.uniform(2000, 50000),
                expense_date=exp_date
            ))
            
        db.add_all(transactions)
        db.add_all(expenses)
        
        # Generate some alerts
        alerts = []
        for i in range(15):
            alert_date = start_date + timedelta(days=random.randint(150, 179))
            dept = random.choice(department_objs)
            severity = random.choices(['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'], weights=[0.1, 0.2, 0.4, 0.3])[0]
            if severity == 'CRITICAL':
                title = random.choice(["Extremely high occupancy", "Emergency overload", "Very low available beds", "Severe staff shortage"])
                description = f"{title} in {dept.name} department requires immediate attention."
            elif severity == 'HIGH':
                title = random.choice(["Revenue decline", "Department underperformance", "Low satisfaction", "High patient wait times"])
                description = f"{title} observed in {dept.name} over the last week."
            else:
                title = random.choice(["Increasing patient load", "Moderate revenue decline", "Equipment maintenance due"])
                description = f"{title} in {dept.name}. Monitor closely."
                
            alerts.append(Alert(
                severity=severity,
                title=title,
                description=description,
                department_id=dept.id,
                metric=random.choice(['occupancy', 'revenue', 'satisfaction', 'patients']),
                value=str(random.randint(50, 150)),
                threshold=str(random.randint(80, 100)),
                created_at=alert_date,
                status=random.choices(['active', 'resolved'], weights=[0.7, 0.3])[0]
            ))
            
        db.add_all(alerts)
        db.commit()

        print(f"Created {len(transactions)} transactions, {len(expenses)} hospital expenses, and {len(alerts)} alerts.")

        # Seed Vendors and Inventory Items
        vendors = [
            Vendor(name="MediSupply Co.", contact_email="orders@medisupply.com", delivery_time_days=2, reliability_score=9.5, rating=4.8),
            Vendor(name="PharmaPlus", contact_email="sales@pharmaplus.com", delivery_time_days=4, reliability_score=8.2, rating=4.1),
            Vendor(name="SurgicalEquip Ltd.", contact_email="contact@surgicalequip.com", delivery_time_days=7, reliability_score=9.0, rating=4.5)
        ]
        db.add_all(vendors)
        db.commit()

        v_map = {v.name: v for v in db.query(Vendor).all()}

        items = [
            {"name": "Paracetamol 500mg", "cat": "Medicine", "stock": 400, "min": 1000, "max": 5000, "daily": 150.0, "price": 0.5, "v": "PharmaPlus"},
            {"name": "Surgical Masks", "cat": "Consumables", "stock": 12000, "min": 5000, "max": 20000, "daily": 1000.0, "price": 0.2, "v": "MediSupply Co."},
            {"name": "Amoxicillin 250mg", "cat": "Medicine", "stock": 2500, "min": 2000, "max": 10000, "daily": 100.0, "price": 2.0, "v": "PharmaPlus"},
            {"name": "MRI Contrast Agent", "cat": "Specialty", "stock": 10, "min": 20, "max": 50, "daily": 2.0, "price": 500.0, "v": "SurgicalEquip Ltd."},
            {"name": "Oxygen Cylinder", "cat": "Consumables", "stock": 45, "min": 50, "max": 150, "daily": 15.0, "price": 45.0, "v": "MediSupply Co."}
        ]

        inv_items = []
        for it in items:
            inv = InventoryItem(
                name=it["name"],
                category=it["cat"],
                current_stock=it["stock"],
                minimum_stock=it["min"],
                maximum_stock=it["max"],
                daily_consumption=it["daily"],
                unit_price=it["price"],
                vendor_id=v_map[it["v"]].id,
                expiry_date=datetime.now(timezone.utc).date() + timedelta(days=random.randint(20, 365))
            )
            inv_items.append(inv)
        
        db.add_all(inv_items)
        db.commit()

        print(f"Created {len(vendors)} vendors and {len(inv_items)} inventory items.")
        print("Database seeded successfully with realistic mock data!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_db()
    seed_data()
