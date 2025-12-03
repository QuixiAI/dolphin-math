import random
from base_generator import ProblemGenerator
from helpers import step, jid


class ExponentEvaluationGenerator(ProblemGenerator):
    """
    Generates exponent evaluation problems (compute a^n).

    Op-codes used:
    - EXP_SETUP: Set up the exponent expression (base, exponent)
    - EXP_EXPAND: Expand as repeated multiplication (expansion_string)
    - EXP_PARTIAL: Show partial products (current_product, next_factor, new_product)
    - Z: Final answer
    """

    def __init__(self, allow_negative_base: bool = True, max_exponent: int = 6):
        """
        Initialize generator.

        Args:
            allow_negative_base: Whether to allow negative bases
            max_exponent: Maximum exponent value
        """
        self.allow_negative_base = allow_negative_base
        self.max_exponent = max_exponent

    def generate(self) -> dict:
        """Generate an exponent evaluation problem."""
        # Generate base
        if self.allow_negative_base and random.choice([True, False]):
            base = random.randint(-5, -2)
        else:
            base = random.randint(2, 10)

        # Generate exponent (2 to max_exponent)
        exponent = random.randint(2, self.max_exponent)

        # Calculate result
        result = base ** exponent

        # Format problem
        if base < 0:
            problem = f"Evaluate: ({base})^{exponent}"
        else:
            problem = f"Evaluate: {base}^{exponent}"

        steps = []

        # Step 1: Set up
        steps.append(step("EXP_SETUP", base, exponent))

        # Step 2: Expand as repeated multiplication
        if base < 0:
            expansion = " × ".join([f"({base})"] * exponent)
        else:
            expansion = " × ".join([str(base)] * exponent)
        steps.append(step("EXP_EXPAND", expansion))

        # Step 3: Show partial products
        current = base
        for i in range(1, exponent):
            new_product = current * base
            steps.append(step("EXP_PARTIAL", current, base, new_product))
            current = new_product

        # Final answer
        steps.append(step("Z", result))

        return dict(
            problem_id=jid(),
            operation="exponent_evaluation",
            problem=problem,
            steps=steps,
            final_answer=str(result),
        )


class ExponentRulesGenerator(ProblemGenerator):
    """
    Generates exponent rule problems.

    Rules covered:
    - Product rule: x^a · x^b = x^(a+b)
    - Quotient rule: x^a / x^b = x^(a-b)
    - Power rule: (x^a)^b = x^(ab)
    - Negative exponents: x^(-n) = 1/x^n
    - Zero exponent: x^0 = 1

    Op-codes used:
    - EXP_RULE_SETUP: Set up the expression (expression_string)
    - EXP_RULE_IDENTIFY: Identify the rule being used (rule_name)
    - EXP_RULE_APPLY: Apply the rule (operation, exp1, exp2, result_exp)
    - EXP_RULE_SIMPLIFY: Simplify the result (simplified_expression)
    - Z: Final answer
    """

    RULES = ['product', 'quotient', 'power', 'negative', 'zero']

    def __init__(self, rule: str = None):
        """
        Initialize generator.

        Args:
            rule: One of 'product', 'quotient', 'power', 'negative', 'zero' or None for random
        """
        if rule is not None and rule not in self.RULES:
            raise ValueError(f"Invalid rule: {rule}. Must be one of {self.RULES} or None.")
        self.rule = rule

    def generate(self) -> dict:
        """Generate an exponent rule problem."""
        rule = self.rule or random.choice(self.RULES)

        if rule == 'product':
            return self._generate_product_rule()
        elif rule == 'quotient':
            return self._generate_quotient_rule()
        elif rule == 'power':
            return self._generate_power_rule()
        elif rule == 'negative':
            return self._generate_negative_exponent()
        else:
            return self._generate_zero_exponent()

    def _generate_product_rule(self) -> dict:
        """Generate x^a · x^b = x^(a+b) problem."""
        base = random.choice(['x', 'y', 'a', 'b', 'm', 'n'])
        exp1 = random.randint(2, 8)
        exp2 = random.randint(2, 8)
        result_exp = exp1 + exp2

        problem = f"Simplify: {base}^{exp1} · {base}^{exp2}"
        answer = f"{base}^{result_exp}"

        steps = []
        steps.append(step("EXP_RULE_SETUP", f"{base}^{exp1} · {base}^{exp2}"))
        steps.append(step("EXP_RULE_IDENTIFY", "product_rule", "x^a · x^b = x^(a+b)"))
        steps.append(step("EXP_RULE_APPLY", "add", exp1, exp2, result_exp))
        steps.append(step("EXP_RULE_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_product_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_quotient_rule(self) -> dict:
        """Generate x^a / x^b = x^(a-b) problem."""
        base = random.choice(['x', 'y', 'a', 'b', 'm', 'n'])
        # Ensure exp1 > exp2 for positive result
        exp1 = random.randint(5, 12)
        exp2 = random.randint(2, exp1 - 1)
        result_exp = exp1 - exp2

        problem = f"Simplify: {base}^{exp1} / {base}^{exp2}"
        answer = f"{base}^{result_exp}"

        steps = []
        steps.append(step("EXP_RULE_SETUP", f"{base}^{exp1} / {base}^{exp2}"))
        steps.append(step("EXP_RULE_IDENTIFY", "quotient_rule", "x^a / x^b = x^(a-b)"))
        steps.append(step("EXP_RULE_APPLY", "subtract", exp1, exp2, result_exp))
        steps.append(step("EXP_RULE_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_quotient_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_power_rule(self) -> dict:
        """Generate (x^a)^b = x^(ab) problem."""
        base = random.choice(['x', 'y', 'a', 'b', 'm', 'n'])
        exp1 = random.randint(2, 5)
        exp2 = random.randint(2, 5)
        result_exp = exp1 * exp2

        problem = f"Simplify: ({base}^{exp1})^{exp2}"
        answer = f"{base}^{result_exp}"

        steps = []
        steps.append(step("EXP_RULE_SETUP", f"({base}^{exp1})^{exp2}"))
        steps.append(step("EXP_RULE_IDENTIFY", "power_rule", "(x^a)^b = x^(ab)"))
        steps.append(step("EXP_RULE_APPLY", "multiply", exp1, exp2, result_exp))
        steps.append(step("EXP_RULE_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_power_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_negative_exponent(self) -> dict:
        """Generate x^(-n) = 1/x^n problem."""
        base = random.choice(['x', 'y', 'a', 'b', 'm', 'n'])
        exp = random.randint(2, 6)

        problem = f"Simplify: {base}^(-{exp})"
        answer = f"1/{base}^{exp}"

        steps = []
        steps.append(step("EXP_RULE_SETUP", f"{base}^(-{exp})"))
        steps.append(step("EXP_RULE_IDENTIFY", "negative_exponent", "x^(-n) = 1/x^n"))
        steps.append(step("EXP_RULE_APPLY", "negate", exp, "", exp))
        steps.append(step("EXP_RULE_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_negative_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_zero_exponent(self) -> dict:
        """Generate x^0 = 1 problem."""
        # Use various bases to make it interesting
        base_type = random.choice(['variable', 'number', 'expression'])

        if base_type == 'variable':
            base = random.choice(['x', 'y', 'a', 'b', 'm', 'n'])
            problem = f"Simplify: {base}^0"
        elif base_type == 'number':
            base = random.randint(2, 100)
            problem = f"Evaluate: {base}^0"
        else:
            # Expression like (2x)^0 or (a+b)^0
            inner = random.choice(['2x', '3y', '5m', 'a+b', 'x-y', 'ab'])
            base = f"({inner})"
            problem = f"Simplify: {base}^0"

        answer = "1"

        steps = []
        if base_type == 'expression':
            steps.append(step("EXP_RULE_SETUP", f"{base}^0"))
        else:
            steps.append(step("EXP_RULE_SETUP", f"{base}^0"))
        steps.append(step("EXP_RULE_IDENTIFY", "zero_exponent", "x^0 = 1 (for x ≠ 0)"))
        steps.append(step("EXP_RULE_SIMPLIFY", "1"))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="exponent_zero_rule",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )


class ScientificNotationGenerator(ProblemGenerator):
    """
    Generates scientific notation problems.

    Problem types:
    - Convert standard form to scientific notation
    - Convert scientific notation to standard form
    - Operations with scientific notation (multiply/divide)

    Op-codes used:
    - SCI_SETUP: Set up the problem (number_or_expression)
    - SCI_IDENTIFY: Identify the coefficient and power (coefficient, power)
    - SCI_MOVE_DECIMAL: Show decimal movement (direction, places)
    - SCI_OPERATION: Perform operation (operation, values, result)
    - Z: Final answer
    """

    def __init__(self, problem_type: str = None):
        """
        Initialize generator.

        Args:
            problem_type: One of 'to_scientific', 'from_scientific', 'multiply', 'divide' or None for random
        """
        valid_types = ['to_scientific', 'from_scientific', 'multiply', 'divide']
        if problem_type is not None and problem_type not in valid_types:
            raise ValueError(f"Invalid problem_type: {problem_type}. Must be one of {valid_types} or None.")
        self.problem_type = problem_type

    def generate(self) -> dict:
        """Generate a scientific notation problem."""
        ptype = self.problem_type or random.choice(['to_scientific', 'from_scientific', 'multiply', 'divide'])

        if ptype == 'to_scientific':
            return self._generate_to_scientific()
        elif ptype == 'from_scientific':
            return self._generate_from_scientific()
        elif ptype == 'multiply':
            return self._generate_multiply()
        else:
            return self._generate_divide()

    def _generate_to_scientific(self) -> dict:
        """Convert standard form to scientific notation."""
        # Generate a coefficient (1 <= c < 10)
        coefficient = random.randint(10, 99) / 10  # gives 1.0 to 9.9

        # Generate power
        power = random.choice([-6, -5, -4, -3, -2, 3, 4, 5, 6, 7, 8])

        # Calculate standard form number
        number = coefficient * (10 ** power)

        # Format number for display
        if power >= 0:
            number_str = f"{int(number)}" if number == int(number) else f"{number:.0f}"
        else:
            number_str = f"{number:.{-power + 1}f}".rstrip('0').rstrip('.')

        problem = f"Write in scientific notation: {number_str}"

        # Format answer
        if coefficient == int(coefficient):
            answer = f"{int(coefficient)} × 10^{power}"
        else:
            answer = f"{coefficient} × 10^{power}"

        steps = []
        steps.append(step("SCI_SETUP", number_str))

        if power > 0:
            steps.append(step("SCI_MOVE_DECIMAL", "left", power))
        else:
            steps.append(step("SCI_MOVE_DECIMAL", "right", -power))

        steps.append(step("SCI_IDENTIFY", coefficient, power))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="scientific_notation_convert_to",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_from_scientific(self) -> dict:
        """Convert scientific notation to standard form."""
        coefficient = random.randint(10, 99) / 10
        power = random.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6])

        # Format input
        if coefficient == int(coefficient):
            sci_notation = f"{int(coefficient)} × 10^{power}"
        else:
            sci_notation = f"{coefficient} × 10^{power}"

        problem = f"Write in standard form: {sci_notation}"

        # Calculate standard form
        number = coefficient * (10 ** power)

        # Format answer
        if power >= 0:
            if number == int(number):
                answer = str(int(number))
            else:
                answer = str(number)
        else:
            # Format with appropriate decimal places
            answer = f"{number:.{-power + 1}f}".rstrip('0').rstrip('.')

        steps = []
        steps.append(step("SCI_SETUP", sci_notation))
        steps.append(step("SCI_IDENTIFY", coefficient, power))

        if power > 0:
            steps.append(step("SCI_MOVE_DECIMAL", "right", power))
        else:
            steps.append(step("SCI_MOVE_DECIMAL", "left", -power))

        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="scientific_notation_convert_from",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_multiply(self) -> dict:
        """Multiply two numbers in scientific notation."""
        # Generate two scientific notation numbers
        c1 = random.randint(10, 50) / 10
        c2 = random.randint(10, 50) / 10
        p1 = random.randint(2, 6)
        p2 = random.randint(2, 6)

        # Calculate result
        c_result = c1 * c2
        p_result = p1 + p2

        # Adjust if coefficient >= 10
        if c_result >= 10:
            c_result /= 10
            p_result += 1

        # Format inputs
        n1 = f"({c1} × 10^{p1})"
        n2 = f"({c2} × 10^{p2})"

        problem = f"Multiply: {n1} × {n2}"

        # Round coefficient for clean answer
        c_result = round(c_result, 2)
        answer = f"{c_result} × 10^{p_result}"

        steps = []
        steps.append(step("SCI_SETUP", f"{n1} × {n2}"))
        steps.append(step("SCI_OPERATION", "multiply_coefficients", c1, c2, c1 * c2))
        steps.append(step("SCI_OPERATION", "add_exponents", p1, p2, p1 + p2))

        if c1 * c2 >= 10:
            steps.append(step("SCI_OPERATION", "adjust_coefficient", c1 * c2, c_result, p_result))

        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="scientific_notation_multiply",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_divide(self) -> dict:
        """Divide two numbers in scientific notation."""
        # Generate two scientific notation numbers
        # Use clean coefficients to avoid floating point issues
        # c2 choices that divide cleanly: 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0
        c2_options = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
        c2 = random.choice(c2_options)
        multiplier = random.randint(2, 8)
        c1 = c2 * multiplier

        p1 = random.randint(5, 10)
        p2 = random.randint(2, 4)

        # Calculate result
        c_result = c1 / c2
        p_result = p1 - p2

        # Adjust if coefficient >= 10
        if c_result >= 10:
            c_result /= 10
            p_result += 1

        # Round to avoid floating point display issues
        c1 = round(c1, 1)
        c_result = round(c_result, 2)

        # Format inputs
        n1 = f"({c1} × 10^{p1})"
        n2 = f"({c2} × 10^{p2})"

        problem = f"Divide: {n1} ÷ {n2}"

        answer = f"{c_result} × 10^{p_result}"

        steps = []
        steps.append(step("SCI_SETUP", f"{n1} ÷ {n2}"))
        steps.append(step("SCI_OPERATION", "divide_coefficients", c1, c2, round(c1 / c2, 2)))
        steps.append(step("SCI_OPERATION", "subtract_exponents", p1, p2, p1 - p2))

        if c1 / c2 >= 10:
            steps.append(step("SCI_OPERATION", "adjust_coefficient", round(c1 / c2, 2), c_result, p_result))

        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="scientific_notation_divide",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )


class RootsAndRadicalsGenerator(ProblemGenerator):
    """
    Generates square root, cube root, and radical simplification problems.

    Op-codes used:
    - ROOT_SETUP: Set up the radical expression (expression)
    - ROOT_IDENTIFY: Identify perfect square/cube factor (number, factor, quotient)
    - ROOT_EXTRACT: Extract the root (root_value, remaining)
    - ROOT_SIMPLIFY: Show simplified form (simplified_expression)
    - Z: Final answer
    """

    def __init__(self, problem_type: str = None):
        """
        Initialize generator.

        Args:
            problem_type: One of 'square_perfect', 'cube_perfect', 'simplify_square' or None for random
        """
        valid_types = ['square_perfect', 'cube_perfect', 'simplify_square']
        if problem_type is not None and problem_type not in valid_types:
            raise ValueError(f"Invalid problem_type: {problem_type}. Must be one of {valid_types} or None.")
        self.problem_type = problem_type

    # Perfect squares up to 225 (15^2)
    PERFECT_SQUARES = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225]
    SQUARE_ROOTS = {1: 1, 4: 2, 9: 3, 16: 4, 25: 5, 36: 6, 49: 7, 64: 8, 81: 9,
                    100: 10, 121: 11, 144: 12, 169: 13, 196: 14, 225: 15}

    # Perfect cubes up to 1000 (10^3)
    PERFECT_CUBES = [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]
    CUBE_ROOTS = {1: 1, 8: 2, 27: 3, 64: 4, 125: 5, 216: 6, 343: 7, 512: 8, 729: 9, 1000: 10}

    def generate(self) -> dict:
        """Generate a roots/radicals problem."""
        ptype = self.problem_type or random.choice(['square_perfect', 'cube_perfect', 'simplify_square'])

        if ptype == 'square_perfect':
            return self._generate_square_perfect()
        elif ptype == 'cube_perfect':
            return self._generate_cube_perfect()
        else:
            return self._generate_simplify_square()

    def _generate_square_perfect(self) -> dict:
        """Generate √n where n is a perfect square."""
        n = random.choice(self.PERFECT_SQUARES[1:])  # Skip 1
        answer = self.SQUARE_ROOTS[n]

        problem = f"Evaluate: √{n}"

        steps = []
        steps.append(step("ROOT_SETUP", f"√{n}"))
        steps.append(step("ROOT_IDENTIFY", n, "perfect_square", answer))
        steps.append(step("ROOT_EXTRACT", answer, ""))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="square_root_perfect",
            problem=problem,
            steps=steps,
            final_answer=str(answer),
        )

    def _generate_cube_perfect(self) -> dict:
        """Generate ∛n where n is a perfect cube."""
        n = random.choice(self.PERFECT_CUBES[1:])  # Skip 1
        answer = self.CUBE_ROOTS[n]

        problem = f"Evaluate: ∛{n}"

        steps = []
        steps.append(step("ROOT_SETUP", f"∛{n}"))
        steps.append(step("ROOT_IDENTIFY", n, "perfect_cube", answer))
        steps.append(step("ROOT_EXTRACT", answer, ""))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="cube_root_perfect",
            problem=problem,
            steps=steps,
            final_answer=str(answer),
        )

    def _generate_simplify_square(self) -> dict:
        """Generate √n where n = a²·b (simplifies to a√b)."""
        # Pick a perfect square factor (not 1)
        perfect_factor = random.choice([4, 9, 16, 25, 36, 49])
        root_of_factor = self.SQUARE_ROOTS[perfect_factor]

        # Pick a small non-perfect square remaining factor
        remaining = random.choice([2, 3, 5, 6, 7, 10, 11, 13])

        n = perfect_factor * remaining
        answer = f"{root_of_factor}√{remaining}"

        problem = f"Simplify: √{n}"

        steps = []
        steps.append(step("ROOT_SETUP", f"√{n}"))
        steps.append(step("ROOT_IDENTIFY", n, perfect_factor, remaining))
        steps.append(step("ROOT_EXTRACT", root_of_factor, f"√{remaining}"))
        steps.append(step("ROOT_SIMPLIFY", answer))
        steps.append(step("Z", answer))

        return dict(
            problem_id=jid(),
            operation="simplify_radical",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
