import unittest
from generators.multiplying_binomials_generator import MultiplyingBinomialsGenerator

class TestMultiplyingBinomialsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MultiplyingBinomialsGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))
            self.assertTrue(any("FOIL_F" in s for s in problem['steps']))

    def test_difference_of_squares(self):
        # Force a=1, b=5, c=1, d=-5 -> (x+5)(x-5) -> x^2 - 25
        # Middle term cancels
        from unittest.mock import patch
        with patch('random.randint', side_effect=[1, 5, 1, -5]):
             problem = self.gen.generate()
             self.assertNotIn("x ", problem['final_answer']) # no linear term
             self.assertIn("x^2", problem['final_answer'])

if __name__ == '__main__':
    unittest.main()
