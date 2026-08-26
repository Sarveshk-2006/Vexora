import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base Declarative Class for ORM Models."""

    pass


# Lazy or resilient Engine creation
engine = None
SessionLocal = None

try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=False,
    )
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
except Exception as e:
    logger.warning(
        f"Database engine initialization failed for URL "
        f"'{settings.DATABASE_URL}': {e}. "
        "Application will continue running in offline/unconnected mode."
    )


def get_db() -> Generator[Session, None, None]:
    """Dependency generator for obtaining a database session.
    Yields None or raises if session cannot be established.
    """
    if SessionLocal is None:
        logger.error(
            "Attempted to access DB session when SessionLocal is not initialized."
        )
        raise RuntimeError("Database engine is not initialized.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
