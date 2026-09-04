import pandas as pd
import os

class FilterEngine:
    DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data", "reports")
    
    @classmethod
    def apply_filters(cls, dataset_name: str, start_date: str, end_date: str, department: str = "all", **kwargs) -> pd.DataFrame:
        file_path = os.path.join(cls.DATA_PATH, f"{dataset_name}.csv")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset {dataset_name} not found.")
            
        df = pd.read_csv(file_path)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
            
        if department and department.lower() != "all" and 'department' in df.columns:
            df = df[df['department'].str.lower() == department.lower()]
            
        # Optional kwargs filters
        for k, v in kwargs.items():
            if v and v.lower() != "all" and k in df.columns:
                df = df[df[k].astype(str).str.lower() == str(v).lower()]
                
        return df
