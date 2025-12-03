import random
from base_generator import ProblemGenerator
from helpers import step, jid
import math

class SystemsEliminationGenerator(ProblemGenerator):
    """
    Generates systems of linear equations to be solved by elimination.
    
    Difficulty:
    - Simple: Coeffs match or are opposites (e.g., 2x and 2x, or 2x and -2x).
    - Multiply One: One equation needs scaling (e.g., 2x and 4x).
    - Multiply Both: Both need scaling (e.g., 2x and 3x).
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        x_sol = random.randint(-10, 10)
        y_sol = random.randint(-10, 10)
        
        difficulty = random.choice(['simple', 'mult_one', 'mult_both'])
        target_var = random.choice(['x', 'y']) # variable to eliminate
        
        # Coeffs for target var
        if difficulty == 'simple':
            # c1 = c2 or c1 = -c2
            c1 = random.randint(1, 5) * random.choice([-1, 1])
            c2 = c1 if random.random() < 0.5 else -c1
        elif difficulty == 'mult_one':
            # c2 is multiple of c1
            base = random.randint(1, 4) * random.choice([-1, 1])
            factor = random.randint(2, 4) * random.choice([-1, 1])
            c1 = base
            c2 = base * factor
        else:
            # LCM case (e.g. 2 and 3)
            c1 = random.randint(2, 5) * random.choice([-1, 1])
            c2 = random.randint(2, 5) * random.choice([-1, 1])
            # Ensure not multiples
            while c2 % c1 == 0 or c1 % c2 == 0:
                 c2 = random.randint(2, 6) * random.choice([-1, 1])
                 
        # Coeffs for other var (random)
        other_c1 = random.randint(-5, 5)
        if other_c1 == 0: other_c1 = 1
        other_c2 = random.randint(-5, 5)
        if other_c2 == 0: other_c2 = 1
        
        # Ensure independence (determinant check)
        det = c1*other_c2 - c2*other_c1
        while det == 0:
            other_c2 = random.randint(-5, 5)
            if other_c2 == 0: other_c2 = 1
            det = c1*other_c2 - c2*other_c1

        # Assign to A, B, D, E
        if target_var == 'x':
            A, B = c1, other_c1
            D, E = c2, other_c2
        else:
            A, B = other_c1, c1
            D, E = other_c2, c2
            
        # Calc Constants
        C = A * x_sol + B * y_sol
        F = D * x_sol + E * y_sol
        
        # Formatting
        def fmt_eq(a, b, res):
            term_a = f"{a}x"
            term_b = f"{b}y"
            if b >= 0: term_b = f"+ {b}y"
            else: term_b = f"- {abs(b)}y"
            return f"{term_a} {term_b} = {res}"
            
        eq1_str = fmt_eq(A, B, C)
        eq2_str = fmt_eq(D, E, F)
        
        steps = []
        steps.append(step("SYS_SETUP", eq1_str, eq2_str))
        
        # Step 1: Multiply to match
        # Goal: make coeffs of target_var opposites (or same, then subtract)
        # Let's aim for opposites to ADD
        
        # Current coeffs for target: c1, c2
        lcm = abs(c1 * c2) // math.gcd(c1, c2)
        target_val = lcm
        
        # We want Eq1 -> target_val, Eq2 -> -target_val
        mult1 = target_val // c1
        mult2 = -target_val // c2
        
        # Optimization: if c1 = -c2, mults are 1, 1.
        # if c1 = c2, mults are 1, -1.
        
        new_A1, new_B1, new_C1 = A * mult1, B * mult1, C * mult1
        new_D2, new_E2, new_F2 = D * mult2, E * mult2, F * mult2
        
        if mult1 != 1 or mult2 != 1:
            msg = []
            if mult1 != 1: msg.append(f"Eq1 * {mult1}")
            if mult2 != 1: msg.append(f"Eq2 * {mult2}")
            steps.append(step("SYS_MULT", ", ".join(msg)))
            
            # Show new system
            steps.append(step("SYS_REWRITE", fmt_eq(new_A1, new_B1, new_C1), fmt_eq(new_D2, new_E2, new_F2)))
            
        # Step 2: Add
        sum_A = new_A1 + new_D2
        sum_B = new_B1 + new_E2
        sum_C = new_C1 + new_F2
        
        term = f"{sum_A}x" if target_var == 'y' else f"{sum_B}y" # The one that survives
        steps.append(step("SYS_ADD", f"Add equations: {term} = {sum_C}"))
        
        # Step 3: Solve
        coeff = sum_A if target_var == 'y' else sum_B
        
        if coeff != 0:
            val = sum_C // coeff
            res_var = 'x' if target_var == 'y' else 'y'
            steps.append(step("EQ_OP_BOTH", "divide", coeff, res_var, val))
        else:
            # Should not happen with valid det check
            val = 0
            
        # Back subst
        # Plug into Eq1 (A x + B y = C)
        # x_sol, y_sol known
        steps.append(step("SYS_SUBST_BACK", f"Substitute into Eq 1"))
        
        other_val = x_sol if target_var == 'y' else y_sol # The one we just found? 
        # Wait, if target=x, we eliminated x. We found y.
        found_var = 'x' if target_var == 'y' else 'y'
        found_val = x_sol if found_var == 'x' else y_sol
        
        # Show subst
        # A(x) + B(y) = C
        if found_var == 'x':
            # A(val) + By = C
            steps.append(step("CALC", f"{A}({found_val}) + {B}y = {C}"))
            val_term = A * found_val
            steps.append(step("EQ_OP_BOTH", "subtract", val_term, f"{B}y", C - val_term))
            steps.append(step("EQ_OP_BOTH", "divide", B, "y", y_sol))
        else:
            # Ax + B(val) = C
            steps.append(step("CALC", f"{A}x + {B}({found_val}) = {C}"))
            val_term = B * found_val
            steps.append(step("EQ_OP_BOTH", "subtract", val_term, f"{A}x", C - val_term))
            steps.append(step("EQ_OP_BOTH", "divide", A, "x", x_sol))
            
        ans = f"x={x_sol}, y={y_sol}"
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="systems_elimination",
            problem=f"Solve the system by elimination:\n1) {eq1_str}\n2) {eq2_str}",
            steps=steps,
            final_answer=ans
        )
