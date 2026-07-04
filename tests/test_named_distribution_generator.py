import math
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.named_distribution_generator import NamedDistributionGenerator
from helpers import DELIM


POISSON_RE = re.compile(
    r"For X~Poisson\(lambda=(\d+)\), use supplied e\^-lambda=([^ ]+) "
    r"to compute P\(X=(\d+)\)\."
)
EXP_RE = re.compile(
    r"For an exponential random variable, use supplied "
    r"e\^\(-lambda\*t\)=([^ ]+) to compute P\(X<t\)\."
)
UNIFORM_RE = re.compile(
    r"For X~Uniform\((-?\d+),(-?\d+)\), compute P\((-?\d+)<X<(-?\d+)\), "
    r"mean, and variance\."
)
NORMAL_RE = re.compile(
    r"For X~Normal\(mu=(-?\d+), sigma=(\d+)\), compute P\(X<(-?\d+)\)\. "
    r"Use supplied Phi\((-?\d+)\)=([^ ]+)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = POISSON_RE.fullmatch(problem)
    if match:
        return {
            "variant": "poisson",
            "lam": int(match.group(1)),
            "exp_value": Fraction(match.group(2)),
            "k": int(match.group(3)),
        }
    match = EXP_RE.fullmatch(problem)
    if match:
        return {"variant": "exponential",
                "exp_value": Fraction(match.group(1))}
    match = UNIFORM_RE.fullmatch(problem)
    if match:
        return {
            "variant": "uniform",
            "low": int(match.group(1)),
            "high": int(match.group(2)),
            "left": int(match.group(3)),
            "right": int(match.group(4)),
        }
    match = NORMAL_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "normal",
        "mu": int(match.group(1)),
        "sigma": int(match.group(2)),
        "x": int(match.group(3)),
        "z": int(match.group(4)),
        "phi": Fraction(match.group(5)),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "poisson":
        lam = parts["lam"]
        k = parts["k"]
        exp_value = parts["exp_value"]
        power = lam ** k
        fact = math.factorial(k)
        numerator = exp_value * power
        probability = numerator / fact
        steps = [
            make_step("DIST_SETUP", "poisson", f"lambda={lam}", f"k={k}"),
            make_step("LOOKUP_SUPPLIED", f"e^-{lam}",
                      fraction_text(exp_value)),
            make_step("E", lam, k, power),
            make_step("FACT", k, fact),
            make_step("M", fraction_text(exp_value), power,
                      fraction_text(numerator)),
            make_step("D", fraction_text(numerator), fact,
                      fraction_text(probability)),
        ]
        answer = f"P(X={k}) = {fraction_text(probability)}"
    elif parts["variant"] == "exponential":
        exp_value = parts["exp_value"]
        probability = 1 - exp_value
        steps = [
            make_step("DIST_SETUP", "exponential", "target=P(X<t)",
                      f"e^(-lambda*t)={fraction_text(exp_value)}"),
            make_step("LOOKUP_SUPPLIED", "e^(-lambda*t)",
                      fraction_text(exp_value)),
            make_step("S", 1, fraction_text(exp_value),
                      fraction_text(probability)),
        ]
        answer = f"P(X<t) = {fraction_text(probability)}"
    elif parts["variant"] == "uniform":
        low = parts["low"]
        high = parts["high"]
        left = parts["left"]
        right = parts["right"]
        interval = high - low
        favorable = right - left
        probability = Fraction(favorable, interval)
        mean_num = low + high
        mean = Fraction(mean_num, 2)
        width_sq = interval ** 2
        variance = Fraction(width_sq, 12)
        steps = [
            make_step("DIST_SETUP", "uniform", f"[{low},{high}]",
                      f"interval=({left},{right})"),
            make_step("S", high, low, interval),
            make_step("S", right, left, favorable),
            make_step("D", favorable, interval, fraction_text(probability)),
            make_step("A", low, high, mean_num),
            make_step("D", mean_num, 2, fraction_text(mean)),
            make_step("E", interval, 2, width_sq),
            make_step("D", width_sq, 12, fraction_text(variance)),
        ]
        answer = (
            f"P = {fraction_text(probability)}, mean = {fraction_text(mean)}, "
            f"variance = {fraction_text(variance)}"
        )
    else:
        mu = parts["mu"]
        sigma = parts["sigma"]
        x_value = parts["x"]
        z = parts["z"]
        phi = parts["phi"]
        diff = x_value - mu
        steps = [
            make_step("DIST_SETUP", "normal", f"mu={mu},sigma={sigma}",
                      f"x={x_value}"),
            make_step("S", x_value, mu, diff),
            make_step("D", diff, sigma, z),
            make_step("LOOKUP_SUPPLIED", f"Phi({z})", fraction_text(phi)),
        ]
        answer = f"P(X<{x_value}) = {fraction_text(phi)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestNamedDistributionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = NamedDistributionGenerator()

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
                if fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "E":
                    self.assertEqual(int(fields[1]) ** int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "FACT":
                    self.assertEqual(math.factorial(int(fields[1])),
                                     int(fields[2]), raw_step)

    def test_variants_are_available(self):
        for variant in NamedDistributionGenerator.VARIANTS:
            result = NamedDistributionGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"named_distribution_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            NamedDistributionGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
