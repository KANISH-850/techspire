from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any, List

class BaseReportAnalytics(ABC):
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    @abstractmethod
    def generate_kpis(self) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def generate_charts(self) -> List[Dict[str, Any]]:
        pass
        
    def get_table_data(self) -> List[Dict[str, Any]]:
        return self.df.fillna("").to_dict(orient="records")
        
    def generate_context_for_llm(self) -> str:
        kpis = self.generate_kpis()
        context = "Key Metrics:\n"
        for k, v in kpis.items():
            context += f"- {k.replace('_', ' ').title()}: {v}\n"
        return context
