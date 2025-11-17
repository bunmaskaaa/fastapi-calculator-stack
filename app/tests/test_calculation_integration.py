import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.models.user import User
from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate, CalculationType
from app.crud.calculation import create_calculation

# Use sqlite for CI/local tests by default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./calc_test.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Recreate tables for a clean test DB
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_insert_calculation(db):
    data = CalculationCreate(a=12, b=4, type=CalculationType.divide)
    calc = create_calculation(db, data)
    assert calc.result == 3

    saved = db.query(Calculation).filter_by(id=calc.id).first()
    assert saved is not None
    assert saved.result == 3