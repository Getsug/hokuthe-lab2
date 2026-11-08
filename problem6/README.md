# Problem 6: Euler's Totient Function

## Objective

Implement `euler_totient(n)`, which returns Euler's totient $\phi(n)$, by reusing the non-recursive `gcd` function from Problem 5 (`problem5/gcd_iterative.py`), unchanged.

## Mathematical background

For a positive integer $n$, $\phi(n)$ is the number of positive integers strictly less than $n$ that are relatively prime to $n$ (that is, $\gcd(i, n) = 1$).

- **Convention:** for $n = 1$ there are no integers less than $n$, so the definition would give 0. By the standard convention $\phi(1) = 1$, and the function handles this case separately.
- **Primes:** $\phi(p) = p - 1$.
- **Multiplicativity:** $\phi(mn) = \phi(m)\,\phi(n)$ when $\gcd(m, n) = 1$.
- **Prime powers:** $\phi(p^k) = p^k - p^{k-1}$.

Example: $\phi(12) = 4$, because 1, 5, 7 and 11 are the integers below 12 coprime to 12.

## Algorithm

1. If `n` is not an `int` (a `bool` is rejected too), raise `TypeError`.
2. If `n < 1`, raise `ValueError`.
3. If `n == 1`, return `1`.
4. Set `count = 0`.
5. For each `i` from 1 to `n-1`: if `gcd(i, n) == 1`, add 1 to `count`.
6. Return `count`.

The function is iterative (no recursion), uses only the standard library plus the imported `gcd`, and does not use `math.gcd` or any factorization shortcut. Floats (including `5.0`), strings, `None`, `Decimal`, `Fraction` and similar types are rejected with `TypeError`; no conversions are performed.

## Dependency on Problem 5

`euler_totient.py` locates `problem5/gcd_iterative.py` relative to its own `__file__` and adds that folder to `sys.path`, so it works when launched from the repository root, from inside `problem6/`, or from any other directory. The Problem 5 file is not modified or copied. Importing it runs no tests and prints nothing.

## Running

From the repository root:

```
python problem6/euler_totient.py
```

or from inside `problem6/`:

```
python euler_totient.py
```

To reuse the function:

```python
from euler_totient import euler_totient
euler_totient(12)  # 4
```

## Testing

The tests are in the `__main__` block of `euler_totient.py` (no test framework). Each check prints one line such as `euler_totient(12) = 4 (expected 4) PASS`, followed by a summary like `34/34 passed`. The exit status is nonzero if any check fails.

The 34 checks are:

- 12 known totient values (n = 1, 2, 3, 4, 5, 6, 10, 12, 13, 15, 36, 100)
- `ValueError` for 0, -1 and -5
- `TypeError` for 5.5, 5.0, True, None, "5", `Decimal(5)` and `Fraction(5)`
- $\phi(p) = p - 1$ for p = 3, 5 and 13
- multiplicativity for (3, 4), (5, 6) and (4, 25)
- prime powers 4, 8, 9, 25 and 27
- a cross-check for n = 1..200 against a reference that uses `math.gcd` (used in test code only)

Tests verify the exception type, not the message.

## Generating the results file

The `Results` folder must exist before redirecting output. From the repository root:

PowerShell:

```
New-Item -ItemType Directory -Force problem6/Results
python problem6/euler_totient.py > problem6/Results/totient_output.txt
```

POSIX shell:

```
mkdir -p problem6/Results && python problem6/euler_totient.py > problem6/Results/totient_output.txt
```

## Performance and limitations

The function makes $n - 1$ gcd calls, each taking $O(\log n)$ arithmetic operations, so it is approximately $O(n \log n)$ in the worst case. All the listed tests (the largest is `n = 100`) run in well under two seconds, which is a goal, not a correctness requirement. The function is correct for every positive integer, but the direct algorithm becomes impractical for very large `n` and may take a very long time. There is no maximum input value or timeout.

## Environment

Intended development environment: Python 3.14.7. The version is not enforced at runtime. Tested with: Python 3.14.7 (Windows 11).
