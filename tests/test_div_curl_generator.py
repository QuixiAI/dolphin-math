import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.div_curl_generator import DivCurlGenerator
from helpers import DELIM


def split_terms(expr):
    if expr == "0":
        return []
    return [raw for raw in expr.replace(" - ", " + -").split(" + ")
            if raw]


def parse_linear(expr, variables):
    coeffs = {var: 0 for var in variables}
    for raw in split_terms(expr):
        sign = -1 if raw.startswith("-") else 1
        raw = raw[1:] if raw.startswith("-") else raw
        coeff = sign
        var = None
        for factor in raw.split("*"):
            if factor.isdigit():
                coeff *= int(factor)
            elif factor in coeffs:
                var = factor
            else:
                raise AssertionError(f"bad factor {factor!r} in {expr!r}")
        if var is not None:
            coeffs[var] += coeff
    return coeffs


def oracle_answer(example):
    problem = example["problem"]
    if problem.startswith("For F(x,y)"):
        p_txt, q_txt = re.fullmatch(
            r"For F\(x,y\) = <(.+), (.+)>, compute the divergence "
            r"and scalar curl\.",
            problem,
        ).groups()
        p = parse_linear(p_txt, "xy")
        q = parse_linear(q_txt, "xy")
        div = p["x"] + q["y"]
        curl = q["x"] - p["y"]
        return f"divergence {div}; curl {curl}"
    p_txt, q_txt, r_txt = re.fullmatch(
        r"For F\(x,y,z\) = <(.+), (.+), (.+)>, compute the "
        r"divergence and curl\.",
        problem,
    ).groups()
    p = parse_linear(p_txt, "xyz")
    q = parse_linear(q_txt, "xyz")
    r = parse_linear(r_txt, "xyz")
    div = p["x"] + q["y"] + r["z"]
    curl_i = r["y"] - q["z"]
    curl_j = p["z"] - r["x"]
    curl_k = q["x"] - p["y"]
    return f"divergence {div}; curl <{curl_i}, {curl_j}, {curl_k}>"


def check_step_arithmetic(example):
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] in {"DIV_SUM", "CURL_COMPONENT"}:
            if Fraction(eval(parts[2], {"__builtins__": {}}, {})) != Fraction(parts[3]):
                return False
    return True


class TestDivCurlGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DivCurlGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_all_variants(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_variant_outputs(self):
        cases = {
            "plane": "scalar curl",
            "space": "divergence and curl",
        }
        for variant, phrase in cases.items():
            gen = DivCurlGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertIn(phrase, result["problem"])

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ 0|--")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for s in result["steps"]:
                self.assertLessEqual(len(s.split(DELIM)) - 1, 4, s)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 2)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            DivCurlGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
