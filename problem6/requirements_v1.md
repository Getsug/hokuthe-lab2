### Overview
This is a python program that computes Euler's Totient function, denoted by $\phi(n)$, which represents the number of positive integers less than $n$ that are relatively prime to $n$. Two integers are considered relatively prime if their Greatest Common Divisor (GCD) is 1. The program will reuse the non-recursive `gcd(a, b)` function developed in Problem 5 without modifying or reimplementing it. For a given positive integer $n$, the program will iterate through all integers from $1$ to $n-1$, calculate the GCD of each integer with $n$ and increment a counter whenever the GCD equals 1. The final count will be returned as the value of $\phi(n)$. The function will handle special cases such as $n=1$, for which $\phi(1)=1$, and reject non-positive inputs. To ensure correctness, the implementation will be tested against known totient values and mathematical properties, including $\phi(p)=p-1$ for prime numbers $p$. The function will use an iterative approach without recursion and remain independently importable for reuse.


### Project Requirements
1. The project is housed in a folder called **problem6**.
2. Use **Python 3.14.7** as the programming language.
3. The project must have a **README** file.
4. The project must **reuse the non-recursive `gcd` function from `problem5/gcd_iterative.py` unchanged**. Do not reimplement, edit or copy the gcd logic. Import it (e.g. via a `sys.path`).
5. The program has a single primary function named **`euler_totient(n)`** that returns $\phi(n)$, the number of integers in $\{1,2,\ldots,n-1\}$ that are coprime to $n$ (with $\phi(1)=1$ by convention).
6. The function takes in a single positive integer `n`. Non-integer inputs must raise a `TypeError` with a clear message. If `n < 1`, it must raise a `ValueError` with a clear message (the totient is only defined for positive integers).
7. The function must implement the definition below exactly as written and in the order written:  
    a. If `n` is not an integer, raise `TypeError`.  
    b. If `n < 1`, raise `ValueError`.  
    c. If `n == 1`, return `1`.  
    d. Initialize `count = 0`.  
    e. For each `i` from 1 to `n-1` inclusive:  
       i. If `gcd(i, n) == 1`, increment `count` by 1.  
    f. Return `count`.
8. The function must call the imported non-recursive `gcd` for every coprimality test. It must **not** use `math.gcd`, must **not** use a factorization shortcut and must **not** reimplement gcd inline.
9. Use standard library only (plus the imported `gcd`).
10. Do not use recursion.
11. The function must be correct for all positive integers `n`, including `n = 1` (where $\phi(1)=1$ by convention).
12. The deliverable Python file must be named **`euler_totient.py`** and must contain `euler_totient(n)`.
13. Add a `if __name__ == "__main__":` block that calls `euler_totient` on the test cases below, printing `euler_totient(n) = result` for each, with the output captured to **`Results/totient_output.txt`** using terminal redirection (e.g. `python problem6/euler_totient.py > problem6/Results/totient_output.txt` when run from the repository root):
    - `euler_totient(1)` → `1`
    - `euler_totient(2)` → `1`
    - `euler_totient(3)` → `2`
    - `euler_totient(4)` → `2`
    - `euler_totient(5)` → `4`
    - `euler_totient(6)` → `2`
    - `euler_totient(10)` → `4`
    - `euler_totient(12)` → `4` (the handout's worked example)
    - `euler_totient(13)` → `12` (prime, so $p-1$)
    - `euler_totient(15)` → `8`
    - `euler_totient(36)` → `12`
    - `euler_totient(100)` → `40`
14. The `__main__` block must also verify that `euler_totient(12) == 4` explicitly (the handout's stated example) and print `PASS` or `FAIL`, so the Results file is self-verifying evidence. It must also test that `euler_totient(0)` and `euler_totient(-5)` raise `ValueError`, that `euler_totient(5.5)` raises `TypeError`, and that $\phi(p)=p-1$ for the prime test inputs 3, 5 and 13, printing `PASS` or `FAIL` for each check.
15. The whole script should run in well preferably in under two seconds on all the test cases above (the largest is `n=100`). This expectation does not apply to the much larger inputs.
16. The `euler_totient(n)` function must remain independently importable so that it  can  be reuse without modifying or duplicating its implementation.
