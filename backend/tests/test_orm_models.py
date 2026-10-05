import sys
import os
from datetime import datetime, date, timezone
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import (
    Base, User, Department, Patient, Admission, Appointment, Bed,
    Transaction, HospitalExpense, Alert, Vendor, InventoryItem,
    PurchaseOrder, PurchaseOrderItem, Conversation, Message
)

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_full_orm_lifecycle(db_session):
    # 1. User
    user = User(username="admin", email="admin@hms.com", hashed_password="hashed_secret")
    db_session.add(user)
    db_session.commit()

    # 2. Department
    dept = Department(name="Cardiology", budget=500000.0)
    db_session.add(dept)
    db_session.commit()

    # 3. Patient
    patient = Patient(
        name="John Doe",
        age=45,
        gender="Male",
        department_id=dept.id,
        admission_date=datetime.now(timezone.utc),
        status="Admitted",
        satisfaction_score=9.5
    )
    db_session.add(patient)
    db_session.commit()

    # 4. Admission
    admission = Admission(
        patient_id=patient.id,
        department_id=dept.id,
        admission_date=datetime.now(timezone.utc),
        status="Admitted"
    )
    db_session.add(admission)

    # 5. Appointment
    appointment = Appointment(
        patient_id=patient.id,
        department_id=dept.id,
        appointment_date=datetime.now(timezone.utc),
        status="Scheduled"
    )
    db_session.add(appointment)

    # 6. Bed
    bed = Bed(department_id=dept.id, bed_number="CARD-101", status="Occupied")
    db_session.add(bed)

    # 7. Transaction & Expense
    tx = Transaction(department_id=dept.id, amount=1200.0, transaction_type="revenue")
    expense = HospitalExpense(description="ECG Machine Maintenance", amount=350.0)
    db_session.add_all([tx, expense])

    # 8. Alert
    alert = Alert(
        severity="HIGH",
        title="High Bed Occupancy",
        description="Cardiology occupancy exceeded 90%",
        department_id=dept.id,
        metric="occupancy",
        value="92%",
        threshold="90%"
    )
    db_session.add(alert)

    # 9. Vendor
    vendor = Vendor(
        name="PharmaCorp",
        contact_person="Alice Smith",
        email="contact@pharmacorp.com",
        phone="555-0199",
        average_delivery_days=3,
        reliability_score=98.5
    )
    db_session.add(vendor)
    db_session.commit()

    # 10. InventoryItem
    item = InventoryItem(
        name="Aspirin 100mg",
        category="Medication",
        sku="MED-ASP-100",
        batch_number="BATCH-2026-A",
        current_stock=150,
        minimum_stock=50,
        maximum_stock=500,
        daily_consumption=25.0,
        unit="Tablets",
        unit_price=0.50,
        expiry_date=date(2027, 12, 31),
        vendor_id=vendor.id
    )
    db_session.add(item)
    db_session.commit()

    # 11. PurchaseOrder & Items
    po = PurchaseOrder(
        vendor_id=vendor.id,
        status="Pending",
        total_amount=250.0,
        expected_delivery_date=datetime.now(timezone.utc)
    )
    db_session.add(po)
    db_session.commit()

    po_item = PurchaseOrderItem(
        purchase_order_id=po.id,
        inventory_item_id=item.id,
        quantity=500,
        unit_price=0.50,
        total_price=250.0
    )
    db_session.add(po_item)

    # 12. Conversation & Message
    conv = Conversation(title="Patient Inquiry - John Doe", status="active")
    db_session.add(conv)
    db_session.commit()

    msg1 = Message(conversation_id=conv.id, role="user", content="Where is John Doe admitted?")
    msg2 = Message(conversation_id=conv.id, role="assistant", content="John Doe is admitted in Cardiology, Bed CARD-101.")
    db_session.add_all([msg1, msg2])
    db_session.commit()

    # Assertions & Verification of ORM relationships
    assert user.id is not None
    assert dept.patients[0].name == "John Doe"
    assert len(dept.beds) == 1
    assert dept.beds[0].bed_number == "CARD-101"
    assert len(patient.appointments) == 1
    assert len(patient.admissions) == 1
    assert vendor.inventory_items[0].name == "Aspirin 100mg"
    assert len(po.items) == 1
    assert po.items[0].inventory_item.name == "Aspirin 100mg"
    assert len(conv.messages) == 2
    assert conv.messages[1].role == "assistant"

    print("All 14+ ORM canonical models and relationships verified successfully!")
