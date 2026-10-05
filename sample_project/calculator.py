def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference between two numbers."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """Return the result of dividing a by b.

    Raises:
        ValueError: If the denominator is zero.
        TypeError: If the inputs are not numbers.
    """
    if not isinstance(a, (int, float)):
        raise TypeError("Numerator must be a number.")
    if not isinstance(b, (int, float)):
        raise TypeError("Denominator must be a number.")
    if b == 0:
        raise ValueError("Denominator cannot be zero.")
    return a / b
