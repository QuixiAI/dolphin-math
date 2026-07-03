import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.exponent_mixed_rules_generator import ExponentMixedRulesGenerator
from helpers import DELIM


def parse_final_exponent(expr):
    """Independently computes the final exponent from the expression text."""
    exps = [int(x) for x in re.findall(r"\^\(?(-?\d+)\)?", expr)]
    assert len(exps) == 3, expr
    if expr.startswith("("):  # (b^a)^b then · or / b^c
        head = exps[0] * exps[1]
        return head - exps[2] if "/" in expr else head + exps[2]
    if "/" in expr:  # b^a · b^b / b^c
        return exps[0] + exps[1] - exps[2]
    return sum(exps)  # triple product


def expected_answer(base, e):
    if e == 0:
        return "1"
    if e == 1:
        return base
    if e > 0:
        return f"{base}^{e}"
    return f"1/{base}" if e == -1 else f"1/{base}^{-e}"


class TestExponentMixedRulesGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ExponentMixedRulesGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "exponent_mixed_rules")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        """A9 oracle: recompute the exponent from the expression alone."""
        for _ in range(400):
            result = self.gen.generate()
            expr = result["problem"].split(": ", 1)[1]
            base = expr.lstrip("(")[0]
            e = parse_final_exponent(expr)
            self.assertEqual(expected_answer(base, e), result["final_answer"],
                             expr)

    def test_all_forms_and_outcomes_reachable(self):
        forms_seen, outcomes = set(), set()
        for _ in range(300):
            result = self.gen.generate()
            expr = result["problem"].split(": ", 1)[1]
            e = parse_final_exponent(expr)
            outcomes.add("zero" if e == 0 else "neg" if e < 0 else "pos")
            forms_seen.add((expr.startswith("("), "/" in expr,
                            expr.count("·")))
        self.assertEqual(outcomes, {"zero", "neg", "pos"})
        self.assertEqual(len(forms_seen), 4)

    def test_rule_application_arithmetic(self):
        """Every EXP_RULE_APPLY must be independently true."""
        for _ in range(400):
            result = self.gen.generate()
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] != "EXP_RULE_APPLY":
                    continue
                verb, x, y, r = f[1], int(f[2]), int(f[3]), int(f[4])
                expected = {"add": x + y, "subtract": x - y,
                            "multiply": x * y}[verb]
                self.assertEqual(expected, r, s)

    def test_finishing_rule_matches_outcome(self):
        for _ in range(300):
            result = self.gen.generate()
            expr = result["problem"].split(": ", 1)[1]
            e = parse_final_exponent(expr)
            identifies = [s.split(DELIM)[1] for s in result["steps"]
                          if s.startswith(f"EXP_RULE_IDENTIFY{DELIM}")]
            if e == 0:
                self.assertIn("zero_exponent", identifies)
            elif e < 0:
                self.assertIn("negative_exponent", identifies)
            else:
                self.assertNotIn("zero_exponent", identifies)
                self.assertNotIn("negative_exponent", identifies)

    def test_answer_has_no_negative_or_zero_exponent(self):
        for _ in range(300):
            ans = self.gen.generate()["final_answer"]
            self.assertNotIn("-", ans)
            self.assertNotRegex(ans, r"\^0")
            self.assertNotRegex(ans, r"\^1$")

    def test_fixed_form_constructor(self):
        for form in ExponentMixedRulesGenerator.FORMS:
            gen = ExponentMixedRulesGenerator(form)
            gen.generate()
        with self.assertRaises(ValueError):
            ExponentMixedRulesGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
