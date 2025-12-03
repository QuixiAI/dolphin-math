import unittest
import sys
import os

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.unit_conversion_generator import UnitConversionGenerator
from helpers import DELIM


class TestUnitConversionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = UnitConversionGenerator()

    def test_conversion_correctness(self):
        res = self.gen.generate()
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        # Problem format: "Convert {value} from to"
        parts = res["problem"].split()
        value = int(parts[1])
        to_unit = parts[-1]
        final_val = int(res["final_answer"].split()[0])
        # Get factor from steps
        factor_step = next(s for s in res["steps"] if s.startswith("CONV_FACTOR"))
        factor = int(factor_step.split(DELIM)[2].split()[0])
        self.assertEqual(final_val, value * factor)


if __name__ == "__main__":
    unittest.main()
