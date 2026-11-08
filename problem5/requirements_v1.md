### Overview
This is a python program that computes the Greatest Common Divisor (GCD) of two integers using the Euclidean algorithm without recursion. The algorithm is based on the mathematical property that $gcd(a,b)=gcd(b,a\bmod b)$, which allows the GCD to be calculated by repeatedly replacing the two integers with the smaller integer and the remainder of their division. The program will use an iterative `while` loop to perform these operations until the remainder becomes zero, at which point the current value of `a` is returned as the GCD. The function will handle cases where the inputs are equal, one input is zero or the integers are relatively prime. To ensure correctness, the implementation will be tested using known GCD values and compared against Python's built-in `math.gcd()` function. The deliverable is a single Python file containing a non-recursive `gcd(a, b)` plus a `__main__` block that verifies it against known cases.

### Project Requirements
1. The project is housed in a folder called **problem5**.
2. Use **Python 3.14.7** as the programming language.
3. The project must have a **README** file.
4. The project must **not use recursion** anywhere.
5. The program has a single public function named **`gcd(a, b)`** that returns the greatest common divisor of two integers.
6. The function takes in two inputs, `a` and `b`, which may be any integers (positive, negative, or zero). It must not crash on any of these.
7. The function must implement the Euclidean algorithm below exactly as written and in the order written:  
    a. Replace `a` and `b` with their absolute values, so the function behaves correctly for negative inputs (gcd is conventionally non-negative).
    b. While `b` is not equal to 0:
    i. Set `(a, b) = (b, a % b)` , one Euclidean step per iteration. 
    c. When `b == 0`, return `a`, which contains the gcd (the last nonzero value for nonzero inputs).
    d. Special case: `gcd(0, 0)` must return `0` (the loop does this naturally, since `b == 0` immediately and `a == 0`).
8. Use **iterative control flow only** (`while` loop). Do not call `gcd` inside itself.
9. Use standard library only. No imports are required for the core function (optionally `math` only for testing against `math.gcd`).
10. The function must run in $O(\log(\min(|a|,|b|)))$ iterations when both inputs are nonzero (the standard Euclidean bound) and use $O(1)$ extra memory. If either input is zero, the algorithm terminates immediately.
11. The deliverable Python file must be named **`gcd_iterative.py`** and must contain `gcd(a, b)`.
12. Add a `if __name__ == "__main__":` block that calls `gcd` on the test cases below, printing `gcd(a, b) = result` for each, with the output captured to **`Results/gcd_output.txt`** using terminal redirection (`python problem5/gcd_iterative.py > problem5/Results/gcd_output.txt`, run from the repository root):
    - `gcd(12, 8)` → `4`
    - `gcd(17, 5)` → `1`
    - `gcd(25, 25)` → `25`
    - `gcd(270, 192)` → `6`
    - `gcd(0, 7)` → `7`
    - `gcd(7, 0)` → `7`
    - `gcd(0, 0)` → `0`
    - `gcd(-12, 8)` → `4`
    - `gcd(12, -8)` → `4`
    - `gcd(-12, -8)` → `4`
    - `gcd(1_000_000_007, 998_244_353)` → verify against `math.gcd` (both are large primes; the answer should be 1)
13. The `__main__` block must also compare every result against Python's built-in `math.gcd` and print `PASS` or `FAIL` per case, so the Results file is self-verifying evidence.
14. The `gcd(a, b)` function must remain independently importable so that it can be reused without modifying or duplicating its implementation.
