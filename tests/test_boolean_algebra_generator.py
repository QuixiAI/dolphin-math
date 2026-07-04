import itertools
import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.boolean_algebra_generator import BooleanAlgebraGenerator
from helpers import DELIM


VARS3 = ["A", "B", "C"]
VARS2 = ["A", "B"]

DNF_RE = re.compile(
    r"Truth table for f\(A,B,C\): (.+)\. Write a disjunctive normal form "
    r"\(DNF\)\."
)
CNF_RE = re.compile(
    r"Truth table for f\(A,B,C\): (.+)\. Write a conjunctive normal form "
    r"\(CNF\)\."
)
KMAP_RE = re.compile(
    r"Use a 2-variable Karnaugh map to simplify f\(A,B\) with truth table "
    r"(.+)\."
)


def bit_rows(width):
    return [format(value, f"0{width}b") for value in range(2 ** width)]


def parse_table(text, width):
    rows = {}
    for piece in text.split(", "):
        row, value = piece.split("->")
        assert re.fullmatch(r"[01]+", row), text
        assert len(row) == width, text
        rows[row] = int(value)
    return rows


def parse_problem(problem):
    match = DNF_RE.fullmatch(problem)
    if match:
        return {"variant": "dnf", "values": parse_table(match.group(1), 3)}
    match = CNF_RE.fullmatch(problem)
    if match:
        return {"variant": "cnf", "values": parse_table(match.group(1), 3)}
    match = KMAP_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "kmap", "values": parse_table(match.group(1), 2)}


def assignment_text(bits, variables):
    return ", ".join(f"{var}={bit}" for var, bit in zip(variables, bits))


def minterm(bits, variables):
    return " AND ".join(var if bit == "1" else f"NOT {var}"
                        for var, bit in zip(variables, bits))


def maxterm(bits, variables):
    return " OR ".join(var if bit == "0" else f"NOT {var}"
                       for var, bit in zip(variables, bits))


def join_terms(terms, connector, identity):
    if not terms:
        return identity
    if len(terms) == 1:
        return terms[0]
    return f" {connector} ".join(f"({term})" for term in terms)


def normal_form_answer(parts):
    values = parts["values"]
    if parts["variant"] == "dnf":
        terms = [minterm(row, VARS3) for row in bit_rows(3) if values[row] == 1]
        return f"DNF = {join_terms(terms, 'OR', '0')}"
    if parts["variant"] == "cnf":
        terms = [maxterm(row, VARS3) for row in bit_rows(3) if values[row] == 0]
        return f"CNF = {join_terms(terms, 'AND', '1')}"
    return f"simplified = {kmap_simplify(values)}"


def cover_for_term(term):
    covers = set()
    for row in bit_rows(2):
        a, b = row
        ok = True
        if "NOT A" in term:
            ok &= a == "0"
        elif "A" in term:
            ok &= a == "1"
        if "NOT B" in term:
            ok &= b == "0"
        elif "B" in term:
            ok &= b == "1"
        if ok:
            covers.add(row)
    return covers


def format_kmap_terms(terms):
    if len(terms) == 1:
        return terms[0]
    rendered = []
    for term in terms:
        rendered.append(f"({term})" if " AND " in term else term)
    return " OR ".join(rendered)


def kmap_simplify(values):
    ones = {row for row, value in values.items() if value == 1}
    if not ones:
        return "0"
    if ones == set(bit_rows(2)):
        return "1"
    candidates = [
        ("A", {"10", "11"}, 1),
        ("B", {"01", "11"}, 1),
        ("NOT A", {"00", "01"}, 1),
        ("NOT B", {"00", "10"}, 1),
        ("NOT A AND NOT B", {"00"}, 2),
        ("NOT A AND B", {"01"}, 2),
        ("A AND NOT B", {"10"}, 2),
        ("A AND B", {"11"}, 2),
    ]
    valid = [item for item in candidates if item[1] <= ones]
    best = None
    for size in range(1, len(valid) + 1):
        for combo in itertools.combinations(valid, size):
            cover = set().union(*(item[1] for item in combo))
            if cover != ones:
                continue
            literal_count = sum(item[2] for item in combo)
            terms = [item[0] for item in combo]
            score = (size, literal_count, format_kmap_terms(terms))
            if best is None or score < best[0]:
                best = (score, terms)
        if best is not None:
            return format_kmap_terms(best[1])
    raise AssertionError(f"no cover for {values}")


def oracle_answer(example):
    return normal_form_answer(parse_problem(example["problem"]))


def check_step_content(example):
    parts = parse_problem(example["problem"])
    values = parts["values"]
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "TRUTH_ROW":
            match = re.fullmatch(
                r"A=([01]), B=([01]), C=([01])",
                fields[1],
            )
            if match is None:
                return False
            row = "".join(match.groups())
            if fields[2] != f"f={values[row]}":
                return False
        elif op == "MINTERM":
            row = fields[1]
            if values[row] != 1 or fields[2] != minterm(row, VARS3):
                return False
        elif op == "MAXTERM":
            row = fields[1]
            if values[row] != 0 or fields[2] != maxterm(row, VARS3):
                return False
        elif op == "DNF_FORM":
            if fields[1] != normal_form_answer(parts).replace("DNF = ", ""):
                return False
        elif op == "CNF_FORM":
            if fields[1] != normal_form_answer(parts).replace("CNF = ", ""):
                return False
        elif op == "KMAP_ROW":
            if fields[1] == "A=0":
                if fields[2] != f"{values['00']}, {values['01']}":
                    return False
            elif fields[1] == "A=1":
                if fields[2] != f"{values['10']}, {values['11']}":
                    return False
            else:
                return False
        elif op == "KMAP_GROUP":
            cells = set(fields[1].split(", "))
            if not cells <= {row for row, value in values.items() if value == 1}:
                return False
            if cover_for_term(fields[2]) != cells:
                return False
        elif op == "KMAP_SIMPLIFY":
            if fields[1] != kmap_simplify(values):
                return False
        elif op == "Z":
            if fields[1:] != [normal_form_answer(parts)]:
                return False
    return True


class TestBooleanAlgebraGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = BooleanAlgebraGenerator()

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

    def test_step_content(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_step_content(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("dnf", "cnf", "kmap"):
            gen = BooleanAlgebraGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"boolean_algebra_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            BooleanAlgebraGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
