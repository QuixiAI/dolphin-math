import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.dijkstra_generator import DijkstraGenerator
from helpers import DELIM


PROBLEM_RE = re.compile(
    r"Use Dijkstra's algorithm on the weighted undirected graph with vertices "
    r"([A-Z](?:, [A-Z])*) and edges ([A-Z]{2}=\d+(?:, [A-Z]{2}=\d+)*). "
    r"Start at ([A-Z]) and find shortest distances to all vertices\."
)


def parse_problem(problem):
    match = PROBLEM_RE.fullmatch(problem)
    assert match is not None, problem
    vertices = match.group(1).split(", ")
    edge_items = []
    adjacency = {vertex: {} for vertex in vertices}
    for item in match.group(2).split(", "):
        edge, weight_text = item.split("=")
        u, v = edge
        weight = int(weight_text)
        edge_items.append(((u, v), weight))
        adjacency[u][v] = weight
        adjacency[v][u] = weight
    return {
        "vertices": vertices,
        "edges": dict(edge_items),
        "adjacency": adjacency,
        "start": match.group(3),
    }


def brute_force_distances(parts):
    vertices = parts["vertices"]
    adjacency = parts["adjacency"]
    start = parts["start"]
    distances = {}

    def visit(current, target, seen, total):
        if current == target:
            return total
        best = None
        for neighbor, weight in adjacency[current].items():
            if neighbor in seen:
                continue
            value = visit(neighbor, target, seen | {neighbor}, total + weight)
            if value is not None and (best is None or value < best):
                best = value
        return best

    for vertex in vertices:
        distances[vertex] = visit(start, vertex, {start}, 0)
    return distances


def oracle_answer(example):
    parts = parse_problem(example["problem"])
    distances = brute_force_distances(parts)
    return (
        "distances = "
        + ", ".join(f"{vertex}:{distances[vertex]}"
                    for vertex in parts["vertices"])
    )


def parse_table(text):
    values = {}
    for item in text.split(", "):
        vertex, value = item.split("=")
        values[vertex] = None if value == "inf" else int(value)
    return values


def dist_value(value):
    return "inf" if value is None else str(value)


def check_trace(example):
    parts = parse_problem(example["problem"])
    vertices = parts["vertices"]
    adjacency = parts["adjacency"]
    distances = {vertex: None for vertex in vertices}
    distances[parts["start"]] = 0
    unvisited = set(vertices)
    visited = []
    current = None
    pending_candidate = None

    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "EDGE_WEIGHT":
            edge = tuple(fields[1])
            if parts["edges"][edge] != int(fields[2]):
                return False
        elif op == "DIJKSTRA_INIT":
            if fields[1] != f"start {parts['start']}":
                return False
            if parse_table(fields[2]) != distances:
                return False
        elif op == "SELECT_MIN":
            selected = fields[1]
            value = int(fields[2])
            expected = min(
                unvisited,
                key=lambda vertex: (
                    distances[vertex] is None,
                    10 ** 9 if distances[vertex] is None else distances[vertex],
                    vertices.index(vertex),
                ),
            )
            if selected != expected or distances[selected] != value:
                return False
            current = selected
            unvisited.remove(current)
            visited.append(current)
        elif op == "A":
            left, right, total = map(int, fields[1:])
            if left + right != total:
                return False
            pending_candidate = total
        elif op == "RELAX":
            match = re.fullmatch(r"([A-Z])->([A-Z])", fields[1])
            if match is None:
                return False
            u, v = match.groups()
            if u != current or v not in unvisited:
                return False
            weight = adjacency[u][v]
            candidate = distances[u] + weight
            if candidate != pending_candidate:
                return False
            old = distances[v]
            if old is None or candidate < old:
                if fields[2:] != [
                    f"update {dist_value(old)} to {candidate}",
                    f"via weight {weight}",
                ]:
                    return False
                distances[v] = candidate
            else:
                if fields[2:] != [f"keep {old}", f"candidate {candidate}"]:
                    return False
        elif op == "DIST_TABLE":
            if fields[1] != f"visited {', '.join(visited)}":
                return False
            if parse_table(fields[2]) != distances:
                return False
        elif op == "Z":
            if fields[1:] != [oracle_answer(example)]:
                return False
    return True


class TestDijkstraGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = DijkstraGenerator()

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

    def test_trace_steps(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_trace(result), result["steps"])

    def test_variant_constructor(self):
        gen = DijkstraGenerator("trace")
        result = gen.generate()
        self.assertEqual(result["operation"], "dijkstra_trace")
        self.assertEqual(result["final_answer"], oracle_answer(result))

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            DijkstraGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
