import random
from base_generator import ProblemGenerator
from helpers import step, jid


class GraphInterpretGenerator(ProblemGenerator):
    """
    Generates problems for reading and interpreting bar charts, line graphs,
    and pictographs. Problems include finding values, comparing categories,
    calculating totals, differences, and identifying min/max.
    """

    def __init__(self, graph_type: str = None):
        """
        Initialize with optional graph type.

        Args:
            graph_type: One of 'bar', 'line', 'pictograph', or None for random.
        """
        self.graph_type = graph_type

    def generate(self) -> dict:
        graph_type = self.graph_type or random.choice(["bar", "line", "pictograph"])

        if graph_type == "bar":
            return self._generate_bar_chart()
        elif graph_type == "line":
            return self._generate_line_graph()
        else:
            return self._generate_pictograph()

    def _generate_bar_chart(self) -> dict:
        """Generate a bar chart interpretation problem."""
        # Create random categorical data
        categories = self._get_categories("bar")
        num_categories = random.randint(4, 6)
        selected = random.sample(categories, num_categories)
        values = {cat: random.randint(5, 50) for cat in selected}

        # Choose question type
        question_type = random.choice([
            "read_value", "compare", "total", "difference", "max", "min"
        ])

        return self._create_bar_problem(values, question_type)

    def _generate_line_graph(self) -> dict:
        """Generate a line graph interpretation problem."""
        # Create time-series data
        time_labels = self._get_time_labels()
        num_points = random.randint(5, 8)
        selected_times = time_labels[:num_points]

        # Generate values with some trend
        start_val = random.randint(10, 30)
        values = {}
        current = start_val
        for t in selected_times:
            values[t] = current
            change = random.randint(-5, 8)
            current = max(5, current + change)

        # Choose question type
        question_type = random.choice([
            "read_value", "increase", "decrease", "max", "min", "range"
        ])

        return self._create_line_problem(values, selected_times, question_type)

    def _generate_pictograph(self) -> dict:
        """Generate a pictograph interpretation problem."""
        categories = self._get_categories("pictograph")
        num_categories = random.randint(3, 5)
        selected = random.sample(categories, num_categories)

        # Each symbol represents a value
        symbol_value = random.choice([2, 5, 10])
        symbols = ["★", "●", "■", "▲", "♦"]
        symbol = random.choice(symbols)

        # Generate symbol counts (1-8 symbols per category)
        symbol_counts = {cat: random.randint(1, 8) for cat in selected}
        actual_values = {cat: count * symbol_value for cat, count in symbol_counts.items()}

        # Choose question type
        question_type = random.choice([
            "read_value", "compare", "total", "difference", "max"
        ])

        return self._create_pictograph_problem(
            symbol_counts, actual_values, symbol, symbol_value, question_type
        )

    def _get_categories(self, context: str) -> list:
        """Return appropriate category names based on context."""
        if context == "bar":
            category_sets = [
                ["Apples", "Oranges", "Bananas", "Grapes", "Strawberries", "Peaches"],
                ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"],
                ["Math", "Science", "English", "History", "Art", "Music"],
                ["Soccer", "Basketball", "Baseball", "Tennis", "Swimming", "Football"],
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            ]
        else:  # pictograph
            category_sets = [
                ["Dogs", "Cats", "Birds", "Fish", "Hamsters"],
                ["Pizza", "Burgers", "Tacos", "Pasta", "Salad"],
                ["Bikes", "Cars", "Buses", "Trains", "Planes"],
                ["Lions", "Tigers", "Bears", "Elephants", "Giraffes"],
            ]
        return random.choice(category_sets)

    def _get_time_labels(self) -> list:
        """Return time-based labels for line graphs."""
        label_sets = [
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"],
            ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8"],
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon2"],
            ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"],
            ["9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm"],
        ]
        return random.choice(label_sets)

    def _format_bar_chart(self, values: dict) -> str:
        """Format bar chart data as text representation."""
        lines = ["Bar Chart Data:"]
        for cat, val in values.items():
            lines.append(f"  {cat}: {val}")
        return "\n".join(lines)

    def _format_line_graph(self, values: dict, times: list) -> str:
        """Format line graph data as text representation."""
        lines = ["Line Graph Data:"]
        for t in times:
            lines.append(f"  {t}: {values[t]}")
        return "\n".join(lines)

    def _format_pictograph(self, symbol_counts: dict, symbol: str, symbol_value: int) -> str:
        """Format pictograph data as text representation."""
        lines = [f"Pictograph (each {symbol} = {symbol_value}):"]
        for cat, count in symbol_counts.items():
            symbols_str = symbol * count
            lines.append(f"  {cat}: {symbols_str}")
        return "\n".join(lines)

    def _create_bar_problem(self, values: dict, question_type: str) -> dict:
        """Create a bar chart problem with steps."""
        steps = []
        categories = list(values.keys())
        chart_repr = self._format_bar_chart(values)

        # Record the graph data
        steps.append(step("GRAPH_DATA", "bar_chart", ",".join(f"{k}:{v}" for k, v in values.items())))

        if question_type == "read_value":
            target = random.choice(categories)
            value = values[target]
            steps.append(step("GRAPH_READ", target, value))
            final_answer = str(value)
            problem = f"{chart_repr}\n\nQuestion: What is the value for {target}?"
            operation = "bar_chart_read"

        elif question_type == "compare":
            cat1, cat2 = random.sample(categories, 2)
            v1, v2 = values[cat1], values[cat2]
            steps.append(step("GRAPH_READ", cat1, v1))
            steps.append(step("GRAPH_READ", cat2, v2))
            if v1 > v2:
                relation = "greater"
                diff = v1 - v2
                steps.append(step("S", v1, v2, diff))
                final_answer = f"{cat1} is greater by {diff}"
            elif v1 < v2:
                relation = "less"
                diff = v2 - v1
                steps.append(step("S", v2, v1, diff))
                final_answer = f"{cat2} is greater by {diff}"
            else:
                relation = "equal"
                final_answer = f"{cat1} and {cat2} are equal"
            steps.append(step("CMP", cat1, cat2, relation))
            problem = f"{chart_repr}\n\nQuestion: Compare {cat1} and {cat2}. Which is greater and by how much?"
            operation = "bar_chart_compare"

        elif question_type == "total":
            total = 0
            for cat in categories:
                v = values[cat]
                steps.append(step("GRAPH_READ", cat, v))
                new_total = total + v
                steps.append(step("A", total, v, new_total))
                total = new_total
            final_answer = str(total)
            problem = f"{chart_repr}\n\nQuestion: What is the total of all values?"
            operation = "bar_chart_total"

        elif question_type == "difference":
            cat1, cat2 = random.sample(categories, 2)
            v1, v2 = values[cat1], values[cat2]
            steps.append(step("GRAPH_READ", cat1, v1))
            steps.append(step("GRAPH_READ", cat2, v2))
            diff = abs(v1 - v2)
            if v1 >= v2:
                steps.append(step("S", v1, v2, diff))
            else:
                steps.append(step("S", v2, v1, diff))
            final_answer = str(diff)
            problem = f"{chart_repr}\n\nQuestion: What is the difference between {cat1} and {cat2}?"
            operation = "bar_chart_difference"

        elif question_type == "max":
            max_val = max(values.values())
            max_cat = [k for k, v in values.items() if v == max_val][0]
            for cat in categories:
                steps.append(step("GRAPH_READ", cat, values[cat]))
            steps.append(step("GRAPH_MAX", max_cat, max_val))
            final_answer = f"{max_cat} ({max_val})"
            problem = f"{chart_repr}\n\nQuestion: Which category has the highest value?"
            operation = "bar_chart_max"

        else:  # min
            min_val = min(values.values())
            min_cat = [k for k, v in values.items() if v == min_val][0]
            for cat in categories:
                steps.append(step("GRAPH_READ", cat, values[cat]))
            steps.append(step("GRAPH_MIN", min_cat, min_val))
            final_answer = f"{min_cat} ({min_val})"
            problem = f"{chart_repr}\n\nQuestion: Which category has the lowest value?"
            operation = "bar_chart_min"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

    def _create_line_problem(self, values: dict, times: list, question_type: str) -> dict:
        """Create a line graph problem with steps."""
        steps = []
        chart_repr = self._format_line_graph(values, times)

        # Record the graph data
        steps.append(step("GRAPH_DATA", "line_graph", ",".join(f"{k}:{v}" for k, v in values.items())))

        if question_type == "read_value":
            target = random.choice(times)
            value = values[target]
            steps.append(step("GRAPH_READ", target, value))
            final_answer = str(value)
            problem = f"{chart_repr}\n\nQuestion: What is the value at {target}?"
            operation = "line_graph_read"

        elif question_type == "increase":
            # Find largest increase between consecutive points
            max_increase = 0
            max_pair = (times[0], times[1])
            for i in range(len(times) - 1):
                t1, t2 = times[i], times[i + 1]
                increase = values[t2] - values[t1]
                steps.append(step("GRAPH_READ", t1, values[t1]))
                steps.append(step("GRAPH_READ", t2, values[t2]))
                steps.append(step("S", values[t2], values[t1], increase))
                steps.append(step("GRAPH_CHANGE", t1, t2, increase))
                if increase > max_increase:
                    max_increase = increase
                    max_pair = (t1, t2)
            steps.append(step("GRAPH_MAX_CHANGE", max_pair[0], max_pair[1], max_increase))
            final_answer = f"{max_pair[0]} to {max_pair[1]} (increase of {max_increase})"
            problem = f"{chart_repr}\n\nQuestion: Between which two consecutive time periods was there the largest increase?"
            operation = "line_graph_increase"

        elif question_type == "decrease":
            # Find largest decrease between consecutive points
            max_decrease = 0
            max_pair = (times[0], times[1])
            for i in range(len(times) - 1):
                t1, t2 = times[i], times[i + 1]
                decrease = values[t1] - values[t2]
                steps.append(step("GRAPH_READ", t1, values[t1]))
                steps.append(step("GRAPH_READ", t2, values[t2]))
                steps.append(step("S", values[t1], values[t2], decrease))
                steps.append(step("GRAPH_CHANGE", t1, t2, -decrease))
                if decrease > max_decrease:
                    max_decrease = decrease
                    max_pair = (t1, t2)
            if max_decrease > 0:
                steps.append(step("GRAPH_MAX_CHANGE", max_pair[0], max_pair[1], -max_decrease))
                final_answer = f"{max_pair[0]} to {max_pair[1]} (decrease of {max_decrease})"
            else:
                final_answer = "No decrease occurred"
            problem = f"{chart_repr}\n\nQuestion: Between which two consecutive time periods was there the largest decrease?"
            operation = "line_graph_decrease"

        elif question_type == "max":
            max_val = max(values.values())
            max_time = [t for t in times if values[t] == max_val][0]
            for t in times:
                steps.append(step("GRAPH_READ", t, values[t]))
            steps.append(step("GRAPH_MAX", max_time, max_val))
            final_answer = f"{max_time} ({max_val})"
            problem = f"{chart_repr}\n\nQuestion: At which time was the value highest?"
            operation = "line_graph_max"

        elif question_type == "min":
            min_val = min(values.values())
            min_time = [t for t in times if values[t] == min_val][0]
            for t in times:
                steps.append(step("GRAPH_READ", t, values[t]))
            steps.append(step("GRAPH_MIN", min_time, min_val))
            final_answer = f"{min_time} ({min_val})"
            problem = f"{chart_repr}\n\nQuestion: At which time was the value lowest?"
            operation = "line_graph_min"

        else:  # range
            max_val = max(values.values())
            min_val = min(values.values())
            for t in times:
                steps.append(step("GRAPH_READ", t, values[t]))
            steps.append(step("GRAPH_MAX", "max", max_val))
            steps.append(step("GRAPH_MIN", "min", min_val))
            range_val = max_val - min_val
            steps.append(step("S", max_val, min_val, range_val))
            final_answer = str(range_val)
            problem = f"{chart_repr}\n\nQuestion: What is the range (difference between highest and lowest values)?"
            operation = "line_graph_range"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )

    def _create_pictograph_problem(
        self, symbol_counts: dict, actual_values: dict, symbol: str,
        symbol_value: int, question_type: str
    ) -> dict:
        """Create a pictograph problem with steps."""
        steps = []
        categories = list(symbol_counts.keys())
        chart_repr = self._format_pictograph(symbol_counts, symbol, symbol_value)

        # Record the graph data and key
        steps.append(step("GRAPH_DATA", "pictograph", f"key:{symbol}={symbol_value}"))
        steps.append(step("PICTO_KEY", symbol, symbol_value))

        if question_type == "read_value":
            target = random.choice(categories)
            count = symbol_counts[target]
            value = actual_values[target]
            steps.append(step("PICTO_COUNT", target, count))
            steps.append(step("M", count, symbol_value, value))
            final_answer = str(value)
            problem = f"{chart_repr}\n\nQuestion: How many does {target} represent?"
            operation = "pictograph_read"

        elif question_type == "compare":
            cat1, cat2 = random.sample(categories, 2)
            c1, c2 = symbol_counts[cat1], symbol_counts[cat2]
            v1, v2 = actual_values[cat1], actual_values[cat2]
            steps.append(step("PICTO_COUNT", cat1, c1))
            steps.append(step("M", c1, symbol_value, v1))
            steps.append(step("PICTO_COUNT", cat2, c2))
            steps.append(step("M", c2, symbol_value, v2))
            if v1 > v2:
                diff = v1 - v2
                steps.append(step("S", v1, v2, diff))
                final_answer = f"{cat1} has {diff} more"
            elif v1 < v2:
                diff = v2 - v1
                steps.append(step("S", v2, v1, diff))
                final_answer = f"{cat2} has {diff} more"
            else:
                final_answer = f"{cat1} and {cat2} are equal"
            steps.append(step("CMP", cat1, cat2, "v1>v2" if v1 > v2 else ("v1<v2" if v1 < v2 else "equal")))
            problem = f"{chart_repr}\n\nQuestion: Compare {cat1} and {cat2}. Which has more and by how much?"
            operation = "pictograph_compare"

        elif question_type == "total":
            total = 0
            for cat in categories:
                count = symbol_counts[cat]
                value = actual_values[cat]
                steps.append(step("PICTO_COUNT", cat, count))
                steps.append(step("M", count, symbol_value, value))
                new_total = total + value
                steps.append(step("A", total, value, new_total))
                total = new_total
            final_answer = str(total)
            problem = f"{chart_repr}\n\nQuestion: What is the total represented by all categories?"
            operation = "pictograph_total"

        elif question_type == "difference":
            cat1, cat2 = random.sample(categories, 2)
            c1, c2 = symbol_counts[cat1], symbol_counts[cat2]
            v1, v2 = actual_values[cat1], actual_values[cat2]
            steps.append(step("PICTO_COUNT", cat1, c1))
            steps.append(step("M", c1, symbol_value, v1))
            steps.append(step("PICTO_COUNT", cat2, c2))
            steps.append(step("M", c2, symbol_value, v2))
            diff = abs(v1 - v2)
            if v1 >= v2:
                steps.append(step("S", v1, v2, diff))
            else:
                steps.append(step("S", v2, v1, diff))
            final_answer = str(diff)
            problem = f"{chart_repr}\n\nQuestion: What is the difference between {cat1} and {cat2}?"
            operation = "pictograph_difference"

        else:  # max
            max_val = max(actual_values.values())
            max_cat = [k for k, v in actual_values.items() if v == max_val][0]
            for cat in categories:
                count = symbol_counts[cat]
                value = actual_values[cat]
                steps.append(step("PICTO_COUNT", cat, count))
                steps.append(step("M", count, symbol_value, value))
            steps.append(step("GRAPH_MAX", max_cat, max_val))
            final_answer = f"{max_cat} ({max_val})"
            problem = f"{chart_repr}\n\nQuestion: Which category has the highest value?"
            operation = "pictograph_max"

        steps.append(step("Z", final_answer))

        return dict(
            problem_id=jid(),
            operation=operation,
            problem=problem,
            steps=steps,
            final_answer=final_answer,
        )
