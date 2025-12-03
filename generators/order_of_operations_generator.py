import random
from base_generator import ProblemGenerator
from helpers import step, jid


class OrderOfOperationsGenerator(ProblemGenerator):
    """Evaluates simple PEMDAS expressions with human-like steps."""

    def generate(self) -> dict:
        # Expression templates (2–4 operations, some with parentheses)
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

        # Avoid division issues by biasing divisibility
        if "b / c" in form and (b % c) != 0:
            c_choices = [x for x in range(2, 12) if b % x == 0]
            if c_choices:
                c = random.choice(c_choices)
        if "(c + d)" in form:
            # make b divisible by (c+d) if used as numerator
            s = c + d
            b = s * random.randint(1, 6)

        expr = form.replace("a", str(a)).replace("b", str(b)).replace("c", str(c)).replace("d", str(d))
        steps = []

        # Helper to append arithmetic step + rewrite
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
                result = x // y
                steps.append(step("D", x, y, result))
            return result

        # Evaluate with manual ordering
        if form in ["a + b * c", "a - b * c"]:
            mult = add_op("M", b, c)
            sign = "+" if "+" in form else "-"
            steps.append(step("REWRITE", f"{a} {sign} {mult}"))
            if sign == "+":
                total = add_op("A", a, mult)
            else:
                total = add_op("S", a, mult)
        elif form in ["a + b / c", "a - b / c"]:
            div = add_op("D", b, c)
            sign = "+" if "+" in form else "-"
            steps.append(step("REWRITE", f"{a} {sign} {div}"))
            if sign == "+":
                total = add_op("A", a, div)
            else:
                total = add_op("S", a, div)
        elif form in ["(a + b) * c", "(a - b) * c"]:
            inner = add_op("A" if "+" in form else "S", a, b)
            steps.append(step("REWRITE", f"{inner} * {c}"))
            total = add_op("M", inner, c)
        else:  # a * (b + c) or a * (b - c)
            inner = add_op("A" if "+" in form else "S", b, c)
            steps.append(step("REWRITE", f"{a} * {inner}"))
            total = add_op("M", a, inner)
        # Extended 3-4 op forms
        if form == "a + b * c - d":
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

        final_answer = str(total)
        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="order_of_operations",
            problem=f"Compute {expr}",
            steps=steps,
            final_answer=final_answer,
        )
