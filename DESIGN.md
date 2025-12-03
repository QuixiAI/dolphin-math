# Design Overview

## Architecture
- **Core contract:** `ProblemGenerator.generate() -> dict` (in `base_generator.py`) returns `problem_id`, `operation`, human-readable `problem`, `steps` (list of delimited op-codes), and `final_answer`. The last step must start with `Z|`.
- **Generators:** One class per skill in `generators/` (e.g., `long_division_generator.py`). Each is independent, seeded via `random` in `dolphin_math_datagen.py`, and responsible for validating its own outputs before returning.
- **Data flow:** `dolphin_math_datagen.py` seeds RNG, selects a generator, calls `generate()`, asserts required keys and final `Z|` step, then writes JSONL via `write_jsonl`. `--sample` prints one example per generator; `-n/-o/-s` builds datasets.
- **Step encoding:** Steps are pipe-delimited strings built with `helpers.step()` and `DELIM="|"`. Opcodes capture atomic reasoning moves (divide, multiply, bring-down, etc.) and end with `Z` holding the formatted answer string.
- **Extensibility:** To add a skill, create a new generator implementing `ProblemGenerator`, emit well-formed steps (including `Z|`), add it to `ALL_GENERATORS` in `dolphin_math_datagen.py`, and mirror tests in `tests/`.

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
