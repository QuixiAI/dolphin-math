import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rotational_dynamics_generator import RotationalDynamicsGenerator
from helpers import DELIM


PARALLEL_RE = re.compile(
    r"A rigid body has center-of-mass moment of inertia I_cm=(\d+) "
    r"kg\*m\^2 and mass (\d+) kg\. Find the moment of inertia about a "
    r"parallel axis (\d+) m away\."
)
ANGULAR_RE = re.compile(
    r"A rotating system has moment of inertia I1=(\d+) kg\*m\^2 and "
    r"angular speed omega1=(\d+) rad/s\. Its moment of inertia changes to "
    r"I2=(\d+) kg\*m\^2 with no external torque\. Find the new angular "
    r"speed\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_parallel_axis(problem):
    inertia_cm, mass, distance = (
        int(value) for value in PARALLEL_RE.fullmatch(problem).groups()
    )
    distance_sq = distance ** 2
    added_inertia = mass * distance_sq
    inertia = inertia_cm + added_inertia
    check_cm = inertia - added_inertia
    steps = [
        make_step("ROT_SETUP", "parallel_axis",
                  f"I_cm={inertia_cm}, m={mass}", f"d={distance}"),
        make_step("ROT_FORMULA", "I=I_cm+m*d^2"),
        make_step("E", distance, 2, distance_sq),
        make_step("M", mass, distance_sq, added_inertia),
        make_step("A", inertia_cm, added_inertia, inertia),
        make_step("S", inertia, added_inertia, check_cm),
        make_step("CHECK", "recover I_cm", check_cm, f"given {inertia_cm}"),
    ]
    answer = f"I={inertia} kg*m^2"
    return steps, answer


def expected_angular_momentum(problem):
    inertia1, omega1, inertia2 = (
        int(value) for value in ANGULAR_RE.fullmatch(problem).groups()
    )
    angular_momentum = inertia1 * omega1
    omega2 = Fraction(angular_momentum, inertia2)
    check_l = inertia2 * omega2
    steps = [
        make_step("ROT_SETUP", "angular_momentum",
                  f"I1={inertia1}, omega1={omega1}", f"I2={inertia2}"),
        make_step("ROT_FORMULA", "I1*omega1=I2*omega2"),
        make_step("M", inertia1, omega1, angular_momentum),
        make_step("D", angular_momentum, inertia2, fraction_text(omega2)),
        make_step("M", inertia2, fraction_text(omega2),
                  fraction_text(check_l)),
        make_step("CHECK", "angular momentum", fraction_text(check_l),
                  f"initial {angular_momentum}"),
    ]
    answer = (
        f"omega2={fraction_text(omega2)} rad/s; "
        f"L={angular_momentum} kg*m^2/s"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if PARALLEL_RE.fullmatch(problem):
        steps, answer = expected_parallel_axis(problem)
    else:
        steps, answer = expected_angular_momentum(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestRotationalDynamicsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = RotationalDynamicsGenerator()

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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
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

    def test_checks_are_true(self):
        for _ in range(300):
            result = self.gen.generate()
            check = [raw for raw in result["steps"]
                     if raw.startswith(f"CHECK{DELIM}")][0]
            _, label, computed, target_text = check.split(DELIM)
            expected = target_text.removeprefix("given ")
            expected = expected.removeprefix("initial ")
            self.assertIn(label, ("recover I_cm", "angular momentum"))
            self.assertEqual(Fraction(computed), Fraction(expected), check)

    def test_variants_are_available(self):
        for variant in RotationalDynamicsGenerator.VARIANTS:
            result = RotationalDynamicsGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"rotational_dynamics_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RotationalDynamicsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
