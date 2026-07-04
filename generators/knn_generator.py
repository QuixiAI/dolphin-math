import random

from base_generator import ProblemGenerator
from helpers import step, jid


LABELS = ["A", "B"]
K = 3
TRAIN_COUNT = 5


def point_text(point):
    return f"({point[0]},{point[1]})"


def training_text(points):
    return ", ".join(
        f"P{index}=({point[0]},{point[1]},{label})"
        for index, (point, label) in enumerate(points, start=1)
    )


def squared_distance(left, right):
    dx = left[0] - right[0]
    dy = left[1] - right[1]
    return dx * dx + dy * dy


def neighbor_text(rows):
    return ",".join(
        f"P{index}:{distance}:{label}" for distance, index, label in rows
    )


class KNNGenerator(ProblemGenerator):
    """
    k-nearest-neighbor classification with an explicit squared-distance table.

    Five labeled 2D training points are compared to one query point; the three
    nearest labels are counted to make the classification.

    Op-codes used:
    - KNN_SETUP / KNN_DISTANCE / KNN_SORT / KNN_NEIGHBORS / LABEL_COUNT
    - CHECK (established): compare class vote counts
    - S / E / A (established/shared): squared Euclidean distance arithmetic
    - Z: predicted class and nearest neighbors
    """

    def generate(self) -> dict:
        grid = [(x, y) for x in range(-5, 6) for y in range(-5, 6)]
        for _ in range(100):
            query = random.choice(grid)
            raw_points = random.sample([point for point in grid if point != query],
                                       TRAIN_COUNT)
            labels = [random.choice(LABELS) for _ in range(TRAIN_COUNT)]
            points = list(zip(raw_points, labels))
            distances = [
                squared_distance(point, query)
                for point, _ in points
            ]
            if len(set(distances)) == len(distances):
                break
        else:
            query = (0, 0)
            points = [
                ((-1, 0), "A"),
                ((1, 0), "A"),
                ((0, 2), "B"),
                ((4, 0), "B"),
                ((0, -5), "B"),
            ]

        steps = [
            step("KNN_SETUP", f"q={point_text(query)}", f"k={K}",
                 f"training={training_text(points)}"),
        ]
        rows = []
        for index, (point, label) in enumerate(points, start=1):
            dx = query[0] - point[0]
            dy = query[1] - point[1]
            dx2 = dx ** 2
            dy2 = dy ** 2
            dist2 = dx2 + dy2
            steps.extend([
                step("S", query[0], point[0], dx),
                step("E", dx, 2, dx2),
                step("S", query[1], point[1], dy),
                step("E", dy, 2, dy2),
                step("A", dx2, dy2, dist2),
                step("KNN_DISTANCE", f"P{index}", f"label={label}",
                     f"d2={dist2}"),
            ])
            rows.append((dist2, index, label))

        rows.sort(key=lambda item: (item[0], item[1]))
        neighbors = rows[:K]
        counts = {
            label: sum(1 for _, _, neighbor_label in neighbors
                       if neighbor_label == label)
            for label in LABELS
        }
        prediction = "A" if counts["A"] > counts["B"] else "B"
        relation = ">" if prediction == "A" else "<"
        steps.extend([
            step("KNN_SORT", neighbor_text(rows)),
            step("KNN_NEIGHBORS", neighbor_text(neighbors)),
            step("LABEL_COUNT", "A", counts["A"]),
            step("LABEL_COUNT", "B", counts["B"]),
            step("CHECK", "A vs B",
                 f"{counts['A']} {relation} {counts['B']}",
                 f"predict={prediction}"),
        ])
        neighbor_labels = ",".join(
            f"P{index}:{label}" for _, index, label in neighbors
        )
        answer = f"class={prediction}; neighbors={neighbor_labels}"
        steps.append(step("Z", answer))
        problem = (
            f"Classify query q={point_text(query)} by {K}-NN using squared "
            f"Euclidean distance. Training points: {training_text(points)}."
        )
        return dict(
            problem_id=jid(),
            operation="knn_classification",
            problem=problem,
            steps=steps,
            final_answer=answer,
        )
