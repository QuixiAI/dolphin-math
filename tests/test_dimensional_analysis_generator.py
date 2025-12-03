import unittest
from unittest.mock import patch

from generators.dimensional_analysis_generator import DimensionalAnalysisGenerator
from helpers import DELIM


class TestDimensionalAnalysisGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = DimensionalAnalysisGenerator()

    def _count_steps(self, steps, opcode):
        return sum(1 for s in steps if s.startswith(f"{opcode}{DELIM}"))

    def test_dosing(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=2):
            mock_choice.return_value = {
                "type": "dosing",
                "desc": "Medication dosing",
                "value_unit": "kg",
                "target_unit": "mg",
                "factors": [("dosage", "10 mg", "1 kg")],
            }
            res = self.gen.generate()
        self.assertEqual(res["operation"], "dimensional_analysis")
        self.assertEqual(self._count_steps(res["steps"], "CONV_FACTOR"), 1)
        self.assertEqual(self._count_steps(res["steps"], "M"), 1)
        self.assertEqual(self._count_steps(res["steps"], "D"), 0)
        # value = 2*5 = 10 kg -> 100 mg
        self.assertEqual(res["final_answer"], "100.0 mg")

    def test_flow(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=2):
            mock_choice.return_value = {
                "type": "flow",
                "desc": "IV flow rate",
                "value_unit": "L/min",
                "target_unit": "mL/hr",
                "factors": [("volume", "1000 mL", "1 L"), ("time", "60 min", "1 hr")],
            }
            res = self.gen.generate()
        self.assertEqual(self._count_steps(res["steps"], "M"), 2)
        self.assertEqual(self._count_steps(res["steps"], "D"), 0)
        # value = 2*2=4 L/min; 4*1000=4000; 4000*60=240000 mL/hr
        self.assertEqual(res["final_answer"], "240000.0 mL/hr")

    def test_pressure_kpa_to_atm(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=1):
            mock_choice.return_value = {
                "type": "pressure_atm",
                "desc": "Pressure conversion",
                "value_unit": "kPa",
                "target_unit": "atm",
                "factors": [("pressure", "1 atm", "101.325 kPa")],
            }
            res = self.gen.generate()
        # value = 1*3=3 kPa; 3*1 / 101.325 ≈ 0.0296 atm
        self.assertTrue(res["final_answer"].endswith(" atm"))
        self.assertIn("0.0296", res["final_answer"])

    def test_dose_rate_mcg_min_to_mg_hr(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=1):
            mock_choice.return_value = {
                "type": "dose_rate",
                "desc": "Dose rate conversion",
                "value_unit": "mcg/min",
                "target_unit": "mg/hr",
                "factors": [
                    ("time", "60 min", "1 hr"),
                    ("mass", "1 mg", "1000 mcg"),
                ],
            }
            res = self.gen.generate()
        # value = 10 mcg/min -> *60 = 600; /1000 = 0.6 mg/hr
        self.assertEqual(res["final_answer"], "0.6 mg/hr")

    def test_pressure(self):
        with patch("generators.dimensional_analysis_generator.random.choice") as mock_choice, \
             patch("generators.dimensional_analysis_generator.random.randint", return_value=3):
            mock_choice.return_value = {
                "type": "pressure",
                "desc": "Pressure conversion",
                "value_unit": "psi",
                "target_unit": "kPa",
                "factors": [("pressure", "6.9 kPa", "1 psi")],
            }
            res = self.gen.generate()
        self.assertEqual(self._count_steps(res["steps"], "M"), 1)
        self.assertEqual(self._count_steps(res["steps"], "D"), 0)
        # value = 3*3=9 psi; 9*6.9=62.1
        self.assertEqual(res["final_answer"], "62.1 kPa")


if __name__ == "__main__":
    unittest.main()
