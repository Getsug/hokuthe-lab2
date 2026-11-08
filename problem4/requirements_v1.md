### Overview
This is a python program that systematically identifies primes numbers and investigates how the percentage of prime numbers changes as the upper bound $(N)$ increases from 5,000 to 5,000,000. The program will use the mathematical property established in Problem 1, which states that every prime number greater than 3 must have the form (6k-1) or (6k+1), where (k) is a positive integer. Starting with (k=1), the program will generate candidates in ascending order and verify their primality using the function developed in Problem 2, while handling the prime numbers 2 and 3 separately. To improve efficiency, the program will maintain a cumulative count of primes rather than restarting the search for every new value of (N), ensuring that each candidate is tested only once. At regular intervals, it will calculate the percentage of prime numbers in the inclusive range $[0,N]$using the formula $\pi(N)/(N+1)\times100$, where $\pi(N)$ represents the number of primes less than or equal to (N). The results will be presented in a clearly labelled graph, with the underlying data saved in a CSV file for verification. Finally, the observed trend will be analysed to explain how the proportion of prime numbers changes as (N) increases.

### Project Requirements
1. The project is housed in a folder called **problem4**.
2. Use **Python 3.14.7** as the programming language.
3. The project must have a **README** file.
4. The project must **reuse the `is_prime` function from `problem2/primality.py` unchanged**.  Meaning, it must not reimplement, edit or copy the primality logic. Import it (e.g. via a `sys.path`).
5. The program has a primary function named **`enumerate_primes_6k(n_max)`** that returns a sorted list of all primes $\le$ `n_max`, built by the $6k\pm1$ scheme.
6. `enumerate_primes_6k` must implement the procedure below exactly as written and in the order written:
    *a. For `n_max < 2`, return `[]`; for `n_max == 2`, return `[2]`. For `n_max >= 3`, initialize `primes = [2, 3]`. These two primes are seeded manually because Problem 1 proved primes greater than 3 are $6k\pm1$, so 2 and 3 never appear as $6k\pm1$ for $k \ge 1$.*
    *b. Set `k = 1`.*
    *c. Loop forever:*
        *i. Set `a = 6*k - 1` and `b = 6*k + 1`.*
        *ii. If both `a > n_max` and `b > n_max`, break out of the loop.*
        *iii. If `a <= n_max` and `is_prime(a)` is `True`, append `a` to `primes`.*
        *iv. If `b <= n_max` and `is_prime(b)` is `True`, append `b` to `primes`.*
        *v. Increment `k` by 1.*
    *d. Sort `primes` and return it.*
7. Because $6k-1 < 6k+1$, appending in that order keeps the list increasing and tests every candidate in increasing numeric order
8. The program must **not restart from zero for each $N$**. Enumerate primes once up to `N_MAX = 5_000_000`, then compute $\pi(N)$ for each sampled $N$ from that single list using `bisect_right` from the standard library to count primes less than or equal to each $N$.
9. Sample $N$ from `N_MIN = 5_000` to `N_MAX = 5_000_000` in steps of `N_SAMPLE_STEP = 1_000` (4,996 sample points).
10. For each sampled $N$, compute the percentage $\pi(N)/(N+1)\times100$ (percentage of numbers in $[0,N]$ that are prime).
11. Plot $N$ on the x-axis and $\pi(N)/(N+1)\times100$ on the y-axis. Include a title, axis labels, and a light grid. Save the figure as **`Results/prime_density.png`** at 150 dpi.
12. Print a summary to stdout containing: $\pi(5{,}000)/(5{,}001)\times100$, $100/\ln(5{,}000)$, $\pi(5{,}000{,}000)/(5{,}000{,}001)\times100$, $100/\ln(5{,}000{,}000)$ and the total number of primes found up to 5,000,000.
13. Write **`Results/claude_observations.md`** with at least four numbered observations about the graph.
14. Use standard library plus `matplotlib` only. Do not require `numpy`.
15. Do not use recursion.
16. Set the matplotlib backend to `Agg` explicitly so the script runs headless without requiring a display.
17. The script must enumerate candidates only once, avoid repeated primality testing across sampled values of $N$, and report its end-to-end execution time without modifying the `is_prime` function from Problem 2.
18. The deliverable Python file must be named **`prime_density.py`** and must contain `enumerate_primes_6k(n_max)`, a `bisect_right`-based counting helper and a `main()` that builds the graph and prints the summary.
19. Add a `if __name__ == "__main__":` block that calls `main()`, producing `Results/prime_density.png` and the printed summary. The printed summary may be captured to a text file in `Results/` as supporting evidence.
20. Save the underlying graph data to **`Results/prime_density.csv`** with columns `N`, `prime_count`, and `prime_percentage`. The values must match those plotted in the graph.
21. Verify the enumeration and percentage calculations using small inputs (`n_max` = 0, 1, 2, 3, 10, 25), confirm that composite candidates such as 25 and 35 are excluded, and check that $\pi(5{,}000)=669$ and $\pi(5{,}000{,}000)=348{,}513$.
