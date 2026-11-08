"""Primality test using descending 6k +/- 1 trial division up to isqrt(n)."""

import math


def is_prime(n: int) -> bool:
    """Return True if n is prime, False otherwise.

    Raises TypeError unless n is an int (bool is rejected; int subclasses are
    accepted). Divisors of the form 6k+1 and 6k-1 are tested in descending
    order from the largest candidate not exceeding isqrt(n) down to 5.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"is_prime() requires an int, got {type(n).__name__}")

    # a. receive n
    # b.
    if n <= 1:
        return False
    # c.
    if n == 2 or n == 3:
        return True
    # d.
    if n % 2 == 0 or n % 3 == 0:
        return False
    # e.
    limit = math.isqrt(n)
    # f.
    for k in range((limit + 1) // 6, 0, -1):
        for candidate in (6 * k + 1, 6 * k - 1):
            if candidate > limit:
                continue
            # g.
            if n % candidate == 0:
                return False
    # h.
    return True


if __name__ == "__main__":
    import sys

    # Plain literal of (n, expected) pairs; verified independently by
    # verify_expected.py. Do not compute these with is_prime().
    EXPECTED = [
        (-7, False), (0, False), (1, False), (2, True), (3, True),
        (4, False), (5, True), (6, False), (7, True), (9, False),
        (11, True), (25, False), (49, False), (91, False), (97, True),
        (121, False), (143, False), (7917, False), (7919, True),
        (10201, False), (999983, True), (1000000000000, False),
        (-1, False), (-2, False), (-3, False), (-4, False), (-25, False),
        (35, False),
        (169, False), (289, False), (361, False), (999966000289, False),
    ]

    failures = 0
    for n, expected in EXPECTED:
        result = is_prime(n)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"{n}, {result}, {status}")
    if failures:
        sys.exit(1)
