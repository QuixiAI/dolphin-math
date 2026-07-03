import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.discriminant_generator import DiscriminantGenerator
from helpers import DELIM


def oracle_answer(example):
    """Recomputes Δ and the classification from the problem text alone."""
    expr = example["problem"].split(": ", 1)[1]
    var = next(v for v in "xyn" if f"{v}^2" in expr)
    m = re.fullmatch(
        rf"(\d*){var}\^2 ([+-]) (\d*){var} ([+-]) (\d+) = 0", expr)
    assert m, expr
    a = int(m.group(1) or 1)
    b = int(m.group(3) or 1) * (1 if m.group(2) == "+" else -1)
    c = int(m.group(5)) * (1 if m.group(4) == "+" else -1)
    d = b * b - 4 * a * c
    if d < 0:
        label = "no real solutions"
    elif d == 0:
        label = "one repeated rational solution"
    else:
        r = int(d ** 0.5)
        while r * r < d:
            r += 1
        label = ("two rational solutions" if r * r == d
                 else "two irrational solutions")
    return f"Δ = {d}; {label}"


class TestDiscriminantGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DiscriminantGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "discriminant_analysis")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute Δ and the class from the problem alone."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_disc_and_square_test_arithmetic(self):
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "DISC":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "SQUARE_TEST":
                    d = int(f[1])
                    squares = [int(x) for x in
                               re.findall(r"\^2 = (\d+)", f[2])]
                    if f[3] == "perfect square":
                        self.assertIn(d, squares, s)
                    else:
                        self.assertEqual(len(squares), 2, s)
                        self.assertTrue(squares[0] < d < squares[1], s)

    def test_all_classes_reachable_and_balanced(self):
        counts = {}
        for _ in range(400):
            result = self.gen.generate()
            label = result["final_answer"].split("; ", 1)[1]
            counts[label] = counts.get(label, 0) + 1
        self.assertEqual(set(counts), set(DiscriminantGenerator.LABELS.values()))
        for label, n in counts.items():
            self.assertGreater(n, 40, counts)

    def test_fixed_outcome_constructor(self):
        for outcome, label in DiscriminantGenerator.LABELS.items():
            gen = DiscriminantGenerator(outcome)
            for _ in range(5):
                self.assertTrue(gen.generate()["final_answer"].endswith(label))
        with self.assertRaises(ValueError):
            DiscriminantGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
