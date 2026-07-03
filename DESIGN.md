# Design Overview

## Architecture
- **Core contract:** `ProblemGenerator.generate() -> dict` (in `base_generator.py`) returns `problem_id`, `operation`, human-readable `problem`, `steps` (list of pipe-delimited op-code strings), and `final_answer`. The last step must be exactly `Z|<final_answer>`. The pipeline then stamps `grade_level` and `difficulty` from `curriculum.py` (generator-emitted values win).
- **Generators:** One class per skill in `generators/` (e.g., `long_division_generator.py`). Each is independent, seeded via `random` in `dolphin_math_datagen.py`, and responsible for validating its own outputs before returning.
- **Data flow:** `dolphin_math_datagen.py` seeds RNG, samples a skill (equal weight per class by default, `--weights` to override) then an instance within it, calls `generate()`, stamps metadata, runs `validate_example()`, dedups on `(operation, problem)`, then writes JSONL via `write_jsonl`. `--sample` prints one example per generator; `-n/-o/-s` builds datasets.
- **Step encoding:** Steps are pipe-delimited strings built with `helpers.step()` and `DELIM="|"`. Opcodes capture atomic reasoning moves (divide, multiply, bring-down, etc.) and end with `Z` holding the formatted answer string.
- **Extensibility:** To add a skill, create a new generator implementing `ProblemGenerator`, emit well-formed steps (including `Z|`), add it to `ALL_GENERATORS` in `dolphin_math_datagen.py`, add a `curriculum.CURRICULUM` entry, regenerate `OPCODES.md`, and mirror tests in `tests/`.

## Pipeline
- **Philosophy:** the scratchpad ultimately belongs to the model — it may invent its own op-codes. The op-code vocabulary is therefore *organic*: no fixed registry, no vocabulary enforcement. `OPCODES.md` is a generated, descriptive legend (`tools/gen_opcode_legend.py`, AST-scan of `step()` call sites plus sampled examples). One rule of hygiene is enforced socially, not mechanically: one op-code = one meaning (don't reuse an existing code with different field semantics).
- **Validation (`validate_example`):** structure only — required keys, non-empty `steps` of non-empty strings, op-code present, at most 4 payload fields per step, final step `Z|<final_answer>` (string-coerced), `grade_level` in {elementary, middle, high}, `difficulty` an int in 1–5.
- **Metadata:** `curriculum.py` maps every registered class to `grade_level`/`difficulty`; `stamp_metadata()` fills the keys post-`generate()` with setdefault semantics so generators can override per-instance. Test-enforced invariant: every `ALL_GENERATORS` class has a valid entry.
- **Sampling:** instances group into skills by class name; each skill draws with equal probability (or its `--weights` override), then one instance uniformly within the skill. `MixedNumberOperationsRandom` is excluded from the default pool as a duplicate of the four `MixedNumberOperationGenerator` variants.
- **Dedup & budget:** exact `(operation, problem)` repeats are skipped (unless `--allow-duplicates`); the attempt budget is `n*10 + 1000` with an early stop after `max(2000, n)` consecutive rejects (exhausted problem space). A per-generator stats table (emitted / duplicates skipped / errors) prints after every build, and `build_dataset` returns the same summary programmatically.
- **Reproducibility:** with `-s/--seed`, builds are byte-for-byte deterministic (`helpers.jid()` draws UUIDs from the seeded `random` module); without a seed, natural randomness.

## Answer Format Conventions (A0)

Validation requires `steps[-1] == "Z|" + final_answer` exactly, and RL graders
need one canonical form. These conventions are the contract; extend this
section (don't fork it) when a new tier introduces new answer shapes.

- **Integers:** plain: `-4`, `366 R4` (division with remainder).
- **Money:** `$20.06` — dollar sign, two decimals, cents always exact.
- **Percentages:** `15%`.
- **Fractions:** lowest terms, `5/2`; mixed numbers space-separated `8 1/2`;
  final answers in mixed-number contexts convert improper → mixed.
- **Decimals:** exact only, minimal digits (`11.4`, not `11.40`).
- **π-forms:** coefficient then π then unit: `36π cubic units`; fractional
  coefficient keeps π before the slash's denominator: `500π/3 cubic units`.
- **Units:** appended when the problem has them: `cubic units`, `square units`.
- **Powers:** `x^5`; negative exponents rewritten: `1/x^3`; fraction bases
  reciprocal-flipped: `(3/2)^2`; exponent 1 and 0 simplified away (`x`, `1`).
- **Single solutions:** bare value `7`. **Inequalities:** `x ≤ 9` (relation
  symbols < > ≤ ≥). **Systems:** `x=-2, y=-3`. **Special solutions:**
  `No solution`, `All real numbers`.
- **Factored forms** (Algebra 1 tier): ASCII signs inside factors,
  GCF first, binomial factors ordered by ascending constant term:
  `3(x - 4)(x + 2)`.
- **Multiple roots:** ascending, joined with " or ": `x = -3 or x = 2`.
- **Radicals:** coefficient then radical `6√2`; variables inside the radical
  parenthesized when compound: `5x√(2x)`; denominators rationalized.
- **Expressions:** terms in descending power order: `2x^2 + 3x - 5`.

## Verification & Trial-and-Error Vocabulary (A1 / A2)

- `CHECK|method|lhs_work|rhs_work` — two independent routes to the same
  value; the two work strings MUST agree. Methods so far: `cross_products`,
  `split`, `tip_two_ways`, `substitute`, `boundary_equality`,
  `multiply_back`. Emitted on roughly half of examples (both habits — with
  and without an explicit check — should appear in training).
- `CHECK_POINT|point|lhs_work|rhs_work` — evaluate both sides at a test
  point; agreement NOT required (a contradiction's check point deliberately
  disagrees; an identity's check points agree).
- `TRY|candidate|test_work` / `REJECT|candidate|reason` /
  `ACCEPT|candidate|confirmation` (A2, reserved) — candidate testing for
  factoring, rational-root search, and radical simplification. Real
  scratchpads contain dead ends; emit the tried-and-rejected candidates,
  not just the winner.

## Derived Record Formats (critic tasks)

**Format decision: no schema change.** A given (worked or partial)
scratchpad embeds in the `problem` text as numbered lines in the normal
pipe dialect — the model reads its own step language as input. The output
is ordinary `steps`. Step fields never contain pipes: given lines are
referenced by their 1-indexed number.

- **Error-spotting** (`error_spotting_*` operations): the problem shows a
  worked solution with exactly one arithmetic mistake; every given line
  after the mistake is consistent with it (real erring-student work — the
  error propagates). Output: `VERIFY|k|ok` sweeps each given line in order;
  `FLAG|k|<true arithmetic, pipe-free>` marks the wrong line; then the work
  is REDONE from line k in ordinary op-codes (lines after k are implicitly
  invalidated), ending with a CHECK where natural and `Z`.
  `final_answer` is composite (Principle 8): `step <k>; <correct answer>` —
  re-solving without locating the error earns nothing.
- **Fill-in-the-missing-step**: one given line is replaced by `____`;
  `final_answer` is the missing step verbatim (pipe format).
- **Estimate-then-compute**: not a new record shape — a variant where steps
  open with `ESTIMATE|<rounding work>|<estimate>` and close with
  `CHECK|magnitude|<estimate>|<exact>` before `Z`.

## Curriculum (Generators & Skills)
- **Long Division:** Integers 2–99 divisors; includes bring-down (`B`), divide (`D`), multiply (`M`), subtract (`S`), remainder (`R`), and final `Z`.
- **Multi-digit Addition (integers):** Column alignment (`INT_ALIGN`), per-column sums with carry (`ADD_COL`), final carry (`CARRY_FINAL`), and final `Z`.
- **Multi-digit Subtraction (integers):** Column alignment (`INT_ALIGN`), per-column differences with borrow (`SUB_COL`), explicit borrow steps (`BORROW`), final `Z`.
- **Multi-digit Multiplication (integers):** Multiplication setup (`MUL_SETUP`), digit-by-digit partials (`MUL_PARTIAL`), summing partials (`ADD_PARTIALS`), final `Z`.
- **Mixed Number Operations (+, -, *, /):** Convert to improper (`MIX_IMPROPER`), align denominators (`L`, `C`), invert for division (`I`), operate on numerators (`A`/`S`/`M`), simplify (`F`), convert back to mixed (`IMPROPER_TO_MIX`), final `Z`.
- **Fraction Comparison:** LCD (`L`, `C`), compare converted fractions (`CMP`), final `Z`.
- **Fraction/Decimal/Percent Conversions:** Conversions across forms (`FRAC_TO_DEC`, `DEC_TO_FRAC`, `PERCENT_TO_DEC`, `DEC_TO_PERCENT`), simplify where needed, final `Z`.
- **Factors & Multiples:** Factor listing via trial division (`FACT_CHECK`, `FACT_PAIR`), prime factorization via repeated division (`PF_STEP`, `PF_PRIME`), GCF via Euclid (`GCD_START`, `GCD_STEP`, `GCD_RESULT`), LCM via product/gcd (`LCM_FROM_GCD`), final `Z`.
- **Order of Operations:** Precedence steps with arithmetic ops and rewrites (`REWRITE`), final `Z`.
- **Geometry (Perimeter/Area/Volume):** Compute perimeters (`PERIM`), areas (`AREA`), and volumes (`VOLUME` for rectangular prisms) using explicit arithmetic steps and rewrites where needed, final `Z`.
- **Place Value & Rounding / Number Comparison:** Digit inspection (`ROUND_CHECK`), rounded result (`ROUND_RESULT`), alignment/comparison (`ALIGN_NUM`, `CMP_NUM`), final `Z`.
- **Divisibility & Classification:** Divisibility checks (`DIV_CHECK`), prime/composite markers (`PRIME`, `COMPOSITE_FACTOR`), final `Z`.
- **Unit Conversions:** Factor-label conversion (`CONV_FACTOR`, `CONV_RESULT`), explicit multiply, final `Z`.
- **Basic Data/Statistics/Probability:** Sort (`SORT`), arithmetic sums/divides for mean (`MEAN_DIV`), median selection (`MEDIAN_PICK`/`MEDIAN_PAIR`), mode counting (`MODE_COUNT`/`MODE`), simple probability setup (`PROB_SETUP`) with division/simplify, final `Z`.
- **Decimal Multiplication:** Partial products (`MUL_PARTIAL`), decimal placement (`COUNT_DP`, `PLACE_DP`), partial sums (`ADD_PARTIALS`).
- **Decimal Addition/Subtraction:** Column alignment (`DEC_ALIGN`), column operations (`DEC_ADD_COL`, `DEC_SUB_COL`), carries (`DEC_CARRY_FINAL`), final `Z`.
- **Decimal Division:** Decimal shifting (`DEC_SHIFT`), setup (`DIV_SETUP`), quotient decimal placement (`PLACE_DP_Q`), reuse of `B/D/M/S`.
- **Fraction Operations (+, -, *, /):** LCD and conversions (`L`, `C`), simplification (`F`), inversion (`I`), arithmetic (`A`, `M`, `D`, `S` reused contextually), final `Z`.
- **Linear Equations (Simple/Complex):** Move terms (`MOVE_TERM`), combine like terms (`COMB_X`, `COMB_CONST`), divide coefficients (`DIV_COEFF`), rewrite (`REWRITE`), final `Z`.
- **Quadratic Equations:** Discriminant (`DISC`), root extraction (`ROOT`), quadratic formula branches (`Q1`, `Q2`), final `Z`.
- **Simplify Algebraic Expressions:** Distribution (`DIST`), combining terms, rewrites, final `Z`.
- **Evaluate Expressions:** Substitution (`SUBST`), arithmetic steps as needed, final `Z`.
- **Proportional Relationships:** Proportion setup (`PROP_SETUP`), solving via algebraic steps, final `Z`.
- **Pythagorean Hypotenuse:** Exponents (`E`), square root (`ROOT`), final `Z`.
- **Percent Problems (find part/percent/whole):** Percent-to-decimal (`PERCENT_TO_DEC`), equation setup/rearrange (`SETUP_PERCENT_EQ`, `REARRANGE_EQ`), calculation (`PERCENT_CALC_PART`), convert back (`DEC_TO_PERCENT`), final `Z`.
- **Abacus-Style Addition:** Initial set (`AB_SET`), informational notes (`AB_INFO`), column adds (`AB_ADD_DGT`), carry propagation (`AB_CARRY`, `AB_CARRY_FINAL`), final `Z`.
- **Graph Interpretation (Bar/Line/Pictograph):** Graph data recording (`GRAPH_DATA`), value reading (`GRAPH_READ`), comparisons (`CMP`), min/max identification (`GRAPH_MIN`, `GRAPH_MAX`), change tracking (`GRAPH_CHANGE`, `GRAPH_MAX_CHANGE`), pictograph key (`PICTO_KEY`) and symbol counting (`PICTO_COUNT`), arithmetic steps reused (`A`, `S`, `M`), final `Z`.
