### Overview
The goal is to estimate, using Monte Carlo simulation, how many random integers must be drawn from a given interval before one of them is prime. This gives an empirical demonstration of the Prime Number Theorem's prediction that primes thin out like $1/\ln N$. Near 5.5 million there should be roughly 15–16 draws on average, and near 500 billion roughly 27 ($\ln \approx 26.94$).

The program must reuse the `is_prime` function from Problem 2 unchanged. It draws uniformly at random from an inclusive interval, repeats the experiment many times, and reports the average number of draws per run. Two intervals are tested (1000 trials near 5.5M, 250 trials near 500B). Each empirical average is printed alongside the theoretical prediction $\ln(\text{midpoint})$, the interval, trial count, seed and execution time. Results are saved to `problem3/Results/averages.txt`. The script should finish in under a minute and use only the Python standard library.

### Project Requirements
1. The project is housed in a folder called **problem3**.
2. Python 3.14.7 is the intended development environment, but the version is not enforced at runtime. The README documents the actual Python version used for testing.
3. The project must have a **README** (contents in requirement 21).
4. The project must reuse `is_prime` from `problem2/primality.py` unchanged, with no reimplementing, editing or copying. The import path is resolved relative to `__file__`, not the current working directory. It must work when launched from the repository root or any other directory.
5. The primary function is **`expected_draws(lo, hi, trials, rng)`**. It estimates the average number of random draws needed to find a prime and returns that average. The signature and return type (a single number) must not change, even for testing purposes.
6. Inputs:
    - `lo`: lower bound (inclusive)
    - `hi`: upper bound (inclusive)
    - `trials`: number of independent repetitions
    - `rng`: a seeded `random.Random` instance used for all draws
7. The function first validates its inputs (requirements 17 and 18), then runs the sampling procedure below exactly as written and in order:  
    a. Initialize `total = 0`.  
    b. Repeat `trials` times:  
        i. Set `count = 0`.  
        ii. Loop forever: draw `x = rng.randint(lo, hi)` (inclusive), increment `count` by 1, and if `is_prime(x)` is `True`, break. Draws are independent and with replacement. The count includes the successful prime draw.  
        iii. Add `count` to `total`.  
    c. Return `total / trials`.  
    There is no maximum-draw cap and no change to the counting procedure.
8. The program runs two experiments, each with its own generator (requirement 11):
    - **Run A:** `lo = 5_000_000`, `hi = 6_000_000`, `trials = 1000`
    - **Run B:** `lo = 500_000_000_000`, `hi = 500_000_000_000 + 1_000_000` (500,001,000,000), `trials = 250`  
    The bounds are not adjusted to make the midpoints round.
9. For each run, print the theoretical prediction `math.log(midpoint)`, where `midpoint = (lo + hi) / 2` is computed from the actual bounds. Nominal midpoints are never hard-coded.
10. Use `rng.randint(lo, hi)`, not `random.randrange`.
11. Each run uses its own generator, `random.Random(12345)`, created separately for Run A and Run B. Run B therefore does not depend on how many numbers Run A consumed. The seed is a documented constant.
12. Use the **Python standard library only**, with no fixed module list and no third-party dependencies.
13. Do not use recursion.
14. The whole script should run in under one minute. This is a performance goal, not a correctness requirement. Print the execution time of each experiment (seconds, 3 decimals) to the console. Also print the total script time.
15. The deliverable is **`random_prime_trials.py`**, containing `expected_draws(...)` and a `main()` that runs both experiments.
16. An `if __name__ == "__main__":` block calls `main()`. `main()` prints the results and writes `Results/averages.txt`, resolved relative to the script's folder (`problem3/Results/`). The directory is created if missing. The file is overwritten on every run, never appended to. Each run's labelled output (console and file) contains:
    - run label (Run A / Run B)
    - `lo`, `hi`, `trials`, seed
    - empirical average (2 decimals)
    - theoretical $\ln(\text{midpoint})$ (2 decimals)
    - execution time in seconds (3 decimals)

    Example: `Run A: lo=5,000,000 hi=6,000,000 trials=1000 seed=12345 | empirical=15.43 | theoretical=15.52 | time=1.234 s`
17. **Input validation, in this order:**
    - **Type checks first.** `TypeError` if `lo`, `hi` or `trials` is not an `int`. `bool` is rejected with `TypeError`. `TypeError` if `rng` is not a `random.Random` instance (subclasses allowed).
    - **Then value checks**, raising `ValueError` if `lo < 2`, `lo > hi`, or `trials < 1`. There is no maximum trial count.
18. **Prime-existence precondition.** After the checks in requirement 17 and before any random draw, `expected_draws` checks that `[lo, hi]` contains at least one prime:
    - Scan integers sequentially from `lo` upward with the unchanged `is_prime`, and stop at the first prime found. Do not scan the whole interval in advance.
    - If `hi` is passed without finding a prime, raise `ValueError` with a descriptive message that includes the interval.
    - The check runs once per `expected_draws` call, never inside the trial loop, and never calls `rng`. It does not consume any generator values.
    - Because `rng` is untouched, seeded results are identical to a run without the check. Only the failure behaviour changes.
    - A single-value composite interval (`lo == hi`) raises `ValueError`.
    - The strategy, its expected cost (a few dozen `is_prime` calls near the assigned intervals) and its worst case (a full scan of a prime-free interval) are documented in `design_v1.md`.
19. **Testing** uses `unittest`, in **`test_random_prime_trials.py`**, with output saved to `Results/test_output.txt`. Failed assertions must fail clearly.
    - **Controlled generator:** a `random.Random` subclass with an overridden `randint()` that returns a predetermined sequence and records every draw. It raises an error if the sequence is exhausted, and never cycles.
    - **Counting:** draws and completed searches are counted through the instrumented generator, never through `is_prime` calls, because validation adds extra calls.
    - **Counting logic:** sequence `4, 6, 8, 11` (with `lo=4`, `hi=11`) requires exactly 4 draws. `[2, 2]` and `[3, 3]` give an average of 1. Test intervals must contain a prime, or validation rejects them.
    - **Single-value intervals:** `lo == hi` with a prime gives exactly 1. `lo == hi` with a composite raises `ValueError`.
    - **Prime-containing intervals** pass validation. **Prime-free intervals** (e.g. `[24, 28]`) raise `ValueError` with no hang, and the test confirms the generator was never called.
    - **Invalid input:** `lo > hi`, `lo < 2`, `trials = 0` and negative `trials` raise `ValueError`. Non-int, bool, float and non-`Random` arguments raise `TypeError`. A case with both a bad type and a bad value raises `TypeError`.
    - **Reproducibility:** two executions with identical parameters and seeds give identical results.
    - **Run completion:** with an instrumented generator, Run A records exactly 1000 prime draws (one per completed search) and Run B exactly 250.
    - **Reuse:** a test confirms `is_prime` is the Problem 2 object, with no local copy.
20. **Optional extras:** a standard error or confidence interval is optional and not required. The required statistic is the arithmetic mean.
21. **README contents:** problem objective, mathematical background, algorithm explanation, input and output specifications, dependencies, execution commands (from the repo root and from `problem3`), testing instructions, output files, random seed, performance considerations (including pre-validation overhead), how `is_prime` is reused from Problem 2, and the actual Python version used for testing.
