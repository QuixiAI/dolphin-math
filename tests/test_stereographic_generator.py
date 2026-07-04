import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.stereographic_generator import StereographicGenerator
from helpers import DELIM


PLANE_RE = re.compile(
    r"Map plane point \(u,v\)=\(([^,]+),([^)]+)\) to the unit sphere "
    r"by stereographic projection from the north pole\."
)
SPHERE_RE = re.compile(
    r"Map sphere point \(X,Y,Z\)=\(([^,]+),([^,]+),([^)]+)\) with "
    r"Z != 1 to the plane by inverse stereographic projection from "
    r"the north pole\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def sphere_from_plane(u, v):
    u2 = u ** 2
    v2 = v ** 2
    sum_sq = u2 + v2
    denom = sum_sq + 1
    x = 2 * u / denom
    y = 2 * v / denom
    z = (sum_sq - 1) / denom
    return x, y, z, u2, v2, sum_sq, denom


def parse_problem(problem):
    match = PLANE_RE.fullmatch(problem)
    if match:
        return {"variant": "plane_to_sphere",
                "u": Fraction(match.group(1)),
                "v": Fraction(match.group(2))}
    match = SPHERE_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "sphere_to_plane",
            "x": Fraction(match.group(1)),
            "y": Fraction(match.group(2)),
            "z": Fraction(match.group(3))}


def expected_plane(parts):
    u = parts["u"]
    v = parts["v"]
    x, y, z, u2, v2, sum_sq, denom = sphere_from_plane(u, v)
    two_u = 2 * u
    two_v = 2 * v
    z_num = sum_sq - 1
    x2 = x ** 2
    y2 = y ** 2
    z2 = z ** 2
    xy_sq = x2 + y2
    unit_sum = xy_sq + z2
    answer = (
        f"sphere point = ({fraction_text(x)}, {fraction_text(y)}, "
        f"{fraction_text(z)})"
    )
    steps = [
        make_step("STEREO_SETUP", "plane_to_sphere",
                  f"u={fraction_text(u)}", f"v={fraction_text(v)}"),
        make_step("FORMULA",
                  "D=u^2+v^2+1; X=2u/D; Y=2v/D; Z=(u^2+v^2-1)/D"),
        make_step("E", fraction_text(u), 2, fraction_text(u2)),
        make_step("E", fraction_text(v), 2, fraction_text(v2)),
        make_step("A", fraction_text(u2), fraction_text(v2),
                  fraction_text(sum_sq)),
        make_step("A", fraction_text(sum_sq), 1, fraction_text(denom)),
        make_step("M", 2, fraction_text(u), fraction_text(two_u)),
        make_step("D", fraction_text(two_u), fraction_text(denom),
                  fraction_text(x)),
        make_step("M", 2, fraction_text(v), fraction_text(two_v)),
        make_step("D", fraction_text(two_v), fraction_text(denom),
                  fraction_text(y)),
        make_step("S", fraction_text(sum_sq), 1, fraction_text(z_num)),
        make_step("D", fraction_text(z_num), fraction_text(denom),
                  fraction_text(z)),
        make_step("E", fraction_text(x), 2, fraction_text(x2)),
        make_step("E", fraction_text(y), 2, fraction_text(y2)),
        make_step("E", fraction_text(z), 2, fraction_text(z2)),
        make_step("A", fraction_text(x2), fraction_text(y2),
                  fraction_text(xy_sq)),
        make_step("A", fraction_text(xy_sq), fraction_text(z2),
                  fraction_text(unit_sum)),
        make_step("CHECK", "X^2+Y^2+Z^2", fraction_text(unit_sum),
                  "unit sphere"),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_sphere(parts):
    denom = 1 - parts["z"]
    u = parts["x"] / denom
    v = parts["y"] / denom
    answer = f"plane point = ({fraction_text(u)}, {fraction_text(v)})"
    steps = [
        make_step("STEREO_SETUP", "sphere_to_plane",
                  f"X={fraction_text(parts['x'])}",
                  f"Y={fraction_text(parts['y'])}",
                  f"Z={fraction_text(parts['z'])}"),
        make_step("FORMULA", "u=X/(1-Z); v=Y/(1-Z)"),
        make_step("S", 1, fraction_text(parts["z"]), fraction_text(denom)),
        make_step("D", fraction_text(parts["x"]), fraction_text(denom),
                  fraction_text(u)),
        make_step("D", fraction_text(parts["y"]), fraction_text(denom),
                  fraction_text(v)),
        make_step("Z", answer),
    ]
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "plane_to_sphere":
        return expected_plane(parts)
    return expected_sphere(parts)


class TestStereographicGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = StereographicGenerator()

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

    def test_variants_are_available(self):
        for variant in ("plane_to_sphere", "sphere_to_plane"):
            gen = StereographicGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"stereographic_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            StereographicGenerator("bogus")

    def test_unit_sphere_check(self):
        gen = StereographicGenerator("plane_to_sphere")
        for _ in range(200):
            result = gen.generate()
            check = [s for s in result["steps"]
                     if s.startswith(f"CHECK{DELIM}")][-1]
            self.assertEqual(check.split(DELIM)[2], "1")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
