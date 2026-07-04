import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.improper_integral_generator import ImproperIntegralGenerator
from helpers import DELIM


def to_py(body):
    s = re.sub(r"e\^\(-(\d*)x\)",
               lambda m: f"math.exp(-{m.group(1) or 1}*x)", body)
    s = s.replace("√x", "x**0.5")
    s = s.replace("^", "**")
    s = re.sub(r"(\d)math", r"\1*math", s)
    return s


def geo_integral(f, lo, hi, n=6000):
    """Midpoint rule on a geometric grid (handles endpoint blow-ups)."""
    r = (hi / lo) ** (1.0 / n)
    total, x = 0.0, lo
    for _ in range(n):
        x2 = x * r
        total += f((x + x2) / 2) * (x2 - x)
        x = x2
    return total


def uni_integral(f, lo, hi, n=6000):
    h = (hi - lo) / n
    return sum(f(lo + (i + 0.5) * h) for i in range(n)) * h


_cache = {}


def oracle_check(example):
    """A9 oracle: independent numeric quadrature of the problem."""
    p = example["problem"]
    key = (p, example["final_answer"])
    if key in _cache:
        return _cache[key]
    m = re.fullmatch(r"Evaluate ∫ from (\S+) to (\S+) of \((.+)\) dx "
                     r"or state that it diverges\.", p)
    lo, hi, body = m.group(1), m.group(2), m.group(3)
    f = eval(f"lambda x: {to_py(body)}", {"math": math})
    if example["final_answer"] == "diverges":
        if hi == "∞":
            grew = geo_integral(f, 1.0, 1e6) - geo_integral(f, 1.0, 1e3)
        else:
            grew = geo_integral(f, 1e-6, 1.0) - geo_integral(f, 1e-3, 1.0)
        ok = grew > 1.0
    else:
        want = float(Fraction(example["final_answer"]))
        if "exp" in to_py(body):
            est = uni_integral(f, 0.0, 60.0)
        elif hi == "∞":
            est = geo_integral(f, float(lo), 1e7)
        else:
            est = geo_integral(f, 1e-12, 1.0)
        ok = abs(est - want) < 0.02 * max(1.0, abs(want))
    _cache[key] = ok
    return ok


class TestImproperIntegralGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ImproperIntegralGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_quadrature(self):
        """A9 oracle: numeric quadrature agrees with each answer."""
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_limit_rewrite_always_present(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"LIMIT_SETUP{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith(f"ANTIDERIV{DELIM}")
                                for s in result["steps"]))

    def test_divergent_and_convergent_both_occur(self):
        answers = [self.gen.generate()["final_answer"] for _ in range(200)]
        self.assertIn("diverges", answers)
        self.assertTrue(any(a != "diverges" for a in answers))

    def test_no_degenerate_renders(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join(result["steps"])
            # "+ -" is allowed: the one-sided limit "a→0+" may precede
            # a negative term. "(?<!\d)" so 21x is not read as 1x.
            for bad in (r"(?<!\d)1x", r"(?<!\d)1√", "--", r"/1\)"):
                self.assertIsNone(re.search(bad, joined),
                                  (bad, result["steps"]))

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(150):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 4)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ImproperIntegralGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
