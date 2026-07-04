import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


DISTRIBUTIONS = [
    [Fraction(1, 2), Fraction(1, 2)],
    [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)],
    [Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)],
    [Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4)],
]


def fraction_text(value):
    return str(Fraction(value))


def list_text(values):
    return "[" + ",".join(fraction_text(v) for v in values) + "]"


def bit_unit(value):
    return "bit" if Fraction(value) == 1 else "bits"


class VonNeumannEntropyGenerator(ProblemGenerator):
    """
    Von Neumann entropy from dyadic eigenvalues:
    S(rho) = -sum lambda_i log2(lambda_i).

    Op-codes used:
    - ENTROPY_SETUP / LOG2
    - M / A (established/shared): exact term and sum arithmetic
    - Z: entropy in bits
    """

    def generate(self) -> dict:
        eigenvalues = list(random.choice(DISTRIBUTIONS))
        random.shuffle(eigenvalues)
        steps = [
            step("ENTROPY_SETUP", f"eigenvalues={list_text(eigenvalues)}",
                 "S=-sum lambda log2(lambda)"),
        ]
        running = Fraction(0)
        for value in eigenvalues:
            exponent = value.denominator.bit_length() - 1
            term = value * exponent
            steps.append(step("LOG2", fraction_text(value), -exponent))
            steps.append(step("M", fraction_text(value), exponent,
                              fraction_text(term)))
            new_running = running + term
            steps.append(step("A", fraction_text(running),
                              fraction_text(term), fraction_text(new_running)))
            running = new_running
        answer = f"S = {fraction_text(running)} {bit_unit(running)}"
        steps.append(step("Z", answer))
        problem = (
            f"Compute the von Neumann entropy in bits for a density "
            f"matrix with eigenvalues {list_text(eigenvalues)}."
        )
        return dict(
            problem_id=jid(),
            operation="von_neumann_entropy_dyadic",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
