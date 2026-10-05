import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import HMSException, hms_exception_handler

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

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Unified Backend API for the Hospital Management System.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HMSException, hms_exception_handler)

# Register Unified API Routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(health_router, prefix=f"{settings.API_V1_STR}/health", tags=["Health"])
app.include_router(dashboard_router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])
app.include_router(chatbot_router, prefix=f"{settings.API_V1_STR}/chatbot", tags=["Chatbot"])
app.include_router(predictive_router, prefix=f"{settings.API_V1_STR}/predictive", tags=["Predictive Analytics"])
app.include_router(reports_router, prefix=f"{settings.API_V1_STR}/reports", tags=["Report Builder"])
app.include_router(inventory_router, prefix=f"{settings.API_V1_STR}/inventory", tags=["Inventory"])
app.include_router(procurement_router, prefix=f"{settings.API_V1_STR}/procurement", tags=["Procurement"])
app.include_router(patients_router, prefix=f"{settings.API_V1_STR}/patients", tags=["Patients"])
app.include_router(appointments_router, prefix=f"{settings.API_V1_STR}/appointments", tags=["Appointments"])
app.include_router(admissions_router, prefix=f"{settings.API_V1_STR}/admissions", tags=["Admissions"])
app.include_router(beds_router, prefix=f"{settings.API_V1_STR}/beds", tags=["Beds"])

@app.get("/", tags=["Root"])
def root():
    return {"message": f"Welcome to {settings.APP_NAME}", "version": settings.APP_VERSION}
