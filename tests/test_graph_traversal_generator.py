import os
import random
import re
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.graph_traversal_generator import GraphTraversalGenerator
from helpers import DELIM


UNDIRECTED_RE = re.compile(
    r"Run (BFS|DFS) from ([A-Z]) on the undirected graph with vertices "
    r"([A-Z](?:, [A-Z])*) and edges ([A-Z]{2}(?:, [A-Z]{2})*)\. "
    r"Visit neighbors in alphabetical order\."
)
TOPO_RE = re.compile(
    r"Find a topological order for the DAG with vertices "
    r"([A-Z](?:, [A-Z])*) and directed edges "
    r"([A-Z]->[A-Z](?:, [A-Z]->[A-Z])*)\. Break ties alphabetically\."
)


def list_text(values):
    return ", ".join(values) if values else "empty"


def parse_problem(problem):
    match = UNDIRECTED_RE.fullmatch(problem)
    if match:
        kind, start, vertices_text, edges_text = match.groups()
        vertices = vertices_text.split(", ")
        adjacency = {vertex: [] for vertex in vertices}
        edges = [tuple(edge) for edge in edges_text.split(", ")]
        for u, v in edges:
            adjacency[u].append(v)
            adjacency[v].append(u)
        for vertex in vertices:
            adjacency[vertex].sort()
        return {"variant": kind.lower(), "start": start,
                "vertices": vertices, "edges": edges,
                "adjacency": adjacency}
    match = TOPO_RE.fullmatch(problem)
    assert match is not None, problem
    vertices = match.group(1).split(", ")
    edges = []
    adjacency = {vertex: [] for vertex in vertices}
    for item in match.group(2).split(", "):
        u, v = item.split("->")
        edges.append((u, v))
        adjacency[u].append(v)
    for vertex in vertices:
        adjacency[vertex].sort()
    return {"variant": "topo", "vertices": vertices, "edges": edges,
            "adjacency": adjacency}


def bfs_order(parts):
    visited = {parts["start"]}
    queue = [parts["start"]]
    order = []
    while queue:
        current = queue.pop(0)
        order.append(current)
        for neighbor in parts["adjacency"][current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def dfs_order(parts):
    visited = set()
    order = []

    def dfs(vertex):
        visited.add(vertex)
        order.append(vertex)
        for neighbor in parts["adjacency"][vertex]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(parts["start"])
    return order


def topo_order(parts):
    indegree = {vertex: 0 for vertex in parts["vertices"]}
    for _, v in parts["edges"]:
        indegree[v] += 1
    available = [vertex for vertex in parts["vertices"] if indegree[vertex] == 0]
    order = []
    while available:
        available.sort()
        current = available.pop(0)
        order.append(current)
        for neighbor in parts["adjacency"][current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                available.append(neighbor)
    return order


def expected_order(parts):
    if parts["variant"] == "bfs":
        return bfs_order(parts)
    if parts["variant"] == "dfs":
        return dfs_order(parts)
    return topo_order(parts)


def oracle_answer(example):
    parts = parse_problem(example["problem"])
    order = expected_order(parts)
    if parts["variant"] == "bfs":
        return f"BFS order = {list_text(order)}"
    if parts["variant"] == "dfs":
        return f"DFS order = {list_text(order)}"
    return f"topological order = {list_text(order)}"


def check_steps(example):
    parts = parse_problem(example["problem"])
    order = expected_order(parts)
    selected_prefix = []
    for raw_step in example["steps"]:
        fields = raw_step.split(DELIM)
        op = fields[0]
        if op == "ADJ_LIST":
            vertex = fields[1]
            if fields[2] != list_text(parts["adjacency"][vertex]):
                return False
        elif op == "VISIT":
            selected_prefix.append(fields[1])
            if fields[2] != list_text(selected_prefix):
                return False
            if selected_prefix != order[:len(selected_prefix)]:
                return False
        elif op == "TOPO_SELECT":
            selected_prefix.append(fields[1])
            if fields[2] != list_text(selected_prefix):
                return False
            if selected_prefix != order[:len(selected_prefix)]:
                return False
        elif op == "DFS_EDGE":
            u, v = fields[1].split("->")
            if v not in parts["adjacency"][u]:
                return False
            if fields[2] not in ("tree", "skip visited"):
                return False
        elif op == "S":
            if int(fields[1]) - int(fields[2]) != int(fields[3]):
                return False
        elif op == "Z":
            if fields[1:] != [oracle_answer(example)]:
                return False
    return True


class TestGraphTraversalGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.gen = GraphTraversalGenerator()

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

    def test_step_content(self):
        for _ in range(300):
            result = self.gen.generate()
            self.assertTrue(check_steps(result), result["steps"])

    def test_variants_are_available(self):
        for variant in ("bfs", "dfs", "topo"):
            gen = GraphTraversalGenerator(variant)
            for _ in range(50):
                result = gen.generate()
                self.assertEqual(result["operation"],
                                 f"graph_traversal_{variant}")
                self.assertEqual(parse_problem(result["problem"])["variant"],
                                 variant)

    def test_invalid_variant_rejected(self):
        with self.assertRaises(ValueError):
            GraphTraversalGenerator("bogus")

    def test_pipe_safe(self):
        for _ in range(300):
            result = self.gen.generate()
            for raw_step in result["steps"]:
                self.assertLessEqual(len(raw_step.split(DELIM)) - 1, 4,
                                     raw_step)
            self.assertNotIn(DELIM, result["final_answer"])


if __name__ == "__main__":
    unittest.main()
