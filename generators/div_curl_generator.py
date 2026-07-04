import random

from base_generator import ProblemGenerator
from helpers import step, jid


def fmt_linear(raw_terms):
    pieces = []
    for coeff, body in raw_terms:
        if coeff == 0:
            continue
        if body:
            text = body if abs(coeff) == 1 else f"{abs(coeff)}*{body}"
        else:
            text = str(abs(coeff))
        if not pieces:
            pieces.append(text if coeff > 0 else f"-{text}")
        else:
            pieces.append(("+ " if coeff > 0 else "- ") + text)
    return " ".join(pieces) if pieces else "0"


def fmt_sum(values):
    pieces = []
    for value in values:
        if not pieces:
            pieces.append(str(value))
        else:
            pieces.append(("+ " if value >= 0 else "- ") + str(abs(value)))
    return " ".join(pieces)


def fmt_diff(a, b):
    return f"{a} + {abs(b)}" if b < 0 else f"{a} - {b}"


class DivCurlGenerator(ProblemGenerator):
    """
    Divergence and curl of linear vector fields.

    Variants:
    - plane: scalar divergence and scalar curl for F(x,y)=<P,Q>
    - space: divergence and vector curl for F(x,y,z)=<P,Q,R>

    Op-codes used:
    - VECTOR_SETUP: vector field and requested operation
    - PARTIAL_RESULT (established): component partial derivatives
    - DIV_SUM: add divergence terms
    - CURL_COMPONENT: signed curl component arithmetic
    - Z: combined divergence/curl answer
    """

    VARIANTS = ["plane", "space"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _coeffs(n):
        return [random.randint(-6, 6) for _ in range(n)]

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "plane":
            px, py, qx, qy = self._coeffs(4)
            p_txt = fmt_linear([(px, "x"), (py, "y")])
            q_txt = fmt_linear([(qx, "x"), (qy, "y")])
            div = px + qy
            curl = qx - py
            steps = [
                step("VECTOR_SETUP", f"F(x,y) = <{p_txt}, {q_txt}>",
                     "divergence and scalar curl"),
                step("PARTIAL_RESULT", "P_x", px),
                step("PARTIAL_RESULT", "Q_y", qy),
                step("DIV_SUM", "P_x + Q_y", fmt_sum([px, qy]), div),
                step("PARTIAL_RESULT", "Q_x", qx),
                step("PARTIAL_RESULT", "P_y", py),
                step("CURL_COMPONENT", "Q_x - P_y",
                     fmt_diff(qx, py), curl),
            ]
            answer = f"divergence {div}; curl {curl}"
            problem = (
                f"For F(x,y) = <{p_txt}, {q_txt}>, compute the "
                f"divergence and scalar curl."
            )
        else:
            px, py, pz, qx, qy, qz, rx, ry, rz = self._coeffs(9)
            p_txt = fmt_linear([(px, "x"), (py, "y"), (pz, "z")])
            q_txt = fmt_linear([(qx, "x"), (qy, "y"), (qz, "z")])
            r_txt = fmt_linear([(rx, "x"), (ry, "y"), (rz, "z")])
            div = px + qy + rz
            curl_i = ry - qz
            curl_j = pz - rx
            curl_k = qx - py
            steps = [
                step("VECTOR_SETUP",
                     f"F(x,y,z) = <{p_txt}, {q_txt}, {r_txt}>",
                     "divergence and curl"),
                step("PARTIAL_RESULT", "P_x", px),
                step("PARTIAL_RESULT", "Q_y", qy),
                step("PARTIAL_RESULT", "R_z", rz),
                step("DIV_SUM", "P_x + Q_y + R_z",
                     fmt_sum([px, qy, rz]), div),
                step("PARTIAL_RESULT", "R_y", ry),
                step("PARTIAL_RESULT", "Q_z", qz),
                step("CURL_COMPONENT", "i", fmt_diff(ry, qz), curl_i),
                step("PARTIAL_RESULT", "P_z", pz),
                step("PARTIAL_RESULT", "R_x", rx),
                step("CURL_COMPONENT", "j", fmt_diff(pz, rx), curl_j),
                step("PARTIAL_RESULT", "Q_x", qx),
                step("PARTIAL_RESULT", "P_y", py),
                step("CURL_COMPONENT", "k", fmt_diff(qx, py), curl_k),
            ]
            answer = (
                f"divergence {div}; curl <{curl_i}, {curl_j}, {curl_k}>"
            )
            problem = (
                f"For F(x,y,z) = <{p_txt}, {q_txt}, {r_txt}>, compute "
                f"the divergence and curl."
            )
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"div_curl_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
