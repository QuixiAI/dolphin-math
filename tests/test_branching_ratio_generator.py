import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.branching_ratio_generator import BranchingRatioGenerator
from helpers import DELIM


BR_RE = re.compile(
    r"A particle has partial widths Gamma_a=(\d+), Gamma_b=(\d+), "
    r"and Gamma_c=(\d+)\. Compute the branching ratio "
    r"BR_([abc])=Gamma_\4/Gamma_total\."
)
LIFETIME_RE = re.compile(
    r"Given hbar=(\d+) and total width Gamma=(\d+), compute "
    r"the lifetime tau=hbar/Gamma\."
)
COMBINED_RE = re.compile(
    r"A particle has partial widths Gamma_a=(\d+), Gamma_b=(\d+), "
    r"Gamma_c=(\d+) and hbar=(\d+)\. Compute Gamma_total, "
    r"BR_([abc])=Gamma_\5/Gamma_total, and tau=hbar/Gamma_total\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def widths_from_groups(groups):
    return {"a": int(groups[0]), "b": int(groups[1]), "c": int(groups[2])}


def widths_text(widths, final_and=True):
    middle = f"Gamma_a={widths['a']}, Gamma_b={widths['b']}"
    if final_and:
        return f"{middle}, and Gamma_c={widths['c']}"
    return f"{middle}, Gamma_c={widths['c']}"


def parse_problem(problem):
    match = BR_RE.fullmatch(problem)
    if match:
        return {
            "variant": "branching_ratio",
            "widths": widths_from_groups(match.groups()),
            "channel": match.group(4),
        }
    match = LIFETIME_RE.fullmatch(problem)
    if match:
        return {
            "variant": "lifetime",
            "hbar": int(match.group(1)),
            "gamma": int(match.group(2)),
        }
    match = COMBINED_RE.fullmatch(problem)
    assert match is not None, problem
    return {
        "variant": "combined",
        "widths": widths_from_groups(match.groups()),
        "hbar": int(match.group(4)),
        "channel": match.group(5),
    }


def total_steps(steps, widths):
    sum_ab = widths["a"] + widths["b"]
    total = sum_ab + widths["c"]
    steps.append(make_step("A", widths["a"], widths["b"], sum_ab))
    steps.append(make_step("A", sum_ab, widths["c"], total))
    return total


def expected_branching_ratio(parts):
    widths = parts["widths"]
    channel = parts["channel"]
    steps = [
        make_step("WIDTH_SETUP", "branching_ratio",
                  widths_text(widths, final_and=False),
                  f"target=BR_{channel}"),
    ]
    total = total_steps(steps, widths)
    br = Fraction(widths[channel], total)
    steps.append(make_step("D", widths[channel], total, fraction_text(br)))
    answer = f"BR_{channel} = {fraction_text(br)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_lifetime(parts):
    hbar = parts["hbar"]
    gamma = parts["gamma"]
    lifetime = Fraction(hbar, gamma)
    steps = [
        make_step("WIDTH_SETUP", "lifetime", f"hbar={hbar}",
                  f"Gamma={gamma}"),
        make_step("D", hbar, gamma, fraction_text(lifetime)),
    ]
    answer = f"tau = {fraction_text(lifetime)}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_combined(parts):
    widths = parts["widths"]
    hbar = parts["hbar"]
    channel = parts["channel"]
    steps = [
        make_step("WIDTH_SETUP", "combined",
                  f"{widths_text(widths, final_and=False)},hbar={hbar}",
                  f"target=BR_{channel},tau"),
    ]
    total = total_steps(steps, widths)
    br = Fraction(widths[channel], total)
    lifetime = Fraction(hbar, total)
    steps.append(make_step("D", widths[channel], total, fraction_text(br)))
    steps.append(make_step("D", hbar, total, fraction_text(lifetime)))
    answer = (
        f"Gamma_total = {total}, BR_{channel} = {fraction_text(br)}, "
        f"tau = {fraction_text(lifetime)}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "branching_ratio":
        return expected_branching_ratio(parts)
    if parts["variant"] == "lifetime":
        return expected_lifetime(parts)
    return expected_combined(parts)


class TestBranchingRatioGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = BranchingRatioGenerator()

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
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in BranchingRatioGenerator.VARIANTS:
            result = BranchingRatioGenerator(variant).generate()
            self.assertEqual(result["operation"],
                             f"branching_ratio_{variant}")
            self.assertEqual(parse_problem(result["problem"])["variant"],
                             variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            BranchingRatioGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])

    def test_all_variants_seen_with_random_generator(self):
        seen = {self.gen.generate()["operation"] for _ in range(200)}
        self.assertEqual(
            seen,
            {"branching_ratio_branching_ratio", "branching_ratio_lifetime",
             "branching_ratio_combined"},
        )


if __name__ == "__main__":
    unittest.main()
