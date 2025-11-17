from enum import Enum
from typing import Optional

from pydantic import BaseModel, model_validator


class CalculationType(str, Enum):
    add = "add"
    sub = "sub"
    multiply = "multiply"
    divide = "divide"


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType

    @model_validator(mode="after")
    def validate_division(self):
        if self.type == CalculationType.divide and self.b == 0:
            raise ValueError("Cannot divide by zero.")
        return self


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: Optional[float] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True