import unittest
import sys
import os

# Ensure repo root is on sys.path for package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.mixed_number_operations_random import MixedNumberOperationsRandom


class TestMixedNumberOperationsRandom(unittest.TestCase):
    def test_random_variants_cover_all_ops(self):
        gen = MixedNumberOperationsRandom()
        seen = set()
        # Run a few times to cover all four; statistically likely within 20 tries.
        for _ in range(20):
            res = gen.generate()
            seen.add(res["operation"])
            if len(seen) == 4:
                break
        self.assertEqual(len(seen), 4, f"Expected all mixed-number ops, saw {seen}")


if __name__ == "__main__":
    unittest.main()
