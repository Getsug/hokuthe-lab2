"""Independent verification of the expected values used by the tests.

Does NOT import or call is_prime(). It reads the EXPECTED table from
primality.py by parsing the file with ast (nothing is imported or executed),
then checks each value, plus the large benchmark inputs, with two methods:

  A. exhaustive trial division (prints the factorisation of composites)
  B. deterministic Miller-Rabin with the first 12 primes as bases
     (proven deterministic for n < 3.3 * 10**24; asserted below)

Limitations:
  * Both methods are this project's own code. Agreement is strong evidence,
    not formal proof.
  * Only the listed values are verified; this does not prove is_prime correct
    for all n (that is test_primality.py's job).
  * Method A costs O(sqrt(n)); it is only used on the listed values.
  * The ast extraction fails loudly if EXPECTED stops being a plain literal.
"""

import ast
import sys
from pathlib import Path

BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
MR_BOUND = 3_317_044_064_679_887_385_961_981  # ~3.3e24
EXTRA_LARGE = [
    (999999999989, True),
    (999966000289, False),
    (999999999745, False),
    (1000000000000, False),
]


def load_expected():
    source = (Path(__file__).parent / "primality.py").read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "EXPECTED" for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise SystemExit("EXPECTED table not found in primality.py")


def factorise(n):
    """Method A: full factorisation by trial division (n >= 2)."""
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def method_a(n):
    if n < 2:
        return False, []
    factors = factorise(n)
    return len(factors) == 1, factors


def method_b(n):
    """Method B: deterministic Miller-Rabin."""
    if n < 2:
        return False
    assert n < MR_BOUND, "Miller-Rabin bases not proven deterministic here"
    for p in BASES:
        if n == p:
            return True
        if n % p == 0:
            return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in BASES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


table = load_expected()
assert all(
    isinstance(n, int) and not isinstance(n, bool) and isinstance(e, bool)
    for n, e in table
), "EXPECTED must contain only (int, bool) pairs"
cases = list(table) + [c for c in EXTRA_LARGE if c not in table]

mismatches = 0
for n, expected in cases:
    a, factors = method_a(n)
    b = method_b(n)
    ok = a == b == expected
    if not ok:
        mismatches += 1
    detail = " * ".join(map(str, factors)) if factors and not a else ""
    print(f"{n}, expected={expected}, A={a}, B={b}, {'OK' if ok else 'MISMATCH'}"
          + (f"  [{n} = {detail}]" if detail else ""))

print(f"Values checked: {len(cases)}")
print(f"Mismatches:     {mismatches}")
sys.exit(1 if mismatches else 0)
