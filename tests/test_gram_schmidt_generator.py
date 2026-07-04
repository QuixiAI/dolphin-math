import ast
import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.gram_schmidt_generator import GramSchmidtGenerator
from helpers import DELIM


def fmt_frac(value):
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def fmt_matrix(M):
    return "[" + ", ".join(
        "[" + ", ".join(fmt_frac(v) for v in row) + "]" for row in M
    ) + "]"


def parse_problem_vectors(problem):
    (matrix_txt,) = re.fullmatch(
        r"Apply Gram-Schmidt to vectors (\[\[.*\]\]) and give an "
        r"orthogonal basis, not normalized\.",
        problem,
    ).groups()
    return ast.literal_eval(matrix_txt)


def dot(a, b):
    return sum(Fraction(x) * Fraction(y) for x, y in zip(a, b))


def vec_sub(a, b):
    return [Fraction(x) - Fraction(y) for x, y in zip(a, b)]


def scalar_vec(c, v):
    return [Fraction(c) * Fraction(x) for x in v]


def gram_schmidt(vectors):
    basis = []
    for v in vectors:
        current = [Fraction(x) for x in v]
        for u in basis:
            coeff = dot(v, u) / dot(u, u)
            current = vec_sub(current, scalar_vec(coeff, u))
        basis.append(current)
    return basis


def oracle_answer(example):
    basis = gram_schmidt(parse_problem_vectors(example["problem"]))
    return f"orthogonal basis {fmt_matrix(basis)}"


def eval_fraction_expr(expr):
    expr = re.sub(r"-?\d+(?:/\d+)?",
                  lambda m: f"Fraction('{m.group(0)}')", expr)
    return eval(expr, {"__builtins__": {}, "Fraction": Fraction}, {})


def parse_basis_from_answer(answer):
    return [[Fraction(v) for v in row]
            for row in ast.literal_eval(
                answer.removeprefix("orthogonal basis ")
            )]


def check_step_arithmetic(example):
    vectors = parse_problem_vectors(example["problem"])
    basis = gram_schmidt(vectors)
    for raw_step in example["steps"]:
        parts = raw_step.split(DELIM)
        if parts[0] == "DOT":
            if eval_fraction_expr(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "PROJ_COEFF":
            if eval_fraction_expr(parts[2]) != Fraction(parts[3]):
                return False
        elif parts[0] == "GS_VECTOR" and parts[1].startswith("u"):
            match = re.fullmatch(r"u(\d+)(?: = v\d+)?", parts[1])
            if match is None:
                continue
            idx = int(match.group(1)) - 1
            if parts[2] != fmt_matrix([basis[idx]])[1:-1]:
                return False
        elif parts[0] == "CHECK":
            i, j = (int(n) - 1 for n in re.fullmatch(
                r"u(\d+)·u(\d+)", parts[1]
            ).groups())
            if dot(basis[i], basis[j]) != Fraction(parts[2]):
                return False
            if parts[3] != "orthogonal":
                return False
    return True


class TestGramSchmidtGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GramSchmidtGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_result_is_pairwise_orthogonal(self):
        for _ in range(300):
            result = self.gen.generate()
            basis = parse_basis_from_answer(result["final_answer"])
            for i in range(len(basis)):
                for j in range(i + 1, len(basis)):
                    self.assertEqual(dot(basis[i], basis[j]), 0)

    def test_variants_have_expected_count(self):
        for variant, count in (("two", 2), ("three", 3)):
            gen = GramSchmidtGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                basis = parse_basis_from_answer(result["final_answer"])
                self.assertEqual(len(basis), count)

    def test_no_degenerate_rendering(self):
        bad = re.compile(r"(?<!\d)1\*|\+ 0|--|\+ -")
        for _ in range(300):
            result = self.gen.generate()
            self.assertIsNone(bad.search(result["problem"]))
            self.assertIsNone(bad.search(result["final_answer"]))
            for raw_step in result["steps"]:
                self.assertIsNone(bad.search(raw_step), raw_step)

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
                self.assertNotIn(f"{DELIM}{DELIM}", raw_step)

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(100):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(ops, {"gram_schmidt_two", "gram_schmidt_three"})

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            GramSchmidtGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
