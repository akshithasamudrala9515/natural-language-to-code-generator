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


def average(numbers):
    """Return the arithmetic mean of a sequence of numbers.

    Args:
        numbers (iterable): An iterable containing numeric values.

    Returns:
        float: The average of the provided numbers.

    Raises:
        TypeError: If `numbers` is not iterable or contains non‑numeric elements.
        ValueError: If the iterable is empty.
    """
    # Ensure the input is iterable
    try:
        iterator = iter(numbers)
    except TypeError:
        raise TypeError("Input must be an iterable of numbers.")

    total = 0
    count = 0
    for n in iterator:
        if not isinstance(n, (int, float)):
            raise TypeError("All elements must be numbers.")
        total += n
        count += 1

    if count == 0:
        raise ValueError("Cannot compute average of an empty sequence.")

    return total / count
