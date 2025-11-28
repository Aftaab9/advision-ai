from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# For local dev: SQLite database file in backend/ folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./advision.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed only for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
