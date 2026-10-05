from typing import Optional
from sqlalchemy.orm import Session
from app.services.predictive.revenue_forecaster import RevenueForecaster
from app.services.predictive.admissions_forecaster import AdmissionsForecaster
from app.services.predictive.bed_occupancy_forecaster import BedOccupancyForecaster
from app.services.predictive.medicine_demand_forecaster import MedicineDemandForecaster
from app.services.predictive.inventory_forecaster import InventoryForecaster

class PredictiveService:
    @staticmethod
    async def get_revenue_forecast(days: int = 30, db: Optional[Session] = None) -> dict:
        forecaster = RevenueForecaster(db=db)
        return await forecaster.forecast(days=days)

    @staticmethod
    async def get_admissions_forecast(days: int = 30, db: Optional[Session] = None) -> dict:
        forecaster = AdmissionsForecaster(db=db)
        return await forecaster.forecast(days=days)

    @staticmethod
    async def get_bed_occupancy_forecast(days: int = 7, db: Optional[Session] = None) -> dict:
        forecaster = BedOccupancyForecaster(db=db)
        return await forecaster.forecast(days=days)

    @staticmethod
    async def get_medicine_demand_forecast(days: int = 30, db: Optional[Session] = None) -> list:
        forecaster = MedicineDemandForecaster(db=db)
        return await forecaster.forecast(days=days)

    @staticmethod
    async def get_inventory_forecast(db: Optional[Session] = None) -> list:
        forecaster = InventoryForecaster(db=db)
        return await forecaster.forecast()

    @staticmethod
    async def get_summary(db: Optional[Session] = None) -> dict:
        rev = RevenueForecaster(db=db)
        adm = AdmissionsForecaster(db=db)
        bed = BedOccupancyForecaster(db=db)

        rev_res = await rev.forecast(days=7)
        adm_res = await adm.forecast(days=7)
        bed_res = await bed.forecast(days=7)

        peak_bed = max([x["value"] for x in bed_res.get("forecast", [])]) if bed_res.get("forecast") else 0.0

        return {
            "revenue_trend": rev_res.get("trend", "stable"),
            "admissions_trend": adm_res.get("trend", "stable"),
            "bed_occupancy_peak": peak_bed,
            "data_source": rev_res.get("data_source", "POSTGRESQL_DB")
        }

