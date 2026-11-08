# Design Document: Prime Density (Problem 4)

Source requirements: [requirements_v2.md](requirements_v2.md).
Status: **approved with the decisions in section 7. Nothing is implemented yet.**
Principle: keep it simple. Two Python files, no classes, standard library plus `matplotlib` only, no recursion.

## 1. Goals and constraints

- Enumerate primes up to 5,000,000 **once** with the 6k±1 scheme, reusing the unchanged `is_prime` from `problem2/primality.py` (req 8, 12, 15).
- Derive π(N) for 4,996 sampled N values from that single list with `bisect_right` (req 14-16).
- Produce the graph, CSV and summary in `problem4/Results/` (req 19-21), then write the observations from the real results (req 22).
- The approach is kept even though measured gains over testing every integer are small (see interrogation.md, round 4). It does not change the O(N^1.5 / ln N) complexity.

## 2. Directory layout

```
problem4/
├── prime_density.py            deliverable: enumeration, counting, CSV, plot, summary
├── test_prime_density.py       unittest suite (own sieve for cross-checking)
├── README.md
├── requirements.txt            matplotlib>=3.8
├── requirements_v1.md / requirements_v2.md
├── design_v1.md
├── interrogation.md
└── Results/
    ├── prime_density.png
    ├── prime_density.csv
    ├── summary.txt
    ├── test_output.txt
    └── claude_observations.md
```

## 3. `prime_density.py`

### 3.1 Module setup

```
PROBLEM_DIR  = Path(__file__).resolve().parent
RESULTS_DIR  = PROBLEM_DIR / "Results"
PROBLEM2_DIR = PROBLEM_DIR.parent / "problem2"
sys.path.insert(0, str(PROBLEM2_DIR));  from primality import is_prime   # req 8, 9
N_MIN, N_MAX, N_SAMPLE_STEP = 5_000, 5_000_000, 1_000
```

- **matplotlib is imported lazily.** `matplotlib.use("Agg")` runs first, then `pyplot` is imported inside `save_plot` only (req 7). Importing `prime_density` from the tests therefore does not need matplotlib or open a display.
- Output locations are module constants and the writer functions take a directory/path argument, so tests can write to a temporary folder and never overwrite the real `Results/`.

### 3.2 Functions

| Function | Responsibility |
|---|---|
| `enumerate_primes_6k(n_max)` | Required. Validates the input, applies the early returns, then runs the 6k±1 loop exactly as in req 12. No final sort. |
| `count_primes_up_to(primes, n)` | Required. `0` if `n < 2`, else `bisect_right(primes, n)`. |
| `sample_points()` | Returns `range(N_MIN, N_MAX + 1, N_SAMPLE_STEP)` (4,996 values). |
| `build_rows(primes)` | For each sampled N, returns `(N, prime_count, prime_percentage)` with `prime_percentage = count / (N + 1) * 100`. These rows are the single source for both the CSV and the plot. |
| `write_csv(rows, path)` | Header `N,prime_count,prime_percentage`, written with the `csv` module. |
| `save_plot(rows, path)` | Builds the figure (see 3.4) and saves it. |
| `format_summary(primes, enum_time, processing_time)` | Returns the summary text (see 3.5). |
| `main()` | Orchestrates the run (see 3.3). |

`sample_points`, `build_rows`, `write_csv`, `save_plot` and `format_summary` are small helpers beyond the three functions that req 23 names. Req 23 says the file "contains" those three, so extra helpers are allowed. They make the pieces testable without rerunning the enumeration.

### 3.3 `enumerate_primes_6k(n_max)` control flow (maps 1:1 to req 12)

```
if isinstance(n_max, bool) or not isinstance(n_max, int): raise TypeError(...)
if n_max < 2:   return []
if n_max == 2:  return [2]
if n_max <= 4:  return [2, 3]
primes = [2, 3]
k = 1
while True:
    a, b = 6*k - 1, 6*k + 1
    if a > n_max and b > n_max: break
    if a <= n_max and is_prime(a): primes.append(a)
    if b <= n_max and is_prime(b): primes.append(b)
    k += 1
return primes
```

- An explicit type check is needed because the early returns happen before `is_prime` is ever called, so `is_prime`'s own `TypeError` would not catch `True` or `2.0`.
- Appending `a` before `b` keeps the list strictly increasing, so there is no sort.

### 3.4 Run flow in `main()`

1. `RESULTS_DIR.mkdir(parents=True, exist_ok=True)`.
2. `t_start = time.perf_counter()`.
3. `primes = enumerate_primes_6k(N_MAX)` (once), then `enum_time = time.perf_counter() - t_start`.
4. `rows = build_rows(primes)`.
5. `write_csv(rows, ...)` then `save_plot(rows, ...)`.
6. `processing_time = time.perf_counter() - t_start`.
7. `text = format_summary(primes, enum_time, processing_time)`, then print it and write it to `Results/summary.txt`.

Both times use `time.perf_counter()`. `processing_time` covers enumeration, sampling, CSV and graph, but not writing the summary, so it is labelled **"processing time"**, not "end-to-end runtime".

Plot details (`save_plot`): `Agg` backend, `figsize=(10, 6)`. A solid line for the measured percentage with no markers. A dashed line for `100 / math.log(N)` on the same N values. Title, axis labels, `grid(alpha=0.3)`, legend, `savefig(dpi=150)`, then `plt.close(fig)`.

The plot and the CSV both come from the same `rows` list. The CSV writes each float with its full `repr`, so the stored values equal the plotted ones exactly and exceed the six-decimal minimum. The theoretical curve is computed only for the graph and the summary, not stored in the CSV.

### 3.5 Summary content (`format_summary`)

Percentages to 4 decimals and the time to 3 decimals, in this order:
1. π(5,000)/(5,001)×100 and 100/ln(5,000)
2. π(5,000,000)/(5,000,001)×100 and 100/ln(5,000,000)
3. total primes up to 5,000,000
4. prime-enumeration time, in seconds (3 decimals)
5. total processing time, in seconds (3 decimals), labelled as excluding summary writing

π(5,000) and π(5,000,000) come from `count_primes_up_to` on the shared list.

## 4. `test_prime_density.py`

Standard-library `unittest` only. It imports `enumerate_primes_6k`, `count_primes_up_to`, `sample_points`, `build_rows`, `write_csv` and `format_summary` from `prime_density`.

- **Shared fixture:** `setUpClass` computes `enumerate_primes_6k(5_000_000)` once and stores it on the class (req "Testing").
- **Independent reference:** an iterative `sieve(n)` using a `bytearray`, defined in the test file only.

| Test group | Requirement | Uses shared list? |
|---|---|---|
| Boundary: `n_max` 0-7 return exactly the primes ≤ `n_max` | 25 | no |
| 25 and 35 absent from `enumerate_primes_6k(50)` | 26 | no |
| `enumerate_primes_6k(n) == sieve(n)` for every n in 0..10,000 | 27 | no |
| π(5,000) = 669 and π(5,000,000) = 348,513 | 28 | yes |
| List is strictly increasing, no duplicates (checked on the 5,000,000 list and on small lists) | 29 | yes |
| `TypeError` for `True`, `False`, `2.0`, `"5"`, `None`; `[]` for negatives | 30 | no |
| `count_primes_up_to`: 0 for n < 2, correct at and around primes | 31 | no |
| `len(sample_points()) == 4996`, first 5,000, last 5,000,000 | 32 | no |
| `build_rows` matches `count_primes_up_to`; CSV round-trips to the same values and has the exact header; summary text contains the expected labels | extra | yes |

The CSV and summary tests write to a temporary directory (`tempfile`), so running the tests never touches the real `Results/`.

**Saving test output (req "Testing"):** the file's `__main__` block runs `unittest` with a small runner that writes to both the console and `Results/test_output.txt`, opened with `encoding="utf-8"`. This avoids shell-redirect differences (PowerShell's `>` writes UTF-16). The tests also work with `python -m unittest`.
- The saved output ends with the number of tests executed, passed and failed. Passed = run − failures − errors − skipped.
- The process exits with a nonzero status if any test fails or errors (`sys.exit(0 if result.wasSuccessful() else 1)`).

## 5. Dependencies, commands and expected runtime

```
pip install -r requirements.txt
python prime_density.py            # graph, CSV, summary
python test_prime_density.py       # tests + saves Results/test_output.txt
```

- Estimated runtime is on the order of 40 seconds for the main run and a similar time for the test suite, which does the enumeration once in its own process. This is an extrapolation from measured smaller runs (interrogation.md, round 4). The real enumeration and processing times will be measured and recorded in the final results and the README. Nothing is estimated there.

## 6. Implementation order

1. `requirements.txt`, then `prime_density.py`.
2. `test_prime_density.py`, then run it and save `Results/test_output.txt`.
3. Run `prime_density.py` to produce the PNG, CSV and `summary.txt`.
4. Look at the actual graph and numbers, then write `Results/claude_observations.md` from them only.
5. Write `README.md` with the measured runtime, the Python version used, and the trend summary.
6. Append this design round to `interrogation.md`. No Git commits.

## 7. Approved decisions

1. **Extra helpers:** `sample_points`, `build_rows`, `write_csv`, `save_plot` and `format_summary` are kept. Each has one clear responsibility, with no further abstractions, and the algorithm stays as in requirements_v2.md.
2. **Timing:** both the enumeration time and the total processing time are measured with `time.perf_counter()` and reported. The total covers enumeration, checkpoint calculations, CSV and graph, and is labelled "processing time" because summary writing is excluded. Real measured values go in the results and the README.
3. **Test output:** the test runner writes `Results/test_output.txt` directly in UTF-8, includes the counts of tests executed, passed and failed, and exits nonzero on any failure.
4. **Matplotlib:** `matplotlib.use("Agg")` runs before `pyplot` is imported, and `pyplot` is imported inside `save_plot()`. The mathematical functions can be tested without matplotlib.
5. **Benchmark:** the optional comparison benchmark is not added.
