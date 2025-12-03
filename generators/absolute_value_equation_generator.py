import random
from base_generator import ProblemGenerator
from helpers import step, jid

class AbsoluteValueEquationGenerator(ProblemGenerator):
    """
    Generates absolute value equations: |ax + b| = c
    
    Problem types:
    - Simple: |x| = c
    - Linear inside: |x + b| = c
    - Linear coeff: |ax + b| = c
    
    Steps:
    1. Setup equation
    2. Split into positive and negative cases (if c > 0)
    3. Solve Case 1
    4. Solve Case 2
    5. Combine solutions
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        # Determine problem structure: |ax + b| = c
        # 80% chance of c > 0 (two solutions)
        # 10% chance of c = 0 (one solution)
        # 10% chance of c < 0 (no solution)
        
        outcome = random.choices(['two_sol', 'one_sol', 'no_sol'], weights=[80, 10, 10])[0]
        
        a = random.choice([1, 1, 1, 2, 3, 4, 5]) # Weigh 1 higher for simpler problems
        b = random.randint(-10, 10)
        
        if outcome == 'two_sol':
            c = random.randint(1, 20)
        elif outcome == 'one_sol':
            c = 0
        else:
            c = random.randint(-10, -1)
            
        # Format the inner expression ax + b
        if a == 1:
            if b == 0:
                inner = "x"
            elif b > 0:
                inner = f"x + {b}"
            else:
                inner = f"x - {abs(b)}"
        else:
            if b == 0:
                inner = f"{a}x"
            elif b > 0:
                inner = f"{a}x + {b}"
            else:
                inner = f"{a}x - {abs(b)}"
                
        equation = f"|{inner}| = {c}"
        steps = []
        steps.append(step("ABS_SETUP", equation))
        
        if c < 0:
            steps.append(step("ABS_CHECK", f"{c} < 0", "Absolute value cannot be negative"))
            steps.append(step("Z", "No solution"))
            return dict(
                problem_id=jid(),
                operation="absolute_value_eq",
                problem=f"Solve: {equation}",
                steps=steps,
                final_answer="No solution"
            )
            
        if c == 0:
            steps.append(step("ABS_SPLIT", "Single case", f"{inner} = 0"))
            # Solve ax + b = 0
            # Reuse logic or just manually step it since it's simple linear
            curr_b = b
            curr_rhs = 0
            
            # Step 1: Remove b
            if b != 0:
                op = "subtract" if b > 0 else "add"
                val = abs(b)
                steps.append(step("EQ_OP_BOTH", op, val, f"{a}x" if a > 1 else "x", -b))
                curr_rhs = -b
                
            # Step 2: Remove a
            if a != 1:
                # check divisibility
                res_val = curr_rhs / a
                if res_val.is_integer():
                    res_val = int(res_val)
                    steps.append(step("EQ_OP_BOTH", "divide", a, "x", res_val))
                    sol = str(res_val)
                else:
                    steps.append(step("EQ_OP_BOTH", "divide", a, "x", f"{curr_rhs}/{a}"))
                    sol = f"{curr_rhs}/{a}"
            else:
                sol = str(curr_rhs)
                
            steps.append(step("Z", f"x = {sol}"))
            return dict(
                problem_id=jid(),
                operation="absolute_value_eq",
                problem=f"Solve: {equation}",
                steps=steps,
                final_answer=f"x = {sol}"
            )

        # Two solutions case
        steps.append(step("ABS_SPLIT", "Two cases", f"{inner} = {c}", f"{inner} = -{c}"))
        
        solutions = []
        
        # Case 1
        steps.append(step("ABS_CASE", "Case 1", f"{inner} = {c}"))
        sol1 = self._solve_linear_steps(a, b, c, steps)
        solutions.append(sol1)
        
        # Case 2
        steps.append(step("ABS_CASE", "Case 2", f"{inner} = -{c}"))
        sol2 = self._solve_linear_steps(a, b, -c, steps)
        solutions.append(sol2)
        
        final_ans = f"x = {solutions[0]}, x = {solutions[1]}"
        steps.append(step("Z", final_ans))
        
        return dict(
            problem_id=jid(),
            operation="absolute_value_eq",
            problem=f"Solve: {equation}",
            steps=steps,
            final_answer=final_ans
        )

    def _solve_linear_steps(self, a, b, rhs, steps):
        """
        Helper to generate steps for ax + b = rhs
        Returns the solution string.
        """
        # ax + b = rhs
        
        # Step 1: Handle b
        curr_rhs = rhs
        if b != 0:
            op = "subtract" if b > 0 else "add"
            val = abs(b)
            # new rhs
            if op == "subtract":
                curr_rhs = curr_rhs - val
            else:
                curr_rhs = curr_rhs + val
                
            steps.append(step("EQ_OP_BOTH", op, val, f"{a}x" if a != 1 else "x", curr_rhs))
        
        # Step 2: Handle a
        if a != 1:
            if curr_rhs % a == 0:
                val = curr_rhs // a
                steps.append(step("EQ_OP_BOTH", "divide", a, "x", val))
                return str(val)
            else:
                # Fraction
                steps.append(step("EQ_OP_BOTH", "divide", a, "x", f"{curr_rhs}/{a}"))
                return f"{curr_rhs}/{a}"
        else:
            return str(curr_rhs)
