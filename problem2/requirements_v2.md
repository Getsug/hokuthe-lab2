### Overview
This is a simple Python program that decides whether a given integer is a prime number or not. The algorithm used exploits two facts:
1. A composite number n must have a factor no larger than $\lfloor\sqrt n\rfloor$, so trial division only needs to reach the square root.
2. From Problem 1, every prime greater than 3 is of the form $6k \pm 1$, so a mod-6 check can identify possible prime candidates with remainder 1 or 5. However, not every number of this form is prime (for example 25, 49 and 91), so these candidates must still be tested for primality.

The function first handles 2 and 3, rejects other even numbers and multiples of 3, then tests eligible divisors of the form $6k\pm1$ in descending order, from the largest candidate not exceeding $\lfloor\sqrt n\rfloor$ down to 5 (the last candidates tested are 7 and 5, for k = 1).

The project is split into four independent files, each with one responsibility:
- `primality.py`: the implementation. Its `__main__` block runs the function on a set of edge cases (including 25, 49 and 91, which survive the $6k \pm 1$ sieve but are composite) and compares each result with a hard-coded expected value. The output is captured in `Results/test_output.txt`.
- `test_primality.py`: deterministic correctness tests comparing `is_prime` with an independent reference implementation. Its output is captured in `Results/test_primality_output.txt`.
- `verify_expected.py`: a reproducible, independent verification of the expected values used by the tests, without using `is_prime`. Its output is captured in `Results/verify_expected_output.txt`.
- `benchmark.py`: performance measurement on representative large inputs, with results saved in `Results/timing.txt`. Correctness testing and performance measurement are kept independent.

The implementation must use only the standard library, avoid recursion, and handle inputs up to at least $10^{12}$ in reasonable time.

### Project Requirements

#### Project structure
1. The project is housed in a folder called `problem2`, containing:
   - `primality.py`: the deliverable implementation
   - `test_primality.py`: deterministic correctness tests against an independent reference
   - `verify_expected.py`: independent verification of the expected test values
   - `benchmark.py`: performance measurements
   - `README.md`
   - `Results/` (containing `test_output.txt`, `test_primality_output.txt`, `verify_expected_output.txt` and `timing.txt`)
2. Python 3.14.7 is the intended development version. The programs must not enforce an exact version at runtime. The Python version actually used for testing must be documented in the README and in the header of `Results/timing.txt`.
3. The project must have a README file (see "README contents" below).

#### Function interface and input handling
4. `is_prime(n)` is called as a function. No command-line or stdin input is required.
   - It accepts Python `int` values, including subclasses of `int`.
   - It must raise `TypeError` with a clear, descriptive message for `bool` values (even though `bool` is an `int` subclass), floats (including `7.0`), strings, `None`, and unsupported third-party numeric types. No implicit conversions are performed.
   - Type validation occurs before the mathematical algorithm (step a below).
   - Valid inputs may be positive, zero or negative. No fixed upper bound is imposed. The README must document that trial division becomes computationally expensive for very large integers.
5. `primality.py` exposes one public function, named `is_prime`. It has type hints (`n: int -> bool`) and a concise docstring. Test and benchmark code must not add further public functions to `primality.py`.
6. `is_prime` returns `True` for prime numbers and `False` for non-prime numbers.
7. The program must implement the algorithm below exactly as written and in the order written (the type check from requirement 4 is a guard that runs before step a):
	*a. Receive an integer n*
	*b. If n is less than or equal to 1, return `False`*
	*c. If n = 2 or n = 3, return `True`*
	*d. If n is divisible by 2 or divisible by 3, return `False`*
	*e. Compute the limit $L=\lfloor\sqrt n\rfloor$. Use `math.isqrt(n)`.*
	*f. Set $k=\lfloor(L+1)/6\rfloor$. For each k descending from this value down to 1, test the candidate $6k+1$ first and then $6k-1$, skipping any candidate greater than L. This walks through every possible prime divisor candidate up to L from the top down, ending with 5.*
	*g. If a candidate divides n, return `False` immediately.*
	*h. If no divisor is found, return `True`.*
8. Use the standard library only:
   - `primality.py` may use `math`, and `sys` for the exit status.
   - `test_primality.py` may additionally use `fractions` (for the type-error cases).
   - `verify_expected.py` may use `ast` (to read the expected table from `primality.py`) and `sys`.
   - `benchmark.py` may use `time`, `statistics`, `platform` and `sys`.
   - No third-party packages are allowed.
9. Do not use recursion.
10. `is_prime` must correctly handle n up to at least $10^{12}$ using the square-root bound and $6k\pm1$ candidate filtering. No strict execution-time threshold is imposed. Elapsed time must be measured and reported for representative large inputs (see "Performance measurement").
11. The deliverable Python file is named `primality.py` and must contain `is_prime(n)`.

#### `__main__` block in `primality.py`
12. `primality.py` contains an `if __name__ == "__main__":` block that:
   - runs `is_prime` on each test case in the table below;
   - compares each result with a hard-coded expected value in a literal table. The table is a single named plain literal of `(n, expected)` pairs (named `EXPECTED`, containing only ints and bools) so that `verify_expected.py` can read it without executing `primality.py`. Expected values must be independently verified by `verify_expected.py` and must not be computed with `is_prime()` or any second primality implementation inside `primality.py`;
   - prints one line per case in the format `n, result, PASS/FAIL` (for example `25, False, PASS`);
   - exits with a nonzero status if any test fails.

   Test cases (all original cases are preserved):

   | Group | Cases |
   |---|---|
   | Original cases | -7, 0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 25, 49, 91, 97, 121, 143, 7917, 7919, 10201, 999983, 1000000000000 |
   | Added negatives | -1, -2, -3, -4, -25 |
   | Added k=1 boundary | 35 (L = 5) (5 and 7 are already in the original cases) |
   | Added perfect-square boundaries | 169, 289, 361, 999983² (= 999966000289) |

   The output is captured to `problem2/Results/test_output.txt` using terminal redirection, run from the repository root in Git Bash or Command Prompt:
   `python problem2/primality.py > problem2/Results/test_output.txt`
   The output must be UTF-8. PowerShell 5.1 redirection (UTF-16) must not be used. The `Results/` directory must exist before the command is run.
13. `is_prime(n)` must remain independently importable (importing `primality` must run no tests and print nothing). Problems 3 and 4 must import this same verified implementation, without modifying it or duplicating its primality logic.

#### Correctness tests (`test_primality.py`)
14. `test_primality.py` is a plain standard-library script (no `unittest` or `pytest`). It imports `is_prime` from `primality` and verifies it against an independent, straightforward trial-division reference implementation that is kept in this file only. The reference must not replace or alter the specified algorithm. The test must:
   - compare every integer from 0 through 10,000 using assertions, so any mismatch causes the test to fail;
   - explicitly include perfect-square boundary cases such as 121 and 10201;
   - verify that invalid types (`True`, `False`, `7.0`, `"7"`, `None`, and a non-`int` numeric type such as `fractions.Fraction`) raise `TypeError`, and that an `int` subclass is accepted;
   - print a clear summary of the number of tests performed, how many passed, and a list of any failures;
   - exit with a nonzero status on any failure.

   The output is captured to `problem2/Results/test_primality_output.txt` (UTF-8, using terminal redirection as in requirement 12).

#### Expected-value verification (`verify_expected.py`)
15. `verify_expected.py` is committed to the repository so that the expected values are reproducibly established. It must not import or call `is_prime()`, and it must not duplicate the responsibilities of `test_primality.py` (it checks the expected *values*, not the function).
   - It reads the `EXPECTED` table from `primality.py` by parsing the file with `ast` (the file is not imported or executed), and also checks the large benchmark inputs 999999999989, 999966000289 and 1000000000000.
   - For each value it determines primality by two independent methods, which must agree with each other and with the expected value: (A) exhaustive trial division, printing the factorisation of composites; (B) deterministic Miller–Rabin using the first 12 prime bases (2 to 37), valid for n < 3.3 × 10²⁴ (the script asserts this bound).
   - It prints one line per value and a summary of values checked and mismatches, and exits with a nonzero status on any disagreement.
   - Its method and limitations are documented in the file's docstring and in the README. The limitations are: both methods are the project's own code, so agreement is strong evidence and not formal proof; it verifies only the listed values and does not prove `is_prime` correct for all n; the `ast` extraction fails loudly if `EXPECTED` stops being a plain literal.
   - Its output is captured to `problem2/Results/verify_expected_output.txt` (UTF-8, using terminal redirection as in requirement 12).

#### Performance measurement (`benchmark.py`)
16. `benchmark.py` imports and times the unchanged `is_prime` and must not modify the primality-testing algorithm. It measures time only and is independent of `test_primality.py`.
   - It uses `time.perf_counter()`.
   - Each input is run five times, and the median, minimum and maximum elapsed times are reported.
   - Inputs: 999999999989 (a large prime, verified by `verify_expected.py`), 999983² = 999966000289 (a large prime square), and 1000000000000 (even, so it returns at step d, included for contrast). Further large inputs may be added.
   - Before timing each input it checks the result against the expected value, so that a wrong answer is never timed.
   - Results are saved in `problem2/Results/timing.txt` (UTF-8) with a header giving the Python version and platform.

#### README contents
17. The README must explain:
   - the algorithm, including the $6k\pm1$ sieve, the square-root bound, and that not every $6k\pm1$ number is prime;
   - usage (importing and calling `is_prime`);
   - the commands to run the correctness tests, the expected-value verification and the benchmark;
   - the verification method of `verify_expected.py` and its limitations;
   - how the output files in `Results/` are generated;
   - the performance limitations: the descending order of divisor testing (as specified in the assignment) is kept, and the trade-off is that composite numbers with small factors take longer to reject than they would in ascending order. Trial division also becomes expensive for very large integers;
   - a brief summary of the recorded timing results (details are in `Results/timing.txt`);
   - the Python version actually used for testing.

#### Deliverables
18. The generated evidence files `Results/test_output.txt`, `Results/test_primality_output.txt`, `Results/verify_expected_output.txt` and `Results/timing.txt` are included in the submission. The `Results/` directory is created before the files are generated.
