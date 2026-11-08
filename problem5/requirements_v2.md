### Overview
This is a Python program that computes the Greatest Common Divisor (GCD) of two integers using the Euclidean algorithm without recursion. The algorithm is based on the mathematical property that $gcd(a,b)=gcd(b,a\bmod b)$, which allows the GCD to be calculated by repeatedly replacing the pair `(a, b)` with `(b, a % b)`. The algorithm does not require `a >= b`: if `a < b`, the first iteration exchanges their roles. The program uses an iterative `while` loop until the remainder becomes zero, at which point the current value of `a` is returned as the GCD.

The function handles equal inputs, zero inputs and relatively prime integers (each covered by an explicitly identified test case), as well as negative integers and integers larger than 64 bits. Inputs that are not Python integers are rejected with `TypeError`. To ensure correctness, the implementation is tested against known GCD values and against Python's built-in `math.gcd()`. The deliverable is a single Python file containing a non-recursive `gcd(a, b)` plus a `__main__` block that verifies it.

### Project Requirements
1. The project is housed in a folder called **problem5**.
2. **Python 3.14.7** is the intended development environment. The exact version is **not** enforced at runtime. The README must document the Python version actually used during testing.
3. The project must have a **README.md** file (see Requirement 18).
4. The project must **not use recursion** anywhere.
5. The program has a single public function named **`gcd(a, b)`** that returns the greatest common divisor of two integers. No other public functions are defined, and no helper functions are needed. The test-running logic is written directly in the `__main__` block.
6. The function takes two inputs, `a` and `b`, which may be any Python integers (positive, negative, or zero). It must not crash on any of these.
7. **Input validation.** Before the Euclidean algorithm begins, the function must validate both inputs. It accepts Python `int` values only and raises `TypeError` for `float`, `str`, `None`, `bool` (although `bool` is a subclass of `int`) and any other non-integer type. Validation happens before any step of Requirement 8.
8. The function must implement the Euclidean algorithm below exactly as written and in the order written (after the validation in Requirement 7):
    a. Replace `a` and `b` with their absolute values, so the function behaves correctly for negative inputs (gcd is conventionally non-negative).
    b. While `b` is not equal to 0:
        i. Set `(a, b) = (b, a % b)`, one Euclidean step per iteration.
    c. When `b == 0`, return `a`, which contains the gcd (the last nonzero value for nonzero inputs).
    d. Special case: `gcd(0, 0)` must return `0` (the loop does this naturally, since `b == 0` immediately and `a == 0`).
    e. The algorithm does not require `a >= b`. If `a < b`, the first iteration swaps their roles.
9. Use **iterative control flow only** (`while` loop). Do not call `gcd` inside itself. Code review is sufficient to verify this; no static-analysis tool is required.
10. Use the standard library only. The core function `gcd(a, b)` must not depend on any import. `math` and `sys` are imported **inside** the `if __name__ == "__main__":` block only (`math` for `math.gcd` comparison, `sys` for the exit status).
11. **Complexity.** For nonzero inputs, the function runs in $O(\log(\min(|a|,|b|)))$ iterations (the standard Euclidean bound, applied to the absolute values) and uses $O(1)$ extra memory under the standard arithmetic-operation model. If either input is zero, the loop runs at most once.
12. The deliverable Python file must be named **`gcd_iterative.py`** and must contain `gcd(a, b)` with the signature `def gcd(a: int, b: int) -> int:` and a concise docstring describing its behavior, inputs, return value and the `TypeError` behavior.
13. The `gcd(a, b)` function must remain independently importable so that it can be reused without modifying or duplicating its implementation (it will be reused in Problem 6). Importing the module must not run the tests or print anything.
14. **Test cases.** Add an `if __name__ == "__main__":` block that runs the **19 tests** below, all in this file. No separate `unittest` or `pytest` file is created.

    GCD tests (15). Each is checked against its hardcoded expected value **and** against `math.gcd`:

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
    | 11 | `gcd(1_000_000_007, 998_244_353)` | 1 | large primes, relatively prime |
    | 12 | `gcd(1, 987654321)` | 1 | `gcd(1, n)` |
    | 13 | `gcd(100, 25)` | 25 | one input a multiple of the other |
    | 14 | `gcd(832040, 514229)` | 1 | consecutive Fibonacci numbers (F30, F29), worst case for iteration count |
    | 15 | `gcd(2**100, 3 * 2**70)` | `2**70` (1180591620717411303424) | integers larger than 64 bits |

    A GCD test passes only if the function result equals both the hardcoded expected value and `math.gcd(a, b)`.

    TypeError tests (4). Each passes only if the call raises `TypeError`:

    | # | Call | Expected |
    |---|------|----------|
    | 16 | `gcd(1.5, 2)` | `TypeError` |
    | 17 | `gcd("a", 2)` | `TypeError` |
    | 18 | `gcd(None, 2)` | `TypeError` |
    | 19 | `gcd(True, 2)` | `TypeError` |

15. **Output format.** The `__main__` block prints one line per test, with the input values, computed result, expected result and status:
    - GCD tests: `gcd(12, 8) = 4 (expected 4) PASS` (or `FAIL`)
    - TypeError tests: `gcd(1.5, 2) raises TypeError (expected TypeError) PASS` (or `FAIL`)

    After all tests, print a final summary such as `19/19 passed` (passed count / total executed). The summary reports `19/19 passed` only if every test succeeds. If any test fails, the script must exit with a nonzero status (via `sys.exit`); otherwise it exits with status 0. Output must be ASCII-only.
16. **Results file.** The output is captured to **`problem5/Results/gcd_output.txt`** using terminal redirection. The `problem5/Results/` directory must exist before redirecting (the script does not create it). The generated `gcd_output.txt` must be included in the final submission.
17. **Execution paths.** The README documents how to run the program and capture its output from both the repository root and the `problem5` directory, and how to create `Results/` if it is missing. Because the output is ASCII-only (valid UTF-8), the documented PowerShell command must not depend on Windows PowerShell 5.1's default redirection encoding (UTF-16); it must set the encoding explicitly (for example `| Out-File -Encoding ascii`) or use `cmd` redirection. Example from the repository root:
    - `python problem5/gcd_iterative.py > problem5/Results/gcd_output.txt`  (cmd / POSIX shells)
    - `python problem5/gcd_iterative.py | Out-File -Encoding ascii problem5/Results/gcd_output.txt`  (PowerShell)
18. **README.md contents.** The README includes: the problem objective, an explanation of the Euclidean algorithm, the mathematical basis, the function interface (signature, inputs, return value, `TypeError` behavior), execution instructions (both paths, Requirement 17), the test cases, result-generation instructions, the Python version actually used during testing, and how `gcd` is reused in Problem 6.
19. **Deliverables.** `gcd_iterative.py`, `README.md`, `Results/gcd_output.txt` and `Interrogation.md` (documenting the learning interaction, using the actual questions and responses). `project_chat.md` is **not** included.
