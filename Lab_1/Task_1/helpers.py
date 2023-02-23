from typing import Literal, Optional, Any


# Type aliases for math function
Operation = Literal["add", "sub", "mult", "div"]


def calculate(x: float, y: float, func: Operation) -> Optional[float]:
    """Performs math operations on two numbers.

    Returns the result of the operation on two numbers, or None
    if either of passed values is not eligible for math operation.
    :argument x any number
    :argument y any number
    :argument func operation to perform
    """

    try:
        result = eval(f"x.__{func[:3] if func != 'div' else 'truediv'}__(y)")
    except (ZeroDivisionError, AttributeError, TypeError):
        result = None

    return result


def filter_even(numbers: list[Any]):
    """Leaves only even values in the list
    :argument numbers list of integers
    """
    return list(filter(lambda x: str(x).isdigit() and int(x) % 2 == 0, numbers))
