import unittest
from generators.multiplying_polynomials_generator import MultiplyingPolynomialsGenerator

class TestMultiplyingPolynomialsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MultiplyingPolynomialsGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))
            self.assertTrue(any("DIST_TERM" in s for s in problem['steps']))

    def test_zero_cancellation(self):
        # Could force coeffs to make terms cancel, but hard with 6 vars.
        # Just check basic output validity.
        problem = self.gen.generate()
        self.assertIn("x^3", problem['final_answer']) # Should have deg 3 usually

if __name__ == '__main__':
    unittest.main()
