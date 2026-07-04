import random

from base_generator import ProblemGenerator
from helpers import step, jid


VARS3 = ["A", "B", "C"]
VARS2 = ["A", "B"]

KMAP_PATTERNS = [
    ("A", {"10", "11"}, [("10, 11", "A")], "A"),
    ("NOT A", {"00", "01"}, [("00, 01", "NOT A")], "NOT A"),
    ("B", {"01", "11"}, [("01, 11", "B")], "B"),
    ("NOT B", {"00", "10"}, [("00, 10", "NOT B")], "NOT B"),
    ("A AND B", {"11"}, [("11", "A AND B")], "A AND B"),
    (
        "A OR B",
        {"01", "10", "11"},
        [("10, 11", "A"), ("01, 11", "B")],
        "A OR B",
    ),
    (
        "A XOR B",
        {"01", "10"},
        [("01", "NOT A AND B"), ("10", "A AND NOT B")],
        "(NOT A AND B) OR (A AND NOT B)",
    ),
]


def bit_rows(width):
    return [format(value, f"0{width}b") for value in range(2 ** width)]


def assignment_text(bits, variables):
    return ", ".join(f"{var}={bit}" for var, bit in zip(variables, bits))


def minterm(bits, variables):
    terms = [var if bit == "1" else f"NOT {var}"
             for var, bit in zip(variables, bits)]
    return " AND ".join(terms)


def maxterm(bits, variables):
    terms = [var if bit == "0" else f"NOT {var}"
             for var, bit in zip(variables, bits)]
    return " OR ".join(terms)


def join_terms(terms, connector, identity):
    if not terms:
        return identity
    if len(terms) == 1:
        return terms[0]
    return f" {connector} ".join(f"({term})" for term in terms)


def truth_table_text(values_by_row):
    return ", ".join(f"{row}->{values_by_row[row]}"
                     for row in sorted(values_by_row))


def random_truth_values():
    rows = bit_rows(3)
    while True:
        values = {row: random.randint(0, 1) for row in rows}
        ones = sum(values.values())
        if 2 <= ones <= 6:
            return values


class BooleanAlgebraGenerator(ProblemGenerator):
    """
    Boolean truth-table normal forms and Karnaugh-map simplification.

    Variants:
    - dnf: build disjunctive normal form from the 1 rows
    - cnf: build conjunctive normal form from the 0 rows
    - kmap: simplify a 2-variable truth table with a Karnaugh map

    Op-codes used:
    - BOOL_SETUP: variables and requested form
    - TRUTH_ROW: one truth-table row
    - MINTERM / MAXTERM: row-to-term conversion
    - DNF_FORM / CNF_FORM: assembled normal form
    - KMAP_SETUP / KMAP_ROW / KMAP_GROUP / KMAP_SIMPLIFY: Karnaugh map trace
    - Z: exact Boolean expression
    """

    VARIANTS = ["dnf", "cnf", "kmap"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant in ("dnf", "cnf"):
            values = random_truth_values()
            rows = bit_rows(3)
            form_name = "DNF" if variant == "dnf" else "CNF"
            focus_value = 1 if variant == "dnf" else 0
            steps = [
                step("BOOL_SETUP", "variables A, B, C",
                     f"{form_name} from f={focus_value} rows"),
            ]
            terms = []
            for row in rows:
                value = values[row]
                steps.append(step("TRUTH_ROW", assignment_text(row, VARS3),
                                  f"f={value}"))
                if value == focus_value:
                    if variant == "dnf":
                        term = minterm(row, VARS3)
                        steps.append(step("MINTERM", row, term))
                    else:
                        term = maxterm(row, VARS3)
                        steps.append(step("MAXTERM", row, term))
                    terms.append(term)
            if variant == "dnf":
                expression = join_terms(terms, "OR", "0")
                answer = f"DNF = {expression}"
                steps.append(step("DNF_FORM", expression))
                problem = (
                    f"Truth table for f(A,B,C): {truth_table_text(values)}. "
                    f"Write a disjunctive normal form (DNF)."
                )
            else:
                expression = join_terms(terms, "AND", "1")
                answer = f"CNF = {expression}"
                steps.append(step("CNF_FORM", expression))
                problem = (
                    f"Truth table for f(A,B,C): {truth_table_text(values)}. "
                    f"Write a conjunctive normal form (CNF)."
                )
        else:
            _, ones, groups, expression = random.choice(KMAP_PATTERNS)
            values = {row: int(row in ones) for row in bit_rows(2)}
            steps = [
                step("BOOL_SETUP", "variables A, B", "K-map simplify"),
                step("KMAP_SETUP", "rows A=0,A=1", "columns B=0,B=1"),
                step("KMAP_ROW", "A=0",
                     f"{values['00']}, {values['01']}"),
                step("KMAP_ROW", "A=1",
                     f"{values['10']}, {values['11']}"),
            ]
            for cells, term in groups:
                steps.append(step("KMAP_GROUP", cells, term))
            steps.append(step("KMAP_SIMPLIFY", expression))
            answer = f"simplified = {expression}"
            problem = (
                f"Use a 2-variable Karnaugh map to simplify f(A,B) with "
                f"truth table {truth_table_text(values)}."
            )

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"boolean_algebra_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
