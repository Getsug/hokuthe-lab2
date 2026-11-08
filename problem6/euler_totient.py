"""Euler's totient function computed with the iterative gcd from Problem 5."""

import sys
from pathlib import Path

_PROBLEM5_DIR = Path(__file__).resolve().parent.parent / "problem5"
sys.path.insert(0, str(_PROBLEM5_DIR))
from gcd_iterative import gcd  # noqa: E402


def euler_totient(n: int) -> int:
    """Return phi(n): the count of integers in 1..n-1 coprime to n (phi(1) = 1).

    Args:
        n: A positive integer (bool is rejected).

    Returns:
        The number of integers i with 1 <= i < n and gcd(i, n) == 1;
        1 when n == 1 (standard convention).

    Raises:
        TypeError: If n is not an int (including bool, float, str, None, ...).
        ValueError: If n < 1.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(
            f"euler_totient() argument must be int, got {type(n).__name__}"
        )
    if n < 1:
        raise ValueError(
            f"euler_totient() argument must be a positive integer, got {n}"
        )
    if n == 1:
        return 1
    count = 0
    for i in range(1, n):
        if gcd(i, n) == 1:
            count += 1
    return count


if __name__ == "__main__":
    import math
    from decimal import Decimal
    from fractions import Fraction

    total = 0
    passed = 0

    def report(label, expected_text, ok):
        global total, passed
        total += 1
        passed += bool(ok)
        print(f"{label} (expected {expected_text}) {'PASS' if ok else 'FAIL'}")

    def raises(exc_type, arg):
        try:
            euler_totient(arg)
        except exc_type:
            return True
        except Exception:
            return False
        return False

    # Value tests (known totient values).
    value_cases = [
        (1, 1), (2, 1), (3, 2), (4, 2), (5, 4), (6, 2),
        (10, 4), (12, 4), (13, 12), (15, 8), (36, 12), (100, 40),
    ]
    for n, expected in value_cases:
        try:
            result = euler_totient(n)
        except Exception as exc:
            result = f"{type(exc).__name__}"
        report(f"euler_totient({n}) = {result}", expected, result == expected)

    # ValueError for non-positive integers.
    for n in (0, -1, -5):
        report(f"euler_totient({n}) raises ValueError", "ValueError",
               raises(ValueError, n))

    # TypeError for non-int inputs.
    for bad in (5.5, 5.0, True, None, "5", Decimal(5), Fraction(5)):
        report(f"euler_totient({bad!r}) raises TypeError", "TypeError",
               raises(TypeError, bad))

    # phi(p) = p - 1 for primes.
    for p in (3, 5, 13):
        try:
            result = euler_totient(p)
        except Exception as exc:
            result = type(exc).__name__
        report(f"euler_totient({p}) = {result} (p - 1)", p - 1, result == p - 1)

    # Multiplicativity for coprime m, n (hand-verified values).
    for m, k, expected in ((3, 4, 4), (5, 6, 8), (4, 25, 40)):
        try:
            lhs = euler_totient(m * k)
            rhs = euler_totient(m) * euler_totient(k)
            ok = math.gcd(m, k) == 1 and lhs == rhs == expected
        except Exception:
            lhs, rhs, ok = "error", "error", False
        report(f"euler_totient({m}*{k}) = {lhs}, "
               f"euler_totient({m})*euler_totient({k}) = {rhs}",
               expected, ok)

    # Prime powers: phi(p^k) = p^k - p^(k-1).
    for p, e in ((2, 2), (2, 3), (3, 2), (5, 2), (3, 3)):
        n = p ** e
        formula = p ** e - p ** (e - 1)
        try:
            result = euler_totient(n)
        except Exception as exc:
            result = type(exc).__name__
        report(f"euler_totient({p}^{e}) = {result}", formula,
               result == formula)

    # Independent cross-check against a math.gcd reference, n = 1..200.
    def reference(n):
        if n == 1:
            return 1
        return sum(1 for i in range(1, n) if math.gcd(i, n) == 1)

    try:
        ok = all(euler_totient(n) == reference(n) for n in range(1, 201))
    except Exception:
        ok = False
    report("euler_totient(n) matches math.gcd reference for n = 1..200",
           "all equal", ok)

    print(f"{passed}/{total} passed")
    sys.exit(0 if passed == total else 1)
