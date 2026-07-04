import random

from base_generator import ProblemGenerator
from helpers import step, jid


def vector_text(values):
    return "[" + ",".join(str(v) for v in values) + "]"


def diag_text(values):
    return "diag(" + ",".join(str(v) for v in values) + ")"


class TensorProductGenerator(ProblemGenerator):
    """
    Build a 4x4 operator from a 2x2 diagonal tensor product and apply
    it to a product state.

    Op-codes used:
    - TENSOR_SETUP / TENSOR_RULE / TENSOR_STATE
    - M (established/shared): exact integer products
    - Z: diagonal 4x4 operator and output vector
    """

    def generate(self) -> dict:
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        d = random.randint(-5, 5)
        if a == 0 and b == 0:
            a = 1
        if c == 0 and d == 0:
            c = 1
        u = [random.randint(-4, 4), random.randint(-4, 4)]
        v = [random.randint(-4, 4), random.randint(-4, 4)]
        if u == [0, 0]:
            u[0] = 1
        if v == [0, 0]:
            v[0] = 1

        diag_entries = [a * c, a * d, b * c, b * d]
        state_entries = [u[0] * v[0], u[0] * v[1],
                         u[1] * v[0], u[1] * v[1]]
        result_entries = [left * right for left, right
                          in zip(diag_entries, state_entries)]
        steps = [
            step("TENSOR_SETUP", f"A=diag({a},{b})", f"B=diag({c},{d})",
                 f"u={vector_text(u)}, v={vector_text(v)}"),
            step("TENSOR_RULE",
                 "diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)"),
            step("M", a, c, diag_entries[0]),
            step("M", a, d, diag_entries[1]),
            step("M", b, c, diag_entries[2]),
            step("M", b, d, diag_entries[3]),
            step("TENSOR_STATE", "u tensor v",
                 vector_text(state_entries)),
            step("M", u[0], v[0], state_entries[0]),
            step("M", u[0], v[1], state_entries[1]),
            step("M", u[1], v[0], state_entries[2]),
            step("M", u[1], v[1], state_entries[3]),
        ]
        for diag_value, state_value, result_value in zip(
                diag_entries, state_entries, result_entries):
            steps.append(step("M", diag_value, state_value, result_value))

        answer = (
            f"A tensor B = {diag_text(diag_entries)}; "
            f"output = {vector_text(result_entries)}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"Let A=diag({a},{b}), B=diag({c},{d}), u={vector_text(u)}, "
            f"and v={vector_text(v)}. Build A tensor B and apply it to "
            f"u tensor v."
        )
        return dict(
            problem_id=jid(),
            operation="tensor_product_diagonal_apply",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
