import unittest
from generators.absolute_value_inequality_generator import AbsoluteValueInequalityGenerator

class TestAbsoluteValueInequalityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = AbsoluteValueInequalityGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(len(problem['steps']) > 0)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))

    def test_special_negative_case(self):
        # We can try to force it or just verify logic if we hit it
        # Mocks are safer
        from unittest.mock import patch
        with patch('random.choices', return_value=['special']):
             # Mock choice to ensure c < 0
             with patch('random.randint', side_effect=[-10, -5]): # b, c
                 problem = self.gen.generate()
                 self.assertTrue("No solution" in problem['final_answer'] or "All real numbers" in problem['final_answer'])

    def test_and_case(self):
        # Force standard case with <
        # Use side_effect for random.choice: 
        # 1st call: op (needs to be '<')
        # 2nd call: a (needs to be int)
        from unittest.mock import patch
        with patch('random.choices', return_value=['standard']):
            with patch('random.choice', side_effect=['<', 2]):
                problem = self.gen.generate()
                self.assertIn("ABS_INEQ_SPLIT|AND case", problem['steps'][1])

    def test_or_case(self):
        # Force standard case with >
        from unittest.mock import patch
        with patch('random.choices', return_value=['standard']):
            with patch('random.choice', side_effect=['>', 3]):
                problem = self.gen.generate()
                self.assertIn("ABS_INEQ_SPLIT|OR case", problem['steps'][1])
                self.assertIn("OR", problem['final_answer'])

if __name__ == '__main__':
    unittest.main()
