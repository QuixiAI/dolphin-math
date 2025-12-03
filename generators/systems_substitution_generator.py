import random
from base_generator import ProblemGenerator
from helpers import step, jid

class SystemsSubstitutionGenerator(ProblemGenerator):
    """
    Generates systems of linear equations to be solved by substitution.
    
    Structure:
    Eq1: ax + by = c
    Eq2: dx + ey = f
    
    At least one variable will have coeff 1 or -1 to make substitution natural.
    Or one equation will be given as y = ... or x = ...
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        # Construct integer solution
        x_sol = random.randint(-10, 10)
        y_sol = random.randint(-10, 10)
        
        # Decide format: 
        # Type 1: y = mx + b (already isolated)
        # Type 2: x + by = c (easy to isolate)
        
        type_choice = random.choice(['isolated', 'easy_isolate'])
        
        steps = []
        
        if type_choice == 'isolated':
            # Eq1: y = ax + b (or x = ay + b)
            # Eq2: cx + dy = e
            
            # Decide isolating x or y
            target_var = random.choice(['x', 'y'])
            other_var = 'y' if target_var == 'x' else 'x'
            
            # Coeffs for Eq1
            a1 = random.randint(-5, 5)
            if a1 == 0: a1 = 1
            b1 = x_sol if target_var == 'x' else y_sol
            # Wait, x = ay + b. 
            # If target=x: x = a1*y + b1_const
            # x_sol = a1*y_sol + b1_const -> b1_const = x_sol - a1*y_sol
            
            val_target = x_sol if target_var == 'x' else y_sol
            val_other = y_sol if target_var == 'x' else x_sol
            
            b1_const = val_target - a1 * val_other
            
            # Format Eq1
            rhs1 = f"{a1}{other_var}"
            if b1_const != 0:
                op = "+" if b1_const > 0 else "-"
                rhs1 += f" {op} {abs(b1_const)}"
            elif a1 == 0: # covered by check
                pass
            
            if a1 == 1: rhs1 = rhs1.replace("1"+other_var, other_var)
            if a1 == -1: rhs1 = rhs1.replace("-1"+other_var, "-"+other_var)
                
            eq1_str = f"{target_var} = {rhs1}"
            
            # Eq2: cx + dy = e
            c2 = random.randint(-5, 5)
            d2 = random.randint(-5, 5)
            if c2 == 0 and d2 == 0: c2 = 1
            
            e2 = c2 * x_sol + d2 * y_sol
            
            # Format Eq2
            term_x = f"{c2}x" if c2 != 0 else ""
            term_y = f"{d2}y" if d2 != 0 else ""
            
            # Sign handling for display
            if d2 > 0 and c2 != 0: term_y = f"+ {d2}y"
            elif d2 < 0: term_y = f"- {abs(d2)}y"
            elif d2 == 0: term_y = ""
            
            eq2_str = f"{term_x} {term_y} = {e2}".strip()
            
            steps.append(step("SYS_SETUP", eq1_str, eq2_str))
            
            # Step 1: Subst
            steps.append(step("SYS_SUBST", f"Substitute ({rhs1}) for {target_var} in Eq 2"))
            
            # Form expression in Eq2
            # e.g., c2(rhs1) + d2y = e2
            if target_var == 'x':
                subst_expr = f"{c2}({rhs1}) {term_y} = {e2}".strip()
            else:
                subst_expr = f"{term_x} {d2}({rhs1}) = {e2}".strip() # kinda messy formatting
                # Standardize: always simplify formatting in code or just output raw
                # Let's try to be clean
                if c2 != 0:
                    prefix = f"{c2}x "
                    if d2 > 0: prefix += "+ "
                    elif d2 < 0: prefix += "- " # abs handled in subst?
                    # If d2 is neg, eq2 was cx - |d|y.
                    # subst: cx - |d|(...)
                    pass
                
            # Let's stick to a simpler representation for the step text
            steps.append(step("SYS_EQ_NEW", f"New equation with {other_var} only"))
            
            # Expand and solve
            # We assume the user/model follows algebra.
            # We can output the simplified linear equation
            # (c2*a1 + d2)y = ...
            
            if target_var == 'x':
                # c2(a1*y + b1) + d2*y = e2
                # (c2*a1 + d2)y + c2*b1 = e2
                new_coeff = c2 * a1 + d2
                new_const = c2 * b1_const
                
                # Check if 0
                steps.append(step("DIST_COMBINE", f"{new_coeff}{other_var} + {new_const} = {e2}"))
                
                # Solve linear
                rhs_final = e2 - new_const
                steps.append(step("EQ_OP_BOTH", "subtract", new_const, f"{new_coeff}{other_var}", rhs_final))
                
                if new_coeff != 0:
                    res_other = rhs_final // new_coeff
                    steps.append(step("EQ_OP_BOTH", "divide", new_coeff, other_var, res_other))
                else:
                    res_other = 0 # degenerate?
            else:
                # target is y. x + d2(a1*x + b1) = e2
                # c2*x + d2*a1*x + d2*b1 = e2
                # (c2 + d2*a1)x + d2*b1 = e2
                new_coeff = c2 + d2 * a1
                new_const = d2 * b1_const
                
                steps.append(step("DIST_COMBINE", f"{new_coeff}{other_var} + {new_const} = {e2}"))
                
                rhs_final = e2 - new_const
                steps.append(step("EQ_OP_BOTH", "subtract", new_const, f"{new_coeff}{other_var}", rhs_final))
                
                if new_coeff != 0:
                    res_other = rhs_final // new_coeff
                    steps.append(step("EQ_OP_BOTH", "divide", new_coeff, other_var, res_other))
            
            # Step Back-Subst
            steps.append(step("SYS_SUBST_BACK", f"Substitute {other_var}={val_other} into Eq 1"))
            steps.append(step("CALC", f"{target_var} = {val_target}"))
            
            ans = f"x={x_sol}, y={y_sol}"
            steps.append(step("Z", ans))
            
            return dict(
                problem_id=jid(),
                operation="systems_substitution",
                problem=f"Solve the system:\n1) {eq1_str}\n2) {eq2_str}",
                steps=steps,
                final_answer=ans
            )

        else:
            # Type 2: easy isolate
            # Eq1: x + by = c (coeff 1)
            # Eq2: dx + ey = f
            # Just create isolated setup then pretend it wasn't
            
            # Let's just forward to isolated logic but add a "ISOLATE" step at start
            # Generate as isolated: x = ...
            # Then rewrite Eq1 as x - ... = ...
            
            # Delegate/Recursion? No, just copy logic.
            
            # Let's assume x + y = c for simplicity 50%
            a1 = 1
            b1 = random.randint(-5, 5)
            c1 = x_sol + b1 * y_sol
            
            term_y = f"{b1}y"
            if b1 > 0: term_y = f"+ {b1}y"
            elif b1 < 0: term_y = f"- {abs(b1)}y"
            elif b1 == 0: term_y = ""
            
            eq1_str = f"x {term_y} = {c1}"
            
            # Eq2
            c2 = random.randint(-5, 5)
            d2 = random.randint(-5, 5)
            e2 = c2 * x_sol + d2 * y_sol
            
            term_x2 = f"{c2}x"
            term_y2 = f"{d2}y"
            if d2 >= 0: term_y2 = f"+ {d2}y"
            
            eq2_str = f"{term_x2} {term_y2} = {e2}"
            
            steps.append(step("SYS_SETUP", eq1_str, eq2_str))
            
            # Step Isolate
            # x = c1 - b1y
            rhs_iso = f"{c1} + {-b1}y" # raw
            # nice format
            rhs_iso = f"{-b1}y + {c1}"
            steps.append(step("SYS_ISOLATE", "Isolate x in Eq 1", f"x = {rhs_iso}"))
            
            # Substitute into Eq 2
            steps.append(step("SYS_SUBST", f"Substitute x in Eq 2"))
            
            # Solve
            # c2(x) + d2y = e2
            # c2(-b1y + c1) + d2y = e2
            # (-c2*b1 + d2)y + c2*c1 = e2
            new_coeff = -c2 * b1 + d2
            new_const = c2 * c1
            
            steps.append(step("DIST_COMBINE", f"{new_coeff}y + {new_const} = {e2}"))
            
            # Solve linear
            rhs_final = e2 - new_const
            steps.append(step("EQ_OP_BOTH", "subtract", new_const, f"{new_coeff}y", rhs_final))
            
            if new_coeff != 0:
                y_res = rhs_final // new_coeff
                steps.append(step("EQ_OP_BOTH", "divide", new_coeff, "y", y_res))
            
            # Back subst
            steps.append(step("SYS_SUBST_BACK", f"Substitute y={y_sol} into x = {rhs_iso}"))
            steps.append(step("CALC", f"x = {x_sol}"))
            
            ans = f"x={x_sol}, y={y_sol}"
            steps.append(step("Z", ans))
            
            return dict(
                problem_id=jid(),
                operation="systems_substitution",
                problem=f"Solve the system:\n1) {eq1_str}\n2) {eq2_str}",
                steps=steps,
                final_answer=ans
            )
