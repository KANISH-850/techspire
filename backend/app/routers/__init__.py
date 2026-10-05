from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.dashboard import router as dashboard_router
from app.routers.chatbot import router as chatbot_router
from app.routers.predictive import router as predictive_router
from app.routers.reports import router as reports_router
from app.routers.inventory import router as inventory_router
from app.routers.procurement import router as procurement_router
from app.routers.patients import router as patients_router
from app.routers.appointments import router as appointments_router
from app.routers.admissions import router as admissions_router
from app.routers.beds import router as beds_router

__all__ = [
    "auth_router",
    "health_router",
    "dashboard_router",
    "chatbot_router",
    "predictive_router",
    "reports_router",
    "inventory_router",
    "procurement_router",
    "patients_router",
    "appointments_router",
    "admissions_router",
    "beds_router"
]
