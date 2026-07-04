import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.rv_transform_generator import RVTransformGenerator
from helpers import DELIM


CDF_RE = re.compile(
    r"Let X~Uniform\(0,(\d+)\) and Y=X\^2\. Use the CDF method to find "
    r"F_Y\(y\), f_Y\(y\), and F_Y\((\d+)\)\."
)
JAC_RE = re.compile(
    r"Let X,Y be independent Uniform\(0,(\d+)\)\. Define U=X\+Y and "
    r"V=X-Y\. Use the Jacobian method to find the inverse map, "
    r"transformed support, density f_UV\(u,v\), and f_UV at the point "
    r"produced by x=(\d+), y=(\d+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_cdf(problem):
    a, y0 = (int(v) for v in CDF_RE.fullmatch(problem).groups())
    s = int(y0 ** 0.5)
    assert s * s == y0
    a_sq = a ** 2
    density = Fraction(1, a)
    cdf_value = Fraction(s, a)
    cdf_formula = f"sqrt(y)/{a}"
    pdf_formula = f"1/({2 * a}*sqrt(y))"
    steps = [
        make_step("TRANSFORM_SETUP", "cdf", f"X~Uniform(0,{a})", "Y=X^2"),
        make_step("DENSITY", "f_X(x)", f"1/{a}"),
        make_step("D", 1, a, fraction_text(density)),
        make_step("E", a, 2, a_sq),
        make_step("SUPPORT", f"0<=x<={a}", f"0<=y<={a_sq}"),
        make_step("CDF_EVENT", "Y<=y", "X^2<=y", "X<=sqrt(y)"),
        make_step("CDF_FORMULA", f"F_Y(y)={cdf_formula}",
                  f"0<=y<={a_sq}"),
        make_step("PDF_FORMULA", f"f_Y(y)={pdf_formula}"),
        make_step("E", s, 2, y0),
        make_step("ROOT", y0, s),
        make_step("D", s, a, fraction_text(cdf_value)),
    ]
    answer = (
        f"support=0<=y<={a_sq}; F_Y(y)={cdf_formula}; "
        f"f_Y(y)={pdf_formula}; F_Y({y0})={fraction_text(cdf_value)}"
    )
    return steps, answer


def expected_jacobian(problem):
    a, x_value, y_value = (int(v) for v in JAC_RE.fullmatch(problem).groups())
    a_sq = a ** 2
    original_density = Fraction(1, a_sq)
    half = Fraction(1, 2)
    det_left = half * -half
    det_right = half * half
    det = det_left - det_right
    abs_det = abs(det)
    transformed_density = original_density * abs_det
    two_a = 2 * a
    u_value = x_value + y_value
    v_value = x_value - y_value
    u_plus_v = u_value + v_value
    u_minus_v = u_value - v_value
    steps = [
        make_step("TRANSFORM_SETUP", "jacobian",
                  f"X,Y~Uniform(0,{a})", "U=X+Y,V=X-Y"),
        make_step("DENSITY", "f_XY(x,y)", f"1/{a}^2"),
        make_step("E", a, 2, a_sq),
        make_step("D", 1, a_sq, fraction_text(original_density)),
        make_step("INVERSE_MAP", "x=(u+v)/2", "y=(u-v)/2"),
        make_step("D", 1, 2, fraction_text(half)),
        make_step("JAC_MATRIX", "dx/du=1/2, dx/dv=1/2",
                  "dy/du=1/2, dy/dv=-1/2"),
        make_step("M", fraction_text(half), fraction_text(-half),
                  fraction_text(det_left)),
        make_step("M", fraction_text(half), fraction_text(half),
                  fraction_text(det_right)),
        make_step("S", fraction_text(det_left), fraction_text(det_right),
                  fraction_text(det)),
        make_step("ABS", fraction_text(det), fraction_text(abs_det)),
        make_step("M", fraction_text(original_density), fraction_text(abs_det),
                  fraction_text(transformed_density)),
        make_step("M", 2, a, two_a),
        make_step("SUPPORT", f"0<=u+v<={two_a}",
                  f"0<=u-v<={two_a}"),
        make_step("A", x_value, y_value, u_value),
        make_step("S", x_value, y_value, v_value),
        make_step("A", u_value, v_value, u_plus_v),
        make_step("S", u_value, v_value, u_minus_v),
        make_step("CHECK", f"u+v={u_plus_v}", f"u-v={u_minus_v}",
                  "in support"),
    ]
    answer = (
        "inverse x=(u+v)/2, y=(u-v)/2; "
        f"support=0<=u+v<={two_a} and 0<=u-v<={two_a}; "
        f"absJ={fraction_text(abs_det)}; "
        f"f_UV(u,v)={fraction_text(transformed_density)}; "
        f"f_UV({u_value},{v_value})={fraction_text(transformed_density)}"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if CDF_RE.fullmatch(problem):
        steps, answer = expected_cdf(problem)
    else:
        steps, answer = expected_jacobian(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestRVTransformGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = RVTransformGenerator()

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
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "ROOT":
                    self.assertEqual(int(fields[2]) ** 2, int(fields[1]),
                                     raw_step)
                elif fields[0] == "ABS":
                    self.assertEqual(abs(Fraction(fields[1])),
                                     Fraction(fields[2]), raw_step)

    def test_variants_are_available(self):
        for variant in RVTransformGenerator.VARIANTS:
            result = RVTransformGenerator(variant).generate()
            self.assertEqual(result["operation"], f"rv_transform_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["steps"][-1],
                             make_step("Z", answer))
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            RVTransformGenerator("bogus")

    def test_enough_unique_problems_for_sampling(self):
        problems = {self.gen.generate()["problem"] for _ in range(500)}
        self.assertGreaterEqual(len(problems), 200)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
