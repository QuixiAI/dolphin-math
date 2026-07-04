import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.line_integral_generator import LineIntegralGenerator
from helpers import DELIM


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_linear(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        if body:
            text = body if abs(coeff) == 1 else f"{abs(coeff)}*{body}"
        else:
            text = str(abs(coeff))
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def fmt_quadratic(a, b, c, d, e):
    return fmt_linear([
        (a, "x^2"),
        (b, "y^2"),
        (c, "x*y"),
        (d, "x"),
        (e, "y"),
    ])


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_linear(expr):
    coeffs = {"x": 0, "y": 0}
    const = 0
    for raw in split_terms(expr):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        coeff = sign
        var = None
        for factor in raw.split("*"):
            if factor.isdigit():
                coeff *= int(factor)
            elif factor in coeffs:
                var = factor
            else:
                raise AssertionError(f"bad factor {factor!r} in {expr!r}")
        if var is None:
            const += coeff
        else:
            coeffs[var] += coeff
    return coeffs["x"], coeffs["y"], const


def phi_value(a, b, c, d, e, x, y):
    return a * x * x + b * y * y + c * x * y + d * x + e * y


def oracle_answer(example):
    problem = example["problem"]
    if problem.startswith("Compute"):
        p_txt, q_txt, x0, y0, x1, y1 = re.fullmatch(
            r"Compute the work integral of F\(x,y\) = <(.+), (.+)> "
            r"along the line segment from \((-?\d+), (-?\d+)\) to "
            r"\((-?\d+), (-?\d+)\)\.",
            problem,
        ).groups()
        px, py, _ = parse_linear(p_txt)
        qx, qy, _ = parse_linear(q_txt)
        x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
        dx = x1 - x0
        dy = y1 - y0
        p_t_coeff = px * dx + py * dy
        p_t_const = px * x0 + py * y0
        q_t_coeff = qx * dx + qy * dy
        q_t_const = qx * x0 + qy * y0
        dot_t_coeff = p_t_coeff * dx + q_t_coeff * dy
        dot_t_const = p_t_const * dx + q_t_const * dy
        work = Fraction(dot_t_coeff, 2) + dot_t_const
        return f"work {fmt_frac(work)}"

    p_txt, q_txt, x0, y0, x1, y1 = re.fullmatch(
        r"For F\(x,y\) = <(.+), (.+)>, find a potential function and "
        r"compute the work from \((-?\d+), (-?\d+)\) to "
        r"\((-?\d+), (-?\d+)\)\.",
        problem,
    ).groups()
    px, py, d = parse_linear(p_txt)
    qx, qy, e = parse_linear(q_txt)
    assert py == qx
    a = px // 2
    b = qy // 2
    c = py
    x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    phi = fmt_quadratic(a, b, c, d, e)
    work = (phi_value(a, b, c, d, e, x1, y1) -
            phi_value(a, b, c, d, e, x0, y0))
    return f"potential {phi}; work {work}"


def eval_fraction_expr(expr):
    expr = re.sub(r"-?\d+", lambda m: f"Fraction({m.group(0)})", expr)
    return eval(expr, {"__builtins__": {}, "Fraction": Fraction}, {})


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] in {"LINE_INTEGRAL", "WORK_DIFF"}:
            if eval_fraction_expr(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "CHECK" and parts[3] != "conservative":
            return False
    return True


class TestLineIntegralGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LineIntegralGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variant_outputs(self):
        cases = {
            "segment_work": "work ",
            "potential_work": "potential ",
        }
        for variant, phrase in cases.items():
            gen = LineIntegralGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertTrue(result["final_answer"].startswith(phrase))

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ 0|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            LineIntegralGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
