import os
import re
import sys
import unittest
from fractions import Fraction
from math import isqrt

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.orbital_mechanics_generator import OrbitalMechanicsGenerator
from helpers import DELIM


CENTRIPETAL_RE = re.compile(
    r"A (\d+) kg object moves in a circle of radius (\d+) m with speed "
    r"(\d+) m/s\. Find centripetal acceleration and centripetal force\."
)
GRAVITY_RE = re.compile(
    r"In a scaled gravitation problem, two masses m1=(\d+) kg and "
    r"m2=(\d+) kg are (\d+) m apart with G=1\. Find the gravitational "
    r"force magnitude\."
)
KEPLER_RE = re.compile(
    r"A planet has orbital radius a1=(\d+) AU and period T1=(\d+) days\. "
    r"Another planet orbits the same star at a2=(\d+) AU\. Use Kepler's "
    r"third law to find the second period\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def exact_square_root(value):
    value = Fraction(value)
    root_num = isqrt(value.numerator)
    root_den = isqrt(value.denominator)
    assert root_num * root_num == value.numerator
    assert root_den * root_den == value.denominator
    return Fraction(root_num, root_den)


def expected_centripetal(problem):
    mass, radius, speed = (
        int(value) for value in CENTRIPETAL_RE.fullmatch(problem).groups()
    )
    speed_sq = speed ** 2
    acceleration = Fraction(speed_sq, radius)
    force = mass * acceleration
    steps = [
        make_step("ORBIT_SETUP", "centripetal_force", f"m={mass}",
                  f"r={radius}, v={speed}"),
        make_step("ORBIT_FORMULA", "a_c=v^2/r"),
        make_step("E", speed, 2, speed_sq),
        make_step("D", speed_sq, radius, fraction_text(acceleration)),
        make_step("ORBIT_FORMULA", "F_c=m*a_c"),
        make_step("M", mass, fraction_text(acceleration),
                  fraction_text(force)),
    ]
    answer = (
        f"a_c={fraction_text(acceleration)} m/s^2; "
        f"F_c={fraction_text(force)} N"
    )
    return steps, answer


def expected_gravity(problem):
    m1, m2, radius = (
        int(value) for value in GRAVITY_RE.fullmatch(problem).groups()
    )
    g_const = 1
    mass_product = m1 * m2
    numerator = g_const * mass_product
    radius_sq = radius ** 2
    force = Fraction(numerator, radius_sq)
    steps = [
        make_step("ORBIT_SETUP", "gravity_force", f"m1={m1}, m2={m2}",
                  f"r={radius}, G={g_const}"),
        make_step("ORBIT_FORMULA", "F=G*m1*m2/r^2"),
        make_step("M", m1, m2, mass_product),
        make_step("M", g_const, mass_product, numerator),
        make_step("E", radius, 2, radius_sq),
        make_step("D", numerator, radius_sq, fraction_text(force)),
    ]
    answer = f"F_g={fraction_text(force)} N"
    return steps, answer


def expected_kepler(problem):
    radius1, period1, radius2 = (
        int(value) for value in KEPLER_RE.fullmatch(problem).groups()
    )
    radius_ratio = Fraction(radius2, radius1)
    radius_ratio_cubed = radius_ratio ** 3
    period_ratio = exact_square_root(radius_ratio_cubed)
    assert period_ratio.denominator == 1
    period2 = period1 * period_ratio.numerator
    steps = [
        make_step("ORBIT_SETUP", "kepler_third",
                  f"T1={period1}, a1={radius1}", f"a2={radius2}"),
        make_step("ORBIT_FORMULA", "(T2/T1)^2=(a2/a1)^3"),
        make_step("D", radius2, radius1, fraction_text(radius_ratio)),
        make_step("E", fraction_text(radius_ratio), 3,
                  fraction_text(radius_ratio_cubed)),
        make_step("ROOT", fraction_text(radius_ratio_cubed),
                  period_ratio.numerator),
        make_step("M", period1, period_ratio.numerator, period2),
    ]
    answer = f"T2={period2} days"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if CENTRIPETAL_RE.fullmatch(problem):
        steps, answer = expected_centripetal(problem)
    elif GRAVITY_RE.fullmatch(problem):
        steps, answer = expected_gravity(problem)
    else:
        steps, answer = expected_kepler(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestOrbitalMechanicsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = OrbitalMechanicsGenerator()

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
                elif fields[0] == "ROOT":
                    self.assertEqual(Fraction(fields[2]) * Fraction(fields[2]),
                                     Fraction(fields[1]), raw_step)

    def test_variants_are_available(self):
        for variant in OrbitalMechanicsGenerator.VARIANTS:
            result = OrbitalMechanicsGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"orbital_mechanics_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            OrbitalMechanicsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
