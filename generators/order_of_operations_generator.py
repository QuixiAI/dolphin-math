import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def dstr(fr):
    """Renders a Fraction whose denominator divides 100 as an exact decimal."""
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    scaled = fr * 100
    assert scaled.denominator == 1, f"not a 2-decimal value: {fr}"
    text = f"{fr.numerator / fr.denominator:.2f}"
    return text.rstrip("0").rstrip(".") if "." in text else text


def mixed_str(fr):
    """Renders a Fraction as a mixed number: '8 1/2', '3/4', or '8'."""
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    whole, rem = divmod(fr.numerator, fr.denominator)
    if whole == 0:
        return f"{fr.numerator}/{fr.denominator}"
    return f"{whole} {rem}/{fr.denominator}"


class OrderOfOperationsGenerator(ProblemGenerator):
    """Evaluates PEMDAS expressions with human-like steps.

    Modes (per-instance, see ALL_GENERATORS):
    - "integers" (default): whole-number expressions, division always exact
    - "decimals": tenths-decimals mixed with integers (edge cases)
    - "mixed_numbers": mixed numbers sharing a denominator, times integers

    The two edge-case modes emit their own difficulty (4) per example,
    overriding the class's static curriculum tier (3) — the A3 mechanism.
    """

    MODES = ["integers", "decimals", "mixed_numbers"]

    def __init__(self, mode="integers"):
        if mode not in self.MODES:
            raise ValueError(f"mode must be one of {self.MODES}")
        self.mode = mode
        self.op_symbol = mode  # shown in --sample and stats labels

    def generate(self) -> dict:
        if self.mode == "decimals":
            return self._generate_decimals()
        if self.mode == "mixed_numbers":
            return self._generate_mixed_numbers()
        return self._generate_integers()

    # ------------------------------------------------------------------
    # integers (original behavior; division guards fixed so every D step
    # is exact — the old guards could silently floor-divide)
    # ------------------------------------------------------------------

    def _generate_integers(self) -> dict:
        forms = [
            "a + b * c",
            "a - b * c",
            "(a + b) * c",
            "(a - b) * c",
            "a * (b + c)",
            "a * (b - c)",
            "a + b / c",
            "a - b / c",
            "a + b * c - d",
            "a - b + c * d",
            "(a + b + c) * d",
            "a * (b + c) - d",
            "(a + b) / c + d",
            "a + b / (c + d)",
        ]
        form = random.choice(forms)
        a, b, c, d = [random.randint(1, 12) for _ in range(4)]

        # Exact-division guards (constructive, never best-effort).
        if form in ("a + b / c", "a - b / c"):
            c = random.randint(2, 12)
            b = c * random.randint(1, 6)
        if form == "(a + b) / c + d":
            while not [x for x in range(2, 12) if (a + b) % x == 0]:
                a, b = random.randint(1, 12), random.randint(1, 12)
            c = random.choice([x for x in range(2, 12) if (a + b) % x == 0])
        if form == "a + b / (c + d)":
            b = (c + d) * random.randint(1, 6)

        expr = (form.replace("a", str(a)).replace("b", str(b))
                    .replace("c", str(c)).replace("d", str(d)))
        steps = []

        def add_op(op, x, y):
            if op == "A":
                result = x + y
                steps.append(step("A", x, y, result))
            elif op == "S":
                result = x - y
                steps.append(step("S", x, y, result))
            elif op == "M":
                result = x * y
                steps.append(step("M", x, y, result))
            else:  # D
                assert x % y == 0, f"non-exact division {x}/{y}"
                result = x // y
                steps.append(step("D", x, y, result))
            return result

        total = None
        if form == "a + b * c":
            mult = add_op("M", b, c)
            steps.append(step("REWRITE", f"{a} + {mult}"))
            total = add_op("A", a, mult)
        elif form == "a - b * c":
            mult = add_op("M", b, c)
            steps.append(step("REWRITE", f"{a} - {mult}"))
            total = add_op("S", a, mult)
        elif form == "a + b / c":
            div = add_op("D", b, c)
            steps.append(step("REWRITE", f"{a} + {div}"))
            total = add_op("A", a, div)
        elif form == "a - b / c":
            div = add_op("D", b, c)
            steps.append(step("REWRITE", f"{a} - {div}"))
            total = add_op("S", a, div)
        elif form == "(a + b) * c":
            inner = add_op("A", a, b)
            steps.append(step("REWRITE", f"{inner} * {c}"))
            total = add_op("M", inner, c)
        elif form == "(a - b) * c":
            inner = add_op("S", a, b)
            steps.append(step("REWRITE", f"{inner} * {c}"))
            total = add_op("M", inner, c)
        elif form == "a * (b + c)":
            inner = add_op("A", b, c)
            steps.append(step("REWRITE", f"{a} * {inner}"))
            total = add_op("M", a, inner)
        elif form == "a * (b - c)":
            inner = add_op("S", b, c)
            steps.append(step("REWRITE", f"{a} * {inner}"))
            total = add_op("M", a, inner)
        elif form == "a + b * c - d":
            mult = add_op("M", b, c)
            steps.append(step("REWRITE", f"{a} + {mult} - {d}"))
            mid = add_op("A", a, mult)
            steps.append(step("REWRITE", f"{mid} - {d}"))
            total = add_op("S", mid, d)
        elif form == "a - b + c * d":
            mult = add_op("M", c, d)
            steps.append(step("REWRITE", f"{a} - {b} + {mult}"))
            mid = add_op("S", a, b)
            steps.append(step("REWRITE", f"{mid} + {mult}"))
            total = add_op("A", mid, mult)
        elif form == "(a + b + c) * d":
            inner1 = add_op("A", a, b)
            steps.append(step("REWRITE", f"{inner1} + {c}"))
            inner2 = add_op("A", inner1, c)
            steps.append(step("REWRITE", f"{inner2} * {d}"))
            total = add_op("M", inner2, d)
        elif form == "a * (b + c) - d":
            inner = add_op("A", b, c)
            steps.append(step("REWRITE", f"{a} * {inner} - {d}"))
            prod = add_op("M", a, inner)
            steps.append(step("REWRITE", f"{prod} - {d}"))
            total = add_op("S", prod, d)
        elif form == "(a + b) / c + d":
            inner = add_op("A", a, b)
            steps.append(step("REWRITE", f"{inner} / {c} + {d}"))
            div = add_op("D", inner, c)
            steps.append(step("REWRITE", f"{div} + {d}"))
            total = add_op("A", div, d)
        elif form == "a + b / (c + d)":
            inner = add_op("A", c, d)
            steps.append(step("REWRITE", f"{a} + {b} / {inner}"))
            div = add_op("D", b, inner)
            steps.append(step("REWRITE", f"{a} + {div}"))
            total = add_op("A", a, div)

        if total is None:
            raise ValueError(f"Unhandled form: {form}")

        final_answer = str(total)
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="order_of_operations",
            problem=f"Compute {expr}",
            steps=steps,
            final_answer=final_answer,
            difficulty=3,
        )

    # ------------------------------------------------------------------
    # decimals: tenths mixed with integers, division-free forms
    # ------------------------------------------------------------------

    def _generate_decimals(self) -> dict:
        def tenth():
            k = random.choice([k for k in range(2, 100) if k % 10 != 0])
            return Fraction(k, 10)

        def integer():
            return Fraction(random.randint(2, 12))

        while True:
            form = random.choice(["a + b * c", "a - b * c", "(a + b) * c",
                                  "(a - b) * c", "a * (b + c)",
                                  "a + b * c - d"])
            # The multiplication always involves at least one decimal.
            a = tenth() if random.random() < 0.7 else integer()
            d = tenth() if random.random() < 0.5 else integer()
            if random.random() < 0.5:
                b, c = tenth(), integer()
            else:
                b, c = integer(), tenth()
            vals = {"a": a, "b": b, "c": c, "d": d}
            expr = form
            for name in "abcd":
                expr = expr.replace(name, dstr(vals[name]))

            steps = []

            def add_op(op, x, y):
                if op == "A":
                    result = x + y
                    steps.append(step("A", dstr(x), dstr(y), dstr(result)))
                elif op == "S":
                    result = x - y
                    steps.append(step("S", dstr(x), dstr(y), dstr(result)))
                else:
                    result = x * y
                    steps.append(step("M", dstr(x), dstr(y), dstr(result)))
                return result

            if form == "a + b * c":
                mult = add_op("M", b, c)
                steps.append(step("REWRITE", f"{dstr(a)} + {dstr(mult)}"))
                total = add_op("A", a, mult)
            elif form == "a - b * c":
                if a - b * c < 0:
                    continue
                mult = add_op("M", b, c)
                steps.append(step("REWRITE", f"{dstr(a)} - {dstr(mult)}"))
                total = add_op("S", a, mult)
            elif form == "(a + b) * c":
                inner = add_op("A", a, b)
                steps.append(step("REWRITE", f"{dstr(inner)} * {dstr(c)}"))
                total = add_op("M", inner, c)
            elif form == "(a - b) * c":
                if a - b < 0:
                    continue
                inner = add_op("S", a, b)
                steps.append(step("REWRITE", f"{dstr(inner)} * {dstr(c)}"))
                total = add_op("M", inner, c)
            elif form == "a * (b + c)":
                inner = add_op("A", b, c)
                steps.append(step("REWRITE", f"{dstr(a)} * {dstr(inner)}"))
                total = add_op("M", a, inner)
            else:  # a + b * c - d
                mult = add_op("M", b, c)
                steps.append(step("REWRITE",
                                  f"{dstr(a)} + {dstr(mult)} - {dstr(d)}"))
                mid = add_op("A", a, mult)
                if mid - d < 0:
                    continue
                steps.append(step("REWRITE", f"{dstr(mid)} - {dstr(d)}"))
                total = add_op("S", mid, d)
            break

        final_answer = dstr(total)
        steps.append(step("Z", final_answer))
        return dict(
            problem_id=jid(),
            operation="order_of_operations_decimals",
            problem=f"Compute {expr}",
            steps=steps,
            final_answer=final_answer,
            difficulty=4,
        )

    # ------------------------------------------------------------------
    # mixed numbers: two mixed numbers sharing a denominator, one integer
    # ------------------------------------------------------------------

    def _generate_mixed_numbers(self) -> dict:
        # Everything re-drawn per attempt: some (den, c, form) combinations
        # are infeasible for "a - b*c" (min b*c can exceed max a).
        while True:
            den = random.choice([2, 3, 4, 5, 8])
            c = random.randint(2, 5)
            form = random.choice(["a + b * c", "a - b * c",
                                  "(a + b) * c", "(a - b) * c"])

            def mixed():
                # num coprime to den so Fraction cannot reduce it — the
                # arithmetic below relies on every value keeping denominator
                # `den` (a reduced Fraction silently broke that once).
                from math import gcd
                whole = random.randint(1, 6)
                num = random.choice([n for n in range(1, den)
                                     if gcd(n, den) == 1])
                return Fraction(whole * den + num, den)

            a, b = mixed(), mixed()
            if form == "a - b * c" and a - b * c < 0:
                continue
            if form == "(a - b) * c" and a - b <= 0:
                continue
            break

        a_txt, b_txt = mixed_str(a), mixed_str(b)
        fa, fb = f"{a.numerator}/{a.denominator}", f"{b.numerator}/{b.denominator}"
        expr = (form.replace("a", a_txt).replace("b", b_txt)
                    .replace("c", str(c)))
        steps = []

        def frac_txt(fr):
            return f"{fr.numerator}/{fr.denominator}"

        def finish(num, den_):
            reduced = Fraction(num, den_)
            if (reduced.numerator, reduced.denominator) != (num, den_):
                steps.append(step("F", f"{num}/{den_}",
                                  frac_txt(reduced) if reduced.denominator > 1
                                  else str(reduced.numerator)))
            answer = mixed_str(reduced)
            if reduced.denominator > 1 and reduced.numerator > reduced.denominator:
                steps.append(step("IMPROPER_TO_MIX", frac_txt(reduced), answer))
            steps.append(step("Z", answer))
            return answer

        if form in ("a + b * c", "a - b * c"):
            steps.append(step("MIX_IMPROPER", b_txt, fb))
            prod_num = b.numerator * c
            steps.append(step("M", fb, c, f"{prod_num}/{den}"))
            sign = "+" if form == "a + b * c" else "-"
            steps.append(step("REWRITE", f"{a_txt} {sign} {prod_num}/{den}"))
            steps.append(step("MIX_IMPROPER", a_txt, fa))
            res_num = (a.numerator + prod_num if sign == "+"
                       else a.numerator - prod_num)
            steps.append(step("A" if sign == "+" else "S",
                              fa, f"{prod_num}/{den}", f"{res_num}/{den}"))
            answer = finish(res_num, den)
        else:
            steps.append(step("MIX_IMPROPER", a_txt, fa))
            steps.append(step("MIX_IMPROPER", b_txt, fb))
            sign = "+" if form == "(a + b) * c" else "-"
            inner_num = (a.numerator + b.numerator if sign == "+"
                         else a.numerator - b.numerator)
            steps.append(step("A" if sign == "+" else "S",
                              fa, fb, f"{inner_num}/{den}"))
            steps.append(step("REWRITE", f"{inner_num}/{den} * {c}"))
            prod_num = inner_num * c
            steps.append(step("M", f"{inner_num}/{den}", c, f"{prod_num}/{den}"))
            answer = finish(prod_num, den)

        return dict(
            problem_id=jid(),
            operation="order_of_operations_mixed_numbers",
            problem=f"Compute {expr}",
            steps=steps,
            final_answer=answer,
            difficulty=4,
        )
