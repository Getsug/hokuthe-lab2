"""unittest tests for random_prime_trials.expected_draws and main."""

import json
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import random_prime_trials as rpt  # noqa: E402
from random_prime_trials import expected_draws  # noqa: E402


class ScriptedRandom(random.Random):
    """Returns a predetermined sequence from randint and records every call.

    Raises AssertionError if the sequence is exhausted (never cycles).
    """

    def __init__(self, sequence):
        super().__init__(0)
        self.sequence = list(sequence)
        self.calls = []

    def randint(self, a, b):
        if len(self.calls) >= len(self.sequence):
            raise AssertionError("scripted sequence exhausted")
        value = self.sequence[len(self.calls)]
        self.calls.append((a, b, value))
        return value


class RecordingRandom(random.Random):
    """Real seeded randint that records every value it returns."""

    def __init__(self, seed):
        super().__init__(seed)
        self.draws = []

    def randint(self, a, b):
        value = super().randint(a, b)
        self.draws.append(value)
        return value


class CountingLogic(unittest.TestCase):
    def test_four_draws(self):
        rng = ScriptedRandom([4, 6, 8, 11])
        self.assertEqual(expected_draws(4, 11, 1, rng), 4)
        self.assertEqual(len(rng.calls), 4)

    def test_two_trials_sum(self):
        # trial 1: 4, 6, 8, 11 (4 draws); trial 2: 7 (1 draw) -> 5 / 2
        rng = ScriptedRandom([4, 6, 8, 11, 7])
        self.assertEqual(expected_draws(4, 11, 2, rng), 2.5)
        self.assertEqual(len(rng.calls), 5)

    def test_minimal_intervals(self):
        self.assertEqual(expected_draws(2, 2, 1, ScriptedRandom([2, 2])), 1)
        self.assertEqual(expected_draws(3, 3, 1, ScriptedRandom([3, 3])), 1)

    def test_single_prime_multiple_trials(self):
        rng = ScriptedRandom([7, 7, 7])
        self.assertEqual(expected_draws(7, 7, 3, rng), 1)

    def test_sequence_exhaustion_raises(self):
        with self.assertRaises(AssertionError):
            expected_draws(4, 11, 1, ScriptedRandom([4, 6, 8]))

    def test_randint_receives_interval_bounds(self):
        rng = ScriptedRandom([11])
        expected_draws(4, 11, 1, rng)
        self.assertEqual(rng.calls, [(4, 11, 11)])


class IntervalPrimeCheck(unittest.TestCase):
    def test_single_prime_value_average_exactly_one(self):
        self.assertEqual(expected_draws(13, 13, 5, random.Random(1)), 1)

    def test_single_composite_value_raises(self):
        rng = ScriptedRandom([9])
        with self.assertRaises(ValueError):
            expected_draws(9, 9, 1, rng)
        self.assertEqual(rng.calls, [])

    def test_prime_only_at_hi_passes(self):
        # 24..29 contains only the prime 29, at the upper end.
        rng = ScriptedRandom([28, 29])
        self.assertEqual(expected_draws(24, 29, 1, rng), 2)

    def test_prime_free_intervals_raise_without_using_rng(self):
        for lo, hi in ((24, 28), (90, 96)):
            with self.subTest(lo=lo, hi=hi):
                rng = ScriptedRandom([lo])
                with self.assertRaises(ValueError) as ctx:
                    expected_draws(lo, hi, 1, rng)
                self.assertIn(f"[{lo}, {hi}]", str(ctx.exception))
                self.assertEqual(rng.calls, [])

    def test_check_does_not_consume_rng(self):
        # Compare with a hand-written copy of the plain procedure.
        lo, hi, trials = 100, 200, 50
        rng_a = random.Random(12345)
        result = expected_draws(lo, hi, trials, rng_a)

        rng_b = random.Random(12345)
        total = 0
        for _ in range(trials):
            count = 0
            while True:
                x = rng_b.randint(lo, hi)
                count += 1
                if rpt.is_prime(x):
                    break
            total += count
        self.assertEqual(result, total / trials)
        self.assertEqual(rng_a.getstate(), rng_b.getstate())


class Validation(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(1)

    def test_type_errors(self):
        bad_ints = [1.5, "7", None, True, False, [7]]
        for bad in bad_ints:
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    expected_draws(bad, 100, 1, self.rng)
                with self.assertRaises(TypeError):
                    expected_draws(2, bad, 1, self.rng)
                with self.assertRaises(TypeError):
                    expected_draws(2, 100, bad, self.rng)

    def test_bad_rng_type(self):
        for bad in (None, random, object(), 12345):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    expected_draws(2, 100, 1, bad)

    def test_rng_subclass_accepted(self):
        self.assertEqual(expected_draws(2, 2, 1, ScriptedRandom([2])), 1)

    def test_value_errors(self):
        cases = [
            (1, 10, 1), (0, 10, 1), (-5, 10, 1),  # lo < 2
            (20, 10, 1),                           # lo > hi
            (2, 10, 0), (2, 10, -1),               # trials < 1
        ]
        for lo, hi, trials in cases:
            with self.subTest(lo=lo, hi=hi, trials=trials):
                with self.assertRaises(ValueError):
                    expected_draws(lo, hi, trials, self.rng)

    def test_type_checked_before_value(self):
        with self.assertRaises(TypeError):
            expected_draws(1.5, 0, 0, self.rng)
        with self.assertRaises(TypeError):
            expected_draws(0, 10, 1, None)
        with self.assertRaises(TypeError):
            expected_draws(20, 10, "x", self.rng)

    def test_invalid_input_does_not_use_rng(self):
        rng = ScriptedRandom([5])
        with self.assertRaises(ValueError):
            expected_draws(20, 10, 1, rng)
        self.assertEqual(rng.calls, [])


class Reproducibility(unittest.TestCase):
    def test_same_seed_same_result_small(self):
        a = expected_draws(100, 200, 200, random.Random(12345))
        b = expected_draws(100, 200, 200, random.Random(12345))
        self.assertEqual(a, b)

    def test_same_seed_same_result_run_a(self):
        _, lo, hi, trials = rpt.RUNS[0]
        a = expected_draws(lo, hi, trials, random.Random(rpt.SEED))
        b = expected_draws(lo, hi, trials, random.Random(rpt.SEED))
        self.assertEqual(a, b)


class RunCompletion(unittest.TestCase):
    """One integration test per assigned experiment, using the real intervals.

    Draws are counted through the instrumented generator. is_prime results
    are memoised only to check that every recorded draw was tested and to
    classify it; the number of draws comes from the generator.
    """

    def run_and_check(self, label, lo, hi, trials):
        results = {}
        real_is_prime = rpt.is_prime

        def spy(n):
            result = real_is_prime(n)
            results[n] = result
            return result

        rng = RecordingRandom(rpt.SEED)
        with mock.patch.object(rpt, "is_prime", spy):
            average = expected_draws(lo, hi, trials, rng)

        draws = rng.draws
        self.assertTrue(all(lo <= x <= hi for x in draws), label)
        primes = sum(1 for x in draws if results[x])
        self.assertEqual(primes, trials, f"{label}: completed searches")
        self.assertTrue(results[draws[-1]], f"{label}: last draw is prime")
        self.assertEqual(average, len(draws) / trials)

    def test_run_a_completes_1000_searches(self):
        _, lo, hi, trials = rpt.RUNS[0]
        self.assertEqual(trials, 1000)
        self.run_and_check("Run A", lo, hi, trials)

    def test_run_b_completes_250_searches(self):
        _, lo, hi, trials = rpt.RUNS[1]
        self.assertEqual((lo, hi, trials), (500_000_000_000, 500_001_000_000, 250))
        self.run_and_check("Run B", lo, hi, trials)


class Reuse(unittest.TestCase):
    def test_is_prime_is_problem2_object(self):
        import primality
        self.assertIs(rpt.is_prime, primality.is_prime)
        expected = (HERE.parent / "problem2" / "primality.py").resolve()
        self.assertEqual(Path(primality.__file__).resolve(), expected)


class PathIndependence(unittest.TestCase):
    PROGRAM = (
        "import sys, json\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "import random, random_prime_trials as m, primality\n"
        "print(json.dumps({'avg': m.expected_draws(2, 2, 1, random.Random(1)),\n"
        "                  'results_dir': str(m.RESULTS_DIR),\n"
        "                  'primality': primality.__file__}))\n"
    )

    def run_from(self, cwd):
        out = subprocess.run(
            [sys.executable, "-I", "-c", self.PROGRAM, str(HERE)],
            cwd=cwd, capture_output=True, text=True, check=True,
        ).stdout
        return json.loads(out)

    def test_other_working_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            for cwd in (tmp, str(HERE.parent)):
                with self.subTest(cwd=cwd):
                    info = self.run_from(cwd)
                    self.assertEqual(info["avg"], 1)
                    self.assertEqual(Path(info["results_dir"]), HERE / "Results")
                    self.assertEqual(
                        Path(info["primality"]).resolve(),
                        (HERE.parent / "problem2" / "primality.py").resolve(),
                    )
            self.assertEqual(list(Path(tmp).iterdir()), [])


class OutputFile(unittest.TestCase):
    TINY_RUNS = [("Run A", 100, 200, 10), ("Run B", 1000, 2000, 5)]

    def test_creates_dir_writes_and_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = Path(tmp) / "new" / "Results"
            self.assertFalse(results.exists())
            for _ in range(2):  # second call must overwrite, not append
                with mock.patch("sys.stdout"):
                    rpt.main(runs=self.TINY_RUNS, results_dir=results)
                lines = (results / "averages.txt").read_text(encoding="utf-8").splitlines()
                self.assertEqual(len(lines), 3)
            self.assertTrue(lines[0].startswith("Run A: lo=100 hi=200 trials=10 seed=12345 | empirical="))
            self.assertTrue(lines[1].startswith("Run B: lo=1,000 hi=2,000 trials=5 seed=12345 | empirical="))
            self.assertRegex(
                lines[0],
                r"empirical=\d+\.\d{2} \| theoretical=\d+\.\d{2} \| time=\d+\.\d{3} s$",
            )
            self.assertRegex(lines[2], r"^Total time: \d+\.\d{3} s$")

    def test_theory_uses_actual_midpoint(self):
        import math
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("sys.stdout"):
                rpt.main(runs=[("Run X", 100, 201, 3)], results_dir=tmp)
            line = (Path(tmp) / "averages.txt").read_text(encoding="utf-8").splitlines()[0]
        self.assertIn(f"theoretical={math.log(150.5):.2f}", line)


if __name__ == "__main__":
    unittest.main(verbosity=2)
