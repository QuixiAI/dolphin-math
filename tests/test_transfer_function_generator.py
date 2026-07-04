import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.transfer_function_generator import (
    TransferFunctionGenerator,
    poly2_text,
)
from helpers import DELIM


ODE_RE = re.compile(
    r"With zero initial conditions, find the transfer function, zero, and "
    r"poles for y''\+(\d+)y'\+(\d+)y=(\d+)x'\+(\d+)x\."
)
BLOCK_RE = re.compile(
    r"Reduce a unity negative-feedback block diagram with G1=(\d+)/\(s\+(\d+)\) "
    r"and G2=(\d+)/\(s\+(\d+)\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def factor_pair(total, product):
    for p1 in range(1, total + 1):
        p2 = total - p1
        if p1 * p2 == product:
            return p1, p2
    raise AssertionError((total, product))


def expected_ode(problem):
    b_value, c_value, gain, numerator_constant = (
        int(value) for value in ODE_RE.fullmatch(problem).groups()
    )
    p1, p2 = factor_pair(b_value, c_value)
    zero = numerator_constant // gain
    numerator = f"{gain}s+{numerator_constant}"
    denominator = poly2_text(b_value, c_value)
    steps = [
        make_step("TF_SETUP", "ode",
                  f"y''+{b_value}y'+{c_value}y={gain}x'+{numerator_constant}x",
                  "zero initial conditions"),
        make_step("A", p1, p2, b_value),
        make_step("M", p1, p2, c_value),
        make_step("M", gain, zero, numerator_constant),
        make_step("LAPLACE", "Y terms", f"({denominator})Y(s)"),
        make_step("LAPLACE", "X terms", f"({numerator})X(s)"),
        make_step("TRANSFER", f"H(s)=({numerator})/({denominator})"),
        make_step("FACTOR", f"{denominator}=(s+{p1})(s+{p2})"),
        make_step("ZERO", f"s=-{zero}"),
        make_step("POLES", f"s=-{p1}, -{p2}"),
    ]
    answer = (
        f"H(s)=({numerator})/({denominator}); "
        f"zero=-{zero}; poles=-{p1},-{p2}"
    )
    return steps, answer


def expected_block(problem):
    a, p, b, q = (int(value) for value in BLOCK_RE.fullmatch(problem).groups())
    gain_product = a * b
    sum_pq = p + q
    product_pq = p * q
    closed_constant = product_pq + gain_product
    forward_den = poly2_text(sum_pq, product_pq)
    closed_den = poly2_text(sum_pq, closed_constant)
    steps = [
        make_step("TF_SETUP", "block_feedback",
                  f"G1={a}/(s+{p}), G2={b}/(s+{q})", "H=1"),
        make_step("SERIES", "G=G1*G2"),
        make_step("M", a, b, gain_product),
        make_step("A", p, q, sum_pq),
        make_step("M", p, q, product_pq),
        make_step("TRANSFER", f"G(s)={gain_product}/({forward_den})"),
        make_step("FEEDBACK", "T=G/(1+G)"),
        make_step("A", product_pq, gain_product, closed_constant),
        make_step("TRANSFER", f"T(s)={gain_product}/({closed_den})"),
    ]
    answer = f"T(s)={gain_product}/({closed_den})"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if ODE_RE.fullmatch(problem):
        steps, answer = expected_ode(problem)
    else:
        steps, answer = expected_block(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestTransferFunctionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = TransferFunctionGenerator()

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

    def test_variants_are_available(self):
        for variant in TransferFunctionGenerator.VARIANTS:
            result = TransferFunctionGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"transfer_function_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            TransferFunctionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
