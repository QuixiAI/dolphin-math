import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.quantum_gate_generator import QuantumGateGenerator
from helpers import DELIM


SINGLE_RE = re.compile(
    r"Apply the (H|X|Y|Z) gate to ket([01]) and give measurement "
    r"probabilities\."
)
CNOT_RE = re.compile(
    r"Apply the CNOT gate to ket([01])([01]) and give measurement "
    r"probabilities\."
)


def make_step(*parts):
    parts = [str(part) for part in parts]
    while parts and parts[-1] == "":
        parts.pop()
    return DELIM.join(parts)


def ket(bit):
    return f"ket{bit}"


def probs_for_basis(bit):
    return ("1", "0") if bit == 0 else ("0", "1")


SEQ_RE = re.compile(
    r"Apply ([HXYZ](?: then [HXYZ])+) to ket([01]) and give "
    r"the final state and measurement probabilities\.")


def parse_problem(problem):
    match = SINGLE_RE.fullmatch(problem)
    if match:
        return {"variant": "single", "gate": match.group(1),
                "bit": int(match.group(2))}
    match = SEQ_RE.fullmatch(problem)
    if match:
        return {"variant": "sequence",
                "gates": match.group(1).split(" then "),
                "bit": int(match.group(2))}
    match = CNOT_RE.fullmatch(problem)
    assert match is not None, problem
    return {"variant": "cnot", "control": int(match.group(1)),
            "target": int(match.group(2))}


def simulate_sequence(gates, bit):
    """Independent oracle: exact complex amplitudes (a0 + a1)/sqrt(2)^k."""
    amps = [1 + 0j, 0j] if bit == 0 else [0j, 1 + 0j]
    k = 0
    for gate in gates:
        a0, a1 = amps
        if gate == "X":
            amps = [a1, a0]
        elif gate == "Y":
            amps = [-1j * a1, 1j * a0]
        elif gate == "Z":
            amps = [a0, -a1]
        else:  # H
            amps = [a0 + a1, a0 - a1]
            k += 1
            if k >= 2 and all(a.real % 2 == 0 and a.imag % 2 == 0
                              for a in amps):
                amps = [a / 2 for a in amps]
                k -= 2
    return amps, k


PHASE_TXT = {(1, 0): "", (-1, 0): "-", (0, 1): "i", (0, -1): "-i"}


def state_text_from_amps(amps, k):
    a0, a1 = amps
    if k == 0:
        if a1 == 0:
            return f"{PHASE_TXT[(int(a0.real), int(a0.imag))]}ket0", ("1", "0")
        return f"{PHASE_TXT[(int(a1.real), int(a1.imag))]}ket1", ("0", "1")
    phase = PHASE_TXT[(int(a0.real), int(a0.imag))]
    sign = "+" if a1 == a0 else "-"
    return f"{phase}(ket0 {sign} ket1)/sqrt(2)", ("1/2", "1/2")


def expected_single(parts):
    gate = parts["gate"]
    bit = parts["bit"]
    matrix = {
        "H": "(1/sqrt(2))*[[1,1],[1,-1]]",
        "X": "[[0,1],[1,0]]",
        "Y": "[[0,-i],[i,0]]",
        "Z": "[[1,0],[0,-1]]",
    }[gate]
    if gate == "H":
        state = "(ket0 + ket1)/sqrt(2)" if bit == 0 else \
            "(ket0 - ket1)/sqrt(2)"
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
        make_step("QUANTUM_SETUP", f"gate={gate}", f"input={ket(bit)}"),
        make_step("GATE_MATRIX", gate, matrix),
        make_step("APPLY_GATE", gate, ket(bit), state),
        make_step("MEASURE_PROB", "computational basis",
                  f"P(0)={p0}", f"P(1)={p1}"),
    ]
    answer = f"state = {state}; P(0) = {p0}, P(1) = {p1}"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_cnot(parts):
    control = parts["control"]
    target = parts["target"]
    out_target = target ^ control
    input_state = f"ket{control}{target}"
    output_state = f"ket{control}{out_target}"
    steps = [
        make_step("QUANTUM_SETUP", "gate=CNOT", f"input={input_state}"),
        make_step("GATE_MATRIX", "CNOT",
                  "ket00bra00+ket01bra01+ket11bra10+ket10bra11"),
        make_step("XOR", f"control={control}", f"target={target}",
                  out_target),
        make_step("APPLY_GATE", "CNOT", input_state, output_state),
        make_step("MEASURE_PROB", "computational basis",
                  f"P({control}{out_target})=1", "all other outcomes 0"),
    ]
    answer = f"state = {output_state}; P({control}{out_target}) = 1"
    steps.append(make_step("Z", answer))
    return steps, answer


def expected_flow(example):
    parts = parse_problem(example["problem"])
    if parts["variant"] == "single":
        return expected_single(parts)
    return expected_cnot(parts)


class TestQuantumGateGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = QuantumGateGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_reconstructs_full_trace_from_problem_text(self):
        for _ in range(200):
            result = self.gen.generate()
            parts = parse_problem(result["problem"])
            if parts["variant"] == "sequence":
                continue  # covered by test_oracle_sequence_simulation
            expected_steps, answer = expected_flow(result)
            self.assertEqual(result["final_answer"], answer, result["problem"])
            self.assertEqual(result["steps"], expected_steps,
                             result["problem"])

    def test_oracle_sequence_simulation(self):
        """A9 oracle: exact amplitude simulation must reproduce the
        final state text and probabilities for gate sequences."""
        gen = QuantumGateGenerator("sequence")
        for _ in range(300):
            result = gen.generate()
            parts = parse_problem(result["problem"])
            amps, k = simulate_sequence(parts["gates"], parts["bit"])
            state, (p0, p1) = state_text_from_amps(amps, k)
            expected = f"state = {state}; P(0) = {p0}, P(1) = {p1}"
            self.assertEqual(result["final_answer"], expected,
                             result["problem"])

    def test_all_gates_available(self):
        seen = set()
        for _ in range(300):
            parts = parse_problem(self.gen.generate()["problem"])
            if parts["variant"] == "single":
                seen.add(parts["gate"])
            elif parts["variant"] == "cnot":
                seen.add("CNOT")
        self.assertEqual(seen, {"H", "X", "Y", "Z", "CNOT"})

    def test_xor_steps(self):
        gen = QuantumGateGenerator("cnot")
        for _ in range(50):
            result = gen.generate()
            xor = [s for s in result["steps"]
                   if s.startswith(f"XOR{DELIM}")][0].split(DELIM)
            control = int(xor[1].split("=")[1])
            target = int(xor[2].split("=")[1])
            self.assertEqual(control ^ target, int(xor[3]))

    def test_variants_and_invalid_variant(self):
        for variant in ("single", "cnot"):
            result = QuantumGateGenerator(variant).generate()
            self.assertEqual(result["operation"], f"quantum_gate_{variant}")
        with self.assertRaises(ValueError):
            QuantumGateGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(200):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
