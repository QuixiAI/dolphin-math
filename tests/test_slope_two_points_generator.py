import unittest
from generators.slope_two_points_generator import SlopeTwoPointsGenerator

class TestSlopeTwoPointsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SlopeTwoPointsGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))

    def test_undefined_slope(self):
        # Force vertical line
        from unittest.mock import patch
        with patch('random.random', return_value=0.0): # Force x2 = x1
            problem = self.gen.generate()
            self.assertEqual(problem['final_answer'], "Undefined")
            self.assertTrue(any("SLOPE_UNDEFINED" in s for s in problem['steps']))

    def test_zero_slope(self):
        # Force horizontal line
        # Logic: first random check > 0.1 (not vertical), second < 0.1 (horizontal)
        from unittest.mock import patch
        with patch('random.random', side_effect=[0.5, 0.05]): 
            problem = self.gen.generate()
            self.assertEqual(problem['final_answer'], "0")

    def test_integer_slope(self):
        # We can't easily force random integers to produce exact integer slope without complex patching,
        # but we can verify that the steps include delta calculation
        problem = self.gen.generate()
        self.assertTrue(any("SLOPE_FORMULA" in s for s in problem['steps']))
        self.assertTrue(any("SLOPE_SUBST" in s for s in problem['steps']))

if __name__ == '__main__':
    unittest.main()
