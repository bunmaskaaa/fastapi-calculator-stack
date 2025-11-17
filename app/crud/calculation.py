from sqlalchemy.orm import Session

from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate
from app.services.calculation_factory import get_operation


def create_calculation(db: Session, data: CalculationCreate, user_id: int | None = None) -> Calculation:
    operation = get_operation(data.type)
    result = operation.compute(data.a, data.b)

    calc = Calculation(
        a=data.a,
        b=data.b,
        type=data.type.value,
        result=result,
        user_id=user_id,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc