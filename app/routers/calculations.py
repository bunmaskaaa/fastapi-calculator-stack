from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud_calculations, schemas

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_calculation(
    calculation_in: schemas.CalculationCreate,
    db: Session = Depends(get_db),
):
    """
    Add (Create) a new calculation.
    """
    return crud_calculations.create_calculation(db, calculation_in)


@router.get(
    "/",
    response_model=list[schemas.CalculationRead],
    status_code=status.HTTP_200_OK,
)
def list_calculations(
    db: Session = Depends(get_db),
):
    """
    Browse: list all calculations.
    """
    return crud_calculations.get_calculations(db)


@router.get(
    "/{calc_id}",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_200_OK,
)
def get_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
):
    """
    Read: get a specific calculation.
    """
    db_calc = crud_calculations.get_calculation(db, calc_id)
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return db_calc


@router.put(
    "/{calc_id}",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_200_OK,
)
def update_calculation_full(
    calc_id: int,
    calculation_in: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    """
    Edit: full update (PUT).
    """
    db_calc = crud_calculations.get_calculation(db, calc_id)
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    return crud_calculations.update_calculation(db, db_calc, calculation_in)


@router.patch(
    "/{calc_id}",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_200_OK,
)
def update_calculation_partial(
    calc_id: int,
    calculation_in: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    """
    Edit: partial update (PATCH).
    """
    db_calc = crud_calculations.get_calculation(db, calc_id)
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    return crud_calculations.update_calculation(db, db_calc, calculation_in)


@router.delete(
    "/{calc_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete: remove a calculation.
    """
    db_calc = crud_calculations.get_calculation(db, calc_id)
    if not db_calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    crud_calculations.delete_calculation(db, db_calc)
    return None