import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.transportation_generator import (
    TransportationGenerator,
    allocation_text,
    cost_terms,
)
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use northwest-corner then one stepping-stone improvement for a 2x2 "
    r"transportation problem with supply \((\d+),(\d+)\), demand "
    r"\((\d+),(\d+)\), and costs \[\[(\d+),(\d+)\],\[(\d+),(\d+)\]\]\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    return tuple(int(match.group(i)) for i in range(1, 9))


def expected_flow(example):
    s1, s2, d1, d2, c11, c12, c21, c22 = parse_problem(example["problem"])
    x11 = d1
    x12 = s1 - d1
    x21 = 0
    x22 = s2
    theta = min(x22, x11)
    new_x21 = x21 + theta
    new_x22 = x22 - theta
    new_x12 = x12 + theta
    new_x11 = x11 - theta
    costs = [c11, c12, c21, c22]
    initial_allocations = [x11, x12, x21, x22]
    final_allocations = [new_x11, new_x12, new_x21, new_x22]
    initial_terms = cost_terms(initial_allocations, costs)
    final_terms = cost_terms(final_allocations, costs)
    initial_sub1 = initial_terms[0] + initial_terms[1]
    initial_sub2 = initial_sub1 + initial_terms[2]
    initial_cost = initial_sub2 + initial_terms[3]
    final_sub1 = final_terms[0] + final_terms[1]
    final_sub2 = final_sub1 + final_terms[2]
    final_cost = final_sub2 + final_terms[3]
    delta_first = c21 - c22
    delta_second = delta_first + c12
    delta = delta_second - c11
    steps = [
        make_step("TRANSPORT_SETUP", f"supply=({s1},{s2})",
                  f"demand=({d1},{d2})",
                  f"costs=({c11},{c12};{c21},{c22})"),
        make_step("CHECK", f"{s1}+{s2}", f"{d1}+{d2}", "balanced"),
        make_step("NW_ALLOC", "cell x11", f"min({s1},{d1})", x11),
        make_step("S", s1, x11, x12),
        make_step("NW_ALLOC", "cell x12", "remaining row 1 supply", x12),
        make_step("NW_ALLOC", "cell x22", "remaining row 2 supply", x22),
        make_step("NW_ALLOC", allocation_text(x11, x12, x21, x22)),
        make_step("COST", "initial"),
    ]
    for allocation, cost, term in zip(initial_allocations, costs,
                                      initial_terms):
        steps.append(make_step("M", allocation, cost, term))
    steps += [
        make_step("A", initial_terms[0], initial_terms[1], initial_sub1),
        make_step("A", initial_sub1, initial_terms[2], initial_sub2),
        make_step("A", initial_sub2, initial_terms[3], initial_cost),
        make_step("STEPPING_STONE", "enter x21",
                  "+x21 -x22 +x12 -x11"),
        make_step("S", c21, c22, delta_first),
        make_step("A", delta_first, c12, delta_second),
        make_step("S", delta_second, c11, delta),
        make_step("CHECK", f"delta={delta}", "improves cost"),
        make_step("THETA", f"min({x22},{x11})", theta),
        make_step("A", x21, theta, new_x21),
        make_step("S", x22, theta, new_x22),
        make_step("A", x12, theta, new_x12),
        make_step("S", x11, theta, new_x11),
        make_step("NW_ALLOC", allocation_text(new_x11, new_x12,
                                               new_x21, new_x22)),
        make_step("COST", "improved"),
    ]
    for allocation, cost, term in zip(final_allocations, costs, final_terms):
        steps.append(make_step("M", allocation, cost, term))
    steps += [
        make_step("A", final_terms[0], final_terms[1], final_sub1),
        make_step("A", final_sub1, final_terms[2], final_sub2),
        make_step("A", final_sub2, final_terms[3], final_cost),
    ]
    answer = (
        f"initial cost={initial_cost}; improved "
        f"{allocation_text(new_x11, new_x12, new_x21, new_x22)}; "
        f"final cost={final_cost}"
    )
    steps.append(make_step("Z", answer))
    return steps, answer


class TestTransportationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = TransportationGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"],
                         "transportation_nw_stepping_stone")
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
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_problem_is_balanced_and_improves(self):
        for _ in range(300):
            result = self.gen.generate()
            s1, s2, d1, d2, *_ = parse_problem(result["problem"])
            self.assertEqual(s1 + s2, d1 + d2)
            expected_steps, answer = expected_flow(result)
            initial = int(re.search(r"initial cost=(\d+)", answer).group(1))
            final = int(re.search(r"final cost=(\d+)", answer).group(1))
            self.assertLess(final, initial)
            self.assertEqual(result["steps"], expected_steps)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
