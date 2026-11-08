# Problem 7: Totient Identity Verification

## Objective
Verify, by direct computation, that $\phi(pq) = (p-1)(q-1)$ for distinct primes $p$ and $q$ between 2000 and 3000 (inclusive). The totient is computed by the GCD-counting `euler_totient()` from Problem 6 and compared with the formula. The formula never replaces the computation.

## Mathematics
- For a prime $p$, every integer in $1..p-1$ is coprime to $p$, so $\phi(p) = p-1$.
- $\phi$ is multiplicative on coprime arguments. Distinct primes are coprime, so $\phi(pq) = \phi(p)\phi(q) = (p-1)(q-1)$.
- For equal primes the identity does not apply: $\phi(p^2) = p(p-1)$, not $(p-1)^2$. The program shows this with the rejected pair `(2011, 2011)`.

## Algorithm
`verify_totient_identity(pairs)` validates the whole batch first (fail fast, no partial results), then for each `(p, q)` computes `n = p*q`, `phi_pq = euler_totient(n)`, `expected = (p-1)*(q-1)` and `matches = (phi_pq == expected)`. It returns a list of dicts with keys `p`, `q`, `pq`, `phi_pq`, `expected`, `matches`.

Validation order: `pairs` is a list (`TypeError`); each element is a tuple (`TypeError`) of length 2 (`ValueError`); values are `int`, not `bool` (`TypeError`); values are in 2000..3000 (`ValueError`); values are prime via `is_prime` (`ValueError`); `p != q` (`ValueError("p and q must be distinct primes")`); no duplicate or reversed combination in the batch (`ValueError`).

`main()` runs the primary pair `(2003, 2011)`, four more pairs `(2017, 2027)`, `(2029, 2039)`, `(2081, 2083)`, `(2969, 2999)`, and the equal-prime contrast case `(2011, 2011)`. The contrast case is outside the table and the PASS/FAIL summary.

## Dependencies
- Problem 2: `is_prime` from `problem2/primality.py`.
- Problem 6: `euler_totient` from `problem6/euler_totient.py`, which in turn uses the iterative `gcd` from Problem 5.

They are imported unchanged, with directories resolved relative to `__file__`, so the program works from any working directory. Standard library only. No recursion.

## Running
```
python problem7/verify_totient.py
```
Exit status is 0 on PASS and 1 if any comparison fails or the run cannot complete.

## Testing
```
cd problem7
python -m unittest test_verify_totient -v
```
Most tests patch `euler_totient` with a stub (`autospec=True`, hand-derived literal values, assertions on the `p*q` argument), because every valid in-range pair costs millions of GCD calls. These tests check logic, not mathematics. The mathematics is checked by:
- `test_integration_primary_pair_slow`: real, unpatched run of `(2003, 2011)`.
- `test_small_semiprime`: real `euler_totient(15) == 8`. This checks the underlying totient function only, not the Problem 7 workflow, because the 2000..3000 range rejects 3 and 5.
- The full real five-pair run of `verify_totient.py` (below).

## Output
`Results/totient_verification.txt` (created automatically, overwritten each run) contains the primary pair, the results table, per-pair and total timings, the contrast-case note, the conclusion, and a final line `All distinct-prime cases verified: PASS` (or `FAIL`). The same text is printed to stdout.

## Results and runtime
Measured on Python 3.14.7, Windows 11:

| Pair | `pq` | phi(pq) | (p-1)(q-1) | match | time |
|---|---|---|---|---|---|
| (2003, 2011) | 4028033 | 4024020 | 4024020 | True | 1.682 s |
| (2017, 2027) | 4088459 | 4084416 | 4084416 | True | 1.773 s |
| (2029, 2039) | 4137131 | 4133064 | 4133064 | True | 1.802 s |
| (2081, 2083) | 4334723 | 4330560 | 4330560 | True | 1.847 s |
| (2969, 2999) | 8904031 | 8898064 | 8898064 | True | 3.904 s |

Total: 11.008 s. The unit test suite (19 tests, including the real `(2003, 2011)` run) takes about 1.7 s. Times vary by machine.

## Known limitations
- `euler_totient` is O(n log n) in the product, so it is slow for much larger primes. The range is fixed at 2000..3000.
- `pairs` must be a list of 2-tuples of `int`.
- Per-pair timing includes that pair's (cheap) validation.
- Python 3.14.7 is the development version and is not enforced at runtime.
