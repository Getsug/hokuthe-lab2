"""Prime density: percentage of primes in [0, N] for N = 5,000 .. 5,000,000.

Primes are enumerated once with the 6k-1 / 6k+1 scheme (Problem 1), using the
unchanged is_prime() from problem2/primality.py (Problem 2). Each pi(N) is then
read from that single sorted list with bisect_right.
"""

import csv
import math
import sys
import time
from bisect import bisect_right
from pathlib import Path

PROBLEM_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROBLEM_DIR / "Results"
PROBLEM2_DIR = PROBLEM_DIR.parent / "problem2"

sys.path.insert(0, str(PROBLEM2_DIR))
from primality import is_prime  # noqa: E402  (reused unchanged from Problem 2)

N_MIN = 5_000
N_MAX = 5_000_000
N_SAMPLE_STEP = 1_000

CSV_HEADER = ["N", "prime_count", "prime_percentage"]


def enumerate_primes_6k(n_max):
    """Return a strictly increasing list of all primes <= n_max (6k+/-1 scheme)."""
    if isinstance(n_max, bool) or not isinstance(n_max, int):
        raise TypeError(
            f"enumerate_primes_6k() requires an int, got {type(n_max).__name__}"
        )
    if n_max < 2:
        return []
    if n_max == 2:
        return [2]
    if n_max <= 4:
        return [2, 3]

    # 2 and 3 are never of the form 6k+/-1 for k >= 1, so they are seeded here.
    primes = [2, 3]
    k = 1
    while True:
        a = 6 * k - 1
        b = 6 * k + 1
        if a > n_max and b > n_max:
            break
        if a <= n_max and is_prime(a):
            primes.append(a)
        if b <= n_max and is_prime(b):
            primes.append(b)
        k += 1
    # a < b < next a, so the list is already strictly increasing: no sort.
    return primes


def count_primes_up_to(primes, n):
    """Return pi(n), the number of primes <= n. `primes` must be sorted ascending."""
    if n < 2:
        return 0
    return bisect_right(primes, n)


def sample_points():
    """Return the sampled N values: 5,000 .. 5,000,000 inclusive, step 1,000."""
    return range(N_MIN, N_MAX + 1, N_SAMPLE_STEP)


def build_rows(primes):
    """Return [(N, prime_count, prime_percentage), ...] for every sampled N."""
    rows = []
    for n in sample_points():
        count = count_primes_up_to(primes, n)
        rows.append((n, count, count / (n + 1) * 100))
    return rows


def write_csv(rows, path):
    """Write rows to a CSV file with header N,prime_count,prime_percentage."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(CSV_HEADER)
        writer.writerows(rows)


def save_plot(rows, path):
    """Plot measured prime percentage and 100/ln(N); save as a 150 dpi PNG."""
    import matplotlib

    matplotlib.use("Agg")  # headless; must precede the pyplot import
    import matplotlib.pyplot as plt

    xs = [r[0] for r in rows]
    measured = [r[2] for r in rows]
    theory = [100 / math.log(n) for n in xs]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(xs, measured, linestyle="-", label=r"Measured: $\pi(N)/(N+1)\times 100$")
    ax.plot(xs, theory, linestyle="--", label=r"Theoretical approximation: $100/\ln(N)$")
    ax.set_title("Percentage of primes in [0, N] as N increases")
    ax.set_xlabel("N (upper bound)")
    ax.set_ylabel("Percentage of integers in [0, N] that are prime (%)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def format_summary(primes, enum_time, processing_time):
    """Return the summary text (percentages: 4 decimals, times: 3 decimals)."""
    lines = []
    for n in (N_MIN, N_MAX):
        count = count_primes_up_to(primes, n)
        pct = count / (n + 1) * 100
        lines.append(f"pi({n:,}) = {count:,}")
        lines.append(f"pi({n:,})/({n + 1:,}) x 100 = {pct:.4f}%")
        lines.append(f"100/ln({n:,}) = {100 / math.log(n):.4f}%")
    lines.append(f"Total primes found up to {N_MAX:,}: {len(primes):,}")
    lines.append(f"Prime-enumeration time: {enum_time:.3f} s")
    lines.append(
        f"Total processing time (enumeration, checkpoints, CSV, graph; "
        f"excludes summary writing): {processing_time:.3f} s"
    )
    return "\n".join(lines) + "\n"


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    t_start = time.perf_counter()
    primes = enumerate_primes_6k(N_MAX)  # enumerated once
    enum_time = time.perf_counter() - t_start

    rows = build_rows(primes)
    write_csv(rows, RESULTS_DIR / "prime_density.csv")
    save_plot(rows, RESULTS_DIR / "prime_density.png")
    processing_time = time.perf_counter() - t_start

    summary = format_summary(primes, enum_time, processing_time)
    print(summary, end="")
    (RESULTS_DIR / "summary.txt").write_text(summary, encoding="utf-8")


if __name__ == "__main__":
    main()
