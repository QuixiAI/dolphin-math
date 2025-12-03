import random
from base_generator import ProblemGenerator
from helpers import step, jid

class LiteralEquationGenerator(ProblemGenerator):
    """
    Generates literal equations (equations with multiple variables) to solve for a specific variable.
    
    Problem types:
    - One-step generic: a + x = b (solve for x) -> x = b - a
    - Two-step generic: ax + b = c (solve for x) -> x = (c - b) / a
    - Common formulas:
        - A = lw (solve for w)
        - P = 2l + 2w (solve for l)
        - y = mx + b (solve for x)
        - d = rt (solve for t)
    
    Op-codes used:
    - EQ_SETUP: Set up the equation
    - EQ_OP_BOTH: Apply operation to both sides
    - EQ_SIMPLIFY: Simplify the expression
    - EQ_RESULT: Show the result
    - Z: Final answer
    """
    
    def __init__(self):
        pass
        
    def generate(self) -> dict:
        """Generate a literal equation problem."""
        problem_type = random.choice([
            'one_step_add', 
            'one_step_sub', 
            'one_step_mult', 
            'one_step_div',
            'two_step_linear',
            'formula_area_rect',
            'formula_perimeter_rect',
            'formula_linear_y'
        ])
        
        if problem_type == 'one_step_add':
            return self._generate_one_step_add()
        elif problem_type == 'one_step_sub':
            return self._generate_one_step_sub()
        elif problem_type == 'one_step_mult':
            return self._generate_one_step_mult()
        elif problem_type == 'one_step_div':
            return self._generate_one_step_div()
        elif problem_type == 'two_step_linear':
            return self._generate_two_step_linear()
        elif problem_type == 'formula_area_rect':
            return self._generate_formula_area_rect()
        elif problem_type == 'formula_perimeter_rect':
            return self._generate_formula_perimeter_rect()
        elif problem_type == 'formula_linear_y':
            return self._generate_formula_linear_y()
        else:
            return self._generate_one_step_add() # Fallback

    def _get_variables(self, count=3, exclude=None):
        if exclude is None:
            exclude = []
        vars = [v for v in "abcdefmnpqrstuwxyz" if v not in exclude]
        return random.sample(vars, count)

    def _generate_one_step_add(self):
        # x + a = b, solve for x -> x = b - a
        x, a, b = self._get_variables(3)
        
        equation = f"{x} + {a} = {b}"
        steps = []
        steps.append(step("EQ_SETUP", equation))
        steps.append(step("EQ_OP_BOTH", "subtract", a, "from both sides"))
        ans = f"{b} - {a}"
        steps.append(step("EQ_RESULT", f"{x} = {ans}"))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="literal_eq_one_step_add",
            problem=f"Solve for {x}: {equation}",
            steps=steps,
            final_answer=ans
        )

    def _generate_one_step_sub(self):
        # x - a = b, solve for x -> x = b + a
        x, a, b = self._get_variables(3)
        
        equation = f"{x} - {a} = {b}"
        steps = []
        steps.append(step("EQ_SETUP", equation))
        steps.append(step("EQ_OP_BOTH", "add", a, "to both sides"))
        ans = f"{b} + {a}"
        steps.append(step("EQ_RESULT", f"{x} = {ans}"))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="literal_eq_one_step_sub",
            problem=f"Solve for {x}: {equation}",
            steps=steps,
            final_answer=ans
        )

    def _generate_one_step_mult(self):
        # ax = b, solve for x -> x = b/a
        # Order matters for display: "ax" vs "xa". Usually coefficient first.
        # Here both are variables, so we pick one as 'coeff'
        a, x, b = self._get_variables(3)
        
        equation = f"{a}{x} = {b}"
        steps = []
        steps.append(step("EQ_SETUP", equation))
        steps.append(step("EQ_OP_BOTH", "divide", a, "from both sides"))
        ans = f"{b}/{a}"
        steps.append(step("EQ_RESULT", f"{x} = {ans}"))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="literal_eq_one_step_mult",
            problem=f"Solve for {x}: {equation}",
            steps=steps,
            final_answer=ans
        )

    def _generate_one_step_div(self):
        # x/a = b, solve for x -> x = ab
        x, a, b = self._get_variables(3)
        
        equation = f"{x}/{a} = {b}"
        steps = []
        steps.append(step("EQ_SETUP", equation))
        steps.append(step("EQ_OP_BOTH", "multiply", a, "to both sides"))
        ans = f"{b}{a}" # or ab, usually alphabetical order is nicer but raw is fine
        # Let's try to sort for cleaner look if simple chars
        if a < b:
            ans = f"{a}{b}"
        else:
            ans = f"{b}{a}"
            
        steps.append(step("EQ_RESULT", f"{x} = {ans}"))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="literal_eq_one_step_div",
            problem=f"Solve for {x}: {equation}",
            steps=steps,
            final_answer=ans
        )

    def _generate_two_step_linear(self):
        # ax + b = c, solve for x -> x = (c - b) / a
        a, x, b, c = self._get_variables(4)
        
        equation = f"{a}{x} + {b} = {c}"
        steps = []
        steps.append(step("EQ_SETUP", equation))
        
        # Step 1: Subtract b
        steps.append(step("EQ_OP_BOTH", "subtract", b, "from both sides"))
        intermediate = f"{c} - {b}"
        steps.append(step("EQ_RESULT", f"{a}{x} = {intermediate}"))
        
        # Step 2: Divide by a
        steps.append(step("EQ_OP_BOTH", "divide", a, "from both sides"))
        ans = f"({intermediate})/{a}"
        steps.append(step("EQ_RESULT", f"{x} = {ans}"))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="literal_eq_two_step_linear",
            problem=f"Solve for {x}: {equation}",
            steps=steps,
            final_answer=ans
        )

    def _generate_formula_area_rect(self):
        # A = lw, solve for w (or l)
        # 50% chance for w or l
        target = random.choice(['w', 'l'])
        other = 'l' if target == 'w' else 'w'
        equation = f"A = {other}{target}" # usually lw
        
        if target == 'l':
             equation = "A = lw" # standard form
             
        steps = []
        steps.append(step("EQ_SETUP", equation))
        steps.append(step("EQ_OP_BOTH", "divide", other, "from both sides"))
        ans = f"A/{other}"
        steps.append(step("EQ_RESULT", f"{target} = {ans}"))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="literal_eq_formula_area",
            problem=f"Solve for {target}: {equation}",
            steps=steps,
            final_answer=ans
        )

    def _generate_formula_perimeter_rect(self):
        # P = 2l + 2w, solve for l (or w)
        target = random.choice(['w', 'l'])
        other = 'l' if target == 'w' else 'w'
        equation = "P = 2l + 2w"
        
        steps = []
        steps.append(step("EQ_SETUP", equation))
        
        # Step 1: Subtract 2*other
        term_to_subtract = f"2{other}"
        steps.append(step("EQ_OP_BOTH", "subtract", term_to_subtract, "from both sides"))
        
        steps.append(step("EQ_RESULT", f"2{target} = P - {term_to_subtract}"))
        
        # Step 2: Divide by 2
        steps.append(step("EQ_OP_BOTH", "divide", "2", "from both sides"))
        
        ans = f"(P - 2{other})/2"
        steps.append(step("EQ_RESULT", f"{target} = {ans}"))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="literal_eq_formula_perimeter",
            problem=f"Solve for {target}: {equation}",
            steps=steps,
            final_answer=ans
        )

    def _generate_formula_linear_y(self):
        # y = mx + b, solve for x
        # or solve for m
        
        target = random.choice(['x', 'm'])
        other = 'm' if target == 'x' else 'x' # coefficient
        
        equation = "y = mx + b"
        
        steps = []
        steps.append(step("EQ_SETUP", equation))
        
        # Step 1: Subtract b
        steps.append(step("EQ_OP_BOTH", "subtract", "b", "from both sides"))
        steps.append(step("EQ_RESULT", f"{other}{target} = y - b"))
        
        # Step 2: Divide by other
        steps.append(step("EQ_OP_BOTH", "divide", other, "from both sides"))
        ans = f"(y - b)/{other}"
        
        steps.append(step("EQ_RESULT", f"{target} = {ans}"))
        steps.append(step("Z", ans))
        
        return dict(
            problem_id=jid(),
            operation="literal_eq_formula_linear_y",
            problem=f"Solve for {target}: {equation}",
            steps=steps,
            final_answer=ans
        )
