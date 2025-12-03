import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.volume_3d_generator import (
    VolumePrismGenerator,
    VolumeCylinderGenerator,
    SurfaceAreaPrismGenerator,
    SurfaceAreaCylinderGenerator,
)
from helpers import DELIM


class TestVolumePrismGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = VolumePrismGenerator()

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
            self.assertIn("volume", result["problem"].lower())
            self.assertIn("cubic units", result["final_answer"])

    def test_rectangular_prism(self):
        gen = VolumePrismGenerator(prism_type='rectangular')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "volume_rectangular_prism")

    def test_triangular_prism(self):
        gen = VolumePrismGenerator(prism_type='triangular')
        for _ in range(5):
            result = gen.generate()
            self.assertEqual(result["operation"], "volume_triangular_prism")


class TestVolumeCylinderGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = VolumeCylinderGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertIn("operation", result)
        self.assertEqual(result["operation"], "volume_cylinder")

    def test_pi_symbol(self):
        gen = VolumeCylinderGenerator(use_pi_symbol=True)
        result = gen.generate()
        self.assertIn("π", result["final_answer"])

    def test_decimal_mode(self):
        gen = VolumeCylinderGenerator(use_pi_symbol=False)
        result = gen.generate()
        self.assertNotIn("π", result["final_answer"])


class TestSurfaceAreaPrismGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = SurfaceAreaPrismGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["operation"], "surface_area_rectangular_prism")
        self.assertIn("square units", result["final_answer"])

    def test_generate_consistency(self):
        for _ in range(10):
            result = self.generator.generate()
            self.assertIn("surface area", result["problem"].lower())
            has_faces = any(s.startswith(f"SA_FACES{DELIM}") for s in result["steps"])
            self.assertTrue(has_faces)


class TestSurfaceAreaCylinderGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = SurfaceAreaCylinderGenerator()

    def test_generate_output_format(self):
        result = self.generator.generate()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["operation"], "surface_area_cylinder")

    def test_pi_symbol(self):
        gen = SurfaceAreaCylinderGenerator(use_pi_symbol=True)
        result = gen.generate()
        self.assertIn("π", result["final_answer"])


if __name__ == '__main__':
    unittest.main()
