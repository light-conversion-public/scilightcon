from typing import List

def add(a, b) -> float:
    """Compute and return the sum of two numbers.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        a (float): A number representing the first addend in the addition.
        b (float): A number representing the second addend in the addition.

    Returns:
        A number representing the arithmetic sum of `a` and `b`.
    """
    return float(a + b)


def substract(a, b) -> float:
    """Compute and return the difference between two numbers.

    Examples:
        >>> substract(4.0, 2.0)
        2.0
        >>> substract(4, 2)
        2.0

    Args:
        a (float): A number representing the first addend in the substraction.
        b (float): A number representing the second addend in the substraction.

    Returns:
        A number representing the arithmetic sum of `a` and `b`.
    """
    return float(a - b)


def multiply(a, b) -> float:
    """Multiplies two numbers.

    Examples:
        >>> multiply(4.0, 2.0)
        8.0

    Args:
        a (float): A number representing the first number.
        b (float): A number representing the second number.

    Returns:
        A number representing the product of `a` and `b`.
    """
    return float(a * b)