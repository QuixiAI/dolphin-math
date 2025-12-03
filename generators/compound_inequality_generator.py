import random
from base_generator import ProblemGenerator
from helpers import step, jid

class CompoundInequalityGenerator(ProblemGenerator):
    """
    Generates compound inequalities.
    
    Problem types:
    - AND (Compact): a < bx + c < d
    - OR (Disjoint): bx + c < a OR bx + c > d
    
    Steps:
    1. Setup
    2. Solve (combined or separate)
    3. Final Result
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        problem_type = random.choice(['and_compact', 'or_disjoint'])
        
        # Coefficients
        b = random.choice([1, 1, 2, 3, 4, 5])
        c = random.randint(-10, 10)
        
        # Bounds
        low = random.randint(-10, 5)
        high = random.randint(low + 5, 20)
        
        # inner: bx + c
        if b == 1:
            if c == 0: inner = "x"
            elif c > 0: inner = f"x + {c}"
            else: inner = f"x - {abs(c)}"
        else:
            if c == 0: inner = f"{b}x"
            elif c > 0: inner = f"{b}x + {c}"
            else: inner = f"{b}x - {abs(c)}"
            
        steps = []
        
        if problem_type == 'and_compact':
            # a < bx + c < d
            # Ensure nice integer solutions if possible, but fractions are ok
            # Let's try to construct it backwards for integers sometimes
            if random.random() < 0.7:
                sol_low = random.randint(-5, 5)
                sol_high = random.randint(sol_low + 2, 10)
                # Reconstruct bounds
                # low < x < high
                # low*b + c < bx + c < high*b + c
                low = sol_low * b + c
                high = sol_high * b + c
            
            problem_str = f"{low} < {inner} < {high}"
            steps.append(step("COMP_INEQ_SETUP", problem_str))
            
            curr_low, curr_high = low, high
            
            # Step 1: Remove c
            if c != 0:
                op = "subtract" if c > 0 else "add"
                val = abs(c)
                if c > 0:
                    curr_low -= val
                    curr_high -= val
                else:
                    curr_low += val
                    curr_high += val
                
                term_middle = f"{b}x" if b != 1 else "x"
                steps.append(step("INEQ_OP_ALL", op, val, f"{curr_low} < {term_middle} < {curr_high}"))
                
            # Step 2: Divide by b
            if b != 1:
                # Format fractions
                l_str = str(curr_low // b) if curr_low % b == 0 else f"{curr_low}/{b}"
                h_str = str(curr_high // b) if curr_high % b == 0 else f"{curr_high}/{b}"
                steps.append(step("INEQ_OP_ALL", "divide", b, f"{l_str} < x < {h_str}"))
                ans = f"{l_str} < x < {h_str}"
            else:
                ans = f"{curr_low} < x < {curr_high}"
                
            steps.append(step("Z", ans))
            return self._pack(problem_str, steps, ans)
            
        else:
            # OR case: bx + c < low OR bx + c > high
            # Construct integer solutions likely
            if random.random() < 0.7:
                sol_low = random.randint(-10, 0)
                sol_high = random.randint(sol_low + 5, 10)
                # x < sol_low OR x > sol_high
                # bx + c < sol_low*b + c
                low = sol_low * b + c
                high = sol_high * b + c
                
            prob1 = f"{inner} < {low}"
            prob2 = f"{inner} > {high}"
            problem_str = f"{prob1} OR {prob2}"
            steps.append(step("COMP_INEQ_SETUP", problem_str))
            
            # Solve Part 1
            sol1 = self._solve_part(b, c, low, '<')
            steps.append(step("COMP_INEQ_PART", "Part 1", f"{prob1} -> {sol1}"))
            
            # Solve Part 2
            sol2 = self._solve_part(b, c, high, '>')
            steps.append(step("COMP_INEQ_PART", "Part 2", f"{prob2} -> {sol2}"))
            
            ans = f"{sol1} OR {sol2}"
            steps.append(step("Z", ans))
            return self._pack(problem_str, steps, ans)

    def _solve_part(self, b, c, rhs, op):
        # bx + c op rhs
        curr = rhs
        if c != 0:
            if c > 0: curr -= c
            else: curr += abs(c)
            
        if b != 1:
            if curr % b == 0:
                val = curr // b
                return f"x {op} {val}"
            else:
                return f"x {op} {curr}/{b}"
        else:
            return f"x {op} {curr}"

    def _pack(self, prob, steps, ans):
        return dict(
            problem_id=jid(),
            operation="compound_inequality",
            problem=f"Solve: {prob}",
            steps=steps,
            final_answer=ans
        )
