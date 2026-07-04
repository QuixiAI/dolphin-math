import random

from base_generator import ProblemGenerator
from helpers import step, jid


LABELS = ["A", "B", "C", "D", "E", "F"]


def make_weighted_graph():
    n = random.randint(4, 6)
    vertices = LABELS[:n]
    edges = {}

    for i in range(1, n):
        u = vertices[i]
        v = random.choice(vertices[:i])
        edges[tuple(sorted((u, v)))] = random.randint(1, 9)

    possible = [
        (vertices[i], vertices[j])
        for i in range(n)
        for j in range(i + 1, n)
        if (vertices[i], vertices[j]) not in edges
    ]
    for edge in random.sample(possible, random.randint(1, min(4, len(possible)))):
        edges[edge] = random.randint(1, 9)

    edge_items = sorted(edges.items())
    adjacency = {vertex: {} for vertex in vertices}
    for (u, v), weight in edge_items:
        adjacency[u][v] = weight
        adjacency[v][u] = weight
    return vertices, edge_items, adjacency


def edge_list_text(edge_items):
    return ", ".join(f"{u}{v}={weight}" for (u, v), weight in edge_items)


def dist_value(value):
    return "inf" if value is None else str(value)


def dist_table(vertices, distances):
    return ", ".join(f"{vertex}={dist_value(distances[vertex])}"
                     for vertex in vertices)


class DijkstraGenerator(ProblemGenerator):
    """
    Dijkstra shortest paths with a full distance-table trace.

    Op-codes used:
    - GRAPH_SETUP / EDGE_WEIGHT: weighted graph setup
    - DIJKSTRA_INIT: initial tentative distances
    - SELECT_MIN: next unvisited vertex with smallest tentative distance
    - RELAX: edge relaxation outcome
    - DIST_TABLE: full tentative-distance table after each selection
    - A (established): candidate distance arithmetic
    - Z: final shortest-distance table
    """

    VARIANTS = ["trace"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or "trace"
        vertices, edge_items, adjacency = make_weighted_graph()
        start = random.choice(vertices)
        distances = {vertex: None for vertex in vertices}
        distances[start] = 0
        unvisited = set(vertices)
        steps = [
            step("GRAPH_SETUP", "weighted undirected graph",
                 f"vertices {', '.join(vertices)}"),
        ]
        for (u, v), weight in edge_items:
            steps.append(step("EDGE_WEIGHT", f"{u}{v}", weight))
        steps.append(step("DIJKSTRA_INIT", f"start {start}",
                          dist_table(vertices, distances)))

        visited = []
        while unvisited:
            current = min(
                unvisited,
                key=lambda vertex: (
                    distances[vertex] is None,
                    10 ** 9 if distances[vertex] is None else distances[vertex],
                    vertices.index(vertex),
                ),
            )
            if distances[current] is None:
                break
            steps.append(step("SELECT_MIN", current, distances[current]))
            unvisited.remove(current)
            visited.append(current)
            for neighbor in sorted(adjacency[current], key=vertices.index):
                if neighbor not in unvisited:
                    continue
                weight = adjacency[current][neighbor]
                candidate = distances[current] + weight
                steps.append(step("A", distances[current], weight, candidate))
                old = distances[neighbor]
                if old is None or candidate < old:
                    distances[neighbor] = candidate
                    steps.append(step("RELAX", f"{current}->{neighbor}",
                                      f"update {dist_value(old)} to {candidate}",
                                      f"via weight {weight}"))
                else:
                    steps.append(step("RELAX", f"{current}->{neighbor}",
                                      f"keep {old}",
                                      f"candidate {candidate}"))
            steps.append(step("DIST_TABLE", f"visited {', '.join(visited)}",
                              dist_table(vertices, distances)))

        answer = (
            "distances = "
            + ", ".join(f"{vertex}:{distances[vertex]}" for vertex in vertices)
        )
        problem = (
            f"Use Dijkstra's algorithm on the weighted undirected graph with "
            f"vertices {', '.join(vertices)} and edges {edge_list_text(edge_items)}. "
            f"Start at {start} and find shortest distances to all vertices."
        )
        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"dijkstra_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
