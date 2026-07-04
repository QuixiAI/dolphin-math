import ast
import os
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.perceptron_generator import PerceptronGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Run one perceptron epoch with eta=(\d+), starting weights "
    r"w=(\([^)]+\)) for samples (\[[^\]]+\])\. Use bias feature x0=1, "
    r"score=w0\+w1\*x1\+w2\*x2, and update when y\*score <= 0\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def tuple_text(values):
    return "(" + ",".join(str(value) for value in values) + ")"


def samples_text(samples):
    return "[" + ", ".join(tuple_text(sample) for sample in samples) + "]"


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    eta = int(match.group(1))
    weights = list(ast.literal_eval(match.group(2)))
    samples = ast.literal_eval(match.group(3))
    return eta, weights, samples


def epoch_update(samples, weights, eta):
    weights = list(weights)
    mistakes = 0
    trace = []
    for index, (x1, x2, label) in enumerate(samples, start=1):
        old_weights = list(weights)
        term1 = weights[1] * x1
        partial = weights[0] + term1
        term2 = weights[2] * x2
        score = partial + term2
        margin = label * score
        update = margin <= 0
        item = {
            "index": index,
            "x1": x1,
            "x2": x2,
            "label": label,
            "old_weights": old_weights,
            "term1": term1,
            "partial": partial,
            "term2": term2,
            "score": score,
            "margin": margin,
            "update": update,
        }
        if update:
            mistakes += 1
            eta_y = eta * label
            delta0 = eta_y
            delta1 = eta_y * x1
            delta2 = eta_y * x2
            weights = [
                weights[0] + delta0,
                weights[1] + delta1,
                weights[2] + delta2,
            ]
            item.update({
                "eta_y": eta_y,
                "delta0": delta0,
                "delta1": delta1,
                "delta2": delta2,
                "new_weights": list(weights),
            })
        else:
            item["new_weights"] = list(weights)
        trace.append(item)
    return weights, mistakes, trace


def expected_flow(example):
    eta, weights, samples = parse_problem(example["problem"])
    final_weights, mistakes, trace = epoch_update(samples, weights, eta)
    steps = [
        make_step("PERCEPTRON_SETUP", f"eta={eta}",
                  f"w={tuple_text(weights)}",
                  f"samples={samples_text(samples)}"),
        make_step("PERCEPTRON_RULE", "score=w0+w1*x1+w2*x2",
                  "if y*score <= 0 update"),
    ]
    for item in trace:
        steps.extend([
            make_step("PERCEPTRON_SAMPLE", f"i={item['index']}",
                      f"x=({item['x1']},{item['x2']})",
                      f"y={item['label']}"),
            make_step("M", item["old_weights"][1], item["x1"],
                      item["term1"]),
            make_step("A", item["old_weights"][0], item["term1"],
                      item["partial"]),
            make_step("M", item["old_weights"][2], item["x2"],
                      item["term2"]),
            make_step("A", item["partial"], item["term2"], item["score"]),
            make_step("PERCEPTRON_SCORE", f"i={item['index']}",
                      f"score={item['score']}"),
            make_step("M", item["label"], item["score"], item["margin"]),
            make_step("CHECK", f"i={item['index']}",
                      f"y*score={item['margin']}",
                      "update" if item["update"] else "keep"),
        ])
        if item["update"]:
            steps.extend([
                make_step("M", eta, item["label"], item["eta_y"]),
                make_step("M", item["eta_y"], 1, item["delta0"]),
                make_step("A", item["old_weights"][0], item["delta0"],
                          item["new_weights"][0]),
                make_step("M", item["eta_y"], item["x1"], item["delta1"]),
                make_step("A", item["old_weights"][1], item["delta1"],
                          item["new_weights"][1]),
                make_step("M", item["eta_y"], item["x2"], item["delta2"]),
                make_step("A", item["old_weights"][2], item["delta2"],
                          item["new_weights"][2]),
                make_step("PERCEPTRON_UPDATE", f"i={item['index']}",
                          f"w={tuple_text(item['new_weights'])}"),
            ])
        else:
            steps.append(make_step("PERCEPTRON_UPDATE", f"i={item['index']}",
                                   "no change",
                                   f"w={tuple_text(item['new_weights'])}"))

    answer = f"w_final={tuple_text(final_weights)}; updates={mistakes}"
    steps.append(make_step("Z", answer))
    return steps, answer


class TestPerceptronGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PerceptronGenerator()

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

    def test_variants_are_available(self):
        for variant in PerceptronGenerator.VARIANTS:
            result = PerceptronGenerator(variant).generate()
            self.assertEqual(result["operation"], f"perceptron_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)
            _, _, samples = parse_problem(result["problem"])
            expected_count = 3 if variant == "three_point_epoch" else 4
            self.assertEqual(len(samples), expected_count)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            PerceptronGenerator("bogus")

    def test_arithmetic_and_update_rule(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(int(fields[1]) + int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(int(fields[1]) * int(fields[2]),
                                     int(fields[3]), raw_step)
                elif fields[0] == "CHECK":
                    margin = int(fields[2].split("=")[1])
                    expected = "update" if margin <= 0 else "keep"
                    self.assertEqual(fields[3], expected, raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
