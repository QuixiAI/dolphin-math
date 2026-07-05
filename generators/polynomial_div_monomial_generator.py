import random
from base_generator import ProblemGenerator
from helpers import step, jid


def mono_txt(coef, power):
    """Monomial with 1-coefficients dropped: x^3, -x, 7, 4x^2."""
    var = "" if power == 0 else "x" if power == 1 else f"x^{power}"
    if not var:
        return str(coef)
    if coef == 1:
        return var
    if coef == -1:
        return f"-{var}"
    return f"{coef}{var}"

class PolynomialDivMonomialGenerator(ProblemGenerator):
    """
    Generates problems for dividing a polynomial by a monomial.
    (ax^n + bx^m + ...) / (dx^k)
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        # Monomial divisor: d x^k
        d = random.randint(-9, 9)
        if d == 0: d = 1
        k = random.randint(1, 3)
        
        # Polynomial Terms: construct such that they divide cleanly usually, or produce simple fractions
        num_terms = random.randint(2, 4)
        poly_terms = []
        
        # Ensure degrees >= k mostly
        for i in range(num_terms):
            power = k + random.randint(0, 4) # degree >= divisor degree usually
            coeff = d * random.randint(-5, 5)
            if coeff == 0: coeff = d # avoid zero terms
            poly_terms.append((coeff, power))
            
        # Sort terms by degree desc
        poly_terms.sort(key=lambda x: x[1], reverse=True)
        
        # Format Poly
        poly_str_parts = []
        for i, (c, p) in enumerate(poly_terms):
            body = mono_txt(abs(c), p)
            sign = "-" if c < 0 else "+"
            if i == 0:
                term = mono_txt(c, p)
            else:
                term = f"{sign} {body}"
            poly_str_parts.append(term)
            
        poly_str = " ".join(poly_str_parts)
        
        # Format Divisor
        div_str = f"{d}x^{k}" if k > 1 else f"{d}x"
        if d == 1: div_str = f"x^{k}" if k > 1 else "x"
        if d == -1: div_str = f"-x^{k}" if k > 1 else "-x"
        
        problem_str = f"({poly_str}) / ({div_str})"
        
        steps = []
        steps.append(step("POLY_DIV_SETUP", problem_str))
        
        # Step 1: Split
        split_parts = []
        simplified_parts = []
        
        for c, p in poly_terms:
            # Term string
            term_c_str = mono_txt(c, p)
            
            split_expr = f"({term_c_str}) / ({div_str})"
            split_parts.append(split_expr)
            
            # Simplify
            new_c = c // d # integer division guaranteed by construction
            new_p = p - k
            
            if new_p < 0:
                # positive exponents in the denominator (algebra 1 style)
                denom = "x" if new_p == -1 else f"x^{abs(new_p)}"
                res = f"{new_c}/{denom}"
            else:
                res = mono_txt(new_c, new_p)
                
            # Handle sign for joining
            if not simplified_parts: # first term
                simplified_parts.append(res)
            else:
                # if res starts with -, keep it. if +, add +
                # if res is "2x", make it "+ 2x"
                # if res is "-2x", make it "- 2x"
                if res.startswith("-"):
                    simplified_parts.append(f"- {res[1:]}")
                else:
                    simplified_parts.append(f"+ {res}")
        
        steps.append(step("POLY_DIV_SPLIT", " + ".join(split_parts)))
        
        ans = " ".join(simplified_parts)
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="poly_div_monomial",
            problem=f"Divide: {problem_str}",
            steps=steps,
            final_answer=ans
        )
