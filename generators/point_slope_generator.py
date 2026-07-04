import random
from base_generator import ProblemGenerator
from helpers import step, jid


def sfrac(num, den):
    """Signed reduced fraction string: (4, 2) -> '2', (-5, 3) -> '-5/3'."""
    import math
    g = math.gcd(num, den)
    n, d = num // g, den // g
    if d < 0:
        n, d = -n, -d
    return str(n) if d == 1 else f"{n}/{d}"


def const_term(num, den):
    """' + c' / ' - c' continuation for a fraction constant; '' when zero."""
    if num == 0:
        return ""
    text = sfrac(abs(num), den)
    return f" + {text}" if num > 0 else f" - {text}"


class PointSlopeGenerator(ProblemGenerator):
    """
    Generates problems involving Point-Slope form.
    
    Task: Given a point (x1, y1) and slope m, write the equation in Slope-Intercept form (y = mx + b).
    (Or start with the equation already written).
    
    Steps:
    1. Setup Point-Slope equation: y - y1 = m(x - x1)
    2. Distribute m
    3. Add/Subtract y1 to isolate y
    4. Combine constants
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        # Generate components (nonzero so 'y - 0' / '(x - 0)' never appear)
        x1 = random.choice([v for v in range(-10, 11) if v != 0])
        y1 = random.choice([v for v in range(-10, 11) if v != 0])
        
        # Slope (integer or simple fraction)
        if random.random() < 0.7:
            m_num = random.randint(-5, 5)
            m_den = 1
            if m_num == 0: m_num = 1 # Avoid trivial horizontal for this exercise usually
        else:
            m_num = random.randint(-5, 5)
            m_den = random.choice([2, 3, 4, 5])
            if m_num == 0: m_num = 1
            
        # Format m string
        if m_den == 1:
            m_str = str(m_num)
        else:
            m_str = f"{m_num}/{m_den}"
            
        # Setup string
        y1_op = "-" if y1 >= 0 else "+"
        x1_op = "-" if x1 >= 0 else "+"
        
        equation = f"y {y1_op} {abs(y1)} = {m_str}(x {x1_op} {abs(x1)})"
        
        steps = []
        steps.append(step("POINT_SLOPE_SETUP", equation))
        steps.append(step("GOAL", "Convert to Slope-Intercept Form (y = mx + b)"))
        
        # Distribute
        # rhs = m*x - m*x1
        term1 = f"{m_str}x"
        c1_num = -m_num * x1
        
        # Display distribution
        if m_den == 1:
            steps.append(step("DIST", m_str, f"(x {x1_op} {abs(x1)})", f"{term1}{const_term(c1_num, 1)}"))
            
            # Move y1
            steps.append(step("EQ_OP_NOTE", "add" if y1 > 0 else "subtract", abs(y1), "to isolate y"))
            
            b_final = c1_num + y1
            
            b_sign = "+" if b_final >= 0 else "-"
            ans = f"y = {m_str}x {b_sign} {abs(b_final)}"
            if b_final == 0: ans = f"y = {m_str}x"
            
        else:
            # Fraction math
            # c1 = c1_num / m_den
            steps.append(step("DIST", m_str, f"(x {x1_op} {abs(x1)})", f"{term1}{const_term(c1_num, m_den)}"))
            
            # Move y1
            steps.append(step("EQ_OP_NOTE", "add" if y1 > 0 else "subtract", abs(y1), "to isolate y"))
            
            # Combine: c1 + y1
            # y1 = (y1 * m_den) / m_den
            y1_scaled = y1 * m_den
            final_num = c1_num + y1_scaled
            
            # Simplify fraction
            import math
            common = math.gcd(final_num, m_den)
            f_num = final_num // common
            f_den = m_den // common
            
            if f_den < 0: # normalize sign
                f_num = -f_num
                f_den = -f_den
                
            if f_den == 1:
                b_str = f"{f_num}"
            else:
                b_str = f"{f_num}/{f_den}"
                
            b_val = final_num / m_den
            
            # Formatting
            if f_num == 0:
                ans = f"y = {m_str}x"
            elif f_num > 0:
                ans = f"y = {m_str}x + {b_str}"
            else:
                ans = f"y = {m_str}x - {abs(f_num)}/{f_den}" if f_den != 1 else f"y = {m_str}x - {abs(f_num)}"
                
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="point_slope_convert",
            problem=f"Convert to Slope-Intercept Form: {equation}",
            steps=steps,
            final_answer=ans
        )
