import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add the parent directory to sys.path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.models.base import Base
from app.models.hospital import Department, Patient, Doctor, Appointment, Admission, Billing, Bed

def seed_data():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data
    session.query(Billing).delete()
    session.query(Admission).delete()
    session.query(Appointment).delete()
    session.query(Bed).delete()
    session.query(Doctor).delete()
    session.query(Patient).delete()
    session.query(Department).delete()
    session.commit()

    # Create Departments
    departments = [
        Department(name="Cardiology", description="Heart related treatments"),
        Department(name="Neurology", description="Brain and nervous system"),
        Department(name="Orthopedics", description="Bones and joints"),
        Department(name="Pediatrics", description="Children's health"),
        Department(name="Emergency", description="Emergency care"),
    ]
    session.add_all(departments)
    session.commit()

    departments = session.query(Department).all()

    # Create Doctors
    specializations = ["Surgeon", "Consultant", "Specialist", "General"]
    doctors = []
    for i in range(20):
        doc = Doctor(
            name=f"Dr. Smith_{i}",
            department_id=random.choice(departments).id,
            specialization=random.choice(specializations),
            status="Active"
        )
        doctors.append(doc)
    session.add_all(doctors)
    session.commit()
    doctors = session.query(Doctor).all()

    # Create Beds
    beds = []
    for dept in departments:
        for _ in range(50):
            bed = Bed(
                department_id=dept.id,
                status=random.choices(["Occupied", "Available", "Maintenance"], weights=[80, 15, 5])[0]
            )
            beds.append(bed)
    session.add_all(beds)
    session.commit()

    # Create Patients
    patients = []
    genders = ["Male", "Female"]
    for i in range(500):
        patient = Patient(
            age=random.randint(1, 90),
            gender=random.choice(genders),
            department_id=random.choice(departments).id,
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 365))
        )
        patients.append(patient)
    session.add_all(patients)
    session.commit()
    patients = session.query(Patient).all()

    # Create Appointments & Admissions & Billing
    appointments = []
    admissions = []
    billings = []

    statuses = ["Completed", "Completed", "Completed", "Cancelled", "Scheduled"]
    
    for patient in patients:
        # Appointments
        for _ in range(random.randint(1, 5)):
            appt = Appointment(
                patient_id=patient.id,
                doctor_id=random.choice(doctors).id,
                department_id=patient.department_id,
                appointment_date=datetime.utcnow() - timedelta(days=random.randint(0, 365)),
                status=random.choice(statuses)
            )
            appointments.append(appt)

        # Admissions
        if random.random() < 0.2:
            admission_date = datetime.utcnow() - timedelta(days=random.randint(10, 300))
            discharge_date = admission_date + timedelta(days=random.randint(1, 14))
            admission = Admission(
                patient_id=patient.id,
                department_id=patient.department_id,
                admission_date=admission_date,
                discharge_date=discharge_date,
                status="Discharged"
            )
            admissions.append(admission)

        # Billing
        for _ in range(random.randint(1, 3)):
            billing = Billing(
                patient_id=patient.id,
                department_id=patient.department_id,
                amount=round(random.uniform(100.0, 5000.0), 2),
                payment_status=random.choices(["Paid", "Pending"], weights=[90, 10])[0],
                billing_date=datetime.utcnow() - timedelta(days=random.randint(0, 365))
            )
            billings.append(billing)

    session.add_all(appointments)
    session.add_all(admissions)
    session.add_all(billings)
    session.commit()

    print("Data seeded successfully!")

if __name__ == "__main__":
    seed_data()
