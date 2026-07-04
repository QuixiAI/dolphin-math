import ast
import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.attention_generator import AttentionGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Compute scaled dot-product attention for Q=(\[\[.*?\]\]), "
    r"K=(\[\[.*?\]\]), V=(\[\[.*?\]\]) with d=2\. Use softmax over "
    r"each row of QK\^T/sqrt\(2\)\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def matrix_text(matrix):
    return "[" + ", ".join(
        "[" + ",".join(fraction_text(value) for value in row) + "]"
        for row in matrix
    ) + "]"


def expected_flow(example):
    match = PROBLEM_RE.fullmatch(example["problem"])
    if not match:
        raise AssertionError(example["problem"])
    q = ast.literal_eval(match.group(1))
    k = ast.literal_eval(match.group(2))
    v = ast.literal_eval(match.group(3))
    tokens = len(q)
    steps = [
        make_step("ATTN_SETUP", f"tokens={tokens},d=2",
                  f"Q={matrix_text(q)}", f"K={matrix_text(k)}"),
        make_step("ATTN_SETUP", f"V={matrix_text(v)}"),
    ]
    for row in range(tokens):
        for col in range(tokens):
            prod1 = q[row][0] * k[col][0]
            prod2 = q[row][1] * k[col][1]
            dot = prod1 + prod2
            steps.extend([
                make_step("M", q[row][0], k[col][0], prod1),
                make_step("M", q[row][1], k[col][1], prod2),
                make_step("A", prod1, prod2, dot),
                make_step("ATTN_SCORE", f"{row + 1},{col + 1}", dot),
            ])

    weight = Fraction(1, tokens)
    outputs = []
    for row in range(tokens):
        exp_sum = 0
        for col in range(tokens):
            steps.append(make_step("SOFTMAX_EXP", f"{row + 1},{col + 1}", 1))
            new_sum = exp_sum + 1
            steps.append(make_step("A", exp_sum, 1, new_sum))
            exp_sum = new_sum
        weights = []
        for col in range(tokens):
            steps.append(make_step("D", 1, exp_sum, fraction_text(weight)))
            steps.append(make_step("SOFTMAX_WEIGHT", f"{row + 1},{col + 1}",
                                   fraction_text(weight)))
            weights.append(weight)
        output_row = []
        for dim in range(2):
            running = Fraction(0)
            for col in range(tokens):
                term = weights[col] * v[col][dim]
                steps.append(make_step("M", fraction_text(weights[col]),
                                       v[col][dim], fraction_text(term)))
                new_running = running + term
                steps.append(make_step("A", fraction_text(running),
                                       fraction_text(term),
                                       fraction_text(new_running)))
                running = new_running
            output_row.append(running)
        steps.append(make_step("ATTN_OUTPUT", row + 1,
                               matrix_text([output_row])))
        outputs.append(output_row)

    answer = f"attention={matrix_text(outputs)}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestAttentionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = AttentionGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"],
                         "attention_scaled_dot_product_uniform")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(400):
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
                elif fields[0] == "D":
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
