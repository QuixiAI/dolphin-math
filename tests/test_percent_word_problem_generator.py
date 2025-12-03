import unittest
from unittest.mock import patch

from generators.percent_word_problem_generator import PercentWordProblemGenerator
from helpers import DELIM


class TestPercentWordProblemGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PercentWordProblemGenerator()

    def test_markup(self):
        with patch("generators.percent_word_problem_generator.random.choice") as mock_choice, \
             patch("generators.percent_word_problem_generator.random.randint", return_value=50):
            mock_choice.side_effect = [("markup", "markup", "A store marks up an item by {}% on a base price of {}. What is the new price?"), 20]
            res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        # 20% of 50 is 10; new price 60
        self.assertEqual(res["final_answer"], "60")

    def test_discount(self):
        with patch("generators.percent_word_problem_generator.random.choice") as mock_choice, \
             patch("generators.percent_word_problem_generator.random.randint", return_value=80):
            mock_choice.side_effect = [("discount", "discount", "A {}% discount is applied to {}. What is the sale price?"), 25]
            res = self.gen.generate()
        # 25% of 80 = 20; sale price 60
        self.assertEqual(res["final_answer"], "60")
        self.assertTrue(any(s.startswith("S|") for s in res["steps"]))

    def test_tax(self):
        with patch("generators.percent_word_problem_generator.random.choice") as mock_choice, \
             patch("generators.percent_word_problem_generator.random.randint", return_value=100):
            mock_choice.side_effect = [("tax", "sales tax", "An item costs {} and a sales tax of {}% is applied. What is the total cost?"), 8]
            res = self.gen.generate()
        # 8% of 100 = 8; total 108
        self.assertEqual(res["final_answer"], "108")
        self.assertTrue(any(s.startswith("A|") for s in res["steps"]))


if __name__ == "__main__":
    unittest.main()
