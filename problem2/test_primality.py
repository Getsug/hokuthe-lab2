"""Deterministic correctness tests for primality.is_prime.

Compares is_prime against an independent trial-division reference. Plain
standard-library script: prints tests run / passed / failed and exits with a
nonzero status if any test fails.
"""

import sys
from fractions import Fraction

from primality import is_prime

run = 0
failures = []


def reference_is_prime(n):
    """Independent, straightforward trial division (no 6k+-1 logic)."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def check(label, actual, expected):
    global run
    run += 1
    if actual != expected:
        failures.append(f"{label}: expected {expected!r}, got {actual!r}")


def check_against_reference(n):
    check(f"is_prime({n})", is_prime(n), reference_is_prime(n))


def check_raises_type_error(value):
    global run
    run += 1
    try:
        is_prime(value)
    except TypeError:
        return
    except Exception as exc:  # wrong exception type
        failures.append(f"is_prime({value!r}): raised {type(exc).__name__}, expected TypeError")
        return
    failures.append(f"is_prime({value!r}): no TypeError raised")


class MyInt(int):
    pass


# 1. Exhaustive small range
for n in range(0, 10001):
    check_against_reference(n)

# 2. Perfect-square boundaries (squares and their neighbours)
for n in (121, 169, 289, 361, 10201, 999983 ** 2):
    for m in (n - 1, n, n + 1):
        check_against_reference(m)

# 3. Loop-boundary cases: k = 1, and L + 1 a multiple of 6 (n = 25, 35, 49, ...)
for n in (5, 7, 25, 35, 49, 143, 169, 5 * 5, 11 * 13, 7 * 11):
    check_against_reference(n)
for L in range(5, 200, 6):  # L + 1 is a multiple of 6
    for n in (L * L, L * L + 2, L * L + 4):
        check_against_reference(n)

# 4. Large inputs
for n in (999999999989, 999966000289, 999999999745, 1000000000000):
    check_against_reference(n)

# 5. Type handling
for bad in (True, False, 7.0, "7", None, Fraction(7, 1)):
    check_raises_type_error(bad)
check("is_prime(MyInt(7))", is_prime(MyInt(7)), True)
check("is_prime(MyInt(9))", is_prime(MyInt(9)), False)

# 6. Negatives and zero
for n in (-7, -1, 0, 1):
    check(f"is_prime({n})", is_prime(n), False)

print(f"Tests run: {run}")
print(f"Passed:    {run - len(failures)}")
print(f"Failed:    {len(failures)}")
for line in failures:
    print(f"FAIL {line}")
sys.exit(1 if failures else 0)
