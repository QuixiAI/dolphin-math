import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.magnetism_generator import MagnetismGenerator
from helpers import DELIM


FORCE_RE = re.compile(
    r"A charge q=(\d+) C moves at speed v=(\d+) m/s through a magnetic "
    r"field B=(\d+) T with sin\(theta\)=([^ ]+)\. Find the magnetic force "
    r"magnitude\."
)
WIRE_RE = re.compile(
    r"A long straight wire carries current I=(\d+) A\. At distance r=(\d+) "
    r"m, use mu0=1 to find the magnetic field magnitude "
    r"B=mu0\*I/\(2πr\)\."
)
LOOP_RE = re.compile(
    r"A circular loop carries current I=(\d+) A and has radius R=(\d+) m\. "
    r"Use mu0=1 to find the magnetic field at the center, "
    r"B=mu0\*I/\(2R\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def over_pi_text(value):
    coeff = Fraction(value)
    if coeff.denominator == 1:
        return f"{coeff.numerator}/π"
    return f"{coeff.numerator}/({coeff.denominator}π)"


def expected_force(problem):
    charge_raw, speed_raw, field_raw, sin_raw = (
        FORCE_RE.fullmatch(problem).groups()
    )
    charge = int(charge_raw)
    speed = int(speed_raw)
    field = int(field_raw)
    sin_theta = Fraction(sin_raw)
    qv = charge * speed
    qvb = qv * field
    force = qvb * sin_theta
    steps = [
        make_step("MAG_SETUP", "force", f"q={charge}, v={speed}",
                  f"B={field}, sin={fraction_text(sin_theta)}"),
        make_step("MAG_FORMULA", "F=q*v*B*sin(theta)"),
        make_step("M", charge, speed, qv),
        make_step("M", qv, field, qvb),
        make_step("M", qvb, fraction_text(sin_theta), fraction_text(force)),
    ]
    answer = f"F={fraction_text(force)} N"
    return steps, answer


def expected_wire(problem):
    current, radius = (int(value) for value in WIRE_RE.fullmatch(problem).groups())
    denominator = 2 * radius
    coeff = Fraction(current, denominator)
    field = over_pi_text(coeff)
    steps = [
        make_step("MAG_SETUP", "straight_wire", f"I={current}, r={radius}",
                  "mu0=1"),
        make_step("MAG_FORMULA", "B=mu0*I/(2πr)"),
        make_step("M", 2, radius, denominator),
        make_step("D", current, denominator, fraction_text(coeff)),
        make_step("PI_DEN", fraction_text(coeff), "π", field),
    ]
    answer = f"B={field} T"
    return steps, answer


def expected_loop(problem):
    current, radius = (int(value) for value in LOOP_RE.fullmatch(problem).groups())
    denominator = 2 * radius
    field = Fraction(current, denominator)
    steps = [
        make_step("MAG_SETUP", "loop_center", f"I={current}, R={radius}",
                  "mu0=1"),
        make_step("MAG_FORMULA", "B=mu0*I/(2R)"),
        make_step("M", 2, radius, denominator),
        make_step("D", current, denominator, fraction_text(field)),
    ]
    answer = f"B={fraction_text(field)} T"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if FORCE_RE.fullmatch(problem):
        steps, answer = expected_force(problem)
    elif WIRE_RE.fullmatch(problem):
        steps, answer = expected_wire(problem)
    else:
        steps, answer = expected_loop(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMagnetismGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MagnetismGenerator()

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
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "PI_DEN":
                    self.assertEqual(fields[2], "π", raw_step)
                    self.assertEqual(over_pi_text(Fraction(fields[1])),
                                     fields[3], raw_step)

    def test_variants_are_available(self):
        for variant in MagnetismGenerator.VARIANTS:
            result = MagnetismGenerator(variant).generate()
            self.assertEqual(result["operation"], f"magnetism_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MagnetismGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
