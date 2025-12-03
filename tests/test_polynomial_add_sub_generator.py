import random
import unittest
from generators.polynomial_add_sub_generator import PolynomialAddSubGenerator

class TestPolynomialAddSubGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PolynomialAddSubGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))
            self.assertTrue(any("POLY_SETUP" in s for s in problem['steps']))

    def test_add(self):
        from unittest.mock import patch
        original_choice = random.choice

        def patched_choice(seq):
            # Only override the op selection; leave other random choices alone.
            if set(seq) == {"+", "-"} and len(seq) == 2:
                return "+"
            return original_choice(seq)

        with patch('random.choice', side_effect=patched_choice):
            problem = self.gen.generate()
            self.assertIn("+", problem['problem'])

    def test_sub(self):
        from unittest.mock import patch
        original_choice = random.choice

        def patched_choice(seq):
            if set(seq) == {"+", "-"} and len(seq) == 2:
                return "-"
            return original_choice(seq)

        with patch('random.choice', side_effect=patched_choice):
            problem = self.gen.generate()
            self.assertIn("-", problem['problem'])

if __name__ == '__main__':
    unittest.main()
