import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.mle_generator import MLEGenerator, data_text, sum_expr
from helpers import DELIM


BERNOULLI_RE = re.compile(
    r"For Bernoulli data \[([0-1,]+)\], write the log-likelihood for p, "
    r"differentiate, and solve for the MLE p_hat\."
)
EXP_RE = re.compile(
    r"For exponential data \[([0-9,]+)\], write the log-likelihood for "
    r"lambda, differentiate, and solve for the MLE lambda_hat\."
)
NORMAL_RE = re.compile(
    r"For normal data \[([-0-9,]+)\] with known sigma\^2=(\d+), write "
    r"the log-likelihood for mu, differentiate, and solve for the MLE "
    r"mu_hat\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_values(raw):
    if raw == "":
        return []
    return [int(part) for part in raw.split(",")]


def expected_bernoulli(problem):
    values = parse_values(BERNOULLI_RE.fullmatch(problem).group(1))
    n = len(values)
    successes = sum(values)
    failures = n - successes
    p_hat = Fraction(successes, n)
    loglik = f"ell(p)={successes}*log(p)+{failures}*log(1-p)"
    score = f"score={successes}/p-{failures}/(1-p)"
    steps = [
        make_step("MLE_SETUP", "bernoulli", "parameter=p",
                  f"data={data_text(values)}"),
        make_step("COUNT", "n", n),
        make_step("COUNT", "sum x_i", successes),
        make_step("S", n, successes, failures),
        make_step("LOG_LIKELIHOOD", loglik),
        make_step("DERIVATIVE", score),
        make_step("SCORE_EQ", f"{successes}/p={failures}/(1-p)"),
        make_step("REWRITE", f"{successes}={n}*p"),
        make_step("D", successes, n, fraction_text(p_hat)),
        make_step("CHECK", f"0<={fraction_text(p_hat)}<=1",
                  "valid Bernoulli parameter"),
    ]
    answer = f"{loglik}; {score}; p_hat={fraction_text(p_hat)}"
    return steps, answer


def expected_exponential(problem):
    values = parse_values(EXP_RE.fullmatch(problem).group(1))
    n = len(values)
    total = sum(values)
    lambda_hat = Fraction(n, total)
    loglik = f"ell(lambda)={n}*log(lambda)-{total}*lambda"
    score = f"score={n}/lambda-{total}"
    steps = [
        make_step("MLE_SETUP", "exponential", "parameter=lambda",
                  f"data={data_text(values)}"),
        make_step("COUNT", "n", n),
        make_step("SUM", "sum x_i", sum_expr(values), total),
        make_step("LOG_LIKELIHOOD", loglik),
        make_step("DERIVATIVE", score),
        make_step("SCORE_EQ", f"{n}/lambda={total}"),
        make_step("D", n, total, fraction_text(lambda_hat)),
        make_step("CHECK", f"lambda_hat={fraction_text(lambda_hat)}>0",
                  "valid rate parameter"),
    ]
    answer = f"{loglik}; {score}; lambda_hat={fraction_text(lambda_hat)}"
    return steps, answer


def expected_normal(problem):
    match = NORMAL_RE.fullmatch(problem)
    values = parse_values(match.group(1))
    sigma_sq = int(match.group(2))
    n = len(values)
    total = sum(values)
    mu_hat = Fraction(total, n)
    loglik = f"ell(mu)=-(1/(2*{sigma_sq}))*sum((x_i-mu)^2)+C"
    score = f"score=({total}-{n}*mu)/{sigma_sq}"
    steps = [
        make_step("MLE_SETUP", "normal_mu", "parameter=mu",
                  f"sigma^2={sigma_sq}"),
        make_step("MLE_SETUP", "data", data_text(values)),
        make_step("COUNT", "n", n),
        make_step("SUM", "sum x_i", sum_expr(values), total),
        make_step("LOG_LIKELIHOOD", loglik),
        make_step("DERIVATIVE", score),
        make_step("SCORE_EQ", f"{total}-{n}*mu=0"),
        make_step("REWRITE", f"{total}={n}*mu"),
        make_step("D", total, n, fraction_text(mu_hat)),
        make_step("CHECK", "mu_hat can be any real number",
                  fraction_text(mu_hat)),
    ]
    answer = f"{loglik}; {score}; mu_hat={fraction_text(mu_hat)}"
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if BERNOULLI_RE.fullmatch(problem):
        steps, answer = expected_bernoulli(problem)
    elif EXP_RE.fullmatch(problem):
        steps, answer = expected_exponential(problem)
    else:
        steps, answer = expected_normal(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestMLEGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MLEGenerator()

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
                if fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "SUM":
                    values = [int(v) for v in re.findall(r"-?\d+", fields[2])]
                    self.assertEqual(sum(values), int(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in MLEGenerator.VARIANTS:
            result = MLEGenerator(variant).generate()
            self.assertEqual(result["operation"], f"mle_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            MLEGenerator("bogus")

    def test_estimates_are_valid(self):
        for variant in MLEGenerator.VARIANTS:
            gen = MLEGenerator(variant)
            for _ in range(100):
                result = gen.generate()
                estimate = Fraction(result["final_answer"].rsplit("=", 1)[1])
                if variant == "bernoulli":
                    self.assertGreaterEqual(estimate, 0)
                    self.assertLessEqual(estimate, 1)
                elif variant == "exponential":
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
