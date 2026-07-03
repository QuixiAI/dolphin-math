import random
from base_generator import ProblemGenerator
from helpers import step, jid

CORES = [2, 3, 5, 6, 7, 10, 11, 13]


def rad_term(coef, f):
    """Renders coef·√f: '5√2', '√3', '-2√5'."""
    if coef == 1:
        return f"√{f}"
    if coef == -1:
        return f"-√{f}"
    return f"{coef}√{f}"


class RadicalAddSubGenerator(ProblemGenerator):
    """
    Adds and subtracts radicals: simplify every term to its like-radicand
    form first, then combine coefficients. About one case in five has
    genuinely unlike radicands after simplification — the honest answer is
    the simplified-but-uncombined expression (the judgment must be earned).

    Op-codes used:
    - ROOT_SETUP: the expression (string)
    - SQUARE_FACTOR / ROOT: simplify one term (shared with the variable
      radical generator)
    - REWRITE: the whole expression after each term simplifies (string)
    - A / S: combine like radical terms (term, term, result)
    - UNLIKE_RADICALS: unlike cores after simplification (comparison, verdict)
    - Z: final answer
    """

    def generate(self) -> dict:
        if random.random() < 0.2:
            return self._unlike_case()
        return self._combinable_case()

    def _simplify_term_steps(self, steps, terms_display, idx, c, s, f,
                             sign=1):
        """Emits the SQUARE_FACTOR/ROOT steps for term idx (if s > 1) and
        the expression REWRITE; returns the simplified term string."""
        simplified = rad_term(c * s, f)
        if s > 1:
            n = s * s * f
            steps.append(step("SQUARE_FACTOR", n, f"{s * s} × {f}", s * s))
            steps.append(step("ROOT", s * s, s))
            terms_display[idx] = (simplified if sign > 0
                                  else f"-{simplified}")
            expr = terms_display[0]
            for t in terms_display[1:]:
                expr += f" - {t[1:]}" if t.startswith("-") else f" + {t}"
            steps.append(step("REWRITE", expr))
        return simplified

    def _combinable_case(self):
        f = random.choice(CORES)
        n_terms = random.choice([2, 2, 3])
        while True:
            cs = [random.randint(1, 4) for _ in range(n_terms)]
            ss = [random.randint(1, 5) for _ in range(n_terms)]
            signs = [1] + [random.choice([-1, 1]) for _ in range(n_terms - 1)]
            if not any(s > 1 for s in ss):
                continue
            total = sum(sign * c * s for sign, c, s in zip(signs, cs, ss))
            if total != 0:
                break

        display = []
        for i, (sign, c, s) in enumerate(zip(signs, cs, ss)):
            t = rad_term(c, s * s * f) if s > 1 else rad_term(c, f)
            display.append(t if sign > 0 else f"-{t}")
        expr = display[0]
        for t in display[1:]:
            expr += f" - {t[1:]}" if t.startswith("-") else f" + {t}"
        original = expr

        steps = [step("ROOT_SETUP", original)]
        simplified = []
        for i, (sign, c, s) in enumerate(zip(signs, cs, ss)):
            self._simplify_term_steps(steps, display, i, c, s, f, sign)
            simplified.append(sign * c * s)

        acc = simplified[0]
        for coef in simplified[1:]:
            steps.append(step("A" if coef > 0 else "S",
                              rad_term(acc, f),
                              rad_term(abs(coef), f),
                              rad_term(acc + coef, f)))
            acc += coef

        answer = rad_term(acc, f)
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="radical_add_sub",
            problem=f"Simplify: {original}",
            steps=steps,
            final_answer=answer,
        )

    def _unlike_case(self):
        f1, f2 = random.sample(CORES, 2)
        f1, f2 = sorted((f1, f2))
        c1, c2 = random.randint(1, 4), random.randint(1, 4)
        s1, s2 = random.randint(1, 4), random.randint(1, 4)
        if s1 == 1 and s2 == 1:
            s1 = random.randint(2, 4)
        sign = random.choice([" + ", " - "])

        t1 = rad_term(c1, s1 * s1 * f1) if s1 > 1 else rad_term(c1, f1)
        t2 = rad_term(c2, s2 * s2 * f2) if s2 > 1 else rad_term(c2, f2)
        original = f"{t1}{sign}{t2}"
        display = [t1, t2 if sign == " + " else f"-{t2}"]

        steps = [step("ROOT_SETUP", original)]
        st1 = self._simplify_term_steps(steps, display, 0, c1, s1, f1)
        st2 = self._simplify_term_steps(steps, display, 1, c2, s2, f2,
                                        1 if sign == " + " else -1)
        answer = f"{st1}{sign}{st2}"
        steps.append(step("UNLIKE_RADICALS", f"√{f1} ≠ √{f2}",
                          "unlike radicands — cannot combine"))
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation="radical_add_sub",
            problem=f"Simplify: {original}",
            steps=steps,
            final_answer=answer,
        )
