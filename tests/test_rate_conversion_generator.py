import unittest
from unittest.mock import patch

from generators.rate_conversion_generator import RateConversionGenerator
from helpers import DELIM


class TestRateConversionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = RateConversionGenerator()

    def _count_steps(self, steps, opcode):
        return sum(1 for s in steps if s.startswith(f"{opcode}{DELIM}"))

    def test_mph_to_ft_s(self):
        with patch("generators.rate_conversion_generator.random.choice") as mock_choice, \
             patch("generators.rate_conversion_generator.random.randint", return_value=2):
            # Choose mph -> ft/s scenario (index 0)
            mock_choice.return_value = {
                "from_unit": "mi/hr",
                "to_unit": "ft/s",
                "length_factor": 5280,
                "time_factor": 3600,
                "value_mult": 15,
                "length_first": True,
            }
            res = self.gen.generate()

        self.assertEqual(res["operation"], "convert_rate")
        self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(self._count_steps(res["steps"], "CONV_FACTOR"), 2)
        self.assertEqual(self._count_steps(res["steps"], "M"), 1)
        self.assertEqual(self._count_steps(res["steps"], "D"), 1)
        # 2 * 15 = 30 mph; 30 * 5280 / 3600 = 44 ft/s
        self.assertIn("ft/s", res["final_answer"])
        self.assertEqual(res["final_answer"], "44 ft/s")

    def test_ft_s_to_mph(self):
        with patch("generators.rate_conversion_generator.random.choice") as mock_choice, \
             patch("generators.rate_conversion_generator.random.randint", return_value=3):
            mock_choice.return_value = {
                "from_unit": "ft/s",
                "to_unit": "mi/hr",
                "length_factor": 5280,
                "time_factor": 3600,
                "value_mult": 22,
                "length_first": False,
            }
            res = self.gen.generate()

        self.assertEqual(self._count_steps(res["steps"], "M"), 1)
        self.assertEqual(self._count_steps(res["steps"], "D"), 1)
        # 3*22 = 66 ft/s -> mph: 66*3600/5280 = 45 mph
        self.assertEqual(res["final_answer"], "45 mi/hr")


if __name__ == "__main__":
    unittest.main()
