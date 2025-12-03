# Design Overview

## Architecture
- **Core contract:** `ProblemGenerator.generate() -> dict` (in `base_generator.py`) returns `problem_id`, `operation`, human-readable `problem`, `steps` (list of delimited op-codes), and `final_answer`. The last step must start with `Z|`.
- **Generators:** One class per skill in `generators/` (e.g., `long_division_generator.py`). Each is independent, seeded via `random` in `dolphin_math_datagen.py`, and responsible for validating its own outputs before returning.
- **Data flow:** `dolphin_math_datagen.py` seeds RNG, selects a generator, calls `generate()`, asserts required keys and final `Z|` step, then writes JSONL via `write_jsonl`. `--sample` prints one example per generator; `-n/-o/-s` builds datasets.
- **Step encoding:** Steps are pipe-delimited strings built with `helpers.step()` and `DELIM="|"`. Opcodes capture atomic reasoning moves (divide, multiply, bring-down, etc.) and end with `Z` holding the formatted answer string.
- **Extensibility:** To add a skill, create a new generator implementing `ProblemGenerator`, emit well-formed steps (including `Z|`), add it to `ALL_GENERATORS` in `dolphin_math_datagen.py`, and mirror tests in `tests/`.

## Curriculum (Generators & Skills)
- **Long Division:** Integers 2–99 divisors; includes bring-down (`B`), divide (`D`), multiply (`M`), subtract (`S`), remainder (`R`), and final `Z`.
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
