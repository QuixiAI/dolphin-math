import os
import random
import re
import sys
import unittest
from fractions import Fraction

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.series_convergence_generator import (
    SeriesConvergenceGenerator,
)
from helpers import DELIM

_cache = {}


def p_val(txt):
    """The exponent p in 1/n^p renders."""
    if txt == "1/n":
        return Fraction(1)
    if txt == "1/√n":
        return Fraction(1, 2)
    m = re.fullmatch(r"1/n\^(\d+)", txt)
    if m:
        return Fraction(int(m.group(1)))
    m = re.fullmatch(r"1/n\^\((\d+)/(\d+)\)", txt)
    return Fraction(int(m.group(1)), int(m.group(2)))


def tail_sum(term, lo=2001, hi=4000):
    return sum(term(n) for n in range(lo, hi + 1))


def p_tail_converges(p):
    """Numeric verdict for sum of 1/n^p via the tail increment."""
    delta = tail_sum(lambda n: n ** -float(p))
    assert delta < 0.05 or delta > 0.3, delta
    return delta < 0.05


def oracle_check(example):
    body_q = example["problem"]
    ans = example["final_answer"]
    key = (body_q, ans)
    if key in _cache:
        return _cache[key]
    ok = _oracle(body_q, ans)
    _cache[key] = ok
    return ok


def _oracle(q, ans):
    m = re.fullmatch(r"Determine whether Σ \((\d*)n( \+ \d+)?\)/"
                     r"\((\d*)n \+ (\d+)\) for n ≥ 1 converges or "
                     r"diverges\.", q)
    if m:
        a, c = int(m.group(1) or 1), int(m.group(3) or 1)
        return ans == "diverges" and a / c > 1e-9
    m = re.fullmatch(r"Determine whether Σ (-?\d+)·\(?(-?\d+(?:/\d+)?)"
                     r"\)?\^n for n ≥ 0 converges or diverges; if it "
                     r"converges, find the sum\.", q)
    if m:
        a, r = int(m.group(1)), Fraction(m.group(2))
        if abs(r) >= 1:
            return ans == "diverges"
        total = sum(a * float(r) ** n for n in range(400))
        mm = re.fullmatch(r"converges to (-?\d+(?:/\d+)?)", ans)
        return mm and abs(total - float(Fraction(mm.group(1)))) < 1e-9
    m = re.fullmatch(r"Determine whether Σ (\d+)\^n/n! for n ≥ 1 "
                     r"converges or diverges\.", q)
    if m:
        c, term, tail = int(m.group(1)), 1.0, 0.0
        for n in range(1, 400):
            term = term * c / n
            if n > 100:
                tail += term
        return ans == "converges" and tail < 1e-6
    m = re.fullmatch(r"Determine whether Σ n!/(\d+)\^n for n ≥ 1 "
                     r"converges or diverges\.", q)
    if m:
        c, term = int(m.group(1)), 1.0
        for n in range(1, 400):
            term = term * n / c
        return ans == "diverges" and term > 1e6
    m = re.fullmatch(r"Determine whether Σ \(-1\)\^\(n\+1\)·(.+) for "
                     r"n ≥ 1 converges absolutely, converges "
                     r"conditionally, or diverges\.", q)
    if m:
        p = p_val(m.group(1))
        want = ("converges absolutely" if p_tail_converges(p)
                else "converges conditionally")
        return ans == want
    m = re.fullmatch(r"Determine whether Σ 1/\(n\^2 \+ (\d+)\) for "
                     r"n ≥ 1 converges or diverges\.", q)
    if m:
        k = int(m.group(1))
        return (ans == "converges" and
                tail_sum(lambda n: 1 / (n * n + k)) < 0.05)
    m = re.fullmatch(r"Determine whether Σ n/\(n\^2 \+ (\d+)\) for "
                     r"n ≥ 1 converges or diverges\.", q)
    if m:
        k = int(m.group(1))
        return (ans == "diverges" and
                tail_sum(lambda n: n / (n * n + k)) > 0.3)
    m = re.fullmatch(r"Determine whether Σ (.+) for n ≥ 1 converges "
                     r"or diverges\.", q)
    assert m, q
    p = p_val(m.group(1))
    want = "converges" if p_tail_converges(p) else "diverges"
    return ans == want


class TestSeriesConvergenceGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = SeriesConvergenceGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps", "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_numeric_partial_sums(self):
        """A9 oracle: partial-sum behavior confirms every verdict."""
        for _ in range(400):
            result = self.gen.generate()
            self.assertTrue(oracle_check(result),
                            (result["problem"], result["final_answer"]))

    def test_choice_step_always_present(self):
        for _ in range(200):
            result = self.gen.generate()
            self.assertTrue(any(s.startswith(f"TEST_CHOOSE{DELIM}")
                                for s in result["steps"]))
            self.assertTrue(any(s.startswith(f"SERIES_SETUP{DELIM}")
                                for s in result["steps"]))

    def test_no_degenerate_renders(self):
        for _ in range(300):
            result = self.gen.generate()
            joined = " ".join(result["steps"])
            for bad in (r"(?<!\d)1n", "--", r"\+ -"):
                self.assertIsNone(re.search(bad, joined),
                                  (bad, result["steps"]))

    def test_all_verdict_kinds_occur(self):
        answers = set()
        for _ in range(300):
            answers.add(self.gen.generate()["final_answer"]
                        .split(" to ")[0])
        self.assertEqual(answers, {"diverges", "converges",
                                   "converges absolutely",
                                   "converges conditionally"})

    def test_all_variants_reachable(self):
        ops = set()
        for _ in range(300):
            ops.add(self.gen.generate()["operation"])
        self.assertEqual(len(ops), 6)

    def test_fixed_variant_constructor(self):
        with self.assertRaises(ValueError):
            SeriesConvergenceGenerator("bogus")


if __name__ == "__main__":
    unittest.main()
