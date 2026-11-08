# Homework 2: Primes, GCD and Euler's Totient

A set of small Python programs on primality, prime density, the Euclidean algorithm and Euler's totient function. Each problem lives in its own folder with its own detailed README. This file is the entry point.

## 1. Project Overview

The lab builds one chain of reusable number-theory tools and then uses them in experiments:

- **Problem 2** provides `is_prime`, which Problems 3, 4 and 7 reuse.
- **Problem 5** provides an iterative `gcd`, which Problem 6 reuses for `euler_totient`.
- **Problem 6** provides `euler_totient`, which Problem 7 reuses.

Every later problem imports the earlier code unchanged and does not copy it. The lab also practises a documented development workflow: requirements, design review, questioning of key decisions, then implementation and verification (see section 8).

## 2. Problems Covered

| # | Topic | Concept | Expected outcome |
|---|---|---|---|
| 1 | Form of primes | Every prime greater than 3 has the form 6k−1 or 6k+1. | A mathematical proof, which Problems 2 and 4 rely on. **There is no `problem1/` folder in this repository**; Problem 1 is only referenced by the other READMEs. |
| 2 | [`is_prime`](problem2/README.md) | Trial division by descending 6k±1 candidates up to ⌊√n⌋. | A correct primality test, checked against independent methods, plus timings. |
| 3 | [Random draws until a prime](problem3/README.md) | Draws until a prime are geometric with mean 1/p. The Prime Number Theorem gives p ≈ 1/ln x. | An empirical average number of draws for two intervals, compared with ln(midpoint). |
| 4 | [Prime density, N = 5,000 to 5,000,000](problem4/README.md) | The share of primes π(N)/(N+1) falls roughly like 1/ln N. | A graph, a CSV (4,996 rows) and a summary of how the percentage changes with N. |
| 5 | [Iterative Euclidean GCD](problem5/README.md) | gcd(a, b) = gcd(b, a mod b), written with a `while` loop and no recursion. | A GCD function that handles negatives, zero and very large integers. |
| 6 | [Euler's totient](problem6/README.md) | φ(n) counts integers below n that are coprime to n (φ(1) = 1 by convention). | `euler_totient(n)` built on the Problem 5 `gcd`. |
| 7 | [Totient identity check](problem7/README.md) | For distinct primes, φ(pq) = (p−1)(q−1). For equal primes, φ(p²) = p(p−1). | Direct computation versus the formula for five prime pairs in 2000..3000, plus a rejected equal-prime case. |

## 3. Repository Structure

```
hokuthe-lab2/
├── README.md                  # this file
├── .gitignore
├── problem2/                  # is_prime
├── problem3/                  # random draws until a prime
├── problem4/                  # prime density (needs matplotlib)
├── problem5/                  # iterative GCD
├── problem6/                  # Euler's totient
└── problem7/                  # totient identity verification
```

Every problem folder follows the same pattern:

| Item | Content |
|---|---|
| `*.py` | Source code and tests (names are in section 5) |
| `README.md` | Detailed documentation for that problem |
| `requirements_v1.md` | The requirements I wrote myself |
| `requirements_v2.md` | The requirements after review with Claude |
| `design_v1.md` | The design reviewed before implementation |
| `interrogation.md` | Questions asked about mathematical and engineering decisions, with the answers |
| `project_chat.md` | The conversation record for that problem |
| `Results/` | Captured program and test output (and the graph and CSV for Problem 4) |

Extra files: `problem2/` also has `verify_expected.py` and `benchmark.py`. `problem4/` also has `requirements.txt` (the pip dependency list, not a requirements document) and `Results/claude_observations.md`.

## 4. Setup and Dependencies

- **Python 3.14.7** (Windows 11) was used for development and for all recorded results. No program checks the version at runtime.
- **Standard library only** for Problems 2, 3, 5, 6 and 7.
- **Problem 4 needs Matplotlib** (`matplotlib>=3.8`; 3.11.2 was used for the recorded results).

Install the one third-party dependency from the repository root:

```
pip install -r problem4/requirements.txt
```

## 5. Running the Programs

All commands are run from the repository root. Problems 5, 6 and 7 import earlier problems using paths relative to their own files, so the working directory does not matter.

| Problem | Command | Notes |
|---|---|---|
| 2 | `python problem2/primality.py` | Self-check against a table of expected values |
| 2 | `python problem2/verify_expected.py` | Independent check of the expected values |
| 2 | `python problem2/test_primality.py` | 10,144 comparisons against a reference |
| 2 | `python problem2/benchmark.py` | Timing of large inputs |
| 3 | `python problem3/random_prime_trials.py` | Writes `problem3/Results/averages.txt`; about 30 s |
| 4 | `python problem4/prime_density.py` | Writes the graph, CSV and summary to `problem4/Results/`; about 1 min |
| 5 | `python problem5/gcd_iterative.py` | 19 checks |
| 6 | `python problem6/euler_totient.py` | 34 checks |
| 7 | `python problem7/verify_totient.py` | Writes `problem7/Results/totient_verification.txt`; about 11 s |

Test suites:

```
python problem3/test_random_prime_trials.py
python problem4/test_prime_density.py
python problem7/test_verify_totient.py
```

Problems 2, 5 and 6 keep their checks in the scripts listed above. Output redirection into `Results/` (and the PowerShell UTF-16 caveat) is described in each problem's README. Programs exit with a nonzero status on failure.

## 6. Testing and Verification

- **Independent references.** Problem 2 compares `is_prime` with a plain trial-division reference for every integer from 0 to 10,000. `verify_expected.py` establishes the expected values without calling `is_prime`, using exhaustive trial division and Miller–Rabin. Problem 4 compares the 6k±1 enumeration with a Sieve of Eratosthenes. Problem 6 cross-checks against `math.gcd` for n = 1 to 200 (in test code only).
- **Known mathematical values.** Examples: π(5,000) = 669 and π(5,000,000) = 348,513 (Problem 4), φ(12) = 4, φ(p) = p − 1, φ(p^k) (Problem 6), and gcd of consecutive Fibonacci numbers (Problem 5).
- **Edge cases.** Types (`bool`, `float`, `str`, `None`), negatives, zero, boundaries and malformed input.
- **Experiments.** Problem 3 runs seeded Monte Carlo simulations (seed 12345). Problem 4 samples 4,996 values of N. Problem 7 computes φ(pq) by direct GCD counting and compares it with (p−1)(q−1).
- **Stubs versus real runs (Problem 7).** Most Problem 7 unit tests stub `euler_totient` for speed. The mathematics is checked by a real unpatched run, a real `euler_totient(15) == 8` test and the full real five-pair run. See `problem7/interrogation.md`.

## 7. Results

All numbers below come from the files in each problem's `Results/` folder. Timings are from one machine and vary between runs.

| Problem | Result |
|---|---|
| 2 | 10,144 of 10,144 reference comparisons passed. 34 expected values checked with 0 mismatches. Median time for a 12-digit prime (999999999989) is about 22 ms. |
| 3 | Run A (5,000,000 to 6,000,000): empirical 15.21, theoretical ln(midpoint) 15.52. Run B (500,000,000,000 + 1,000,000): empirical 28.18, theoretical 26.94. Total about 30.7 s. Both gaps are within sampling noise. |
| 4 | The share of primes falls from 13.3773% at N = 5,000 to 6.9703% at N = 5,000,000 (348,513 primes). 100/ln(N) stays below the measured values (11.7410% and 6.4830% at the two ends). Total processing time was 57.7 s. |
| 5 | 19 of 19 checks passed. |
| 6 | 34 of 34 checks passed. |
| 7 | For all five pairs, φ(pq) equals (p−1)(q−1), and the summary line reads PASS. Example: φ(2003 × 2011) = φ(4,028,033) = 4,024,020. The 19 unit tests passed. Total run time was 11.0 s. `(2011, 2011)` is rejected as not distinct. |

The test counts above are taken from the recorded `Results/` files for Problems 2 to 6. For Problem 7 the unit tests and the full experiment were run during implementation, and the results file ends with `All distinct-prime cases verified: PASS`.

## 8. AI-Assisted Development

The work follows the same workflow for each problem:

1. I wrote `requirements_v1.md` independently.
2. I discussed it with Claude, which listed ambiguities, missing requirements and edge cases without implementing anything. I answered each question, and the agreed result became `requirements_v2.md`.
3. Claude proposed `design_v1.md`, and I reviewed it and approved or changed it before any code was written.
4. I interrogated important mathematical and engineering decisions (for example why a stub is used in tests, or why all inputs are validated before computing). The questions and answers are in `interrogation.md`.
5. Claude implemented the design. I verified the implementations through independent tests, known values and the experiments' recorded outputs.

The conversation record for each problem is in its `project_chat.md`.
