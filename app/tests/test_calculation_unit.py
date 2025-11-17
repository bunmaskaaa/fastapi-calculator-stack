import pytest

from app.schemas.calculation import CalculationCreate, CalculationType
from app.services.calculation_factory import get_operation


def test_factory_operations():
    assert get_operation(CalculationType.add).compute(2, 3) == 5
    assert get_operation(CalculationType.sub).compute(5, 3) == 2
    assert get_operation(CalculationType.multiply).compute(4, 3) == 12
    assert get_operation(CalculationType.divide).compute(9, 3) == 3


def test_divide_by_zero_in_schema():
    with pytest.raises(ValueError):
        CalculationCreate(a=10, b=0, type=CalculationType.divide)