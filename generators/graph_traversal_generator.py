import random

from base_generator import ProblemGenerator
from helpers import step, jid


LABELS = ["A", "B", "C", "D", "E", "F"]


def edge_name(edge):
    return "".join(edge)


def undirected_graph():
    n = random.randint(4, 6)
    vertices = LABELS[:n]
    edges = set()
    for i in range(1, n):
        edges.add(tuple(sorted((vertices[i], random.choice(vertices[:i])))))
    possible = [
        (vertices[i], vertices[j])
        for i in range(n)
        for j in range(i + 1, n)
        if (vertices[i], vertices[j]) not in edges
    ]
    for edge in random.sample(possible, random.randint(1, min(n, len(possible)))):
        edges.add(edge)
    adjacency = {vertex: [] for vertex in vertices}
    for u, v in sorted(edges):
        adjacency[u].append(v)
        adjacency[v].append(u)
    for vertex in vertices:
        adjacency[vertex].sort()
    return vertices, sorted(edges), adjacency


def dag_graph():
    n = random.randint(4, 6)
    vertices = LABELS[:n]
    edges = set()
    for i in range(n - 1):
        edges.add((vertices[i], vertices[i + 1]))
    for i in range(n):
        for j in range(i + 2, n):
            if random.random() < 0.35:
                edges.add((vertices[i], vertices[j]))
    adjacency = {vertex: [] for vertex in vertices}
    for u, v in sorted(edges):
        adjacency[u].append(v)
    return vertices, sorted(edges), adjacency


def edge_list_text(edges, directed=False):
    if directed:
        return ", ".join(f"{u}->{v}" for u, v in edges)
    return ", ".join(edge_name(edge) for edge in edges)


def list_text(values):
    return ", ".join(values) if values else "empty"


class GraphTraversalGenerator(ProblemGenerator):
    """
    BFS/DFS visit orders and topological sorting traces.

    Variants:
    - bfs: queue trace from a start vertex
    - dfs: recursive depth-first trace from a start vertex
    - topo: Kahn topological sort with alphabetical tie-breaking

    Op-codes used:
    - GRAPH_SETUP / ADJ_LIST: graph setup
    - QUEUE_STATE / ENQUEUE / VISIT: BFS trace
    - DFS_EDGE: DFS tree and skip edges
    - INDEGREE / TOPO_AVAILABLE / TOPO_SELECT / INDEGREE_UPDATE / TOPO_READY:
      topological-sort trace
    - S (established): indegree decrement
    - Z: final order
    """

    VARIANTS = ["bfs", "dfs", "topo"]

    def __init__(self, variant=None):
        if variant is not None and variant not in self.VARIANTS:
            raise ValueError(f"variant must be one of {self.VARIANTS} or None")
        self.variant = variant

    def generate(self) -> dict:
        variant = self.variant or random.choice(self.VARIANTS)

        if variant in ("bfs", "dfs"):
            vertices, edges, adjacency = undirected_graph()
            start = random.choice(vertices)
            steps = [
                step("GRAPH_SETUP", "undirected graph",
                     f"vertices {', '.join(vertices)}"),
            ]
            for vertex in vertices:
                steps.append(step("ADJ_LIST", vertex, list_text(adjacency[vertex])))

            if variant == "bfs":
                visited = {start}
                queue = [start]
                order = []
                steps.append(step("QUEUE_STATE", "initial", list_text(queue)))
                while queue:
                    current = queue.pop(0)
                    steps.append(step("QUEUE_STATE", f"front {current}",
                                      list_text([current] + queue)))
                    order.append(current)
                    steps.append(step("VISIT", current, list_text(order)))
                    for neighbor in adjacency[current]:
                        if neighbor in visited:
                            continue
                        visited.add(neighbor)
                        queue.append(neighbor)
                        steps.append(step("ENQUEUE", neighbor,
                                          f"from {current}",
                                          list_text(queue)))
                answer = f"BFS order = {list_text(order)}"
                problem = (
                    f"Run BFS from {start} on the undirected graph with "
                    f"vertices {', '.join(vertices)} and edges "
                    f"{edge_list_text(edges)}. Visit neighbors in "
                    f"alphabetical order."
                )
            else:
                visited = set()
                order = []

                def dfs(vertex):
                    visited.add(vertex)
                    order.append(vertex)
                    steps.append(step("VISIT", vertex, list_text(order)))
                    for neighbor in adjacency[vertex]:
                        if neighbor in visited:
                            steps.append(step("DFS_EDGE",
                                              f"{vertex}->{neighbor}",
                                              "skip visited"))
                        else:
                            steps.append(step("DFS_EDGE",
                                              f"{vertex}->{neighbor}",
                                              "tree"))
                            dfs(neighbor)

                dfs(start)
                answer = f"DFS order = {list_text(order)}"
                problem = (
                    f"Run DFS from {start} on the undirected graph with "
                    f"vertices {', '.join(vertices)} and edges "
                    f"{edge_list_text(edges)}. Visit neighbors in "
                    f"alphabetical order."
                )
        else:
            vertices, edges, adjacency = dag_graph()
            indegree = {vertex: 0 for vertex in vertices}
            for u, v in edges:
                indegree[v] += 1
            steps = [
                step("GRAPH_SETUP", "directed acyclic graph",
                     f"vertices {', '.join(vertices)}"),
            ]
            for vertex in vertices:
                steps.append(step("ADJ_LIST", vertex, list_text(adjacency[vertex])))
            for vertex in vertices:
                steps.append(step("INDEGREE", vertex, indegree[vertex]))

            available = [vertex for vertex in vertices if indegree[vertex] == 0]
            order = []
            while available:
                available.sort()
                steps.append(step("TOPO_AVAILABLE", list_text(available)))
                current = available.pop(0)
                order.append(current)
                steps.append(step("TOPO_SELECT", current, list_text(order)))
                for neighbor in adjacency[current]:
                    old = indegree[neighbor]
                    new = old - 1
                    steps.append(step("S", old, 1, new))
                    indegree[neighbor] = new
                    steps.append(step("INDEGREE_UPDATE", neighbor, new))
                    if new == 0:
                        available.append(neighbor)
                        steps.append(step("TOPO_READY", neighbor))
            answer = f"topological order = {list_text(order)}"
            problem = (
                f"Find a topological order for the DAG with vertices "
                f"{', '.join(vertices)} and directed edges "
                f"{edge_list_text(edges, directed=True)}. Break ties "
                f"alphabetically."
            )

        steps.append(step("Z", answer))
        return dict(
            problem_id=jid(),
            operation=f"graph_traversal_{variant}",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
