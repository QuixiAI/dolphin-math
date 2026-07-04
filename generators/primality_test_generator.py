import random
from math import gcd

from base_generator import ProblemGenerator
from helpers import step, jid


PRIMES = [31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
COMPOSITES = [21, 25, 27, 33, 35, 39, 45, 49, 51, 55, 57, 65,
              69, 77, 81, 85, 87, 91, 95, 99, 121, 143, 145,
              187, 221, 341]


def list_text(values):
    return ", ".join(str(value) for value in values)


def decompose(n):
    value = n - 1
    s = 0
    d = value
    divisions = []
    while d % 2 == 0:
        next_d = d // 2
        divisions.append((d, next_d))
        s += 1
        d = next_d
    return s, d, divisions


def witness_passes(n, witness):
    s, d, _ = decompose(n)
    x = pow(witness, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(1, s):
        x = (x * x) % n
        if x == n - 1:
            return True
    return False


class PrimalityTestGenerator(ProblemGenerator):
    """
    Miller-Rabin primality test traces with supplied witnesses.

    Op-codes used:
    - MR_SETUP / MR_DECOMPOSE: n and n-1 = 2^s d
    - MR_WITNESS / MR_SQUARE / MR_WITNESS_RESULT: per-witness trace
    - D / M / MOD_POWER / MOD_REDUCE (established/shared): arithmetic
    - Z: composite witness or probably-prime result for the witnesses
    """

    def generate(self) -> dict:
        if random.random() < 0.45:
            n = random.choice(PRIMES)
            witnesses = sorted(random.sample(range(2, min(n - 1, 12)), 2))
        else:
            while True:
                n = random.choice(COMPOSITES)
                pool = [a for a in range(2, min(n - 1, 20))
                        if gcd(a, n) == 1]
                random.shuffle(pool)
                witnesses = sorted(pool[:2])
                if any(not witness_passes(n, witness)
                       for witness in witnesses):
                    break

        s, d, divisions = decompose(n)
        steps = [
            step("MR_SETUP", f"n={n}", f"witnesses {list_text(witnesses)}"),
        ]
        for value, next_value in divisions:
            steps.append(step("D", value, 2, next_value))
        steps.append(step("MR_DECOMPOSE", n - 1, f"2^{s} * {d}"))

        composite_witness = None
        for witness in witnesses:
            steps.append(step("MR_WITNESS", witness))
            x = pow(witness, d, n)
            steps.append(step("MOD_POWER", f"{witness}^{d}", f"mod {n}", x))
            if x in (1, n - 1):
                steps.append(step("MR_WITNESS_RESULT", witness,
                                  "passes initial"))
                continue

            passed = False
            for r in range(1, s):
                previous = x
                squared = previous * previous
                x = squared % n
                steps.append(step("M", previous, previous, squared))
                steps.append(step("MOD_REDUCE", squared, f"mod {n}", x))
                steps.append(step("MR_SQUARE", f"r={r}", x))
                if x == n - 1:
                    steps.append(step("MR_WITNESS_RESULT", witness,
                                      f"passes at r={r}"))
                    passed = True
                    break
            if not passed:
                steps.append(step("MR_WITNESS_RESULT", witness, "composite"))
                composite_witness = witness
                break

        if composite_witness is None:
            answer = f"probably prime for witnesses = {list_text(witnesses)}"
        else:
            answer = f"composite; witness = {composite_witness}"
        problem = (
            f"Use the Miller-Rabin test on n={n} with witnesses "
            f"{list_text(witnesses)}."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="primality_test_miller_rabin",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
