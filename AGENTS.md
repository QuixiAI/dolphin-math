# Repository Guidelines

## Project Structure & Module Organization
- Core entrypoint: `dolphin_math_datagen.py` orchestrates dataset builds and samples, instantiating generator classes and handling `--generators` filtering. Mixed-number ops include a random wrapper; factors/GCF/LCM, conversions/comparisons, and order-of-operations generators are wired in.
- Base contract: `base_generator.py` defines `ProblemGenerator.generate()` with required keys (`problem_id`, `operation`, `problem`, `steps`, `final_answer`); `steps[-1]` must start with `Z|`.
- Generators: `generators/` holds one file per skill (e.g., `multi_digit_addition_generator.py`, `long_division_generator.py`). Add new classes there and to `ALL_GENERATORS`.
- **CRITICAL:** Every new generator class MUST be registered in `dolphin_math_datagen.py`:
  1. Add an import statement at the top of the file (e.g., `from generators.my_new_generator import MyNewGenerator`)
  2. Add an instance to the `ALL_GENERATORS` list (e.g., `MyNewGenerator()`)
  Generators not in `ALL_GENERATORS` will NOT appear in `--sample` output or dataset generation!
- Tests: `tests/` mirrors generator names (`test_long_division_generator.py`, etc.) using `unittest`. Keep new tests co-located with matching generator names.
- Artifacts: JSONL datasets write to repo root unless you pass `-o`. Avoid committing large generated files.

## Build, Test, and Development Commands
- **Virtual environment:** Always activate the venv before running commands: `source .venv/bin/activate`
- Sample run: `python dolphin_math_datagen.py --sample` (add `--generators ClassA,ClassB` to limit; add `-s` to fix seed).
- Full dataset: `python dolphin_math_datagen.py -n 50000 -o dolphin_math_50000.jsonl` (optionally add `--generators ...` and `-s`).
- Default dataset filename when `-o` omitted: `dolphin_math_<n>.jsonl`.
- Tests (all): `python -m unittest discover tests`.
- Tests (focused): `python -m unittest tests.test_quadratic_generator`.

## Coding Style & Naming Conventions
- Python 3.9+; 4-space indentation; prefer explicit, side-effect-free helpers.
- Module/file naming: snake_case for modules and functions; UpperCamelCase for classes; constants in ALL_CAPS when needed.
- Determinism only when a seed is provided; otherwise allow natural randomness. Always emit `Z|` as the final step. For mixed numbers, always emit `F` and `IMPROPER_TO_MIX` when applicable; for percent/conversion outputs avoid scientific notation; for factor/gcd/lcm flows include human-readable steps (trial division, Euclid steps, LCD comparisons); for order-of-operations include `REWRITE` steps after each precedence move.
- Follow existing patterns (e.g., `op_symbol` for operator-specific generators); keep error messages concise and informative.

## Testing Guidelines
- Add/extend `unittest` cases in `tests/` for each generator; mirror file names.
- Use deterministic seeds in tests to stabilize expectations; assert both `steps` content and final answers where possible. Patch `random` if you need specific borrow/carry scenarios.
- Run `python -m unittest discover tests` before raising a PR; include targeted runs when touching a single generator.
- Manual check: `python dolphin_math_datagen.py --sample --generators <GeneratorName>` and verify the steps match human pencil-and-paper workflow (alignment, carries/borrows, etc.).
- For new skills: define op-codes upfront, keep every arithmetic action explicit (no hidden mental math), and ensure rewrites show the current expression after each operation.

## Commit & Pull Request Guidelines
- Commit messages: short present-tense summaries (e.g., `add percent generator edge cases`, `fix quadratic step formatting`), matching existing history.
- Pull requests should include: purpose/summary, key commands run (tests, sample or dataset generation), sample output snippet or file path, and any linked issues.
- Screenshot/JSON snippets are welcome when changes affect output formatting or op-code ordering.
- Keep diffs minimal and grouped by concern (generator logic vs. tests vs. docs); avoid drive-by refactors unless necessary.

## Security & Configuration Tips
- Avoid writing large datasets to the repo by default; pass `-o /tmp/...` for local experiments.
- Do not log sensitive paths or environment details; printed output should be limited to sample/problem data and high-level progress.
- Keep `pyproject.toml` dependencies minimal (currently stdlib); if adding deps, document why and pin versions.
