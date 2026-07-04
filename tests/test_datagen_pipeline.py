import contextlib
import io
import json
import os
import random
import sys
import tempfile
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import curriculum
from curriculum import CURRICULUM, GRADE_LEVELS, stamp_metadata
from dolphin_math_datagen import (
    ALL_GENERATORS,
    DEFAULT_POOL_EXCLUDED,
    build_dataset,
    group_into_skills,
    parse_weights,
    resolve_pool,
    validate_example,
)
from generators.multi_digit_addition_generator import MultiDigitAdditionGenerator
from generators.long_division_generator import LongDivisionGenerator
from generators.mixed_number_operations_random import MixedNumberOperationsRandom


from base_generator import ProblemGenerator
from helpers import jid


def quiet_build_dataset(**kwargs):
    """build_dataset with its progress/stats output suppressed."""
    with contextlib.redirect_stdout(io.StringIO()):
        return build_dataset(**kwargs)


def make_valid_example():
    return {
        "problem_id": "test-id",
        "operation": "test_op",
        "problem": "1 + 1",
        "steps": ["A|1|1|2", "Z|2"],
        "final_answer": "2",
        "grade_level": "elementary",
        "difficulty": 2,
    }


class TestValidateExample(unittest.TestCase):
    def test_valid_example_passes(self):
        validate_example(make_valid_example())

    def test_valid_example_from_real_generator(self):
        random.seed(42)
        gen = MultiDigitAdditionGenerator()
        example = stamp_metadata(gen.generate(), gen)
        validate_example(example)

    def test_int_final_answer_accepted(self):
        ex = make_valid_example()
        ex["final_answer"] = 2
        validate_example(ex)

    def test_missing_key(self):
        for key in ("problem_id", "operation", "problem", "steps",
                    "final_answer", "grade_level", "difficulty"):
            ex = make_valid_example()
            del ex[key]
            with self.assertRaises(ValueError, msg=key):
                validate_example(ex)

    def test_empty_steps(self):
        ex = make_valid_example()
        ex["steps"] = []
        with self.assertRaises(ValueError):
            validate_example(ex)

    def test_non_string_step(self):
        ex = make_valid_example()
        ex["steps"] = [("A", 1, 1, 2), "Z|2"]
        with self.assertRaises(ValueError):
            validate_example(ex)

    def test_step_with_too_many_fields(self):
        ex = make_valid_example()
        ex["steps"] = ["A|1|2|3|4|5", "Z|2"]
        with self.assertRaises(ValueError):
            validate_example(ex)

    def test_step_with_empty_opcode(self):
        ex = make_valid_example()
        ex["steps"] = ["|1|1|2", "Z|2"]
        with self.assertRaises(ValueError):
            validate_example(ex)

    def test_last_step_not_z(self):
        ex = make_valid_example()
        ex["steps"] = ["Z|2", "A|1|1|2"]
        with self.assertRaises(ValueError):
            validate_example(ex)

    def test_z_payload_mismatch(self):
        ex = make_valid_example()
        ex["final_answer"] = "3"
        with self.assertRaises(ValueError):
            validate_example(ex)

    def test_bad_grade_level(self):
        ex = make_valid_example()
        ex["grade_level"] = "kindergarten"
        with self.assertRaises(ValueError):
            validate_example(ex)

    def test_all_grade_bands_validate(self):
        for band in ("elementary", "middle", "high", "college",
                     "graduate"):
            ex = make_valid_example()
            ex["grade_level"] = band
            validate_example(ex)

    def test_bad_difficulty(self):
        for bad in (0, 6, "3", 2.5, True):
            ex = make_valid_example()
            ex["difficulty"] = bad
            with self.assertRaises(ValueError, msg=repr(bad)):
                validate_example(ex)


class _UnregisteredGenerator(ProblemGenerator):
    """Test double with no CURRICULUM entry."""

    def __init__(self, emit_metadata=False):
        self.emit_metadata = emit_metadata

    def generate(self):
        example = {
            "problem_id": jid(),
            "operation": "unregistered_op",
            "problem": "2 + 2",
            "steps": ["A|2|2|4", "Z|4"],
            "final_answer": "4",
        }
        if self.emit_metadata:
            example["grade_level"] = "middle"
            example["difficulty"] = 5
        return example


class TestStampMetadata(unittest.TestCase):
    def test_stamps_from_table(self):
        gen = MultiDigitAdditionGenerator()
        random.seed(1)
        example = stamp_metadata(gen.generate(), gen)
        expected = CURRICULUM["MultiDigitAdditionGenerator"]
        self.assertEqual(example["grade_level"], expected["grade_level"])
        self.assertEqual(example["difficulty"], expected["difficulty"])

    def test_generator_provided_values_win(self):
        gen = MultiDigitAdditionGenerator()
        random.seed(1)
        example = gen.generate()
        example["grade_level"] = "high"
        example["difficulty"] = 5
        stamped = stamp_metadata(example, gen)
        self.assertEqual(stamped["grade_level"], "high")
        self.assertEqual(stamped["difficulty"], 5)

    def test_unknown_class_without_keys_raises(self):
        gen = _UnregisteredGenerator()
        with self.assertRaises(ValueError) as ctx:
            stamp_metadata(gen.generate(), gen)
        self.assertIn("CURRICULUM", str(ctx.exception))

    def test_unknown_class_with_self_emitted_keys_ok(self):
        gen = _UnregisteredGenerator(emit_metadata=True)
        example = stamp_metadata(gen.generate(), gen)
        self.assertEqual(example["grade_level"], "middle")
        self.assertEqual(example["difficulty"], 5)


class TestCurriculumCoverage(unittest.TestCase):
    def test_every_registered_generator_has_curriculum_entry(self):
        """Load-bearing invariant: adding a generator to ALL_GENERATORS
        requires adding its class to curriculum.CURRICULUM."""
        missing = sorted(
            {g.__class__.__name__ for g in ALL_GENERATORS} - set(CURRICULUM)
        )
        self.assertEqual(missing, [],
                         f"Classes missing from curriculum.CURRICULUM: {missing}")

    def test_curriculum_entries_are_valid(self):
        for name, meta in CURRICULUM.items():
            self.assertIn(meta["grade_level"], GRADE_LEVELS, name)
            self.assertIsInstance(meta["difficulty"], int, name)
            self.assertTrue(1 <= meta["difficulty"] <= 5, name)

    def test_no_orphan_curriculum_entries(self):
        registered = {g.__class__.__name__ for g in ALL_GENERATORS}
        orphans = sorted(set(CURRICULUM) - registered)
        self.assertEqual(orphans, [],
                         f"CURRICULUM entries with no registered generator: {orphans}")


class TestSkillSampling(unittest.TestCase):
    def test_variant_instances_form_one_skill(self):
        skills = group_into_skills(resolve_pool())
        self.assertEqual(len(skills["FractionOpGenerator"]), 4)
        self.assertEqual(len(skills["MixedNumberOperationGenerator"]), 4)
        self.assertEqual(len(skills["DecimalAddSubGenerator"]), 2)

    def test_default_pool_excludes_wrapper(self):
        names = {g.__class__.__name__ for g in resolve_pool()}
        self.assertFalse(names & DEFAULT_POOL_EXCLUDED)
        self.assertEqual(
            len(names),
            len({g.__class__.__name__ for g in ALL_GENERATORS}
                - DEFAULT_POOL_EXCLUDED),
        )

    def test_explicit_selection_honored_verbatim(self):
        wrapper = MixedNumberOperationsRandom()
        pool = resolve_pool([wrapper])
        self.assertEqual(pool, [wrapper])
        self.assertIn("MixedNumberOperationsRandom", group_into_skills(pool))

    def test_empty_explicit_selection_raises(self):
        with self.assertRaises(ValueError):
            resolve_pool([])


class TestParseWeights(unittest.TestCase):
    AVAILABLE = {"LongDivisionGenerator", "QuadraticGenerator"}

    def test_inline_spec(self):
        weights = parse_weights(
            "LongDivisionGenerator=2.5, QuadraticGenerator=0.5", self.AVAILABLE)
        self.assertEqual(weights, {"LongDivisionGenerator": 2.5,
                                   "QuadraticGenerator": 0.5})

    def test_json_file_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "weights.json")
            with open(path, "w", encoding="utf-8") as fp:
                json.dump({"QuadraticGenerator": 3}, fp)
            weights = parse_weights(path, self.AVAILABLE)
            self.assertEqual(weights, {"QuadraticGenerator": 3.0})

    def test_unknown_skill_lists_available(self):
        with self.assertRaises(ValueError) as ctx:
            parse_weights("NoSuchSkill=2", self.AVAILABLE)
        self.assertIn("Available:", str(ctx.exception))
        self.assertIn("LongDivisionGenerator", str(ctx.exception))

    def test_bad_entries(self):
        for spec in ("LongDivisionGenerator", "LongDivisionGenerator=abc",
                     "LongDivisionGenerator=0", "LongDivisionGenerator=-1"):
            with self.assertRaises(ValueError, msg=spec):
                parse_weights(spec, self.AVAILABLE)

    def test_missing_json_file(self):
        with self.assertRaises(ValueError):
            parse_weights("/nonexistent/weights.json", self.AVAILABLE)

    def test_weights_skew_sampling(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "skew.jsonl")
            quiet_build_dataset(
                path=path, n=200, seed=7,
                generators=[LongDivisionGenerator(),
                            MultiDigitAdditionGenerator()],
                weights={"LongDivisionGenerator": 9.0,
                         "MultiDigitAdditionGenerator": 1.0},
            )
            with open(path, encoding="utf-8") as fp:
                rows = [json.loads(line) for line in fp]
            share = sum(r["operation"] == "long_division" for r in rows) / len(rows)
            self.assertGreater(share, 0.7)


class _TinySpaceGenerator(ProblemGenerator):
    """Test double with only 3 distinct problems; emits its own metadata."""

    def generate(self):
        a = random.randint(1, 3)
        return {
            "problem_id": jid(),
            "operation": "tiny_add",
            "problem": f"{a} + 0",
            "steps": [f"A|{a}|0|{a}", f"Z|{a}"],
            "final_answer": str(a),
            "grade_level": "elementary",
            "difficulty": 1,
        }


class TestDeduplication(unittest.TestCase):
    def test_duplicates_skipped_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "dedup.jsonl")
            summary = quiet_build_dataset(path=path, n=10, seed=5,
                                    generators=[_TinySpaceGenerator()])
            with open(path, encoding="utf-8") as fp:
                rows = [json.loads(line) for line in fp]
            self.assertEqual(len(rows), 3)  # problem space exhausted
            self.assertEqual(summary["count"], 3)
            self.assertEqual(len({r["problem"] for r in rows}), 3)
            stats = summary["stats"]["_TinySpaceGenerator"]
            self.assertEqual(stats["emitted"], 3)
            self.assertGreater(stats["duplicates_skipped"], 0)

    def test_allow_duplicates_restores_old_behavior(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "dups.jsonl")
            summary = quiet_build_dataset(path=path, n=10, seed=5,
                                    generators=[_TinySpaceGenerator()],
                                    allow_duplicates=True)
            with open(path, encoding="utf-8") as fp:
                rows = [json.loads(line) for line in fp]
            self.assertEqual(len(rows), 10)
            self.assertEqual(summary["stats"]["_TinySpaceGenerator"]["duplicates_skipped"], 0)

    def test_errors_counted_in_stats(self):
        class _Broken(ProblemGenerator):
            def generate(self):
                raise RuntimeError("boom")

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "err.jsonl")
            summary = quiet_build_dataset(path=path, n=3, seed=5,
                                    generators=[_Broken()])
            self.assertEqual(summary["count"], 0)
            self.assertGreater(summary["stats"]["_Broken"]["errors"], 0)


class TestBuildDatasetEndToEnd(unittest.TestCase):
    def _build(self, path, **kwargs):
        quiet_build_dataset(path=path, **kwargs)
        with open(path, encoding="utf-8") as fp:
            return [json.loads(line) for line in fp]

    def test_build_writes_valid_unique_examples(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "out.jsonl")
            rows = self._build(path, n=25, seed=42,
                               generators=[MultiDigitAdditionGenerator()])
            self.assertEqual(len(rows), 25)
            seen_keys = set()
            for row in rows:
                validate_example(row)
                self.assertEqual(row["steps"][-1],
                                 "Z|" + str(row["final_answer"]))
                key = (row["operation"], row["problem"])
                self.assertNotIn(key, seen_keys)
                seen_keys.add(key)

    def test_same_seed_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            p1 = os.path.join(tmp, "a.jsonl")
            p2 = os.path.join(tmp, "b.jsonl")
            quiet_build_dataset(path=p1, n=40, seed=123)
            quiet_build_dataset(path=p2, n=40, seed=123)
            with open(p1, encoding="utf-8") as f1, open(p2, encoding="utf-8") as f2:
                self.assertEqual(f1.read(), f2.read())


if __name__ == "__main__":
    unittest.main()
