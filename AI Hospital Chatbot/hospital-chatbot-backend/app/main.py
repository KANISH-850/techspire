import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from app.core.config import settings
from app.core.logging import setup_logging
from app.shared.exceptions import (
    HospitalChatbotException,
    hospital_chatbot_exception_handler,
)

# Initialize structured logging before creating the app
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API for the Hospital AI Chatbot module.",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173", 
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
from app.modules.chatbot.api.router import router as chatbot_router
from app.modules.chatbot.api.auth_router import router as auth_router
app.include_router(chatbot_router, prefix=settings.API_V1_STR + '/chatbot', tags=['Chatbot'])
app.include_router(auth_router, prefix=settings.API_V1_STR + '/auth', tags=['Authentication'])

# Register custom exception handlers
app.add_exception_handler(HospitalChatbotException, hospital_chatbot_exception_handler)  # type: ignore



@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc: SQLAlchemyError):
    logger.error(f"Database error occurred: {exc}")
    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=400,
            content={"error": "Database constraint violation (e.g., User does not exist or duplicate entry).", "status": "error"},
        )
    return JSONResponse(
        status_code=500,
        content={"error": "A database error occurred.", "status": "error"},
    )


from sqlalchemy import text
from app.core.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint serving as a basic entry point.
    """
    return {"message": f"Welcome to {settings.APP_NAME}", "version": settings.APP_VERSION}

@app.get("/health/db", tags=["Health"])
def health_db(db: Session = Depends(get_db)):
    """
    Verify database connection by executing a simple SELECT 1 query.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Successfully connected to the database."}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )

@app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
def health_check():
    """
    Generic health check for the API.
    """
    return {"status": "ok", "message": "API is healthy"}
