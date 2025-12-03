import unittest
from generators.polynomial_div_monomial_generator import PolynomialDivMonomialGenerator

class TestPolynomialDivMonomialGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PolynomialDivMonomialGenerator()

    def test_generate_structure(self):
        for _ in range(20):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)
            self.assertTrue(problem['steps'][-1].startswith("Z|"))
            self.assertTrue(any("POLY_DIV_SPLIT" in s for s in problem['steps']))

if __name__ == '__main__':
    unittest.main()
