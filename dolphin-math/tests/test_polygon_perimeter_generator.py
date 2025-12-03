import unittest
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.polygon_perimeter_generator import PolygonPerimeterGenerator
from helpers import DELIM


class TestPolygonPerimeterGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = PolygonPerimeterGenerator()

    def test_perimeter_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        perim = int(res["final_answer"])
        sides_part = res["problem"].split(":")[1]
        sides = [int(s.strip()) for s in sides_part.split(",")]
        self.assertEqual(sum(sides), perim)


if __name__ == "__main__":
    unittest.main()
