import random
from base_generator import ProblemGenerator
from helpers import step, jid

class MultiplyingBinomialsGenerator(ProblemGenerator):
    """
    Generates problems for multiplying two binomials using FOIL.
    (ax + b)(cx + d)
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        # Coeffs
        a = random.randint(-9, 9)
        if a == 0: a = 1
        b = random.randint(-9, 9)
        # Avoid 0 for b to keep it a binomial
        if b == 0: b = random.choice([-1, 1])
        
        c = random.randint(-9, 9)
        if c == 0: c = 1
        d = random.randint(-9, 9)
        if d == 0: d = random.choice([-1, 1])
        
        # Formatting helper
        def fmt_binom(c1, c0):
            t1 = f"{c1}x" if c1 != 1 else "x"
            if c1 == -1: t1 = "-x"
            
            sign = "+" if c0 >= 0 else "-"
            return f"({t1} {sign} {abs(c0)})"
            
        poly1 = fmt_binom(a, b)
        poly2 = fmt_binom(c, d)
        
        problem_str = f"{poly1}{poly2}"
        
        steps = []
        steps.append(step("FOIL_SETUP", problem_str))
        
        # First
        f_val = a * c
        f_str = f"{f_val}x^2" if f_val != 1 else "x^2"
        if f_val == -1: f_str = "-x^2"
        steps.append(step("FOIL_F", f"First: ({a}x) * ({c}x)", f_str))
        
        # Outer
        o_val = a * d
        o_str = f"{o_val}x"
        steps.append(step("FOIL_O", f"Outer: ({a}x) * ({d})", o_str))
        
        # Inner
        i_val = b * c
        i_str = f"{i_val}x"
        steps.append(step("FOIL_I", f"Inner: ({b}) * ({c}x)", i_str))
        
        # Last
        l_val = b * d
        l_str = str(l_val)
        steps.append(step("FOIL_L", f"Last: ({b}) * ({d})", l_str))
        
        # Add (Combine O + I)
        mid_val = o_val + i_val
        mid_str = f"{mid_val}x"
        if mid_val > 0: mid_str = f"+ {mid_val}x"
        elif mid_val < 0: mid_str = f"- {abs(mid_val)}x"
        elif mid_val == 0: mid_str = "" # cancels out
        
        l_sign = f"+ {l_val}" if l_val >= 0 else f"- {abs(l_val)}"
        
        ans = f"{f_str} {mid_str} {l_sign}".strip()
        # Clean up double spaces
        ans = ans.replace("  ", " ")
        if mid_str == "":
            ans = f"{f_str} {l_sign}".strip()
            
        steps.append(step("POLY_COMBINE", f"Combine Like Terms: {o_str} + {i_str} = {mid_val}x"))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="multiply_binomials_foil",
            problem=f"Multiply: {problem_str}",
            steps=steps,
            final_answer=ans
        )
