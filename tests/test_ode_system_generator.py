import ast
import math
import os
import random
import re
import sys
import unittest
from fractions import Fraction
from math import gcd, isqrt

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.ode_system_generator import ODESystemGenerator
from helpers import DELIM


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v)))
            for i in range(len(A))]


def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def fmt_vector(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def fmt_terms(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        text = body if body and abs(coeff) == 1 else (
            f"{abs(coeff)}{body}" if body else str(abs(coeff))
        )
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def char_poly(trace, det):
    return fmt_terms([(1, "r^2"), (-trace, "r"), (det, "")])


def eigenvalues(A):
    trace = A[0][0] + A[1][1]
    det = det2(A)
    disc = trace * trace - 4 * det
    root = isqrt(disc)
    assert root * root == disc
    return sorted([(trace - root) // 2, (trace + root) // 2])


def rref(M):
    work = [[Fraction(v) for v in row] for row in M]
    rows, cols = len(work), len(work[0])
    pivot_cols = []
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows)
                      if work[r][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [v / scale for v in work[pivot_row]]
        for r in range(rows):
            if r == pivot_row or work[r][col] == 0:
                continue
            factor = work[r][col]
            work[r] = [
                work[r][j] - factor * work[pivot_row][j]
                for j in range(cols)
            ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, pivot_cols


def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


def primitive_int_vector(vec):
    scale = 1
    for value in vec:
        scale = lcm(scale, value.denominator)
    ints = [value.numerator * (scale // value.denominator) for value in vec]
    common = 0
    for value in ints:
        common = gcd(common, abs(value))
    ints = [value // common for value in ints]
    first = next(value for value in ints if value != 0)
    if first < 0:
        ints = [-value for value in ints]
    return ints


def subtract_lambda(A, lam):
    return [
        [A[i][j] - (lam if i == j else 0) for j in range(2)]
        for i in range(2)
    ]


def null_vector(M):
    R, pivot_cols = rref(M)
    free_cols = [j for j in range(2) if j not in pivot_cols]
    vec = [Fraction(0), Fraction(0)]
    vec[free_cols[0]] = Fraction(1)
    for row, pivot in enumerate(pivot_cols):
        vec[pivot] = -R[row][free_cols[0]]
    return primitive_int_vector(vec)


def exp_t(lam):
    if lam == 1:
        return "e^t"
    if lam == -1:
        return "e^(-t)"
    return f"e^({lam}t)"


def combo_text(terms):
    pieces = []
    for coeff, lam in terms:
        if coeff == 0:
            continue
        body = exp_t(lam) if abs(coeff) == 1 else f"{abs(coeff)}{exp_t(lam)}"
        if not pieces:
            pieces.append(body if coeff > 0 else f"-{body}")
        elif coeff > 0:
            pieces.append(f"+ {body}")
        else:
            pieces.append(f"- {body}")
    return " ".join(pieces) if pieces else "0"


def solution_vector(constants, lambdas, vectors):
    entries = []
    for row in range(2):
        terms = [
            (constants[i] * vectors[i][row], lambdas[i])
            for i in range(2)
        ]
        entries.append(combo_text(terms))
    return f"x(t) = [{entries[0]}, {entries[1]}]"


def parse_problem(problem):
    match = re.fullmatch(
        r"Solve x' = A x for A = (\[\[.*\]\]) with x\(0\) = "
        r"(\[.*\]) using eigenvalues\.",
        problem,
    )
    assert match is not None, problem
    return ast.literal_eval(match.group(1)), ast.literal_eval(match.group(2))


def solve_constants(vectors, x0):
    v1, v2 = vectors
    det = v1[0] * v2[1] - v2[0] * v1[1]
    c1 = Fraction(x0[0] * v2[1] - v2[0] * x0[1], det)
    c2 = Fraction(v1[0] * x0[1] - x0[0] * v1[1], det)
    assert c1.denominator == 1 and c2.denominator == 1
    return [c1.numerator, c2.numerator]


def oracle_parts(example):
    A, x0 = parse_problem(example["problem"])
    lambdas = eigenvalues(A)
    vectors = [null_vector(subtract_lambda(A, lam)) for lam in lambdas]
    constants = solve_constants(vectors, x0)
    return {
        "A": A,
        "x0": x0,
        "trace": A[0][0] + A[1][1],
        "det": det2(A),
        "lambdas": lambdas,
        "vectors": vectors,
        "constants": constants,
        "answer": solution_vector(constants, lambdas, vectors),
    }


def oracle_answer(example):
    return oracle_parts(example)["answer"]


def solution_satisfies_system(example):
    parts = oracle_parts(example)
    t = 0.27
    x = [0.0, 0.0]
    xp = [0.0, 0.0]
    for c, lam, vec in zip(parts["constants"], parts["lambdas"],
                           parts["vectors"]):
        factor = c * math.exp(lam * t)
        for i in range(2):
            x[i] += factor * vec[i]
            xp[i] += lam * factor * vec[i]
    Ax = matvec(parts["A"], x)
    x_at_zero = [sum(c * vec[i] for c, vec in zip(parts["constants"],
                                                  parts["vectors"]))
                 for i in range(2)]
    return (all(abs(xp[i] - Ax[i]) < 1e-8 for i in range(2)) and
            x_at_zero == parts["x0"])


def check_step_arithmetic(example):
    parts = oracle_parts(example)
    A = parts["A"]
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "TRACE":
            if int(fields[2]) != parts["trace"]:
                return False
        elif op == "M":
            if int(fields[1]) * int(fields[2]) != int(fields[3]):
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
        elif op == "DET2":
            if fields[1:] != ["ad - bc", str(parts["det"])]:
                return False
        elif op == "CHAR_EQ":
            expected = f"{char_poly(parts['trace'], parts['det'])} = 0"
            if fields[1:] != ["det(A - rI)", expected]:
                return False
        elif op == "EIGENPAIR":
            lam = int(fields[1].split(" = ")[1])
            vec = ast.literal_eval(fields[2])
            if matvec(subtract_lambda(A, lam), vec) != [0, 0]:
                return False
        elif op == "CHECK":
            vec = ast.literal_eval(fields[1].removeprefix("A*"))
            Av = ast.literal_eval(fields[2])
            if matvec(A, vec) != Av:
                return False
        elif op == "SOLVE_CONST":
            expected = [f"C1 = {parts['constants'][0]}",
                        f"C2 = {parts['constants'][1]}"]
            if fields[1:] != expected:
                return False
        elif op == "Z":
            if fields[1:] != [parts["answer"]]:
                return False
    return True


class TestODESystemGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = ODESystemGenerator()

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

    def test_solution_satisfies_system_and_initial_vector(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(solution_satisfies_system(result),
                            result["problem"])

    def test_step_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_arithmetic(result), result["steps"])

    def test_fixed_variant_constructor(self):
        gen = ODESystemGenerator("two_by_two_distinct")
        result = gen.generate()
        self.assertEqual(result["operation"], "ode_system_two_by_two_distinct")
        with self.assertRaises(ValueError):
            ODESystemGenerator("bogus")

    def test_no_degenerate_rendering(self):
        bad = re.compile(
            r"(?<![A-Za-z0-9])1r|(?<![A-Za-z0-9])1e|"
            r"(?<![A-Za-z0-9])1v|\+ -|--"
        )
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


if __name__ == "__main__":
    unittest.main()
