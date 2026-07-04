import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.z_transform_generator import (
    ZTransformGenerator,
    power_base_text,
    seq_text,
    transform_text,
    z_denom_text,
)
from helpers import DELIM


GEOM_RE = re.compile(
    r"Find the z-transform of x\[n\]=(\d+)\*(\(?-?\d+\)?)\^n u\[n\] and "
    r"compute x\[0\] through x\[3\]\."
)
DIFF_RE = re.compile(
    r"Solve y\[n\]-(\(?-?\d+\)?)y\[n-1\]=delta\[n\] with y\[-1\]=0 using "
    r"z-transforms, and list y\[0\] through y\[4\]\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def expected_geometric(problem):
    amplitude_raw, r_raw = GEOM_RE.fullmatch(problem).groups()
    amplitude = int(amplitude_raw)
    r_value = int(r_raw.strip("()"))
    terms = []
    steps = [
        make_step("ZT_SETUP", "geometric",
                  f"x[n]={amplitude}*{power_base_text(r_value)}^n u[n]"),
        make_step("ZT_PAIR", "Z{r^n u[n]}=1/(1-r z^-1)"),
        make_step("REWRITE", f"X(z)={transform_text(amplitude, r_value)}"),
    ]
    for n in range(4):
        power = r_value ** n
        term = amplitude * power
        terms.append(term)
        steps += [
            make_step("E", r_value, n, power),
            make_step("M", amplitude, power, term),
        ]
    steps.append(make_step("TERMS", f"x[0..3]={seq_text(terms)}"))
    answer = (
        f"X(z)={transform_text(amplitude, r_value)}; "
        f"ROC magnitude(z)>{abs(r_value)}; terms={seq_text(terms)}"
    )
    return steps, answer


def expected_difference(problem):
    a_value = int(DIFF_RE.fullmatch(problem).group(1).strip("()"))
    a_text = power_base_text(a_value)
    terms = []
    steps = [
        make_step("ZT_SETUP", "difference",
                  f"y[n]-{a_text}y[n-1]=delta[n]", "y[-1]=0"),
        make_step("SHIFT", "Z{y[n-1]}=z^-1Y(z)"),
        make_step("REWRITE", f"({z_denom_text(a_value)})Y(z)=1"),
        make_step("REWRITE", f"Y(z)={transform_text(1, a_value)}"),
    ]
    for n in range(5):
        term = a_value ** n
        terms.append(term)
        steps.append(make_step("E", a_value, n, term))
    steps.append(make_step("TERMS", f"y[0..4]={seq_text(terms)}"))
    answer = f"Y(z)={transform_text(1, a_value)}; y[0..4]={seq_text(terms)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if GEOM_RE.fullmatch(problem):
        steps, answer = expected_geometric(problem)
    else:
        steps, answer = expected_difference(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestZTransformGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ZTransformGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ZTransformGenerator.VARIANTS:
            result = ZTransformGenerator(variant).generate()
            self.assertEqual(result["operation"], f"z_transform_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ZTransformGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
