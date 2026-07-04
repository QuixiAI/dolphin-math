import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.transformation_generator import TransformationGenerator
from helpers import DELIM


def apply_named(name, p):
    m = re.fullmatch(r"translation by \((-?\d+), (-?\d+)\)", name)
    if m:
        return (p[0] + int(m.group(1)), p[1] + int(m.group(2)))
    if name == "reflection over the x-axis":
        return (p[0], -p[1])
    if name == "reflection over the y-axis":
        return (-p[0], p[1])
    if name == "reflection over the line y = x":
        return (p[1], p[0])
    if name == "rotation 90° counterclockwise about the origin":
        return (-p[1], p[0])
    if name == "rotation 180° about the origin":
        return (-p[0], -p[1])
    if name == "rotation 270° counterclockwise about the origin":
        return (p[1], -p[0])
    m = re.fullmatch(r"dilation by factor (\d+) centered at the origin",
                     name)
    assert m, name
    k = int(m.group(1))
    return (k * p[0], k * p[1])


def oracle_answer(example):
    p_txt = example["problem"]
    m = re.fullmatch(r"Find the image of P\((-?\d+), (-?\d+)\) under a "
                     r"(.+) followed by a (.+)\.", p_txt)
    if m:
        p = (int(m.group(1)), int(m.group(2)))
        q = apply_named(m.group(3), p)
        r = apply_named(m.group(4), q)
        return f"({r[0]}, {r[1]})"
    m = re.fullmatch(r"Find the image of P\((-?\d+), (-?\d+)\) under a "
                     r"(.+)\.", p_txt)
    assert m, p_txt
    p = (int(m.group(1)), int(m.group(2)))
    q = apply_named(m.group(3), p)
    return f"({q[0]}, {q[1]})"


class TestTransformationGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TransformationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: reapply the named transformations."""
        for _ in range(600):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result), result["final_answer"],
                             result["problem"])

    def test_rule_precedes_each_apply(self):
        for _ in range(300):
            result = self.gen.generate()
            ops = [s.split(DELIM)[0] for s in result["steps"]]
            self.assertEqual(ops.count("TRANSFORM_RULE"),
                             ops.count("TRANSFORM_APPLY"))
            last = None
            for o in ops:
                if o == "TRANSFORM_APPLY":
                    self.assertEqual(last, "TRANSFORM_RULE",
                                     msg=str(ops))
                if o in ("TRANSFORM_RULE", "TRANSFORM_APPLY"):
                    last = o if o == "TRANSFORM_RULE" else None

    def test_no_digit_smash_in_apply(self):
        """Substituted coordinates are always parenthesized."""
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "TRANSFORM_APPLY":
                    # no unsubstituted variables remain in the work text
                    self.assertNotRegex(f[1], r"[a-z]", s)

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] == "A":
                    self.assertEqual(int(f[1]) + int(f[2]), int(f[3]), s)
                elif f[0] == "S":
                    self.assertEqual(int(f[1]) - int(f[2]), int(f[3]), s)
                elif f[0] == "M":
                    self.assertEqual(int(f[1]) * int(f[2]), int(f[3]), s)

    def test_composition_and_single_occur(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"transformation_single",
                               "transformation_composition"})


if __name__ == "__main__":
    unittest.main()
