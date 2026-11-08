### Overview
The goal is to estimate, using Monte Carlo simulation, how many random integers must be drawn from a given interval before one of them is prime. This gives a concrete, empirical demonstration of the Prime Number Theorem's prediction that primes thin out like $1/ln⁡N$ such that near 5.5 million there should be roughly 15–16 draws on average. Near 500 billion the draws should be roughly 27.

The program must reuse the `is_prime` function from Problem 2 unchanged (do not reimplement it), draw uniformly at random from an inclusive interval, repeat the experiment many times and report the average number of draws per run. Two intervals are tested with different trial counts (1000 trials near 5.5M, 250 trials near 500B) and each empirical average is printed alongside the theoretical prediction ln⁡(midpoint) for comparison. Results are saved to `Results/averages.txt` as evidence in the submission. The whole script should finish in reasonable time, preferably under a minute, using the standard library only.

### Project Requirements
1. The project is housed in a folder called **problem3**.
2. Use **Python 3.14.7** as the programming language.
3. The project must have a **README** file.
4. The project must **reuse the `is_prime` function from `problem2/primality.py` unchanged**. That is, it must not reimplement, edit or copy the primality logic. Import it (e.g. via a `sys.path`).
5. The program has a primary function named **`expected_draws(lo, hi, trials, rng)`** that estimates the average number of random draws needed to find a prime and returns that average.
6. The function takes in four inputs:
    - `lo`: the lower bound of the interval (inclusive)
    - `hi`: the upper bound of the interval (inclusive)
    - `trials`: the number of independent repetitions of the experiment
    - `rng`: a seeded `random.Random` instance used for all draws
7. The function must implement the procedure below exactly as written and in the order written:  
    a. Initialize `total = 0`.  
    b. Repeat the following `trials` times: 
	    i. Set `count = 0`. 
	    ii. Loop forever: draw `x = rng.randint(lo, hi)` (inclusive of both endpoints), increment `count` by 1 and if `is_prime(x)` is `True`, break out of the inner loop. Each draw is independent and sampling is with replacement, so the same number may be drawn more than once. The count includes the successful prime draw. 
	    iii. Add `count` to `total`. 
    c. Return `total / trials` (the empirical average number of draws per prime found).
8. The program must run **two experiments** and print the average for each:
    - **Run A:** `lo = 5_000_000`, `hi = 6_000_000`, `trials = 1000`
    - **Run B:** `lo = 500_000_000_000`, `hi = 500_000_000_000 + 1_000_000`, `trials = 250`
9. For each run, also print the **theoretical prediction** `ln(midpoint)` where `midpoint = (lo + hi) / 2`, so the empirical average can be compared against the Prime Number Theorem estimate.
10. Use `rng.randint(lo, hi)` (inclusive on both ends) and **not** `random.randrange`.
11. Create a dedicated random generator with `rng = random.Random(12345)` and pass it to `expected_draws()` for both experiments so results are reproducible.
12. Use standard library only (`random`, `math`, `sys`, `pathlib`).
13. Do not use recursion.
14. The whole script should run end-to-end in reasonable time, preferably **in under one minute** and report its execution time. This is a performance goal, not a strict correctness requirement.
15. The deliverable Python file must be named **`random_prime_trials.py`** and must contain `expected_draws(...)` plus a `main()` that runs both experiments.
16. Add a `if __name__ == "__main__":` block that runs both experiments and saves the printed averages to **`Results/averages.txt`**, with each line labelled by run (Run A / Run B) and showing the empirical average alongside the theoretical `ln(midpoint)` prediction.
17. Validate that `lo` and `hi` are integers, `lo <= hi`, `trials` is a positive integer, and `rng` is a `random.Random` instance. Raise `ValueError` for invalid bounds or trial counts and `TypeError` for incorrect input types. The function assumes the interval contains at least one prime; otherwise the search would not terminate.
18. Test the counting logic with a controlled sequence of draws (e.g. `4, 6, 8, 11`, which must require 4 draws), test `[2, 2]` and `[3, 3]` (average 1), test invalid bounds and zero trials, and verify that using the same seed and parameters reproduces the same results. Verify that Run A completes 1000 successful searches and Run B completes 250.
