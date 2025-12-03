import unittest
from generators.systems_substitution_generator import SystemsSubstitutionGenerator

class TestSystemsSubstitutionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SystemsSubstitutionGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))
            self.assertTrue(any("SYS_SETUP" in s for s in problem['steps']))

    def test_isolated_case(self):
        from unittest.mock import patch
        with patch('random.choice', return_value='isolated'):
             problem = self.gen.generate()
             # Should involve substitution directly
             self.assertTrue(any("SYS_SUBST" in s for s in problem['steps']))

    def test_easy_isolate_case(self):
        from unittest.mock import patch
        with patch('random.choice', return_value='easy_isolate'):
             problem = self.gen.generate()
             # Should have ISOLATE step
             self.assertTrue(any("SYS_ISOLATE" in s for s in problem['steps']))

if __name__ == '__main__':
    unittest.main()
