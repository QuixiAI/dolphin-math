import random
from base_generator import ProblemGenerator
from helpers import step, jid

class ParallelPerpendicularLineGenerator(ProblemGenerator):
    """
    Generates problems to find the equation of a line parallel or perpendicular 
    to a given line, passing through a specific point.
    
    Steps:
    1. Identify slope of given line (m1)
    2. Determine new slope (m2):
       - Parallel: m2 = m1
       - Perpendicular: m2 = -1/m1
    3. Use Point-Slope form with new point (x1, y1) and m2
    4. Convert to Slope-Intercept
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        relation = random.choice(['parallel', 'perpendicular'])
        
        # Given Point (x1, y1)
        x1 = random.randint(-10, 10)
        y1 = random.randint(-10, 10)
        
        # Given Line: y = mx + b or Ax + By = C?
        # Let's stick to y = mx + b for clarity in this specific skill, 
        # or mix it up. Let's do y = mx + b for 80% simplicity.
        # Construct m1 such that m2 is nice (integer or simple fraction)
        
        if relation == 'parallel':
            # m2 = m1. Make m1 simple.
            m1_num = random.randint(-5, 5)
            m1_den = random.choice([1, 1, 2, 3])
            if m1_num == 0: m1_num = 1 # avoid horizontal for now unless specifically testing
        else:
            # m2 = -1/m1. Make m1 such that its reciprocal is simple-ish.
            # actually we want m2 to be the simple one usually for the point-slope math.
            m2_num = random.randint(-5, 5)
            m2_den = random.choice([1, 1, 2, 3])
            if m2_num == 0: m2_num = 1
            
            # So m1 is negative reciprocal of m2
            # m1 = -m2_den / m2_num
            m1_num = -m2_den
            m1_den = m2_num
            # Normalize sign
            if m1_den < 0:
                m1_num = -m1_num
                m1_den = -m1_den
                
        # Given line equation string
        b_given = random.randint(-10, 10)
        m1_str = self._fmt_frac(m1_num, m1_den)
        b_given_sign = "+" if b_given >= 0 else "-"
        given_line = f"y = {m1_str}x {b_given_sign} {abs(b_given)}"
        if b_given == 0: given_line = f"y = {m1_str}x"
        
        problem_str = f"Find the equation of the line {relation} to {given_line} that passes through ({x1}, {y1})"
        
        steps = []
        steps.append(step("LINE_RELATION_SETUP", relation, given_line, f"({x1}, {y1})"))
        
        # Step 1: Identify Slope
        steps.append(step("FIND_SLOPE", "Given slope (m1)", m1_str))
        
        # Step 2: New Slope
        if relation == 'parallel':
            m2_num, m2_den = m1_num, m1_den
            m2_str = m1_str
            reason = "Parallel lines have the same slope"
        else:
            # Perpendicular
            # m2 = -1 / m1
            # Flip fraction and change sign
            m2_num = -m1_den
            m2_den = m1_num
            if m2_den < 0:
                m2_num = -m2_num
                m2_den = -m2_den
            m2_str = self._fmt_frac(m2_num, m2_den)
            reason = "Perpendicular lines have negative reciprocal slopes"
            
        steps.append(step("NEW_SLOPE", f"New slope (m2) = {m2_str}", reason))
        
        # Step 3: Point-Slope to Slope-Intercept
        # y - y1 = m2(x - x1)
        # Reuse logic from EquationFromTwoPoints or PointSlope
        # y = m2x - m2*x1 + y1
        
        # c1 = -m2 * x1
        c1_num = -m2_num * x1
        c1_den = m2_den
        
        # b_final = c1 + y1
        y1_scaled = y1 * c1_den
        b_final_num = c1_num + y1_scaled
        b_final_den = c1_den
        
        # Simplify b
        import math
        common = math.gcd(b_final_num, b_final_den)
        b_num = b_final_num // common
        b_den = b_final_den // common
        
        if b_den < 0:
            b_num = -b_num
            b_den = -b_den
            
        b_str = self._fmt_frac(b_num, b_den, is_coeff=False)
        
        # Construct steps for visible work
        y1_op = "-" if y1 >= 0 else "+"
        x1_op = "-" if x1 >= 0 else "+"
        pt_slope_eq = f"y {y1_op} {abs(y1)} = {m2_str}(x {x1_op} {abs(x1)})"
        steps.append(step("POINT_SLOPE_SETUP", pt_slope_eq))
        
        # Distribute
        dist_term = f"{m2_str}x"
        
        # Constant from distribution
        # -m2*x1
        dist_const_num = -m2_num * x1
        dist_const_den = m2_den
        dist_const_str = self._fmt_frac(dist_const_num, dist_const_den, is_coeff=False)
        if not dist_const_str.startswith("-"): dist_const_str = "+" + dist_const_str
        
        steps.append(step("DIST", m2_str, f"(x {x1_op} {abs(x1)})", f"{dist_term} {dist_const_str}".strip()))
        
        # Move y1
        steps.append(step("EQ_OP_BOTH", "add" if y1 > 0 else "subtract", abs(y1), "to isolate y"))
        
        # Final formatting
        if b_num == 0:
            ans = f"y = {m2_str}x"
        elif b_num > 0:
            ans = f"y = {m2_str}x + {b_str}"
        else:
            ans = f"y = {m2_str}x - {abs(b_num)}" if b_den == 1 else f"y = {m2_str}x - {abs(b_num)}/{b_den}"
            
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="parallel_perpendicular_line",
            problem=problem_str,
            steps=steps,
            final_answer=ans
        )

    def _fmt_frac(self, num, den, is_coeff=True):
        if den == 0: return "undef"
        if num == 0: return "0"
        if den == 1:
            if is_coeff and num == 1: return ""
            if is_coeff and num == -1: return "-"
            return str(num)
        
        # Simplify display only? No, assume mostly simplified inputs from logic
        return f"{num}/{den}"
