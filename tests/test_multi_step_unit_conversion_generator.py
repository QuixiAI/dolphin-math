import unittest
from unittest.mock import patch

from generators.multi_step_unit_conversion_generator import MultiStepUnitConversionGenerator
from helpers import DELIM


class TestMultiStepUnitConversionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MultiStepUnitConversionGenerator()

    def _count_steps(self, steps, opcode):
        return sum(1 for s in steps if s.startswith(f"{opcode}{DELIM}"))

    def test_area_conversion_steps(self):
        with patch("generators.multi_step_unit_conversion_generator.random.choice", side_effect=[("m", "cm", 100), "area"]), \
             patch("generators.multi_step_unit_conversion_generator.random.randint", return_value=3):
            res = self.gen.generate()

        self.assertEqual(res["operation"], "convert_area")
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(self._count_steps(res["steps"], "CONV_FACTOR"), 2)
        self.assertEqual(self._count_steps(res["steps"], "M"), 2)
        self.assertIn("cm^2", res["final_answer"])
        self.assertEqual(res["final_answer"], "30000 cm^2")

    def test_volume_conversion_steps(self):
        with patch("generators.multi_step_unit_conversion_generator.random.choice", side_effect=[("ft", "in", 12), "volume"]), \
             patch("generators.multi_step_unit_conversion_generator.random.randint", return_value=2):
            res = self.gen.generate()

        self.assertEqual(res["operation"], "convert_volume")
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(self._count_steps(res["steps"], "CONV_FACTOR"), 3)
        self.assertEqual(self._count_steps(res["steps"], "M"), 3)
        self.assertIn("in^3", res["final_answer"])
        # 2 * 12^3 = 3456
        self.assertEqual(res["final_answer"], "3456 in^3")


if __name__ == "__main__":
    unittest.main()
