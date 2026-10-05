import sys
import os
from datetime import datetime, date, timedelta, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.core.config import settings
from app.models import (
    User, Department, Bed, Patient, Admission, Appointment,
    Transaction, HospitalExpense, Alert, Vendor, InventoryItem, PurchaseOrder
)

def seed_database():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(User).filter(User.username == settings.SEED_ADMIN_USERNAME).first():
            print("Database already seeded.")
            return

        print("Seeding database with initial HMS data...")

        # 1. Admin User
        admin_user = User(
            username=settings.SEED_ADMIN_USERNAME,
            email=settings.SEED_ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.SEED_ADMIN_PASSWORD),
            is_active=True
        )
        db.add(admin_user)



        # 2. Departments
        cardiology = Department(name="Cardiology", budget=500000.0)
        neurology = Department(name="Neurology", budget=450000.0)
        orthopedics = Department(name="Orthopedics", budget=350000.0)
        emergency = Department(name="Emergency", budget=600000.0)
        pediatrics = Department(name="Pediatrics", budget=300000.0)
        db.add_all([cardiology, neurology, orthopedics, emergency, pediatrics])
        db.commit()

        # 3. Beds
        beds = [
            Bed(department_id=cardiology.id, bed_number="CARD-101", status="Occupied"),
            Bed(department_id=cardiology.id, bed_number="CARD-102", status="Available"),
            Bed(department_id=neurology.id, bed_number="NEU-201", status="Occupied"),
            Bed(department_id=emergency.id, bed_number="EMG-001", status="Occupied"),
            Bed(department_id=emergency.id, bed_number="EMG-002", status="Available")
        ]
        db.add_all(beds)

        # 4. Patients
        now = datetime.now(timezone.utc)
        p1 = Patient(name="John Doe", age=45, gender="Male", department_id=cardiology.id, admission_date=now - timedelta(days=5), status="Admitted", satisfaction_score=9.2)
        p2 = Patient(name="Jane Smith", age=34, gender="Female", department_id=neurology.id, admission_date=now - timedelta(days=2), status="Admitted", satisfaction_score=8.8)
        p3 = Patient(name="Robert Johnson", age=58, gender="Male", department_id=emergency.id, admission_date=now - timedelta(days=1), status="Admitted", satisfaction_score=9.5)
        p4 = Patient(name="Emily Davis", age=29, gender="Female", department_id=pediatrics.id, admission_date=now - timedelta(days=10), discharge_date=now - timedelta(days=3), status="Discharged", satisfaction_score=9.0)
        db.add_all([p1, p2, p3, p4])
        db.commit()

        # 5. Admissions & Appointments
        adm1 = Admission(patient_id=p1.id, department_id=cardiology.id, admission_date=now - timedelta(days=5), status="Admitted")
        adm2 = Admission(patient_id=p4.id, department_id=pediatrics.id, admission_date=now - timedelta(days=10), discharge_date=now - timedelta(days=3), status="Discharged")
        appt1 = Appointment(patient_id=p1.id, department_id=cardiology.id, appointment_date=now + timedelta(days=1), status="Scheduled")
        db.add_all([adm1, adm2, appt1])

        # 6. Transactions & Historical Revenue (60 days)
        transactions = []
        for i in range(60, 0, -1):
            dt = now - timedelta(days=i)
            # Daily revenue for cardiology, neurology, emergency
            transactions.append(Transaction(department_id=cardiology.id, amount=12000.0 + (i * 50) + (i % 7) * 200, transaction_type="revenue", transaction_date=dt))
            transactions.append(Transaction(department_id=neurology.id, amount=8000.0 + (i * 30) + (i % 5) * 150, transaction_type="revenue", transaction_date=dt))
            transactions.append(Transaction(department_id=emergency.id, amount=15000.0 + (i * 40) + (i % 3) * 300, transaction_type="revenue", transaction_date=dt))
        
        exp1 = HospitalExpense(description="Medical Supplies Restock", amount=3200.0, expense_date=now - timedelta(days=3))
        db.add_all(transactions + [exp1])

        # 6b. Historical Admissions (60 days)
        historical_admissions = []
        for i in range(60, 0, -1):
            dt = now - timedelta(days=i)
            count = 10 + (i % 5)
            for k in range(count):
                historical_admissions.append(Admission(
                    patient_id=p1.id if k % 2 == 0 else p2.id,
                    department_id=cardiology.id if k % 3 == 0 else emergency.id,
                    admission_date=dt,
                    discharge_date=dt + timedelta(days=2) if k % 4 == 0 else None,
                    status="Admitted" if k % 4 != 0 else "Discharged"
                ))
        db.add_all(historical_admissions)
        db.commit()


        # 7. Alerts
        a1 = Alert(severity="HIGH", title="High ICU Occupancy", description="Cardiology bed utilization near capacity", department_id=cardiology.id, metric="occupancy", value="85%", threshold="80%")
        a2 = Alert(severity="CRITICAL", title="Low Stock Warning", description="Aspirin stock below minimum threshold", metric="stock", value="15 units", threshold="50 units")
        db.add_all([a1, a2])

        # 8. Vendors
        v1 = Vendor(name="PharmaCorp Ltd", contact_person="Alice Johnson", email="orders@pharmacorp.com", phone="555-0199", address="123 Pharma Way", average_delivery_days=3, reliability_score=98.5, rating=4.9)
        v2 = Vendor(name="MedSupply Global", contact_person="Bob Miller", email="support@medsupply.com", phone="555-0288", address="456 Supply Blvd", average_delivery_days=5, reliability_score=94.0, rating=4.7)
        db.add_all([v1, v2])
        db.commit()

        # 9. Inventory Items
        inv1 = InventoryItem(name="Aspirin 100mg", category="Medication", sku="MED-ASP-100", batch_number="B-2026-01", current_stock=15, minimum_stock=50, maximum_stock=500, daily_consumption=10.0, unit="Tablets", unit_price=0.50, expiry_date=date(2027, 6, 30), vendor_id=v1.id)
        inv2 = InventoryItem(name="Paracetamol 500mg", category="Medication", sku="MED-PAR-500", batch_number="B-2026-02", current_stock=350, minimum_stock=100, maximum_stock=1000, daily_consumption=25.0, unit="Tablets", unit_price=0.25, expiry_date=date(2027, 12, 31), vendor_id=v1.id)
        inv3 = InventoryItem(name="Surgical Gloves (M)", category="Supplies", sku="SUP-GLV-M", batch_number="B-2026-03", current_stock=120, minimum_stock=200, maximum_stock=1000, daily_consumption=40.0, unit="Pairs", unit_price=1.20, expiry_date=date(2028, 1, 15), vendor_id=v2.id)
        db.add_all([inv1, inv2, inv3])
        db.commit()

        # 10. Purchase Order
        po1 = PurchaseOrder(vendor_id=v1.id, status="Pending", total_amount=250.0, expected_delivery_date=now + timedelta(days=3))
        db.add(po1)
        db.commit()

        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
