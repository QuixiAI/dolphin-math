import random
from base_generator import ProblemGenerator
from helpers import step, jid
import math

class StandardFormConversionGenerator(ProblemGenerator):
    """
    Generates problems converting between Standard Form (Ax + By = C) and Slope-Intercept Form (y = mx + b).
    
    Directions:
    1. Standard -> Slope-Intercept (Solve for y)
    2. Slope-Intercept -> Standard (Rearrange to Ax + By = C, integer coeffs)
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        direction = random.choice(['to_slope_intercept', 'to_standard'])
        
        if direction == 'to_slope_intercept':
            # Ax + By = C
            # Ensure B != 0
            A = random.randint(-9, 9)
            if A == 0: A = 1
            B = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            C = random.randint(-20, 20)
            
            # Form equation
            # Ax + By = C
            op_b = "+" if B >= 0 else "-"
            term_a = f"{A}x"
            term_b = f"{abs(B)}y"
            equation = f"{term_a} {op_b} {term_b} = {C}"
            
            steps = []
            steps.append(step("EQ_SETUP", equation))
            steps.append(step("GOAL", "Convert to Slope-Intercept Form (y = mx + b)"))
            
            # Step 1: Move Ax
            op_move = "subtract" if A > 0 else "add"
            val_move = abs(A)
            
            term_b_signed = f"{B}y"
            rhs_step1 = f"{-A}x + {C}" if C >= 0 else f"{-A}x - {abs(C)}"
            
            steps.append(step("MOVE_TERM", f"{term_a}", "to right side", f"{term_b_signed} = {rhs_step1}"))
            
            # Step 2: Divide by B
            steps.append(step("EQ_OP_BOTH", "divide", B, "to isolate y"))
            
            # Simplify fractions
            # m = -A/B
            # b = C/B
            
            common_m = math.gcd(-A, B)
            m_num = -A // common_m
            m_den = B // common_m
            if m_den < 0:
                m_num = -m_num
                m_den = -m_den
            
            if m_den == 1:
                m_str = f"{m_num}"
            else:
                m_str = f"{m_num}/{m_den}"
                
            common_b = math.gcd(C, B)
            b_num = C // common_b
            b_den = B // common_b
            if b_den < 0:
                b_num = -b_num
                b_den = -b_den
                
            if b_den == 1:
                b_str = f"{b_num}"
            else:
                b_str = f"{b_num}/{b_den}"
                
            # Construct final string
            # y = m_str x + b_str
            # Handle b sign
            if b_num == 0:
                b_part = ""
            elif b_num > 0:
                b_part = f" + {b_str}"
            else:
                # b_str has negative sign if den=1?
                # if fraction, num is negative.
                if b_den == 1:
                    b_part = f" - {abs(b_num)}"
                else:
                    b_part = f" - {abs(b_num)}/{b_den}"
            
            ans = f"y = {m_str}x{b_part}"
            if m_num == 0: ans = f"y ={b_part}"
            
            steps.append(step("Z", ans))
            
            return dict(
                problem_id=jid(),
                operation="standard_to_slope_intercept",
                problem=f"Convert to Slope-Intercept Form: {equation}",
                steps=steps,
                final_answer=ans
            )
            
        else:
            # Slope-Intercept -> Standard
            # y = (n/d)x + b
            
            m_num = random.randint(-5, 5)
            m_den = random.choice([1, 2, 3, 4, 5])
            if m_num == 0: m_num = 1
            
            b_num = random.randint(-10, 10)
            b_den = random.choice([1, 2, 3, 4, 5]) # allow different denominators
            
            # Formulate y = mx + b
            if m_den == 1: m_str = f"{m_num}"
            else: m_str = f"{m_num}/{m_den}"
            
            if b_den == 1: b_str = f"{b_num}"
            else: b_str = f"{b_num}/{b_den}"
            
            rhs = f"{m_str}x + {b_str}".replace("+ -", "- ")
            equation = f"y = {rhs}"
            
            steps = []
            steps.append(step("EQ_SETUP", equation))
            steps.append(step("GOAL", "Convert to Standard Form (Ax + By = C, integers)"))
            
            # Step 1: Clear fractions (LCM of denoms)
            lcm = (m_den * b_den) // math.gcd(m_den, b_den)
            
            if lcm > 1:
                steps.append(step("EQ_OP_BOTH", "multiply", lcm, "to clear fractions"))
                
                # New coeffs
                term_y = f"{lcm}y"
                new_A = m_num * (lcm // m_den)
                new_C = b_num * (lcm // b_den)
                
                rhs_cleared = f"{new_A}x + {new_C}".replace("+ -", "- ")
                steps.append(step("REWRITE", f"{term_y} = {rhs_cleared}"))
            else:
                lcm = 1
                term_y = "y"
                new_A = m_num
                new_C = b_num
                
            # Step 2: Move Ax to left
            # We want Ax + By = C
            # Currently: By = Ax + C
            # -> -Ax + By = C
            
            steps.append(step("MOVE_TERM", f"{new_A}x", "to left side", f"{-new_A}x + {term_y} = {new_C}".replace("+ -", "- ")))
            
            curr_A = -new_A
            curr_B = lcm
            curr_C = new_C
            
            # Step 3: Ensure A is positive (standard convention often prefers A >= 0)
            if curr_A < 0:
                steps.append(step("EQ_OP_BOTH", "multiply", -1, "to make A positive"))
                curr_A = -curr_A
                curr_B = -curr_B
                curr_C = -curr_C
                
            # Construct final
            term_A = f"{curr_A}x" if curr_A != 1 else "x"
            if curr_A == 0: term_A = "" # unlikely with logic above but possible if m=0
            
            op_B = "+" if curr_B >= 0 else "-"
            term_B = f"{abs(curr_B)}y" if abs(curr_B) != 1 else "y"
            
            ans = f"{term_A} {op_B} {term_B} = {curr_C}".strip()
            if term_A == "": ans = f"{op_B}{term_B} = {curr_C}".strip() # handle leading sign if no x
            
            steps.append(step("Z", ans))
            
            return dict(
                problem_id=jid(),
                operation="slope_intercept_to_standard",
                problem=f"Convert to Standard Form: {equation}",
                steps=steps,
                final_answer=ans
            )
