"""Tests for verify_totient.py.

Most tests patch euler_totient with a stub (in-range products are 4-9 million,
so the real function is slow). Stubbed tests check logic; the real
integration test and the full run of verify_totient.py check the mathematics.
"""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import verify_totient as vt
from verify_totient import verify_totient_identity

# Hand-derived (p-1)(q-1) literals, keyed by pq. Not computed from the code.
STUB_VALUES = {
    4028033: 4024020,  # 2003 * 2011
    4088459: 4084416,  # 2017 * 2027
    4137131: 4133064,  # 2029 * 2039
    4334723: 4330560,  # 2081 * 2083
    8904031: 8898064,  # 2969 * 2999
}
ALL_PAIRS = [(2003, 2011), (2017, 2027), (2029, 2039), (2081, 2083), (2969, 2999)]


def patch_totient(values=None):
    """Patch euler_totient with an autospec'd lookup stub (KeyError if unexpected)."""
    table = STUB_VALUES if values is None else values
    return mock.patch(
        "verify_totient.euler_totient", autospec=True,
        side_effect=lambda n: table[n],
    )


class TestValidStubbed(unittest.TestCase):
    def test_record_keys_and_values(self):
        with patch_totient() as stub:
            result = verify_totient_identity([(2003, 2011)])
        stub.assert_called_once_with(2003 * 2011)
        self.assertEqual(result, [{
            "p": 2003, "q": 2011, "pq": 4028033, "phi_pq": 4024020,
            "expected": 4024020, "matches": True,
        }])

    def test_all_pairs_in_order(self):
        with patch_totient() as stub:
            result = verify_totient_identity(ALL_PAIRS)
        stub.assert_has_calls([mock.call(p * q) for p, q in ALL_PAIRS])
        self.assertEqual([(r["p"], r["q"]) for r in result], ALL_PAIRS)
        self.assertTrue(all(r["matches"] for r in result))
        self.assertEqual([r["phi_pq"] for r in result], list(STUB_VALUES.values()))

    def test_empty_list(self):
        with patch_totient() as stub:
            self.assertEqual(verify_totient_identity([]), [])
        stub.assert_not_called()

    def test_wrong_totient_detected(self):
        with patch_totient({4028033: 4024021}):
            result = verify_totient_identity([(2003, 2011)])
        self.assertIs(result[0]["matches"], False)
        report = vt._format_report(result, [0.0], 0.0, "note")
        self.assertEqual(
            report.splitlines()[-1], "All distinct-prime cases verified: FAIL"
        )


class TestInvalidInput(unittest.TestCase):
    def check(self, exc, pairs):
        with patch_totient() as stub:
            with self.assertRaises(exc):
                verify_totient_identity(pairs)
        stub.assert_not_called()

    def test_equal_primes(self):
        with patch_totient():
            with self.assertRaisesRegex(ValueError, "distinct primes"):
                verify_totient_identity([(2011, 2011)])

    def test_composite(self):
        self.check(ValueError, [(2001, 2011)])
        self.check(ValueError, [(2003, 2001)])

    def test_out_of_range(self):
        self.check(ValueError, [(1999, 2003)])
        self.check(ValueError, [(2003, 3001)])

    def test_bounds_inclusive_but_not_prime(self):
        # 2000 and 3000 pass the range check, then fail primality.
        for pair in [(2000, 2003), (2003, 3000)]:
            with patch_totient():
                with self.assertRaisesRegex(ValueError, "not prime"):
                    verify_totient_identity([pair])

    def test_bad_types(self):
        for bad in (2003.0, "2003", None, True):
            self.check(TypeError, [(bad, 2011)])
            self.check(TypeError, [(2003, bad)])

    def test_malformed(self):
        for bad in ((2003, 2011), None, "ab", {(2003, 2011)}):
            self.check(TypeError, bad)
        for bad in ([2003, 2011], 5, None):
            self.check(TypeError, [bad])
        for bad in ((2003,), (2003, 2011, 2017), ()):
            self.check(ValueError, [bad])

    def test_duplicates(self):
        self.check(ValueError, [(2003, 2011), (2003, 2011)])
        self.check(ValueError, [(2003, 2011), (2011, 2003)])

    def test_fail_fast_no_partial_results(self):
        self.check(ValueError, [(2003, 2011), (2017, 2027), (2001, 2011)])


class TestRealTotient(unittest.TestCase):
    def test_small_semiprime(self):
        """Real euler_totient(15) == 8.

        Checks the underlying totient function only. It does not exercise the
        Problem 7 workflow, because the 2000..3000 range rejects 3 and 5.
        """
        self.assertEqual(vt.euler_totient(15), 8)

    def test_integration_primary_pair_slow(self):
        """Slow: real, unpatched run of (2003, 2011)."""
        result = verify_totient_identity([(2003, 2011)])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["phi_pq"], 4024020)
        self.assertEqual(result[0]["expected"], 4024020)
        self.assertIs(result[0]["matches"], True)


class TestReport(unittest.TestCase):
    def records(self, pairs=ALL_PAIRS):
        return [
            {"p": p, "q": q, "pq": p * q, "phi_pq": STUB_VALUES[p * q],
             "expected": (p - 1) * (q - 1), "matches": True}
            for p, q in pairs
        ]

    def test_report_layout(self):
        recs = self.records()
        report = vt._format_report(recs, [1.0] * 5, 5.0, "Contrast note")
        lines = report.splitlines()
        self.assertEqual(lines[0], "Primary pair: p = 2003, q = 2011")
        for header in ("p", "q", "pq", "phi(pq)", "(p-1)(q-1)", "match?"):
            self.assertIn(header, lines[2])
        self.assertEqual(lines[-1], "All distinct-prime cases verified: PASS")
        self.assertIn("Conclusion:", lines[-2])
        self.assertIn("Total: 5.000 s", report)


class TestMainStubbed(unittest.TestCase):
    def run_main(self, values=None, results=None):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Results" / "totient_verification.txt"  # missing dir
            out = io.StringIO()
            with mock.patch.object(vt, "RESULTS_PATH", path), \
                    patch_totient(values), contextlib.redirect_stdout(out):
                status = vt.main()
                first = path.read_text(encoding="utf-8") if path.exists() else None
                if results == "twice":
                    vt.main()
                    first = (first, path.read_text(encoding="utf-8"))
        return status, out.getvalue(), first

    def test_pass(self):
        status, printed, content = self.run_main()
        self.assertEqual(status, 0)
        self.assertEqual(printed, content)
        self.assertTrue(content.startswith("Primary pair: p = 2003, q = 2011"))
        self.assertIn("Contrast case (not in table): (2011, 2011)", content)
        table = content.split("\n\n")[1].splitlines()
        self.assertEqual(len(table), 6)  # header + five distinct-prime rows
        self.assertNotIn("(2011, 2011)", "\n".join(table))
        self.assertTrue(content.endswith("All distinct-prime cases verified: PASS\n"))

    def test_overwrite(self):
        status, _, (first, second) = self.run_main(results="twice")
        self.assertEqual(status, 0)
        self.assertEqual(first.count("Primary pair:"), 1)
        self.assertEqual(second.count("Primary pair:"), 1)

    def test_fail_exit_status(self):
        bad = dict(STUB_VALUES)
        bad[4028033] = 4024021
        status, printed, content = self.run_main(bad)
        self.assertEqual(status, 1)
        self.assertTrue(content.endswith("All distinct-prime cases verified: FAIL\n"))

    def test_unexpected_exception(self):
        err = io.StringIO()
        with mock.patch("verify_totient.euler_totient", autospec=True,
                        side_effect=RuntimeError("boom")), \
                contextlib.redirect_stderr(err):
            status = vt.main()
        self.assertEqual(status, 1)
        self.assertIn("boom", err.getvalue())


if __name__ == "__main__":
    unittest.main()
