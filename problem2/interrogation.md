# Interrogation: Why separate files instead of one `primality.py`?

**Question:** Why did you choose to separate `test_primality.py`, `benchmark.py`, and `verify_expected.py` rather than putting everything inside `primality.py`? What are the advantages and disadvantages of this architecture for such a small program?

## First, a correction on where each file came from

The three files do not have the same origin, and "I chose" is only partly accurate:

| File | Origin | Status |
|---|---|---|
| `test_primality.py` | **Your decision** (clarification 10: "Place independent reference verification in a separate `test_primality.py` file"). I raised the question (Q10) because requirement 5 ("a single function") conflicted with requirement 14 (a reference test). | Required in requirements_v2.md |
| `benchmark.py` | **My proposal** (Q2), which you approved. The alternative I offered was putting timing inside `test_primality.py`. | Required in requirements_v2.md |
| `verify_expected.py` | **My suggestion only**, in the open points of design_v1.md (point 3). It is a one-off script for cross-checking the hard-coded expected values. | **Not decided.** It is not in the requirements, and I proposed it as a throwaway script that might not be committed. |

So the "separate files" architecture is mostly a consequence of your requirements. My own additions are `benchmark.py` and the optional `verify_expected.py`.

## Why separate at all

1. **Requirement 5 (a single public function) and requirement 13 (reuse by Problems 3 and 4).** If `primality.py` held a reference implementation, a benchmark harness and a verifier, it would no longer be "one function", and anyone importing it would pull in code they don't need.
2. **Independence of the reference test (requirement 14).** The point of a reference implementation is to be an *independent* check. Placing it in a different file makes that independence visible. A reader can see that the two implementations share no code.
3. **Different outputs and different purposes.** Each script produces its own evidence file (`test_output.txt`, `test_primality_output.txt`, `timing.txt`). Correctness checks are deterministic. Timings are noisy and machine-dependent. Mixing them would put a noisy result next to a pass/fail result.
4. **No unspecified code inside the deliverable.** `primality.py` is the artifact that Problems 3 and 4 will import. Keeping it small means the "verified, unchanged" claim in requirement 13 applies to a short file that is easy to audit.

## Advantages

- **Auditability.** The deliverable is about 20–30 lines of logic. It can be compared against the spec step by step.
- **Real independence.** A bug copied into both the function and its checker is the classic failure of self-testing code. Separate files make that harder to do by accident.
- **Clean imports.** `import primality` has no side effects and no extra dependencies (`statistics`, `platform`, `time`), and exposes only `is_prime`.
- **Separation of concerns.** The tests can fail without touching the benchmark, and the benchmark can be re-run on another machine without re-running the tests.
- **Matches common practice.** Production code, tests and benchmarks living in separate modules is the normal layout, so the structure transfers to Problems 3 and 4 and to larger projects.
- **Easier to extend.** Adding test groups or benchmark inputs doesn't change the deliverable at all.

## Disadvantages

- **More files for a small program.** Three Python files, a README, and three result files for what is a ~25-line function. For a throwaway script, that is real overhead.
- **More to keep in sync.** The test cases appear in two places by design: the hard-coded table in `primality.py`'s `__main__` block and the groups in `test_primality.py`. Edits to one must be considered for the other. The benchmark's input list and its expected results are a third copy of some values.
- **Import/path fragility.** `test_primality.py` and `benchmark.py` do `from primality import is_prime`. That works when the scripts are run as files, because the script's own directory is on `sys.path`. It can break if they're run from another layout (for example as a package or by a test runner). Problems 3 and 4 face the same issue from sibling folders, and this is unresolved.
- **More commands to run and document.** The README has to explain three commands and three output files. A reviewer has to open more files to see that everything works.
- **Self-check in the deliverable partly duplicates the test file.** The `__main__` block in `primality.py` is itself a mini test suite. This is what the requirements ask for, but it means there are two verification mechanisms, and some overlap is unavoidable.
- **`verify_expected.py` adds a third verification layer.** It is arguably over-engineering unless the expected values really need an extra independent check. That is why I flagged it as optional and uncommitted.

## Alternatives I considered

| Alternative | Pros | Cons |
|---|---|---|
| **Everything in `primality.py`** | One file, one command, nothing to keep in sync | Violates "single public function". Imports pull in benchmark and reference code. The reference is not visibly independent. Deliverable is harder to audit. |
| **`primality.py` + one combined `test_primality.py` (tests and timing together)** | Two files, fewer moving parts | Timing noise mixed with deterministic checks, and one output file mixing two kinds of evidence. |
| **`unittest`/`pytest` instead of a plain script** | Standard tooling, discovery, richer failure reports | Doesn't give the exact "tests run / passed / failed" summary format you asked for without extra work. `pytest` is not standard library. |
| **Current design (three files)** | Clean separation, independent evidence | More files, as listed above. |

## Assessment

For a program this small, the separation is more structure than the code alone would justify, and a single file would be perfectly workable if this were a standalone script. The architecture is justified here by this project's specific requirements: the single-public-function rule, the independence of the reference check, reuse by later problems, and separate evidence files for a submission. I would keep `primality.py` and `test_primality.py` separate in any case. `benchmark.py` is the most optional of the three, and merging it into the test file would be a defensible simplification if you want fewer files. `verify_expected.py` should stay a throwaway script unless you want the verification evidence in the submission.

**Decision needed from you:** keep the three-file layout as specified, or merge `benchmark.py` into `test_primality.py`? And should `verify_expected.py` be committed, or stay uncommitted?

*Resolution (from your later reply):* the four-file structure is kept. `benchmark.py` stays separate, and `verify_expected.py` is kept in the repository.

---

# Interrogation 2: Why the 6k±1 descending search never misses a divisor, and why the square-root bound is needed

**Question:** Our primality-testing algorithm checks divisors of the form 6k+1 and 6k−1 in descending order, starting from the square-root bound. How can we mathematically prove that this approach will never miss a divisor of a composite number? Also, why is it necessary to include the square-root boundary, and what would happen if we excluded it?

## Part 1. Proof that no composite number is missed

**Setting.** Let n be an integer that has passed steps (b), (c) and (d): n > 3, and n is divisible by neither 2 nor 3. Let $L=\lfloor\sqrt n\rfloor$ and $K=\lfloor (L+1)/6\rfloor$. The loop tests, for every integer k with $1\le k\le K$, the candidates 6k+1 and 6k−1 that are $\le L$.

**Theorem (completeness).** If n is composite, the loop finds a candidate that divides n, so `is_prime(n)` returns `False`.

**Theorem (soundness).** If n is prime, the loop never finds a divisor, so `is_prime(n)` returns `True`.

### Lemma 1: a composite number has a prime factor no larger than $L$

Let n be composite and let p be its smallest prime factor. Write n = p·m. Then m > 1, and every prime factor of m is also a prime factor of n, so it is $\ge p$. Therefore $m\ge p$, and

$$p^2 \le p\,m = n \;\Rightarrow\; p\le\sqrt n .$$

Since p is an integer, $p\le\lfloor\sqrt n\rfloor = L$.

### Lemma 2: that factor has the form 6k±1 with k ≥ 1

n is odd and not divisible by 3 (step d), so its prime factor p is not 2 and not 3. Hence $p\ge 5$. Look at p modulo 6:

| p mod 6 | Consequence |
|---|---|
| 0, 2, 4 | p is even, so p = 2, which is excluded |
| 3 | p is divisible by 3, so p = 3, which is excluded |
| 1 | p = 6k+1 |
| 5 | p = 6k−1 |

So p = 6k+1 or p = 6k−1, and $p\ge5$ forces $k\ge1$ (5 = 6·1−1, 7 = 6·1+1).

### Lemma 3: every number of the form 6k±1 with $5\le c\le L$ is among the tested candidates

Let c = 6k±1 with $5\le c\le L$ and $k\ge1$. We need $k\le K$.
- If c = 6k+1 ≤ L, then $6k\le L-1$, so $k\le (L-1)/6\le (L+1)/6$.
- If c = 6k−1 ≤ L, then $6k\le L+1$, so $k\le (L+1)/6$.

In both cases k is an integer not larger than $(L+1)/6$, so $k\le\lfloor (L+1)/6\rfloor = K$. The loop visits every k from K down to 1, and the skip rule only discards candidates greater than L. So c is tested.

### Proof of completeness

By Lemma 1, n has a prime factor p with $p\le L$. By Lemma 2, p = 6k±1 with $p\ge5$. By Lemma 3, p is tested. When it is tested, $n \bmod p = 0$, and step (g) returns `False`. ∎

### Proof of soundness (no false `False`)

Suppose the loop returns `False`. Then some candidate c with $5\le c\le L$ divides n. Since $L\le\sqrt n<n$ for n > 1, we have 1 < c < n, so c is a proper divisor and n is composite. Consequently a prime n can never be rejected by the loop. The steps before the loop are also exact: n ≤ 1 is not prime, 2 and 3 are prime, and any n > 3 divisible by 2 or 3 has a proper divisor and is composite. ∎

### Remarks

1. **The order of the loop does not affect correctness.** The proof only uses that every k in 1..K is visited. Descending order (as the assignment requires) changes how soon a divisor is found, not whether it is found. For a composite whose smallest factor is large, descending order reaches that factor near the end, which is why the README notes the performance trade-off.
2. **Composite candidates are harmless.** Candidates such as 25, 35 and 49 have the form 6k±1 but are not prime. Testing them cannot cause a wrong answer: if a composite c divides n, then n is composite and `False` is correct (soundness). Their only cost is a few wasted divisions.
3. **Why K = ⌊(L+1)/6⌋ is exactly right.** The largest k with 6k−1 ≤ L is ⌊(L+1)/6⌋. For k = K+1 we have 6(K+1) > L+1, so even the smaller candidate 6(K+1)−1 exceeds L. No valid candidate lies above K.
4. **Worked examples (all in the test list).**

| n | L | K | Candidates tested | Result |
|---|---|---|---|---|
| 25 | 5 | 1 | 7 is skipped (> L), then 5 divides 25 | False |
| 49 | 7 | 1 | 7 divides 49 | False |
| 91 = 7·13 | 9 | 1 | 7 divides 91 | False |
| 121 = 11² | 11 | 2 | k = 2: 13 skipped, 11 divides 121 | False |
| 10201 = 101² | 101 | 17 | k = 17: 103 skipped, 101 divides 10201 | False |
| 7 (prime) | 2 | 0 | loop is empty | True |

## Part 2. Why the square-root bound is necessary, and what happens without it

The bound does two separate jobs. It makes the algorithm **fast**, and with a descending search it also gives the search a **starting point** and keeps it **correct**.

### 2.1 It is the reason the search is short (efficiency)

Lemma 1 shows that if any proper divisor exists, one exists at or below √n. Searching beyond L is therefore redundant: every divisor d > L is paired with a cofactor n/d < √n that would already have been found.

Estimated cost for n ≈ 10¹² (back-of-the-envelope figures, not measured):

| | With bound | Without bound (up to n − 1) |
|---|---|---|
| Largest candidate | about 10⁶ | about 10¹² |
| Values of k | about 166,000 | about 1.7 × 10¹¹ |
| Rough time in CPython | well under a second | many hours or days |

That is a factor of about √n (10⁶ here) more work. Removing the bound turns a method that comfortably handles 10¹² into one that is unusable there. This is why requirement 10 can be met at all. The actual timings will be measured by `benchmark.py`.

### 2.2 With a descending search it provides the starting point

A descending loop needs a top value. In step (f) that top is derived from L (k = ⌊(L+1)/6⌋). Without L, the only natural top would be n itself, which leads to the next problem.

### 2.3 Without a bound the search would give wrong answers for primes unless it is also capped below n

If candidates were allowed up to and including n, a prime n of the form 6k±1 would eventually test c = n, and n mod n = 0 would make the function return `False` for **every** such prime. The algorithm would be wrong, not just slow. A correct bound-free version must therefore stop at n − 1 (or at n/2 or n/5, which are still huge). The square root is the tightest bound that keeps the correctness proof above intact.

### 2.4 What happens if the bound is too small, even by one

The proof needs every divisor candidate up to **exactly** L. If L is too small, divisors are missed:

- For n = p² the only prime factor is p = √n. If the computed limit were p − 1, no candidate would reach p, and the function would wrongly return `True` for 25, 49, 121 and 10201.
- This is why step (e) specifies `math.isqrt(n)`. It is exact for integers of any size. `int(math.sqrt(n))` converts n to a float, and above about 2⁵³ the float square root can round to the wrong side of an exact integer, which is a real danger for large perfect squares.
- This is also why the test list includes perfect-square boundary cases (25, 49, 121, 169, 289, 361, 10201, 999983²): they are exactly the inputs where an off-by-one error in L would be exposed.

### 2.5 Summary

| Choice of upper limit | Correct? | Fast? |
|---|---|---|
| Exactly $\lfloor\sqrt n\rfloor$ (as specified) | Yes (proved above) | Yes, O(√n) |
| Larger than √n but below n | Yes | No, slower in proportion to the extra range |
| Up to and including n | **No**: primes of the form 6k±1 are rejected | No |
| Smaller than √n (including an off-by-one error) | **No**: composites such as p² are accepted as prime | Faster, but wrong |

## Caveat on this answer

The proof above is mathematical and covers the algorithm as specified. It is not a proof that the future Python code matches the specification. That is why the design also calls for exhaustive comparison with an independent reference for 0–10,000, the perfect-square boundary tests, and the separate verification of the large expected values. The cost figures in section 2.1 are estimates. The measured numbers will come from `benchmark.py`.
