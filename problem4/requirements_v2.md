### Overview
This is a python program that systematically identifies primes numbers and investigates how the percentage of prime numbers changes as the upper bound $(N)$ increases from 5,000 to 5,000,000. The program will use the mathematical property established in Problem 1, which states that every prime number greater than 3 must have the form (6k-1) or (6k+1), where (k) is a positive integer. Starting with (k=1), the program will generate candidates in ascending order and verify their primality using the function developed in Problem 2, while handling the prime numbers 2 and 3 separately. To improve efficiency, the program will maintain a cumulative count of primes rather than restarting the search for every new value of (N), ensuring that each candidate is tested only once. At every fixed step of 1,000 from N = 5,000 to N = 5,000,000, it will calculate the percentage of prime numbers in the inclusive range $[0,N]$ using the formula $\pi(N)/(N+1)\times100$, where $\pi(N)$ represents the number of primes less than or equal to (N). The results will be presented in a clearly labelled graph that also shows the theoretical approximation $100/\ln(N)$, with the underlying data saved in a CSV file for verification. Finally, the observed trend will be analysed to explain how the proportion of prime numbers changes as (N) increases.

### Project Requirements

**Project setup**
1. The project is housed in a folder called **problem4**.
2. The intended development environment is **Python 3.14.7**. The program must not enforce this exact version at runtime. The README documents the Python version actually used for testing.
3. The project must contain a **README.md**, a **requirements.txt**, and an **interrogation.md**.
4. `requirements.txt` lists `matplotlib` as the only third-party dependency, using a compatible-version constraint (e.g. `matplotlib>=3.8`) rather than an exact pin.
5. Use the standard library plus `matplotlib` only. Do not require `numpy`.
6. Do not use recursion (in production code and in test code).
7. Set the matplotlib backend to `Agg` explicitly, before importing `pyplot`, so the script runs headless without requiring a display.

**Reuse of Problem 2**
8. The project must **reuse the `is_prime` function from `problem2/primality.py` unchanged**. It must not reimplement, edit or copy the primality logic.
9. The path to `problem2/` is resolved relative to `__file__` (e.g. `Path(__file__).resolve().parent.parent / "problem2"`) and added to `sys.path`. The program must not assume it is launched from the repository root or any particular working directory.

**Core function: `enumerate_primes_6k(n_max)`**
10. The primary function is named **`enumerate_primes_6k(n_max)`**. It returns a strictly increasing list of all primes $\le$ `n_max`, built by the $6k\pm1$ scheme.
11. **Input validation:** non-integer inputs, including `bool`, raise `TypeError`. Negative integers return `[]`.
12. The function implements the procedure below exactly as written and in the order written:
    - a. If `n_max < 2`, return `[]`.
    - b. If `n_max == 2`, return `[2]`.
    - c. If `n_max` is 3 or 4, return `[2, 3]`.
    - d. Otherwise (`n_max >= 5`), initialize `primes = [2, 3]`. These two primes are seeded manually because Problem 1 proved primes greater than 3 are $6k\pm1$, so 2 and 3 never appear as $6k\pm1$ for $k \ge 1$.
    - e. Set `k = 1`.
    - f. Loop:
        - i. Set `a = 6*k - 1` and `b = 6*k + 1`.
        - ii. If both `a > n_max` and `b > n_max`, break out of the loop.
        - iii. If `a <= n_max` and `is_prime(a)` is `True`, append `a` to `primes`.
        - iv. If `b <= n_max` and `is_prime(b)` is `True`, append `b` to `primes`.
        - v. Increment `k` by 1.
    - g. Return `primes`. **There is no final sort.**
    
    The early returns in steps a-c exit the function immediately, before the main loop. The main loop runs only when `n_max >= 5`.
13. Because $6k-1 < 6k+1 < 6(k+1)-1$, appending in that order keeps the list strictly increasing and tests every candidate in increasing numeric order. This is why no sort is needed; a test verifies it (requirement 29).

**Counting and sampling**
14. The program provides **`count_primes_up_to(primes, n)`**, which returns `bisect_right(primes, n)` (from the standard library). It returns `0` when `n < 2`. It assumes `primes` is sorted in ascending order.
15. The program must **not restart from zero for each $N$**. It enumerates primes once up to `N_MAX = 5_000_000`, then computes $\pi(N)$ for each sampled $N$ from that single list using `count_primes_up_to`. Each candidate is tested only once, and no primality test is repeated across sampled values of $N$.
16. Sample $N$ from `N_MIN = 5_000` to `N_MAX = 5_000_000` in steps of `N_SAMPLE_STEP = 1_000`. Both endpoints are included, giving `(5_000_000 - 5_000) // 1_000 + 1 = 4_996` sample points.
17. For each sampled $N$, compute the percentage $\pi(N)/(N+1)\times100$ (percentage of numbers in $[0,N]$ that are prime).
18. The program measures the end-to-end execution time with `time.perf_counter()` and reports it, without modifying `is_prime`. There is no strict time limit, and no progress indicator is required.

**Outputs.** All outputs are saved under `problem4/Results/`, resolved relative to `__file__` regardless of the current working directory. `Results/` is created automatically if missing, using `Path.mkdir(parents=True, exist_ok=True)`.

19. **Graph: `Results/prime_density.png`**
    - Figure size 10 × 6 inches, saved at 150 dpi, followed by `plt.close()`.
    - x-axis: $N$ (linear scale). y-axis: $\pi(N)/(N+1)\times100$.
    - The measured percentage is drawn as a continuous line with no individual markers.
    - $100/\ln(N)$ is drawn as a second **dashed** line, with a legend distinguishing the measured prime percentage from the theoretical approximation.
    - Include a title, readable axis labels, and a light grid.
    - The plotted values are the same underlying values saved in the CSV.
20. **CSV: `Results/prime_density.csv`**
    - Exactly three columns, header `N,prime_count,prime_percentage`. The theoretical $100/\ln(N)$ is not a CSV column.
    - Written with the standard `csv` module with consistent line endings.
    - `prime_percentage` is stored with at least six decimal places.
    - The values match those plotted in the graph.
21. **Summary: printed to stdout and automatically saved to `Results/summary.txt`**, containing:
    - $\pi(5{,}000)/(5{,}001)\times100$ and $100/\ln(5{,}000)$
    - $\pi(5{,}000{,}000)/(5{,}000{,}001)\times100$ and $100/\ln(5{,}000{,}000)$
    - the total number of primes found up to 5,000,000
    - the end-to-end execution time

    Percentages are printed to four decimal places and execution time to three decimal places.
22. **Observations: `Results/claude_observations.md`**
    - Written only after the actual graph and numerical results exist; it uses measured values only and invents no experimental values.
    - At least four numbered, data-supported observations covering: the decreasing prime percentage, the increasing total prime count, the relationship to the Prime Number Theorem ($\pi(N)/N \approx 1/\ln N$), and the efficiency of the $6k\pm1$ approach.
    - The user reviews it and adds their own interpretation.
    - It holds the detailed trend analysis; the README holds only a concise summary of the trend.

**Code structure**
23. The deliverable Python file is named **`prime_density.py`** and contains `enumerate_primes_6k(n_max)`, `count_primes_up_to(primes, n)`, and a `main()` that builds the graph, writes the CSV, and prints and saves the summary.
24. Add an `if __name__ == "__main__":` block that calls `main()`, producing `Results/prime_density.png`, `Results/prime_density.csv`, `Results/summary.txt`, and the printed summary.

**Testing.** Tests are in a separate **`test_prime_density.py`**, using the standard-library `unittest` only (no pytest, no other third-party test dependencies). The test output is saved to `Results/test_output.txt`. The full prime enumeration up to 5,000,000 is computed **once** in `setUpClass` and shared across every test that needs it. It is not repeated. Small boundary and unit tests stay independent of it where practical. The full verification of $\pi(5{,}000{,}000)=348{,}513$ is part of the default test suite.

25. **Boundary tests:** for `n_max` = 0, 1, 2, 3, 4, 5, 6, and 7, the returned list is exactly the primes $\le$ `n_max` (e.g. 3 and 4 give `[2, 3]`; 5 and 6 give `[2, 3, 5]`; 7 gives `[2, 3, 5, 7]`).
26. **Composite exclusion:** 25 and 35 are absent from `enumerate_primes_6k(50)`, even though both satisfy the $6k\pm1$ candidate condition.
27. **Independent cross-check:** an independent **iterative** Sieve of Eratosthenes, implemented only in the test code and without recursion, must equal `enumerate_primes_6k(n)` for `n` from 0 through 10,000. The sieve is used for verification only and never replaces the $6k\pm1$ enumeration in the production program.
28. **Known values:** $\pi(5{,}000)=669$ and $\pi(5{,}000{,}000)=348{,}513$.
29. **Order and uniqueness:** the enumerated list is strictly increasing and contains no duplicates.
30. **Input validation:** `TypeError` for `True`, `False`, `2.0`, `"5"`, and `None`; `[]` for negative integers.
31. **Counting helper:** `count_primes_up_to` returns `0` for `n < 2` and gives correct counts at and around prime values.
32. **Sample count:** the sampling grid has 4,996 points from 5,000 to 5,000,000 inclusive.

**Documentation and process**
33. The README includes: the problem objective; the mathematical explanation ($6k\pm1$); the algorithm; descriptions of each function; dependencies and the Python version actually used; execution commands; testing instructions; output files; measured runtimes; known limitations; and a concise summary of the observed trend.
34. `interrogation.md` records the user's actual questions and the assistant's responses.
35. Do not create or commit `project_chat.md` unless it is explicitly needed. No Git commits are made by the assistant; the user manages the repository.
