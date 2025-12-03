import unittest
import sys
import os
import random

# Ensure repo root on path
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from generators.graph_interpret_generator import GraphInterpretGenerator
from helpers import DELIM


class TestGraphInterpretGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = GraphInterpretGenerator()
        self.bar_gen = GraphInterpretGenerator(graph_type="bar")
        self.line_gen = GraphInterpretGenerator(graph_type="line")
        self.picto_gen = GraphInterpretGenerator(graph_type="pictograph")

    def test_output_structure(self):
        """Test that output has all required keys and Z step."""
        for _ in range(10):
            res = self.gen.generate()
            self.assertIn("problem_id", res)
            self.assertIn("operation", res)
            self.assertIn("problem", res)
            self.assertIn("steps", res)
            self.assertIn("final_answer", res)
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))

    def test_bar_chart_generation(self):
        """Test bar chart problems are generated correctly."""
        random.seed(42)
        for _ in range(5):
            res = self.bar_gen.generate()
            self.assertIn("bar_chart", res["operation"])
            self.assertIn("Bar Chart Data:", res["problem"])
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
            # Verify GRAPH_DATA step exists
            graph_data_steps = [s for s in res["steps"] if s.startswith("GRAPH_DATA")]
            self.assertEqual(len(graph_data_steps), 1)
            self.assertIn("bar_chart", graph_data_steps[0])

    def test_line_graph_generation(self):
        """Test line graph problems are generated correctly."""
        random.seed(43)
        for _ in range(5):
            res = self.line_gen.generate()
            self.assertIn("line_graph", res["operation"])
            self.assertIn("Line Graph Data:", res["problem"])
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
            # Verify GRAPH_DATA step exists
            graph_data_steps = [s for s in res["steps"] if s.startswith("GRAPH_DATA")]
            self.assertEqual(len(graph_data_steps), 1)
            self.assertIn("line_graph", graph_data_steps[0])

    def test_pictograph_generation(self):
        """Test pictograph problems are generated correctly."""
        random.seed(44)
        for _ in range(5):
            res = self.picto_gen.generate()
            self.assertIn("pictograph", res["operation"])
            self.assertIn("Pictograph", res["problem"])
            self.assertIn("each", res["problem"])  # Key description
            self.assertTrue(res["steps"][-1].startswith(f"Z{DELIM}"))
            # Verify PICTO_KEY step exists
            picto_key_steps = [s for s in res["steps"] if s.startswith("PICTO_KEY")]
            self.assertEqual(len(picto_key_steps), 1)

    def test_deterministic_with_seed(self):
        """Test that same seed produces same output."""
        random.seed(100)
        res1 = self.gen.generate()
        random.seed(100)
        res2 = self.gen.generate()
        self.assertEqual(res1["problem"], res2["problem"])
        self.assertEqual(res1["final_answer"], res2["final_answer"])
        self.assertEqual(res1["steps"], res2["steps"])

    def test_bar_read_value_correctness(self):
        """Test bar chart read value calculation."""
        random.seed(200)
        # Force a read_value question by generating multiple and checking
        for _ in range(20):
            res = self.bar_gen.generate()
            if res["operation"] == "bar_chart_read":
                # Parse the chart data from GRAPH_DATA step
                graph_data = [s for s in res["steps"] if s.startswith("GRAPH_DATA")][0]
                data_part = graph_data.split(DELIM)[2]
                values = {}
                for pair in data_part.split(","):
                    k, v = pair.split(":")
                    values[k] = int(v)
                # Find what was asked
                question = res["problem"].split("Question:")[1].strip()
                for cat in values:
                    if cat in question:
                        self.assertEqual(res["final_answer"], str(values[cat]))
                        break
                break

    def test_pictograph_multiplication(self):
        """Test pictograph correctly multiplies symbols by key value."""
        random.seed(300)
        for _ in range(20):
            res = self.picto_gen.generate()
            if res["operation"] == "pictograph_read":
                # Find PICTO_KEY step to get symbol value
                picto_key = [s for s in res["steps"] if s.startswith("PICTO_KEY")][0]
                symbol_value = int(picto_key.split(DELIM)[2])
                # Find PICTO_COUNT step
                picto_count = [s for s in res["steps"] if s.startswith("PICTO_COUNT")][0]
                count = int(picto_count.split(DELIM)[2])
                # Verify multiplication
                expected = count * symbol_value
                self.assertEqual(res["final_answer"], str(expected))
                break

    def test_all_operation_types_covered(self):
        """Test that various operation types can be generated."""
        random.seed(500)
        operations_seen = set()
        for _ in range(100):
            res = self.gen.generate()
            operations_seen.add(res["operation"])

        # Should have at least some variety
        self.assertGreater(len(operations_seen), 5)
        # Should have all three graph types
        bar_ops = [op for op in operations_seen if "bar_chart" in op]
        line_ops = [op for op in operations_seen if "line_graph" in op]
        picto_ops = [op for op in operations_seen if "pictograph" in op]
        self.assertGreater(len(bar_ops), 0)
        self.assertGreater(len(line_ops), 0)
        self.assertGreater(len(picto_ops), 0)


if __name__ == "__main__":
    unittest.main()
