import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


def ket(n):
    return f"ket{n}"


def sqrt_text(value):
    if value == 0:
        return "0"
    if value == 1:
        return "1"
    return f"sqrt({value})"


def sqrt_ket(coeff, n):
    root = sqrt_text(coeff)
    if root == "0":
        return "0"
    if root == "1":
        return ket(n)
    return f"{root} {ket(n)}"


def scaled_ket(coeff, n):
    if coeff == 0:
        return "0"
    if coeff == 1:
        return ket(n)
    if coeff == -1:
        return f"-{ket(n)}"
    return f"{coeff} {ket(n)}"


class LadderOperatorGenerator(ProblemGenerator):
    """
    Harmonic-oscillator ladder-operator algebra and energy levels.

    Variants:
    - single_step_energy: apply a or adag once, then compute the new energy.
    - number_energy: compute N=adag*a on ket n, then compute E_n.
    - commutator_energy: compare a*adag and adag*a on ket n, then compute E_n.

    Op-codes used:
    - LADDER_SETUP / LADDER_RULE / LADDER_APPLY / NUMBER_OPERATOR
    - LADDER_COMM / ENERGY_LEVEL
    - A / S / M / D / ROOT (established/shared): exact coefficient arithmetic
    - CHECK / Z: identity verification and final result
    """

    VARIANTS = ["single_step_energy", "number_energy", "commutator_energy"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "single_step_energy":
            problem, steps, answer = self._generate_single_step()
        elif variant == "number_energy":
            problem, steps, answer = self._generate_number_energy()
        else:
            problem, steps, answer = self._generate_commutator_energy()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"ladder_operator_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    @staticmethod
    def _rule_steps(variant, n, hbar, omega):
        return [
            step("LADDER_SETUP", variant, f"state={ket(n)}",
                 f"hbar={hbar}, omega={omega}"),
            step("LADDER_RULE", "a ketn=sqrt(n) ket(n-1)",
                 "adag ketn=sqrt(n+1) ket(n+1)"),
        ]

    @staticmethod
    def _energy_steps(n, hbar, omega):
        two_n = 2 * n
        odd = two_n + 1
        hbar_omega = hbar * omega
        numerator = hbar_omega * odd
        energy = Fraction(numerator, 2)
        return [
            step("M", 2, n, two_n),
            step("A", two_n, 1, odd),
            step("M", hbar, omega, hbar_omega),
            step("M", hbar_omega, odd, numerator),
            step("D", numerator, 2, fraction_text(energy)),
            step("ENERGY_LEVEL", f"E_{n}=hbar*omega*(n+1/2)",
                 fraction_text(energy)),
        ], energy

    def _generate_single_step(self):
        operator = random.choice(["a", "adag"])
        n = random.randint(1, 30) if operator == "a" else random.randint(0, 30)
        hbar = random.randint(1, 12)
        omega = random.randint(1, 12)
        if operator == "a":
            new_n = n - 1
            coeff = n
            move_step = step("S", n, 1, new_n)
            applied = sqrt_ket(coeff, new_n)
        else:
            new_n = n + 1
            coeff = new_n
            move_step = step("A", n, 1, new_n)
            applied = sqrt_ket(coeff, new_n)
        steps = self._rule_steps("single_step_energy", n, hbar, omega)
        steps.extend([
            move_step,
            step("LADDER_APPLY", f"{operator} {ket(n)}", applied),
        ])
        energy_steps, energy = self._energy_steps(new_n, hbar, omega)
        steps.extend(energy_steps)
        answer = (
            f"{operator} {ket(n)}={applied}; "
            f"E_{new_n}={fraction_text(energy)}"
        )
        problem = (
            f"For harmonic oscillator state {ket(n)} with hbar={hbar} and "
            f"omega={omega}, apply {operator} once and compute the new energy."
        )
        return problem, steps, answer

    def _generate_number_energy(self):
        n = random.randint(1, 30)
        hbar = random.randint(1, 12)
        omega = random.randint(1, 12)
        lowered = sqrt_ket(n, n - 1)
        product = n * n
        steps = self._rule_steps("number_energy", n, hbar, omega)
        steps.extend([
            step("LADDER_APPLY", f"a {ket(n)}", lowered),
            step("LADDER_APPLY", f"adag {lowered}",
                 f"sqrt({n})*sqrt({n}) {ket(n)}"),
            step("M", n, n, product),
            step("ROOT", product, n),
            step("NUMBER_OPERATOR", f"N {ket(n)}", scaled_ket(n, n)),
        ])
        energy_steps, energy = self._energy_steps(n, hbar, omega)
        steps.extend(energy_steps)
        answer = f"N {ket(n)}={scaled_ket(n, n)}; E_{n}={fraction_text(energy)}"
        problem = (
            f"For harmonic oscillator state {ket(n)} with hbar={hbar} and "
            f"omega={omega}, compute N=adag*a and E_{n}."
        )
        return problem, steps, answer

    def _generate_commutator_energy(self):
        n = random.randint(1, 30)
        hbar = random.randint(1, 12)
        omega = random.randint(1, 12)
        up_n = n + 1
        raised = sqrt_ket(up_n, up_n)
        lowered = sqrt_ket(n, n - 1)
        aa_dag_coeff = up_n
        adag_a_coeff = n
        diff = aa_dag_coeff - adag_a_coeff
        steps = self._rule_steps("commutator_energy", n, hbar, omega)
        steps.extend([
            step("A", n, 1, up_n),
            step("LADDER_APPLY", f"adag {ket(n)}", raised),
            step("LADDER_APPLY", f"a {raised}",
                 f"sqrt({up_n})*sqrt({up_n}) {ket(n)}"),
            step("M", up_n, up_n, up_n * up_n),
            step("ROOT", up_n * up_n, aa_dag_coeff),
            step("LADDER_APPLY", f"a {ket(n)}", lowered),
            step("LADDER_APPLY", f"adag {lowered}",
                 f"sqrt({n})*sqrt({n}) {ket(n)}"),
            step("M", n, n, n * n),
            step("ROOT", n * n, adag_a_coeff),
            step("S", aa_dag_coeff, adag_a_coeff, diff),
            step("LADDER_COMM", "[a,adag] ketn", scaled_ket(diff, n)),
            step("CHECK", "identity", "[a,adag]=1", "matches ketn"),
        ])
        energy_steps, energy = self._energy_steps(n, hbar, omega)
        steps.extend(energy_steps)
        answer = (
            f"[a,adag] {ket(n)}={scaled_ket(diff, n)}; "
            f"E_{n}={fraction_text(energy)}"
        )
        problem = (
            f"For harmonic oscillator state {ket(n)} with hbar={hbar} and "
            f"omega={omega}, compare a*adag and adag*a, then compute E_{n}."
        )
        return problem, steps, answer
