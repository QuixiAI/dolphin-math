import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class RVTransformGenerator(ProblemGenerator):
    """
    Transform random variables with CDF and Jacobian methods.

    Variants:
    - cdf_square: Y=X^2 for X uniform on [0,a]
    - jacobian_sum_difference: U=X+Y, V=X-Y for a uniform square

    Op-codes used:
    - TRANSFORM_SETUP: method, original variables, and transformation
    - DENSITY: original density statement
    - SUPPORT: transformed support
    - CDF_EVENT / CDF_FORMULA / PDF_FORMULA: CDF-method derivation
    - INVERSE_MAP / JAC_MATRIX: inverse transformation and Jacobian matrix
    - CHECK: support verification at a sample point
    - A / S / M / D / E / ROOT / ABS (established/shared): exact arithmetic
    - Z: transformed formula, support, density, and requested evaluation
    """

    VARIANTS = ["cdf_square", "jacobian_sum_difference"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "cdf_square":
            problem, steps, answer = self._generate_cdf_square()
        else:
            problem, steps, answer = self._generate_jacobian()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"rv_transform_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_cdf_square(self):
        a = random.randint(2, 30)
        s = random.randint(1, a)
        a_sq = a ** 2
        density = Fraction(1, a)
        y0 = s ** 2
        cdf_value = Fraction(s, a)
        cdf_formula = f"sqrt(y)/{a}"
        pdf_formula = f"1/({2 * a}*sqrt(y))"
        steps = [
            step("TRANSFORM_SETUP", "cdf", f"X~Uniform(0,{a})", "Y=X^2"),
            step("DENSITY", "f_X(x)", f"1/{a}"),
            step("D", 1, a, fraction_text(density)),
            step("E", a, 2, a_sq),
            step("SUPPORT", f"0<=x<={a}", f"0<=y<={a_sq}"),
            step("CDF_EVENT", "Y<=y", "X^2<=y", "X<=sqrt(y)"),
            step("CDF_FORMULA", f"F_Y(y)={cdf_formula}",
                 f"0<=y<={a_sq}"),
            step("PDF_FORMULA", f"f_Y(y)={pdf_formula}"),
            step("E", s, 2, y0),
            step("ROOT", y0, s),
            step("D", s, a, fraction_text(cdf_value)),
        ]
        answer = (
            f"support=0<=y<={a_sq}; F_Y(y)={cdf_formula}; "
            f"f_Y(y)={pdf_formula}; F_Y({y0})={fraction_text(cdf_value)}"
        )
        problem = (
            f"Let X~Uniform(0,{a}) and Y=X^2. Use the CDF method to find "
            f"F_Y(y), f_Y(y), and F_Y({y0})."
        )
        return problem, steps, answer

    def _generate_jacobian(self):
        a = random.randint(2, 25)
        x_value = random.randint(0, a)
        y_value = random.randint(0, a)
        a_sq = a ** 2
        original_density = Fraction(1, a_sq)
        half = Fraction(1, 2)
        det_left = half * -half
        det_right = half * half
        det = det_left - det_right
        abs_det = abs(det)
        transformed_density = original_density * abs_det
        two_a = 2 * a
        u_value = x_value + y_value
        v_value = x_value - y_value
        u_plus_v = u_value + v_value
        u_minus_v = u_value - v_value
        steps = [
            step("TRANSFORM_SETUP", "jacobian",
                 f"X,Y~Uniform(0,{a})", "U=X+Y,V=X-Y"),
            step("DENSITY", "f_XY(x,y)", f"1/{a}^2"),
            step("E", a, 2, a_sq),
            step("D", 1, a_sq, fraction_text(original_density)),
            step("INVERSE_MAP", "x=(u+v)/2", "y=(u-v)/2"),
            step("D", 1, 2, fraction_text(half)),
            step("JAC_MATRIX", "dx/du=1/2, dx/dv=1/2",
                 "dy/du=1/2, dy/dv=-1/2"),
            step("M", fraction_text(half), fraction_text(-half),
                 fraction_text(det_left)),
            step("M", fraction_text(half), fraction_text(half),
                 fraction_text(det_right)),
            step("S", fraction_text(det_left), fraction_text(det_right),
                 fraction_text(det)),
            step("ABS", fraction_text(det), fraction_text(abs_det)),
            step("M", fraction_text(original_density), fraction_text(abs_det),
                 fraction_text(transformed_density)),
            step("M", 2, a, two_a),
            step("SUPPORT", f"0<=u+v<={two_a}",
                 f"0<=u-v<={two_a}"),
            step("A", x_value, y_value, u_value),
            step("S", x_value, y_value, v_value),
            step("A", u_value, v_value, u_plus_v),
            step("S", u_value, v_value, u_minus_v),
            step("CHECK", f"u+v={u_plus_v}", f"u-v={u_minus_v}",
                 "in support"),
        ]
        answer = (
            "inverse x=(u+v)/2, y=(u-v)/2; "
            f"support=0<=u+v<={two_a} and 0<=u-v<={two_a}; "
            f"absJ={fraction_text(abs_det)}; "
            f"f_UV(u,v)={fraction_text(transformed_density)}; "
            f"f_UV({u_value},{v_value})={fraction_text(transformed_density)}"
        )
        problem = (
            f"Let X,Y be independent Uniform(0,{a}). Define U=X+Y and "
            f"V=X-Y. Use the Jacobian method to find the inverse map, "
            f"transformed support, density f_UV(u,v), and f_UV at the "
            f"point produced by x={x_value}, y={y_value}."
        )
        return problem, steps, answer
