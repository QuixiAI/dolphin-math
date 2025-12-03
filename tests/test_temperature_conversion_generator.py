import unittest
from unittest.mock import patch

from generators.temperature_conversion_generator import TemperatureConversionGenerator
from helpers import DELIM


class TestTemperatureConversionGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = TemperatureConversionGenerator()

    def test_f_to_c(self):
        with patch("generators.temperature_conversion_generator.random.choice", return_value=("F", "C")), \
             patch("generators.temperature_conversion_generator.random.randint", return_value=68):
            res = self.gen.generate()
        self.assertEqual(res["operation"], "convert_temperature")
        steps = res["steps"]
        self.assertTrue(steps[-1].startswith(f"Z{DELIM}"))
        # 68F -> 20 C
        self.assertIn("20", res["final_answer"])
        self.assertEqual(res["final_answer"], "20 C")

    def test_c_to_f(self):
        with patch("generators.temperature_conversion_generator.random.choice", return_value=("C", "F")), \
             patch("generators.temperature_conversion_generator.random.randint", return_value=0):
            res = self.gen.generate()
        # 0C -> 32F
        self.assertEqual(res["final_answer"], "32 F")
        self.assertTrue(any(s.startswith("M|9") for s in res["steps"]))

    def test_k_to_f(self):
        with patch("generators.temperature_conversion_generator.random.choice", return_value=("K", "F")), \
             patch("generators.temperature_conversion_generator.random.randint", return_value=273):
            res = self.gen.generate()
        self.assertEqual(res["final_answer"], "31.73 F")
        self.assertTrue(any(s.startswith("A|") for s in res["steps"]))


if __name__ == "__main__":
    unittest.main()
