### Overview
This a simple python program that decides whether a given integer is a prime number or not. The algorithm used exploits two facts: 
1. A composite number n must have a factor no larger than $\lfloor\sqrt n\rfloor$ , so trial division only needs to reach the square root
2. From Problem 1, every prime greater than 3 is of the form $6k \pm 1$, so a mod-6 check can identify possible prime candidates with remainder 1 or 5, but these candidates must still be tested for primality. 
The function first handles 2 and 3, rejects other even numbers and multiples of 3, then tests eligible divisors of the form $6k\pm1$ in descending order from the largest candidate not exceeding $\lfloor\sqrt n\rfloor$ down to 5. Correctness is verified by a `__main__` block that runs the function on a set of edge cases that includes numbers like 25, 49 and 91 that survive the $6k \pm 1$ sieve but are composite. The output is captured in `Results/test_output.txt` as evidence that the code was run and works. The implementation must use only the standard library, avoid recursion and handle inputs up to at least 10^12 in reasonable time.

### Project Requirements
1. The project is housed in a folder called problem2
2. Use python 3.14.7 as the programming language
3. The project must have a README file. 
4. The program takes in a single integer. It can be a positive or a negative number. Non-integer inputs (including Boolean values) must raise `TypeError`.
5. The program has a single function named is_prime
6. The program should return True for prime numbers and False for non prime numbers
7. The program should implement the algorithm below exactly as it is written and in the order it is written:
	*a. Receive an integer n* 
	*b. If n is less than or equal to 1, return ``False``*
	*c.  If n = 2 or n = 3, return ``True``*
	*d. If n is divisible by 2 or divisible by 3, return ``False``*
	*e. Compute the limit L such that $L=\lfloor\sqrt n\rfloor$. Use `math.isqrt(n)`.*
	*f. Take your upper limit L, add 1, divide by 6 and round down. The result  is the starting k. Then count k downward to 1 and at each step test the two numbers 6k−1 and 6k+1, skipping whichever one is bigger than L. This walks through every possible prime divisor candidate up to L from the top down. In short, set $k=\lfloor(L+1)/6\rfloor$. For each k descending to 1, test candidates $6k+1$ first and then $6k-1$, skipping any candidate greater than L*
	*g.  if a candidate divides n, return ``False`` immediately*
	*h. if no divisor is found, return ``True``.*
8. Use standard library only (math)
9.  Do not use recursion
10. The program must correctly handle n up to at least $10^{12}$ using the square-root bound and $6k\pm1$ candidate filtering. Measure execution time for representative large inputs.
11. The deliverable python file should be named primality.py and must contain `is_prime(n)`.
12. Add a `if __name__ == "__main__":` block that calls `is_prime` on the test cases -7, 0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 25, 49, 91, 97, 121, 143, 7917, 7919, 10201, 999983 and 1000000000000, printing `n, is_prime(n)` for each, with the output captured to `Results/test_output.txt` using terminal redirection (`python problem2/primality.py > problem2/Results/test_output.txt`).
13. The `is_prime(n)` function must remain independently importable so that it can be  reused,  remains unchanged  and without duplicating the primality logic.
14. Verify the function against an independent reference primality test for a range of small integers and include perfect-square boundary cases such as 121 and 10201. The reference test must not replace the specified algorithm.
