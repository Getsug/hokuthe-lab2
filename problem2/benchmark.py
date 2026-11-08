"""Timing of primality.is_prime on large inputs (measurement only).

Each input is run 5 times; median, min and max are reported in milliseconds.
The result is checked against the expected value before timing.
"""

import platform
import statistics
import sys
import time

from primality import is_prime

RUNS = 5
# (n, expected, description)
INPUTS = [
    (999999999989, True, "large prime"),
    (999966000289, False, "999983**2, prime square"),
    (999999999745, False, "5 * 199999999949, factor 5 found last"),
    (1000000000000, False, "even, exits at step d"),
]

print(f"Python:   {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Runs per input: {RUNS}")
print()
print(f"{'n':>15}  {'result':<6}  {'median ms':>10}  {'min ms':>10}  {'max ms':>10}  description")

for n, expected, description in INPUTS:
    result = is_prime(n)  # also serves as warm-up
    if result != expected:
        sys.exit(f"is_prime({n}) returned {result}, expected {expected}; not timing")
    times = []
    for _ in range(RUNS):
        start = time.perf_counter()
        is_prime(n)
        times.append((time.perf_counter() - start) * 1000)
    print(f"{n:>15}  {str(result):<6}  {statistics.median(times):>10.3f}  "
          f"{min(times):>10.3f}  {max(times):>10.3f}  {description}")
