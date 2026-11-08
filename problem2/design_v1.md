# Design Document: `is_prime` (Problem 2)

Source requirements: [requirements_v2.md](requirements_v2.md).
Status: **final, awaiting your approval before implementation. Nothing is implemented yet.**
Principle: keep it simple. Four plain stdlib scripts, no classes, no frameworks, no third-party dependencies, and one responsibility per file.

## 1. Goals and constraints

- Implement `is_prime(n)` exactly per the algorithm in requirements_v2.md (req 7): descending $6k\pm1$ trial division up to $\lfloor\sqrt n\rfloor$, testing $6k+1$ before $6k-1$.
- Standard library only, no recursion, correct for n up to at least $10^{12}$.
- Four small scripts, so that implementation, correctness testing, expected-value verification and benchmarking each have one clear home:

| File | Role |
|---|---|
| `primality.py` | The deliverable: `is_prime` plus a self-check `__main__` block |
| `test_primality.py` | Deterministic correctness tests of `is_prime` against a reference implementation (no timing) |
| `verify_expected.py` | Reproducible, independent verification of the expected *values* (does not test the function) |
| `benchmark.py` | Timing of large inputs (no correctness testing beyond a sanity check) |

Correctness and performance stay independent, so a failure in one can be investigated without the other.

## 2. Directory layout

```
problem2/
├── primality.py
├── test_primality.py
├── verify_expected.py
├── benchmark.py
├── README.md
├── requirements_v1.md / requirements_v2.md
├── design_v1.md
├── project_chat.md / interrogation.md
└── Results/
    ├── test_output.txt
    ├── test_primality_output.txt
    ├── verify_expected_output.txt
    └── timing.txt
```

## 3. Component design

### 3.1 `primality.py`

**Public API:** one function, `is_prime(n: int) -> bool`, with a concise docstring. There are no other public names. The expected-value table, the loop and the exit logic live inline in the `if __name__ == "__main__":` block, so no helper functions are added. `sys` is imported only for the exit status.

**Control flow (maps 1:1 to the spec steps):**

```
guard:  if isinstance(n, bool) or not isinstance(n, int): raise TypeError(clear message)
(a)     receive n
(b)     if n <= 1: return False
(c)     if n == 2 or n == 3: return True
(d)     if n % 2 == 0 or n % 3 == 0: return False
(e)     L = math.isqrt(n)
(f)     for k in range((L + 1) // 6, 0, -1):
            for c in (6*k + 1, 6*k - 1):      # 6k+1 first
                if c > L: continue
                (g) if n % c == 0: return False
(h)     return True
```

Design decisions:

- **Type guard.** `isinstance(n, int)` accepts `int` subclasses. `bool` is itself an `int` subclass, so it is rejected explicitly and first. Floats (including `7.0`), strings, `None`, `Fraction` and third-party numeric types fail the `int` check. There is no conversion. The message names the offending type, for example `is_prime() requires an int, got float`.
- **Iteration.** `range(start, 0, -1)` gives the descending walk without recursion and with no off-by-one risk. The two-element tuple enforces "6k+1 first, then 6k−1". Each candidate is checked against L, so the spec's skip rule is explicit. The skip can only trigger for 6k+1 at the top k.
- **Edge cases of the loop bounds.**
  - n = 5 or 7: L = 2, so k = ⌊3/6⌋ = 0, the loop is empty, and the function returns `True` (correct).
  - n = 25 to 48 (L = 5): k = 1, 7 > L is skipped, and 5 is tested. For n = 25 and 35 this returns `False`.
  - n = 49 to 120 (L = 7 to 10): k = 1, and both 7 and 5 are tested (for L = 7, 7 ≤ L).
- **No micro-optimisation.** The loop is kept literal to the spec. Pre-computing candidates or using `all(...)` would deviate from "exactly as written and in the order written".
- **Large `n`.** `math.isqrt` is exact for arbitrary-size ints (no float rounding). For n ≈ 10¹², L ≈ 10⁶, so there are at most about 166,000 values of k (two candidates each), which takes well under a second in CPython.

**`__main__` block:**

1. A literal named table, `EXPECTED = [(n, expected), ...]`, covering every case in req 12: the original cases, the added negatives (-1, -2, -3, -4, -25), 35, 169, 289, 361 and 999983² (999966000289). It is a plain literal of ints and bools so that `verify_expected.py` can read it with `ast` (see 3.3).
2. For each pair, call `is_prime(n)`, compare to `expected`, and print `f"{n}, {result}, PASS"` or `FAIL`.
3. Track a failure count. After the loop, `sys.exit(1)` if any failed.

**Independence of expected values.** The values are written by hand and never computed by `is_prime`. They are cross-checked by `verify_expected.py` (3.3).

### 3.2 `test_primality.py`

Stdlib only, a plain script (`python problem2/test_primality.py`), with no unittest or pytest. The script's own directory is on `sys.path` when it is run this way, so `from primality import is_prime` works from any working directory.

Contents:

- `reference_is_prime(n)`: the independent reference. It is plain trial division: `n < 2` returns False, then test every integer d from 2 while `d*d <= n`. It has no 6k±1 logic and shares no code with `primality.py`.
- **Test groups**, each counted separately:
  1. **Exhaustive small range:** every n from 0 to 10,000 compared against the reference.
  2. **Perfect-square boundaries:** 121, 169, 289, 361, 10201 and 999983², with neighbours (p²−1, p²+1) where meaningful.
  3. **Loop-boundary cases:** 5, 7, 25, 35, 49, and cases where L+1 is a multiple of 6.
  4. **Large inputs:** 999999999989, 999966000289 and 1000000000000 against the reference (about 10⁶ iterations each at most).
  5. **Type errors:** `True`, `False`, `7.0`, `"7"`, `None` and `Fraction(7, 1)` must raise `TypeError`. An instance of `class MyInt(int)` must be accepted and give the correct answer.
  6. **Negatives and zero:** -7, -1, 0 and 1 return False.
- **Checking and reporting.** Every comparison is an explicit check that raises or records an `AssertionError`-style failure with the case, expected value and actual value. The script keeps going so that all failures are listed. The final output is:
  ```
  Tests run: N
  Passed:    P
  Failed:    F
  ```
  followed by one line per failure. It calls `sys.exit(1)` if F > 0.

### 3.3 `verify_expected.py`

Purpose: a reproducible check that the hard-coded expected values are correct, determined **without calling `is_prime()`** and without reusing the algorithm under test.

**Inputs checked**
1. The `EXPECTED` table in `primality.py`, read with `ast` (parse the file, find the `EXPECTED` assignment, `ast.literal_eval` its value). The file is parsed, not imported or executed, and the check covers the exact table that the `__main__` block uses.
2. The extra large cases used in `test_primality.py` and `benchmark.py`: 999999999989, 999966000289 and 1000000000000. They are listed in `verify_expected.py` itself.

**Two independent methods per value** (the verdicts must agree):
- **Method A, factorisation by exhaustive trial division:** find the smallest factor by testing every integer from 2 up to √n. It is also written differently from the reference in `test_primality.py`, because it returns the factorisation. This is slow only for the large values, at about 10⁶ divisions. The factors are printed, so a reader can check by multiplication, for example `7917 = 3 * 7 * 13 * 29`.
- **Method B, deterministic Miller–Rabin:** uses the first 12 prime bases (2 to 37), which is proven deterministic for all n < 3.3 × 10²⁴, far beyond the values used here. It uses only `pow(a, d, n)`.

**Behaviour**
- For each value: print `n, expected, method A verdict, method B verdict, OK/MISMATCH`.
- Print a summary (values checked, mismatches) and `sys.exit(1)` if any method disagrees with another or with the expected value.
- Output goes to `Results/verify_expected_output.txt`.

**Documentation of method and limitations** (also summarised in the README)
- Both methods are my own code. Their agreement is strong evidence but not a formal proof or an external authority.
- Method A is a complete proof only because it is exhaustive for each value. Its cost is O(√n), so it is only used on the specific values listed.
- Method B is deterministic only below its documented bound (about 3.3 × 10²⁴). The script asserts n is below that bound before using it.
- It verifies only the listed values. It does not prove `is_prime` correct for all n. That is the job of `test_primality.py` (0–10,000 exhaustively, plus selected large values).
- The `ast` extraction relies on `EXPECTED` staying a plain literal. If it is changed to computed code, the script fails loudly instead of silently skipping it.
- It does not duplicate `test_primality.py`: that script tests the function, and this one only establishes what the correct answers are.

### 3.4 `benchmark.py`

- Imports the unchanged `is_prime`. It does not copy or patch it.
- Inputs: 999999999989 (prime), 999966000289 (= 999983², composite) and 1000000000000 (even, early exit, for contrast). The list is easy to extend.
- Per input: one untimed warm-up call, then 5 timed runs with `time.perf_counter()`. It reports median, min and max in milliseconds using `statistics.median`.
- Before timing, it checks that the result equals the expected value for the input, so it never times a wrong answer.
- The header records `sys.version` and `platform.platform()`. The table goes to stdout and is redirected into `Results/timing.txt`.
- Timing is kept out of `primality.py` and `test_primality.py`, so the tests stay deterministic.

## 4. Workflow

1. Create `problem2/Results/`.
2. Write `primality.py` and run it manually. Confirm all lines show PASS.
3. Write `verify_expected.py` and run it. Confirm there are no mismatches. This runs before the tests so the expected table is trusted first.
4. Write `test_primality.py` and run it. Confirm 0 failures.
5. Write `benchmark.py` and run it.
6. Generate the evidence files from the repo root in Git Bash (or cmd):
   ```
   python problem2/primality.py        > problem2/Results/test_output.txt
   python problem2/test_primality.py   > problem2/Results/test_primality_output.txt
   python problem2/verify_expected.py  > problem2/Results/verify_expected_output.txt
   python problem2/benchmark.py        > problem2/Results/timing.txt
   ```
7. Write `README.md` with the algorithm, usage, commands, the descending-order trade-off, the large-integer limitation, the verification method and its limitations, a timing summary taken from the real `timing.txt`, and the Python version actually used.
8. Final check: re-run all four and confirm exit codes are 0, and confirm that importing `primality` prints nothing.

## 5. Technical considerations and risks

- **Output encoding on Windows.** Redirect from Git Bash or cmd. PowerShell 5.1 `>` produces UTF-16. All output is ASCII, so UTF-8 is guaranteed in practice.
- **Python version.** The local interpreter may not be 3.14.7. The code uses nothing version-specific. The README and `timing.txt` record the version actually used (check with `python --version` first).
- **Descending order performance.** Composites whose smallest factor is 5 or more (for example 5·p for a large prime p) are found only near the end of the descending walk, so they take about as long as a prime of similar size. This trade-off goes in the README. It does not affect correctness and stays within the 10¹² target.
- **Very large integers.** Runtime grows as √n, so there is no cap in the code but it becomes impractical beyond roughly 10¹⁴–10¹⁶. This is documented.
- **Reuse by Problems 3 and 4.** `primality.py` has no import-time side effects, so it can be imported as-is. Those problems must make it importable (same folder, or a `sys.path` entry or package layout) and must not copy the code. The README will say so, and the exact mechanism is decided when Problems 3 and 4 are designed.
- **Single public function vs. tests.** The expected table and runner are inline in `__main__`, the reference lives only in `test_primality.py`, and the verification methods live only in `verify_expected.py`, so requirement 5 holds without helpers in `primality.py`.
- **Single source of truth for expected values.** The table lives only in `primality.py`. `verify_expected.py` reads it with `ast` instead of keeping a second copy. The only duplicated numbers are the three large benchmark inputs.

## 6. Consistency with requirements_v2.md

| Requirement | Where addressed in this design |
|---|---|
| Req 1 (structure, four scripts, `Results/` files) | §1, §2 |
| Req 2 (Python version, not enforced) | §5, §3.4 |
| Req 3, 17 (README) | §4 step 7 |
| Req 4 (type handling) | §3.1 guard, §3.2 group 5 |
| Req 5 (one public function, hints, docstring) | §3.1, §5 |
| Req 6, 7 (algorithm, order) | §3.1 pseudocode |
| Req 8 (stdlib only: `math`, `sys`, `fractions`, `ast`, `time`, `statistics`, `platform`) | §3.1 to §3.4 |
| Req 9 (no recursion) | §3.1 |
| Req 10, 16 (large inputs, timing) | §3.4, §3.1 |
| Req 11 (filename) | §3.1 |
| Req 12 (`__main__`, `EXPECTED` literal, cases) | §3.1 |
| Req 13 (importable, unchanged) | §3.1, §5 |
| Req 14 (correctness tests, plain script) | §3.2 |
| Req 15 (`verify_expected.py`) | §3.3 |
| Req 18 (four evidence files) | §4 step 6 |

## 7. Changes made to requirements_v2.md

requirements_v2.md was updated in place to match this design:

1. **Overview and req 1:** the project is described as four files with one responsibility each, and `verify_expected.py` and `Results/verify_expected_output.txt` are added to the structure.
2. **New req 15:** `verify_expected.py` independently verifies the expected values without `is_prime()`, using two methods, with its method and limitations documented. The benchmark, README and evidence requirements were renumbered to 16, 17 and 18.
3. **Req 8:** lists the stdlib modules per script (`fractions`, `ast`, `sys`, `time`, `statistics`, `platform`).
4. **Req 12:** the expected table is a named plain literal, `EXPECTED`, so it can be read with `ast`.
5. **Req 14:** `test_primality.py` is stated to be a plain stdlib script.
6. **Req 16:** the benchmark is stated to be independent of the tests and to check results before timing.
7. **Req 17 and 18:** the README covers the verification method and limitations, and the fourth evidence file is included.

## 8. Out of scope

- No CLI or stdin interface, no probabilistic or faster primality methods inside `is_prime`, no caching, and no third-party test frameworks.
- Problems 3 and 4.

## 9. Decisions recorded

- Design document: `problem2/design_v1.md`.
- `test_primality.py` is a plain stdlib script with explicit checks, a tests run/passed/failed report, and a nonzero exit status on any failure.
- `verify_expected.py` is kept in the repository (included in the submission) as a reproducible verification script. It verifies expected values only and does not duplicate `test_primality.py`.
- `benchmark.py` stays separate from `test_primality.py`, so correctness and performance can be investigated independently.
- Implementation, correctness testing, verification and benchmarking stay in separate files.
- The design stays simple: no classes, no frameworks, no third-party dependencies.
- The descending 6k±1 algorithm is unchanged.
