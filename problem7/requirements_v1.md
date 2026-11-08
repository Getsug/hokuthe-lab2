
### Overview
This is a python program that verifies the mathematical relationship between Euler's Totient function and the product of two distinct prime numbers. The program will identify two prime numbers, $p$ and $q$, between $2000$ and $3000$ using the `is_prime()` function developed in Problem 2 and calculate their product $n=pq$. It will then compute $\phi(n)$ using the `euler_totient()` function developed in Problem 6, which relies on the non-recursive GCD function from Problem 5. The computed result will be compared against the theoretical formula $\phi(pq)=(p-1)(q-1)$ to verify whether both methods produce the same value. This process will be repeated for several combinations of distinct prime numbers within the specified range to provide additional evidence of correctness. The program will reuse the existing functions without modifying or reimplementing them, display the selected primes, their product, the computed totient, the theoretical value and whether the results match. The results will be saved in the `Results` folder for verification. 


### Project Requirements
1. The project is housed in a folder called **problem7**.
2. Use **Python 3.14.7** as the programming language.
3. The project must have a **README** file.
4. The project must **reuse both `euler_totient` from `problem6/euler_totient.py` and `is_prime` from `problem2/primality.py` unchanged**. Do not reimplement, edit, or copy either. Import them (e.g. via `sys.path`).
5. The program has a primary function named **`verify_totient_identity(pairs)`** that takes a list of prime pairs `[(p, q), ...]` and returns a list of result records, one per pair, each record containing at minimum: `p`, `q`, `pq`, `phi_pq`, `(p-1)*(q-1)` and boolean `matches`.
6. `verify_totient_identity` must implement the procedure below exactly as written and in the order written, for each pair `(p, q)`:  
    a. Validate that `p` and `q` are integers (excluding booleans) and raise `TypeError` otherwise. Check that both are between 2000 and 3000 and raise `ValueError` if not. Check that both are prime using the imported `is_prime` and raise `ValueError` if not.
    b. Check that `p != q` and raise `ValueError` if not.
    c. Compute `n = p * q`. 
    d. Compute `phi_pq = euler_totient(n)` using the imported function from Problem 6.
    e. Compute `expected = (p - 1) * (q - 1)`.  
    f. Set `matches = (phi_pq == expected)`.
    g. Append the record to the results list. 
    h. Return the results list.
7. The program must select **two distinct primes between 2000 and 3000** as its primary example. Use **(2003, 2011)** as the primary pair; the choice must be **fixed and reproducible**. The two primes must be clearly printed at the top of the output.
8. In addition to the primary pair, the program must test **at least four more distinct prime pairs** in the same range, to demonstrate the identity holds generally and is not an artifact of one choice. A suggested set:
    - (2017, 2027)
    - (2029, 2039)
    - (2081, 2083)
    - (2969, 2999)
    The program must **verify** each candidate is prime using `is_prime` before using it. Do not hard-code without checking.
9. The program must also test **one non-example for contrast**: a pair with `p == q` (e.g. (2011, 2011)) to show that the distinct-prime identity does not apply when the primes are not distinct. This case must be handled **without raising an uncaught exception**: the program should catch the `ValueError` from `verify_totient_identity`, print a one-line explanation that $\phi(p^2)=p(p-1)$ rather than $(p-1)^2$, and continue. 
10. The program must write a results table to **`Results/totient_verification.txt`** with one row per pair, columns: `p`, `q`, `pq`, `phi(pq)`, `(p-1)(q-1)`, `match?`. All rows for distinct-prime pairs must show `match? = True`. The file must end with a summary line: `All distinct-prime cases verified: PASS` (or `FAIL` if any mismatch).
11. The program must print a short **conclusion** to stdout and to the results file, explaining in one or two sentences why the identity holds.
12. Use standard library only (plus the imported `euler_totient` and `is_prime`).
13. Do not use recursion.
14. The whole script should complete in reasonable time while preserving the direct GCD-based `euler_totient()` implementation from Problem 6. Measure and report execution time; do not replace the required computation with the theoretical formula.
15. The deliverable Python file must be named **`verify_totient.py`** and must contain `verify_totient_identity(pairs)` plus a `main()` that runs the primary pair, the four additional pairs and the `p == q` contrast case, writing the results table and conclusion to `Results/totient_verification.txt`.
16. Add a `if __name__ == "__main__":` block that calls `main()`, producing `Results/totient_verification.txt` and the printed summary; the file is the self-verifying evidence for the submission.
17. Verify that the program handles valid distinct-prime pairs, equal primes (`ValueError`), composite inputs (`ValueError`), non-integer inputs (`TypeError`), an empty list of pairs (return `[]`), and malformed pairs (raise a clear exception). Verify that the results file contains the expected valid-pair records and that its summary reflects the actual comparisons.
