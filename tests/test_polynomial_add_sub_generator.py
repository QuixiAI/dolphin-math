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
        with patch('random.choice', return_value='+'):
             problem = self.gen.generate()
             self.assertIn("+", problem['problem'])

    def test_sub(self):
        from unittest.mock import patch
        with patch('random.choice', return_value='-'):
             problem = self.gen.generate()
             self.assertIn("-", problem['problem'])

if __name__ == '__main__':
    unittest.main()
