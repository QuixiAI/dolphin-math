import random
from base_generator import ProblemGenerator
from helpers import step, jid


class SimpleStatsGenerator(ProblemGenerator):
    """Computes mean, median, and mode for small integer datasets."""

    def generate(self) -> dict:
        data = [random.randint(1, 20) for _ in range(random.randint(5, 9))]
        target = random.choice(["mean", "median", "mode"])
        steps = []

        # Sort for median/mode clarity
        sorted_data = sorted(data)
        steps.append(step("SORT", ",".join(map(str, data)), ",".join(map(str, sorted_data))))

        if target == "mean":
            total = 0
            for val in sorted_data:
                new_total = total + val
                steps.append(step("A", total, val, new_total))
                total = new_total
            steps.append(step("MEAN_DIV", total, len(sorted_data), total / len(sorted_data)))
            final_answer = f"{total / len(sorted_data):.2f}"
            operation = "mean"
            problem = f"Find mean of {sorted_data}"

        elif target == "median":
            n = len(sorted_data)
            mid = n // 2
            if n % 2 == 1:
                median = sorted_data[mid]
                steps.append(step("MEDIAN_PICK", sorted_data[mid], "", median))
            else:
                pair = (sorted_data[mid - 1], sorted_data[mid])
                steps.append(step("MEDIAN_PAIR", pair[0], pair[1]))
                median = (pair[0] + pair[1]) / 2
                steps.append(step("MEAN_DIV", pair[0] + pair[1], 2, median))
            final_answer = str(median)
            operation = "median"
            problem = f"Find median of {sorted_data}"

        else:  # mode
            freq = {}
            for val in sorted_data:
                freq[val] = freq.get(val, 0) + 1
                steps.append(step("MODE_COUNT", val, freq[val]))
            max_freq = max(freq.values())
            modes = [k for k, v in freq.items() if v == max_freq]
            final_answer = ", ".join(map(str, modes))
            steps.append(step("MODE", max_freq, final_answer))
            operation = "mode"
            problem = f"Find mode of {sorted_data}"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
