import unittest
from generators.standard_form_conversion_generator import StandardFormConversionGenerator

class TestStandardFormConversionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = StandardFormConversionGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))

    def test_to_slope_intercept(self):
        from unittest.mock import patch
        # 1. direction, 2. B (int)
        with patch('random.choice', side_effect=['to_slope_intercept', 2]):
             problem = self.gen.generate()
             self.assertIn("y =", problem['final_answer'])
             self.assertNotIn("Ax", problem['final_answer'])

    def test_to_standard(self):
        from unittest.mock import patch
        # 1. direction, 2. m_den, 3. b_den
        with patch('random.choice', side_effect=['to_standard', 2, 3]):
             problem = self.gen.generate()
             self.assertIn("=", problem['final_answer'])
             # Standard form usually has x and y on LHS.
             # Check if x and y are in the answer string
             self.assertTrue("x" in problem['final_answer'] and "y" in problem['final_answer'])

if __name__ == '__main__':
    unittest.main()
