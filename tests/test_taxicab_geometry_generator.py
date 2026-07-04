import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.taxicab_geometry_generator import TaxicabGeometryGenerator
from helpers import DELIM


def brute_circle(r, metric):
    count = 0
    for x in range(-r - 1, r + 2):
        for y in range(-r - 1, r + 2):
            d = abs(x) + abs(y) if metric == "taxi" else max(abs(x),
                                                             abs(y))
            if d == r:
                count += 1
    return count


def oracle_answer(example):
    p = example["problem"]
    m = re.fullmatch(r"Using the (taxicab|Chebyshev) metric, find the "
                     r"distance between \((-?\d+), (-?\d+)\) and "
                     r"\((-?\d+), (-?\d+)\)\.", p)
    if m:
        x1, y1, x2, y2 = (int(v) for v in m.groups()[1:])
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        return str(dx + dy if m.group(1) == "taxicab" else max(dx, dy))
    m = re.fullmatch(r"In (taxicab|Chebyshev) geometry, how many lattice "
                     r"points lie at distance exactly (\d+) from the "
                     r"origin\?", p)
    if m:
        r = int(m.group(2))
        return str(brute_circle(r, "taxi" if m.group(1) == "taxicab"
                                else "cheb"))
    m = re.fullmatch(r"For the points \((-?\d+), (-?\d+)\) and "
                     r"\((-?\d+), (-?\d+)\), find both the taxicab "
                     r"distance and the Chebyshev distance\.", p)
    assert m, p
    x1, y1, x2, y2 = (int(v) for v in m.groups())
    dx, dy = abs(x2 - x1), abs(y2 - y1)
    return f"taxicab {dx + dy}; Chebyshev {max(dx, dy)}"


class TestTaxicabGeometryGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TaxicabGeometryGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: brute-force lattice counts and direct distances."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_no_pipes_inside_fields(self):
        """abs() notation, never |x| bars, so fields stay pipe-safe."""
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                op = s.split(DELIM)[0]
                self.assertTrue(op.replace("_", "").isalpha(), s)

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)
                elif f[0] == "ABS_VAL":
                    self.assertEqual(abs(int(f[1].strip("()"))),
                                     int(f[2]), s)
                elif f[0] == "MAX":
                    vals = [int(v) for v in f[1].split(", ")]
                    self.assertEqual(max(vals), int(f[2]), s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(200):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 5)


if __name__ == "__main__":
    unittest.main()
