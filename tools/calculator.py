import operator

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

def calculate(a: float, b: float, operation: str) -> float:
    print(f"[TOOL] calculate({a}, {b}, '{operation}')")
    
    # Check if the operation is valid
    if operation not in OPERATORS:
        raise ValueError(f"Unsupported operation: '{operation}'")
        
    # Look up the operator function and call it with a and b
    return OPERATORS[operation](a, b)
