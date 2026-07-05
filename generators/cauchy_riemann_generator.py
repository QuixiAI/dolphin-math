import random

from base_generator import ProblemGenerator
from helpers import step, jid


def expr_text(terms):
    parts = []
    for coef, var in terms:
        if coef == 0:
            continue
        abs_coef = abs(coef)
        if var:
            body = var if abs_coef == 1 else f"{abs_coef}{var}"
        else:
            body = str(abs_coef)
        if not parts:
            parts.append(body if coef > 0 else f"-{body}")
        else:
            parts.append(f"+ {body}" if coef > 0 else f"- {body}")
    return " ".join(parts) if parts else "0"


def u_text(a, b, c):
    return expr_text([(a, "x^2"), (-a, "y^2"), (b, "x"), (-c, "y")])


def v_text(a, b, c, delta=0):
    return expr_text([(2 * a, "xy"), (c, "x"), (b + delta, "y")])


def ux_text(a, b):
    return expr_text([(2 * a, "x"), (b, "")])


def uy_text(a, c):
    return expr_text([(-2 * a, "y"), (-c, "")])


def vx_text(a, c):
    return expr_text([(2 * a, "y"), (c, "")])


def vy_text(a, b, delta=0):
    return expr_text([(2 * a, "x"), (b + delta, "")])


class CauchyRiemannGenerator(ProblemGenerator):
    """
    Cauchy-Riemann verification and harmonic conjugates for polynomial
    real/imaginary parts.

    Variants:
    - verify: check u_x=v_y and u_y=-v_x
    - harmonic_conjugate: integrate u_x to find v

    Op-codes used:
    - CR_SETUP / HARMONIC_SETUP: problem setup
    - PARTIAL / INTEGRATE: derivative and integration steps
    - CHECK: Cauchy-Riemann comparisons
    - Z: verdict or harmonic conjugate
    """

    VARIANTS = ["verify", "harmonic_conjugate"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        a = random.choice([v for v in range(-4, 5) if v != 0])
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        if variant == "verify":
            problem, steps, answer = self._generate_verify(a, b, c)
        else:
            problem, steps, answer = self._generate_harmonic(a, b, c)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"cauchy_riemann_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_verify(self, a, b, c):
        delta = random.choice([0, 0, 1, -1])
        u = u_text(a, b, c)
        v = v_text(a, b, c, delta)
        first_ok = delta == 0
        second_ok = True
        verdict = "yes" if first_ok and second_ok else "no"
        steps = [
            step("CR_SETUP", f"u={u}", f"v={v}"),
            step("PARTIAL", "u_x", ux_text(a, b)),
            step("PARTIAL", "u_y", uy_text(a, c)),
            step("PARTIAL", "v_x", vx_text(a, c)),
            step("PARTIAL", "v_y", vy_text(a, b, delta)),
            step("CHECK", "u_x = v_y", "yes" if first_ok else "no"),
            step("CHECK", "u_y = -v_x", "yes" if second_ok else "no"),
        ]
        # composite verdict: name both equation checks so the bare yes/no
        # label is not a gradable coin flip
        answer = (f"Cauchy-Riemann = {verdict} "
                  f"(u_x = v_y: {'yes' if first_ok else 'no'}; "
                  f"u_y = -v_x: {'yes' if second_ok else 'no'})")
        problem = (
            f"For a={a}, b={b}, c={c}, let "
            "u=a(x^2-y^2)+b*x-c*y and "
            f"v=2a*x*y+c*x+(b{delta:+d})*y. "
            "Verify the Cauchy-Riemann equations."
        )
        return problem, steps, answer

    def _generate_harmonic(self, a, b, c):
        u = u_text(a, b, c)
        v = v_text(a, b, c)
        steps = [
            step("HARMONIC_SETUP", f"u={u}"),
            step("PARTIAL", "u_x", ux_text(a, b)),
            step("PARTIAL", "u_y", uy_text(a, c)),
            step("INTEGRATE", "v_y = u_x", f"v={v} + phi(x)"),
            step("PARTIAL", "v_x", vx_text(a, c)),
            step("CHECK", "v_x = -u_y", "yes"),
        ]
        answer = f"v = {v}"
        problem = (
            f"For a={a}, b={b}, c={c}, let "
            "u=a(x^2-y^2)+b*x-c*y. Find a harmonic conjugate v with "
            "constant 0."
        )
        return problem, steps, answer
