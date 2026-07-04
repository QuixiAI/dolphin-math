import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.index_raising_generator import IndexRaisingGenerator
from helpers import DELIM


LOWER_RE = re.compile(
    r"Lower v\^i=(\[[^\]]+\]) using the diagonal (\w+) metric "
    r"g_ii=(\[[^\]]+\])\."
)
RAISE_RE = re.compile(
    r"Raise w_i=(\[[^\]]+\]) using the diagonal (\w+) inverse metric "
    r"g\^ii=(\[[^\]]+\])\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_vector(text):
    return [Fraction(value) for value in text.strip("[]").split(",")]


def fraction_text(value):
    return str(Fraction(value))


def vector_text(values):
    return "[" + ",".join(fraction_text(value) for value in values) + "]"


def parse_problem(problem):
    match = LOWER_RE.fullmatch(problem)
    if match:
        return {
            "variant": "lower",
            "components": parse_vector(match.group(1)),
            "metric_name": match.group(2),
            "diag": parse_vector(match.group(3)),
        }
    match = RAISE_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "raise",
        "components": parse_vector(match.group(1)),
        "metric_name": match.group(2),
        "diag": parse_vector(match.group(3)),
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    action = parts["variant"]
    metric_field = "g_ii" if action == "lower" else "g^ii"
    result_name = "v_i" if action == "lower" else "w^i"
    entry_prefix = "v_" if action == "lower" else "w^"
    result = [
        factor * value
        for factor, value in zip(parts["diag"], parts["components"])
    ]
    steps = [
        make_step("INDEX_METRIC", action, parts["metric_name"],
                  f"{metric_field}={vector_text(parts['diag'])}"),
    ]
    for idx, (factor, value, out) in enumerate(
        zip(parts["diag"], parts["components"], result), start=1
    ):
        steps.extend([
            make_step("M", fraction_text(factor), fraction_text(value),
                      fraction_text(out)),
            make_step("TENSOR_ENTRY", f"{entry_prefix}{idx}",
                      fraction_text(out)),
        ])
    answer = f"{result_name} = {vector_text(result)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestIndexRaisingGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = IndexRaisingGenerator()

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

    def test_variants_are_available(self):
        for variant in IndexRaisingGenerator.VARIANTS:
            result = IndexRaisingGenerator(variant).generate()
            self.assertEqual(result["operation"], f"index_raising_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            IndexRaisingGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
