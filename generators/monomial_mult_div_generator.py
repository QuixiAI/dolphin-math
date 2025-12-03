import random
from base_generator import ProblemGenerator
from helpers import step, jid

class MonomialMultDivGenerator(ProblemGenerator):
    """
    Generates problems for multiplying and dividing monomials.
    
    e.g. (3x^2)(4x^5) or (10x^5)/(2x^2)
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        op = random.choice(['*', '/'])
        
        if op == '*':
            # Mult: (ax^n)(bx^m)
            c1 = random.randint(-9, 9)
            if c1 == 0: c1 = 1
            c2 = random.randint(-9, 9)
            if c2 == 0: c2 = 1
            
            p1 = random.randint(1, 9)
            p2 = random.randint(1, 9)
            
            term1 = f"{c1}x^{p1}" if p1 > 1 else f"{c1}x"
            term2 = f"{c2}x^{p2}" if p2 > 1 else f"{c2}x"
            
            problem_str = f"({term1})({term2})"
            
            steps = []
            steps.append(step("MONO_SETUP", problem_str))
            
            # Step 1: Coeffs
            new_c = c1 * c2
            steps.append(step("MONO_MULT_COEFF", f"{c1} * {c2}", str(new_c)))
            
            # Step 2: Exponents
            new_p = p1 + p2
            steps.append(step("MONO_ADD_EXP", f"x^{p1} * x^{p2} = x^({p1}+{p2})", f"x^{new_p}"))
            
            ans = f"{new_c}x^{new_p}"
            steps.append(step("Z", ans))
            
            return dict(
                problem_id=jid(),
                operation="monomial_mult",
                problem=f"Simplify: {problem_str}",
                steps=steps,
                final_answer=ans
            )
            
        else:
            # Div: (ax^n)/(bx^m)
            # Ensure divisibility for simple answer
            c2 = random.randint(-9, 9)
            if c2 == 0: c2 = 1
            factor = random.randint(1, 9) * random.choice([-1, 1])
            c1 = c2 * factor
            
            p2 = random.randint(1, 5)
            diff = random.randint(0, 5)
            p1 = p2 + diff
            
            term1 = f"{c1}x^{p1}" if p1 > 1 else f"{c1}x"
            term2 = f"{c2}x^{p2}" if p2 > 1 else f"{c2}x"
            
            problem_str = f"({term1}) / ({term2})"
            
            steps = []
            steps.append(step("MONO_SETUP", problem_str))
            
            # Coeffs
            new_c = c1 // c2
            steps.append(step("MONO_DIV_COEFF", f"{c1} / {c2}", str(new_c)))
            
            # Exponents
            new_p = p1 - p2
            if new_p == 0:
                steps.append(step("MONO_SUB_EXP", f"x^{p1} / x^{p2} = x^({p1}-{p2})", "x^0 = 1"))
                ans = f"{new_c}"
            elif new_p == 1:
                steps.append(step("MONO_SUB_EXP", f"x^{p1} / x^{p2} = x^({p1}-{p2})", "x^1 = x"))
                ans = f"{new_c}x"
            else:
                steps.append(step("MONO_SUB_EXP", f"x^{p1} / x^{p2} = x^({p1}-{p2})", f"x^{new_p}"))
                ans = f"{new_c}x^{new_p}"
                
            steps.append(step("Z", ans))
            
            return dict(
                problem_id=jid(),
                operation="monomial_div",
                problem=f"Simplify: {problem_str}",
                steps=steps,
                final_answer=ans
            )
