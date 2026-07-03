import random
from base_generator import ProblemGenerator
from helpers import step, jid


class SigmaNotationGenerator(ProblemGenerator):
    """
    Expands sigma notation term by term and evaluates the sum for small
    upper bounds. Lower bounds other than 1 (including 0) appear so the
    index range itself is exercised.

    Variants:
    - linear: Σ (ak + b) — each term substituted and evaluated
    - square: Σ k^2
    - power:  Σ b^k, lower bound often 0 (b^0 = 1 is the trap)

    Op-codes used:
    - SIGMA_SETUP: the notation and the goal (notation, goal)
    - SIGMA_TERM: one expanded term (index, substituted expression, value)
    - SIGMA_EXPAND: the fully expanded sum in one line
    - A: the running total, added pairwise left to right (established)
    - Z: final answer
    """

    VARIANTS = ["linear", "square", "power"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "linear":
            a = random.randint(1, 5)
            b = random.randint(-4, 9)
            lo = random.choice([1, 1, 1, 0, 2, 3])
            count = random.randint(4, 6)
            head = "k" if a == 1 else f"{a}k"
            if b == 0:
                expr = head
            else:
                expr = f"{head} + {b}" if b > 0 else f"{head} - {-b}"
            shown = f"({expr})" if b != 0 else expr

            def term_expr(k):
                sk = f"({k})"
                base = sk if a == 1 else f"{a}{sk}"
                if b == 0:
                    return base
                return f"{base} + {b}" if b > 0 else f"{base} - {-b}"

            def term_val(k):
                return a * k + b
        elif variant == "square":
            a = random.choice([1, 1, 2, 3])
            lo = random.choice([0, 1, 2, 3, 4])
            count = random.randint(4, 6)
            shown = "k^2" if a == 1 else f"{a}k^2"

            def term_expr(k):
                return f"({k})^2" if a == 1 else f"{a}({k})^2"

            def term_val(k):
                return a * k * k
        else:
            base = random.choice([2, 2, 3, 3, 4, 5])
            c = random.choice([1, 1, 1, 2, 3])
            lo = random.choice([0, 0, 1])
            count = random.randint(4, 5) if base <= 3 else 4
            shown = f"{base}^k" if c == 1 else f"{c}·{base}^k"

            def term_expr(k):
                head = f"{base}^{k}"
                return head if c == 1 else f"{c}·{head}"

            def term_val(k):
                return c * base ** k

        hi = lo + count - 1
        ks = list(range(lo, hi + 1))
        vals = [term_val(k) for k in ks]
        notation = f"Σ_(k={lo})^({hi}) {shown}"

        steps = [step("SIGMA_SETUP", notation, "expand and evaluate")]
        for k, v in zip(ks, vals):
            steps.append(step("SIGMA_TERM", f"k={k}", term_expr(k), v))
        steps.append(step("SIGMA_EXPAND", " + ".join(
            f"({v})" if v < 0 else str(v) for v in vals)))
        running = vals[0]
        for v in vals[1:]:
            steps.append(step("A", running, v, running + v))
            running += v
        steps.append(step("Z", running))

        return dict(
            problem_id=jid(),
            operation=f"sigma_notation_{variant}",
            problem=f"Expand and evaluate: {notation}.",
            steps=steps,
            final_answer=str(running),
        )
