import operator


OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def calculate(a: float, b: float, operation: str) -> float:

    if operation not in OPERATORS:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    if operation == "/" and b == 0:
        raise ValueError("Cannot divide by zero.")

    return OPERATORS[operation](a, b)