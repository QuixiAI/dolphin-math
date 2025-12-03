import unittest
from generators.compound_inequality_generator import CompoundInequalityGenerator

class TestCompoundInequalityGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = CompoundInequalityGenerator()

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

    def test_and_case(self):
        from unittest.mock import patch
        # Side effect: 1st call = type, 2nd call = b (int)
        with patch('random.choice', side_effect=['and_compact', 2]):
             problem = self.gen.generate()
             self.assertTrue("<" in problem['problem'] and "OR" not in problem['problem'])
             self.assertTrue(any("INEQ_OP_ALL" in s for s in problem['steps']))

    def test_or_case(self):
        from unittest.mock import patch
        with patch('random.choice', side_effect=['or_disjoint', 3]):
             problem = self.gen.generate()
             self.assertIn("OR", problem['problem'])
             self.assertIn("OR", problem['final_answer'])
             self.assertTrue(any("COMP_INEQ_PART" in s for s in problem['steps']))

if __name__ == '__main__':
    unittest.main()
