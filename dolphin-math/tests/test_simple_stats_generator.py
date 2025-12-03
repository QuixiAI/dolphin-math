import unittest
import sys
import os
from statistics import mean, median, multimode

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.simple_stats_generator import SimpleStatsGenerator
from helpers import DELIM


class TestSimpleStatsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = SimpleStatsGenerator()

    def test_stats_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        data_str = res["problem"].split("of")[1].strip().strip("[]")
        data = [int(x.strip()) for x in data_str.split(",") if x.strip()]
        op = res["operation"]
        if op == "mean":
            expected = round(mean(data), 2)
            self.assertAlmostEqual(float(res["final_answer"]), expected, places=2)
        elif op == "median":
            self.assertAlmostEqual(float(res["final_answer"]), float(median(data)))
        else:
            modes = multimode(data)
            result_modes = [int(x.strip()) for x in res["final_answer"].split(",")]
            self.assertCountEqual(result_modes, modes)


if __name__ == "__main__":
    unittest.main()
