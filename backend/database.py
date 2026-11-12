"""
SQLAlchemy database setup for ShopMate AI.
Uses SQLite for persistent local storage.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# ---------------------------------------------------------------------------
# Database URL
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'shopmate.db')}"

# ---------------------------------------------------------------------------
# Engine & Session
# ---------------------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite + FastAPI
    echo=False,  # Set to True to log SQL queries during debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


# ---------------------------------------------------------------------------
# Dependency for FastAPI routes (get DB session)
# ---------------------------------------------------------------------------
def get_db():
    """Yields a SQLAlchemy session and closes it when done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

