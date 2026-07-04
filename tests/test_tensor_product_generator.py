import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.tensor_product_generator import TensorProductGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Let A=diag\((-?\d+),(-?\d+)\), B=diag\((-?\d+),(-?\d+)\), "
    r"u=\[(-?\d+),(-?\d+)\], and v=\[(-?\d+),(-?\d+)\]\. "
    r"Build A tensor B and apply it to u tensor v\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def vector_text(values):
    return "[" + ",".join(str(v) for v in values) + "]"


def diag_text(values):
    return "diag(" + ",".join(str(v) for v in values) + ")"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    values = [int(match.group(i)) for i in range(1, 9)]
    return {
        "a": values[0], "b": values[1], "c": values[2],
        "d": values[3], "u": values[4:6], "v": values[6:8],
    }


def expected_flow(example):
    parts = parse_problem(example["problem"])
    a, b, c, d = parts["a"], parts["b"], parts["c"], parts["d"]
    u, v = parts["u"], parts["v"]
    diag_entries = [a * c, a * d, b * c, b * d]
    state_entries = [u[0] * v[0], u[0] * v[1],
                     u[1] * v[0], u[1] * v[1]]
    result_entries = [left * right for left, right
                      in zip(diag_entries, state_entries)]
    steps = [
        make_step("TENSOR_SETUP", f"A=diag({a},{b})", f"B=diag({c},{d})",
                  f"u={vector_text(u)}, v={vector_text(v)}"),
        make_step("TENSOR_RULE",
                  "diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)"),
        make_step("M", a, c, diag_entries[0]),
        make_step("M", a, d, diag_entries[1]),
        make_step("M", b, c, diag_entries[2]),
        make_step("M", b, d, diag_entries[3]),
        make_step("TENSOR_STATE", "u tensor v", vector_text(state_entries)),
        make_step("M", u[0], v[0], state_entries[0]),
        make_step("M", u[0], v[1], state_entries[1]),
        make_step("M", u[1], v[0], state_entries[2]),
        make_step("M", u[1], v[1], state_entries[3]),
    ]
    for diag_value, state_value, result_value in zip(
            diag_entries, state_entries, result_entries):
        steps.append(make_step("M", diag_value, state_value, result_value))
    answer = (
        f"A tensor B = {diag_text(diag_entries)}; "
        f"output = {vector_text(result_entries)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestTensorProductGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = TensorProductGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "tensor_product_diagonal_apply")
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
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
