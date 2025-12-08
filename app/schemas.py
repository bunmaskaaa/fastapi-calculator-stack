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

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CalculationBase(BaseModel):
    operation: str
    operand_a: float
    operand_b: float
    result: float


class CalculationCreate(CalculationBase):
    pass


class CalculationUpdate(BaseModel):
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)