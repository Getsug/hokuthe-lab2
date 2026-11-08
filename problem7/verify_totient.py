"""Verify phi(pq) = (p-1)(q-1) for distinct primes p, q in 2000..3000.

Reuses is_prime (Problem 2) and euler_totient (Problem 6) unchanged.
"""

import sys
from pathlib import Path
from time import perf_counter

_ROOT = Path(__file__).resolve().parent.parent
for _d in ("problem2", "problem6"):
    sys.path.insert(0, str(_ROOT / _d))
from primality import is_prime  # noqa: E402
from euler_totient import euler_totient  # noqa: E402

LOW = 2000
HIGH = 3000
PRIMARY_PAIR = (2003, 2011)
ADDITIONAL_PAIRS = [(2017, 2027), (2029, 2039), (2081, 2083), (2969, 2999)]
CONTRAST_PAIR = (2011, 2011)
DISTINCT_MSG = "p and q must be distinct primes"
RESULTS_PATH = Path(__file__).resolve().parent / "Results" / "totient_verification.txt"

CONCLUSION = (
    "Conclusion: for distinct primes p and q, phi(p) = p - 1 and phi(q) = q - 1, "
    "and phi is multiplicative on coprime arguments, so phi(pq) = (p-1)(q-1). "
    "Every computed value above agrees with this formula."
)


def _validate_pairs(pairs):
    """Validate the whole batch; raise TypeError/ValueError on the first problem."""
    if not isinstance(pairs, list):
        raise TypeError(f"pairs must be a list, got {type(pairs).__name__}")
    seen = set()
    for pair in pairs:
        if not isinstance(pair, tuple):
            raise TypeError(
                f"each pair must be a tuple, got {type(pair).__name__}: {pair!r}"
            )
        if len(pair) != 2:
            raise ValueError(f"each pair must have exactly 2 elements, got {pair!r}")
        for value in pair:
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(
                    f"pair {pair!r}: values must be int, got {type(value).__name__}"
                )
        for value in pair:
            if not LOW <= value <= HIGH:
                raise ValueError(
                    f"pair {pair!r}: {value} is outside {LOW}..{HIGH}"
                )
        for value in pair:
            if not is_prime(value):
                raise ValueError(f"pair {pair!r}: {value} is not prime")
        p, q = pair
        if p == q:
            raise ValueError(f"pair {pair!r}: {DISTINCT_MSG}")
        key = frozenset(pair)
        if key in seen:
            raise ValueError(f"pair {pair!r}: duplicate combination in batch")
        seen.add(key)


def verify_totient_identity(pairs):
    """Return one result dict per (p, q) pair comparing phi(pq) with (p-1)(q-1)."""
    _validate_pairs(pairs)
    results = []
    for p, q in pairs:
        n = p * q
        phi_pq = euler_totient(n)
        expected = (p - 1) * (q - 1)
        results.append({
            "p": p, "q": q, "pq": n, "phi_pq": phi_pq,
            "expected": expected, "matches": phi_pq == expected,
        })
    return results


def _format_report(records, timings, total, contrast_note):
    """Build the full report text; the last line is the PASS/FAIL summary."""
    p0, q0 = records[0]["p"], records[0]["q"]
    lines = [f"Primary pair: p = {p0}, q = {q0}", ""]
    lines.append(
        f"{'p':>6}  {'q':>6}  {'pq':>10}  {'phi(pq)':>10}  "
        f"{'(p-1)(q-1)':>10}  {'match?':>6}"
    )
    for r in records:
        lines.append(
            f"{r['p']:>6}  {r['q']:>6}  {r['pq']:>10}  {r['phi_pq']:>10}  "
            f"{r['expected']:>10}  {str(r['matches']):>6}"
        )
    lines += ["", "Timing (euler_totient, perf_counter):"]
    for r, t in zip(records, timings):
        lines.append(f"  ({r['p']}, {r['q']}): {t:.3f} s")
    lines.append(f"  Total: {total:.3f} s")
    lines += ["", contrast_note, "", CONCLUSION]
    status = "PASS" if all(r["matches"] for r in records) else "FAIL"
    lines.append(f"All distinct-prime cases verified: {status}")
    return "\n".join(lines) + "\n"


def _contrast_note():
    """Run the equal-prime contrast case and return its explanatory note."""
    try:
        verify_totient_identity([CONTRAST_PAIR])
    except ValueError as exc:
        if DISTINCT_MSG not in str(exc):
            raise
    else:
        raise RuntimeError("contrast case unexpectedly succeeded")
    p = CONTRAST_PAIR[0]
    return (
        f"Contrast case (not in table): {CONTRAST_PAIR} is rejected because the "
        f"primes are not distinct. For p = q, phi(p^2) = p(p-1) = {p * (p - 1)}, "
        f"not (p-1)^2 = {(p - 1) ** 2}."
    )


def main():
    """Run the experiment, print and save the report; return the exit status."""
    try:
        pairs = [PRIMARY_PAIR, *ADDITIONAL_PAIRS]
        _validate_pairs(pairs)
        records, timings = [], []
        start_total = perf_counter()
        for pair in pairs:
            t0 = perf_counter()
            records.append(verify_totient_identity([pair])[0])
            timings.append(perf_counter() - t0)
        total = perf_counter() - start_total
        report = _format_report(records, timings, total, _contrast_note())
        RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULTS_PATH.write_text(report, encoding="utf-8")
        print(report, end="")
        return 0 if all(r["matches"] for r in records) else 1
    except Exception as exc:  # noqa: BLE001
        print(f"Experiment failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
