# Repository Guidelines

## Project Structure & Module Organization
- Core entrypoint: `dolphin_math_datagen.py` orchestrates dataset builds and samples, instantiating all generator classes.
- Base contract: `base_generator.py` defines `ProblemGenerator.generate()` and expected output keys (`problem_id`, `operation`, `problem`, `steps`, `final_answer`).
- Generators: `generators/` holds one file per topic (e.g., `long_division_generator.py`, `quadratic_generator.py`). Each class should emit a final step starting with `Z|`.
- Tests: `tests/` mirrors generator names (`test_long_division_generator.py`, etc.) using `unittest`. Keep new tests co-located with matching generator names.
- Assets/output: JSONL datasets are written to repo root unless you pass an explicit path.

## Build, Test, and Development Commands
- Sample run of every generator: `python dolphin_math_datagen.py --sample` (seeded with `-s` for reproducibility).
- Full dataset: `python dolphin_math_datagen.py -n 50000 -o dolphin_math_50000.jsonl -s 123`.
- Default dataset filename when `-o` omitted: `dolphin_math_<n>.jsonl`.
- Tests (all): `python -m unittest discover tests`.
- Tests (focused): `python -m unittest tests.test_quadratic_generator`.

## Coding Style & Naming Conventions
- Python 3.9+; 4-space indentation; prefer explicit, side-effect-free helpers.
- Module/file naming: snake_case for modules and functions; UpperCamelCase for classes; constants in ALL_CAPS when needed.
- Keep `generate()` outputs deterministic under a provided seed; validate required keys and ensure `steps[-1]` carries the `Z|` opcode.
- Follow existing argument patterns (`op_symbol` for operator-specific generators) and keep error messages concise and informative.

## Testing Guidelines
- Add or update `unittest` cases in `tests/` for any new generator logic or edge handling; mirror test names to generator files.
- Use deterministic seeds in tests to stabilize expectations; assert both `steps` content and final answers where possible.
- Run `python -m unittest discover tests` before raising a PR; include targeted runs if only one generator is touched.

## Commit & Pull Request Guidelines
- Commit messages: short present-tense summaries (e.g., `add percent generator edge cases`, `fix quadratic step formatting`), matching existing history.
- Pull requests should include: purpose/summary, key commands run (tests, sample or dataset generation), sample output snippet or file path, and any linked issues.
- Screenshot/JSON snippets are welcome when changes affect output formatting or op-code ordering.
- Keep diffs minimal and grouped by concern (generator logic vs. tests vs. docs); avoid drive-by refactors unless necessary.

## Security & Configuration Tips
- Avoid writing large datasets to the repo by default; pass `-o /tmp/...` for local experiments.
- Do not log sensitive paths or environment details; printed output should be limited to sample/problem data and high-level progress.
