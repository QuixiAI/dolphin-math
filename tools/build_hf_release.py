#!/usr/bin/env python3
"""Build a Hugging Face-compatible QuixiMath dataset release.

The builder streams generated examples directly to sharded Parquet files using
the size-config layout described in dataset_plan.md. Smaller configs are prefix
subsets of larger configs within each split.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from quixi_math_datagen import (  # noqa: E402
    _instance_label,
    group_into_skills,
    resolve_pool,
    validate_example,
)
from curriculum import stamp_metadata  # noqa: E402


DEFAULT_CONFIGS = {
    "preview": {"train": 50_000},
    "10M_tokens": {"train": 100_000, "validation": 10_000},
    "100M_tokens": {"train": 800_000, "validation": 50_000, "test": 50_000},
    "1B_tokens": {"train": 8_800_000, "validation": 100_000, "test": 100_000},
}

SMOKE_CONFIGS = {
    "preview": {"train": 200},
    "10M_tokens": {"train": 400, "validation": 100},
    "100M_tokens": {"train": 800, "validation": 150, "test": 150},
    "1B_tokens": {"train": 1_200, "validation": 200, "test": 200},
}

CONFIG_ORDER = ("preview", "10M_tokens", "100M_tokens", "1B_tokens")
SPLIT_ORDER = ("test", "validation", "train")

SCHEMA = pa.schema(
    [
        ("row_id", pa.int64()),
        ("example_id", pa.string()),
        ("problem_id", pa.string()),
        ("generator", pa.string()),
        ("generator_label", pa.string()),
        ("operation", pa.string()),
        ("grade_level", pa.string()),
        ("difficulty", pa.int64()),
        ("problem", pa.string()),
        ("steps", pa.list_(pa.string())),
        ("final_answer", pa.string()),
        ("text", pa.string()),
    ]
)


def text_for_example(example: Mapping[str, object]) -> str:
    steps = "\n".join(str(s) for s in example["steps"])
    return (
        f"Problem:\n{example['problem']}\n\n"
        f"Solution steps:\n{steps}\n\n"
        f"Final answer:\n{example['final_answer']}"
    )


def git_value(args: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None
    return result.stdout.strip()


def size_category(rows: int) -> str:
    bands = [
        (1_000, "n<1K"),
        (10_000, "1K<n<10K"),
        (100_000, "10K<n<100K"),
        (1_000_000, "100K<n<1M"),
        (10_000_000, "1M<n<10M"),
        (100_000_000, "10M<n<100M"),
    ]
    for limit, label in bands:
        if rows < limit:
            return label
    return "n>100M"


class SplitWriter:
    def __init__(
        self,
        output_dir: Path,
        config: str,
        split: str,
        target_rows: int,
        shard_rows: int,
        compression: str,
    ) -> None:
        self.output_dir = output_dir
        self.config = config
        self.split = split
        self.target_rows = target_rows
        self.shard_rows = shard_rows
        self.compression = compression
        self.rows: List[dict] = []
        self.row_count = 0
        self.text_chars = 0
        self.shard_index = 0
        self.total_shards = max(1, math.ceil(target_rows / shard_rows))
        (output_dir / config).mkdir(parents=True, exist_ok=True)

    def add(self, row: dict) -> None:
        if self.row_count >= self.target_rows:
            return
        self.rows.append(dict(row))
        self.row_count += 1
        self.text_chars += len(row["text"])
        if len(self.rows) >= self.shard_rows:
            self.flush()

    def flush(self) -> None:
        if not self.rows:
            return
        path = (
            self.output_dir
            / self.config
            / f"{self.split}-{self.shard_index:05d}-of-{self.total_shards:05d}.parquet"
        )
        table = pa.Table.from_pylist(self.rows, schema=SCHEMA)
        pq.write_table(table, path, compression=self.compression)
        self.rows.clear()
        self.shard_index += 1

    def close(self) -> None:
        self.flush()

    @property
    def rough_tokens(self) -> int:
        return round(self.text_chars / 4)


class ReleaseStats:
    def __init__(self) -> None:
        self.rows_by_config_split: MutableMapping[str, MutableMapping[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.text_chars_by_config_split: MutableMapping[
            str, MutableMapping[str, int]
        ] = defaultdict(lambda: defaultdict(int))
        self.rows_by_largest_split: Counter[str] = Counter()
        self.grade: Counter[str] = Counter()
        self.difficulty: Counter[str] = Counter()
        self.grade_difficulty: Counter[str] = Counter()
        self.generator: Counter[str] = Counter()
        self.operation: Counter[str] = Counter()
        self.generator_stats: MutableMapping[str, Counter[str]] = defaultdict(Counter)
        self.attempts_by_split: Counter[str] = Counter()

    def observe_largest_row(self, split: str, row: Mapping[str, object]) -> None:
        grade = str(row["grade_level"])
        difficulty = str(row["difficulty"])
        self.rows_by_largest_split[split] += 1
        self.grade[grade] += 1
        self.difficulty[difficulty] += 1
        self.grade_difficulty[f"{grade}|{difficulty}"] += 1
        self.generator[str(row["generator"])] += 1
        self.operation[str(row["operation"])] += 1

    def observe_writer(self, writer: SplitWriter) -> None:
        self.rows_by_config_split[writer.config][writer.split] = writer.row_count
        self.text_chars_by_config_split[writer.config][writer.split] = writer.text_chars

    def as_json(self) -> dict:
        return {
            "rows_by_config_split": {
                config: dict(splits)
                for config, splits in sorted(self.rows_by_config_split.items())
            },
            "rough_tokens_by_config_split": {
                config: {
                    split: round(chars / 4)
                    for split, chars in sorted(splits.items())
                }
                for config, splits in sorted(self.text_chars_by_config_split.items())
            },
            "rows_by_largest_split": dict(sorted(self.rows_by_largest_split.items())),
            "attempts_by_split": dict(sorted(self.attempts_by_split.items())),
            "rows_by_grade_level": dict(sorted(self.grade.items())),
            "rows_by_difficulty": dict(sorted(self.difficulty.items())),
            "rows_by_grade_level_and_difficulty": dict(
                sorted(self.grade_difficulty.items())
            ),
            "rows_by_generator": dict(sorted(self.generator.items())),
            "rows_by_operation": dict(sorted(self.operation.items())),
            "generator_stats": {
                name: dict(counts)
                for name, counts in sorted(self.generator_stats.items())
            },
        }


def selected_writers(
    writers: Mapping[Tuple[str, str], SplitWriter],
    split: str,
    row_index: int,
) -> Iterable[SplitWriter]:
    for config in CONFIG_ORDER:
        writer = writers.get((config, split))
        if writer is not None and row_index < writer.target_rows:
            yield writer


def max_rows_by_split(configs: Mapping[str, Mapping[str, int]]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for split in ("train", "validation", "test"):
        result[split] = max((splits.get(split, 0) for splits in configs.values()), default=0)
    return result


def make_row(
    example: Mapping[str, object],
    gen_instance: object,
    split: str,
    row_id: int,
) -> dict:
    text = text_for_example(example)
    return {
        "row_id": row_id,
        "example_id": f"{split}-{row_id:09d}",
        "problem_id": str(example["problem_id"]),
        "generator": gen_instance.__class__.__name__,
        "generator_label": _instance_label(gen_instance),
        "operation": str(example["operation"]),
        "grade_level": str(example["grade_level"]),
        "difficulty": int(example["difficulty"]),
        "problem": str(example["problem"]),
        "steps": list(example["steps"]),
        "final_answer": str(example["final_answer"]),
        "text": text,
    }


def generate_release(
    output_dir: Path,
    configs: Mapping[str, Mapping[str, int]],
    seed: int,
    shard_rows: int,
    compression: str,
) -> dict:
    random.seed(seed)
    gen_pool = resolve_pool(None)
    skills = group_into_skills(gen_pool)
    skill_names = list(skills)
    split_targets = max_rows_by_split(configs)
    stats = ReleaseStats()
    seen = set()

    writers: Dict[Tuple[str, str], SplitWriter] = {}
    for config in CONFIG_ORDER:
        for split, rows in configs.get(config, {}).items():
            writers[(config, split)] = SplitWriter(
                output_dir=output_dir,
                config=config,
                split=split,
                target_rows=rows,
                shard_rows=shard_rows,
                compression=compression,
            )

    for split in SPLIT_ORDER:
        target = split_targets.get(split, 0)
        if target <= 0:
            continue
        print(f"Generating {target:,} unique rows for largest {split} split...")
        emitted = 0
        attempts = 0
        max_attempts = target * 20 + 100_000
        consecutive_rejects = 0
        max_consecutive_rejects = max(200_000, target)
        while emitted < target and attempts < max_attempts:
            if consecutive_rejects >= max_consecutive_rejects:
                raise RuntimeError(
                    f"No accepted {split} rows in {consecutive_rejects:,} attempts; "
                    "problem space may be exhausted."
                )
            attempts += 1
            skill = random.choice(skill_names)
            gen_instance = random.choice(skills[skill])
            label = _instance_label(gen_instance)
            try:
                example = gen_instance.generate()
                if not example:
                    raise ValueError("generate() returned an empty example")
                example = stamp_metadata(example, gen_instance)
                validate_example(example)
            except Exception as exc:
                stats.generator_stats[label]["errors"] += 1
                consecutive_rejects += 1
                if stats.generator_stats[label]["errors"] <= 5:
                    print(f"ERROR: {label} failed validation: {exc}")
                continue

            key = (example["operation"], example["problem"])
            if key in seen:
                stats.generator_stats[label]["duplicates_skipped"] += 1
                consecutive_rejects += 1
                continue

            seen.add(key)
            row = make_row(example, gen_instance, split, emitted)
            for writer in selected_writers(writers, split, emitted):
                writer.add(row)
            stats.observe_largest_row(split, row)
            stats.generator_stats[label]["emitted"] += 1
            emitted += 1
            consecutive_rejects = 0
            if emitted % 100_000 == 0 or emitted == target:
                print(
                    f"... {split}: {emitted:,}/{target:,} rows "
                    f"after {attempts:,} attempts"
                )
        stats.attempts_by_split[split] = attempts
        if emitted != target:
            raise RuntimeError(
                f"Target for {split} not reached: emitted {emitted:,}/{target:,} "
                f"after {attempts:,} attempts."
            )

    for writer in writers.values():
        writer.close()
        stats.observe_writer(writer)

    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "source_repo": str(ROOT),
        "source_git_commit": git_value(["rev-parse", "HEAD"]),
        "source_git_dirty": bool(git_value(["status", "--short"])),
        "configs": configs,
        "shard_rows": shard_rows,
        "compression": compression,
        "default_pool_skills": len(skills),
        "default_pool_instances": len(gen_pool),
        **stats.as_json(),
    }
    return metadata


def table_rows(rows: Iterable[Tuple[str, object]]) -> str:
    lines = ["| Field | Value |", "|---|---:|"]
    for key, value in rows:
        if isinstance(value, int):
            rendered = f"{value:,}"
        else:
            rendered = str(value)
        lines.append(f"| {key} | {rendered} |")
    return "\n".join(lines)


def split_stats_table(metadata: Mapping[str, object]) -> str:
    rows_by_config = metadata["rows_by_config_split"]
    tokens_by_config = metadata["rough_tokens_by_config_split"]
    lines = ["| Config | Split | Rows | Estimated tokens |", "|---|---|---:|---:|"]
    for config in CONFIG_ORDER:
        splits = rows_by_config.get(config, {})
        for split in ("train", "validation", "test"):
            if split in splits:
                rows = splits[split]
                tokens = tokens_by_config.get(config, {}).get(split, 0)
                lines.append(f"| `{config}` | `{split}` | {rows:,} | {tokens:,} |")
    return "\n".join(lines)


def distribution_table(counter: Mapping[str, int], key_name: str, limit: Optional[int] = None) -> str:
    items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    if limit is not None:
        items = items[:limit]
    lines = [f"| {key_name} | Rows |", "|---|---:|"]
    for key, value in items:
        lines.append(f"| `{key}` | {value:,} |")
    return "\n".join(lines)


def yaml_header(metadata: Mapping[str, object]) -> str:
    largest_rows = sum(metadata["rows_by_config_split"]["1B_tokens"].values())
    lines = [
        "---",
        "language:",
        "- en",
        "license: other",
        "tags:",
        "- synthetic",
        "- math",
        "- reasoning",
        "- step-by-step",
        "- text-generation",
        "- language-modeling",
        "task_categories:",
        "- text-generation",
        "task_ids:",
        "- language-modeling",
        "size_categories:",
        f"- {size_category(largest_rows)}",
        "pretty_name: QuixiMath-1B",
        "configs:",
    ]
    for config in CONFIG_ORDER:
        splits = metadata["rows_by_config_split"].get(config, {})
        lines.append(f"- config_name: {config}")
        lines.append("  data_files:")
        for split in ("train", "validation", "test"):
            if split in splits:
                lines.append(f"  - split: {split}")
                lines.append(f"    path: {config}/{split}-*.parquet")
    lines.extend(
        [
            "train-eval-index:",
            "- config: 10M_tokens",
            "  task: text-generation",
            "  task_id: language-modeling",
            "  splits:",
            "    train_split: train",
            "    eval_split: validation",
            "  col_mapping:",
            "    text: text",
            "- config: 100M_tokens",
            "  task: text-generation",
            "  task_id: language-modeling",
            "  splits:",
            "    train_split: train",
            "    eval_split: validation",
            "  col_mapping:",
            "    text: text",
            "- config: 1B_tokens",
            "  task: text-generation",
            "  task_id: language-modeling",
            "  splits:",
            "    train_split: train",
            "    eval_split: validation",
            "  col_mapping:",
            "    text: text",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def write_readme(output_dir: Path, metadata: Mapping[str, object]) -> None:
    rows_by_config = metadata["rows_by_config_split"]
    tokens_by_config = metadata["rough_tokens_by_config_split"]
    largest_rows = sum(rows_by_config["1B_tokens"].values())
    largest_tokens = sum(tokens_by_config["1B_tokens"].values())
    body = f"""# Dataset Card for QuixiMath-1B

## Dataset Summary

QuixiMath-1B is a synthetic math reasoning corpus generated from the QuixiMath
procedural problem generators. Each record contains a natural-language problem,
explicit step-by-step scratchpad opcodes, a canonical final answer, and metadata
for filtering or reweighting by skill, operation, grade band, and relative
difficulty.

The canonical corpus is coverage-first rather than prescriptively stratified:
trainers can choose their own sampling mix using the included metadata columns.
The size configs are nested prefix subsets within each split.

## How to Load

```python
from datasets import load_dataset

ds = load_dataset("QuixiAI/QuixiMath-1B", "100M_tokens")
train = load_dataset("QuixiAI/QuixiMath-1B", "100M_tokens", split="train")
```

For a local checkout:

```python
from datasets import load_dataset

ds = load_dataset("{output_dir}", "preview")
```

## Configs And Splits

{split_stats_table(metadata)}

The largest config contains {largest_rows:,} rows and approximately
{largest_tokens:,} rough text tokens, estimated as `len(text) / 4`.

## Data Schema

Columns:

- `row_id`: stable integer row index within the split.
- `example_id`: stable string ID such as `train-000000123`.
- `problem_id`: generator-provided problem identifier.
- `generator`: generator class name.
- `generator_label`: generator class plus variant marker when applicable.
- `operation`: problem operation/category label.
- `grade_level`: one of `elementary`, `middle`, `high`, `college`, `graduate`.
- `difficulty`: integer 1-5, relative to `grade_level`.
- `problem`: problem text.
- `steps`: list of pipe-delimited scratchpad steps.
- `final_answer`: canonical answer string.
- `text`: training-ready text field containing problem, steps, and final answer.

## Dataset Stats

{table_rows([
    ("Default sampled skills", metadata["default_pool_skills"]),
    ("Default generator instances", metadata["default_pool_instances"]),
    ("Seed", metadata["seed"]),
    ("Shard rows", metadata["shard_rows"]),
])}

### Grade Distribution

{distribution_table(metadata["rows_by_grade_level"], "Grade level")}

### Difficulty Distribution

{distribution_table(metadata["rows_by_difficulty"], "Difficulty")}

### Top Operations

{distribution_table(metadata["rows_by_operation"], "Operation", limit=25)}

## Generation

Generated at: `{metadata["generated_at_utc"]}`

Source repository: `{metadata["source_repo"]}`

Source git commit: `{metadata.get("source_git_commit") or "unknown"}`

Source git dirty: `{metadata["source_git_dirty"]}`

Exact duplicate `(operation, problem)` pairs were skipped across the generated
largest splits before nested configs were materialized. Per-generator duplicate
and error counts are stored in `generation_stats.json`.

## Licensing Information

License: other
"""
    (output_dir / "README.md").write_text(yaml_header(metadata) + body, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output-dir",
        default="~/datasets/QuixiMath-1B",
        help="Output dataset directory.",
    )
    parser.add_argument(
        "--preset",
        choices=("full", "smoke"),
        default="full",
        help="Use full release row counts or tiny smoke-test counts.",
    )
    parser.add_argument("--seed", type=int, default=20260707)
    parser.add_argument("--shard-rows", type=int, default=100_000)
    parser.add_argument("--compression", default="zstd")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Remove output directory first if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    configs = DEFAULT_CONFIGS if args.preset == "full" else SMOKE_CONFIGS

    if output_dir.exists():
        if not args.overwrite:
            raise SystemExit(f"Output directory already exists: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    metadata = generate_release(
        output_dir=output_dir,
        configs=configs,
        seed=args.seed,
        shard_rows=args.shard_rows,
        compression=args.compression,
    )
    (output_dir / "generation_stats.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_readme(output_dir, metadata)
    print(f"Done: {output_dir}")


if __name__ == "__main__":
    main()
