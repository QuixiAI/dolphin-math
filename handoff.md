# Handoff — dolphin-math generator backlog

Everything a new agent needs to resume building this synthetic math dataset.
Read this once, then work from `TODO.md`, `DESIGN.md`, and `AGENTS.md`.

## What this project is

`dolphin-math` (github.com:QuixiAI/dolphin-math) is a synthetic math dataset
that teaches a model to use a **pipe-delimited scratchpad**. Each record is one
problem worked start to finish, where the visible reasoning is a list of
op-code steps. The dataset is produced by independent Python *generators* — 216
distinct problem-type classes across ~206 files (a few files define more than
one class; a few classes are registered as several instances/variants) — each
emitting fully-worked examples with an exactly checkable final answer.
`PROBLEM_TYPES.md` is the authoritative catalog and count.

Record schema (every generator returns this dict):

```python
{
  "problem_id": jid(),                 # helpers.jid() — random id
  "operation": "z_score_standardize",  # "<generator>_<variant>"
  "problem":  "…natural-language prompt…",
  "steps":    ["CODE|f1|f2|f3|f4", …, "Z|<final_answer>"],
  "final_answer": "<string>",
  # grade_level / difficulty are stamped by the pipeline (see below),
  # or emitted by the generator to override.
}
```

- Steps are strings built by `helpers.step(code, *fields)` — **max 4 payload
  fields** after the op-code. The last step is always `Z|<final_answer>` and
  `steps[-1] == "Z|" + str(final_answer)` holds universally.
- The scratchpad vocabulary **belongs to the model**: op-codes are organic, one
  code = one meaning, invented freely. `OPCODES.md` is descriptive/generated,
  not a registry. Reuse an existing code only if the field semantics match.

## The standing task (the loop)

The user runs a self-paced `/loop`: **work the `TODO.md` backlog one item at a
time until told to stop.** Per iteration:

1. If an item is in progress (uncommitted generator work), continue it;
   otherwise pick the next actionable item from `TODO.md` per the **Suggested
   Order** section (near the bottom of `TODO.md`), prioritizing the "Critic &
   Estimation Formats" section until empty (currently empty — see its note).
2. Implement the generator per the item's inline contract:
   `- [ ] description · \`ClassName\` · grade · d<difficulty>`.
   Every arithmetic action is an explicit step; steps are human-legible (the
   cues a person writes on paper); include CHECK / trial-and-error steps when
   the item calls for them.
3. Write a mirrored `tests/test_<snake>.py` with an **independent A9 oracle**
   that recomputes `final_answer` **from the problem text alone** (see below).
4. Register in three places (details below) and regenerate `OPCODES.md` **and**
   `PROBLEM_TYPES.md`.
5. Run **only the new generator's test file** (per Eric — do NOT run the whole
   suite during generator development; it's slow and against his instruction).
6. Build ~200 seeded examples restricted to the new generator; check the
   dedup/stats table for problem-space exhaustion **and zero validation
   errors**.
7. Critically review the generated examples: math correctness, faithful
   pencil-and-paper procedure, answer format, difficulty spread. Fix and
   rebuild until excellent.
8. When excellent: delete the item's line from `TODO.md`, commit (rules below),
   push, and **immediately continue to the next item in the same turn** — chain
   as many items as possible with no idle pauses. Only schedule a wakeup when
   *ending* a turn.

At a turn boundary, it's worth running the **full** suite once
(`uv run python -m unittest discover tests`, ~4s, ~1200 tests) as a cross-file
regression check — that's how a latent legend bug got caught this session.

## Hard rules (do not violate)

- **Commit author:** sole author `Eric Hartford <eric@quixi.ai>`, **NO
  `Co-Authored-By` trailer, ever.** Commit with
  `git commit --author="Eric Hartford <eric@quixi.ai>" -m "short present-tense message"`.
  (There's a memory file enforcing this.)
- **Test only the new generator** during development (`uv run python -m unittest
  tests.test_<name>`). Nothing in a test should take over a minute.
- **No idle pauses** between items — chain them within a turn.
- **`uv run python …`** for everything — bare `python` is not on PATH.
- **Pipe-safety:** a step field must NEVER contain a raw ASCII `|`. Use
  `abs(r)` not `|r|`, and `‖u‖` not `|u|`. A stray `|` inflates the field count
  and fails `validate_example` ("more than 4 payload fields"). This bit us twice
  this session (DOT_FORMULA, z-score `|z| > 2 rule`).
- **Principle 5:** any needed transcendental / lookup value (trig values, z*,
  t*, ln 2, N(d₁)) is **supplied in the problem text**, avoided by construction
  (dyadic probabilities, nice angles, perfect-square n), or the answer stays
  symbolic/exact. Never emit a rounded decimal as if exact.
- **Exactness:** final answers are exact — integers, `Fraction`s, exact decimals
  (`dec()`), exact radicals (`sqrt_txt`), exact π (`pi_txt`), or symbolic. Build
  the data so this is possible (see "Exactness engineering" below).

## Repo layout & key files

- `generators/*.py` — one class per problem type; each has `generate() -> dict`
  and usually a `variant` constructor arg + `VARIANTS` list.
- `tests/test_*.py` — mirrored unittest files with A9 oracles.
- `dolphin_math_datagen.py` — the pipeline: `ALL_GENERATORS` list, imports,
  `validate_example`, `stamp_metadata`, skill sampling, dedup, stats table, CLI.
- `curriculum.py` — `CURRICULUM: {ClassName: {grade_level, difficulty}}`,
  `GRADE_LEVELS`, `stamp_metadata`, `clamp_difficulty`. Grade bands:
  `elementary, middle, high, college, graduate`. Difficulty 1–5 read **relative
  to the band**.
- `helpers.py` — `step`, `jid`, `DELIM` (`"|"`).
- `OPCODES.md` — generated by `tools/gen_opcode_legend.py` (`--check` verifies).
- `PROBLEM_TYPES.md` — generated by `tools/gen_problem_types.py` (`--check`);
  user-facing catalog (description + grade/difficulty + variants + a worked
  example per generator).
- `tools/check_backlog.py` — fails if a shipped (registered) generator still has
  an unchecked `TODO.md` line.
- `DESIGN.md` — pipeline contract, answer-format conventions, "Derived Record
  Formats" (critic/estimate formats). `AGENTS.md` — the checklist & commands.

## Registration chain (edit exactly these, in order)

For a new `FooGenerator` in `generators/foo_generator.py`:

1. `dolphin_math_datagen.py`: add `from generators.foo_generator import
   FooGenerator` next to the previous import, and `FooGenerator(),` in the
   `ALL_GENERATORS` list next to the previous instance.
2. `curriculum.py`: add `"FooGenerator": {"grade_level": HIGH, "difficulty":
   5},` next to the previous entry (use the item's grade/difficulty).
3. Regenerate: `uv run python tools/gen_opcode_legend.py` and
   `uv run python tools/gen_problem_types.py`.

The `test_datagen_pipeline` "coverage invariant" enforces that every
`ALL_GENERATORS` class has a valid `CURRICULUM` entry — a missing entry fails
the full suite.

## Commands (copy-paste)

```bash
# test only the new generator
uv run python -m unittest tests.test_foo_generator

# regenerate the two generated docs
uv run python tools/gen_opcode_legend.py
uv run python tools/gen_problem_types.py

# build ~200 restricted examples (seeded) and read the stats table
uv run python dolphin_math_datagen.py -n 200 -o /tmp/foo.jsonl -s 7 --generators FooGenerator

# full suite (turn boundary only)
uv run python -m unittest discover tests

# backlog honesty check
uv run python tools/check_backlog.py

# commit + push
git add -A && git commit --author="Eric Hartford <eric@quixi.ai>" -m "add foo generator" && git push
```

The build's stats table prints `emitted / dup_skip / errors`. **errors must be
0.** A high `dup_skip` with `emitted < 200` and a `WARN` means the problem space
is exhausted — that's acceptable for small deterministic spaces (log it, move
on), not a failure.

## The A9 oracle (required in every test)

The load-bearing quality gate. Each test recomputes `final_answer` **from
`problem` text alone** by an *independent* method, then asserts equality over
hundreds of samples. Independent means: don't re-run the generator's own
formula — use a different route. Styles used successfully:

- Exact `Fraction` recomputation from parsed problem values.
- Numeric central-difference secants for derivatives / antiderivatives.
- Numeric quadrature (midpoint on geometric grids) for integrals, incl. improper.
- Brute-force sweeps / lattice counts / special-angle enumeration.
- Polyline length for arc length; on-curve slope for implicit diff.
- Perfect-square / identity checks (A·A⁻¹ = I, derivative-recovers-integrand).

Oracles repeatedly caught real generator bugs pre-ship this session (reversed
tax/cost operands, a decimal-point parser break, unrealistic sample sizes).
**Trust the oracle; when it fails, the generator is usually wrong, not the
oracle** — but check both.

Also standard in each test: output-contract test, `test_all_variants_reachable`,
`test_fixed_variant_constructor` (bad variant → `ValueError`), a pipe-safety /
degenerate-render check, and (where relevant) a "both outcomes occur" test for
decision variants.

## Rendering conventions (from DESIGN.md; enforce by eye + degenerate tests)

No `1x` / `-1x` / `1(` / `^1` / `+ 0`; substituted values parenthesized
(`2(3)`); explicit `·` between a numeric coefficient and numeric base
(`-4·5^x`); money `$X.YY`; exact decimals via `dec(Fraction)`; exact π via
`pi_txt`; radicals via `sqrt_txt`; `+ C` on antiderivatives; units on
word-problem answers. A common test guards these with regex like
`(?<!\d)1x`, `"--"`, `r"\+ -"`, `r"\^1\b"`.

## Exactness engineering (the recurring trick — this is the craft)

Answers must be exact, so **construct the data backwards from a clean answer**:

- Pythagorean triples for right-triangle sides; `sqrt_txt` for exact radicals.
- Perfect-square denominators / sample sizes so `√n` is an integer
  (`ConfidenceInterval`, `HypothesisTest` use `n ∈ {25,100,400}`).
- Probabilities/steps over a denominator dividing 100 (or 2^a·5^b) so
  `dec()` terminates (`ExpectedValue` uses `{4,5,10,20}`).
- `p̂ = 0.5` for proportion SEs (only case where `p̂(1−p̂)` is a perfect square).
- **`RegressionGenerator`** is the showcase: fix `x = 1..5` (so `Sxx = 10`), and
  make `y`-deviations a scaled permutation of `{−2,−1,0,1,2}` so `Syy = 10k²`
  and `√(Sxx·Syy) = 10k` is a perfect square → `b`, `a`, `r`, `r²`, residuals
  all exact decimals.
- Divisible coefficients for antiderivatives; L·U integer Gaussian elimination;
  unit-pivot U; squarefree radicands.
- `dec()` (in `exponential_model_generator`) only works for terminating decimals
  (denominator 2^a·5^b) — it silently assumes that. If a value might not
  terminate, render a `Fraction` string instead, or constrain inputs so it does.

Shared helpers worth reusing (import paths):
`helpers.step/jid/DELIM`; `exponential_model_generator.dec/money`;
`arc_sector_generator.pi_txt`; `geometric_mean_generator.sqrt_txt`;
`integration_by_parts_generator.cm` (coefficient·body renderer);
`mixed_number_operation_generator.to_improper/to_mixed`;
`matrix_ops_generator.mat/rnd_mat`; `factor_trinomial_generator.pair_search`
(raises `ValueError` on product 0 — exclude zero roots).

## Gotchas learned this session

- **Pipe injection** in a step field (see Hard rules). Add a pipe-safety
  assertion to every test.
- **Latent bugs in pre-existing generators** surface when you add A9 oracles:
  `PercentWordProblemGenerator` had reversed tax operands; the proportion
  generator had reversed cost/ratio operands. When rewriting an old generator,
  its old mock-based test may need to become an A9 oracle test.
- **`gen_opcode_legend` dynamic sites:** if a generator emits op-codes from a
  data catalog via a loop variable (`for code,… in path: step(code,…)`), the
  scanner now harvests them from tuple literals (fixed this session). Don't
  reintroduce a bare `step(f"X_{i}", …)` — that becomes an unresolved warning.
- **Oracle regex traps:** decimals break `[^.]`/`[\d.]+` parsers (`0.3.` swallows
  the sentence period; `76.5` splits on the internal dot). Split on `". "`
  (period-space) or use `(\d+(?:\.\d+)?)` and `rstrip('.')`.
- **Substring routing** in multi-variant oracles: order conditions from most
  specific to least (a sample-size-mean problem also contains "confidence
  interval for the mean").
- **Realism:** exact ≠ sensible. A proportion margin of error of 1 gives n=1;
  keep proportion margins small (`{0.02,0.025,0.04,0.05,0.1}`).

## Current state (as of this handoff)

- 216 registered generator classes (~206 files); ~212 test files; full suite
  ~1198 tests, green.
- **Done tracks:** Functions, Sequences & Series, Complex Numbers, Polynomials
  & Rational Functions, Exponentials & Logarithms, Conics, Geometry, Trig,
  Vectors & Matrices, Limits, Calculus Derivatives, Calculus Integrals & ODEs,
  Calculus Series (BC). Statistics: FiveNumberSummary, StandardDeviation,
  ZScore, FrequencyTable, Regression, ExpectedValue, ConfidenceInterval,
  HypothesisTest.
- **Cross-Cutting Upgrades A3–A8 all done** (section is empty): per-instance
  difficulty (A3, on the four integer-arithmetic generators via
  `curriculum.clamp_difficulty`), phrasing banks (A4) + distractor variants (A6)
  on the word-problem generators, `CompositeArithmeticGenerator` (A5),
  `tools/check_backlog.py` (A7), `college`/`graduate` grade bands (A8).
- Registration-chain tails: `dolphin_math_datagen.py` import + instance for
  `HypothesisTestGenerator`; `curriculum.py` entry likewise.

## Next actionable items (in Suggested Order)

1. **`ChiSquareGenerator`** · high · d5 — goodness-of-fit and independence with
   expected-count tables (last Statistics item). Exactness: build observed
   counts so χ² = Σ(O−E)²/E is a clean fraction; provide the critical value
   (Principle 5) and decide reject / fail to reject.
2. **Probability track:** `PermutationCombinationGenerator` (middle · d4, note:
   "was falsely checked off — no generator exists"), `BinomialProbabilityGenerator`
   (middle · d4, also falsely checked off — use nCr/Pascal, dyadic p for exact),
   `ProbabilityAdditionRuleGenerator`, `ConditionalProbabilityGenerator`
   (two-way tables + simple Bayes), `GeometricProbabilityGenerator`,
   `GeometricDistributionGenerator`.
3. **Applied & Cross-Disciplinary:** Finance, Kinematics, PhysicsFormula,
   BaseConversion, BaseArithmetic, BitwiseOps, ModularArithmetic (ISBN-10/Luhn),
   ManualSquareRoot, CalendarArithmetic, FermiEstimation.
4. Then the University & Graduate backlog (a large trunk — Multivariable Calc,
   Linear Algebra, ODEs, Discrete, Number Theory, Numerical Methods, then
   applied physics, then graduate/frontier). See `TODO.md` Suggested Order §9–12.

`TODO.md` is the source of truth; `git log` shows the running history (short
present-tense messages, one generator per commit). The loop's wakeup prompt is
already scheduled and carries the full per-item instructions.
