import unittest
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.geometry_area_perimeter_generator import GeometryAreaPerimeterGenerator
from helpers import DELIM


class TestGeometryAreaPerimeterGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GeometryAreaPerimeterGenerator()

    def test_format_and_z(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertIn("Perimeter=", res["final_answer"])
        self.assertIn("Area=", res["final_answer"])

    def test_rectangle_case(self):
        # Force rectangle for deterministic check
        import unittest.mock as mock

        with mock.patch(
            "generators.geometry_area_perimeter_generator.random.choice",
            return_value="rectangle",
        ), mock.patch(
            "generators.geometry_area_perimeter_generator.random.randint",
            side_effect=[4, 5],  # width, height
        ):
            res = self.gen.generate()
        perim = 2 * (4 + 5)
        area = 4 * 5
        self.assertEqual(res["final_answer"], f"Perimeter={perim}, Area={area}")


if __name__ == "__main__":
    unittest.main()
