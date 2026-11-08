# Observations: percentage of primes in [0, N], N = 5,000 to 5,000,000

All numbers come from `Results/prime_density.csv`, `Results/summary.txt` and the graph `Results/prime_density.png`, produced by one run of `prime_density.py` (Python 3.14.7, matplotlib 3.11.2). The percentage is π(N)/(N+1) × 100.

## Observations

1. **The percentage of primes falls as N grows, steeply at first and then slowly.** It is 13.3773% at N = 5,000 (669 primes), 9.5919% at N = 100,000, 7.8498% at N = 1,000,000 and 6.9703% at N = 5,000,000 (348,513 primes). Most of the drop happens early: from N = 5,000 to N = 100,000 the percentage falls by 3.79 points, but from N = 1,000,000 to N = 5,000,000 it falls by only 0.88 points, even though N grows five-fold.
2. **The drop is not strictly monotone at the 1,000-step sampling level.** Overall the curve decreases, but the percentage rose between consecutive samples in 777 of the 4,995 steps. The smallest percentage in the sampled data is at N = 4,999,000 (6.970233%), slightly below the value at N = 5,000,000 (6.970259%). These small reversals happen when a 1,000-wide block contains more primes than the current average density predicts.
3. **The number of primes keeps increasing while their share decreases.** The prime count rises at every sample, from 669 to 348,513. The number of new primes per 1,000-step shrinks, from 114 between N = 5,000 and N = 6,000 to 71 between N = 4,999,000 and N = 5,000,000. The count of primes grows more slowly than N itself, which is why the percentage falls.
4. **The data follows the Prime Number Theorem's trend, π(N)/N ≈ 1/ln N, but 100/ln(N) underestimates the measured percentage at every sampled N.** At N = 5,000 the measured value is 13.3773% against 11.7410% from 100/ln(N), a ratio of 1.139. At N = 5,000,000 it is 6.9703% against 6.4830%, a ratio of 1.075. The absolute gap shrinks from 1.64 points to 0.49 points, and the ratio falls from 1.139 to 1.075, so the approximation gets relatively closer as N grows. Both curves decrease with the same overall shape on the graph. The sampled gap never goes below 0.487 points.
5. **Efficiency of the 6k±1 approach.** Generating only 6k±1 candidates removes about two-thirds of the calls to `is_prime`, but the removed calls are the cheap ones that `is_prime` rejects immediately as multiples of 2 or 3. In a separate ad-hoc comparison (see `interrogation.md`, round 4) over N = 100,000 to 800,000, the speedup was only about 1.01× to 1.12× and it shrank as N grew. The runtime is dominated by the trial division that `is_prime` performs for primes and for composites whose smallest factor is large. In this run the enumeration up to 5,000,000 took 47.759 s and the full processing took 57.713 s. The 6k±1 scheme is therefore a small constant-factor saving and does not change the O(N^1.5 / ln N) cost.

## Your interpretation

*(To be added by the user.)*
