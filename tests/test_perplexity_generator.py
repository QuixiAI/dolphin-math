import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.perplexity_generator import PerplexityGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"For a sequence of ([0-9]+) tokens where each true-token probability "
    r"is p=1/([0-9]+), compute total negative log-likelihood, average "
    r"cross-entropy, and perplexity\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    tokens = int(match.group(1))
    denom = int(match.group(2))
    probability = Fraction(1, denom)
    steps = [
        make_step("PERPLEXITY_SETUP", f"tokens={tokens}", f"p=1/{denom}"),
        make_step("D", 1, denom, fraction_text(probability)),
        make_step("NEG_LOG", f"p={fraction_text(probability)}",
                  f"ln({denom})"),
        make_step("NLL", f"{tokens} tokens", f"{tokens}*ln({denom})"),
        make_step("CROSS_ENTROPY", "average", f"ln({denom})"),
        make_step("D", 1, fraction_text(probability), denom),
        make_step("PERPLEXITY", "exp(CE)", denom),
    ]
    answer = (
        f"total_nll={tokens}*ln({denom}); CE=ln({denom}); "
        f"perplexity={denom}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestPerplexityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PerplexityGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "perplexity_dyadic")
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

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
