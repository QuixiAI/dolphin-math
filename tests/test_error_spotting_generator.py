import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.error_spotting_generator import ErrorSpottingGenerator
from helpers import DELIM


def parse_given(problem):
    """Returns the numbered given-scratchpad lines as a list of step strings."""
    lines = re.findall(r"^\d+\) (.+)$", problem, re.M)
    assert lines, problem
    return lines


def detect_error_equation(problem, given):
    """Independent detector: solve the equation, walk the given chain, and
    return (wrong_line_1indexed, true_x)."""
    m = re.search(r"Solve for x: (\d+)x ([+-]) (\d+) = (-?\d+)", problem)
    a, sign, b, c = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
    rhs_true = c - b if sign == "+" else c + b
    assert rhs_true % a == 0
    x_true = rhs_true // a

    combine = given[1].split(DELIM)     # EQ_OP_BOTH|verb|b|ax|rhs
    rhs_given = int(combine[4])
    if rhs_given != rhs_true:
        return 2, x_true
    divide = given[3].split(DELIM)      # EQ_OP_BOTH|divide|a|x|x
    if int(divide[4]) != x_true:
        return 4, x_true
    raise AssertionError("no error found in given work")


def detect_error_ratio(problem, given):
    """Independent detector for the ratio-table mode."""
    nums = re.search(r"Flour \(cups\): (\d+), \?\nSugar \(cups\): (\d+), (\d+)",
                     problem)
    pair1, pair2, known = (int(v) for v in nums.groups())
    from math import gcd
    g = gcd(pair1, pair2)
    a, b = pair1 // g, pair2 // g
    assert known % b == 0
    k = known // b
    missing_true = a * k

    base = given[1].split(DELIM)        # RATIO_BASE|pair|g|a:b
    if base[3] != f"{a}:{b}" or int(base[2]) != g:
        return 2, missing_true
    d = given[2].split(DELIM)           # D|known|b|k
    if int(d[3]) != k:
        return 3, missing_true
    mstep = given[3].split(DELIM)       # M|a|k|product
    if int(mstep[3]) != missing_true:
        return 4, missing_true
    raise AssertionError("no error found in given work")


class TestErrorSpottingGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ErrorSpottingGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])
        self.assertRegex(result["final_answer"], r"^step \d+; -?\d+$")

    def test_oracle_error_detection(self):
        """A9 oracle: an independent detector must find the SAME wrong line
        and the same corrected answer as the generator claims."""
        for _ in range(400):
            result = self.gen.generate()
            given = parse_given(result["problem"])
            detect = (detect_error_equation
                      if result["operation"] == "error_spotting_equation"
                      else detect_error_ratio)
            k_true, value_true = detect(result["problem"], given)
            self.assertEqual(result["final_answer"],
                             f"step {k_true}; {value_true}",
                             result["problem"])

    def test_exactly_one_seeded_error(self):
        """The flagged line is wrong; the given final Z is consistent with
        the propagated error (the student followed their mistake through)."""
        for _ in range(300):
            result = self.gen.generate()
            given = parse_given(result["problem"])
            flag = next(s for s in result["steps"]
                        if s.startswith(f"FLAG{DELIM}"))
            k = int(flag.split(DELIM)[1])
            # FLAG text: "<work> = <true>, not <given>"
            m = re.search(r"= (-?\d+), not (-?\d+)$", flag.split(DELIM)[2])
            self.assertIsNotNone(m, flag)
            true_val, given_val = int(m.group(1)), int(m.group(2))
            self.assertNotEqual(true_val, given_val, flag)
            self.assertTrue(given[k - 1].endswith(str(given_val)),
                            (given[k - 1], flag))
            # student's own Z carries the propagated wrong result
            self.assertNotEqual(given[-1], f"Z{DELIM}{true_val}")

    def test_verify_sweep_covers_lines_before_error(self):
        for _ in range(300):
            result = self.gen.generate()
            codes = [s.split(DELIM) for s in result["steps"]]
            flag_idx = next(i for i, f in enumerate(codes) if f[0] == "FLAG")
            k = int(codes[flag_idx][1])
            verifies = [f for f in codes[:flag_idx]]
            self.assertEqual([f[0] for f in verifies], ["VERIFY"] * (k - 1))
            self.assertEqual([int(f[1]) for f in verifies],
                             list(range(1, k)))
            self.assertTrue(all(f[2] == "ok" for f in verifies))

    def test_redo_steps_use_normal_vocabulary_and_end_with_check(self):
        for _ in range(200):
            result = self.gen.generate()
            codes = [s.split(DELIM)[0] for s in result["steps"]]
            flag_idx = codes.index("FLAG")
            tail = codes[flag_idx + 1:]
            self.assertNotIn("VERIFY", tail)
            self.assertIn("CHECK", tail)
            self.assertEqual(tail[-1], "Z")

    def test_modes_reachable_and_fixed(self):
        seen = {self.gen.generate()["operation"] for _ in range(60)}
        self.assertEqual(seen, {"error_spotting_equation",
                                "error_spotting_ratio"})
        gen = ErrorSpottingGenerator("ratio")
        for _ in range(10):
            self.assertEqual(gen.generate()["operation"],
                             "error_spotting_ratio")
        with self.assertRaises(ValueError):
            ErrorSpottingGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
