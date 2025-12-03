import unittest
from unittest.mock import patch

from generators.proportion_word_problem_generator import ProportionWordProblemGenerator
from helpers import DELIM


class TestProportionWordProblemGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ProportionWordProblemGenerator()

    def _last(self, steps):
        return steps[-1]

    def test_speed(self):
        with patch("generators.proportion_word_problem_generator.random.choice") as mock_choice, \
             patch("generators.proportion_word_problem_generator.random.randint", side_effect=[3, 2, 4]):
            mock_choice.return_value = ("speed", "If a car travels {} miles in {} hours, how far will it travel in {} hours?", "mi", "hr", "distance")
            res = self.gen.generate()
        # 3*2=6 miles in 2 hours; for 4 hours -> cross multiply 6*4=24; /2 = 12
        self.assertEqual(res["final_answer"], "12.0 mi")
        self.assertTrue(self._last(res["steps"]).startswith(f"Z{DELIM}"))

    def test_cost(self):
        with patch("generators.proportion_word_problem_generator.random.choice") as mock_choice, \
             patch("generators.proportion_word_problem_generator.random.randint", side_effect=[4, 3, 5]):
            mock_choice.return_value = ("cost", "If {} pounds of apples cost ${}, how much do {} pounds cost?", "lb", "$", "money")
            res = self.gen.generate()
        # a = 4*3=12 pounds cost $3; want 5 pounds: 12*5=60; /3 = 20
        self.assertEqual(res["final_answer"], "$20.00")

    def test_ratio_table(self):
        with patch("generators.proportion_word_problem_generator.random.choice") as mock_choice, \
             patch("generators.proportion_word_problem_generator.random.randint", side_effect=[2, 2, 5]):
            mock_choice.return_value = ("ratio_table", "Complete the ratio: {} {} corresponds to {} {}. What corresponds to {} {}?", None, None, "generic")
            res = self.gen.generate()
        # a = 2*2=4, b=2, target=5 => 4*5/2 =10
        self.assertEqual(res["final_answer"], "10.0")


if __name__ == "__main__":
    unittest.main()
