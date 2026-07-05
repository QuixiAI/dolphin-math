import random

from base_generator import ProblemGenerator
from helpers import step, jid


SINGLE_GATES = ["H", "X", "Y", "Z"]

# exact single-qubit state machine over {|0>, |1>, |+>, |->} with a
# global phase in {1, -1, i, -i}: gate -> kind -> (new_kind, phase_factor)
GATE_ACTION = {
    "X": {"0": ("1", 1), "1": ("0", 1), "+": ("+", 1), "-": ("-", -1)},
    "Z": {"0": ("0", 1), "1": ("1", -1), "+": ("-", 1), "-": ("+", 1)},
    "Y": {"0": ("1", 1j), "1": ("0", -1j), "+": ("-", -1j), "-": ("+", 1j)},
    "H": {"0": ("+", 1), "1": ("-", 1), "+": ("0", 1), "-": ("1", 1)},
}
PHASE_TXT = {1: "", -1: "-", 1j: "i", -1j: "-i"}
KIND_TXT = {
    "0": "ket0",
    "1": "ket1",
    "+": "(ket0 + ket1)/sqrt(2)",
    "-": "(ket0 - ket1)/sqrt(2)",
}


def state_txt(kind, phase):
    return f"{PHASE_TXT[phase]}{KIND_TXT[kind]}"


def ket(bit):
    return f"ket{bit}"


def probs_for_basis(bit):
    return ("1", "0") if bit == 0 else ("0", "1")


class QuantumGateGenerator(ProblemGenerator):
    """
    Apply H, X, Y, Z, and CNOT gates to basis states, with exact
    measurement probabilities.

    Variants:
    - single: one-qubit gate on |0> or |1>.
    - sequence: 2-3 one-qubit gates applied in order, phase tracked exactly.
    - cnot: two-qubit CNOT on |control target>.

    Op-codes used:
    - QUANTUM_SETUP / GATE_MATRIX / APPLY_GATE / MEASURE_PROB / XOR
    - Z: output state and probabilities
    """

    VARIANTS = ["single", "sequence", "cnot"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "single":
            problem, steps, answer = self._generate_single()
        elif variant == "sequence":
            problem, steps, answer = self._generate_sequence()
        else:
            problem, steps, answer = self._generate_cnot()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"quantum_gate_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_single(self):
        gate = random.choice(SINGLE_GATES)
        bit = random.randint(0, 1)
        matrix = {
            "H": "(1/sqrt(2))*[[1,1],[1,-1]]",
            "X": "[[0,1],[1,0]]",
            "Y": "[[0,-i],[i,0]]",
            "Z": "[[1,0],[0,-1]]",
        }[gate]
        if gate == "H":
            if bit == 0:
                state = "(ket0 + ket1)/sqrt(2)"
            else:
                state = "(ket0 - ket1)/sqrt(2)"
            p0, p1 = "1/2", "1/2"
        elif gate == "X":
            out = 1 - bit
            state = ket(out)
            p0, p1 = probs_for_basis(out)
        elif gate == "Y":
            out = 1 - bit
            phase = "i" if bit == 0 else "-i"
            state = f"{phase}{ket(out)}"
            p0, p1 = probs_for_basis(out)
        else:
            phase = "" if bit == 0 else "-"
            state = f"{phase}{ket(bit)}"
            p0, p1 = probs_for_basis(bit)
        steps = [
            step("QUANTUM_SETUP", f"gate={gate}", f"input={ket(bit)}"),
            step("GATE_MATRIX", gate, matrix),
            step("APPLY_GATE", gate, ket(bit), state),
            step("MEASURE_PROB", "computational basis",
                 f"P(0)={p0}", f"P(1)={p1}"),
        ]
        answer = f"state = {state}; P(0) = {p0}, P(1) = {p1}"
        problem = f"Apply the {gate} gate to {ket(bit)} and give measurement probabilities."
        return problem, steps, answer

    def _generate_sequence(self):
        n = random.choice([2, 3])
        gates = [random.choice(SINGLE_GATES) for _ in range(n)]
        bit = random.randint(0, 1)
        kind, phase = str(bit), 1
        steps = [step("QUANTUM_SETUP", f"gates={' then '.join(gates)}",
                      f"input={ket(bit)}")]
        for gate in gates:
            prev_txt = state_txt(kind, phase)
            new_kind, factor = GATE_ACTION[gate][kind]
            phase = phase * factor
            kind = new_kind
            steps.append(step("APPLY_GATE", gate, prev_txt,
                              state_txt(kind, phase)))
        state = state_txt(kind, phase)
        if kind in ("0", "1"):
            p0, p1 = probs_for_basis(int(kind))
        else:
            p0, p1 = "1/2", "1/2"
        steps.append(step("MEASURE_PROB", "computational basis",
                          f"P(0)={p0}", f"P(1)={p1}"))
        answer = f"state = {state}; P(0) = {p0}, P(1) = {p1}"
        problem = (f"Apply {' then '.join(gates)} to {ket(bit)} and give "
                   f"the final state and measurement probabilities.")
        return problem, steps, answer

    def _generate_cnot(self):
        control = random.randint(0, 1)
        target = random.randint(0, 1)
        out_target = target ^ control
        input_state = f"ket{control}{target}"
        output_state = f"ket{control}{out_target}"
        steps = [
            step("QUANTUM_SETUP", "gate=CNOT", f"input={input_state}"),
            step("GATE_MATRIX", "CNOT",
                 "ket00bra00+ket01bra01+ket11bra10+ket10bra11"),
            step("XOR", f"control={control}", f"target={target}",
                 out_target),
            step("APPLY_GATE", "CNOT", input_state, output_state),
            step("MEASURE_PROB", "computational basis",
                 f"P({control}{out_target})=1", "all other outcomes 0"),
        ]
        answer = f"state = {output_state}; P({control}{out_target}) = 1"
        problem = (
            f"Apply the CNOT gate to {input_state} and give measurement "
            f"probabilities."
        )
        return problem, steps, answer
