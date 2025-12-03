import unittest
from generators.literal_equation_generator import LiteralEquationGenerator

class TestLiteralEquationGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = LiteralEquationGenerator()

    def test_one_step_add(self):
        problem = self.gen._generate_one_step_add()
        self.assertIn("Solve for", problem['problem'])
        self.assertEqual(problem['operation'], "literal_eq_one_step_add")
        self.assertTrue(len(problem['steps']) > 0)

    def test_one_step_sub(self):
        problem = self.gen._generate_one_step_sub()
        self.assertIn("Solve for", problem['problem'])
        self.assertEqual(problem['operation'], "literal_eq_one_step_sub")

    def test_one_step_mult(self):
        problem = self.gen._generate_one_step_mult()
        self.assertIn("Solve for", problem['problem'])
        self.assertEqual(problem['operation'], "literal_eq_one_step_mult")

    def test_one_step_div(self):
        problem = self.gen._generate_one_step_div()
        self.assertIn("Solve for", problem['problem'])
        self.assertEqual(problem['operation'], "literal_eq_one_step_div")

    def test_two_step_linear(self):
        problem = self.gen._generate_two_step_linear()
        self.assertIn("Solve for", problem['problem'])
        self.assertEqual(problem['operation'], "literal_eq_two_step_linear")

    def test_formula_area_rect(self):
        problem = self.gen._generate_formula_area_rect()
        self.assertIn("Solve for", problem['problem'])
        self.assertTrue(problem['operation'] == "literal_eq_formula_area")

    def test_formula_perimeter_rect(self):
        problem = self.gen._generate_formula_perimeter_rect()
        self.assertIn("Solve for", problem['problem'])
        self.assertTrue(problem['operation'] == "literal_eq_formula_perimeter")

    def test_formula_linear_y(self):
        problem = self.gen._generate_formula_linear_y()
        self.assertIn("Solve for", problem['problem'])
        self.assertTrue(problem['operation'] == "literal_eq_formula_linear_y")

    def test_generate_random(self):
        # Test that the main generate method returns a valid problem
        for _ in range(10):
            problem = self.gen.generate()
            self.assertIn("problem_id", problem)
            self.assertIn("operation", problem)
            self.assertIn("problem", problem)
            self.assertIn("steps", problem)
            self.assertIn("final_answer", problem)

if __name__ == '__main__':
    unittest.main()
