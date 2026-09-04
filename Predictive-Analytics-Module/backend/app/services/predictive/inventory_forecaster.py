import pandas as pd
from datetime import timedelta
from .base import BaseForecaster
from .ai_explanation import AIExplanationService

class InventoryForecaster(BaseForecaster):
    def __init__(self):
        super().__init__("inventory.csv")
        
    async def forecast(self) -> list:
        df = self.load_data()
        results = []
        
        for medicine in df['medicine_name'].unique():
            med_df = df[df['medicine_name'] == medicine].copy()
            if len(med_df) < 2:
                continue
                
            last_record = med_df.iloc[-1]
            current_stock = float(last_record['closing_stock'])
            
            # Use recent 30 days to calculate average daily consumption
            recent = med_df.tail(30)
            avg_daily_consumption = recent['consumed'].mean()
            
            if avg_daily_consumption <= 0:
                days_until_stockout = 999
                risk = "LOW"
            else:
                days_until_stockout = int(current_stock / avg_daily_consumption)
                if days_until_stockout < 7:
                    risk = "HIGH"
                elif days_until_stockout < 14:
                    risk = "MEDIUM"
                else:
                    risk = "LOW"
                    
            recommended_reorder = avg_daily_consumption * 30 # Recommend 30 days stock
            
            context = f"{medicine} has {current_stock} stock left. With average daily consumption of {avg_daily_consumption:.1f}, stockout in {days_until_stockout} days. Risk is {risk}."
            fallback = f"{medicine} is at {risk} risk of stockout in {days_until_stockout} days. Consider reordering {recommended_reorder:.0f} units."
            
            explanation = await AIExplanationService.get_explanation(context, fallback)
            
            results.append({
                "medicine": medicine,
                "current_stock": current_stock,
                "daily_consumption": float(avg_daily_consumption),
                "days_until_stockout": days_until_stockout,
                "risk": risk,
                "recommended_reorder": float(recommended_reorder),
                "explanation": explanation
            })
            
        return results
