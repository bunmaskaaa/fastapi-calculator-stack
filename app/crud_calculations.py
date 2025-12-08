from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


# ---------- Helpers ----------

def calculate_result(operation: str, a: float, b: float) -> float:
    op = operation.lower()
    if op == "add":
        return a + b
    elif op == "subtract":
        return a - b
    elif op == "multiply":
        return a * b
    elif op == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError(f"Unsupported operation: {operation}")


def get_or_create_system_user(db: Session) -> models.User:
    """
    Create or fetch a 'system' user to own calculations created without auth.
    No password hashing here to avoid bcrypt issues in tests.
    """
    email = "system@example.com"

    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return user

    user = models.User(
        username="system",
        email=email,
        hashed_password="not-used",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- CRUD operations ----------

def get_calculations(db: Session) -> List[models.Calculation]:
    return (
        db.query(models.Calculation)
        .order_by(models.Calculation.created_at.desc())
        .all()
    )


def get_calculation(db: Session, calc_id: int) -> Optional[models.Calculation]:
    return (
        db.query(models.Calculation)
        .filter(models.Calculation.id == calc_id)
        .first()
    )


def create_calculation(
    db: Session,
    data: schemas.CalculationCreate,
) -> models.Calculation:
    """
    Create a calculation.

    For this assignment & tests, we trust the `result` that comes from the client.
    """
    system_user = get_or_create_system_user(db)

    calc = models.Calculation(
        user_id=system_user.id,
        operation=data.operation,
        operand1=data.operand_a,
        operand2=data.operand_b,
        result=data.result,  # use the client-provided result
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


def update_calculation(
    db: Session,
    calc_id: int,
    data: schemas.CalculationUpdate,
) -> Optional[models.Calculation]:
    calc = get_calculation(db, calc_id)
    if not calc:
        return None

    operation_changed = False
    operands_changed = False

    if data.operation is not None:
        calc.operation = data.operation
        operation_changed = True
    if data.operand_a is not None:
        calc.operand1 = data.operand_a
        operands_changed = True
    if data.operand_b is not None:
        calc.operand2 = data.operand_b
        operands_changed = True

    # If caller explicitly sends a result, trust that value
    if data.result is not None:
        calc.result = data.result
    # Otherwise, if something about the operation/operands changed, recompute
    elif operation_changed or operands_changed:
        calc.result = calculate_result(calc.operation, calc.operand1, calc.operand2)

    db.commit()
    db.refresh(calc)
    return calc


def delete_calculation(db: Session, calc_id: int) -> bool:
    calc = get_calculation(db, calc_id)
    if not calc:
        return False
    db.delete(calc)
    db.commit()
    return True