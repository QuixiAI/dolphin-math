import unittest
from generators.monomial_mult_div_generator import MonomialMultDivGenerator

class TestMonomialMultDivGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MonomialMultDivGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))

    def test_mult(self):
        found = False
        for _ in range(50):
            problem = self.gen.generate()
            if "monomial_mult" in problem['operation']:
                found = True
                self.assertIn("MONO_MULT_COEFF", str(problem['steps']))
                break
        self.assertTrue(found)

    def test_div(self):
        found = False
        for _ in range(50):
            problem = self.gen.generate()
            if "monomial_div" in problem['operation']:
                found = True
                self.assertIn("MONO_DIV_COEFF", str(problem['steps']))
                break
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()
