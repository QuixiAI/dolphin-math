import unittest
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.volume_rect_prism_generator import VolumeRectPrismGenerator
from helpers import DELIM


class TestVolumeRectPrismGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = VolumeRectPrismGenerator()

    def test_volume_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        l = int(res["problem"].split("L=")[1].split(",")[0])
        w = int(res["problem"].split("W=")[1].split(",")[0])
        h = int(res["problem"].split("H=")[1])
        self.assertEqual(int(res["final_answer"]), l * w * h)


if __name__ == "__main__":
    unittest.main()
