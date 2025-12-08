from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from .. import crud_calculations

router = APIRouter(
    prefix="/calculations",
    tags=["calculations"],
)


@router.post(
    "/",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_calculation(
    payload: schemas.CalculationCreate,
    db: Session = Depends(get_db),
):
    """
    Add: POST /calculations/
    No auth required for tests.
    """
    calc = crud_calculations.create_calculation(db, payload)
    return calc


@router.get(
    "/",
    response_model=List[schemas.CalculationRead],
)
def browse_calculations(
    db: Session = Depends(get_db),
):
    """
    Browse: GET /calculations/
    """
    return crud_calculations.get_calculations(db)


@router.get(
    "/{calc_id}",
    response_model=schemas.CalculationRead,
)
def read_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
):
    """
    Read: GET /calculations/{id}
    """
    calc = crud_calculations.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )
    return calc


@router.patch(
    "/{calc_id}",
    response_model=schemas.CalculationRead,
)
@router.put(
    "/{calc_id}",
    response_model=schemas.CalculationRead,
)
def edit_calculation(
    calc_id: int,
    payload: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    """
    Edit: PATCH/PUT /calculations/{id}
    """
    try:
        calc = crud_calculations.update_calculation(db, calc_id, payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    if not calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )

    return calc


@router.delete(
    "/{calc_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete: DELETE /calculations/{id}
    """
    success = crud_calculations.delete_calculation(db, calc_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found",
        )
    return None