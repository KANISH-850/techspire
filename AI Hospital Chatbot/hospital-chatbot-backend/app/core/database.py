import logging
from typing import Generator


from sqlalchemy import create_engine, text

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm import sessionmaker, DeclarativeBase

# pyrefly: ignore [missing-import]
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine with connection pooling
try:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
        pool_pre_ping=True,
        echo=False
    )
    logger.info("Database engine created successfully.")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Create SessionLocal class for session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Declarative base class for models
class Base(DeclarativeBase):
    pass


# Dependency to get database session
def get_db() -> Generator:
    """
    Dependency injection for database session.
    Provides a new session per request and ensures it's closed afterward.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def check_database_connection() -> bool:
    """
    Check if the database connection is alive.
    Returns True if connection is successful, False otherwise.
    """
    try:
        with engine.connect() as connection:
            # Execute a simple query to ensure connectivity
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
