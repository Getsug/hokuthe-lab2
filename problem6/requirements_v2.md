### Overview
This is a Python program that computes Euler's totient function, denoted by $\phi(n)$. For a positive integer $n$, $\phi(n)$ is the number of positive integers strictly less than $n$ that are relatively prime to $n$. Two integers are relatively prime if their greatest common divisor (GCD) is 1.

For $n = 1$ there are no positive integers less than $n$, so the definition above would give 0. By the standard convention, $\phi(1) = 1$. This case is handled separately and explicitly.

The program reuses the non-recursive `gcd(a, b)` function developed in Problem 5, without modifying or reimplementing it. For a given positive integer $n \ge 2$, the program iterates through all integers from $1$ to $n-1$, computes the GCD of each integer with $n$, and increments a counter whenever the GCD equals 1. The final count is returned as $\phi(n)$. The function rejects invalid inputs (non-integers and integers less than 1).

To ensure correctness, the implementation is tested against known totient values and mathematical properties: $\phi(p) = p - 1$ for prime $p$, multiplicativity for coprime arguments, and the prime-power formula. The function uses an iterative approach without recursion and remains independently importable for reuse.

### Project Requirements
1. The project is housed in a folder called **problem6**.
2. Use **Python 3.14.7** as the intended development environment. The exact version is not enforced at runtime. The README must document the Python version actually used during testing.
3. The project must have a **README** file (see Requirement 20).
4. The project must **reuse the non-recursive `gcd` function from `problem5/gcd_iterative.py` unchanged**. Do not reimplement, edit or copy the gcd logic. Import it by resolving the path to `problem5/gcd_iterative.py` relative to `__file__` (for example, by adding that directory to `sys.path`), so the program works whether it is launched from the repository root or from inside `problem6/`. Importing the GCD module must not execute its `__main__` test block or produce any output.
5. The program has a single primary function with the signature **`def euler_totient(n: int) -> int:`**. It returns $\phi(n)$, the number of integers in $\{1, 2, \ldots, n-1\}$ that are coprime to $n$ (with $\phi(1) = 1$ by convention). The function must have a concise docstring describing the argument, the return value and the possible exceptions.
6. The function takes a single positive integer `n`.
    a. Any input that is not an `int` must raise a `TypeError` with a clear, descriptive message that identifies the invalid type. This includes `bool` (consistent with Problem 5), `float` (including integer-valued floats such as `5.0`), `str`, `None`, `decimal.Decimal`, `fractions.Fraction` and unsupported third-party numeric types. No implicit conversions are performed.
    b. If `n < 1`, the function must raise a `ValueError` with a clear, descriptive message that identifies the invalid value (the totient is defined only for positive integers).
    c. Tests verify the exception type only, not the exact message.
7. The function must implement the following procedure exactly as written and in the order written:
    a. If `n` is not an `int` (or is a `bool`), raise `TypeError`.
    b. If `n < 1`, raise `ValueError`.
    c. If `n == 1`, return `1`.
    d. Initialize `count = 0`.
    e. For each `i` from 1 to `n-1` inclusive:
       i. If `gcd(i, n) == 1`, increment `count` by 1.
    f. Return `count`.
8. The function must call the imported non-recursive `gcd` for every coprimality test. The production `euler_totient` function must **not** use `math.gcd`, must **not** use a factorization shortcut and must **not** reimplement gcd inline. `math.gcd` may be used only in independent verification code inside the test (`__main__`) section.
9. Use the standard library only (plus the imported `gcd`).
10. Do not use recursion.
11. The function must be mathematically correct for all positive integers `n`, including `n = 1`. This does not imply that very large inputs must complete quickly. No maximum input value or timeout is imposed.
12. The deliverable Python file must be named **`euler_totient.py`** and must contain `euler_totient(n)`.
13. Add an `if __name__ == "__main__":` block that runs the test cases below. For each test it prints one line in the format `euler_totient(12) = 4 (expected 4) PASS` (or `FAIL`). The block ends with a summary line giving the number of tests passed and the number of tests executed (for example, `32/32 passed`). The script exits with a nonzero status if any test fails and with status 0 otherwise. The output is captured to **`Results/totient_output.txt`** using terminal redirection.
    Value tests (all known totient values):
    - `euler_totient(1)` → `1`
    - `euler_totient(2)` → `1`
    - `euler_totient(3)` → `2`
    - `euler_totient(4)` → `2`
    - `euler_totient(5)` → `4`
    - `euler_totient(6)` → `2`
    - `euler_totient(10)` → `4`
    - `euler_totient(12)` → `4`
    - `euler_totient(13)` → `12` (prime, so $p - 1$)
    - `euler_totient(15)` → `8`
    - `euler_totient(36)` → `12`
    - `euler_totient(100)` → `40`
14. The `__main__` block must also run the following checks, each printing one `PASS` or `FAIL` line in the same style (a check that expects an exception prints, for example, `euler_totient(0) raises ValueError (expected ValueError) PASS`). Each check counts toward the summary. The `euler_totient(12)` case is not repeated as a separate test.
    a. **ValueError** is raised for `0`, `-1` and `-5`.
    b. **TypeError** is raised for `5.5`, `5.0`, `True`, `None`, `"5"`, `Decimal(5)` and `Fraction(5)`.
    c. **Prime property** $\phi(p) = p - 1$ holds for the prime inputs `3`, `5` and `13`, reusing the value tests above.
    d. **Multiplicativity** $\phi(mn) = \phi(m)\,\phi(n)$ holds for coprime pairs, using small hand-verified values: $(3, 4)$ giving $\phi(12) = 4$, $(5, 6)$ giving $\phi(30) = 8$ and $(4, 25)$ giving $\phi(100) = 40$.
    e. **Prime powers** $\phi(p^k) = p^k - p^{k-1}$ hold for small hand-verified values: $\phi(4) = 2$, $\phi(8) = 4$, $\phi(9) = 6$, $\phi(25) = 20$ and $\phi(27) = 18$.
    f. Independent verification code in the test section may use `math.gcd` to cross-check results. The production function may not.
15. Executing all of the listed test cases in under two seconds is a desirable goal (the largest input is `n = 100`), not a strict correctness requirement. It does not apply to much larger inputs.
16. The `euler_totient(n)` function must remain independently importable so that it can be reused without modifying or duplicating its implementation. Importing `euler_totient.py` must not run the tests or produce output.
17. **Complexity.** The direct algorithm performs $n - 1$ GCD computations, each taking $O(\log n)$ arithmetic operations, so the total is approximately $O(n \log n)$ in the worst case. This must be documented in the README (and may be summarized in the docstring). No factorization-based shortcut is introduced.
18. **Large inputs.** The README must state that the direct GCD-based algorithm becomes impractical for very large `n` and that large inputs may require substantial execution time.
19. **Results directory.** `problem6/Results/` must exist before the output is redirected (shell redirection does not create directories). The README documents the commands to create the directory and generate the file, for example (from the repository root):
    - PowerShell: `New-Item -ItemType Directory -Force problem6/Results; python problem6/euler_totient.py > problem6/Results/totient_output.txt`
    - POSIX shell: `mkdir -p problem6/Results && python problem6/euler_totient.py > problem6/Results/totient_output.txt`
20. **README contents.** The README must include:
    a. the problem objective;
    b. the mathematical explanation (definition, the $\phi(1) = 1$ convention, and the properties tested);
    c. the algorithm;
    d. the dependency on Problem 5;
    e. execution instructions;
    f. the testing procedure;
    g. how to generate the results file (see Requirement 19);
    h. performance limitations (see Requirements 17 and 18);
    i. the Python version actually used during testing.
21. **Testing approach.** Keep the tests in the `__main__` block of `euler_totient.py`. Do not introduce a separate testing framework unless a genuine need arises.
22. **Documents.** `requirements_v2.md` is prepared first. After it is approved, `design.md` is prepared. The user's questions and the responses to them are recorded in `interrogation.md`.
