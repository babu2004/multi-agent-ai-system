import operator


OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def calculate(a: float, b: float, operation: str) -> float:
    print(f"[TOOL] calculate({a}, {b}, '{operation}')")
    raise ValueError("TEST TOOL FAILURE")