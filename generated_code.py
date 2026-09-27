def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Simple tests
if __name__ == "__main__":
    test_numbers = [0, 1, 2, 3, 4, 5, 16, 17, 19, 20, 23, 24, 29, 31, 97, 100]
    for num in test_numbers:
        print(f"{num}: {'Prime' if is_prime(num) else 'Not prime'}")