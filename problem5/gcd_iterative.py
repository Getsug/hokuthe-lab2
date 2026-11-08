def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of two integers.

    Uses the iterative Euclidean algorithm (no recursion). The result is
    always non-negative, and gcd(0, 0) is 0.

    Args:
        a: An integer (positive, negative or zero).
        b: An integer (positive, negative or zero).

    Returns:
        The non-negative greatest common divisor of a and b.

    Raises:
        TypeError: If a or b is not an int (bool is rejected as well).
    """
    for value in (a, b):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(
                f"gcd() arguments must be int, got {type(value).__name__}"
            )

    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a


if __name__ == "__main__":
    import math
    import sys

    gcd_cases = [
        (12, 8, 4),
        (17, 5, 1),
        (25, 25, 25),
        (270, 192, 6),
        (0, 7, 7),
        (7, 0, 7),
        (0, 0, 0),
        (-12, 8, 4),
        (12, -8, 4),
        (-12, -8, 4),
        (1_000_000_007, 998_244_353, 1),
        (1, 987654321, 1),
        (100, 25, 25),
        (832040, 514229, 1),
        (2**100, 3 * 2**70, 2**70),
    ]
    type_cases = [(1.5, 2), ("a", 2), (None, 2), (True, 2)]

    passed = 0
    total = 0

    for a, b, expected in gcd_cases:
        result = gcd(a, b)
        ok = result == expected and result == math.gcd(a, b)
        print(f"gcd({a}, {b}) = {result} (expected {expected}) "
              f"{'PASS' if ok else 'FAIL'}")
        total += 1
        passed += ok

    for a, b in type_cases:
        try:
            gcd(a, b)
            ok = False
        except TypeError:
            ok = True
        print(f"gcd({a!r}, {b!r}) raises TypeError (expected TypeError) "
              f"{'PASS' if ok else 'FAIL'}")
        total += 1
        passed += ok

    print(f"{passed}/{total} passed")
    sys.exit(0 if passed == total else 1)
