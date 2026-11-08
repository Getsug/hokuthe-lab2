
## Trade-off: validating prime existence vs. preserving the original experiment (Q10)

**The problem.** `expected_draws` loops until it draws a prime. If the interval `[lo, hi]` contains no prime (for example `[24, 28]`, or `lo == hi == 9`), the inner loop never ends. Requirement 17 currently handles this by assuming the caller supplies a valid interval.

**Option 1: do nothing (current v1).**
- Keeps the procedure in requirement 7 exactly as written.
- Adds no extra `is_prime` calls and no extra logic.
- A bad interval hangs the program, with no error and no message.
- The two required runs both contain many primes, so they are safe. The risk only appears if someone reuses the function with other bounds.

**Option 2: cap the draws per trial (for example, raise an error after N draws).**
- It guarantees termination.
- It changes the experiment. The procedure says "loop forever", and a cap makes the loop bounded.
- Choosing N is arbitrary. If N is too small, a legitimate but unlucky trial gets rejected. If N is too large, the cap protects nothing.
- It does not prove that no prime exists. It only shows that none was found after N draws.
- I don't recommend it. It conflicts most directly with "implement exactly as written".

**Option 3: a one-time precondition check before the trials begin.**
Scan the interval from `lo` upward with `is_prime` and stop at the first prime. If the scan reaches `hi` without finding one, raise `ValueError`.
- It runs once per call, not once per trial, and it never touches `rng`.
- Because it does not use `rng`, the draw sequence, the counts and the reproducibility with seed 12345 are all unchanged.
- The trial procedure in requirement 7 stays exactly as written. The check is a separate step before it.
- It is cheap in practice. Primes are dense enough (about 1 in 16 near 5.5M, about 1 in 28 near 500B) that the scan stops after a few dozen calls.
- The worst case is a long interval with no primes, which needs a full scan. In the opposite case, a short prime-free interval fails fast, and that is where the check is most useful.
- It adds `is_prime` calls outside the procedure. If a test counts `is_prime` calls to verify "1000 searches", the check inflates the count. Tests should count draws through a wrapped `rng`, or the check should be excluded from the count.
- With a fake `rng` that returns a fixed sequence (such as `4, 6, 8, 11`), the `lo`/`hi` passed to the test must contain a prime, or the check will reject the test inputs.
- The check also costs a few lines of code and a few more tests, and it must be written carefully so that it does not recurse or reimplement primality logic.

**What the choice really trades.**
- Strict fidelity to the written procedure keeps the experiment unchanged, but it leaves the function able to hang.
- Safety needs extra behaviour. Option 2 puts that behaviour inside the experiment and distorts it. Option 3 keeps it outside, so the experiment is unchanged and only the failure mode improves.

**Recommendation.** Option 3. It protects against the hang and leaves the measured result untouched. The cost is a handful of extra `is_prime` calls and a documented rule about how tests count calls. If you want the smallest possible change from v1, Option 1 is acceptable, as long as the README states the assumption clearly.

## Why the expected number of draws is about ln(N), why it grows with N, and why experiments differ from theory

### 1. Why the expected number of draws is about ln(N)

**Step 1: the draws form a geometric process.** Each draw is uniform on the interval, independent of the others, and with replacement. Let p be the fraction of integers in the interval that are prime. Every draw is then prime with the same probability p, independently. The number of draws up to and including the first prime, X, is geometric:

$$P(X = k) = (1-p)^{k-1}\,p, \qquad k = 1, 2, 3, \dots$$

Its mean is

$$E[X] = \sum_{k\ge 1} k\,(1-p)^{k-1}\,p = \frac{1}{p}.$$

This step is exact. The counting rule in requirement 7 (the successful prime draw is counted) is what makes the mean $1/p$ instead of $1/p - 1$.

**Step 2: the Prime Number Theorem gives p.** The theorem says the number of primes up to $x$ satisfies

$$\pi(x) \sim \frac{x}{\ln x}.$$

Differentiating, the density of primes near $x$ is $1/\ln x$. For an interval $[lo, hi]$ that is short compared with its position, $\ln x$ barely changes across it, so

$$p \approx \frac{1}{\ln m}, \qquad m = \frac{lo + hi}{2}.$$

More precisely, $p = \dfrac{\pi(hi) - \pi(lo - 1)}{hi - lo + 1}$, and the theorem says this is close to $\dfrac{1}{\ln m}$ when the interval is short relative to $m$.

**Step 3: combine.**

$$E[X] = \frac{1}{p} \approx \ln m.$$

This is the prediction printed for each run, which is why requirement 9 uses `math.log(midpoint)`.

**Heuristic behind the density.** Among integers near $x$, a random one is divisible by a prime $q$ with probability $1/q$. The chance of escaping every prime $q \le \sqrt{x}$ is about $\prod_{q\le\sqrt{x}}(1 - 1/q)$. Mertens' theorem gives this product as about $\dfrac{e^{-\gamma}}{\ln\sqrt{x}} = \dfrac{2e^{-\gamma}}{\ln x}$. The constant $2e^{-\gamma} \approx 1.12$ is not 1 only because the independence assumption is a heuristic. The true density is $1/\ln x$.

### 2. Why 500 billion needs more draws than 5.5 million

Primes thin out logarithmically. Since $\ln$ is increasing, a larger $N$ means a smaller density $1/\ln N$ and therefore a larger mean $\ln N$:

| Interval | Midpoint | $\ln(\text{midpoint})$ | Density $1/\ln$ |
|---|---|---|---|
| Run A (5,000,000 to 6,000,000) | 5,500,000 | 15.52 | about 6.4% (1 in 15.5) |
| Run B (500,000,000,000 to 500,001,000,000) | 500,000,500,000 | 26.94 | about 3.7% (1 in 26.9) |

The midpoint of Run B is about $9 \times 10^4$ times that of Run A, but $\ln$ grows slowly, so the number of draws rises only from about 15.5 to about 26.9, a factor of about 1.7. The cause is that large numbers have more possible divisors below their square root, so a smaller share of them survive. Multiplying $N$ by $e$ adds only 1 to the expected draws.

### 3. Why the experimental averages differ from the predictions

**a. Sampling noise (the largest effect).** The result is a mean of `trials` independent geometric variables. Each has variance $\dfrac{1-p}{p^2}$, so the standard deviation of one trial is about $\sqrt{1-p}/p \approx \ln m$. The standard error of the average over $T$ trials is therefore about $\dfrac{\ln m}{\sqrt{T}}$:

| Run | Trials | Standard error |
|---|---|---|
| A | 1000 | about 0.47 |
| B | 250 | about 1.67 |

So an empirical average within about one standard error of the prediction (roughly 15.0 to 16.0 for Run A, 25.3 to 28.6 for Run B) is normal, and about 1 run in 20 would fall outside two standard errors. Run B has fewer trials and a larger mean, so it is noisier, and a gap of 1 to 2 draws there does not signal a problem. Because both runs use seed 12345, they are reproducible, but the particular numbers are still one random sample, not a more accurate one.

**b. The prime number theorem is asymptotic.** $\pi(x) \sim x/\ln x$ has a relative error that falls slowly. The estimate $1/\ln x$ is not exact at finite $x$. A better approximation of the density is $1/\ln x$ with a small correction, since $\mathrm{li}(x)$ approximates $\pi(x)$ better than $x/\ln x$.

**c. The density varies across the interval.** The theory uses the midpoint. The true value is the average density over the interval, which in expectation is slightly different from $1/\ln m$ because $1/\ln x$ is convex. For these intervals the effect is tiny (Run A's range is about 18% of its midpoint, Run B's is 0.0002%).

**d. Actual prime counts differ from the smooth estimate.** The real number of primes in an interval fluctuates around the PNT estimate in an irregular way. I checked Run A with a sieve: $[5{,}000{,}000,\ 6{,}000{,}000]$ contains exactly 64,336 primes, so $p = 64{,}336 / 1{,}000{,}001 \approx 0.06434$ and the exact expected number of draws is $1/p \approx 15.54$, against the prediction of 15.52. The prediction is good, but even the exact value is not exactly $\ln m$. For Run B the exact count is not known without a very large sieve.

**e. Averages of geometric variables are skewed.** The distribution of a single trial has a long right tail (a trial of 80 or more draws happens occasionally). With 250 trials, one or two long trials can raise the mean by more than a draw. The mean is unbiased, but its distribution is not symmetric, so a gap in one direction is somewhat more likely to be large.

**f. Implementation points that do not cause differences.**
- The pre-validation scan (requirement 18) uses no random numbers, so it does not shift results.
- Counting the successful draw is required for the mean to equal $1/p$. Excluding it would bias the average down by exactly 1.
- Drawing with replacement keeps the geometric model exact. Drawing without replacement would slightly shorten the search.

### 4. How to judge the results

Compare the gap with the standard error, not with zero. For a stronger check, the optional standard error from requirement 20 would show whether the gap is within about 2 standard errors. To distinguish sampling noise from a systematic gap, increase the number of trials. The standard error shrinks as $1/\sqrt{T}$, so 100 times more trials gives 10 times less noise, while a systematic gap would remain.
