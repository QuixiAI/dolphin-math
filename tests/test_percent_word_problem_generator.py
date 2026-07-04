import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.percent_word_problem_generator import (
    PercentWordProblemGenerator,
)
from generators.exponential_model_generator import dec
from helpers import DELIM

SUBTRACTIVE = ("decrease", "shrink", "discount", " off", "sale price")


def oracle_answer(problem):
    """Recompute the answer from the problem text alone (A9).

    Every core phrasing ends with '?'; any distractor is appended
    after as a declarative sentence, so the numbers before the first
    '?' are exactly the rate and the base.
    """
    core = problem[: problem.index("?") + 1]
    pct = int(re.search(r"(\d+)%", core).group(1))
    nums = [int(n) for n in re.findall(r"\d+", core)]
    rest = list(nums)
    rest.remove(pct)  # removes the first pct occurrence; base remains
    base = rest[0]
    change = Fraction(base) * Fraction(pct, 100)
    lower = core.lower()
    if any(k in lower for k in SUBTRACTIVE):
        total = base - change
    else:
        total = base + change
    return (str(total.numerator) if total.denominator == 1
            else dec(total))


class TestPercentWordProblemGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = PercentWordProblemGenerator()
        self.dgen = PercentWordProblemGenerator(distractor=True)

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_recompute_plain(self):
        """A9 oracle: recompute from the problem text."""
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(oracle_answer(result["problem"]),
                             result["final_answer"], result["problem"])

    def test_oracle_recompute_with_distractor(self):
        """The distractor number must not change the answer."""
        for _ in range(500):
            result = self.dgen.generate()
            self.assertEqual(oracle_answer(result["problem"]),
                             result["final_answer"], result["problem"])

    def test_distractor_first_step_selects_data(self):
        for _ in range(200):
            result = self.dgen.generate()
            self.assertTrue(result["steps"][0]
                            .startswith(f"SELECT_RELEVANT{DELIM}"))
            self.assertIn("ignore", result["steps"][0])

    def test_plain_has_no_select_step(self):
        for _ in range(100):
            result = self.gen.generate()
            self.assertFalse(any(s.startswith(f"SELECT_RELEVANT{DELIM}")
                                 for s in result["steps"]))

    def test_multiple_phrasings_occur(self):
        openings = {result["problem"][:14]
                    for result in (self.gen.generate()
                                   for _ in range(300))}
        self.assertGreaterEqual(len(openings), 5)

    def test_tax_problem_text_is_consistent(self):
        """Regression: the tax phrasing once reversed base and rate."""
        for _ in range(1000):
            result = self.gen.generate()
            if "sales tax" in result["problem"]:
                self.assertEqual(oracle_answer(result["problem"]),
                                 result["final_answer"],
                                 result["problem"])


if __name__ == "__main__":
    unittest.main()
