import unittest
from generators.parallel_perpendicular_line_generator import ParallelPerpendicularLineGenerator

class TestParallelPerpendicularLineGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = ParallelPerpendicularLineGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))

    def test_parallel_logic(self):
        from unittest.mock import patch
        # 1. relation, 2. m1_den
        with patch('random.choice', side_effect=['parallel', 1]):
             problem = self.gen.generate()
             self.assertIn("parallel", problem['problem'])
             self.assertTrue(any("Parallel lines have the same slope" in s for s in problem['steps']))

    def test_perpendicular_logic(self):
        from unittest.mock import patch
        # 1. relation, 2. m2_den
        with patch('random.choice', side_effect=['perpendicular', 1]):
             problem = self.gen.generate()
             self.assertIn("perpendicular", problem['problem'])
             self.assertTrue(any("negative reciprocal" in s for s in problem['steps']))

if __name__ == '__main__':
    unittest.main()
