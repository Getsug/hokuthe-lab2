# Problem 4: Prime density for N = 5,000 to 5,000,000

## Objective

Find how the percentage of primes in the inclusive range [0, N] changes as the upper bound N grows from 5,000 to 5,000,000 in steps of 1,000 (4,996 sample points). The percentage is π(N)/(N+1) × 100, where π(N) is the number of primes ≤ N.

## Mathematical explanation

Problem 1 showed that every prime greater than 3 has the form 6k−1 or 6k+1 for some positive integer k. So the only candidates that need testing are 6k−1 and 6k+1, and the primes 2 and 3 are added by hand because they are never of that form for k ≥ 1. Each candidate is checked with `is_prime` from Problem 2, which is reused unchanged from `problem2/primality.py`.

## Algorithm

`enumerate_primes_6k(n_max)`:
1. Reject non-integers (including `bool`) with `TypeError`. Return `[]` for `n_max < 2`, `[2]` for `n_max == 2`, and `[2, 3]` for `n_max` of 3 or 4. These early returns happen before the loop.
2. Otherwise start with `primes = [2, 3]` and `k = 1`.
3. Loop: set `a = 6k−1` and `b = 6k+1`. Stop when both exceed `n_max`. Append `a` then `b` if each is within `n_max` and `is_prime` says it is prime. Increase `k`.
4. Return `primes`. There is no sort, because candidates are tested in increasing order, so the list is already strictly increasing.

The program enumerates primes once up to 5,000,000. Each π(N) is read from that single list with `bisect_right`, so no candidate is tested twice.

## Functions (`prime_density.py`)

| Function | Purpose |
|---|---|
| `enumerate_primes_6k(n_max)` | The 6k±1 enumeration described above. |
| `count_primes_up_to(primes, n)` | π(n) as `bisect_right(primes, n)`; 0 for n < 2. `primes` must be sorted. |
| `sample_points()` | The sampled N values, 5,000 to 5,000,000 inclusive, step 1,000. |
| `build_rows(primes)` | `(N, prime_count, prime_percentage)` for each sampled N. Feeds both the CSV and the graph. |
| `write_csv(rows, path)` | Writes the CSV with header `N,prime_count,prime_percentage`. |
| `save_plot(rows, path)` | Draws the graph (measured percentage plus the dashed 100/ln(N) curve) and saves it at 150 dpi. Imports matplotlib here, with the `Agg` backend. |
| `format_summary(primes, enum_time, processing_time)` | Builds the summary text. |
| `main()` | Runs everything and saves the outputs in `Results/`. |

## Dependencies and environment

- Python 3.14.7 was used for development and testing. The code does not check the version at runtime.
- Third-party dependency: `matplotlib` only (`requirements.txt`: `matplotlib>=3.8`). Version 3.11.2 was used for the results here. No `numpy` is required directly.
- The standard library covers everything else.

```
pip install -r requirements.txt
```

## Running

Run from any directory:

```
python problem4/prime_density.py        # graph, CSV and summary
python problem4/test_prime_density.py   # tests; saves Results/test_output.txt
```

Alternatively, from inside `problem4/`: `python -m unittest test_prime_density`.

Output paths are always `problem4/Results/`, which is created if missing.

## Testing

`test_prime_density.py` uses only `unittest`. It runs 15 tests and the last run reported 15 executed, 15 passed, 0 failed. It covers:
- `n_max` values 0 to 7, and 25 and 35 excluded from `enumerate_primes_6k(50)`
- an independent iterative Sieve of Eratosthenes compared with the enumeration for every n from 0 through 10,000, and for the full 5,000,000 range
- π(5,000) = 669 and π(5,000,000) = 348,513
- strict ordering with no duplicates, `TypeError` for invalid types, `[]` for negatives, the counting helper, and the 4,996 sample points
- the CSV round trip and the summary text

The expensive enumeration up to 5,000,000 is computed once and shared by the tests that need it. The process exits nonzero if any test fails.

## Output files (`Results/`)

| File | Content |
|---|---|
| `prime_density.png` | Measured percentage and the 100/ln(N) approximation. |
| `prime_density.csv` | 4,996 rows: `N`, `prime_count`, `prime_percentage`. |
| `summary.txt` | The printed summary. |
| `test_output.txt` | Test results (UTF-8), with executed, passed and failed counts. |
| `claude_observations.md` | Detailed observations from the actual results. |

## Measured results and runtimes

From the last run on the development machine:

| Quantity | Value |
|---|---|
| π(5,000)/(5,001) × 100 | 13.3773% (100/ln(5,000) = 11.7410%) |
| π(5,000,000)/(5,000,001) × 100 | 6.9703% (100/ln(5,000,000) = 6.4830%) |
| Total primes up to 5,000,000 | 348,513 |
| Prime-enumeration time | 47.759 s |
| Total processing time (enumeration, checkpoints, CSV, graph; excludes summary writing) | 57.713 s |
| Test suite (15 tests) | 66.162 s |

The roughly 10 s between enumeration and total processing is the checkpoint calculation, the CSV and the graph. That run was also the first matplotlib use on the machine, and matplotlib printed that it was building its font cache, so some of that time is a one-off cost. Times vary from run to run and between machines.

## Trend summary

The percentage of primes falls as N grows: from 13.3773% at N = 5,000 to 6.9703% at N = 5,000,000, while the number of primes rises from 669 to 348,513. The fall is steep at first and then slow. The data follows the Prime Number Theorem's trend of about 100/ln(N), which stays below the measured values (by 1.64 points at N = 5,000 and 0.49 points at N = 5,000,000). The sampled percentage is not strictly decreasing at every 1,000-step. See `Results/claude_observations.md` for the full analysis.

## Known limitations

- `is_prime` uses trial division, so the full run takes about a minute. Run time grows roughly like N^1.5 / ln N.
- Generating only 6k±1 candidates is a small constant-factor saving, not a change in complexity. A comparison on smaller N showed gains of about 1% to 12% (see `interrogation.md`, round 4).
- All primes up to 5,000,000 are kept in a list (about 14 MB). This is fine at this scale but would not suit a much larger N.
- The summary and graph describe only the 4,996 sampled points, not every N.
- The reported times were measured on one machine in one run.
