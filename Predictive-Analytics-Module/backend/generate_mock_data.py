import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "predictive")

def ensure_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def generate_dates(days=365):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    return pd.date_range(start=start_date, end=end_date, freq='D')

def generate_revenue(dates):
    departments = ['Cardiology', 'Neurology', 'Orthopedics', 'General', 'Emergency']
    data = []
    
    for date in dates:
        # Weekend effect (lower on weekends except Emergency)
        is_weekend = date.weekday() >= 5
        
        for dept in departments:
            base = np.random.randint(50000, 150000)
            if dept == 'Emergency':
                base += np.random.randint(20000, 50000)
            elif is_weekend:
                base = int(base * 0.6)
                
            # Add some noise and trend
            trend = (date - dates[0]).days * 10
            revenue = base + trend + np.random.randint(-10000, 10000)
            expenses = int(revenue * np.random.uniform(0.6, 0.8))
            net_revenue = revenue - expenses
            
            data.append([date, dept, revenue, expenses, net_revenue])
            
    df = pd.DataFrame(data, columns=['date', 'department', 'revenue', 'expenses', 'net_revenue'])
    df.to_csv(os.path.join(DATA_DIR, 'revenue.csv'), index=False)

def generate_admissions(dates):
    departments = ['Cardiology', 'Neurology', 'Orthopedics', 'General', 'Emergency']
    data = []
    
    for date in dates:
        is_weekend = date.weekday() >= 5
        
        for dept in departments:
            base_adm = np.random.randint(10, 50)
            if dept == 'Emergency':
                base_adm += np.random.randint(10, 30)
            elif is_weekend:
                base_adm = int(base_adm * 0.5)
                
            trend = int((date - dates[0]).days * 0.05)
            admissions = max(0, base_adm + trend + np.random.randint(-5, 5))
            
            emergency = int(admissions * np.random.uniform(0.1, 0.4))
            if dept == 'Emergency':
                emergency = admissions
                
            inpatient = int((admissions - emergency) * np.random.uniform(0.3, 0.7))
            outpatient = admissions - emergency - inpatient
            
            data.append([date, dept, admissions, emergency, outpatient, inpatient])
            
    df = pd.DataFrame(data, columns=['date', 'department', 'admissions', 'emergency_admissions', 'outpatient', 'inpatient'])
    df.to_csv(os.path.join(DATA_DIR, 'admissions.csv'), index=False)

def generate_bed_occupancy(dates):
    total_beds = 500
    data = []
    
    for date in dates:
        # Seasonal effect: higher in winter months
        month = date.month
        seasonal_multiplier = 1.2 if month in [11, 12, 1, 2] else 1.0
        
        base_occupancy = np.random.randint(300, 400)
        occupied_beds = int(base_occupancy * seasonal_multiplier) + np.random.randint(-20, 20)
        occupied_beds = min(total_beds, max(0, occupied_beds))
        occupancy_rate = round(occupied_beds / total_beds, 4)
        
        data.append([date, total_beds, occupied_beds, occupancy_rate])
        
    df = pd.DataFrame(data, columns=['date', 'total_beds', 'occupied_beds', 'occupancy_rate'])
    df.to_csv(os.path.join(DATA_DIR, 'bed_occupancy.csv'), index=False)

def generate_medicine_demand(dates):
    medicines = ['Paracetamol', 'Amoxicillin', 'Insulin', 'Antibiotics', 'IV Fluids']
    departments = ['General', 'Emergency', 'ICU']
    data = []
    
    for date in dates:
        for med in medicines:
            for dept in departments:
                base = np.random.randint(10, 100)
                if med == 'IV Fluids' and dept == 'Emergency':
                    base += 50
                    
                trend = int((date - dates[0]).days * 0.02)
                quantity = max(0, base + trend + np.random.randint(-5, 15))
                
                data.append([date, med, quantity, dept])
                
    df = pd.DataFrame(data, columns=['date', 'medicine_name', 'quantity_used', 'department'])
    df.to_csv(os.path.join(DATA_DIR, 'medicine_demand.csv'), index=False)

def generate_inventory(dates):
    medicines = ['Paracetamol', 'Amoxicillin', 'Insulin', 'Antibiotics', 'IV Fluids']
    data = []
    
    # Initial stocks
    current_stock = {med: np.random.randint(500, 2000) for med in medicines}
    
    for date in dates:
        for med in medicines:
            opening_stock = current_stock[med]
            consumed = np.random.randint(20, 150)
            
            # Received if stock is low (reorder point)
            received = 0
            if opening_stock - consumed < 300:
                received = np.random.randint(1000, 2000)
                
            closing_stock = max(0, opening_stock - consumed + received)
            current_stock[med] = closing_stock
            
            data.append([date, med, opening_stock, consumed, received, closing_stock])
            
    df = pd.DataFrame(data, columns=['date', 'medicine_name', 'opening_stock', 'consumed', 'received', 'closing_stock'])
    df.to_csv(os.path.join(DATA_DIR, 'inventory.csv'), index=False)

def main():
    ensure_dir()
    dates = generate_dates(365) # 1 year of data
    
    print("Generating Revenue Data...")
    generate_revenue(dates)
    
    print("Generating Admissions Data...")
    generate_admissions(dates)
    
    print("Generating Bed Occupancy Data...")
    generate_bed_occupancy(dates)
    
    print("Generating Medicine Demand Data...")
    generate_medicine_demand(dates)
    
    print("Generating Inventory Data...")
    generate_inventory(dates)
    
    print("Data generation complete! Files saved to:", DATA_DIR)

if __name__ == "__main__":
    main()
