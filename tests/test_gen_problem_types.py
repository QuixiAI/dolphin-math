import os
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from tools.gen_problem_types import (
    collect, render, title_for, description_for,
)


class TestGenProblemTypes(unittest.TestCase):
    def test_title_camel_split(self):
        self.assertEqual(title_for("MultiDigitAdditionGenerator"),
                         "Multi Digit Addition")

    def test_description_stops_before_variants(self):
        class Fake:
            """A short lead line.

            Variants:
            - should not appear
            """
        desc = description_for(Fake)
        self.assertEqual(desc, "A short lead line.")
        self.assertNotIn("should not appear", desc)

    def test_collect_covers_every_class(self):
        from dolphin_math_datagen import ALL_GENERATORS
        classes = {type(g).__name__ for g in ALL_GENERATORS}
        entries = collect(seed=0)
        self.assertEqual({e["class"] for e in entries}, classes)
        for e in entries:
            self.assertIsNotNone(e["example"])
            self.assertTrue(e["variants"])
            self.assertIn("problem", e["example"])

    def test_render_is_deterministic(self):
        self.assertEqual(render(collect(seed=0)),
                         render(collect(seed=0)))

    def test_disk_file_is_fresh(self):
        path = os.path.join(repo_root, "PROBLEM_TYPES.md")
        with open(path, encoding="utf-8") as fh:
            on_disk = fh.read()
        self.assertEqual(on_disk, render(collect(seed=0)),
                         "PROBLEM_TYPES.md is stale; regenerate with "
                         "tools/gen_problem_types.py")


if __name__ == "__main__":
    unittest.main()
