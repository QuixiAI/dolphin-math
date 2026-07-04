import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.dp_table_generator import DPTableGenerator
from helpers import DELIM


KNAP_RE = re.compile(
    r"Fill the 0/1 knapsack DP table for capacity (\d+) with items (.+)\. "
    r"What maximum value fits\?"
)
ITEM_RE = re.compile(r"(\d+):\(w=(\d+),v=(\d+)\)")
LCS_RE = re.compile(
    r"Fill the LCS DP table for X=([A-D]+) and Y=([A-D]+)\. "
    r"What is the LCS length\?"
)
EDIT_RE = re.compile(
    r"Fill the edit-distance DP table from source=([A-D]+) to "
    r"target=([A-D]+)\. What is the minimum edit distance\?"
)
COIN_RE = re.compile(
    r"Fill the coin-change DP table for coins ([\d, ]+) and target (\d+), "
    r"counting combinations with unlimited coins\. How many ways are there\?"
)


def row_text(row):
    return ", ".join(str(value) for value in row)


def item_text(items):
    return "; ".join(
        f"{idx}:(w={weight},v={value})"
        for idx, (weight, value) in enumerate(items, start=1)
    )


def coin_text(coins):
    return ", ".join(str(coin) for coin in coins)


def parse_problem(problem):
    match = KNAP_RE.fullmatch(problem)
    if match:
        capacity = int(match.group(1))
        items = []
        for item in match.group(2).split("; "):
            item_match = ITEM_RE.fullmatch(item)
            assert item_match is not None, item
            _, weight, value = item_match.groups()
            items.append((int(weight), int(value)))
        return {"variant": "knapsack", "capacity": capacity, "items": items}

    match = LCS_RE.fullmatch(problem)
    if match:
        x, y = match.groups()
        return {"variant": "lcs", "x": x, "y": y}

    match = EDIT_RE.fullmatch(problem)
    if match:
        source, target = match.groups()
        return {"variant": "edit_distance", "source": source,
                "target": target}

    match = COIN_RE.fullmatch(problem)
    assert match is not None, problem
    coins = [int(value) for value in match.group(1).split(", ")]
    target = int(match.group(2))
    return {"variant": "coin_change", "coins": coins, "target": target}


def knapsack_table(parts):
    capacity = parts["capacity"]
    table = [[0] * (capacity + 1)]
    for weight, value in parts["items"]:
        previous = table[-1]
        row = []
        for c in range(capacity + 1):
            if c == 0:
                row.append(0)
            elif weight > c:
                row.append(previous[c])
            else:
                row.append(max(previous[c], value + previous[c - weight]))
        table.append(row)
    return table


def lcs_table(parts):
    x = parts["x"]
    y = parts["y"]
    table = [[0] * (len(y) + 1)]
    for i, x_char in enumerate(x, start=1):
        row = [0]
        for j, y_char in enumerate(y, start=1):
            if x_char == y_char:
                row.append(table[i - 1][j - 1] + 1)
            else:
                row.append(max(table[i - 1][j], row[j - 1]))
        table.append(row)
    return table


def edit_distance_table(parts):
    source = parts["source"]
    target = parts["target"]
    table = [list(range(len(target) + 1))]
    for i, source_char in enumerate(source, start=1):
        row = [i]
        for j, target_char in enumerate(target, start=1):
            if source_char == target_char:
                row.append(table[i - 1][j - 1])
            else:
                row.append(min(
                    table[i - 1][j] + 1,
                    row[j - 1] + 1,
                    table[i - 1][j - 1] + 1,
                ))
        table.append(row)
    return table


def coin_change_table(parts):
    target = parts["target"]
    table = [[1] + [0] * target]
    for coin in parts["coins"]:
        row = []
        for amount in range(target + 1):
            if amount == 0:
                row.append(1)
            elif coin > amount:
                row.append(table[-1][amount])
            else:
                row.append(table[-1][amount] + row[amount - coin])
        table.append(row)
    return table


def expected_table(parts):
    if parts["variant"] == "knapsack":
        return knapsack_table(parts)
    if parts["variant"] == "lcs":
        return lcs_table(parts)
    if parts["variant"] == "edit_distance":
        return edit_distance_table(parts)
    return coin_change_table(parts)


def oracle_answer(example):
    parts = parse_problem(example["problem"])
    table = expected_table(parts)
    if parts["variant"] == "knapsack":
        return f"maximum value = {table[-1][parts['capacity']]}"
    if parts["variant"] == "lcs":
        return f"LCS length = {table[-1][-1]}"
    if parts["variant"] == "edit_distance":
        return f"edit distance = {table[-1][-1]}"
    return f"ways = {table[-1][parts['target']]}"


def cell_value(parts, table, coord):
    if parts["variant"] == "knapsack":
        match = re.fullmatch(r"i=(\d+),c=(\d+)", coord)
    elif parts["variant"] == "coin_change":
        match = re.fullmatch(r"i=(\d+),amount=(\d+)", coord)
    else:
        match = re.fullmatch(r"i=(\d+),j=(\d+)", coord)
    if match is None:
        return None
    i, j = map(int, match.groups())
    if i < 0 or i >= len(table) or j < 0 or j >= len(table[i]):
        return None
    return table[i][j]


def check_steps(example):
    parts = parse_problem(example["problem"])
    table = expected_table(parts)
    seen_rows = set()

    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "DP_SETUP":
            if parts["variant"] == "knapsack":
                if fields[1:] != ["0/1 knapsack",
                                  f"capacity {parts['capacity']}"]:
                    return False
            elif parts["variant"] == "lcs":
                if fields[1:] != ["LCS", f"X={parts['x']}",
                                  f"Y={parts['y']}"]:
                    return False
            elif parts["variant"] == "edit_distance":
                if fields[1:] != ["edit distance",
                                  f"source={parts['source']}",
                                  f"target={parts['target']}"]:
                    return False
            else:
                if fields[1:] != ["coin change", f"target {parts['target']}"]:
                    return False
        elif op == "DP_ITEMS":
            if fields[1] != item_text(parts["items"]):
                return False
        elif op == "DP_COINS":
            if fields[1] != coin_text(parts["coins"]):
                return False
        elif op == "DP_ROW":
            match = re.fullmatch(r"i=(\d+)", fields[1])
            if match is None:
                return False
            row_idx = int(match.group(1))
            if row_idx >= len(table):
                return False
            if fields[2] != row_text(table[row_idx]):
                return False
            seen_rows.add(row_idx)
        elif op == "DP_CELL":
            value = cell_value(parts, table, fields[1])
            if value is None or int(fields[3]) != value:
                return False
        elif op == "A":
            if int(fields[1]) + int(fields[2]) != int(fields[3]):
                return False
        elif op == "MAX":
            if max(int(fields[1]), int(fields[2])) != int(fields[3]):
                return False
        elif op == "MIN3":
            candidates = [int(fields[1]), int(fields[2]), int(fields[3])]
            if min(candidates) != int(fields[4]):
                return False
        elif op == "Z":
            if fields[1:] != [oracle_answer(example)]:
                return False
    return seen_rows == set(range(len(table)))


class TestDPTableGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DPTableGenerator()

    def test_output_contract(self):
        result = self.gen.generate()
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer"):
            self.assertIn(key, result)
        self.assertTrue(result["steps"][-1].startswith(f"Z{DELIM}"))
        self.assertEqual(result["steps"][-1].split(DELIM, 1)[1],
                         result["final_answer"])

    def test_oracle_answer_from_problem_text(self):
        for _ in range(500):
            result = self.gen.generate()
            self.assertEqual(result["final_answer"], oracle_answer(result),
                             result["problem"])

    def test_step_content_and_arithmetic(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_steps(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("knapsack", "lcs", "edit_distance", "coin_change"):
            gen = DPTableGenerator(variant)
            for _ in range(40):
                result = gen.generate()
                self.assertEqual(result["operation"], f"dp_table_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DPTableGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
