# Dolphin Math Data Generator
<img width="410" alt="image" src="https://github.com/user-attachments/assets/f8a5d3d2-7820-4f7c-a5d3-fbac667e7084" />

## Purpose

This project generates synthetic math problems covering various arithmetic, algebra, geometry, and statistics topics. Crucially, it also generates detailed, step-by-step solutions intended to mimic the process a human would follow when solving the problem manually (like a "visible scratchpad").

The output is designed for training language models to perform multi-step mathematical reasoning.

It works for both SFT and RL. You should generate separate datasets for SFT and RL. SFT teaches it the syntax, RL teaches it to git gud at it.

## Features

**114 skills · ~224 problem operations · 283 scratchpad op-codes · every
generator oracle-tested.** The authoritative inventory is the code: run
`python dolphin_math_datagen.py --sample` to see one example of everything,
or read `curriculum.py` for the class → grade/difficulty table. The backlog
of what's next lives in [TODO.md](TODO.md).

Coverage by grade band (35 elementary · 44 middle · 35 high school):

- **Elementary (3-5):** the classic by-hand algorithms — long division with
  bring-downs, column addition/subtraction/multiplication with carries and
  borrows, fractions/decimals/percents with LCDs, factors/GCF/LCM via trial
  division and Euclid, place value, unit conversions, basic geometry, data
  reading, probability.
- **Middle (6-8):** ratios and proportional reasoning, integer operations,
  one/two-step equations and inequalities (including fraction/decimal
  coefficients cleared via LCD, and identities/contradictions), exponent
  rules (with decimal and fractional bases), scientific notation, angle
  relationships, circle/prism/cylinder/pyramid/cone/sphere measurement,
  statistics, compound probability, consumer math.
- **High school:** the full Algebra 1 factoring ladder (GCF, trinomials by
  visible trial-and-error, special forms, grouping), quadratics solved four
  ways (factoring, square roots, completing the square, formula) plus
  discriminant analysis, radicals end to end (simplify, add, multiply,
  rationalize with conjugates, rational exponents, radical equations with
  extraneous-root rejection), rational expressions, systems, lines,
  polynomials, and normal-distribution probability with the z-table
  excerpt supplied in the problem.

Signature behaviors, beyond topic coverage:

- **Visible trial-and-error** (`TRY`/`REJECT`/`ACCEPT`): factoring searches
  show every rejected candidate pair; radical equations test every
  candidate root in the original equation and reject the extraneous ones
  with the disagreement shown.
- **Self-verification** (`CHECK`): cross-multiplication, substitute-back,
  multiply-back, FOIL-back, and estimate comparisons — emitted on a
  fraction of examples so both habits appear in training.
- **Critic formats:** error-spotting (a worked scratchpad with one seeded,
  propagated mistake — find it, flag it, redo from that line) and
  fill-in-the-missing-step, with composite answers that make the reward
  ungameable. See DESIGN.md "Derived Record Formats".
- **Estimate-then-compute** variants that open with a 1-sig-fig or
  compatible-numbers `ESTIMATE` and close by comparing the exact result
  against it.


## Usage

### Generating Samples

To see one sample output from each generator type:

```bash
python dolphin_math_datagen.py --sample
```

You can optionally specify a random seed using `-s` or `--seed`.

Limit to specific generators (comma-separated class names):
```bash
python dolphin_math_datagen.py --sample --generators MultiDigitAdditionGenerator,LongDivisionGenerator
```

### Generating a Dataset

To generate a full dataset file in JSON Lines format:

```bash
python dolphin_math_datagen.py -n <number_of_examples> -o <output_file.jsonl>
```

You can restrict generation to a subset of generators:
```bash
python dolphin_math_datagen.py -n 5000 -o subset.jsonl --generators MultiDigitAdditionGenerator,DecimalMultGenerator
```

Example: Generate 50,000 examples with seed 123:
```bash
# Specify output file explicitly:
python dolphin_math_datagen.py -n 50000 -o my_dataset.jsonl -s 123

# Use default output filename (dolphin_math_50000.jsonl):
python dolphin_math_datagen.py -n 50000 -s 123
```

Default values are 10,000 examples (outputting to `dolphin_math_10000.jsonl` by default if `-o` is omitted). Omit `-s/--seed` for non-deterministic data; provide a seed to make runs reproducible byte-for-byte.

### Sampling, Weights, and Deduplication

Dataset builds sample **equally per skill** (generator class): variant instances of one class — e.g. the four `FractionOpGenerator` ops — share a single slot, so no skill is over-represented just because it has more instances. Override individual skill weights with `--weights` (unlisted skills keep weight 1.0):

```bash
# inline spec
python dolphin_math_datagen.py -n 10000 --weights "QuadraticGenerator=3,MeanGenerator=0.5"

# or a JSON file: {"QuadraticGenerator": 3}
python dolphin_math_datagen.py -n 10000 --weights weights.json
```

Exact repeats of `(operation, problem)` are skipped by default; pass `--allow-duplicates` to keep them. Each build prints a per-generator stats table (emitted / duplicates skipped / errors) and stops early with a warning if the selected skills' problem space is exhausted before reaching `-n`.

Note: `MixedNumberOperationsRandom` is excluded from the default pool (it duplicates the four `MixedNumberOperationGenerator` variants) but can still be requested explicitly via `--generators`.

### Running Tests

Unit tests are provided for each generator. To run all tests:

```bash
python -m unittest discover tests
# or, with the dev dependency group installed (uv sync):
uv run pytest tests
```

---

## Output Format

Each line of the generated JSONL is one problem:

```json
{
  "problem_id": "1f8b6be5-...",
  "operation": "long_division",
  "problem": "1834 / 5",
  "steps": ["D|18|5|3", "M|3|5|15", "S|18|15|3", "B|3|3|33", "...", "Z|366 R4"],
  "final_answer": "366 R4",
  "grade_level": "elementary",
  "difficulty": 3
}
```

- `steps` — the visible scratchpad: pipe-delimited op-code strings (`CODE|field|field|...`, up to 4 payload fields), ending with `Z|<final_answer>`.
- `grade_level` (`elementary` / `middle` / `high`) and `difficulty` (coarse 1-5 tier) are stamped from the per-class table in `curriculum.py`; a generator may emit either key itself to override (e.g. difficulty computed from its operands).

## Op-Code Legend

The full legend of op-codes in use lives in [OPCODES.md](OPCODES.md) — a **generated** file; regenerate it with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and the legend is *descriptive*, not prescriptive. The pipeline validates only step *structure* (op-code present, field count, final `Z|` matching `final_answer`) — never the vocabulary. When writing generators, stay consistent within a generator and keep every step human-legible: the same cues a person would write on paper.

---

## Curriculum Progress

114 skills implemented; the remaining backlog (currently ~372 items through
graduate-level math, physics, information theory, and transformer
arithmetic) lives in [TODO.md](TODO.md) — a pure backlog where shipped items
are deleted, so it never goes stale. Counts here are summaries; the code is
the source of truth.

---

## Dependencies

- Python 3.9+ (uses only standard library)
- No external packages required

---

## Project Structure

```
dolphin-math/
├── dolphin_math_datagen.py   # Main CLI and generator orchestration
├── base_generator.py         # Abstract base class for generators
├── helpers.py                # Utility functions (step formatter, UUID)
├── curriculum.py             # Class -> grade_level/difficulty table
├── tools/
│   └── gen_opcode_legend.py  # Regenerates OPCODES.md (--check to verify)
├── generators/               # All generator implementations
│   ├── __init__.py
│   ├── long_division_generator.py
│   ├── fraction_op_generator.py
│   └── ... (98 generator files)
├── tests/                    # Unit tests for all generators
│   ├── __init__.py
│   ├── test_long_division_generator.py
│   └── ... (101 test files)
├── OPCODES.md                # Generated op-code legend
├── DESIGN.md                 # Architecture, answer conventions, formats
├── README.md                 # This file
├── AGENTS.md                 # Guidelines for AI coding agents
├── TODO.md                   # Curriculum roadmap
└── pyproject.toml           # Package configuration
```

---

## Contributing

When adding a new generator:

1. Create `generators/my_new_generator.py` extending `ProblemGenerator`
2. Create `tests/test_my_new_generator.py` with unit tests, including an
   oracle that recomputes the answer from the problem text alone (see the
   A9 rule in AGENTS.md)
3. **IMPORTANT**: Add import and instance to `ALL_GENERATORS` in `dolphin_math_datagen.py`
4. Add the class to `curriculum.CURRICULUM` (grade_level + difficulty) — test-enforced
5. Regenerate the op-code legend: `python tools/gen_opcode_legend.py`
6. Delete the item's line from `TODO.md` (it's a pure backlog — only unimplemented skills are listed)
7. Run `python dolphin_math_datagen.py --sample --generators MyNewGenerator` to verify output
8. Run `python -m unittest discover tests` to ensure all tests pass
