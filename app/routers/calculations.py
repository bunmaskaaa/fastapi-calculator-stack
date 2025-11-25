# app/routers/calculations.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/calculations", tags=["calculations"])


@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def create_calculation(
    calc_in: schemas.CalculationCreate,
    db: Session = Depends(get_db),
):
    calc = models.Calculation(
        operation=calc_in.operation,
        operand_a=calc_in.operand_a,
        operand_b=calc_in.operand_b,
        result=calc_in.result,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


@router.get("/", response_model=List[schemas.CalculationRead])
def list_calculations(db: Session = Depends(get_db)):
    return db.query(models.Calculation).all()


@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def get_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.get(models.Calculation, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def update_calculation(
    calc_id: int,
    calc_in: schemas.CalculationCreate,
    db: Session = Depends(get_db),
):
    calc = db.get(models.Calculation, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    calc.operation = calc_in.operation
    calc.operand_a = calc_in.operand_a
    calc.operand_b = calc_in.operand_b
    calc.result = calc_in.result

    db.commit()
    db.refresh(calc)
    return calc


@router.patch("/{calc_id}", response_model=schemas.CalculationRead)
def partial_update_calculation(
    calc_id: int,
    calc_in: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    calc = db.get(models.Calculation, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    update_data = calc_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(calc, field, value)

    db.commit()
    db.refresh(calc)
    return calc


@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.get(models.Calculation, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    db.delete(calc)
    db.commit()
    return None