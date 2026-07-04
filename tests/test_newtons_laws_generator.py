import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.newtons_laws_generator import NewtonsLawsGenerator
from helpers import DELIM


ATWOOD_RE = re.compile(
    r"An Atwood machine has masses m1=(\d+) kg and m2=(\d+) kg with m2 "
    r"heavier\. Use g=10 m/s\^2 to solve for acceleration and tension\."
)
INCLINE_RE = re.compile(
    r"A (\d+) kg block slides down an incline with supplied "
    r"sin\(theta\)=([^,]+), cos\(theta\)=([^,]+), and friction coefficient "
    r"mu=([^.]*)\. Use g=10 m/s\^2 to find normal force, friction, and "
    r"acceleration\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_atwood(problem):
    m1, m2 = (int(value) for value in ATWOOD_RE.fullmatch(problem).groups())
    g = 10
    mass_diff = m2 - m1
    force_diff = mass_diff * g
    total_mass = m1 + m2
    acceleration = Fraction(force_diff, total_mass)
    g_plus_a = Fraction(g) + acceleration
    tension = m1 * g_plus_a
    steps = [
        make_step("NEWTON_SETUP", "atwood", f"m1={m1}, m2={m2}", f"g={g}"),
        make_step("FORCE_EQ", "T-m1*g=m1*a"),
        make_step("FORCE_EQ", "m2*g-T=m2*a"),
        make_step("ELIMINATE", "(m2-m1)g=(m1+m2)a"),
        make_step("S", m2, m1, mass_diff),
        make_step("M", mass_diff, g, force_diff),
        make_step("A", m1, m2, total_mass),
        make_step("D", force_diff, total_mass, fraction_text(acceleration)),
        make_step("A", g, fraction_text(acceleration), fraction_text(g_plus_a)),
        make_step("M", m1, fraction_text(g_plus_a), fraction_text(tension)),
    ]
    answer = (
        f"a={fraction_text(acceleration)} m/s^2; "
        f"T={fraction_text(tension)} N"
    )
    return steps, answer


def expected_incline(problem):
    match = INCLINE_RE.fullmatch(problem)
    mass = int(match.group(1))
    sin_value = Fraction(match.group(2))
    cos_value = Fraction(match.group(3))
    mu = Fraction(match.group(4))
    g = 10
    weight = mass * g
    parallel = weight * sin_value
    normal = weight * cos_value
    friction = mu * normal
    net = parallel - friction
    acceleration = net / mass
    steps = [
        make_step("NEWTON_SETUP", "incline_friction",
                  f"m={mass}, mu={fraction_text(mu)}", f"g={g}"),
        make_step("NEWTON_SETUP", f"sin={fraction_text(sin_value)}",
                  f"cos={fraction_text(cos_value)}"),
        make_step("M", mass, g, weight),
        make_step("FORCE_COMPONENT", "parallel=m*g*sin"),
        make_step("M", weight, fraction_text(sin_value),
                  fraction_text(parallel)),
        make_step("FORCE_COMPONENT", "normal=m*g*cos"),
        make_step("M", weight, fraction_text(cos_value),
                  fraction_text(normal)),
        make_step("FORCE_COMPONENT", "friction=mu*N"),
        make_step("M", fraction_text(mu), fraction_text(normal),
                  fraction_text(friction)),
        make_step("FORCE_EQ", "m*a=parallel-friction"),
        make_step("S", fraction_text(parallel), fraction_text(friction),
                  fraction_text(net)),
        make_step("D", fraction_text(net), mass, fraction_text(acceleration)),
    ]
    answer = (
        f"N={fraction_text(normal)} N; friction={fraction_text(friction)} N; "
        f"a={fraction_text(acceleration)} m/s^2"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if ATWOOD_RE.fullmatch(problem):
        steps, answer = expected_atwood(problem)
    else:
        steps, answer = expected_incline(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestNewtonsLawsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = NewtonsLawsGenerator()

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

    def test_variants_are_available(self):
        for variant in NewtonsLawsGenerator.VARIANTS:
            result = NewtonsLawsGenerator(variant).generate()
            self.assertEqual(result["operation"], f"newtons_laws_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NewtonsLawsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
