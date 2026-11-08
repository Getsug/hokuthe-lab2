# Problem 2: `is_prime`

A simple Python program that decides whether an integer is prime, using descending $6k\pm1$ trial division up to $\lfloor\sqrt n\rfloor$. Standard library only, no recursion.

Tested with **Python 3.14.7** (Windows 11). The code does not enforce a specific version.

## Files

| File | Purpose |
|---|---|
| `primality.py` | The implementation: `is_prime(n)`, plus a `__main__` self-check |
| `test_primality.py` | Correctness tests against an independent trial-division reference |
| `verify_expected.py` | Independent verification of the expected test values |
| `benchmark.py` | Timing of large inputs |
| `Results/` | Captured output: `test_output.txt`, `test_primality_output.txt`, `verify_expected_output.txt`, `timing.txt` |
| `requirements_v2.md`, `design_v1.md` | Approved requirements and design |

## Algorithm

1. If `n <= 1`, return `False`.
2. If `n` is 2 or 3, return `True`.
3. If `n` is divisible by 2 or 3, return `False`.
4. Let `L = math.isqrt(n)`.
5. Let `k = (L + 1) // 6`. For each `k` descending to 1, test `6k+1` first and then `6k-1`, skipping any candidate greater than `L`. If a candidate divides `n`, return `False`.
6. Otherwise return `True`.

Why it works:
- **Square-root bound.** A composite `n` has a prime factor `p` with `p*p <= n`, so only divisors up to `L` need testing.
- **6k±1.** Every prime greater than 3 has the form `6k±1` (Problem 1), so after removing multiples of 2 and 3 only these candidates are needed. Not every number of that form is prime (25, 49 and 91 are composite), which is why the candidates are still tested as divisors.
- The smallest prime factor of a composite `n` is always among the candidates tested, so no composite is missed. See `interrogation.md` for the proof.

`is_prime` raises `TypeError` for anything that is not an `int` (including `bool`, `float` such as `7.0`, `str`, `None`). Subclasses of `int` are accepted. There is no implicit conversion.

## Usage

```python
from primality import is_prime

is_prime(7919)   # True
is_prime(91)     # False
is_prime(-7)     # False
is_prime(True)   # raises TypeError
```

`primality.py` has no side effects on import. Later problems should import this same file and must not copy the code.

## Running (from the repository root, in Git Bash or cmd)

```
python problem2/primality.py        > problem2/Results/test_output.txt
python problem2/verify_expected.py  > problem2/Results/verify_expected_output.txt
python problem2/test_primality.py   > problem2/Results/test_primality_output.txt
python problem2/benchmark.py        > problem2/Results/timing.txt
```

Create `problem2/Results/` first. Do not use PowerShell 5.1 for the redirection: it writes UTF-16.

Each script exits with a nonzero status on any failure (`benchmark.py` exits nonzero if a result is wrong).

## Verification

- `primality.py` (`__main__`): runs `is_prime` on 32 cases against a hard-coded `EXPECTED` table and prints `n, result, PASS/FAIL`.
- `test_primality.py`: compares `is_prime` with a plain trial-division reference for every integer 0 to 10,000, perfect-square boundaries (121, 169, 289, 361, 10201, 999983² and neighbours), loop-boundary cases, large inputs, type errors and negatives. Latest run: 10144 tests, 10144 passed, 0 failed.
- `verify_expected.py`: establishes the expected values **without calling `is_prime`**. It reads the `EXPECTED` table from `primality.py` by parsing it with `ast` (nothing is executed), and checks each value, plus the large benchmark inputs, with two methods that must agree: (A) exhaustive trial division, printing factorisations, and (B) deterministic Miller–Rabin with the first 12 primes as bases (valid for n < 3.3 × 10²⁴). Latest run: 34 values, 0 mismatches.

Limitations of the verification: both methods are this project's own code, so agreement is strong evidence and not formal proof; only the listed values are verified, and it does not prove `is_prime` correct for all `n`; the `ast` extraction fails loudly if `EXPECTED` stops being a plain literal.

## Performance

Median of 5 runs, from `Results/timing.txt` (`time.perf_counter()`):

| n | Case | Median |
|---|---|---|
| 999999999989 | large prime | about 22 ms |
| 999999999745 = 5 × 199999999949 | composite whose smallest factor is 5 | about 22 ms |
| 999966000289 = 999983² | prime square | about 0.001 ms |
| 1000000000000 | even, exits at step d | under 0.001 ms |

Limitations:
- **Descending order trade-off.** The assignment requires testing divisors from the top down. Composites with a large factor close to √n (such as 999983²) are rejected almost immediately. Composites whose smallest factor is small but at least 5 (such as 5 × a large prime) are only caught at the very end, so they cost about as much as a prime of similar size. Ascending order would reject those quickly.
- **No upper bound, but the cost grows as √n.** Around 10¹² takes tens of milliseconds. Each factor of 100 in `n` multiplies the worst-case time by about 10, so inputs far beyond about 10¹⁴ to 10¹⁶ become impractically slow for trial division.
