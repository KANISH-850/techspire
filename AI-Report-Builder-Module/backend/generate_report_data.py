import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "reports")

def ensure_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def generate_dates(days=365):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    return pd.date_range(start=start_date, end=end_date, freq='D')

def generate_financial(dates):
    departments = ['Cardiology', 'Neurology', 'Orthopedics', 'General', 'Emergency', 'Oncology', 'Pediatrics']
    data = []
    
    for date in dates:
        for dept in departments:
            # Transactions per department per day
            num_tx = np.random.randint(5, 50)
            for _ in range(num_tx):
                revenue = np.random.uniform(500, 5000)
                expense = revenue * np.random.uniform(0.3, 0.8)
                tx_type = np.random.choice(['Consultation', 'Surgery', 'Medication', 'Lab Test', 'Room Charge'])
                data.append([
                    date, dept, tx_type, round(revenue, 2), round(expense, 2), round(revenue - expense, 2)
                ])
                
    df = pd.DataFrame(data, columns=['date', 'department', 'transaction_type', 'revenue', 'expense', 'net_revenue'])
    df.to_csv(os.path.join(DATA_DIR, 'financial.csv'), index=False)

def generate_clinical(dates):
    departments = ['Cardiology', 'Neurology', 'Orthopedics', 'General', 'Emergency']
    data = []
    
    for date in dates:
        for dept in departments:
            admissions = np.random.randint(2, 30)
            if dept == 'Emergency':
                admissions += 20
                
            discharges = max(0, admissions + np.random.randint(-5, 5))
            emergency_cases = admissions if dept == 'Emergency' else int(admissions * np.random.uniform(0.1, 0.3))
            
            data.append([
                date, dept, admissions, discharges, emergency_cases
            ])
            
    df = pd.DataFrame(data, columns=['date', 'department', 'admissions', 'discharges', 'emergency_cases'])
    df.to_csv(os.path.join(DATA_DIR, 'clinical.csv'), index=False)

def generate_operational(dates):
    departments = ['Cardiology', 'Neurology', 'Orthopedics', 'General', 'Emergency']
    data = []
    
    for date in dates:
        for dept in departments:
            total_beds = 100
            occupied = np.random.randint(40, 95)
            critical_alerts = np.random.randint(0, 5)
            staff_on_duty = np.random.randint(10, 30)
            
            data.append([
                date, dept, total_beds, occupied, critical_alerts, staff_on_duty
            ])
            
    df = pd.DataFrame(data, columns=['date', 'department', 'total_beds', 'occupied_beds', 'critical_alerts', 'staff_on_duty'])
    df.to_csv(os.path.join(DATA_DIR, 'operational.csv'), index=False)

def generate_inventory(dates):
    medicines = ['Paracetamol', 'Amoxicillin', 'Insulin', 'Antibiotics', 'IV Fluids', 'Syringes', 'Bandages', 'O2 Cylinders']
    data = []
    
    current_date = dates[-1] # Only snapshot needed for inventory usually, but let's do timeseries
    
    for date in dates:
        for med in medicines:
            stock = np.random.randint(10, 5000)
            consumed = int(stock * np.random.uniform(0.01, 0.1))
            unit_price = np.random.uniform(5, 500)
            
            # 5% chance of being expired
            expired = int(stock * np.random.uniform(0.0, 0.1)) if np.random.random() < 0.05 else 0
            expiring_soon = int(stock * np.random.uniform(0.0, 0.2)) if np.random.random() < 0.1 else 0
            
            data.append([
                date, med, stock, consumed, expired, expiring_soon, round(stock * unit_price, 2)
            ])
            
    df = pd.DataFrame(data, columns=['date', 'item_name', 'current_stock', 'consumed', 'expired', 'expiring_soon', 'stock_value'])
    df.to_csv(os.path.join(DATA_DIR, 'inventory.csv'), index=False)

def generate_procurement(dates):
    vendors = ['MedSupply Co.', 'PharmaGlobal', 'HealthEquip Inc.', 'SurgicalTools Ltd.']
    data = []
    
    for date in dates:
        # Not every day has an order
        if np.random.random() > 0.3:
            continue
            
        num_orders = np.random.randint(1, 5)
        for _ in range(num_orders):
            vendor = np.random.choice(vendors)
            value = np.random.uniform(1000, 50000)
            status = np.random.choice(['Completed', 'Pending', 'Cancelled'], p=[0.7, 0.2, 0.1])
            delivery_time_days = np.random.randint(1, 14) if status == 'Completed' else None
            
            data.append([
                date, vendor, round(value, 2), status, delivery_time_days
            ])
            
    df = pd.DataFrame(data, columns=['date', 'vendor', 'purchase_value', 'status', 'delivery_time_days'])
    df.to_csv(os.path.join(DATA_DIR, 'procurement.csv'), index=False)

def main():
    ensure_dir()
    dates = generate_dates(180) # 6 months
    
    print("Generating Financial Data...")
    generate_financial(dates)
    print("Generating Clinical Data...")
    generate_clinical(dates)
    print("Generating Operational Data...")
    generate_operational(dates)
    print("Generating Inventory Data...")
    generate_inventory(dates)
    print("Generating Procurement Data...")
    generate_procurement(dates)
    
    print(f"Data generation complete! Files saved to: {DATA_DIR}")

if __name__ == "__main__":
    main()
