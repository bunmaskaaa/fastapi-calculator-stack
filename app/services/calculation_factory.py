from app.schemas.calculation import CalculationType


class Operation:
    def compute(self, a: float, b: float) -> float:
        raise NotImplementedError


class Add(Operation):
    def compute(self, a, b):
        return a + b


class Sub(Operation):
    def compute(self, a, b):
        return a - b


class Multiply(Operation):
    def compute(self, a, b):
        return a * b


class Divide(Operation):
    def compute(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b


def get_operation(calc_type: CalculationType) -> Operation:
    mapping = {
        CalculationType.add: Add(),
        CalculationType.sub: Sub(),
        CalculationType.multiply: Multiply(),
        CalculationType.divide: Divide(),
    }
    return mapping[calc_type]