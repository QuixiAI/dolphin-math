import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.factor_trinomial_generator import FactorTrinomialGenerator
from helpers import DELIM


def parse_problem(problem):
    """'Factor: x^2 - 2x - 8' -> (var, b, c)."""
    expr = problem.split(": ", 1)[1]
    m = re.fullmatch(r"([a-z])\^2 ([+-]) (\d*)\1 ([+-]) (\d+)", expr)
    assert m, expr
    var = m.group(1)
    b = int(m.group(3) or 1) * (1 if m.group(2) == "+" else -1)
    c = int(m.group(5)) * (1 if m.group(4) == "+" else -1)
    return var, b, c


def parse_answer(ans, var):
    """'(x - 4)(x + 2)' -> (-4, 2)."""
    pairs = re.findall(rf"\({var} ([+-]) (\d+)\)", ans)
    assert len(pairs) == 2, ans
    return tuple(int(n) * (1 if s == "+" else -1) for s, n in pairs)


class TestFactorTrinomialGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FactorTrinomialGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertEqual(result["operation"], "factor_trinomial")
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_roots_from_problem_text(self):
        """A9 oracle: the answer's roots must satisfy sum=b, product=c,
        and be ordered ascending (A0)."""
        for _ in range(400):
            result = self.gen.generate()
            var, b, c = parse_problem(result["problem"])
            p, q = parse_answer(result["final_answer"], var)
            self.assertEqual(p + q, b, result["problem"])
            self.assertEqual(p * q, c, result["problem"])
            self.assertLess(p, q, "factors not in ascending order")

    def test_trial_and_error_semantics(self):
        """TRY arithmetic true; REJECT iff sum wrong; ACCEPT is the winner
        and every TRY is resolved by exactly one REJECT or ACCEPT."""
        for _ in range(400):
            result = self.gen.generate()
            var, b, c = parse_problem(result["problem"])
            seq = [s.split(DELIM) for s in result["steps"]
                   if s.split(DELIM)[0] in ("TRY", "REJECT", "ACCEPT")]
            self.assertEqual(seq[-1][0], "ACCEPT")
            pending = None
            accepts = 0
            for f in seq:
                if f[0] == "TRY":
                    self.assertIsNone(pending, "unresolved TRY")
                    m, n = (int(v) for v in f[1].strip("()").split(", "))
                    self.assertEqual(m * n, c, str(f))
                    work_sum = int(f[2].rsplit("=", 1)[1])
                    self.assertEqual(m + n, work_sum, str(f))
                    pending = (m, n, work_sum)
                elif f[0] == "REJECT":
                    self.assertIsNotNone(pending)
                    self.assertNotEqual(pending[2], b, str(f))
                    pending = None
                else:  # ACCEPT
                    self.assertIsNotNone(pending)
                    self.assertEqual(pending[2], b, str(f))
                    p, q = parse_answer(result["final_answer"], var)
                    self.assertEqual({pending[0], pending[1]}, {p, q})
                    pending = None
                    accepts += 1
            self.assertEqual(accepts, 1)

    def test_rejections_occur_and_vary(self):
        counts = set()
        for _ in range(300):
            result = self.gen.generate()
            counts.add(sum(1 for s in result["steps"]
                           if s.startswith(f"REJECT{DELIM}")))
        self.assertIn(0, counts, "winner-first cases should exist")
        self.assertTrue(any(c >= 2 for c in counts),
                        "multi-rejection cases should exist")

    def test_foil_check_matches_original(self):
        for _ in range(200):
            result = self.gen.generate()
            check = next(s for s in result["steps"]
                         if s.startswith(f"CHECK{DELIM}"))
            f = check.split(DELIM)
            var, b, c = parse_problem(result["problem"])
            # lhs middle terms must combine to bx
            mids = re.findall(rf"([+-]) (\d*){var}(?!\^)", f[2])
            total = sum(int(n or 1) * (1 if s == "+" else -1) for s, n in mids)
            self.assertEqual(total, b, check)
            self.assertEqual(f[3], result["problem"].split(": ", 1)[1], check)


def parse_general(problem):
    """'Factor: 6x^2 + 7x - 3' -> (var, a, b, c)."""
    expr = problem.split(": ", 1)[1]
    m = re.fullmatch(r"(\d*)([a-z])\^2 ([+-]) (\d*)\2 ([+-]) (\d+)", expr)
    assert m, expr
    a = int(m.group(1) or 1)
    var = m.group(2)
    b = int(m.group(4) or 1) * (1 if m.group(3) == "+" else -1)
    c = int(m.group(6)) * (1 if m.group(5) == "+" else -1)
    return var, a, b, c


def parse_binomials(ans, var):
    """'(3x - 1)(2x + 3)' -> [(3, -1), (2, 3)]."""
    pairs = re.findall(rf"\((\d*){var} ([+-]) (\d+)\)", ans)
    assert len(pairs) == 2, ans
    return [(int(p or 1), int(n) * (1 if s == "+" else -1))
            for p, s, n in pairs]


class TestFactorTrinomialGeneral(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = FactorTrinomialGenerator("general")

    def test_oracle_expansion_and_primitivity(self):
        """A9 oracle: the answer's binomials must expand to the trinomial,
        the trinomial must be primitive, a != 1, ordering per A0."""
        from math import gcd
        for _ in range(400):
            result = self.gen.generate()
            var, a, b, c = parse_general(result["problem"])
            self.assertGreater(a, 1)
            (q, s), (p, r) = parse_binomials(result["final_answer"], var)
            self.assertEqual(q * p, a, result["problem"])
            self.assertEqual(q * r + p * s, b, result["problem"])
            self.assertEqual(s * r, c, result["problem"])
            self.assertEqual(gcd(gcd(a, abs(b)), abs(c)), 1,
                             "trinomial not primitive")
            self.assertLessEqual(s, r, "factors not ordered by constant")
            self.assertEqual(result["difficulty"], 5)

    def test_ac_search_and_split_consistent(self):
        for _ in range(300):
            result = self.gen.generate()
            var, a, b, c = parse_general(result["problem"])
            ac = next(s for s in result["steps"]
                      if s.startswith(f"AC_PRODUCT{DELIM}"))
            self.assertEqual(int(ac.split(DELIM)[2]), a * c, ac)
            accept = next(s for s in result["steps"]
                          if s.startswith(f"ACCEPT{DELIM}"))
            m, n = (int(v) for v in
                    accept.split(DELIM)[1].strip("()").split(", "))
            self.assertEqual(m * n, a * c)
            self.assertEqual(m + n, b)

    def test_grouping_arithmetic(self):
        """Each FACTOR_GROUP's gcf × binomial must reproduce its group."""
        for _ in range(300):
            result = self.gen.generate()
            var, a, b, c = parse_general(result["problem"])
            common = None
            for s in result["steps"]:
                f = s.split(DELIM)
                if f[0] != "FACTOR_GROUP":
                    continue
                group, gcf_txt, bino = f[1], f[2], f[3]
                gm = re.fullmatch(rf"(-?\d*)({var})?", gcf_txt)
                self.assertIsNotNone(gm, s)
                coef_txt = gm.group(1)
                gcf_coef = {"": 1, "-": -1}.get(coef_txt, None)
                if gcf_coef is None:
                    gcf_coef = int(coef_txt)
                gcf_pow = 1 if gm.group(2) else 0
                bm = re.fullmatch(rf"\((\d*){var} ([+-]) (\d+)\)", bino)
                self.assertIsNotNone(bm, s)
                bq = int(bm.group(1) or 1)
                bconst = int(bm.group(3)) * (1 if bm.group(2) == "+" else -1)
                # expand gcf × (bq·x + bconst) and compare to the group
                terms = {1 + gcf_pow: gcf_coef * bq,
                         gcf_pow: gcf_coef * bconst}
                got = {}
                for part in group.replace(" - ", " + -").split(" + "):
                    mm = re.fullmatch(
                        rf"(-?\d*)(?:{var}(?:\^(\d+))?)?", part.strip())
                    coef = {"": 1, "-": -1}.get(mm.group(1), None)
                    if coef is None:
                        coef = int(mm.group(1))
                    power = 0
                    if var in part:
                        power = int(mm.group(2)) if mm.group(2) else 1
                    got[power] = got.get(power, 0) + coef
                self.assertEqual(terms, got, s)
                if common is None:
                    common = bino
                else:
                    self.assertEqual(common, bino,
                                     "groups share no common binomial")

    def test_general_mode_operation(self):
        seen = {self.gen.generate()["operation"] for _ in range(20)}
        self.assertEqual(seen, {"factor_trinomial_general"})
        with self.assertRaises(ValueError):
            FactorTrinomialGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
