import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.method_of_moments_generator import (
    MethodOfMomentsGenerator,
    data_text,
    sum_expr,
)
from helpers import DELIM


POISSON_RE = re.compile(
    r"For data \[([0-9,]+)\] from a Poisson\(lambda\) model, use the "
    r"first moment equation to find the method-of-moments estimator "
    r"lambda_hat\."
)
EXP_RE = re.compile(
    r"For data \[([0-9,]+)\] from an Exponential\(lambda\) model, use "
    r"E\[X\]=1/lambda to find the method-of-moments estimator "
    r"lambda_hat\."
)
UNIFORM_RE = re.compile(
    r"For data \[([0-9,]+)\] from a Uniform\(0,theta\) model, use "
    r"E\[X\]=theta/2 to find the method-of-moments estimator theta_hat\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_values(raw):
    return [int(part) for part in raw.split(",")]


def summary_steps(model, parameter, values):
    n = len(values)
    total = sum(values)
    mean = Fraction(total, n)
    steps = [
        make_step("MOM_SETUP", model, f"parameter={parameter}",
                  f"data={data_text(values)}"),
        make_step("COUNT", "n", n),
        make_step("SUM", "sum x_i", sum_expr(values), total),
        make_step("D", total, n, fraction_text(mean)),
        make_step("SAMPLE_MOMENT", "xbar", fraction_text(mean)),
    ]
    return n, total, mean, steps


def expected_poisson(problem):
    values = parse_values(POISSON_RE.fullmatch(problem).group(1))
    _, _, mean, steps = summary_steps("poisson", "lambda", values)
    lambda_hat = mean
    steps += [
        make_step("MOM_EQUATION", "E[X]=lambda", "xbar=lambda"),
        make_step("REWRITE", f"lambda_hat={fraction_text(lambda_hat)}"),
        make_step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>=0",
                  "valid Poisson parameter"),
    ]
    answer = (
        f"xbar={fraction_text(mean)}; "
        f"lambda_hat={fraction_text(lambda_hat)}"
    )
    return steps, answer


def expected_exponential(problem):
    values = parse_values(EXP_RE.fullmatch(problem).group(1))
    n, total, mean, steps = summary_steps("exponential", "lambda", values)
    lambda_hat = Fraction(n, total)
    steps += [
        make_step("MOM_EQUATION", "E[X]=1/lambda", "xbar=1/lambda"),
        make_step("REWRITE", "lambda_hat=1/xbar"),
        make_step("D", n, total, fraction_text(lambda_hat)),
        make_step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>0",
                  "valid rate parameter"),
    ]
    answer = (
        f"xbar={fraction_text(mean)}; "
        f"lambda_hat={fraction_text(lambda_hat)}"
    )
    return steps, answer


def expected_uniform(problem):
    values = parse_values(UNIFORM_RE.fullmatch(problem).group(1))
    _, _, mean, steps = summary_steps("uniform_zero_theta", "theta", values)
    theta_hat = 2 * mean
    steps += [
        make_step("MOM_EQUATION", "E[X]=theta/2", "xbar=theta/2"),
        make_step("REWRITE", "theta_hat=2*xbar"),
        make_step("M", 2, fraction_text(mean), fraction_text(theta_hat)),
        make_step("CHECK", f"theta_hat={fraction_text(theta_hat)}>0",
                  "valid upper endpoint"),
    ]
    answer = (
        f"xbar={fraction_text(mean)}; "
        f"theta_hat={fraction_text(theta_hat)}"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if POISSON_RE.fullmatch(problem):
        steps, answer = expected_poisson(problem)
    elif EXP_RE.fullmatch(problem):
        steps, answer = expected_exponential(problem)
    else:
        steps, answer = expected_uniform(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMethodOfMomentsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MethodOfMomentsGenerator()

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
                if fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "SUM":
                    values = [int(v) for v in re.findall(r"\d+", fields[2])]
                    self.assertEqual(sum(values), int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in MethodOfMomentsGenerator.VARIANTS:
            result = MethodOfMomentsGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"method_of_moments_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MethodOfMomentsGenerator("bogus")

    def test_estimates_have_valid_domains(self):
        for variant in MethodOfMomentsGenerator.VARIANTS:
            gen = MethodOfMomentsGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                estimate = Fraction(result["final_answer"].rsplit("=", 1)[1])
                self.assertGreaterEqual(estimate, 0)
                if variant != "poisson":
                    self.assertGreater(estimate, 0)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
