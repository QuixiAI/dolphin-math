# QuixiMath Dataset Release Plan

## Recommendation

Publish QuixiMath as one Hugging Face dataset repo with size-based configs and
normal semantic splits inside each config.

Do not make `train_10M_tokens`, `train_100M_tokens`, and `train_1B_tokens`
separate split names. In Hugging Face terms, size variants are configs/subsets;
`train`, `validation`, and `test` are splits.

The main release should be:

| Config | Purpose | Approx size |
|---|---|---:|
| `preview` | HF viewer, Data Studio, browsing, quick inspection | 10k-100k examples |
| `10M_tokens` | quick experiments and smoke tests | ~50k-150k examples |
| `100M_tokens` | normal fine-tuning release | ~400k-800k examples |
| `1B_tokens` | flagship release and serious SFT/pretraining use | ~4M-8M examples |

Release `100M_tokens` first. Use it to validate the pipeline, Hugging Face
viewer behavior, metadata, duplicate rates, answer formatting, and dataset card.
Then publish `1B_tokens` as the headline release, with the smaller configs kept
available for practical use.

## Hugging Face Layout

Use configs for sizes:

```yaml
configs:
  - config_name: preview
    data_files:
      - split: train
        path: preview/train-*.parquet

  - config_name: 10M_tokens
    data_files:
      - split: train
        path: 10M_tokens/train-*.parquet
      - split: validation
        path: 10M_tokens/validation-*.parquet

  - config_name: 100M_tokens
    data_files:
      - split: train
        path: 100M_tokens/train-*.parquet
      - split: validation
        path: 100M_tokens/validation-*.parquet
      - split: test
        path: 100M_tokens/test-*.parquet

  - config_name: 1B_tokens
    data_files:
      - split: train
        path: 1B_tokens/train-*.parquet
      - split: validation
        path: 1B_tokens/validation-*.parquet
      - split: test
        path: 1B_tokens/test-*.parquet
```

Users then load it like:

```python
from datasets import load_dataset

ds = load_dataset("QuixiAI/QuixiMath", "100M_tokens")
train = load_dataset("QuixiAI/QuixiMath", "100M_tokens", split="train")
```

## Size Configs Should Be Nested

Make the smaller configs deterministic subsets of the larger release:

```text
preview subset of 10M_tokens subset of 100M_tokens subset of 1B_tokens
```

That makes scaling experiments cleaner and lets the dataset card say that
QuixiMath includes official nested subsets for fast experiments and scaling
studies.

The easiest operational model is to generate the largest validated corpus first,
assign stable row IDs, then materialize smaller configs by deterministic
downsampling from that corpus.

## Sampling Strategy

The canonical released corpus should be coverage-first and richly labeled, not
prescriptively stratified. Trainers can then choose their own sampling mix by
filtering or reweighting rows using `grade_level`, `difficulty`, `generator`,
`operation`, trace length, or any other metadata.

Equal-per-skill sampling is a good default for the base corpus because it makes
every procedural skill visible. It is not grade-balanced with the current
registry, so the dataset card must publish the observed distribution clearly.

Current default skill distribution:

| Grade band | Skills | Equal-skill share |
|---|---:|---:|
| elementary | 35 | 6.9% |
| middle | 64 | 12.6% |
| high | 148 | 29.1% |
| college | 153 | 30.1% |
| graduate | 109 | 21.4% |

Under pure equal-skill sampling, more than half of the dataset is
college/graduate, and roughly two thirds is difficulty 4-5. That is acceptable
for a canonical coverage corpus as long as the metadata and distribution tables
are explicit.

Do not hide this by baking a single grade-balanced recipe into the only release.
Instead, publish optional training recipes. For example, a trainer may choose a
grade-balanced mix:

Recommended default train mix:

| Grade band | Train share |
|---|---:|
| elementary | 15% |
| middle | 20% |
| high | 30% |
| college | 25% |
| graduate | 10% |

This recipe keeps advanced material substantial without letting the long tail of
college and graduate generators dominate a training run. It should be documented
as a recipe, not treated as the canonical corpus distribution.

Do not stratify by difficulty alone. Difficulty is relative to the grade band:
`college` difficulty 2 does not mean the same thing as `elementary` difficulty
2.

Within each grade band, allocate across available difficulties with smoothing.
For example:

| Relative difficulty | Suggested share within grade |
|---|---:|
| 1 | 10% where available |
| 2 | 20% where available |
| 3 | 35% where available |
| 4 | 25% where available |
| 5 | 10% where available |

If a grade band does not have some difficulty buckets, redistribute that share
across the available buckets and keep per-skill minimums so small buckets still
appear.

## Validation And Test Splits

Validation and test should not simply mirror the training mix. They should be
better for measuring coverage.

Use one of these approaches:

1. Equal per skill, with enough examples per skill for stable reporting.
2. Equal by `(grade_level, difficulty)` bucket, then uniform by skill within the
   bucket.

I prefer equal per skill for the public benchmark split because it is simple to
explain and makes every generator visible. Keep `grade_level`, `difficulty`,
`operation`, and generator metadata in every row so users can compute filtered
metrics.

Recommended split sizes:

| Split | Size |
|---|---:|
| validation | 50k-200k examples |
| test | 50k-200k examples |

For benchmark claims, freeze the test split and do not regenerate it between
releases unless the dataset version changes clearly.

## Preview Config

The preview config is for humans and the Hugging Face viewer, not model
training. It should be small, diverse, and pleasant to inspect.

Make it approximately balanced by grade band and include every default sampled
skill if possible. Prefer examples with readable trace length and no unusually
large payloads. The preview can have only a `train` split.

## Dataset Card Positioning

Lead with the differentiator, not just the size.

Suggested wording:

> QuixiMath-1B is a 1B-token synthetic math reasoning corpus generated from
> 500+ procedural problem families, spanning elementary through graduate
> topics. Each example includes a problem, explicit step-by-step scratchpad,
> canonical final answer, grade band, relative difficulty, operation metadata,
> and reproducible generation metadata.

Be precise about what `1B` means. The card should include a table like:

| Field | Value |
|---|---|
| Rows | e.g. 5.2M |
| Estimated tokens | e.g. 1.03B |
| Problem types / skills | e.g. 509 default sampled skills |
| Operation variants | generated from opcode catalog |
| Splits | train / validation / test |
| Size configs | preview / 10M_tokens / 100M_tokens / 1B_tokens |
| License | Apache-2.0 |

## Quality Gates Before Release

Before publishing a config:

- Run the full generator test suite.
- Generate the split with a fixed seed and store the generation command.
- Confirm generator errors are zero.
- Inspect duplicate skip rates by generator.
- Validate required fields, final `Z|` step payloads, and pipe safety.
- Regenerate and check `OPCODES.md`.
- Regenerate and check `PROBLEM_TYPES.md`.
- Convert to Parquet and verify the Hugging Face viewer loads.
- Compute and publish distribution tables for grade, difficulty, operation, and
  generator class.

## Final Shape

The release should be described as:

```text
QuixiAI/QuixiMath
  config: preview
    split: train

  config: 10M_tokens
    split: train
    split: validation

  config: 100M_tokens
    split: train
    split: validation
    split: test

  config: 1B_tokens
    split: train
    split: validation
    split: test
```

The headline should be:

```text
QuixiMath-1B, with official nested 10M and 100M token configs for fast
experiments.
```

The important correction to a naive equal-skill plan is:

```text
Train split: stratified by grade_level, then difficulty, then skill.
Validation/test: coverage-balanced and frozen.
Configs: size variants.
Splits: train/validation/test only.
```
