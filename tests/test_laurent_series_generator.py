import ast
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.laurent_series_generator import LaurentSeriesGenerator
from helpers import DELIM


POLE_RE = re.compile(
    r"Find the Laurent coefficients c_n for n=(-?\d+)\.\.(-?\d+) "
    r"about z=(-?\d+) of f\(z\) = (.+)\. The numerator coefficients "
    r"in powers of (.+) are (\[[^]]+\])\."
)
GEOMETRIC_RE = re.compile(
    r"Find the Taylor coefficients c_n for n=0\.\.(\d+) about z=(-?\d+) "
    r"of f\(z\) = (.+), written as sum c_n (.+)\^n\."
)
RATIONAL_RE = re.compile(r"(-?\d+)/(z|\(z[+-]\d+\))")


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def z_minus(a):
    if a == 0:
        return "z"
    if a > 0:
        return f"(z-{a})"
    return f"(z+{-a})"


def poly_text(coeffs, base):
    parts = []
    for power, coef in enumerate(coeffs):
        if coef == 0:
            continue
        abs_coef = abs(coef)
        if power == 0:
            body = str(abs_coef)
        elif power == 1:
            body = base if abs_coef == 1 else f"{abs_coef}{base}"
        else:
            body = f"{base}^{power}" if abs_coef == 1 else \
                f"{abs_coef}{base}^{power}"
        if not parts:
            parts.append(body if coef > 0 else f"-{body}")
        else:
            parts.append(f"+ {body}" if coef > 0 else f"- {body}")
    return " ".join(parts) if parts else "0"


def signed_term(value):
    return f"+ {value}" if value >= 0 else f"- {-value}"


def parse_pole(denominator):
    if denominator == "z":
        return 0
    body = denominator.strip("()")
    if "+" in body:
        return -int(body.split("+")[1])
    return int(body.split("-")[1])


def denominator_text(pole):
    return z_minus(pole)


def coefficient_answer(coeffs):
    return ", ".join(f"c_{power}={Fraction(value)}"
                     for power, value in coeffs)


def parse_problem(problem):
    match = POLE_RE.fullmatch(problem)
    if match:
        lo = int(match.group(1))
        hi = int(match.group(2))
        a = int(match.group(3))
        function = match.group(4)
        base = match.group(5)
        coeffs = ast.literal_eval(match.group(6))
        return {"variant": "pole", "lo": lo, "hi": hi, "a": a,
                "function": function, "base": base, "coeffs": coeffs}

    match = GEOMETRIC_RE.fullmatch(problem)
    assert match is not None, problem
    degree = int(match.group(1))
    a = int(match.group(2))
    function = match.group(3)
    base = match.group(4)
    rational = RATIONAL_RE.fullmatch(function)
    assert rational is not None, problem
    numerator = int(rational.group(1))
    pole = parse_pole(rational.group(2))
    return {"variant": "geometric", "degree": degree, "a": a,
            "function": function, "base": base, "numerator": numerator,
            "pole": pole}


def expected_pole(parts):
    order = -parts["lo"]
    coeffs = parts["coeffs"]
    function = f"({poly_text(coeffs, parts['base'])})/{parts['base']}^{order}"
    steps = [
        make_step("LAURENT_SETUP", f"center a={parts['a']}",
                  f"w={parts['base']}", f"f={function}"),
        make_step("REWRITE", f"f = numerator/w^{order}",
                  f"numerator power k gives c_(k-{order})"),
    ]
    answer_terms = []
    for power, coef in enumerate(coeffs):
        laurent_power = power - order
        steps.append(make_step("POWER_SHIFT", f"k={power}",
                               f"{power}-{order}", laurent_power))
        steps.append(make_step("COEFF", f"c_{laurent_power}", coef))
        answer_terms.append((laurent_power, coef))
    answer = coefficient_answer(answer_terms)
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_geometric(parts):
    d = parts["a"] - parts["pole"]
    steps = [
        make_step("LAURENT_SETUP", f"center a={parts['a']}",
                  f"w={parts['base']}", f"f={parts['function']}"),
        make_step("REWRITE", f"{denominator_text(parts['pole'])} = "
                  f"w {signed_term(d)}", f"d=a-b={d}"),
        make_step("GEOMETRIC_FORMULA",
                  "c_n = A*(-1)^n/d^(n+1)",
                  f"A={parts['numerator']}, d={d}"),
    ]
    answer_terms = []
    for n in range(parts["degree"] + 1):
        sign = -1 if n % 2 else 1
        denominator_power = d ** (n + 1)
        signed_numerator = parts["numerator"] * sign
        coef = Fraction(signed_numerator, denominator_power)
        steps.append(make_step("E", d, n + 1, denominator_power))
        steps.append(make_step("M", parts["numerator"], sign,
                               signed_numerator))
        steps.append(make_step("D", signed_numerator, denominator_power,
                               coef))
        steps.append(make_step("COEFF", f"c_{n}", coef))
        answer_terms.append((n, coef))
    answer = coefficient_answer(answer_terms)
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "pole":
        return expected_pole(parts)
    return expected_geometric(parts)


class TestLaurentSeriesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = LaurentSeriesGenerator()

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

    def test_geometric_coefficients_match_closed_form(self):
        gen = LaurentSeriesGenerator("geometric")
        for _ in range(200):
            result = gen.generate()
            parts = parse_problem(result["problem"])
            d = parts["a"] - parts["pole"]
            coeffs = [
                (n, Fraction(parts["numerator"] * ((-1) ** n),
                             d ** (n + 1)))
                for n in range(parts["degree"] + 1)
            ]
            self.assertEqual(result["final_answer"],
                             coefficient_answer(coeffs))

    def test_arithmetic_steps(self):
        gen = LaurentSeriesGenerator("geometric")
        for _ in range(200):
            result = gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(int(fields[1]),
                                              int(fields[2])),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in ("pole", "geometric"):
            gen = LaurentSeriesGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"laurent_series_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            LaurentSeriesGenerator("bogus")

    def test_no_degenerate_rendering_or_extra_pipes(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join([result["problem"]] + result["steps"])
            for bad in ("+ -", "--", "^1"):
                self.assertNotIn(bad, joined)
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
