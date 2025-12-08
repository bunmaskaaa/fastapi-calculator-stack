from typing import Optional, List

from sqlalchemy.orm import Session

from app import models, schemas


def create_calculation(
    db: Session, calculation_in: schemas.CalculationCreate
) -> models.Calculation:
    """
    Create a new calculation row from a CalculationCreate schema.
    Uses operand_a and operand_b to match the SQLAlchemy model.
    """
    calc = models.Calculation(
        operation=calculation_in.operation,
        operand_a=calculation_in.operand_a,
        operand_b=calculation_in.operand_b,
        result=calculation_in.result,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


def get_calculations(db: Session) -> List[models.Calculation]:
    """
    Return all calculations, newest first.
    """
    return (
        db.query(models.Calculation)
        .order_by(models.Calculation.created_at.desc())
        .all()
    )


def get_calculation(db: Session, calc_id: int) -> Optional[models.Calculation]:
    """
    Return a single calculation by id, or None.
    """
    return (
        db.query(models.Calculation)
        .filter(models.Calculation.id == calc_id)
        .first()
    )


def update_calculation(
    db: Session,
    db_calc: models.Calculation,
    calculation_in: schemas.CalculationUpdate,
) -> models.Calculation:
    """
    Full or partial update of an existing calculation.
    Only fields provided in CalculationUpdate are modified.
    """
    data = calculation_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_calc, field, value)
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


def delete_calculation(db: Session, db_calc: models.Calculation) -> None:
    """
    Delete a calculation and commit the change.
    """
    db.delete(db_calc)
    db.commit()