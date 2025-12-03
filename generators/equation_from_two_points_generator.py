import random
from base_generator import ProblemGenerator
from helpers import step, jid

class EquationFromTwoPointsGenerator(ProblemGenerator):
    """
    Generates problems to find the equation of a line passing through two points.
    Target form: Slope-Intercept (y = mx + b).
    
    Steps:
    1. Find slope m = (y2-y1)/(x2-x1)
    2. Use Point-Slope form: y - y1 = m(x - x1)
    3. Distribute m
    4. Isolate y
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        # Construct points such that slope is likely an integer or simple fraction
        x1 = random.randint(-10, 10)
        y1 = random.randint(-10, 10)
        
        # Decide slope
        slope_num = random.randint(-5, 5)
        slope_den = random.choice([1, 1, 1, 2, 3]) # higher weight on integer slopes
        if slope_den == 0: slope_den = 1
        
        # Calculate x2, y2
        # x2 = x1 + slope_den * k
        k = random.choice([-1, 1, 2])
        x2 = x1 + slope_den * k
        y2 = y1 + slope_num * k
        
        # Recalculate actual slope components just to be safe/standard
        delta_y = y2 - y1
        delta_x = x2 - x1
        
        # Slope m
        if delta_x == 0:
            # Vertical line x = c
            steps = []
            steps.append(step("EQ_2PT_SETUP", f"({x1}, {y1})", f"({x2}, {y2})"))
            steps.append(step("SLOPE_CALC", "x2 = x1", "Undefined slope (Vertical Line)"))
            ans = f"x = {x1}"
            steps.append(step("Z", ans))
            return dict(
                problem_id=jid(),
                operation="equation_from_two_points",
                problem=f"Find the equation of the line passing through ({x1}, {y1}) and ({x2}, {y2})",
                steps=steps,
                final_answer=ans
            )

        # Calculate m for display
        m_val = delta_y / delta_x
        is_int = m_val.is_integer()
        if is_int:
            m_str = str(int(m_val))
            m_num = int(m_val)
            m_den = 1
        else:
            # Simplification logic again or just use fractions module logic manually
            import math
            common = math.gcd(delta_y, delta_x)
            m_num = delta_y // common
            m_den = delta_x // common
            if m_den < 0:
                m_num = -m_num
                m_den = -m_den
            m_str = f"{m_num}/{m_den}"

        problem_str = f"Find the equation of the line passing through ({x1}, {y1}) and ({x2}, {y2})"
        steps = []
        steps.append(step("EQ_2PT_SETUP", f"({x1}, {y1})", f"({x2}, {y2})"))
        
        # Step 1: Slope
        steps.append(step("SLOPE_FORMULA", "m = (y2 - y1) / (x2 - x1)"))
        steps.append(step("SLOPE_SUBST", f"m = ({y2} - {y1}) / ({x2} - {x1})"))
        steps.append(step("SLOPE_RESULT", m_str))
        
        # Step 2: Point-Slope
        # y - y1 = m(x - x1)
        # Handle signs nicely
        y1_op = "-" if y1 >= 0 else "+"
        x1_op = "-" if x1 >= 0 else "+"
        pt_slope = f"y {y1_op} {abs(y1)} = {m_str}(x {x1_op} {abs(x1)})"
        steps.append(step("POINT_SLOPE_SETUP", pt_slope))
        
        # Step 3: Distribute
        # rhs = mx - m*x1
        # m*x1 calculation
        # if m is int:
        rhs_const_num = -m_num * x1
        rhs_const_den = m_den
        
        if m_den == 1:
            term1 = f"{m_str}x"
            term2 = f"{rhs_const_num}" if rhs_const_num < 0 else f"+{rhs_const_num}"
            if rhs_const_num == 0: term2 = ""
            steps.append(step("DIST", m_str, f"(x {x1_op} {abs(x1)})", f"{term1} {term2}".strip()))
            
            # Step 4: Add/Sub y1
            # Final b = rhs_const + y1
            b_final = rhs_const_num + y1
            
            # Show the move
            op_y1 = "add" if y1 > 0 else "subtract" # inverse of left side
            # Wait, if y - 3, we add 3. if y + 3, we subtract 3.
            # y1_op was based on sign. if y1=3 -> y-3. we add 3.
            
            steps.append(step("EQ_OP_BOTH", "add" if y1 > 0 else "subtract", abs(y1), "to isolate y"))
            
            b_sign = "+" if b_final >= 0 else "-"
            ans = f"y = {m_str}x {b_sign} {abs(b_final)}"
            if b_final == 0: ans = f"y = {m_str}x"
            if m_num == 0: ans = f"y = {b_final}"
            
        else:
            # Fraction math for b
            # Distribute: m(x - x1) -> (num/den)x - (num/den)*x1
            term1 = f"{m_str}x"
            c1_num = -m_num * x1 
            # c1 = c1_num / m_den
            
            steps.append(step("DIST", m_str, f"(x {x1_op} {abs(x1)})", f"{term1} + {c1_num}/{m_den}"))
            
            # Combine constant: b = c1 + y1
            # y1 as fraction: (y1 * m_den) / m_den
            y1_scaled = y1 * m_den
            final_num = c1_num + y1_scaled
            
            # simplify final b
            import math
            common_b = math.gcd(final_num, m_den)
            f_num = final_num // common_b
            f_den = m_den // common_b
            
            if f_den == 1:
                b_str = f"{f_num}"
            else:
                b_str = f"{f_num}/{f_den}"
                
            steps.append(step("COMB_CONST", f"{c1_num}/{m_den}", str(y1), b_str))
            
            b_val = final_num / m_den
            b_sign = "+" if b_val >= 0 else "-" # simplistic check
            # formatting b_str might include negative sign
            if f_num < 0:
                b_sign = "-"
                b_str = b_str.replace("-", "") # remove sign for formatted string
            elif f_num == 0:
                b_sign = ""
                b_str = ""
            else:
                b_sign = "+"
            
            # reconstruct
            if b_str:
                ans = f"y = {m_str}x {b_sign} {b_str}"
            else:
                ans = f"y = {m_str}x"
                
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="equation_from_two_points",
            problem=problem_str,
            steps=steps,
            final_answer=ans
        )
