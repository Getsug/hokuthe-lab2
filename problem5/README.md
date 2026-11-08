# Problem 5: Iterative Euclidean GCD

## Objective
Compute the greatest common divisor (GCD) of two integers with the Euclidean algorithm, using a `while` loop and **no recursion**. The function handles positive, negative and zero inputs, and integers of any size.

## The Euclidean algorithm
The algorithm rests on the property

$$gcd(a, b) = gcd(b, a \bmod b)$$

Writing `a = q*b + r` with `0 <= r < b`, the pairs `(a, b)` and `(b, r)` have exactly the same common divisors: anything dividing `a` and `b` divides `r = a - q*b`, and anything dividing `b` and `r` divides `a = q*b + r`. Equal sets of common divisors have the same greatest element.

The implementation:

1. Replace `a` and `b` with their absolute values (the divisors of `n` and `-n` are the same).
2. While `b != 0`: set `(a, b) = (b, a % b)`.
3. When `b == 0`, return `a`.

Notes:
- `a >= b` is not required. If `a < b`, the first iteration swaps them, because `a % b == a`.
- `gcd(0, 0)` returns `0`, since the loop never runs.
- The loop terminates because `b` strictly decreases (`0 <= a % b < b`) and stays non-negative.
- For nonzero inputs it takes O(log(min(|a|, |b|))) iterations and O(1) extra memory. If an input is zero, the loop runs at most once.

A longer walkthrough with the proof and a worked example is in [interrogation.md](interrogation.md).

## Function interface
File: `gcd_iterative.py`

```python
def gcd(a: int, b: int) -> int
```

- **Inputs:** `a`, `b`: Python integers (positive, negative or zero).
- **Returns:** the non-negative GCD.
- **Raises:** `TypeError` if either argument is not an `int`. This includes `float`, `str`, `None` and `bool`. The check happens before the algorithm runs.

`gcd` is the only public function. It needs no imports and importing the module prints nothing.

## Python version
Developed and tested with **Python 3.14.7**. The version is not enforced at runtime; the code uses only features available in far older Python 3 versions.

## How to run
The program uses only the standard library.

From the repository root:

```
python problem5/gcd_iterative.py
```

From inside the `problem5` directory:

```
python gcd_iterative.py
```

The script prints one line per test and a final summary, for example `19/19 passed`. It exits with status 0 if every test passes and a nonzero status otherwise.

## Test cases
The `__main__` block of `gcd_iterative.py` runs 19 tests.

GCD tests: each must equal both the hardcoded expected value and `math.gcd(a, b)`.

| # | Call | Expected | Category |
|---|------|----------|----------|
| 1 | `gcd(12, 8)` | 4 | basic |
| 2 | `gcd(17, 5)` | 1 | relatively prime |
| 3 | `gcd(25, 25)` | 25 | equal inputs |
| 4 | `gcd(270, 192)` | 6 | basic |
| 5 | `gcd(0, 7)` | 7 | zero input |
| 6 | `gcd(7, 0)` | 7 | zero input |
| 7 | `gcd(0, 0)` | 0 | zero input |
| 8 | `gcd(-12, 8)` | 4 | negative |
| 9 | `gcd(12, -8)` | 4 | negative |
| 10 | `gcd(-12, -8)` | 4 | negative |
| 11 | `gcd(1_000_000_007, 998_244_353)` | 1 | large primes |
| 12 | `gcd(1, 987654321)` | 1 | `gcd(1, n)` |
| 13 | `gcd(100, 25)` | 25 | one input a multiple of the other |
| 14 | `gcd(832040, 514229)` | 1 | consecutive Fibonacci numbers |
| 15 | `gcd(2**100, 3 * 2**70)` | `2**70` | larger than 64 bits |

`TypeError` tests: each passes only if the call raises `TypeError`.

| # | Call |
|---|------|
| 16 | `gcd(1.5, 2)` |
| 17 | `gcd("a", 2)` |
| 18 | `gcd(None, 2)` |
| 19 | `gcd(True, 2)` |

## Generating `Results/gcd_output.txt`
The `Results` directory must exist before redirecting output. Create it if needed:

- PowerShell: `New-Item -ItemType Directory -Force problem5/Results`
- cmd / POSIX shells: `mkdir problem5/Results`

The output is ASCII-only. Windows PowerShell 5.1 writes UTF-16 with a plain `>`, so set the encoding explicitly there.

From the repository root:

- cmd / POSIX shells:
  ```
  python problem5/gcd_iterative.py > problem5/Results/gcd_output.txt
  ```
- PowerShell:
  ```
  python problem5/gcd_iterative.py | Out-File -Encoding ascii problem5/Results/gcd_output.txt
  ```

From inside `problem5`, use `gcd_iterative.py` and `Results/gcd_output.txt` as the paths.

The committed `Results/gcd_output.txt` shows 19 PASS lines followed by `19/19 passed`.

## Reuse in Problem 6
`gcd` can be imported without modifying or copying it:

```python
from gcd_iterative import gcd

print(gcd(48, 18))  # 6
```

Run Python from the `problem5` directory, or add that directory to `sys.path`, so the import resolves.
