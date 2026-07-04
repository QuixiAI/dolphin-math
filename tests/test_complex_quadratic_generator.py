import math
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.complex_quadratic_generator import ComplexQuadraticGenerator
from helpers import DELIM


def parse_eq(problem):
    """'Solve: x^2 - 4x + 13 = 0.' -> (B, C)."""
    m = re.fullmatch(r"Solve: x\^2(?: ([+-]) (\d+)?x)? \+ (\d+) = 0\.",
                     problem)
    assert m, problem
    B = int(m.group(2) or 1) * (1 if m.group(1) == "+" else -1) \
        if m.group(1) else 0
    return B, int(m.group(3))


def parse_root(text):
    """'2 + 3i' / '3 - i√2' / 'i√5' / '-2i' -> (p, q, k) with root
    p + q·i·√k (k=1 for gaussian)."""
    m = re.fullmatch(r"(?:(-?\d+) ([+-]) )?(-?)(\d*)i(?:√(\d+))?", text)
    assert m, text
    p = int(m.group(1) or 0)
    mag = int(m.group(4) or 1)
    neg = (m.group(2) == "-") or (m.group(3) == "-")
    return p, -mag if neg else mag, int(m.group(5) or 1)


def oracle_check(example):
    """Substitute both roots into x^2 + Bx + C symbolically."""
    B, C = parse_eq(example["problem"])
    m = re.fullmatch(r"x = (.+) or x = (.+)", example["final_answer"])
    assert m, example["final_answer"]
    for txt in m.groups():
        p, q, k = parse_root(txt)
        # (p + qi√k)^2 + B(p + qi√k) + C
        real = p * p - q * q * k + B * p + C
        imag_coef = 2 * p * q + B * q   # coefficient of i√k
        if real != 0 or imag_coef != 0:
            return False
    return True


class TestComplexQuadraticGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ComplexQuadraticGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "quadratic_complex_roots")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_roots_satisfy_equation(self):
        """A9 oracle: both roots substituted back give exactly zero."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_discriminant_is_negative_and_correct(self):
        for _ in range(300):
            result = self.gen.generate()
            B, C = parse_eq(result["problem"])
            d = next(s for s in result["steps"]
                     if s.startswith(f"DISC{DELIM}"))
            self.assertEqual(int(d.split(DELIM)[2]), B * B - 4 * C, d)
            self.assertLess(int(d.split(DELIM)[2]), 0)
            self.assertTrue(any(s.startswith(f"DISC_CLASSIFY{DELIM}")
                                for s in result["steps"]))

    def test_roots_are_conjugates(self):
        for _ in range(300):
            result = self.gen.generate()
            m = re.fullmatch(r"x = (.+) or x = (.+)",
                             result["final_answer"])
            p1, q1, k1 = parse_root(m.group(1))
            p2, q2, k2 = parse_root(m.group(2))
            self.assertEqual((p1, k1), (p2, k2))
            self.assertEqual(q1, -q2)
            self.assertGreater(q1, 0)  # + root listed first

    def test_radical_k_is_squarefree(self):
        gen = ComplexQuadraticGenerator("radical")
        for _ in range(200):
            result = gen.generate()
            m = re.search(r"√(\d+)", result["final_answer"])
            k = int(m.group(1))
            for f in range(2, int(math.isqrt(k)) + 1):
                self.assertNotEqual(k % (f * f), 0,
                                    result["final_answer"])

    def test_pure_imaginary_case_occurs(self):
        found = False
        for _ in range(400):
            result = self.gen.generate()
            if "x^2 +" in result["problem"] and "x " not in \
                    result["problem"].split("^2")[1].split("=")[0]:
                found = True
                break
        self.assertTrue(found)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            ComplexQuadraticGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
