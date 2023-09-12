import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    os.environ.get('SQLALCHEMY_DATABASE_URI'),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db() -> Generator:
    """Return a session context manager.

    Yields:
        Session: Database session instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
