import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec

DENOMS = [6, 8, 10, 12, 20]

# Die events on {1..6}: (description, set).
DIE_EVENTS = [
    ("even", {2, 4, 6}),
    ("odd", {1, 3, 5}),
    ("greater than 4", {5, 6}),
    ("less than 3", {1, 2}),
    ("prime", {2, 3, 5}),
    ("a multiple of 3", {3, 6}),
    ("at least 4", {4, 5, 6}),
]


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


class ProbabilityAdditionRuleGenerator(ProblemGenerator):
    """
    The addition rule P(A ∪ B) = P(A) + P(B) − P(A ∩ B), for both
    mutually exclusive events (intersection 0) and overlapping ones,
    plus the rearrangement that solves for the intersection. A concrete
    die variant reads the events as sets and counts outcomes. All
    probabilities are exact fractions.

    Variants:
    - mutually_exclusive: P(A ∪ B) = P(A) + P(B)
    - overlapping:        P(A ∪ B) = P(A) + P(B) − P(A ∩ B)
    - find_intersection:  solve P(A ∩ B) = P(A) + P(B) − P(A ∪ B)
    - die:                P(A ∪ B) for two events on a fair die

    Op-codes used:
    - ADD_SETUP: the given probabilities (or die events) and the goal
    - ADD_FORMULA: the addition rule being applied
    - DOMAIN_NOTE (established): mutually exclusive → intersection 0
    - COUNT: outcomes in a die event
    - A / S / FRAC_REDUCE (established): the arithmetic
    - Z: the exact probability
    """

    VARIANTS = ["mutually_exclusive", "overlapping",
                "find_intersection", "die"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant == "die":
            (na, sa), (nb, sb) = random.sample(DIE_EVENTS, 2)
            union = sa | sb
            inter = sa & sb
            steps = [
                step("ADD_SETUP",
                     f"fair die; A = {sorted(sa)}, B = {sorted(sb)}",
                     "P(A ∪ B)"),
                step("COUNT", f"A = {sorted(sa)}", f"{len(sa)}/6"),
                step("COUNT", f"B = {sorted(sb)}", f"{len(sb)}/6"),
                step("COUNT", f"A ∩ B = {sorted(inter)}",
                     f"{len(inter)}/6"),
                step("ADD_FORMULA",
                     "P(A ∪ B) = P(A) + P(B) - P(A ∩ B)"),
                step("A", f"{len(sa)}/6", f"{len(sb)}/6",
                     f"{len(sa) + len(sb)}/6"),
                step("S", f"{len(sa) + len(sb)}/6", f"{len(inter)}/6",
                     f"{len(union)}/6"),
            ]
            value = Fraction(len(union), 6)
            if exact(value) != f"{len(union)}/6":
                steps.append(step("FRAC_REDUCE", f"{len(union)}/6",
                                  exact(value)))
            answer = exact(value)
            problem = (f"A fair die is rolled. Let A be the event that "
                       f"the roll is {na} ({sorted(sa)}) and B the "
                       f"event that it is {nb} ({sorted(sb)}). Find "
                       f"P(A or B).")
        else:
            D = random.choice(DENOMS)

            def fr(k):
                return f"{k}/{D}"

            if variant == "mutually_exclusive":
                a = random.randint(1, D - 2)
                b = random.randint(1, D - 1 - a)
                total = a + b
                steps = [
                    step("ADD_SETUP",
                         f"P(A) = {fr(a)}, P(B) = {fr(b)}, "
                         f"mutually exclusive", "P(A ∪ B)"),
                    step("DOMAIN_NOTE", "mutually exclusive",
                         "P(A ∩ B) = 0"),
                    step("ADD_FORMULA", "P(A ∪ B) = P(A) + P(B)"),
                    step("A", fr(a), fr(b), fr(total)),
                ]
                value = Fraction(total, D)
                answer_k = total
                problem = (f"Events A and B are mutually exclusive "
                           f"with P(A) = {fr(a)} and P(B) = {fr(b)}. "
                           f"Find P(A or B).")
            elif variant == "overlapping":
                a = random.randint(2, D - 2)
                b = random.randint(2, D - 2)
                c = random.randint(1, min(a, b))
                while a + b - c > D - 1:  # keep P(A ∪ B) < 1
                    c += 1
                total = a + b
                union = total - c
                steps = [
                    step("ADD_SETUP",
                         f"P(A) = {fr(a)}, P(B) = {fr(b)}, "
                         f"P(A ∩ B) = {fr(c)}", "P(A ∪ B)"),
                    step("ADD_FORMULA",
                         "P(A ∪ B) = P(A) + P(B) - P(A ∩ B)"),
                    step("A", fr(a), fr(b), fr(total)),
                    step("S", fr(total), fr(c), fr(union)),
                ]
                value = Fraction(union, D)
                answer_k = union
                problem = (f"Events A and B have P(A) = {fr(a)}, "
                           f"P(B) = {fr(b)}, and P(A and B) = {fr(c)}. "
                           f"Find P(A or B).")
            else:  # find_intersection
                a = random.randint(2, D - 2)
                b = random.randint(2, D - 2)
                c = random.randint(1, min(a, b))
                while a + b - c > D - 1:  # keep given P(A ∪ B) < 1
                    c += 1
                union = a + b - c
                total = a + b
                steps = [
                    step("ADD_SETUP",
                         f"P(A) = {fr(a)}, P(B) = {fr(b)}, "
                         f"P(A ∪ B) = {fr(union)}", "P(A ∩ B)"),
                    step("ADD_FORMULA",
                         "P(A ∩ B) = P(A) + P(B) - P(A ∪ B)"),
                    step("A", fr(a), fr(b), fr(total)),
                    step("S", fr(total), fr(union), fr(c)),
                ]
                value = Fraction(c, D)
                answer_k = c
                problem = (f"Events A and B have P(A) = {fr(a)}, "
                           f"P(B) = {fr(b)}, and P(A or B) = "
                           f"{fr(union)}. Find P(A and B).")
            if exact(value) != fr(answer_k):
                steps.append(step("FRAC_REDUCE", fr(answer_k),
                                  exact(value)))
            answer = exact(value)
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation=f"probability_addition_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
