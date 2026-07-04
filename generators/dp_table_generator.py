import random

from base_generator import ProblemGenerator
from helpers import step, jid


LETTERS = "ABCD"


def row_text(row):
    return ", ".join(str(value) for value in row)


def item_text(items):
    return "; ".join(
        f"{idx}:(w={weight},v={value})"
        for idx, (weight, value) in enumerate(items, start=1)
    )


def coin_text(coins):
    return ", ".join(str(coin) for coin in coins)


def random_word(length):
    return "".join(random.choice(LETTERS) for _ in range(length))


class DPTableGenerator(ProblemGenerator):
    """
    Dynamic-programming table filling for common discrete math algorithms.

    Variants:
    - knapsack: 0/1 knapsack maximum value table
    - lcs: longest common subsequence length table
    - edit_distance: Levenshtein distance table
    - coin_change: unlimited-coin combination count table

    Op-codes used:
    - DP_SETUP / DP_ITEMS / DP_COINS: problem setup
    - DP_CELL / DP_ROW: table entries and completed rows
    - MAX / MIN3 / A (established): recurrence arithmetic
    - Z: final value read from the completed table
    """

    VARIANTS = ["knapsack", "lcs", "edit_distance", "coin_change"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)
        if variant == "knapsack":
            problem, steps, answer = self._generate_knapsack()
        elif variant == "lcs":
            problem, steps, answer = self._generate_lcs()
        elif variant == "edit_distance":
            problem, steps, answer = self._generate_edit_distance()
        else:
            problem, steps, answer = self._generate_coin_change()
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"dp_table_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )

    def _generate_knapsack(self):
        count = random.randint(3, 4)
        items = [
            (random.randint(1, 5), random.randint(2, 11))
            for _ in range(count)
        ]
        capacity = random.randint(5, 9)
        if all(weight > capacity for weight, _ in items):
            items[0] = (random.randint(1, capacity), items[0][1])

        table = [[0] * (capacity + 1)]
        steps = [
            step("DP_SETUP", "0/1 knapsack", f"capacity {capacity}"),
            step("DP_ITEMS", item_text(items)),
            step("DP_ROW", "i=0", row_text(table[0])),
        ]
        for i, (weight, value) in enumerate(items, start=1):
            previous = table[i - 1]
            row = []
            for c in range(capacity + 1):
                if c == 0:
                    best = 0
                    steps.append(step("DP_CELL", f"i={i},c={c}", "base", best))
                elif weight > c:
                    best = previous[c]
                    steps.append(step("DP_CELL", f"i={i},c={c}",
                                      f"skip w={weight} > c", best))
                else:
                    take = value + previous[c - weight]
                    steps.append(step("A", value, previous[c - weight], take))
                    skip = previous[c]
                    best = max(skip, take)
                    steps.append(step("MAX", skip, take, best))
                    steps.append(step("DP_CELL", f"i={i},c={c}",
                                      f"max skip {skip}, take {take}", best))
                row.append(best)
            table.append(row)
            steps.append(step("DP_ROW", f"i={i}", row_text(row)))
        answer = f"maximum value = {table[-1][capacity]}"
        problem = (
            f"Fill the 0/1 knapsack DP table for capacity {capacity} with "
            f"items {item_text(items)}. What maximum value fits?"
        )
        return problem, steps, answer

    def _generate_lcs(self):
        x = random_word(random.randint(4, 5))
        y = random_word(random.randint(4, 5))
        steps = [
            step("DP_SETUP", "LCS", f"X={x}", f"Y={y}"),
        ]
        table = [[0] * (len(y) + 1)]
        steps.append(step("DP_ROW", "i=0", row_text(table[0])))
        for i, x_char in enumerate(x, start=1):
            row = [0]
            steps.append(step("DP_CELL", f"i={i},j=0", "base", 0))
            for j, y_char in enumerate(y, start=1):
                if x_char == y_char:
                    value = table[i - 1][j - 1] + 1
                    steps.append(step("A", table[i - 1][j - 1], 1, value))
                    steps.append(step("DP_CELL", f"i={i},j={j}",
                                      f"match {x_char}", value))
                else:
                    up = table[i - 1][j]
                    left = row[j - 1]
                    value = max(up, left)
                    steps.append(step("MAX", up, left, value))
                    steps.append(step("DP_CELL", f"i={i},j={j}",
                                      f"max up {up}, left {left}", value))
                row.append(value)
            table.append(row)
            steps.append(step("DP_ROW", f"i={i}", row_text(row)))
        answer = f"LCS length = {table[-1][-1]}"
        problem = (
            f"Fill the LCS DP table for X={x} and Y={y}. "
            f"What is the LCS length?"
        )
        return problem, steps, answer

    def _generate_edit_distance(self):
        source = random_word(random.randint(3, 5))
        target = random_word(random.randint(3, 5))
        first_row = list(range(len(target) + 1))
        table = [first_row]
        steps = [
            step("DP_SETUP", "edit distance", f"source={source}",
                 f"target={target}"),
            step("DP_ROW", "i=0", row_text(first_row)),
        ]
        for i, source_char in enumerate(source, start=1):
            row = [i]
            steps.append(step("DP_CELL", f"i={i},j=0",
                              f"delete {i} chars", i))
            for j, target_char in enumerate(target, start=1):
                if source_char == target_char:
                    value = table[i - 1][j - 1]
                    steps.append(step("DP_CELL", f"i={i},j={j}",
                                      f"match {source_char}", value))
                else:
                    delete = table[i - 1][j] + 1
                    insert = row[j - 1] + 1
                    replace = table[i - 1][j - 1] + 1
                    steps.append(step("A", table[i - 1][j], 1, delete))
                    steps.append(step("A", row[j - 1], 1, insert))
                    steps.append(step("A", table[i - 1][j - 1], 1, replace))
                    value = min(delete, insert, replace)
                    steps.append(step("MIN3", delete, insert, replace, value))
                    steps.append(step("DP_CELL", f"i={i},j={j}",
                                      "min delete, insert, replace", value))
                row.append(value)
            table.append(row)
            steps.append(step("DP_ROW", f"i={i}", row_text(row)))
        answer = f"edit distance = {table[-1][-1]}"
        problem = (
            f"Fill the edit-distance DP table from source={source} to "
            f"target={target}. What is the minimum edit distance?"
        )
        return problem, steps, answer

    def _generate_coin_change(self):
        pool = [2, 3, 4, 5, 6]
        coins = sorted([1] + random.sample(pool, 2))
        target = random.randint(5, 10)
        table = [[1] + [0] * target]
        steps = [
            step("DP_SETUP", "coin change", f"target {target}"),
            step("DP_COINS", coin_text(coins)),
            step("DP_ROW", "i=0", row_text(table[0])),
        ]
        for i, coin in enumerate(coins, start=1):
            row = []
            for amount in range(target + 1):
                if amount == 0:
                    ways = 1
                    steps.append(step("DP_CELL", f"i={i},amount={amount}",
                                      "base empty set", ways))
                elif coin > amount:
                    ways = table[i - 1][amount]
                    steps.append(step("DP_CELL", f"i={i},amount={amount}",
                                      f"no coin {coin}", ways))
                else:
                    without = table[i - 1][amount]
                    with_coin = row[amount - coin]
                    ways = without + with_coin
                    steps.append(step("A", without, with_coin, ways))
                    steps.append(step("DP_CELL", f"i={i},amount={amount}",
                                      f"without {without}, with {with_coin}",
                                      ways))
                row.append(ways)
            table.append(row)
            steps.append(step("DP_ROW", f"i={i}", row_text(row)))
        answer = f"ways = {table[-1][target]}"
        problem = (
            f"Fill the coin-change DP table for coins {coin_text(coins)} "
            f"and target {target}, counting combinations with unlimited coins. "
            f"How many ways are there?"
        )
        return problem, steps, answer
