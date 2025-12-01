# app/schemas.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# =======================
# Calculation Schemas
# =======================

class CalculationBase(BaseModel):
    operation: str
    operand_a: float
    operand_b: float


class CalculationCreate(CalculationBase):
    pass


class CalculationRead(CalculationBase):
    id: int
    result: float
    created_at: datetime
    user_id: Optional[int] = None

    class Config:
        from_attributes = True  # Pydantic v2; use from_orm=True in v1


# =======================
# Auth / User Schemas
# =======================

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"