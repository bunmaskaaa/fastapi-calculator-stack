# app/db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DEFAULT_DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_db"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)
print(">>> USING DATABASE_URL (app.db.database):", DATABASE_URL)

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()