import random
from fractions import Fraction

from base_generator import ProblemGenerator
from helpers import step, jid


def fraction_text(value):
    return str(Fraction(value))


class PerplexityGenerator(ProblemGenerator):
    """
    Cross-entropy and perplexity from dyadic probabilities.

    If each true-token probability is p=1/2^k, then average cross-entropy is
    -ln(p)=ln(2^k) and perplexity exp(CE)=2^k exactly.

    Op-codes used:
    - PERPLEXITY_SETUP / NEG_LOG / NLL / CROSS_ENTROPY / PERPLEXITY
    - D (established/shared): probability and reciprocal/perplexity
    - Z: total NLL, average CE, perplexity
    """

    def generate(self) -> dict:
        tokens = random.randint(1, 200)
        denom = random.choice([2, 4, 8, 16, 32, 64, 128, 256])
        probability = Fraction(1, denom)
        steps = [
            step("PERPLEXITY_SETUP", f"tokens={tokens}", f"p=1/{denom}"),
            step("D", 1, denom, fraction_text(probability)),
            step("NEG_LOG", f"p={fraction_text(probability)}",
                 f"ln({denom})"),
            step("NLL", f"{tokens} tokens", f"{tokens}*ln({denom})"),
            step("CROSS_ENTROPY", "average", f"ln({denom})"),
            step("D", 1, fraction_text(probability), denom),
            step("PERPLEXITY", "exp(CE)", denom),
        ]
        answer = (
            f"total_nll={tokens}*ln({denom}); CE=ln({denom}); "
            f"perplexity={denom}"
        )
        steps.append(step("Z", answer))
        problem = (
            f"For a sequence of {tokens} tokens where each true-token "
            f"probability is p=1/{denom}, compute total negative "
            "log-likelihood, average cross-entropy, and perplexity."
        )
        return dict(
            problem_id=jid(),
            operation="perplexity_dyadic",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
