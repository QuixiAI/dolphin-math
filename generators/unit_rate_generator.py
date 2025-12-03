import random
from base_generator import ProblemGenerator
from helpers import step, jid


class UnitRateGenerator(ProblemGenerator):
    """
    Generates unit rate calculation problems.

    Problems involve finding how much of something corresponds to one unit.
    For example: "If 5 apples cost $3.50, how much does 1 apple cost?"

    Op-codes used:
    - UNIT_RATE_SETUP: Set up the problem (total_quantity, total_amount, unit_label)
    - UNIT_RATE_DIV: Divide to find rate (total_amount, quantity, unit_rate)
    - Z: Final answer
    """

    # Context templates: (item_plural, item_singular, unit_type, unit_symbol)
    CONTEXTS = [
        ("apples", "apple", "dollars", "$"),
        ("oranges", "orange", "dollars", "$"),
        ("books", "book", "dollars", "$"),
        ("pencils", "pencil", "cents", "¢"),
        ("cookies", "cookie", "cents", "¢"),
        ("miles", "mile", "hours", " hours"),
        ("kilometers", "kilometer", "hours", " hours"),
        ("pages", "page", "minutes", " minutes"),
        ("laps", "lap", "minutes", " minutes"),
        ("gallons", "gallon", "dollars", "$"),
        ("liters", "liter", "dollars", "$"),
        ("pounds", "pound", "dollars", "$"),
        ("kilograms", "kilogram", "dollars", "$"),
        ("shirts", "shirt", "dollars", "$"),
        ("tickets", "ticket", "dollars", "$"),
    ]

    def generate(self) -> dict:
        """Generate a unit rate calculation problem."""
        # Pick a random context
        item_plural, item_singular, unit_type, unit_symbol = random.choice(self.CONTEXTS)

        # Generate quantity (number of items)
        quantity = random.randint(2, 12)

        # Generate total amount based on unit type
        if unit_type == "dollars":
            # Create a total that divides evenly or to nice decimals
            # Unit price between $0.50 and $10.00
            unit_price_cents = random.choice([25, 50, 75, 100, 125, 150, 175, 200, 250, 300, 350, 400, 450, 500, 600, 750, 800, 900, 1000])
            total_cents = unit_price_cents * quantity
            total_amount = total_cents / 100
            unit_rate = unit_price_cents / 100

            # Format amounts
            total_str = f"${total_amount:.2f}"
            unit_rate_str = f"${unit_rate:.2f}"

        elif unit_type == "cents":
            # Unit price between 5 and 50 cents
            unit_rate = random.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
            total_amount = unit_rate * quantity

            total_str = f"{total_amount}¢"
            unit_rate_str = f"{unit_rate}¢"

        elif unit_type == "hours":
            # Time rates - ensure clean division
            unit_rate = random.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6])
            total_amount = unit_rate * quantity

            total_str = f"{total_amount} {unit_type}"
            if unit_rate == int(unit_rate):
                unit_rate_str = f"{int(unit_rate)} {unit_type}" if unit_rate != 1 else f"1 hour"
            else:
                unit_rate_str = f"{unit_rate} {unit_type}"

        else:  # minutes
            unit_rate = random.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30])
            total_amount = unit_rate * quantity

            total_str = f"{total_amount} {unit_type}"
            unit_rate_str = f"{unit_rate} {unit_type}" if unit_rate != 1 else f"1 minute"

        # Create problem text
        if unit_type == "dollars" or unit_type == "cents":
            problem = f"If {quantity} {item_plural} cost {total_str}, what is the cost of 1 {item_singular}?"
        elif unit_type == "hours":
            problem = f"If it takes {total_str} to travel {quantity} {item_plural}, how long does it take to travel 1 {item_singular}?"
        else:  # minutes
            problem = f"If it takes {total_str} to complete {quantity} {item_plural}, how long does it take to complete 1 {item_singular}?"

        # Build solution steps
        steps = []

        # Step 1: Set up the unit rate problem
        steps.append(step("UNIT_RATE_SETUP", quantity, item_plural, total_str))

        # Step 2: Divide total by quantity
        steps.append(step("UNIT_RATE_DIV", total_str, quantity, unit_rate_str))

        # Final answer
        steps.append(step("Z", unit_rate_str))

        return dict(
            problem_id=jid(),
            operation="unit_rate",
            problem=problem,
            steps=steps,
            final_answer=unit_rate_str,
        )


class UnitRateFromTableGenerator(ProblemGenerator):
    """
    Generates unit rate problems where students find rate from a table of values.

    Op-codes used:
    - UNIT_RATE_TABLE: Show the table data (x_values, y_values)
    - UNIT_RATE_PICK: Pick a row to calculate from (x, y)
    - UNIT_RATE_DIV: Divide to find rate (y, x, rate)
    - Z: Final answer
    """

    def generate(self) -> dict:
        """Generate a unit rate from table problem."""
        # Generate a unit rate
        rate = random.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25])

        # Generate 3-4 x values
        num_rows = random.randint(3, 4)
        x_values = sorted(random.sample(range(1, 11), num_rows))
        y_values = [x * rate for x in x_values]

        # Create table representation
        table_x = ",".join(str(x) for x in x_values)
        table_y = ",".join(str(y) for y in y_values)

        # Choose context
        contexts = [
            ("hours worked", "dollars earned", "hour"),
            ("gallons of gas", "miles traveled", "gallon"),
            ("pounds of fruit", "total cost in dollars", "pound"),
            ("hours", "pages read", "hour"),
            ("days", "miles run", "day"),
        ]
        x_label, y_label, unit = random.choice(contexts)

        # Create problem
        table_str = f"| {x_label} | {y_label} |\n"
        table_str += "|" + "-" * (len(x_label) + 2) + "|" + "-" * (len(y_label) + 2) + "|\n"
        for x, y in zip(x_values, y_values):
            table_str += f"| {x} | {y} |\n"

        problem = f"Find the unit rate ({y_label} per {unit}) from the table:\n{table_str}"

        # Build steps
        steps = []

        # Show table data
        steps.append(step("UNIT_RATE_TABLE", table_x, table_y))

        # Pick a row (use the first one for simplicity)
        x_pick, y_pick = x_values[0], y_values[0]
        steps.append(step("UNIT_RATE_PICK", x_pick, y_pick))

        # Calculate rate
        steps.append(step("UNIT_RATE_DIV", y_pick, x_pick, rate))

        # Final answer
        steps.append(step("Z", rate))

        return dict(
            problem_id=jid(),
            operation="unit_rate_table",
            problem=problem,
            steps=steps,
            final_answer=str(rate),
        )
