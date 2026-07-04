import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid
from generators.exponential_model_generator import dec


def exact(fr):
    """Terminating decimal when possible, else the reduced fraction."""
    d = fr.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return dec(fr) if d == 1 else str(fr)


class ConditionalProbabilityGenerator(ProblemGenerator):
    """
    Conditional probability from a two-way table and Bayes-style diagnostic
    test questions built from sensitivity and specificity. Counts are small
    integers, so each answer is exact.

    Variants:
    - table:           compute P(A given B) from a 2x2 count table
    - bayes_positive:  compute P(disease=yes given test positive)
    - bayes_negative:  compute P(disease=no given test negative)

    Op-codes used:
    - COND_SETUP: table or diagnostic setup and target probability
    - COND_TOTAL: denominator count for the conditioning event
    - COND_COUNT: numerator count for the joint event
    - COND_FORMULA: P(A given B) = count(A and B)/count(B)
    - BAYES_SETUP: disease counts, test rates, and target probability
    - BAYES_CELL: diagnostic cell count, arithmetic, result
    - BAYES_FORMULA: posterior ratio from diagnostic cells
    - A / FRAC_BUILD / CHECK (established): arithmetic and verification
    - Z: the exact conditional probability
    """

    VARIANTS = ["table", "bayes_positive", "bayes_negative"]
    RATES = [
        (Fraction(3, 4), Fraction(4, 5)),
        (Fraction(4, 5), Fraction(9, 10)),
        (Fraction(5, 6), Fraction(7, 8)),
        (Fraction(7, 10), Fraction(3, 4)),
        (Fraction(9, 10), Fraction(19, 20)),
    ]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    @staticmethod
    def _frac_step(num, den):
        raw = Fraction(num, den)
        return step("FRAC_BUILD", f"{num}/{den}", exact(raw)), exact(raw)

    def _generate_table(self):
        cells = {
            ("yes", "bike"): random.randint(4, 28),
            ("no", "bike"): random.randint(4, 28),
            ("yes", "bus"): random.randint(4, 28),
            ("no", "bus"): random.randint(4, 28),
        }
        target_kind = random.choice(["club_given_commute",
                                     "commute_given_club"])
        club_value = random.choice(["yes", "no"])
        commute_value = random.choice(["bike", "bus"])

        if target_kind == "club_given_commute":
            target = f"club={club_value}"
            given = f"commute={commute_value}"
            numerator = cells[(club_value, commute_value)]
            denominator = sum(cells[(rv, commute_value)]
                              for rv in ("yes", "no"))
            total_label = f"commute={commute_value} total"
            total_work = (f"{cells[('yes', commute_value)]} + "
                          f"{cells[('no', commute_value)]} = {denominator}")
            joint_label = f"club={club_value} and commute={commute_value}"
        else:
            target = f"commute={commute_value}"
            given = f"club={club_value}"
            numerator = cells[(club_value, commute_value)]
            denominator = sum(cells[(club_value, cv)]
                              for cv in ("bike", "bus"))
            total_label = f"club={club_value} total"
            total_work = (f"{cells[(club_value, 'bike')]} + "
                          f"{cells[(club_value, 'bus')]} = {denominator}")
            joint_label = f"club={club_value} and commute={commute_value}"

        frac_step, answer = self._frac_step(numerator, denominator)
        steps = [
            step("COND_SETUP",
                 f"yes/bike {cells[('yes', 'bike')]}, "
                 f"no/bike {cells[('no', 'bike')]}, "
                 f"yes/bus {cells[('yes', 'bus')]}, "
                 f"no/bus {cells[('no', 'bus')]}",
                 f"P({target} given {given})"),
            step("COND_TOTAL", total_label, total_work),
            step("COND_COUNT", joint_label, numerator),
            step("COND_FORMULA",
                 "P(A given B) = count(A and B)/count(B)"),
            frac_step,
            step("CHECK", f"{numerator} <= {denominator}",
                 "valid conditional probability"),
            step("Z", answer),
        ]
        problem = (
            "A two-way table for students has counts: "
            f"club=yes and commute=bike: {cells[('yes', 'bike')]}; "
            f"club=no and commute=bike: {cells[('no', 'bike')]}; "
            f"club=yes and commute=bus: {cells[('yes', 'bus')]}; "
            f"club=no and commute=bus: {cells[('no', 'bus')]}. "
            f"Find P({target} given {given}). Give an exact answer."
        )
        return "table", problem, steps, answer

    def _generate_bayes(self, variant):
        sensitivity, specificity = random.choice(self.RATES)
        sens_den = sensitivity.denominator
        spec_den = specificity.denominator
        disease = sens_den * random.randint(4, 12)
        no_disease = spec_den * random.randint(8, 24)
        total = disease + no_disease

        true_positive = (disease * sensitivity).numerator
        false_negative = disease - true_positive
        true_negative = (no_disease * specificity).numerator
        false_positive = no_disease - true_negative

        if variant == "bayes_positive":
            target = "P(disease=yes given test positive)"
            denominator = true_positive + false_positive
            numerator = true_positive
            split_label = "positive tests"
            formula = "P(disease=yes given positive) = TP/(TP + FP)"
            add_step = step("A", true_positive, false_positive, denominator)
        else:
            target = "P(disease=no given test negative)"
            denominator = true_negative + false_negative
            numerator = true_negative
            split_label = "negative tests"
            formula = "P(disease=no given negative) = TN/(TN + FN)"
            add_step = step("A", true_negative, false_negative, denominator)

        frac_step, answer = self._frac_step(numerator, denominator)
        steps = [
            step("BAYES_SETUP",
                 f"disease=yes {disease}, disease=no {no_disease}",
                 f"sensitivity {sensitivity}, specificity {specificity}",
                 target),
            step("BAYES_CELL", "true positive",
                 f"{disease} * {sensitivity}", true_positive),
            step("BAYES_CELL", "false negative",
                 f"{disease} - {true_positive}", false_negative),
            step("BAYES_CELL", "true negative",
                 f"{no_disease} * {specificity}", true_negative),
            step("BAYES_CELL", "false positive",
                 f"{no_disease} - {true_negative}", false_positive),
            add_step,
            step("BAYES_FORMULA", formula),
            frac_step,
            step("CHECK", split_label,
                 f"posterior denominator = {denominator}"),
            step("Z", answer),
        ]
        problem = (
            f"A screening test is used for {total} people. Disease=yes "
            f"count is {disease} and disease=no count is {no_disease}. "
            "Sensitivity P(test positive given disease=yes) = "
            f"{sensitivity}. Specificity P(test negative given disease=no) "
            f"= {specificity}. Find {target}. Give an exact answer."
        )
        return variant, problem, steps, answer

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "table":
            op_suffix, problem, steps, answer = self._generate_table()
        else:
            op_suffix, problem, steps, answer = self._generate_bayes(variant)

        return dict(
            problem_id=jid(),
            operation=f"conditional_probability_{op_suffix}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
