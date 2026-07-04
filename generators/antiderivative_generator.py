import random
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.derivative_power_rule_generator import poly_pow, term_pow


class AntiderivativeGenerator(ProblemGenerator):
    """
    Antiderivatives with the divide-by-new-exponent arithmetic shown
    per term, and + C always attached.

    Variants:
    - power: polynomial with every coefficient divisible by its new
             exponent, so all antiderivative coefficients are integers
    - trig:  c·sin(kx), c·cos(kx), c·sec²(kx) with k dividing c
    - exp:   c·e^(kx) with k dividing c, or c/x -> c·ln(abs(x))

    Op-codes used:
    - INTEG_SETUP: the integral (integral, goal)
    - INTEG_RULE: the rule used (name, formula)
    - D: coefficient over new exponent (established)
    - ANTIDERIV: one term integrated (term, antiderivative)
    - REWRITE / Z: assembled F(x) + C (established)
    """

    VARIANTS = ["power", "trig", "exp"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or \
            random.choice(["power", "power", "trig", "exp"])

        if variant == "power":
            degs = sorted(random.sample(range(0, 4),
                                        random.randint(2, 3)),
                          reverse=True)
            terms = []
            for n in degs:
                k = random.choice([v for v in range(-4, 5) if v != 0])
                terms.append((k * (n + 1), n))
            f_txt = poly_pow(terms)
            steps = [
                step("INTEG_SETUP", f"∫ ({f_txt}) dx",
                     "antiderivative"),
                step("INTEG_RULE", "power rule",
                     "∫ x^n dx = x^(n+1)/(n+1) + C"),
            ]
            anti = []
            for c, n in terms:
                newc = c // (n + 1)
                if n + 1 > 1:
                    steps.append(step("D", c, n + 1, newc))
                steps.append(step("ANTIDERIV", term_pow(c, n),
                                  term_pow(newc, n + 1)))
                anti.append((newc, n + 1))
            F = poly_pow(anti)
            answer = f"{F} + C"
            problem = f"Find ∫ ({f_txt}) dx."
        elif variant == "trig":
            k = random.choice([1, 2, 3, 4])
            c = k * random.choice([v for v in range(-5, 6) if v != 0])
            fn = random.choice(["sin", "cos", "sec^2"])
            arg = "x" if k == 1 else f"{k}x"
            newc = c // k
            body = f"{c} {fn}({arg})" if abs(c) != 1 else \
                (f"{fn}({arg})" if c == 1 else f"-{fn}({arg})")
            if fn == "sin":
                rule = "∫ sin(u) du = -cos(u) + C"
                out = -newc
                res = (f"{out} cos({arg})" if abs(out) != 1 else
                       (f"cos({arg})" if out == 1 else f"-cos({arg})"))
            elif fn == "cos":
                rule = "∫ cos(u) du = sin(u) + C"
                out = newc
                res = (f"{out} sin({arg})" if abs(out) != 1 else
                       (f"sin({arg})" if out == 1 else f"-sin({arg})"))
            else:
                rule = "∫ sec^2(u) du = tan(u) + C"
                out = newc
                res = (f"{out} tan({arg})" if abs(out) != 1 else
                       (f"tan({arg})" if out == 1 else f"-tan({arg})"))
            steps = [
                step("INTEG_SETUP", f"∫ {body} dx", "antiderivative"),
                step("INTEG_RULE", "trig rule", rule),
            ]
            if k > 1:
                steps.append(step("D", c, k, newc))
            steps.append(step("ANTIDERIV", body, res))
            answer = f"{res} + C"
            problem = f"Find ∫ {body} dx."
        else:
            if random.random() < 0.6:
                k = random.choice([2, 3, 4])
                c = k * random.choice([v for v in range(-5, 6)
                                       if v != 0])
                newc = c // k
                body = f"{c}e^({k}x)"
                res = (f"{newc}e^({k}x)" if abs(newc) != 1 else
                       (f"e^({k}x)" if newc == 1 else f"-e^({k}x)"))
                steps = [
                    step("INTEG_SETUP", f"∫ {body} dx",
                         "antiderivative"),
                    step("INTEG_RULE", "exponential rule",
                         "∫ e^(kx) dx = e^(kx)/k + C"),
                    step("D", c, k, newc),
                    step("ANTIDERIV", body, res),
                ]
            else:
                c = random.choice([v for v in range(-6, 7) if v != 0])
                body = f"{c}/x"
                res = (f"{c} ln(abs(x))" if abs(c) != 1 else
                       ("ln(abs(x))" if c == 1 else "-ln(abs(x))"))
                steps = [
                    step("INTEG_SETUP", f"∫ {body} dx",
                         "antiderivative"),
                    step("INTEG_RULE", "log rule",
                         "∫ (1/x) dx = ln(abs(x)) + C"),
                    step("ANTIDERIV", body, res),
                ]
            answer = f"{res} + C"
            problem = f"Find ∫ {body} dx."
        steps.append(step("REWRITE", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"antiderivative_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
