"""unittest suite for prime_density.py (standard library only).

Run:  python test_prime_density.py     (also writes Results/test_output.txt)
  or: python -m unittest test_prime_density
"""

import csv
import sys
import tempfile
import unittest
from pathlib import Path

from prime_density import (
    N_MAX,
    N_MIN,
    RESULTS_DIR,
    build_rows,
    count_primes_up_to,
    enumerate_primes_6k,
    format_summary,
    sample_points,
    write_csv,
)


def sieve(n):
    """Independent iterative Sieve of Eratosthenes (verification only)."""
    if n < 2:
        return []
    flags = bytearray([1]) * (n + 1)
    flags[0] = flags[1] = 0
    i = 2
    while i * i <= n:
        if flags[i]:
            flags[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
        i += 1
    return [i for i, f in enumerate(flags) if f]


class TestSmallInputs(unittest.TestCase):
    def test_boundaries_0_to_7(self):
        expected = {
            0: [], 1: [], 2: [2], 3: [2, 3], 4: [2, 3], 5: [2, 3, 5],
            6: [2, 3, 5], 7: [2, 3, 5, 7],
        }
        for n_max, primes in expected.items():
            with self.subTest(n_max=n_max):
                self.assertEqual(enumerate_primes_6k(n_max), primes)

    def test_composites_25_and_35_excluded(self):
        result = enumerate_primes_6k(50)
        self.assertNotIn(25, result)
        self.assertNotIn(35, result)
        self.assertEqual(result, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                                  41, 43, 47])

    def test_matches_sieve_0_to_10000(self):
        for n in range(0, 10_001):
            self.assertEqual(enumerate_primes_6k(n), sieve(n), f"n_max={n}")

    def test_small_lists_strictly_increasing(self):
        for n in (10, 25, 100, 1000):
            primes = enumerate_primes_6k(n)
            self.assertTrue(all(a < b for a, b in zip(primes, primes[1:])))


class TestValidation(unittest.TestCase):
    def test_type_errors(self):
        for bad in (True, False, 2.0, "5", None):
            with self.subTest(value=bad):
                with self.assertRaises(TypeError):
                    enumerate_primes_6k(bad)

    def test_negative_returns_empty(self):
        for n in (-1, -2, -100, -5_000_000):
            with self.subTest(n=n):
                self.assertEqual(enumerate_primes_6k(n), [])


class TestCountHelper(unittest.TestCase):
    def test_below_two_is_zero(self):
        primes = [2, 3, 5, 7]
        for n in (-5, 0, 1):
            self.assertEqual(count_primes_up_to(primes, n), 0)

    def test_counts_around_primes(self):
        primes = [2, 3, 5, 7, 11, 13]
        expected = {2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 10: 4, 11: 5, 12: 5,
                    13: 6, 100: 6}
        for n, count in expected.items():
            with self.subTest(n=n):
                self.assertEqual(count_primes_up_to(primes, n), count)


class TestSampling(unittest.TestCase):
    def test_sample_points(self):
        pts = sample_points()
        self.assertEqual(len(pts), 4996)
        self.assertEqual(pts[0], 5_000)
        self.assertEqual(pts[-1], 5_000_000)
        self.assertEqual(pts[1] - pts[0], 1_000)


class TestFullRange(unittest.TestCase):
    """Tests that share one enumeration up to 5,000,000 (computed once)."""

    @classmethod
    def setUpClass(cls):
        cls.primes = enumerate_primes_6k(N_MAX)

    def test_known_values(self):
        self.assertEqual(count_primes_up_to(self.primes, 5_000), 669)
        self.assertEqual(count_primes_up_to(self.primes, 5_000_000), 348_513)
        self.assertEqual(len(self.primes), 348_513)

    def test_strictly_increasing_no_duplicates(self):
        self.assertTrue(all(a < b for a, b in zip(self.primes, self.primes[1:])))
        self.assertEqual(len(set(self.primes)), len(self.primes))

    def test_matches_sieve_on_full_range(self):
        self.assertEqual(self.primes, sieve(N_MAX))

    def test_build_rows(self):
        rows = build_rows(self.primes)
        self.assertEqual(len(rows), 4996)
        for n, count, pct in rows[:50] + rows[-50:]:
            self.assertEqual(count, count_primes_up_to(self.primes, n))
            self.assertEqual(pct, count / (n + 1) * 100)
        self.assertEqual(rows[0][:2], (5_000, 669))
        self.assertEqual(rows[-1][:2], (5_000_000, 348_513))

    def test_csv_round_trip(self):
        rows = build_rows(self.primes)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prime_density.csv"
            write_csv(rows, path)
            with open(path, newline="", encoding="utf-8") as f:
                read = list(csv.reader(f))
        self.assertEqual(read[0], ["N", "prime_count", "prime_percentage"])
        self.assertEqual(len(read) - 1, 4996)
        for (n, count, pct), line in zip(rows, read[1:]):
            self.assertEqual(int(line[0]), n)
            self.assertEqual(int(line[1]), count)
            self.assertEqual(float(line[2]), pct)  # exact: repr round-trips

    def test_summary_text(self):
        text = format_summary(self.primes, 1.5, 2.25)
        self.assertIn("pi(5,000) = 669", text)
        self.assertIn("pi(5,000,000) = 348,513", text)
        self.assertIn("100/ln(5,000)", text)
        self.assertIn("100/ln(5,000,000)", text)
        self.assertIn("348,513", text)
        self.assertIn("Prime-enumeration time: 1.500 s", text)
        self.assertIn("excludes summary writing): 2.250 s", text)


class _Tee:
    """Write to several text streams at once."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)

    def flush(self):
        for s in self.streams:
            s.flush()


def run_and_save():
    """Run all tests, save Results/test_output.txt (UTF-8), return exit status."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    with open(RESULTS_DIR / "test_output.txt", "w", encoding="utf-8") as f:
        tee = _Tee(sys.stdout, f)
        result = unittest.TextTestRunner(stream=tee, verbosity=2).run(suite)
        executed = result.testsRun
        failed = len(result.failures) + len(result.errors)
        skipped = len(result.skipped)
        passed = executed - failed - skipped
        tee.write(
            f"\nTests executed: {executed}\nPassed: {passed}\nFailed: {failed}\n"
        )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_and_save())
