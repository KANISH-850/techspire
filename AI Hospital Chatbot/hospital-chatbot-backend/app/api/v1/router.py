from fastapi import APIRouter
from . import dashboard
from . import predictive
from . import reports
from . import inventory

api_router = APIRouter()
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(predictive.router, prefix="/predictive", tags=["predictive"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
