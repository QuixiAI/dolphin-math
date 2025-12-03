import unittest
from generators.slope_intercept_form_generator import SlopeInterceptFormGenerator

class TestSlopeInterceptFormGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SlopeInterceptFormGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))

    def test_horizontal_line(self):
        from unittest.mock import patch
        with patch('random.choice', return_value='horizontal'):
            problem = self.gen.generate()
            self.assertIn("m=0", problem['final_answer'])
            self.assertNotIn("x", problem['problem']) # y = b

    def test_no_b(self):
        from unittest.mock import patch
        with patch('random.choice', return_value='no_b'):
            problem = self.gen.generate()
            self.assertIn("b=0", problem['final_answer'])

if __name__ == '__main__':
    unittest.main()
