# Design Document: Random Prime Trials (Problem 3)

Source requirements: [requirements_v2.md](requirements_v2.md).
Status: **final, approved. Decisions from the review are recorded in section 7.**
Principle: keep it simple. Two plain stdlib scripts, no classes except one small test helper, no third-party dependencies.

## 1. Goals and constraints

- Implement `expected_draws(lo, hi, trials, rng)` with the sampling procedure of requirement 7 exactly as written. No draw cap and no change to the counting.
- Reuse `is_prime` from `problem2/primality.py` unchanged (import only, never copy).
- Validate inputs (types first, then values), then check once that the interval contains a prime, then run the trials.
- Standard library only, no recursion.
- Two files, so that the experiment and its tests each have one home:

| File | Role |
|---|---|
| `random_prime_trials.py` | The deliverable: `expected_draws`, `main()`, the two runs, console and file output |
| `test_random_prime_trials.py` | `unittest` tests, using an instrumented generator |

## 2. Directory layout

```
problem3/
├── random_prime_trials.py
├── test_random_prime_trials.py
├── README.md
├── requirements_v1.md / requirements_v2.md
├── design_v1.md
├── interrogation.md
└── Results/
    ├── averages.txt
    └── test_output.txt
```

`Results/` is created by `main()` if missing. The test output is produced by redirecting the test run (see section 5).

## 3. Component design

### 3.1 `random_prime_trials.py`

**Import of `is_prime` (req 4).** At module top:

```
PROBLEM2_DIR = Path(__file__).resolve().parent.parent / "problem2"
sys.path.insert(0, str(PROBLEM2_DIR))
from primality import is_prime
```

This is independent of the working directory. `problem2/primality.py` has no import-time side effects (its test table is inside `__main__`), so the import prints nothing. The `sys.path` entry is inserted at position 0, so a stray `primality` module elsewhere cannot shadow it. If the import fails, the error is left to propagate (a missing file should fail loudly).

**Public names:** `expected_draws(lo, hi, trials, rng)` and `main()`. Constants `SEED = 12345`, `RUNS` (a list of the two experiment definitions), and `RESULTS_DIR`.

**Control flow of `expected_draws`:**

```
# 1. type checks (req 17)
for each of lo, hi, trials: if isinstance(v, bool) or not isinstance(v, int): raise TypeError(names the argument and type)
if not isinstance(rng, random.Random): raise TypeError(...)

# 2. value checks (req 17)
if lo < 2:      raise ValueError
if lo > hi:     raise ValueError
if trials < 1:  raise ValueError

# 3. prime-existence precondition (req 18), once, never touches rng
for candidate in range(lo, hi + 1):
    if is_prime(candidate): break
else:
    raise ValueError(f"interval [{lo}, {hi}] contains no prime")

# 4. sampling procedure, exactly req 7
total = 0
for _ in range(trials):
    count = 0
    while True:
        x = rng.randint(lo, hi)
        count += 1
        if is_prime(x):
            break
    total += count
return total / trials
```

Design decisions:

- **Type checks run before any value check**, so a call with a bad type and a bad value raises `TypeError`. Each message names the argument.
- **Validation is separate from the procedure.** Steps 1 to 3 never call `rng`, so a seeded run gives the same numbers with or without them. Step 4 is the original algorithm, untouched.
- **Existence scan.** `range(lo, hi + 1)` is lazy, so no list is built. The loop stops at the first prime. The `for ... else` raises only when the whole interval was scanned. Iteration, no recursion.
- **Single-value interval.** `lo == hi` scans one number: a prime passes (and averages exactly 1), a composite raises `ValueError`.
- **Unbounded `trials`.** No maximum, as required.
- **Return value.** One `float` (`total / trials`), unchanged from the specification.

**Midpoint and theory (req 9).** In `main()`, `midpoint = (lo + hi) / 2` and `theory = math.log(midpoint)`, computed from the actual bounds of each run.

**Signature of `main`:** `main(runs=RUNS, results_dir=RESULTS_DIR)`. Both parameters default to the assigned experiments and `problem3/Results/`, so the command line behaviour is exactly as required. The parameters exist only so tests can exercise file writing with a tiny experiment in a temporary folder, without repeating the real experiments and without touching the real `averages.txt`.

**`main()` flow (req 8, 11, 14, 16):**

1. Start a total timer (`time.perf_counter()`). The total therefore includes every run, including the pre-validation scans inside each `expected_draws` call. Each run's timer likewise includes its own scan.
2. For each run definition (label, `lo`, `hi`, `trials`): create a **new** `random.Random(SEED)`, start a run timer, call `expected_draws`, stop the timer, compute the theory value, and build one output line.
3. Print each line to the console as soon as its run finishes, so progress is visible during the longer Run B.
4. After both runs, print the total time.
5. Create `Results/` (`mkdir(parents=True, exist_ok=True)`), then write all lines plus the total time to `Results/averages.txt` with `write_text`, which overwrites any previous file.

Line format (req 16), numbers with thousands separators for the bounds:

```
Run A: lo=5,000,000 hi=6,000,000 trials=1000 seed=12345 | empirical=15.43 | theoretical=15.52 | time=1.234 s
```

Total time line: `Total time: 36.789 s`. File encoding is ASCII, and the file is written with `encoding="utf-8"` explicitly, so the output does not depend on the platform default.

The `__main__` block is only `main()`.

### 3.2 `test_random_prime_trials.py`

Standard library `unittest`, run as `python problem3/test_random_prime_trials.py` or with `python -m unittest`. The module imports `expected_draws` from `random_prime_trials` (same folder, so it is importable when the script is run directly) and `is_prime` from the same object that module uses.

**Instrumented generator (req 19).** One small class:

```
class ScriptedRandom(random.Random):
    # __init__(sequence): stores the sequence, an index, and a draws list
    # randint(a, b): returns the next value and records it and the (a, b) arguments;
    #                raises AssertionError("sequence exhausted") if no values are left
```

It never cycles. It is a real `random.Random` subclass, so the type check passes. A second small class, `RecordingRandom(random.Random)`, wraps real seeded behaviour: its `randint` calls `super().randint` and records every returned value and the call count, so the Run A and Run B completion tests use real random draws while counting through the generator.

**Test cases** (one `unittest.TestCase` class per group):

| Group | Cases |
|---|---|
| Counting logic | `4, 6, 8, 11` with `lo=4, hi=11, trials=1` needs 4 draws, average 4.0. Two trials such as `[4, 11, 6, 7]` give a hand-computed average, confirming multi-trial summing. |
| Minimal intervals | `[2, 2]` and `[3, 3]` average exactly 1. Two trials of a single prime value also give 1. |
| Single value | prime `lo == hi` returns 1. Composite `lo == hi` (for example 9) raises `ValueError`. |
| Prime-containing | An interval such as `[24, 29]` passes validation. An interval whose only prime is at `hi` passes (scan reaches the last number). |
| Prime-free | `[24, 28]` and `[90, 96]` raise `ValueError`, the message includes the interval, and the generator's recorded call count is 0 (the check never touched `rng`). |
| Validation order | Non-int `lo`/`hi`/`trials` (float, string, `None`, `True`) raise `TypeError`. Non-`Random` `rng` (including `None` and the `random` module) raises `TypeError`. `lo < 2` (1, 0, -5), `lo > hi`, `trials` of 0 and -1 raise `ValueError`. A bad type combined with a bad value raises `TypeError`. |
| Reproducibility | Two calls with `random.Random(12345)` and identical parameters return identical floats (small interval and Run A parameters). |
| Validation does not consume rng | The state after a call is the same as the state of a fresh generator advanced only by the trials. This is checked by comparing the result of a seeded run to a hand-rolled copy of the plain procedure (the loop from req 7, written in the test) using an identically seeded generator. |
| Run completion (integration) | With a `RecordingRandom(12345)` and the real parameters: Run A's recorded draws contain exactly 1000 primes (checking each recorded value with `is_prime`), the last draw is prime, and the average equals `len(draws) / 1000`. The same for Run B with exactly 250 primes and `len(draws) / 250`. Each of these two experiments runs **once** in the whole suite. No other test repeats them. |
| Reuse | `random_prime_trials.is_prime is primality.is_prime` (same object), and the `primality` module's `__file__` ends in `problem2/primality.py`. |
| Path independence (subprocess) | A subprocess is started with the working directory set to a temporary folder (and a second time to the repo root). It runs a short inline program that imports `random_prime_trials` by absolute path, calls `expected_draws` on a tiny interval, and prints `is_prime.__module__`'s file, `RESULTS_DIR` and the result. The test checks that the import succeeded, that `RESULTS_DIR` is `problem3/Results` regardless of the working directory, and that nothing was created in the temporary folder. |
| Output file writing | `main(runs=<tiny runs>, results_dir=<temporary folder>)` creates the missing directory, writes the labelled lines (label, bounds, trials, seed, 2-decimal numbers, 3-decimal time) and a total-time line, and a second call **overwrites** the file (the line count does not double). |

**Cost of the integration test.** Run B's completion test repeats Run B's work (about 35 s, see section 4). It is the only full repeat of an experiment. Every other test uses tiny intervals and runs in milliseconds, so the suite takes about 40 s in total.

**Output.** unittest runs with `verbosity=2` via `unittest.main()`. It reports `Ran N tests` and ends with `OK` or `FAILED (...)` on stderr, so the redirect command in section 5 (`> ... 2>&1`) merges both streams. `unittest.main()` exits with status 1 on any failure or error.

## 4. Performance analysis and pre-validation overhead

This section is the documentation of the overhead requested in requirement 18. The figures below were measured with the unchanged Problem 2 `is_prime` on Python 3.14.7 (the interpreter on this machine) and are estimates for planning, not final results. The real numbers will be recorded in the README after implementation.

### 4.1 The cost of one `is_prime` call

Problem 2's `is_prime` walks the 6k±1 candidates in **descending** order from isqrt(n). So:

- Even numbers and multiples of 3 (two thirds of all integers) exit immediately.
- **Primes and composites whose smallest factor is 5 or more** (about one third of all integers) take close to a full walk, about isqrt(n)/3 loop iterations with two candidates each.
- Near 5 x 10^11, isqrt(n) is about 707,000, so a full walk is about 235,000 iterations.
- **Measured:** the average cost of a call on a uniformly random integer in Run B's interval is **about 5.3 ms** (300 draws). Run A's cost is negligible (isqrt about 2,400).

### 4.2 Expected cost of the experiments

| Run | Draws (expected) | Cost per call | Estimated time |
|---|---|---|---|
| A | 1000 x about 15.5 = about 15,500 | tiny (isqrt about 2,400) | well under 1 s |
| B | 250 x about 26.9 = about 6,700 | about 5.3 ms | **about 35 s** |

The random variation of the average draw count is about +/-6% (a geometric distribution with a mean near 27, over 250 trials), so Run B may take roughly 33 to 38 s. The goal of "under one minute" holds, with a margin of about 1.6x on this machine. A much slower machine could exceed it. The goal is not a correctness requirement.

### 4.3 Cost of the pre-validation scan

- The scan tests `lo, lo+1, ...` and stops at the first prime. The expected number of tested integers is about ln(lo), which is about 15.5 for Run A and about 27 for Run B.
- **Measured for Run B:** the first prime at or above 500,000,000,000 is 500,000,000,023, found after 24 integers in **about 0.10 s**. That is about **0.3% of Run B's time**. The Run A scan is on the order of milliseconds.
- It runs once per experiment, not once per trial. It consumes no random numbers, so it does not change seeded results.
- **Worst cases:**
  - A prime-free interval is scanned in full. For short intervals this is trivial.
  - The scan length near n is bounded by the largest prime gap there (a few hundred at 5 x 10^11), so any interval of about 1,000,000 numbers at that size, including Run B's, always contains a prime and exits early. An adversarial long prime-free interval does not exist at this scale.
  - Because the unchanged `is_prime` is expensive for numbers coprime to 6 (section 4.1), a scan of many such numbers near 5 x 10^11 would cost about 5 ms each. The assigned runs never come close to this.
- **Why this strategy.** It reuses `is_prime`, needs no extra code beyond a short loop, preserves the sampling algorithm, and costs well under 1% of the run. A sieve would be faster for dense scans, but is unnecessary and would add code beyond what the requirement asks for.

### 4.4 What is not optimised

`is_prime` is unchanged (requirement 4). No caching of results (it would change timing and not the draws, but adds complexity), no multiprocessing, and no shortcut around the `randint`-then-`is_prime` loop.

## 5. Workflow

1. Create `problem3/Results/` (the program also creates it if missing).
2. Write `random_prime_trials.py`. Run `python problem3/random_prime_trials.py` from the repo root and from another working directory. Confirm both work and the output format matches requirement 16.
3. Write `test_random_prime_trials.py`. Run the tests. Confirm 0 failures.
4. Generate the evidence files from the repo root in Git Bash (or cmd):
   ```
   python problem3/random_prime_trials.py                 # also writes Results/averages.txt
   python problem3/test_random_prime_trials.py > problem3/Results/test_output.txt 2>&1
   ```
5. Write `README.md` (requirement 21), using the real timings and the Python version actually used.
6. Final check: re-run both, confirm exit codes of 0, confirm `averages.txt` is overwritten (not appended) on a second run, and confirm `problem2/primality.py` is unmodified (`git status` / `git diff problem2`).

## 6. Technical considerations and risks

- **Run time.** Run B is dominated by the descending-order `is_prime` (section 4). Expected about 35 s, so the under-one-minute goal has only about 1.6x margin on this machine.
- **Run B test cost.** The completion test repeats Run B, so the whole test suite takes about 40 s.
- **Output encoding on Windows.** Redirect from Git Bash or cmd (PowerShell 5.1 `>` writes UTF-16). The output is ASCII only, and the results file is written explicitly as UTF-8.
- **Import by path.** The `sys.path` insertion at index 0 and the `primality` module name are tied to Problem 2's layout. If that file is renamed or moved, the import fails with `ModuleNotFoundError`, which is the desired loud failure.
- **Mid-run output.** Each run's line is printed as soon as it finishes, but the file is written only at the end. If the script is interrupted during Run B, no file is written and an old file stays in place.
- **Reproducibility.** Separate generators with the same seed make each run independently reproducible. Results depend on the `random.Random.randint` algorithm of the Python version, so exact averages may differ between Python versions. The README states the version used.
- **Python version.** Not enforced. Nothing in the code is version-specific.

## 7. Decisions recorded

1. The full Run B completion test stays in the default suite, verifying 250 completed trials on the real interval. It is the single integration test. Smaller deterministic tests cover individual behaviours.
2. Test output is produced with `python problem3/test_random_prime_trials.py > problem3/Results/test_output.txt 2>&1`. The report shows the number of tests run, and any failure gives a non-zero exit status.
3. The automated subprocess test for working-directory independence is kept. It checks both the import and the output path.
4. `is_prime` from Problem 2 is not modified. The README reports actual measured times after implementation, and the one-minute runtime is a performance goal, not a correctness requirement. The pre-validation scan runs once per experiment, uses no random numbers, and is included in the measured run and total times. Timing numbers in section 4 are preliminary estimates and are not reported as results.
5. Implementation follows this design and requirements_v2.md exactly, with no alternative algorithms and no extra dependencies.

## 8. Consistency with requirements_v2.md

| Requirement | Where addressed in this design |
|---|---|
| Req 1 (folder) | section 2 |
| Req 2 (Python version, not enforced) | section 6, section 5 step 5 |
| Req 3, 21 (README) | section 5 step 5 |
| Req 4 (reuse `is_prime`, `__file__` path) | section 3.1 import, section 3.2 Reuse and Path tests |
| Req 5, 6 (signature, inputs, return) | section 3.1 |
| Req 7 (procedure unchanged) | section 3.1 step 4 |
| Req 8, 11 (two runs, separate seeded generators) | section 3.1 `main()` |
| Req 9 (theory from actual midpoint) | section 3.1 |
| Req 10 (`randint`) | section 3.1 step 4 |
| Req 12, 13 (stdlib only, no recursion) | section 1, section 3.1 |
| Req 14 (timing) | section 3.1 `main()`, section 4 |
| Req 15 (file and functions) | section 3.1 |
| Req 16 (output format, overwrite, relative `Results/`) | section 3.1 `main()` |
| Req 17 (validation order) | section 3.1 steps 1 and 2, section 3.2 Validation order |
| Req 18 (prime-existence precondition, overhead documented) | section 3.1 step 3, section 4 |
| Req 19 (tests) | section 3.2 |
| Req 20 (optional statistics) | not implemented, out of scope |

## 9. Out of scope

- Standard error or confidence intervals (optional extra in requirement 20).
- Any change to `problem2/primality.py`, a draw cap, caching, multiprocessing or a faster primality test.
- Problem 4.
