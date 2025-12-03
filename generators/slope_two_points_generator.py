import random
from base_generator import ProblemGenerator
from helpers import step, jid

class SlopeTwoPointsGenerator(ProblemGenerator):
    """
    Generates problems to find the slope between two points (x1, y1) and (x2, y2).
    
    Formula: m = (y2 - y1) / (x2 - x1)
    
    Steps:
    1. Setup points
    2. Show formula
    3. Substitute values
    4. Calculate numerator (delta y)
    5. Calculate denominator (delta x)
    6. Simplify fraction/divide
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        x1 = random.randint(-10, 10)
        y1 = random.randint(-10, 10)
        
        # Ensure x2 is different from x1 most of the time to avoid undefined too often
        # But include some vertical lines (10% chance)
        if random.random() < 0.1:
            x2 = x1
        else:
            x2 = random.choice([x for x in range(-10, 11) if x != x1])
            
        # Same for y2, 10% chance of horizontal line if not vertical
        if x1 != x2 and random.random() < 0.1:
            y2 = y1
        else:
            y2 = random.randint(-10, 10)
            
        problem_str = f"Find the slope of the line passing through ({x1}, {y1}) and ({x2}, {y2})"
        steps = []
        steps.append(step("SLOPE_SETUP", f"({x1}, {y1})", f"({x2}, {y2})"))
        steps.append(step("SLOPE_FORMULA", "m = (y2 - y1) / (x2 - x1)"))
        
        # Substitution
        subst_str = f"m = ({y2} - {y1}) / ({x2} - {x1})"
        # Be mindful of double negatives for display clarity
        y1_str = f"({y1})" if y1 < 0 else str(y1)
        x1_str = f"({x1})" if x1 < 0 else str(x1)
        # Maybe clearer: m = (y2 - y1) / (x2 - x1)
        # Let's format it nicely
        steps.append(step("SLOPE_SUBST", f"m = ({y2} - {y1_str}) / ({x2} - {x1_str})"))
        
        # Calculate diffs
        delta_y = y2 - y1
        delta_x = x2 - x1
        
        steps.append(step("S", y2, y1, delta_y))
        steps.append(step("S", x2, x1, delta_x))
        
        if delta_x == 0:
            steps.append(step("SLOPE_UNDEFINED", "Division by zero"))
            ans = "Undefined"
        else:
            # Simplify fraction
            # Reuse logic or standard math
            if delta_y == 0:
                steps.append(step("D", 0, delta_x, 0))
                ans = "0"
            elif delta_y % delta_x == 0:
                val = delta_y // delta_x
                steps.append(step("D", delta_y, delta_x, val))
                ans = str(val)
            else:
                # Reduce fraction
                import math
                common = math.gcd(delta_y, delta_x)
                num = delta_y // common
                den = delta_x // common
                
                # Handle negative denominator standard (put negative on top or front)
                if den < 0:
                    num = -num
                    den = -den
                    
                steps.append(step("F", f"{delta_y}/{delta_x}", f"{num}/{den}"))
                ans = f"{num}/{den}"
        
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="slope_two_points",
            problem=problem_str,
            steps=steps,
            final_answer=ans
        )
