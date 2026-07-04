import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.electrostatics_generator import ElectrostaticsGenerator
from helpers import DELIM


FIELD_RE = re.compile(
    r"In scaled units with k=1, charges q1=(-?\d+) C at x=-(\d+) m and "
    r"q2=(-?\d+) C at x=(\d+) m lie on the x-axis\. Find the signed "
    r"electric field at the origin, taking right as positive\."
)
POTENTIAL_RE = re.compile(
    r"In scaled units with k=1, three point charges are at distances "
    r"r1=(\d+) m, r2=(\d+) m, r3=(\d+) m from the origin with charges "
    r"q1=(-?\d+) C, q2=(-?\d+) C, q3=(-?\d+) C\. Find the electric "
    r"potential at the origin\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_field(problem):
    q1, r1, q2, r2 = (
        int(value) for value in FIELD_RE.fullmatch(problem).groups()
    )
    r1_sq = r1 ** 2
    r2_sq = r2 ** 2
    e1 = Fraction(q1, r1_sq)
    neg_q2 = -q2
    e2 = Fraction(neg_q2, r2_sq)
    total = e1 + e2
    steps = [
        make_step("ELEC_SETUP", "field_axis", f"q1={q1}, x1=-{r1}",
                  f"q2={q2}, x2={r2}"),
        make_step("ELEC_SETUP", "right positive", "k=1"),
        make_step("ELEC_FORMULA", "left charge: E1=q1/r1^2"),
        make_step("E", r1, 2, r1_sq),
        make_step("D", q1, r1_sq, fraction_text(e1)),
        make_step("ELEC_FORMULA", "right charge: E2=-q2/r2^2"),
        make_step("M", -1, q2, neg_q2),
        make_step("E", r2, 2, r2_sq),
        make_step("D", neg_q2, r2_sq, fraction_text(e2)),
        make_step("A", fraction_text(e1), fraction_text(e2),
                  fraction_text(total)),
    ]
    answer = f"E={fraction_text(total)} N/C right-positive"
    return steps, answer


def expected_potential(problem):
    r1, r2, r3, q1, q2, q3 = (
        int(value) for value in POTENTIAL_RE.fullmatch(problem).groups()
    )
    v1 = Fraction(q1, r1)
    v2 = Fraction(q2, r2)
    partial = v1 + v2
    v3 = Fraction(q3, r3)
    total = partial + v3
    steps = [
        make_step("ELEC_SETUP", "potential_axis", f"q1={q1}, r1={r1}",
                  f"q2={q2}, r2={r2}"),
        make_step("ELEC_SETUP", f"q3={q3}, r3={r3}", "k=1"),
        make_step("ELEC_FORMULA", "V=sum(q_i/r_i)"),
        make_step("D", q1, r1, fraction_text(v1)),
        make_step("D", q2, r2, fraction_text(v2)),
        make_step("A", fraction_text(v1), fraction_text(v2),
                  fraction_text(partial)),
        make_step("D", q3, r3, fraction_text(v3)),
        make_step("A", fraction_text(partial), fraction_text(v3),
                  fraction_text(total)),
    ]
    answer = f"V={fraction_text(total)} V"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if FIELD_RE.fullmatch(problem):
        steps, answer = expected_field(problem)
    else:
        steps, answer = expected_potential(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestElectrostaticsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ElectrostaticsGenerator()

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
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(Fraction(fields[1]) ** int(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ElectrostaticsGenerator.VARIANTS:
            result = ElectrostaticsGenerator(variant).generate()
            self.assertEqual(result["operation"], f"electrostatics_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            ElectrostaticsGenerator("bogus")

    def test_positive_and_negative_totals_occur(self):
        totals = set()
        for _ in range(500):
            answer = self.gen.generate()["final_answer"]
            totals.add(Fraction(answer.split("=", 1)[1].split(" ", 1)[0]) > 0)
        self.assertEqual(totals, {False, True})

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
