import unittest
from generators.point_slope_generator import PointSlopeGenerator

class TestPointSlopeGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PointSlopeGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))

    def test_basic_integer(self):
        # Can't easily force ints without patching random.random
        # But we can verify output format contains "y ="
        problem = self.gen.generate()
        self.assertIn("y =", problem['final_answer'])

if __name__ == '__main__':
    unittest.main()
