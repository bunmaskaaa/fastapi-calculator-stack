# app/schemas.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- User Schemas ----------

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # FastAPI / SQLAlchemy 2.x compatible


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------- Calculation Schemas ----------

class CalculationBase(BaseModel):
    operation: str
    operand_a: float
    operand_b: float


class CalculationCreate(CalculationBase):
    # For this assignment, we'll send the result from the client/tests
    # (you could also compute it on the server if you want).
    result: float


class CalculationUpdate(BaseModel):
    operation: Optional[str] = None
    operand_a: Optional[float] = None
    operand_b: Optional[float] = None
    result: Optional[float] = None


class CalculationRead(CalculationBase):
    id: int
    result: float
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True