import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.classifier_metrics_generator import ClassifierMetricsGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Given confusion matrix counts TP=(\d+), FP=(\d+), FN=(\d+), "
    r"TN=(\d+), compute precision, recall, and F1 for the positive class\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    if not match:
        raise AssertionError(problem)
    return tuple(int(part) for part in match.groups())


def expected_flow(example):
    tp, fp, fn, tn = parse_problem(example["problem"])
    predicted_positive = tp + fp
    actual_positive = tp + fn
    precision = Fraction(tp, predicted_positive)
    recall = Fraction(tp, actual_positive)
    product = precision * recall
    f1_numerator = 2 * product
    f1_denominator = precision + recall
    f1 = f1_numerator / f1_denominator
    steps = [
        make_step("METRICS_SETUP", f"TP={tp}, FP={fp}, FN={fn}, TN={tn}"),
        make_step("METRIC_FORMULA", "precision=TP/(TP+FP)"),
        make_step("A", tp, fp, predicted_positive),
        make_step("D", tp, predicted_positive, fraction_text(precision)),
        make_step("METRIC_FORMULA", "recall=TP/(TP+FN)"),
        make_step("A", tp, fn, actual_positive),
        make_step("D", tp, actual_positive, fraction_text(recall)),
        make_step("METRIC_FORMULA", "F1=2PR/(P+R)"),
        make_step("M", fraction_text(precision), fraction_text(recall),
                  fraction_text(product)),
        make_step("M", 2, fraction_text(product),
                  fraction_text(f1_numerator)),
        make_step("A", fraction_text(precision), fraction_text(recall),
                  fraction_text(f1_denominator)),
        make_step("D", fraction_text(f1_numerator),
                  fraction_text(f1_denominator), fraction_text(f1)),
    ]
    answer = (
        f"precision={fraction_text(precision)}; "
        f"recall={fraction_text(recall)}; F1={fraction_text(f1)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestClassifierMetricsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ClassifierMetricsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "classifier_precision_recall_f1")
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
