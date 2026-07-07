# Quixi Math Data Generator

<img width="504" height="322" alt="math" src="https://github.com/user-attachments/assets/47fb7346-2ba1-49fb-b9e6-21917f078256" />

<img width="410" alt="image" src="https://github.com/user-attachments/assets/f8a5d3d2-7820-4f7c-a5d3-fbac667e7084" />

## Purpose

Quixi Math generates synthetic math problems with visible, step-by-step
scratchpads. Each example includes the problem text, pipe-delimited solution
steps, a canonical final answer, and curriculum metadata.

The dataset is designed for training and evaluating language models on
multi-step mathematical reasoning. It can be used for SFT-style trace learning
and RL-style answer/reasoning validation; generate separate datasets for those
uses so syntax learning and reward optimization can be controlled separately.

## Current Inventory

The generated catalog is the source of truth:
[PROBLEM_TYPES.md](PROBLEM_TYPES.md).

Current repo snapshot:

- **510 problem-type entries** in the generated catalog, one per registered
  generator class
- **526 registered generator instances**; **525** are in the default pool
- **509 default sampled skills** in dataset builds; `MixedNumberOperationsRandom`
  is an opt-in wrapper and is excluded from the default pool to avoid
  double-counting the four explicit mixed-number operation variants
- **1,149 distinct operation variant labels** across the catalog
- **1,602 observed scratchpad op-codes** in [OPCODES.md](OPCODES.md)
- Catalog grade-band distribution: **36 elementary**, **64 middle**,
  **148 high**, **153 college**, **109 graduate**

The CLI samples equally per skill by default, not equally per generator
instance. Variant instances of one class, such as `FractionOpGenerator('+')`
and `FractionOpGenerator('/')`, share one skill slot unless explicitly
weighted.

## Coverage

Coverage now spans elementary through graduate-level topics:

- **Elementary:** whole-number algorithms, decimals, fractions, mixed numbers,
  conversions, factors/GCF/LCM, order of operations, number sense, unit
  conversions, elementary geometry, graph reading, simple statistics, and
  probability.
- **Middle school:** ratios and rates, proportional relationships, integer
  operations, equations and inequalities, exponent rules, scientific notation,
  geometry and measurement, compound probability, finance, physics formulas,
  base arithmetic, modular arithmetic, and calendar/manual computation.
- **High school:** Algebra 1/2, factoring, polynomial and rational
  expressions, systems, functions, sequences, conics, geometry, trigonometry,
  vectors, matrices, calculus, statistics, probability, finite math, and
  critic formats such as error spotting and fill-in-the-step records.
- **College:** multivariable calculus, linear algebra, differential equations,
  discrete math, graph algorithms, number theory, abstract algebra, complex
  analysis, numerical methods, distributions, optimization, signals, physics,
  chemistry, information theory, machine learning, and finance.
- **Graduate:** differential geometry, quantum mechanics and quantum
  information, Lie/group and tensor notation, relativity, particle/field
  physics, advanced probability/statistics, information theory, deep learning,
  kernel methods, transformer arithmetic, and quantitative finance.

Signature behaviors:

- Every arithmetic action is explicit when it would naturally appear in a
  pencil-and-paper solution.
- `CHECK`, substitute-back, multiply-back, sign-chart, table, and theorem
  checks are emitted where natural.
- Trial paths can be visible through `TRY`, `REJECT`, and `ACCEPT`.
- Derived critic records keep the same JSONL schema while embedding the
  worked or partial scratchpad in the prompt text.
- Generated op-code and problem-type docs can be checked for freshness in CI.

## Usage

Prefer `uv run python ...` so the repo environment is selected explicitly.
If you are not using `uv`, activate the virtual environment first:

```bash
source .venv/bin/activate
```

### Generate Samples

With no arguments, the CLI prints one sample from each registered generator
instance:

```bash
uv run python quixi_math_datagen.py
```

The explicit form is:

```bash
uv run python quixi_math_datagen.py --sample
```

Use a seed for reproducible samples:

```bash
uv run python quixi_math_datagen.py --sample -s 7
```

Limit samples to specific generator classes:

```bash
uv run python quixi_math_datagen.py --sample \
  --generators MultiDigitAdditionGenerator,LongDivisionGenerator
```

### Generate a Dataset

Generate JSONL with an explicit output path:

```bash
uv run python quixi_math_datagen.py -n 50000 -o quixi_math_50000.jsonl -s 123
```

If `-o/--output` is omitted, the output path defaults to
`quixi_math_<n>.jsonl`:

```bash
uv run python quixi_math_datagen.py -n 50000 -s 123
```

Restrict a build to selected generator classes:

```bash
uv run python quixi_math_datagen.py -n 5000 -o subset.jsonl \
  --generators MultiDigitAdditionGenerator,DecimalMultGenerator
```

Omit `-s/--seed` for natural randomness. Provide a seed when byte-for-byte
reproducibility matters.

### Sampling, Weights, and Deduplication

Dataset builds sample equally per skill by default. Override individual skill
weights with `--weights`; unlisted skills keep weight `1.0`.

Inline weights:

```bash
uv run python quixi_math_datagen.py -n 10000 \
  --weights "QuadraticGenerator=3,MeanGenerator=0.5"
```

JSON file weights:

```json
{
  "QuadraticGenerator": 3,
  "MeanGenerator": 0.5
}
```

```bash
uv run python quixi_math_datagen.py -n 10000 --weights weights.json
```

Exact `(operation, problem)` repeats are skipped by default. Pass
`--allow-duplicates` to keep repeats, which is useful for very large datasets
or intentionally small exact problem spaces.

Every dataset run prints a per-generator stats table with emitted counts,
duplicate skips, and errors. If the selected problem space is exhausted before
`-n`, generation stops early with a warning.

## Output Format

Each JSONL line is one problem:

```json
{
  "problem_id": "1f8b6be5-...",
  "operation": "long_division",
  "problem": "1834 / 5",
  "steps": ["D|18|5|3", "M|3|5|15", "S|18|15|3", "B|3|3|33", "Z|366 R4"],
  "final_answer": "366 R4",
  "grade_level": "elementary",
  "difficulty": 3
}
```

Required fields:

- `problem_id`: generated UUID
- `operation`: internal operation or variant label
- `problem`: human-readable prompt
- `steps`: visible scratchpad as `CODE|field|field|...` strings
- `final_answer`: canonical answer string
- `grade_level`: `elementary`, `middle`, `high`, `college`, or `graduate`
- `difficulty`: integer from 1 to 5, read relative to the grade band

The final step must be exactly `Z|<final_answer>`. Metadata is stamped from
`curriculum.py` after generation unless a generator intentionally overrides it.

Answer-format conventions live in [DESIGN.md](DESIGN.md). Generated examples
are structurally validated before being written.

## Generated Docs

Two files are generated and should not be hand-edited:

- [PROBLEM_TYPES.md](PROBLEM_TYPES.md): user-facing catalog with one worked
  example per problem type
- [OPCODES.md](OPCODES.md): descriptive legend of observed scratchpad op-codes

Regenerate or check them with:

```bash
uv run python tools/gen_problem_types.py
uv run python tools/gen_problem_types.py --check

uv run python tools/gen_opcode_legend.py
uv run python tools/gen_opcode_legend.py --check
```

The op-code vocabulary is descriptive and organic. New op-codes are fine, but
do not reuse an existing op-code with different field semantics.

## Testing

Run the full unittest suite:

```bash
uv run python -m unittest discover tests
```

If the dev dependency group is installed, pytest is also available:

```bash
uv run pytest tests
```

Focused generator tests follow the module name:

```bash
uv run python -m unittest tests.test_quadratic_generator
```

Before handing off generator changes, also run:

```bash
uv run python tools/gen_opcode_legend.py --check
uv run python tools/gen_problem_types.py --check
uv run python quixi_math_datagen.py --sample --generators MyNewGenerator
```

For capacity checks, use:

```bash
uv run python tools/probe_generator_capacity.py
```

## Dependencies

- Python 3.9+
- Runtime dependencies: none beyond the standard library
- Dev dependency group: `pytest>=8.0`

## Project Structure

```text
quixi-math/
├── quixi_math_datagen.py      # Main CLI, sampling, validation, JSONL build
├── base_generator.py            # ProblemGenerator contract
├── helpers.py                   # step formatter, seeded UUID helper, utilities
├── curriculum.py                # class -> grade_level/difficulty table
├── generators/                  # generator implementations
├── tests/                       # unittest coverage and oracle helpers
├── tools/
│   ├── gen_opcode_legend.py     # regenerates OPCODES.md
│   ├── gen_problem_types.py     # regenerates PROBLEM_TYPES.md
│   └── probe_generator_capacity.py
├── DESIGN.md                    # architecture and answer conventions
├── OPCODES.md                   # generated op-code legend
├── PROBLEM_TYPES.md             # generated problem-type catalog
├── TODO.md                      # implementation follow-ups/history
├── AGENTS.md                    # coding-agent guidelines
└── pyproject.toml               # package metadata and dev dependencies
```

Generated datasets are written to the repo root unless `-o` points elsewhere.
Avoid committing large JSONL files; use `/tmp/...` for local experiments.

## Contributing

When adding a new generator:

1. Create `generators/my_new_generator.py` extending `ProblemGenerator`.
2. Create `tests/test_my_new_generator.py` with `unittest` coverage.
3. Include an oracle test that recomputes `final_answer` from the problem text
   alone, preferably by a route independent of the generator implementation.
4. Add an import and an instance to `ALL_GENERATORS` in
   `quixi_math_datagen.py`.
5. Add a `curriculum.CURRICULUM` entry for the class.
6. Regenerate `OPCODES.md` and `PROBLEM_TYPES.md`.
7. Run the focused test, a restricted seeded sample, and the full test suite.

Each generator must emit pipe-safe steps, use exact arithmetic when practical,
and end with `Z|<final_answer>`.
