import random
from fractions import Fraction
from base_generator import ProblemGenerator
from helpers import step, jid


class CompoundProbabilityIndependentGenerator(ProblemGenerator):
    """
    Generates compound probability problems with independent events.

    P(A and B) = P(A) × P(B) for independent events

    Op-codes used:
    - PROB_SETUP: Describe the probability scenario (event_description)
    - PROB_IDENTIFY: Identify individual probabilities (event, probability)
    - PROB_INDEPENDENT: Note that events are independent
    - PROB_MULTIPLY: Multiply probabilities (P(A), P(B), result)
    - PROB_SIMPLIFY: Simplify the fraction if needed (original, simplified)
    - Z: Final answer
    """

    CONTEXTS = [
        {
            "name": "coin_flip",
            "items": ["heads", "tails"],
            "total": 2,
            "object": "coin",
            "action": "flip"
        },
        {
            "name": "die_roll",
            "items": ["1", "2", "3", "4", "5", "6"],
            "total": 6,
            "object": "die",
            "action": "roll"
        },
        {
            "name": "card_suit",
            "items": ["hearts", "diamonds", "clubs", "spades"],
            "total": 4,
            "favorable": 1,
            "object": "card",
            "action": "draw"
        },
    ]

    def generate(self) -> dict:
        """Generate a compound probability problem with independent events."""
        problem_type = random.choice(['two_coins', 'two_dice', 'coin_and_die', 'with_replacement'])

        if problem_type == 'two_coins':
            return self._generate_two_coins()
        elif problem_type == 'two_dice':
            return self._generate_two_dice()
        elif problem_type == 'coin_and_die':
            return self._generate_coin_and_die()
        else:
            return self._generate_with_replacement()

    def _generate_two_coins(self) -> dict:
        """Generate problem with two coin flips."""
        outcomes = [("heads", "heads"), ("heads", "tails"), ("tails", "heads"), ("tails", "tails")]
        target = random.choice(outcomes)

        problem = f"A coin is flipped twice. What is the probability of getting {target[0]} on the first flip and {target[1]} on the second flip?"

        steps_list = []
        steps_list.append(step("PROB_SETUP", f"Two coin flips, looking for {target[0]} then {target[1]}"))
        steps_list.append(step("PROB_IDENTIFY", f"P({target[0]})", "1/2"))
        steps_list.append(step("PROB_IDENTIFY", f"P({target[1]})", "1/2"))
        steps_list.append(step("PROB_INDEPENDENT", "Coin flips are independent events"))
        steps_list.append(step("PROB_MULTIPLY", "1/2", "1/2", "1/4"))

        final_answer = "1/4"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="compound_probability_independent",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_two_dice(self) -> dict:
        """Generate problem with two dice rolls."""
        target1 = random.randint(1, 6)
        target2 = random.randint(1, 6)

        problem = f"Two dice are rolled. What is the probability of getting a {target1} on the first die and a {target2} on the second die?"

        steps_list = []
        steps_list.append(step("PROB_SETUP", f"Two dice rolls, looking for {target1} then {target2}"))
        steps_list.append(step("PROB_IDENTIFY", f"P(rolling {target1})", "1/6"))
        steps_list.append(step("PROB_IDENTIFY", f"P(rolling {target2})", "1/6"))
        steps_list.append(step("PROB_INDEPENDENT", "Dice rolls are independent events"))
        steps_list.append(step("PROB_MULTIPLY", "1/6", "1/6", "1/36"))

        final_answer = "1/36"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="compound_probability_independent",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_coin_and_die(self) -> dict:
        """Generate problem with coin flip and die roll."""
        coin_target = random.choice(["heads", "tails"])
        die_target = random.randint(1, 6)

        problem = f"A coin is flipped and a die is rolled. What is the probability of getting {coin_target} and rolling a {die_target}?"

        steps_list = []
        steps_list.append(step("PROB_SETUP", f"Coin flip and die roll, looking for {coin_target} and {die_target}"))
        steps_list.append(step("PROB_IDENTIFY", f"P({coin_target})", "1/2"))
        steps_list.append(step("PROB_IDENTIFY", f"P(rolling {die_target})", "1/6"))
        steps_list.append(step("PROB_INDEPENDENT", "Coin flip and die roll are independent events"))
        steps_list.append(step("PROB_MULTIPLY", "1/2", "1/6", "1/12"))

        final_answer = "1/12"
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="compound_probability_independent",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_with_replacement(self) -> dict:
        """Generate problem drawing with replacement (independent)."""
        colors = ["red", "blue", "green", "yellow"]
        total = random.randint(8, 15)

        # Generate counts for each color
        counts = {}
        remaining = total
        for i, color in enumerate(colors[:-1]):
            if remaining > len(colors) - i:
                count = random.randint(1, remaining - (len(colors) - i - 1))
                counts[color] = count
                remaining -= count
            else:
                counts[color] = 1
                remaining -= 1
        counts[colors[-1]] = remaining

        # Pick two colors to draw
        color1 = random.choice(colors)
        color2 = random.choice(colors)

        problem = f"A bag contains {', '.join(f'{counts[c]} {c}' for c in colors)} marbles. A marble is drawn, replaced, and another marble is drawn. What is the probability of drawing a {color1} marble first and a {color2} marble second?"

        p1 = Fraction(counts[color1], total)
        p2 = Fraction(counts[color2], total)
        result = p1 * p2

        steps_list = []
        steps_list.append(step("PROB_SETUP", f"Draw with replacement: {color1} then {color2}"))
        steps_list.append(step("PROB_IDENTIFY", f"P({color1})", str(p1)))
        steps_list.append(step("PROB_IDENTIFY", f"P({color2})", str(p2)))
        steps_list.append(step("PROB_INDEPENDENT", "Drawing with replacement means independent events"))
        steps_list.append(step("PROB_MULTIPLY", str(p1), str(p2), str(result)))

        final_answer = str(result)
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="compound_probability_independent",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )


class CompoundProbabilityDependentGenerator(ProblemGenerator):
    """
    Generates compound probability problems with dependent events.

    P(A and B) = P(A) × P(B|A) for dependent events

    Op-codes used:
    - PROB_SETUP: Describe the probability scenario
    - PROB_IDENTIFY: Identify individual probabilities
    - PROB_DEPENDENT: Note that events are dependent
    - PROB_CONDITIONAL: Calculate conditional probability P(B|A)
    - PROB_MULTIPLY: Multiply probabilities
    - PROB_SIMPLIFY: Simplify the fraction
    - Z: Final answer
    """

    def generate(self) -> dict:
        """Generate a compound probability problem with dependent events."""
        problem_type = random.choice(['without_replacement', 'cards'])

        if problem_type == 'without_replacement':
            return self._generate_without_replacement()
        else:
            return self._generate_cards()

    def _generate_without_replacement(self) -> dict:
        """Generate problem drawing without replacement (dependent)."""
        colors = ["red", "blue"]
        color1_count = random.randint(3, 7)
        color2_count = random.randint(3, 7)
        total = color1_count + color2_count

        color1 = "red"
        color2 = random.choice(["red", "blue"])

        problem = f"A bag contains {color1_count} red marbles and {color2_count} blue marbles. Two marbles are drawn without replacement. What is the probability of drawing a {color1} marble first and a {color2} marble second?"

        # First draw
        p1_num = color1_count if color1 == "red" else color2_count
        p1 = Fraction(p1_num, total)

        # Second draw (conditional)
        if color2 == color1:
            p2_num = p1_num - 1
        else:
            p2_num = color2_count if color1 == "red" else color1_count
        p2 = Fraction(p2_num, total - 1)

        result = p1 * p2

        steps_list = []
        steps_list.append(step("PROB_SETUP", f"Draw without replacement: {color1} then {color2}"))
        steps_list.append(step("PROB_IDENTIFY", f"P(first {color1})", str(p1)))
        steps_list.append(step("PROB_DEPENDENT", "Drawing without replacement means dependent events"))
        steps_list.append(step("PROB_CONDITIONAL", f"P({color2}|first was {color1})", str(p2)))
        steps_list.append(step("PROB_MULTIPLY", str(p1), str(p2), str(result)))

        final_answer = str(result)
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="compound_probability_dependent",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )

    def _generate_cards(self) -> dict:
        """Generate problem with cards drawn without replacement."""
        # Draw two cards without replacement
        # Example: probability of drawing two hearts

        suit = random.choice(["hearts", "diamonds", "clubs", "spades"])

        problem = f"Two cards are drawn from a standard deck without replacement. What is the probability that both cards are {suit}?"

        # P(first heart) = 13/52
        p1 = Fraction(13, 52)

        # P(second heart | first was heart) = 12/51
        p2 = Fraction(12, 51)

        result = p1 * p2

        steps_list = []
        steps_list.append(step("PROB_SETUP", f"Draw two {suit} cards without replacement"))
        steps_list.append(step("PROB_IDENTIFY", f"P(first {suit})", f"{p1} = 13/52"))
        steps_list.append(step("PROB_DEPENDENT", "Drawing without replacement means dependent events"))
        steps_list.append(step("PROB_CONDITIONAL", f"P(second {suit}|first was {suit})", f"{p2} = 12/51"))
        steps_list.append(step("PROB_MULTIPLY", "13/52", "12/51", str(result)))

        # Simplify
        simplified = Fraction(result.numerator, result.denominator)
        if simplified != result:
            steps_list.append(step("PROB_SIMPLIFY", str(result), str(simplified)))

        final_answer = str(simplified)
        steps_list.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation="compound_probability_dependent",
            problem=problem,
            steps=steps_list,
            final_answer=final_answer,
        )
