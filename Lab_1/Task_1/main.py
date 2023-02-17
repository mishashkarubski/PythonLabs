from typing import Union, Literal, Optional


# Type aliases for math function
Operation = Literal["add", "sub", "mult", "div"]
Number = Union[int, float, complex]


def main():
    """
    Prints "Hello, World!".
    Creates a function that returns the result of a mathematical operation.
    Creates list of numbers and returns list of even numbers in this list.
    """
    print("Hello, World!")

    def mathfunc(x: Number, y: Number, func: Operation) -> Optional[Number]:
        """Performs math operations on two numbers."""
        try:
            result = eval(f"x.__{func[:3] if func != 'div' else 'truediv'}__(y)")
        except (AttributeError, TypeError):
            result = None

        return result


if __name__ == "__main__":
    main()
