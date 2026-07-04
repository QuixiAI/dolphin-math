import os
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.optics_generator import OpticsGenerator
from helpers import DELIM


SNELL_RE = re.compile(
    r"A ray goes from medium n1=(\d+) to n2=(\d+)\. Given "
    r"sin\(theta1\)=([^,]+), use Snell's law to find sin\(theta2\)\."
)
LENS_RE = re.compile(
    r"A thin lens has focal length f=(\d+) cm and object distance "
    r"d_o=(\d+) cm\. Find image distance d_i\."
)
MIRROR_RE = re.compile(
    r"A concave mirror has focal length f=(\d+) cm, object distance "
    r"d_o=(\d+) cm, and object height h_o=(\d+) cm\. Find d_i, "
    r"magnification m, and image height h_i\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def fraction_text(value):
    return str(Fraction(value))


def expected_snell(problem):
    n1_raw, n2_raw, sin1_raw = SNELL_RE.fullmatch(problem).groups()
    n1 = int(n1_raw)
    n2 = int(n2_raw)
    sin1 = Fraction(sin1_raw)
    product = n1 * sin1
    sin2 = product / n2
    steps = [
        make_step("OPTICS_SETUP", "snell", f"n1={n1}, n2={n2}",
                  f"sin(theta1)={fraction_text(sin1)}"),
        make_step("OPTICS_FORMULA", "n1*sin(theta1)=n2*sin(theta2)"),
        make_step("M", n1, fraction_text(sin1), fraction_text(product)),
        make_step("D", fraction_text(product), n2, fraction_text(sin2)),
    ]
    answer = f"sin(theta2)={fraction_text(sin2)}"
    return steps, answer


def lens_values(focal, object_distance):
    inv_f = Fraction(1, focal)
    inv_do = Fraction(1, object_distance)
    inv_di = inv_f - inv_do
    image_distance = Fraction(1, inv_di)
    return inv_f, inv_do, inv_di, image_distance


def expected_lens(problem):
    focal, object_distance = (
        int(value) for value in LENS_RE.fullmatch(problem).groups()
    )
    inv_f, inv_do, inv_di, image_distance = lens_values(
        focal, object_distance
    )
    steps = [
        make_step("OPTICS_SETUP", "thin_lens",
                  f"f={focal}", f"d_o={object_distance}"),
        make_step("OPTICS_FORMULA", "1/f=1/d_o+1/d_i"),
        make_step("D", 1, focal, fraction_text(inv_f)),
        make_step("D", 1, object_distance, fraction_text(inv_do)),
        make_step("S", fraction_text(inv_f), fraction_text(inv_do),
                  fraction_text(inv_di)),
        make_step("D", 1, fraction_text(inv_di),
                  fraction_text(image_distance)),
    ]
    answer = f"d_i={fraction_text(image_distance)} cm"
    return steps, answer


def expected_mirror(problem):
    focal, object_distance, object_height = (
        int(value) for value in MIRROR_RE.fullmatch(problem).groups()
    )
    inv_f, inv_do, inv_di, image_distance = lens_values(
        focal, object_distance
    )
    magnification = -image_distance / object_distance
    image_height = magnification * object_height
    steps = [
        make_step("OPTICS_SETUP", "mirror_magnification",
                  f"f={focal}, d_o={object_distance}",
                  f"h_o={object_height}"),
        make_step("OPTICS_FORMULA", "1/f=1/d_o+1/d_i"),
        make_step("D", 1, focal, fraction_text(inv_f)),
        make_step("D", 1, object_distance, fraction_text(inv_do)),
        make_step("S", fraction_text(inv_f), fraction_text(inv_do),
                  fraction_text(inv_di)),
        make_step("D", 1, fraction_text(inv_di),
                  fraction_text(image_distance)),
        make_step("OPTICS_FORMULA", "m=-d_i/d_o, h_i=m*h_o"),
        make_step("D", fraction_text(-image_distance), object_distance,
                  fraction_text(magnification)),
        make_step("M", fraction_text(magnification), object_height,
                  fraction_text(image_height)),
    ]
    answer = (
        f"d_i={fraction_text(image_distance)} cm; "
        f"m={fraction_text(magnification)}; "
        f"h_i={fraction_text(image_height)} cm"
    )
    return steps, answer


def expected_flow(example):
    problem = example["problem"]
    if SNELL_RE.fullmatch(problem):
        steps, answer = expected_snell(problem)
    elif LENS_RE.fullmatch(problem):
        steps, answer = expected_lens(problem)
    else:
        steps, answer = expected_mirror(problem)
    steps.append(make_step("Z", answer))
    return steps, answer


class TestOpticsGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = OpticsGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_arithmetic_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                fields = raw_step.split(DELIM)
                if fields[0] == "A":
                    self.assertEqual(Fraction(fields[1]) + Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "S":
                    self.assertEqual(Fraction(fields[1]) - Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "M":
                    self.assertEqual(Fraction(fields[1]) * Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)
                elif fields[0] == "D":
                    self.assertEqual(Fraction(fields[1]) / Fraction(fields[2]),
                                     Fraction(fields[3]), raw_step)

    def test_variants_are_available(self):
        for variant in OpticsGenerator.VARIANTS:
            result = OpticsGenerator(variant).generate()
            self.assertEqual(result["operation"], f"optics_{variant}")
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer)
            self.assertEqual(result["steps"], expected_steps)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            OpticsGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
