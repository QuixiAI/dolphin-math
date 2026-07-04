import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.relativistic_energy_generator import RelativisticEnergyGenerator
from helpers import DELIM


REST_RE = re.compile(
    r"Using E=m\*c\^2, find the rest energy for mass m=(\d+) kg and "
    r"c=(\d+) m/s\."
)
MASS_RE = re.compile(
    r"In c=1 units, a particle has momentum p=(\d+) and mass m=(\d+)\. "
    r"Find E from E\^2=p\^2\+m\^2\."
)
VELOCITY_RE = re.compile(
    r"In c=1 units, velocities u=([^ ]+) and v=([^ ]+) are collinear\. "
    r"Compute the relativistic velocity sum w\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_rest(problem):
    mass, c = (int(value) for value in REST_RE.fullmatch(problem).groups())
    c_sq = c ** 2
    energy = mass * c_sq
    steps = [
        make_step("REL_ENERGY_SETUP", "rest_energy", f"m={mass}", f"c={c}"),
        make_step("REL_ENERGY_FORMULA", "E=m*c^2"),
        make_step("E", c, 2, c_sq),
        make_step("M", mass, c_sq, energy),
    ]
    answer = f"E={energy} J"
    return steps, answer


def expected_mass(problem):
    momentum, mass = (
        int(value) for value in MASS_RE.fullmatch(problem).groups()
    )
    p_sq = momentum ** 2
    m_sq = mass ** 2
    e_sq = p_sq + m_sq
    energy = int(e_sq ** 0.5)
    assert energy * energy == e_sq
    steps = [
        make_step("REL_ENERGY_SETUP", "energy_momentum", "c=1",
                  f"p={momentum}, m={mass}"),
        make_step("REL_ENERGY_FORMULA", "E=sqrt(p^2+m^2)"),
        make_step("E", momentum, 2, p_sq),
        make_step("E", mass, 2, m_sq),
        make_step("A", p_sq, m_sq, e_sq),
        make_step("ROOT", f"sqrt({e_sq})", energy),
    ]
    answer = f"E={energy}"
    return steps, answer


def expected_velocity(problem):
    u_raw, v_raw = VELOCITY_RE.fullmatch(problem).groups()
    u = Fraction(u_raw)
    v = Fraction(v_raw)
    numerator = u + v
    product = u * v
    denominator = 1 + product
    velocity = numerator / denominator
    steps = [
        make_step("REL_ENERGY_SETUP", "velocity_addition",
                  f"u={fraction_text(u)}", f"v={fraction_text(v)}"),
        make_step("REL_ENERGY_FORMULA", "w=(u+v)/(1+u*v), c=1"),
        make_step("A", fraction_text(u), fraction_text(v),
                  fraction_text(numerator)),
        make_step("M", fraction_text(u), fraction_text(v),
                  fraction_text(product)),
        make_step("A", 1, fraction_text(product), fraction_text(denominator)),
        make_step("D", fraction_text(numerator), fraction_text(denominator),
                  fraction_text(velocity)),
    ]
    answer = f"w={fraction_text(velocity)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if REST_RE.fullmatch(problem):
        steps, answer = expected_rest(problem)
    elif MASS_RE.fullmatch(problem):
        steps, answer = expected_mass(problem)
    else:
        steps, answer = expected_velocity(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestRelativisticEnergyGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = RelativisticEnergyGenerator()

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
                    root = int(fields[2])
                    radicand = int(fields[1].removeprefix("sqrt(").rstrip(")"))
                    self.assertEqual(root * root, radicand, raw_step)

    def test_variants_are_available(self):
        for variant in RelativisticEnergyGenerator.VARIANTS:
            result = RelativisticEnergyGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"relativistic_energy_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RelativisticEnergyGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
