from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ==========================
# User / Auth Schemas
# ==========================

class UserCreate(BaseModel):
    # Tests send: username, email, password
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True  # Pydantic v2-friendly


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ==========================
# Calculation Schemas (BREAD)
# ==========================

class CalculationCreate(BaseModel):
    # Match what tests send:
    # {
    #   "operation": "add",
    #   "operand_a": 2.0,
    #   "operand_b": 3.0,
    #   "result": 5.0
    # }
    operation: str
    operand_a: float
    operand_b: float
    result: float


class CalculationUpdate(BaseModel):
    # For PATCH/PUT edits (all optional)
    operation: Optional[str] = None
    operand_a: Optional[float] = None
    operand_b: Optional[float] = None
    result: Optional[float] = None


class CalculationRead(BaseModel):
    id: int
    operation: str
    operand_a: float
    operand_b: float
    result: float
    # optional metadata, if present in model
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True