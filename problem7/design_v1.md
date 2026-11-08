# Design v1: Problem 7 (Totient Identity Verification)

Implements `requirements_v2.md`. Requirement numbers (R#) refer to that document.

## 1. Deliverables

```
problem7/
  verify_totient.py            # verify_totient_identity + main (R5, R6)
  test_verify_totient.py       # unittest suite (R14)
  README.md                    # R15
  Results/totient_verification.txt   # generated (R12)
  requirements_v1.md, requirements_v2.md, design_v1.md
```

Nothing is added to `problem2/`, `problem5/` or `problem6/` (R1).

## 2. Module layout of `verify_totient.py`

1. Module docstring.
2. Imports: `sys`, `time`, `pathlib.Path`, then the two dependency imports.
3. Constants: `PRIMARY_PAIR`, `ADDITIONAL_PAIRS`, `CONTRAST_PAIR`, `LOW = 2000`, `HIGH = 3000`, `RESULTS_PATH`, `DISTINCT_MSG`.
4. `_validate_pairs(pairs)` (private helper).
5. `verify_totient_identity(pairs)`.
6. `_format_report(records, timings, total, contrast_note)` (pure formatting).
7. `main()`.
8. `if __name__ == "__main__": sys.exit(main())`.

### 2.1 Imports (R4)

```python
_ROOT = Path(__file__).resolve().parent.parent
for _d in ("problem2", "problem6"):
    sys.path.insert(0, str(_ROOT / _d))
from primality import is_prime
from euler_totient import euler_totient
```

`euler_totient.py` adds `problem5` to `sys.path` itself, so no extra handling is needed. Paths come from `__file__`, so the working directory does not matter. Importing `verify_totient` runs nothing.

### 2.2 `_validate_pairs(pairs)` (R7)

Runs over the whole batch before any computation, so nothing is partially processed (R7h). For each element, in order:

1. `pairs` is a `list`, else `TypeError`.
2. The element is a `tuple`, else `TypeError`. `len != 2` gives `ValueError`.
3. `p` and `q` are `int` and not `bool`, else `TypeError`.
4. `LOW <= p, q <= HIGH`, else `ValueError`.
5. `is_prime(p)` and `is_prime(q)`, else `ValueError`.
6. `p != q`, else `ValueError("p and q must be distinct primes")` (`DISTINCT_MSG`).
7. `frozenset((p, q))` is not already in a `seen` set, else `ValueError` (duplicate or reversed combination).

Steps 1 to 3 are applied to the element before 4 to 7, as R7 requires. Every message names the offending pair and the reason.

### 2.3 `verify_totient_identity(pairs)` (R6, R8)

```python
def verify_totient_identity(pairs):
    _validate_pairs(pairs)
    results = []
    for p, q in pairs:
        n = p * q
        phi_pq = euler_totient(n)
        expected = (p - 1) * (q - 1)
        results.append({"p": p, "q": q, "pq": n, "phi_pq": phi_pq,
                        "expected": expected, "matches": phi_pq == expected})
    return results
```

An empty list passes validation and returns `[]`. The loop is iterative, with no recursion. `euler_totient(n)` is always called, and the formula is only the comparison value.

### 2.4 `main()` (R9 to R13)

Per-pair timing needs a `perf_counter` around each `euler_totient` call. The function's contract returns plain records (R6, no extra keys), so `main()` times each pair by calling `verify_totient_identity([pair])` individually:

```
start_total = perf_counter()
for pair in [PRIMARY_PAIR, *ADDITIONAL_PAIRS]:
    t0 = perf_counter()
    rec = verify_totient_identity([pair])[0]
    timings.append(perf_counter() - t0)
    records.append(rec)
total = perf_counter() - start_total
```

Consequences of this choice:

- **Batch-level checks.** Per-pair calls skip the duplicate-combination check across the five pairs. Calling `verify_totient_identity` on the whole batch as well would run the expensive computation twice. So `main()` first calls the private `_validate_pairs(all_five)` once. It runs the cheap checks (`is_prime` on ten numbers) and the duplicate test, with no totient work, and it is excluded from the timing.
- **Per-pair time.** It includes the cheap validation of that one pair. It is dominated by `euler_totient`.

Contrast case:

```
try:
    verify_totient_identity([CONTRAST_PAIR])
except ValueError as e:
    if DISTINCT_MSG not in str(e): raise
    note = "... (2011, 2011) rejected: primes are not distinct; phi(p^2) = p(p-1), not (p-1)^2"
else:
    raise RuntimeError("contrast case unexpectedly succeeded")
```

Any other `ValueError`, or success, is treated as a failure (R11).

Report and exit:

1. Build the report text with `_format_report`. It has the order from R12: primary pair header, table, timings and total, contrast note, conclusion, summary line.
2. Create `Results/` with `mkdir(parents=True, exist_ok=True)`, then write the file with `write_text(..., encoding="utf-8")`, which overwrites. Print the same text to stdout.
3. `status = "PASS" if all(r["matches"] ...) else "FAIL"`. The summary line is `All distinct-prime cases verified: {status}`, always the last line.
4. Return `0` on PASS and `1` on FAIL. An unexpected exception (including file-write failure) is caught at the top of `main()`, reported to stderr, and returns `1` (R13). No partial file claims PASS: the file is written only after all computation succeeds.

### 2.5 Report format

```
Primary pair: p = 2003, q = 2011
<blank>
       p       q         pq    phi(pq)  (p-1)(q-1)  match?
    2003    2011    4028033    4024020     4024020    True
...
Timing (euler_totient, perf_counter):
  (2003, 2011): 1.23 s
  ...
  Total: 12.3 s
<blank>
Contrast case (not in table): ...
<blank>
Conclusion: ...
All distinct-prime cases verified: PASS
```

Columns are fixed-width via f-string alignment. The header is exactly `p`, `q`, `pq`, `phi(pq)`, `(p-1)(q-1)`, `match?`. Times are printed with `:.3f` seconds.

## 3. Tests: `test_verify_totient.py` (R14)

Standard `unittest`, one `TestCase` per area. In-range primes cost millions of GCD calls per pair, so the default suite avoids repeating the real five-pair computation. Stubbed tests check logic. The real runs check the mathematics (see the interrogation, Q1).

### 3.1 Stub rules (approved)

- **Patching:** `mock.patch("verify_totient.euler_totient", autospec=True, side_effect=...)`. `autospec=True` makes the mock respect the real function's signature.
- **Fixed literal values:** the stub returns hard-coded literals per input, never a formula computed in the test from `p` and `q`. The literals were derived by hand as `(p-1)(q-1)` and checked by integer arithmetic outside the code under test:

  | Pair | `pq` (stub argument) | Stub return |
  |---|---|---|
  | (2003, 2011) | 4028033 | 4024020 |
  | (2017, 2027) | 4088459 | 4084416 |
  | (2029, 2039) | 4137131 | 4133064 |
  | (2081, 2083) | 4334723 | 4330560 |
  | (2969, 2999) | 8904031 | 8898064 |

  The stub is a lookup on the argument, so an unexpected argument raises `KeyError` and fails the test.
- **Argument check:** each stubbed test asserts the mock was called with exactly `p * q` (`assert_called_once_with` or `assert_has_calls` in order).
- **Deliberately wrong value:** one case returns a wrong literal (for example `4024021` for `4028033`). It asserts `matches is False`, and that a report built from that record ends with `All distinct-prime cases verified: FAIL`.

### 3.2 Real-function tests

- **Small semiprime:** real `euler_totient(15)` must return 8. The test docstring and the README state that this checks the underlying totient function only. It does not exercise the Problem 7 workflow, because the 2000 to 3000 range restriction rejects 3 and 5.
- **Integration test (kept):** one real, unpatched `verify_totient_identity([(2003, 2011)])` must return one record with `phi_pq == expected == 4024020` and `matches is True`. It is labelled as slow.
- **No real `main()` test in the default suite.** The complete five-pair real experiment runs once during final verification (section 5), not in the unit tests.

### 3.3 Cases

| Area | Cases |
|---|---|
| Valid (stubbed) | Record keys and values; empty list returns `[]` with the stub not called; order preserved; call arguments are `p*q` |
| Wrong totient (stubbed) | Wrong literal gives `matches=False`; report ends with FAIL |
| Equal primes | `(2011, 2011)` raises `ValueError` containing `"distinct primes"` |
| Composite / range | `(2001, 2011)` composite; `(1999, 2003)` and `(2003, 3001)` out of range; bounds 2000 and 3000 are in range but rejected as non-prime |
| Types | `float`, `str`, `None`, `True` as `p` or `q` give `TypeError` |
| Malformed | `pairs` as a tuple/None/str gives `TypeError`; element as list/int gives `TypeError`; length 1 or 3 gives `ValueError` |
| Duplicates | `[(2003, 2011), (2003, 2011)]` and `[(2003, 2011), (2011, 2003)]` give `ValueError` |
| Fail-fast | A bad final pair raises and returns nothing; the stub is not called |
| Report | `_format_report` with fixed records: header text matches, summary is the last line, PASS for all-match records |
| `main()` (stubbed) | Totient stubbed, `RESULTS_PATH` patched to a temporary directory. Checks: file is created (including the missing `Results/` directory) and overwritten on a second run; printed output equals the file content; the primary pair is first; the contrast note appears and is not in the table; the file ends with PASS and the exit status is 0. With a wrong stub value, the file ends with FAIL and the exit status is 1. An unexpected exception returns 1 |

## 4. README outline (R15)

Objective; maths (`phi(p)=p-1`, multiplicativity, `phi(p^2)=p(p-1)`); algorithm (steps of R8); dependencies (Problems 2, 5, 6 with how they are imported); run commands (`python verify_totient.py`, `python -m unittest test_verify_totient -v`); outputs; measured runtimes and the Python version, filled in after the real run; limitations (O(n) totient, range hard-wired, pairs must be a list of tuples).

## 5. Implementation order

1. `verify_totient.py`.
2. `test_verify_totient.py`, then run it (fast suite plus the one real `(2003, 2011)` integration test).
3. Final verification: run `python verify_totient.py` once for the complete real five-pair experiment, recording timings and the Python version.
4. README with actual measurements.
5. Commit only after your approval.

## 6. Risks and open points

- **Runtime.** Each pair needs about 4 to 9 million `gcd` calls, so a full run may take from tens of seconds to a few minutes. This is accepted per R13 and measured, not limited.
- **Per-pair timing versus the batch API.** Timing each pair through a one-element call is a deliberate choice (see 2.4). The alternative is to add a private timing hook or extra record keys, which would break R6's exact key set.
