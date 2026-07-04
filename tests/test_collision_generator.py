import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.collision_generator import CollisionGenerator
from helpers import DELIM


INELASTIC_1D_RE = re.compile(
    r"In a 1D perfectly inelastic collision, m1=(\d+) kg has u1=(-?\d+) "
    r"m/s and m2=(\d+) kg has u2=(-?\d+) m/s\. Find the common final "
    r"velocity\."
)
ELASTIC_1D_RE = re.compile(
    r"In a 1D elastic collision, m1=(\d+) kg has u1=(-?\d+) m/s and "
    r"m2=(\d+) kg has u2=(-?\d+) m/s\. Find final velocities v1 and v2\."
)
INELASTIC_2D_RE = re.compile(
    r"In a 2D perfectly inelastic collision, m1=(\d+) kg has "
    r"v1=\((-?\d+),(-?\d+)\) m/s and m2=(\d+) kg has "
    r"v2=\((-?\d+),(-?\d+)\) m/s\. Find the common final velocity vector\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_inelastic_1d(problem):
    m1, u1, m2, u2 = (
        int(value) for value in INELASTIC_1D_RE.fullmatch(problem).groups()
    )
    p1 = m1 * u1
    p2 = m2 * u2
    total_p = p1 + p2
    total_m = m1 + m2
    v = Fraction(total_p, total_m)
    steps = [
        make_step("COLLISION_SETUP", "inelastic_1d",
                  f"m1={m1}, u1={u1}", f"m2={m2}, u2={u2}"),
        make_step("MOMENTUM", "p1=m1*u1"),
        make_step("M", m1, u1, p1),
        make_step("MOMENTUM", "p2=m2*u2"),
        make_step("M", m2, u2, p2),
        make_step("A", p1, p2, total_p),
        make_step("A", m1, m2, total_m),
        make_step("FORMULA", "v=(p1+p2)/(m1+m2)"),
        make_step("D", total_p, total_m, fraction_text(v)),
    ]
    answer = f"stuck-together velocity={fraction_text(v)} m/s"
    return steps, answer


def expected_elastic_1d(problem):
    m1, u1, m2, u2 = (
        int(value) for value in ELASTIC_1D_RE.fullmatch(problem).groups()
    )
    total_m = m1 + m2
    diff12 = m1 - m2
    diff21 = m2 - m1
    two_m2 = 2 * m2
    two_m1 = 2 * m1
    v1_num_part1 = diff12 * u1
    v1_num_part2 = two_m2 * u2
    v1_num = v1_num_part1 + v1_num_part2
    v2_num_part1 = two_m1 * u1
    v2_num_part2 = diff21 * u2
    v2_num = v2_num_part1 + v2_num_part2
    v1 = Fraction(v1_num, total_m)
    v2 = Fraction(v2_num, total_m)
    steps = [
        make_step("COLLISION_SETUP", "elastic_1d",
                  f"m1={m1}, u1={u1}", f"m2={m2}, u2={u2}"),
        make_step("A", m1, m2, total_m),
        make_step("FORMULA", "v1=((m1-m2)u1+2m2u2)/(m1+m2)"),
        make_step("S", m1, m2, diff12),
        make_step("M", diff12, u1, v1_num_part1),
        make_step("M", 2, m2, two_m2),
        make_step("M", two_m2, u2, v1_num_part2),
        make_step("A", v1_num_part1, v1_num_part2, v1_num),
        make_step("D", v1_num, total_m, fraction_text(v1)),
        make_step("FORMULA", "v2=(2m1u1+(m2-m1)u2)/(m1+m2)"),
        make_step("M", 2, m1, two_m1),
        make_step("M", two_m1, u1, v2_num_part1),
        make_step("S", m2, m1, diff21),
        make_step("M", diff21, u2, v2_num_part2),
        make_step("A", v2_num_part1, v2_num_part2, v2_num),
        make_step("D", v2_num, total_m, fraction_text(v2)),
    ]
    answer = f"v1={fraction_text(v1)} m/s; v2={fraction_text(v2)} m/s"
    return steps, answer


def expected_inelastic_2d(problem):
    m1, v1x, v1y, m2, v2x, v2y = (
        int(value) for value in INELASTIC_2D_RE.fullmatch(problem).groups()
    )
    p1x = m1 * v1x
    p2x = m2 * v2x
    px = p1x + p2x
    p1y = m1 * v1y
    p2y = m2 * v2y
    py = p1y + p2y
    total_m = m1 + m2
    vx = Fraction(px, total_m)
    vy = Fraction(py, total_m)
    steps = [
        make_step("COLLISION_SETUP", "inelastic_2d",
                  f"m1={m1}, v1=({v1x},{v1y})",
                  f"m2={m2}, v2=({v2x},{v2y})"),
        make_step("MOMENTUM", "x components"),
        make_step("M", m1, v1x, p1x),
        make_step("M", m2, v2x, p2x),
        make_step("A", p1x, p2x, px),
        make_step("MOMENTUM", "y components"),
        make_step("M", m1, v1y, p1y),
        make_step("M", m2, v2y, p2y),
        make_step("A", p1y, p2y, py),
        make_step("A", m1, m2, total_m),
        make_step("D", px, total_m, fraction_text(vx)),
        make_step("D", py, total_m, fraction_text(vy)),
    ]
    answer = (
        f"stuck-together velocity=({fraction_text(vx)},"
        f"{fraction_text(vy)}) m/s"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if INELASTIC_1D_RE.fullmatch(problem):
        steps, answer = expected_inelastic_1d(problem)
    elif ELASTIC_1D_RE.fullmatch(problem):
        steps, answer = expected_elastic_1d(problem)
    else:
        steps, answer = expected_inelastic_2d(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestCollisionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = CollisionGenerator()

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
        for variant in CollisionGenerator.VARIANTS:
            result = CollisionGenerator(variant).generate()
            self.assertEqual(result["operation"], f"collision_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            CollisionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
