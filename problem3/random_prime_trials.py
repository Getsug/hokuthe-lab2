"""Monte Carlo estimate of how many random draws are needed to hit a prime.

Draws are uniform on an inclusive interval [lo, hi]. The empirical average
number of draws per prime is compared with the Prime Number Theorem
prediction ln(midpoint). Primality testing reuses Problem 2's is_prime,
imported unchanged from problem2/primality.py.
"""

import math
import random
import sys
import time
from pathlib import Path

# Resolve problem2/ relative to this file, not the working directory.
PROBLEM2_DIR = Path(__file__).resolve().parent.parent / "problem2"
sys.path.insert(0, str(PROBLEM2_DIR))
from primality import is_prime  # noqa: E402  (path must be set first)

SEED = 12345
RESULTS_DIR = Path(__file__).resolve().parent / "Results"

# (label, lo, hi, trials)
RUNS = [
    ("Run A", 5_000_000, 6_000_000, 1000),
    ("Run B", 500_000_000_000, 500_000_000_000 + 1_000_000, 250),
]


def expected_draws(lo, hi, trials, rng):
    """Return the average number of draws needed to find a prime.

    Draws x = rng.randint(lo, hi) (inclusive, with replacement) until
    is_prime(x) is True, counting the successful draw, and repeats this
    `trials` times.

    Raises TypeError for wrong argument types (bool is rejected for the
    integer arguments) and ValueError for lo < 2, lo > hi, trials < 1, or
    an interval that contains no prime.
    """
    # Type checks first.
    for name, value in (("lo", lo), ("hi", hi), ("trials", trials)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if not isinstance(rng, random.Random):
        raise TypeError(f"rng must be a random.Random, got {type(rng).__name__}")

    # Then value checks.
    if lo < 2:
        raise ValueError(f"lo must be >= 2, got {lo}")
    if lo > hi:
        raise ValueError(f"lo must be <= hi, got lo={lo}, hi={hi}")
    if trials < 1:
        raise ValueError(f"trials must be a positive integer, got {trials}")

    # Precondition: the interval must contain a prime (otherwise the search
    # would never end). Runs once, stops at the first prime, never uses rng.
    for candidate in range(lo, hi + 1):
        if is_prime(candidate):
            break
    else:
        raise ValueError(f"interval [{lo}, {hi}] contains no prime")

    # Sampling procedure (requirement 7).
    total = 0
    for _ in range(trials):
        count = 0
        while True:
            x = rng.randint(lo, hi)
            count += 1
            if is_prime(x):
                break
        total += count
    return total / trials


def main(runs=RUNS, results_dir=RESULTS_DIR):
    """Run the experiments, print the results and save them to averages.txt."""
    lines = []
    total_start = time.perf_counter()
    for label, lo, hi, trials in runs:
        rng = random.Random(SEED)  # separate generator per run
        start = time.perf_counter()
        average = expected_draws(lo, hi, trials, rng)
        elapsed = time.perf_counter() - start
        theory = math.log((lo + hi) / 2)
        line = (
            f"{label}: lo={lo:,} hi={hi:,} trials={trials} seed={SEED} | "
            f"empirical={average:.2f} | theoretical={theory:.2f} | "
            f"time={elapsed:.3f} s"
        )
        print(line, flush=True)
        lines.append(line)
    total_line = f"Total time: {time.perf_counter() - total_start:.3f} s"
    print(total_line)
    lines.append(total_line)

    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "averages.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
