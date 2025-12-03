import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.angle_relationships_generator import (
    AngleRelationshipsGenerator,
    AnglesWithParallelLinesGenerator,
    TriangleAngleSumGenerator,
)
from helpers import DELIM


class TestAngleRelationshipsGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = AngleRelationshipsGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("problem_id", result)
        self.assertIn("operation", result)
        self.assertIn("problem", result)
        self.assertIn("steps", result)
        self.assertIn("final_answer", result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            has_setup = any(s.startswith(f"ANGLE_SETUP{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup, "Missing ANGLE_SETUP step")

    def test_complementary(self):
        gen = AngleRelationshipsGenerator(relationship_type='complementary')
        for _ in range(5):
            result = gen.generate()
            self.assertIn("complementary", result["operation"])

    def test_supplementary(self):
        gen = AngleRelationshipsGenerator(relationship_type='supplementary')
        for _ in range(5):
            result = gen.generate()
            self.assertIn("supplementary", result["operation"])

    def test_vertical(self):
        gen = AngleRelationshipsGenerator(relationship_type='vertical')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "vertical_angles")


class TestAnglesWithParallelLinesGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = AnglesWithParallelLinesGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("operation", result)
        self.assertTrue(result["operation"].startswith("parallel_"))

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            self.assertIn("parallel", result["problem"].lower())
            has_setup = any(s.startswith(f"PARALLEL_SETUP{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup)


class TestTriangleAngleSumGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = TriangleAngleSumGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("operation", result)
        # Operation can be triangle_angle_sum, triangle_angle_sum_algebraic, or exterior_angle_theorem
        valid_ops = ["triangle_angle_sum", "triangle_angle_sum_algebraic", "exterior_angle_theorem"]
        self.assertIn(result["operation"], valid_ops)

    def test_generate_consistency(self):
        for _ in range(20):
            result = self.generator.generate()
            self.assertIn("triangle", result["problem"].lower())
            has_setup = any(s.startswith(f"TRI_ANGLE_SETUP{DELIM}") for s in result["steps"])
            self.assertTrue(has_setup)


if __name__ == '__main__':
    unittest.main()
