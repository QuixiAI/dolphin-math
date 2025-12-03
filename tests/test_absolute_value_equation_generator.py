import unittest
from generators.absolute_value_equation_generator import AbsoluteValueEquationGenerator

class TestAbsoluteValueEquationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = AbsoluteValueEquationGenerator()

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

    def test_no_solution_logic(self):
        # Force a negative c scenario by monkeypatching or just running enough times?
        # Better to check if logic handles it when it appears.
        # Let's try to mock the random choice
        import random
        from unittest.mock import patch
        
        with patch('random.choices', return_value=['no_sol']):
            problem = self.gen.generate()
            self.assertEqual(problem['final_answer'], "No solution")
            self.assertTrue(any("ABS_CHECK" in s for s in problem['steps']))

    def test_one_solution_logic(self):
        from unittest.mock import patch
        with patch('random.choices', return_value=['one_sol']):
            problem = self.gen.generate()
            self.assertNotEqual(problem['final_answer'], "No solution")
            self.assertTrue(any("ABS_SPLIT|Single case" in s for s in problem['steps']))

    def test_two_solution_logic(self):
        from unittest.mock import patch
        with patch('random.choices', return_value=['two_sol']):
            problem = self.gen.generate()
            self.assertIn(",", problem['final_answer']) # usually x=A, x=B
            self.assertTrue(any("ABS_SPLIT|Two cases" in s for s in problem['steps']))
            self.assertTrue(any("ABS_CASE|Case 1" in s for s in problem['steps']))
            self.assertTrue(any("ABS_CASE|Case 2" in s for s in problem['steps']))

if __name__ == '__main__':
    unittest.main()
