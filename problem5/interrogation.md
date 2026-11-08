# Interrogation: Problem 5 (Iterative Euclidean GCD)

## Q1. Why does replacing (a, b) with (b, a mod b) preserve the GCD? Why must the algorithm terminate?

**Question (as asked):** I understand that the Euclidean algorithm repeatedly replaces (a,b) with (b,a mod b), but why does this operation preserve the greatest common divisor? Can you explain the mathematical proof using a concrete example, and show why the algorithm must eventually terminate?

**Response:**

### Part 1: Why the GCD is preserved

Let `a = q*b + r`, where `q = a // b` and `r = a % b`, so `0 <= r < b`. The claim is

> gcd(a, b) = gcd(b, r)

The proof shows that the pairs (a, b) and (b, r) have exactly the **same set of common divisors**. If the sets are equal, their largest elements are equal.

**Step 1: every common divisor of (a, b) divides r.**
Suppose `d | a` and `d | b`. Then `d | q*b`, since it is a multiple of `b`. A divisor of two numbers divides their difference, so `d | (a - q*b)`, and `a - q*b = r`. Hence `d | b` and `d | r`, so `d` is a common divisor of (b, r).

**Step 2: every common divisor of (b, r) divides a.**
Suppose `d | b` and `d | r`. Then `d | q*b`, and a divisor of two numbers divides their sum, so `d | (q*b + r)`, and `q*b + r = a`. Hence `d | a` and `d | b`, so `d` is a common divisor of (a, b).

Steps 1 and 2 together give: CommonDivisors(a, b) = CommonDivisors(b, r). The greatest element of equal sets is the same, so gcd(a, b) = gcd(b, r). Nothing in the proof depends on `a` and `b` being anything beyond integers with `b != 0`, so each loop iteration is safe.

### Concrete example: gcd(270, 192)

| Step | Equation | (a, b) after the step |
|------|----------|-----------------------|
| start | | (270, 192) |
| 1 | 270 = 1 * 192 + **78** | (192, 78) |
| 2 | 192 = 2 * 78 + **36** | (78, 36) |
| 3 | 78 = 2 * 36 + **6** | (36, 6) |
| 4 | 36 = 6 * 6 + **0** | (6, 0) |

When `b == 0`, the loop stops and the function returns `a = 6`.

Checking the claim on step 1, `270 = 1*192 + 78`:
- Take `d = 6`. It divides 270 (270 = 6*45) and 192 (192 = 6*32). By Step 1 of the proof it must divide `270 - 192 = 78`, and indeed 78 = 6*13.
- Take `d = 3`. It divides 270 and 192, and it also divides 78 (78 = 3*26).
- Going the other way, `6` divides 192 and 78, so it divides `1*192 + 78 = 270`.
- A number that is not a common divisor of (270, 192), such as 4 (270 / 4 is not an integer), also does not divide both 192 and 78 (78 / 4 is not an integer). The two pairs agree on every number.

The common divisors of (270, 192) are 1, 2, 3, 6. Those of (192, 78) are the same four numbers, and so are those of (78, 36), (36, 6) and (6, 0). The greatest of them stays 6 throughout, which is why the answer is not changed by any step.

**The last step.** When `b == 0`, every integer divides 0, so the common divisors of (a, 0) are just the divisors of `a`. The greatest divisor of `a` is `|a|`, so gcd(a, 0) = a. That is why returning `a` when `b == 0` is correct.

**Negatives.** The divisors of `n` and `-n` are identical, so gcd(a, b) = gcd(|a|, |b|). That is why step 8a (take absolute values) does not change the answer, and it also means `a % b` is only ever computed on non-negative numbers.

**Unordered inputs.** If `a < b`, then `a // b = 0` and `a % b = a`, so `(a, b) -> (b, a)`. For gcd(192, 270), the first iteration gives (270, 192), and the rest follows the table above. This is why no `a >= b` check is needed.

### Part 2: Why the algorithm must terminate

1. The remainder satisfies `0 <= r < b`. After one iteration the new second value is `r`, and it is **strictly smaller** than the old second value `b`.
2. So the sequence of second values `b0 > b1 > b2 > ...` is a strictly decreasing sequence of non-negative integers.
3. There is no infinite strictly decreasing sequence of non-negative integers (the well-ordering principle): after at most `b0` steps the value would run out of room, since it would have to go below 0.
4. So the second value must eventually reach 0, which is the loop's exit condition.

In the example the second values are 192, 78, 36, 6, 0, which is strictly decreasing and ends at 0 after 4 iterations.

### Why it is fast (links to Requirement 11)

The number of iterations is logarithmic, not just finite. Claim: `a % b < a/2` whenever `a >= b > 0`.
- If `b <= a/2`, then `r < b <= a/2`.
- If `b > a/2`, then `q = 1` and `r = a - b < a/2`.

So after every two iterations the larger value has at least halved, giving at most about `2 * log2(min(|a|, |b|))` iterations. Consecutive Fibonacci numbers, such as test #14 `gcd(832040, 514229)`, are the worst case: every quotient is 1, so the values shrink as slowly as possible.

### Takeaway for the implementation

- **Invariant** at the top of every loop iteration: gcd(a, b) equals the answer for the original absolute values.
- **Termination:** `b` strictly decreases and stays non-negative.
- **Exit:** when `b == 0`, `a` is the answer.

This invariant, termination argument and exit condition together prove the loop in `gcd` is correct.

---

## Q2. Is 19 tests, double checking, exception handling, PASS/FAIL reporting and exit codes justified for a function this small? What is the minimum convincing test strategy?

**Question (as asked):** For a function that only requires a few lines of Python, our design includes 19 test cases, expected-value comparisons, exception handling, PASS/FAIL reporting, and process exit codes. Is this amount of testing justified for such a small function? What would be the minimum testing strategy that still provides convincing evidence of correctness?

**Response:**

### Short answer

Partly. The function is about four lines of algorithm, so the amount of test *machinery* is out of proportion to it. But most of the cost is in the reporting around the tests, not in the tests themselves, and a few of the tests do real work. Some pieces are justified, some are redundant, and one thing is better than what we planned: an exhaustive check of a small range.

### What the size of the function does and does not tell you

Size is a poor guide to risk here. The four lines hide several behaviors that are easy to get wrong:
- **Sign handling.** Python's `%` takes the sign of the divisor. Without `abs`, `gcd(-12, 8)` still returns 4 by luck, but `gcd(12, -8)` returns -4 and `gcd(-12, -8)` returns -4. So tests #9 and #10 catch a missing `abs`, and test #8 alone would not.
- **Zero handling.** `gcd(0, 0)`, `gcd(0, 7)` and `gcd(7, 0)` take different paths through the loop (zero iterations, one iteration, zero iterations).
- **Input order.** Whether `a < b` works depends on the first iteration swapping the values.
- **Validation.** The type check is extra code beyond the algorithm, and `bool` is a trap because it is an `int`.

These are exactly the places where small functions go wrong, so a few targeted tests are justified.

### Piece by piece

| Piece | Verdict | Reason |
|---|---|---|
| Tests for zero, negative, equal, `a < b` | **Justified** | Each exercises a distinct behavior (see above). |
| Tests for `TypeError` (4) | **Justified, but could be 2** | They cover real code. `float` and `bool` are the two interesting cases; `str` and `None` fail the same `isinstance` check as `float`. |
| Large-integer test (#15) | **Justified, 1 test** | Python has no overflow, so one test is enough evidence. |
| Fibonacci test (#14) | **Mild value** | It shows the worst case for iteration count, but a correctness test with this input adds little over the others. Its value is mostly illustrative. |
| Several similar basic cases (#1, #4, #13) | **Redundant** | They exercise the same path as each other. |
| Hardcoded expected value **and** `math.gcd` | **Partly redundant** | `math.gcd` is already a trusted oracle. The hardcoded value is only a guard against a wrong oracle call, which is very unlikely. Its real benefit is that the output file shows the expected value in a human-readable form. |
| `try`/`except` | **Needed** | It is the only way to test that `TypeError` is raised. It is not "extra" exception handling. |
| PASS/FAIL printing | **Needed for this assignment** | The assignment wants `Results/gcd_output.txt` as evidence. It is not needed for correctness itself. |
| Exit code | **Marginal here** | It matters if something automated runs the script. For a one-off coursework run, an `assert` failing would also stop the script with a nonzero status. |
| Summary line (`19/19 passed`) | **Marginal** | It is convenient, not essential. |

Note that the exit code, the double check and the summary line came from your requirements decisions (Q2 and Q3), so they are intentional. I am not saying they are wrong, only that they add cost relative to the evidence they produce.

### Minimum convincing strategy

The strongest evidence is not a longer list of hand-picked cases. It is **comparison against an oracle over an exhaustive range, plus a few targeted spot checks**:

1. **Exhaustive small range against `math.gcd`.** Check every pair `(a, b)` with `a` and `b` from -30 to 30 (3,721 pairs). That range automatically covers: both zeros, one zero, equal inputs, `a < b` and `a > b`, all four sign combinations, coprime pairs, and one number a multiple of the other. This is far more coverage than 15 hand-picked cases.
2. **One large-integer case**, beyond 64 bits, against `math.gcd`.
3. **One Fibonacci case**, to show the worst-case iteration count terminates correctly.
4. **Two type checks**: `gcd(1.5, 2)` and `gcd(True, 2)` raise `TypeError`.

Roughly:

```python
if __name__ == "__main__":
    import math
    r = range(-30, 31)
    assert all(gcd(a, b) == math.gcd(a, b) for a in r for b in r)
    assert gcd(2**100, 3 * 2**70) == math.gcd(2**100, 3 * 2**70)
    assert gcd(832040, 514229) == 1
    for bad in [(1.5, 2), (True, 2)]:
        try:
            gcd(*bad)
        except TypeError:
            pass
        else:
            raise AssertionError(bad)
    print("all checks passed")
```

That is about ten lines and about 3,725 checks. A failing `assert` already produces a traceback and a nonzero exit status, so no separate summary or `sys.exit` is needed.

### Why that is "convincing"

Evidence of correctness for this function comes from three independent sources, and no single source has to carry all of it:
- **A proof.** Q1 shows the invariant, termination and exit condition, so the algorithm is correct on paper.
- **Exhaustive testing of a small domain.** Every behavior class (sign, zero, order, equal, coprime, multiple) appears many times over, and the outputs are compared with an independent implementation.
- **Spot checks outside that domain.** Large integers and the Fibonacci worst case.

What testing cannot do is prove the function correct for all integers. Even 3,721 pairs cover only a tiny part of the input space. The reason the result is still convincing is that the proof covers the general case, and the tests confirm that the *code* matches the proof in each behavior class.

### How the plan compares

| | Current plan (v2 requirements) | Minimum strategy |
|---|---|---|
| Hand-written test cases | 19 | about 5 |
| Pairs actually checked | 19 | about 3,725 |
| Behavior classes covered | all | all |
| Human-readable evidence file | yes (one line per case) | one line, `all checks passed` |
| Code size | longer (tables, loops, counters, helper logic) | about 10 lines |

The minimum strategy gives stronger evidence of correctness. The current plan gives a more readable evidence file, which is what the assignment's `Results/gcd_output.txt` asks for. Those are different goals.

### Recommendation

- If the output file needs to show individual cases, keep the existing 19 cases but **add the exhaustive range check** as one more line in the output (for example `exhaustive -30..30 (3721 pairs) PASS`). That keeps the readable evidence and adds the strongest test.
- If you would rather simplify, use the minimum strategy above and drop the hardcoded-expected comparison, the per-line counters and the explicit `sys.exit`.

Either way, a change would mean updating `requirements_v2.md` and `design_v1.md`, which you have already approved, so I have not changed them. Which direction do you prefer?

---

## Q3. Why are the 19 tests inside the `__main__` block of `gcd_iterative.py`, when Problems 2, 3 and 4 kept tests in separate files? When would a separate `test_gcd.py` become the better decision?

**Question (as asked):** In Problems 2, 3, and 4, we separated production code from testing. However, for Problem 5, we put all 19 tests inside the __main__ block of gcd_iterative.py. Why is this design appropriate here? At what point would moving the tests into a separate test_gcd.py file become a better engineering decision?

**Response:**

### What the earlier problems looked like

I checked the repository before answering. The earlier problems had real reasons to separate:

| Problem | Production file | Test file | What the tests needed |
|---|---|---|---|
| 2 | `primality.py` (64 lines) | `test_primality.py` (92 lines) | An independent trial-division reference, `Fraction` comparisons, a plain script with its own counters |
| 3 | `random_prime_trials.py` (106 lines) | `test_random_prime_trials.py` (296 lines) | `unittest`, `mock`, `tempfile`, `subprocess`, seeded `random` |
| 4 | `prime_density.py` (148 lines) | `test_prime_density.py` (190 lines) | `unittest`, `tempfile`, CSV file checks |

In each of those, the production code does something with side effects (random draws, writing result files, benchmarking, producing CSV and plots), and the tests need scaffolding that has nothing to do with the production logic: temporary directories, mocks, subprocess calls, a second reference implementation. Putting that into the production file would bury the code you actually want to read, and the tests were as long as or longer than the code under test (up to about 3 times longer in Problem 3).

### Why a single file is appropriate for Problem 5

1. **The function is pure and tiny.** `gcd` is about four lines of algorithm plus validation and a docstring. It does no I/O, uses no randomness, keeps no state and has no dependencies. Nothing needs mocking or fixtures.
2. **The test data is a plain table.** Each test is a tuple `(a, b, expected)`, compared with `math.gcd`. There is no scaffolding to hide. The runner is a short loop (roughly 40 lines for the whole block, versus 92 to 296 lines of test code in the earlier problems; these Problem 5 numbers are my estimate, since nothing is implemented yet).
3. **The assignment treats the test output as a deliverable.** The requirements ask for the `__main__` block to print `gcd(a, b) = result (expected ...) PASS`, so that `Results/gcd_output.txt` is evidence. The requirements also say the deliverable is "a single Python file." Putting the tests next to the function makes the file self-verifying: `python gcd_iterative.py` is the whole workflow.
4. **Importing stays clean.** The tests sit under `if __name__ == "__main__":`, so `from gcd_iterative import gcd` (the Problem 6 use) runs nothing and prints nothing. `math` and `sys` are imported only inside the block, so the core function has no dependency on them. This means the thing the earlier problems protect (production code that is not polluted by test code) is still protected, just by the `__main__` guard instead of by a file boundary.
5. **The decision was deliberate.** It came from your answer to Q14 in the requirements review: the assignment is small enough for a single-file implementation, with a separate test file "unless a genuine need arises." So this is the stated rule, not a gap.

### What this design costs

It is not free, and the downsides are real:
- **No test discovery.** `python -m unittest` and `pytest` will not find these tests. They only run via `python gcd_iterative.py`.
- **No selective runs.** You cannot run one test, or re-run only the failures.
- **First unexpected exception aborts the run.** In the design, a test that raises the wrong exception type crashes the script with a traceback rather than recording a `FAIL` and continuing. A framework would isolate each test.
- **Inconsistency with Problems 2 to 4.** A reader moving between problems has to learn a different layout.
- **Test code ships with the module.** It is inert on import, but the file is longer than the function strictly needs.
- **The `__main__` path itself is not tested.** Nothing checks that, for example, the exit code really is nonzero on failure, except the manual check in the verification plan.

For a four-line pure function these costs are small. They grow as the code grows.

### When a separate `test_gcd.py` becomes the better decision

Move the tests out as soon as **any** of these becomes true:

1. **The module grows.** A second public function, or helper functions, appear (for example `lcm`, or an extended GCD returning Bezout coefficients). The test block then starts to dominate the file, and tests for different functions need to be organized.
2. **The tests need scaffolding.** Fixtures, mocks, temporary files, subprocess calls or seeded randomness. This was the situation in Problems 3 and 4, and it is the clearest signal.
3. **The test code outweighs the production code by a wide margin.** As a rule of thumb, once the `__main__` block is several times longer than the code it tests, a reader opening the file has to scroll past tests to find the implementation. Problem 3's 296 lines of tests for 106 lines of code is that case.
4. **You need unittest or pytest features.** Test discovery, running one test, per-test isolation and failure reporting, parametrization, coverage measurement, or CI that runs `pytest` automatically.
5. **Other code depends on the function.** Problem 6 will import `gcd`. If anything is later changed in `gcd` (or if Problem 6 adds code around it), a test suite that can be run on its own, with its own pass/fail result, is a regression safety net. A script you have to remember to run by hand is weaker.
6. **Tests become slow or heavy.** A test run that takes seconds or longer (for example the exhaustive range check at much larger bounds) should not be tied to running the module itself.
7. **More than one person works on it,** or tests should be excluded when the module is packaged or distributed.
8. **The `__main__` behavior itself needs testing** (exit codes, output format), which is naturally done from the outside by a separate test that runs the script.

### Why moving later is cheap

Because `gcd` is already importable and the test data is a plain table, converting is mechanical:
1. Create `test_gcd.py` with `from gcd_iterative import gcd`.
2. Copy the two tables and the loops, or rewrite them as `unittest` or `pytest` cases (the tables become `subTest` loops or `parametrize`).
3. Delete the test block from `gcd_iterative.py`, leaving only the function.
4. Update the README's run and results-generation commands (the output file would then come from the test script).

So starting with the simple design does not lock anything in. A rule that works: **start with the simplest structure that the current code justifies, and split at the first trigger above.** For Problem 5 none of the triggers is met today.

### Summary

The single-file design is appropriate because the function is pure and tiny, the tests are a plain table without scaffolding, and the assignment wants self-verifying output from one file. It stays appropriate until the module grows, the tests need infrastructure, or other code starts to depend on the function. Problems 2 to 4 each hit one of those triggers from the start, which is why they were split and this one was not.
