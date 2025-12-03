import random
from base_generator import ProblemGenerator
from helpers import step, jid

class SlopeInterceptFormGenerator(ProblemGenerator):
    """
    Generates problems to identify slope and y-intercept from an equation.
    
    Problem types:
    - Standard: y = mx + b
    - Swapped: y = b + mx
    - Missing b: y = mx
    - Missing m: y = b
    - Implicit coeff: y = x + b, y = -x + b
    
    Steps:
    1. Setup equation
    2. Compare to y = mx + b
    3. Identify m
    4. Identify b
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        m = random.randint(-10, 10)
        b = random.randint(-10, 10)
        
        # Decide format
        fmt = random.choice(['standard', 'swapped', 'no_b', 'horizontal'])
        
        if fmt == 'horizontal':
            m = 0
            # y = b
            equation = f"y = {b}"
            
        elif fmt == 'no_b':
            b = 0
            if m == 0: m = 1 # avoid y=0 which is trivial axis
            # y = mx
            m_str = self._fmt_coeff(m)
            equation = f"y = {m_str}x"
            
        elif fmt == 'swapped':
            if m == 0: m = 1
            if b == 0: b = 1
            # y = b + mx
            m_str = self._fmt_coeff(m)
            # handle sign of m for spacing
            op = "+" if m > 0 else "-"
            m_val_str = f"{abs(m)}x" if abs(m) != 1 else "x"
            equation = f"y = {b} {op} {m_val_str}"
            
        else: # Standard
            if m == 0: m = 1
            # y = mx + b
            m_str = self._fmt_coeff(m)
            op = "+" if b >= 0 else "-"
            equation = f"y = {m_str}x {op} {abs(b)}"

        steps = []
        steps.append(step("SLOPE_INT_SETUP", equation))
        steps.append(step("SLOPE_INT_MATCH", "Compare to Slope-Intercept Form", "y = mx + b"))
        
        # Identify m
        steps.append(step("SLOPE_INT_IDENTIFY", "Slope (m)", str(m)))
        
        # Identify b
        steps.append(step("SLOPE_INT_IDENTIFY", "y-intercept (b)", str(b)))
        
        ans = f"m={m}, b={b}"
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="slope_intercept_identify",
            problem=f"Identify the slope and y-intercept of the line: {equation}",
            steps=steps,
            final_answer=ans
        )

    def _fmt_coeff(self, val):
        if val == 1: return ""
        if val == -1: return "-"
        return str(val)
