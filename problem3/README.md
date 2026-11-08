# Problem 3: Random draws until a prime

## Objective
Estimate, by Monte Carlo simulation, how many integers drawn uniformly at random from an interval are needed before one is prime, and compare the empirical average with the Prime Number Theorem prediction.

## Mathematical background
Each draw is prime with probability p, the fraction of primes in the interval, independently of the other draws (sampling with replacement). The number of draws up to and including the first prime is geometric with mean 1/p. The Prime Number Theorem gives the density of primes near x as 1/ln x, so the expected number of draws is about ln(midpoint), with midpoint = (lo + hi) / 2. That is roughly 15.5 near 5.5 million and roughly 26.9 near 500 billion. A fuller derivation, and the reasons empirical averages differ from the prediction, are in [interrogation.md](interrogation.md).

## Algorithm
`expected_draws(lo, hi, trials, rng)` in `random_prime_trials.py`:
1. Validate types (`TypeError`), then values (`ValueError`): `lo >= 2`, `lo <= hi`, `trials >= 1`. `bool` is rejected as an integer argument, and `rng` must be a `random.Random`.
2. Precondition, once per call: scan `lo, lo+1, ...` with `is_prime`, stopping at the first prime. If none is found up to `hi`, raise `ValueError`. This scan never uses `rng`.
3. Sampling procedure: `total = 0`; repeat `trials` times: `count = 0`; loop `x = rng.randint(lo, hi)`, `count += 1`, stop when `is_prime(x)`; `total += count`. Return `total / trials`. There is no draw cap, and the successful draw is counted.

`main()` runs two experiments, each with its own `random.Random(12345)`:

| Run | lo | hi | trials |
|---|---|---|---|
| A | 5,000,000 | 6,000,000 | 1000 |
| B | 500,000,000,000 | 500,001,000,000 | 250 |

## Reuse of `is_prime` from Problem 2
`random_prime_trials.py` adds `problem2/` to `sys.path`, computed from `__file__` (not the working directory), and imports `is_prime` from `problem2/primality.py`. The file is not copied or edited, and the tests check that the imported function is the Problem 2 object.

## Input and output
- Input: none (no command-line arguments); the experiments are defined in the script.
- Console and `Results/averages.txt` (overwritten on each run, created if missing, relative to this folder): one line per run with the bounds, trials, seed, empirical average (2 decimals), theoretical `ln(midpoint)` (2 decimals) and run time (3 decimals), then the total time.

## Dependencies
Python standard library only. No third-party packages.

## Running
From the repository root or from any other directory:
```
python problem3/random_prime_trials.py
```

## Testing
```
python problem3/test_random_prime_trials.py > problem3/Results/test_output.txt 2>&1
```
Uses `unittest`; the report states the number of tests run, and a failure gives a nonzero exit status. The tests use an instrumented generator (`ScriptedRandom`, `RecordingRandom`) to count draws, not `is_prime` calls. They cover the counting logic (`4, 6, 8, 11` takes 4 draws; `[2, 2]` and `[3, 3]` average 1), prime-containing and prime-free intervals, single-value intervals, validation order, reproducibility, working-directory independence, output file writing and overwriting, and one full integration run each of A (1000 searches) and B (250 searches).

## Random seed
12345 for both runs, with a separate generator per run, so each run is reproducible on its own. Exact averages depend on the Python version's `random` implementation.

## Measured results
Python 3.14.7, Windows 11. These are the actual numbers from `Results/averages.txt`:

| Run | Empirical average | Theoretical ln(midpoint) | Time |
|---|---|---|---|
| A | 15.21 | 15.52 | 0.210 s |
| B | 28.18 | 26.94 | 30.512 s |
| Total | | | 30.722 s |

Timing varies between runs. Another run from the repository root gave 0.193 s, 29.420 s and 29.614 s with identical averages. The full test suite ran 25 tests in 32.127 s.

The gaps are -0.31 (Run A) and +1.24 (Run B). The standard error of an average is about ln(midpoint)/sqrt(trials), about 0.47 for Run A and 1.67 for Run B, so both gaps are well within normal sampling noise. For Run A the exact prime count in the interval is 64,336 (from a separate sieve), giving an exact expectation of 15.54 draws.

## Performance considerations
- Problem 2's `is_prime` tests divisors in descending order, so numbers coprime to 6 near 5 x 10^11 cost a nearly full trial-division walk. This makes Run B dominate the run time. The one-minute runtime is a performance goal, not a correctness requirement, and was met here (29.6 to 30.7 s total).
- The pre-validation scan runs once per experiment and stops at the first prime. A separate measurement before implementation found the first prime at or above 500,000,000,000 (500,000,000,023) after 24 integers in about 0.10 s. That is a standalone measurement, not a separate line in the output. The scan time is included in each run's reported time and in the total.
