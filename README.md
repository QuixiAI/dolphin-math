# Dolphin Math Data Generator
<img width="410" alt="image" src="https://github.com/user-attachments/assets/f8a5d3d2-7820-4f7c-a5d3-fbac667e7084" />

## Purpose

This project generates synthetic math problems covering various arithmetic, algebra, geometry, and statistics topics. Crucially, it also generates detailed, step-by-step solutions intended to mimic the process a human would follow when solving the problem manually (like a "visible scratchpad").

The output is designed for training language models to perform multi-step mathematical reasoning.

It works for both SFT and RL. You should generate separate datasets for SFT and RL. SFT teaches it the syntax, RL teaches it to git gud at it.

## Features

### Elementary (Grades 3-5) — 34 Problem Types

#### Basic Arithmetic
- **Long Division** — with remainder, showing divide/multiply/subtract/bring-down cycle
- **Multi-digit Addition** — standard column algorithm with carries
- **Multi-digit Subtraction** — standard column algorithm with borrows
- **Multi-digit Multiplication** — partial products method
- **Mixed Number Operations** — all four operations (+, -, *, /) with LCD, simplification
- **Fraction Comparison** — find common denominator and compare
- **Fraction/Decimal/Percent Conversions** — bidirectional conversions
- **Decimal Addition/Subtraction** — column alignment with decimal points
- **Decimal Multiplication** — integer multiplication then decimal placement
- **Decimal Division** — shift decimals, long division, place decimal in quotient
- **Fraction Operations** — add, subtract, multiply, divide with LCD and simplification

#### Factors & Multiples
- **Finding All Factors** — trial division with factor pairs
- **Prime Factorization** — factor tree method
- **GCF (Greatest Common Factor)** — Euclidean algorithm
- **LCM (Least Common Multiple)** — via GCD formula

#### Order of Operations
- **PEMDAS Problems** — with rewrite steps showing work

#### Basic Geometry
- **Perimeter/Area of Rectangles, Squares, Triangles, Parallelograms, Trapezoids**
- **Perimeter of General Polygons** — sum of all sides
- **Volume of Rectangular Prisms**

#### Number Sense
- **Place Value and Rounding** — whole numbers and decimals
- **Comparing/Ordering Numbers** — whole numbers and decimals
- **Divisibility Rules** — prime/composite classification

#### Units & Measurement
- **Unit Conversions** — length, weight, capacity, time, money

#### Data & Probability
- **Mean, Median, Mode** — for small datasets
- **Simple Probability** — single event with uniform outcomes
- **Graph Interpretation** — bar charts, line graphs, pictographs

#### Tools/Methods
- **Abacus-style Addition** — column-by-column with carries

---

### Middle School (Grades 6-8) — 41 Problem Types

#### Ratios & Proportions
- **Unit Rate Calculations** — find rate per unit
- **Unit Rate from Tables** — extract rate from data tables
- **Scaling Problems** — maps, blueprints, models
- **Similar Figures** — find missing sides using scale factors
- **Proportional Relationships** — solve proportions

#### Integer Operations
- **Adding/Subtracting Integers** — with number line reasoning
- **Multiplying/Dividing Integers** — sign rules

#### Expressions & Equations
- **One-step Equations** — all operations (x+a=b, ax=b, etc.)
- **Two-step Equations** — (ax+b=c, a(x+b)=c, etc.)
- **One-step Inequalities** — with inequality flip for negative coefficients
- **Two-step Inequalities** — with proper sign handling
- **Simple Linear Equations** — (ax + b = c)
- **Complex Linear Equations** — variables on both sides (ax + b = cx + d)
- **Simplifying Expressions** — distribution and combining like terms
- **Evaluating Expressions** — variable substitution

#### Exponents & Roots
- **Exponent Evaluation** — compute powers like 2^5, (-3)^4
- **Exponent Rules** — product, quotient, power, negative, zero exponent
- **Scientific Notation** — convert to/from, operations
- **Square Roots** — perfect squares
- **Cube Roots** — perfect cubes
- **Simplifying Radicals** — √72 → 6√2

#### Geometry
- **Angle Relationships** — complementary, supplementary, vertical (numeric and algebraic)
- **Angles with Parallel Lines** — corresponding, alternate interior/exterior, co-interior
- **Triangle Angle Sum** — find missing angle
- **Exterior Angle Theorem**
- **Circle Area and Circumference** — with π symbol or decimal
- **Volume of Prisms** — rectangular and triangular
- **Volume of Cylinders**
- **Surface Area of Prisms**
- **Surface Area of Cylinders**
- **Pythagorean Theorem — Find Hypotenuse**
- **Pythagorean Theorem — Find Leg**
- **Pythagorean Word Problems** — ladders, distances, etc.

#### Statistics
- **Mean (Average)** — sum and divide with steps
- **Median** — sort and find middle
- **Mode** — frequency counting (unimodal, bimodal, no mode)
- **Range** — max minus min
- **Mean Absolute Deviation (MAD)**

#### Probability
- **Simple Probability** — P = favorable/total
- **Compound Probability — Independent Events** — coin flips, dice
- **Compound Probability — Dependent Events** — drawing without replacement

---

### High School — 6 Problem Types (more coming)

#### Algebra
- **Quadratic Equations** — using quadratic formula with discriminant
- **Percentage Problems** — find part, percent, or whole

---

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

Default values are 10,000 examples (outputting to `dolphin_math_10000.jsonl` by default if `-o` is omitted). Omit `-s/--seed` for non-deterministic data; provide a seed to make runs reproducible.

### Running Tests

Unit tests are provided for each generator. To run all tests:

```bash
python -m unittest discover tests
```

---

## Op-Code Reference

The `steps` field in the output JSON contains a list of strings, each representing a step in the solution. Steps are formatted as `OP_CODE|arg1|arg2|...`.

### Naming Conventions

- **Short codes** (1-2 chars): Core arithmetic operations used across many generators
- **Prefixed codes**: Domain-specific operations grouped by prefix (e.g., `STAT_`, `EQ_`, `PYTHAG_`)

### Core Arithmetic (used across generators)
| Code | Description | Arguments |
|------|-------------|-----------|
| `A` | Add | addend1, addend2, sum |
| `S` | Subtract | minuend, subtrahend, difference |
| `M` | Multiply | factor1, factor2, product |
| `D` | Divide | dividend, divisor, quotient |
| `B` | Bring down (long division) | remainder_before, digit_down, new_number |
| `R` | Remainder | final_remainder |
| `E` | Exponent/Power | base, exponent, result |
| `Z` | Final answer | answer_string |

### Fractions
| Code | Description | Arguments |
|------|-------------|-----------|
| `L` | Find LCD | denominator1, denominator2, lcd |
| `C` | Convert to LCD | original_fraction, lcd, converted_fraction |
| `I` | Invert fraction | original, inverted |
| `F` | Simplify fraction | unsimplified, simplified |
| `CMP` | Compare fractions | frac1, frac2, relation (<, >, =) |

### Mixed Numbers
| Code | Description | Arguments |
|------|-------------|-----------|
| `MIX_IMPROPER` | Convert mixed to improper | mixed_str, improper_str |
| `IMPROPER_TO_MIX` | Convert improper to mixed | improper_str, mixed_str |

### Integer Column Arithmetic
| Code | Description | Arguments |
|------|-------------|-----------|
| `INT_ALIGN` | Align numbers for column math | num1_padded, num2_padded |
| `ADD_COL` | Add column | col_name, calculation, result_with_carry |
| `SUB_COL` | Subtract column | col_name, calculation, result_with_borrow |
| `BORROW` | Borrow from next column | col_name, from_left, 1 |
| `CARRY_FINAL` | Final carry digit | carry_value |

### Decimal Arithmetic
| Code | Description | Arguments |
|------|-------------|-----------|
| `DEC_ALIGN` | Align by decimal point | num1_aligned, num2_aligned |
| `DEC_ADD_COL` | Add decimal column | col_name, calculation, result |
| `DEC_SUB_COL` | Subtract decimal column | col_name, calculation, result |
| `DEC_CARRY_FINAL` | Final decimal carry | carry_value |
| `DEC_SHIFT` | Shift decimal for division | original_expr, shifted_expr, places |
| `MUL_SETUP` | Setup multiplication | int1, int2 |
| `MUL_PARTIAL` | Partial product | digit, multiplicand, partial_product |
| `ADD_PARTIALS` | Sum partial products | expression, result |
| `COUNT_DP` | Count decimal places | dp1, dp2, total |
| `PLACE_DP` | Place decimal in result | integer_result, places, final_result |
| `DIV_SETUP` | Setup division | dividend, divisor |
| `PLACE_DP_Q` | Place decimal in quotient | quotient_digits, position |

### Factors & Multiples
| Code | Description | Arguments |
|------|-------------|-----------|
| `FACT_CHECK` | Check divisibility | n, divisor, remainder |
| `FACT_PAIR` | Record factor pair | factor1, factor2 |
| `PF_STEP` | Prime factorization step | n, prime, quotient |
| `PF_PRIME` | Mark as prime | n |
| `GCD_START` | Start Euclidean algorithm | a, b |
| `GCD_STEP` | Euclidean step | a, b, remainder |
| `GCD_RESULT` | Final GCD | gcd |
| `LCM_FROM_GCD` | Compute LCM | product_expr, gcd, lcm |

### Equations & Inequalities
| Code | Description | Arguments |
|------|-------------|-----------|
| `EQ_SETUP` | Show equation | equation_string |
| `EQ_OP_BOTH` | Apply operation to both sides | operation, value, result_expr, result_value |
| `EQ_SIMPLIFY` | Simplify equation | simplified_equation |
| `EQ_RESULT` | Final result | variable, value |
| `INEQ_SETUP` | Show inequality | inequality_string |
| `INEQ_OP_BOTH` | Apply operation to both sides | operation, value, result_expr, result_value |
| `INEQ_SIMPLIFY` | Simplify inequality | simplified_inequality |
| `INEQ_FLIP` | Flip inequality sign | reason |
| `INEQ_RESULT` | Final result | variable, relation, value |

### Algebra
| Code | Description | Arguments |
|------|-------------|-----------|
| `REWRITE` | Rewrite expression | new_form |
| `DIST` | Distribute | factor, expression, result |
| `COMB_X` | Combine x terms | term1, term2, result |
| `COMB_CONST` | Combine constants | const1, const2, result |
| `SUBST` | Substitute value | variable, value, result_expression |
| `MOVE_TERM` | Move term across equals | term, target_side, result_equation |
| `DIV_COEFF` | Divide by coefficient | numerator, denominator, result |
| `DISC` | Discriminant | b_squared, four_ac, discriminant |
| `ROOT` | Square root | radicand, result |
| `Q1`, `Q2` | Quadratic roots | neg_b, sqrt_disc, two_a, root_value |
| `PROP_SETUP` | Setup proportion | proportion_string |

### Exponents & Radicals
| Code | Description | Arguments |
|------|-------------|-----------|
| `EXP_SETUP` | Setup exponent | base, exponent |
| `EXP_EXPAND` | Expand multiplication | expanded_form |
| `EXP_PARTIAL` | Partial multiplication | value1, value2, result |
| `EXP_RULE_SETUP` | Setup exponent rule | expression |
| `EXP_RULE_IDENTIFY` | Identify rule | rule_name, rule_formula |
| `EXP_RULE_APPLY` | Apply rule | operation, exp1, exp2, result |
| `EXP_RULE_SIMPLIFY` | Simplify result | simplified |
| `SCI_SETUP` | Setup scientific notation | number |
| `SCI_IDENTIFY` | Identify coefficient/exponent | coefficient, exponent |
| `SCI_MOVE_DECIMAL` | Move decimal | direction, places |
| `ROOT_SETUP` | Setup root | expression |
| `ROOT_IDENTIFY` | Identify root type | radicand, type, result |
| `ROOT_EXTRACT` | Extract root | result |

### Geometry
| Code | Description | Arguments |
|------|-------------|-----------|
| `PERIM` | Perimeter result | value |
| `AREA` | Area result | value |
| `VOLUME` | Volume result | value |
| `CIRCLE_SETUP` | Setup circle problem | value, type (radius/diameter) |
| `CIRCLE_FORMULA` | Show formula | formula |
| `CIRCLE_SUBSTITUTE` | Substitute values | substituted_formula |
| `CIRCLE_CALCULATE` | Calculate | calculation, result |
| `VOL_SETUP` | Setup volume | shape, dimensions |
| `VOL_FORMULA` | Volume formula | formula |
| `VOL_BASE_AREA` | Calculate base area | calculation, result |
| `VOL_CALCULATE` | Calculate volume | calculation, result |
| `SA_SETUP` | Setup surface area | shape, dimensions |
| `SA_FORMULA` | Surface area formula | formula |
| `SA_FACES` | Calculate face areas | face_type, calculation, result |
| `SA_BASES` | Calculate base areas | calculation, result |
| `SA_LATERAL` | Calculate lateral area | calculation, result |
| `SA_TOTAL` | Total surface area | calculation, result |

### Pythagorean Theorem
| Code | Description | Arguments |
|------|-------------|-----------|
| `PYTHAG_SETUP` | Setup problem | c=hyp, a=leg, b=? |
| `PYTHAG_FORMULA` | Show formula | formula |
| `PYTHAG_SUBSTITUTE` | Substitute values | substituted_formula |
| `PYTHAG_SQUARE` | Square a value | value, result |
| `PYTHAG_SOLVE` | Solve for unknown | equation, result |
| `PYTHAG_ROOT` | Take square root | radicand, result |
| `PYTHAG_CONTEXT` | Word problem context | context_type, values |
| `PYTHAG_MODEL` | Model the problem | leg1, leg2, unknown |
| `PYTHAG_CALCULATE` | Intermediate calculation | calculation, result |

### Angles
| Code | Description | Arguments |
|------|-------------|-----------|
| `ANGLE_SETUP` | Setup angle problem | relationship, equation |
| `ANGLE_RELATION` | Simplify relationship | simplified_equation |
| `ANGLE_SOLVE` | Solve for variable | equation, solution |
| `PARALLEL_SETUP` | Setup parallel lines | angle_type, relationship |
| `PARALLEL_RELATION` | Show equation | equation |
| `PARALLEL_SOLVE` | Solve | equation, solution |
| `TRI_ANGLE_SETUP` | Setup triangle angles | angle1, angle2, angle3 |
| `TRI_ANGLE_SUM` | Show sum equation | equation |
| `TRI_ANGLE_SOLVE` | Solve for angle | equation, result |

### Scaling & Similarity
| Code | Description | Arguments |
|------|-------------|-----------|
| `SCALE_SETUP` | Setup scale | scale_unit, actual_unit, factor |
| `SCALE_IDENTIFY` | Identify given/find | given_value, find_type |
| `SCALE_MULT` | Multiply by scale | value, factor, result |
| `SCALE_DIV` | Divide by scale | value, factor, result |
| `SIMILAR_SETUP` | Setup similar figures | figure_type, sides_a, sides_b |
| `SIMILAR_SCALE` | Find scale factor | side_a, side_b, factor |
| `SIMILAR_APPLY` | Apply scale factor | known_side, factor, result |
| `UNIT_RATE_SETUP` | Setup unit rate | quantity, unit, total |
| `UNIT_RATE_DIV` | Calculate rate | total, quantity, rate |
| `UNIT_RATE_TABLE` | Show table data | x_values, y_values |
| `UNIT_RATE_PICK` | Pick values from table | x, y |

### Statistics
| Code | Description | Arguments |
|------|-------------|-----------|
| `STAT_SETUP` | Setup dataset | values |
| `STAT_SUM` | Sum values | expression, result |
| `STAT_COUNT` | Count values | n |
| `STAT_DIVIDE` | Divide for mean | expression, result |
| `STAT_ORDER` | Order values | ordered_values |
| `STAT_MIDDLE` | Find middle | position(s), value(s) |
| `STAT_AVERAGE` | Average middle values | calculation, result |
| `STAT_FREQUENCY` | Count frequency | value, count |
| `STAT_MODE` | Identify mode | mode_value(s), frequency |
| `STAT_MIN` | Find minimum | value |
| `STAT_MAX` | Find maximum | value |
| `STAT_RANGE` | Calculate range | calculation, result |
| `STAT_MEAN` | Calculate mean | calculation, result |
| `STAT_DEVIATION` | Calculate deviation | value, mean, deviation |
| `STAT_ABS_DEV` | Absolute deviation | deviation, abs_deviation |
| `STAT_MAD` | Mean absolute deviation | sum, count, result |
| `SORT` | Sort values | unsorted, sorted |
| `MEAN_DIV` | Divide for mean | sum, count, result |
| `MODE_COUNT` | Count for mode | value, count |
| `MODE` | Mode result | max_count, mode_values |
| `MEDIAN_PAIR` | Middle pair for even count | value1, value2 |

### Probability
| Code | Description | Arguments |
|------|-------------|-----------|
| `PROB_SETUP` | Setup probability | description or favorable, total |
| `PROB_IDENTIFY` | Identify probability | event, probability |
| `PROB_INDEPENDENT` | Note independence | explanation |
| `PROB_DEPENDENT` | Note dependence | explanation |
| `PROB_CONDITIONAL` | Conditional probability | event, probability |
| `PROB_MULTIPLY` | Multiply probabilities | prob1, prob2, result |

### Percentages
| Code | Description | Arguments |
|------|-------------|-----------|
| `PERCENT_TO_DEC` | Convert percent to decimal | percent, decimal |
| `SETUP_PERCENT_EQ` | Setup equation | equation |
| `REARRANGE_EQ` | Rearrange equation | rearranged |
| `PERCENT_CALC_PART` | Calculate part | percent_dec, whole, result |
| `DEC_TO_PERCENT` | Convert decimal to percent | decimal, percent |
| `FRAC_TO_DEC` | Convert fraction to decimal | fraction, decimal |
| `DEC_TO_FRAC` | Convert decimal to fraction | decimal, fraction |

### Unit Conversions
| Code | Description | Arguments |
|------|-------------|-----------|
| `CONV_FACTOR` | Conversion factor | from_unit, to_unit |
| `CONV_RESULT` | Conversion result | from_value, to_value |

### Place Value & Rounding
| Code | Description | Arguments |
|------|-------------|-----------|
| `ROUND_CHECK` | Check rounding digit | value, place, comparison |
| `ROUND_RESULT` | Rounding result | original, rounded |
| `ALIGN_NUM` | Align for comparison | num1, num2 |
| `CMP_NUM` | Compare numbers | num1, num2, relation |

### Divisibility
| Code | Description | Arguments |
|------|-------------|-----------|
| `DIV_CHECK` | Check divisibility | n, divisor, remainder |
| `PRIME` | Mark as prime | n |
| `COMPOSITE_FACTOR` | Show factor | factor, cofactor |

### Graph Interpretation
| Code | Description | Arguments |
|------|-------------|-----------|
| `GRAPH_DATA` | Graph type and data | graph_type, data_string |
| `GRAPH_READ` | Read value | category/time, value |
| `GRAPH_MIN` | Minimum value | category, value |
| `GRAPH_MAX` | Maximum value | category, value |
| `GRAPH_CHANGE` | Change between points | from, to, change |
| `GRAPH_MAX_CHANGE` | Largest change | from, to, change |
| `PICTO_KEY` | Pictograph key | symbol, value_per_symbol |
| `PICTO_COUNT` | Count symbols | category, count |

### Abacus
| Code | Description | Arguments |
|------|-------------|-----------|
| `AB_SET` | Set initial number | number |
| `AB_INFO` | Informational text | text |
| `AB_ADD_DGT` | Add digits in column | col_name, calculation, sum |
| `AB_CARRY` | Carry to next column | from_col, carry, to_col |
| `AB_CARRY_FINAL` | Final carry | carry_value |

---

## Curriculum Progress

| Category | Implemented | Remaining |
|----------|-------------|-----------|
| Elementary (3-5) | 34 | 0 |
| Middle School (6-8) | 41 | 0 |
| Algebra 1 | 4 | 48 |
| Geometry | 1 | 28 |
| Algebra 2 | 1 | 40 |
| Precalculus | 0 | 38 |
| AP Statistics | 0 | 26 |
| AP Calculus AB | 0 | 38 |
| AP Calculus BC | 0 | 24 |
| **Total** | **81** | **~243** |

See [TODO.md](TODO.md) for the complete curriculum roadmap.

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
├── generators/               # All generator implementations
│   ├── __init__.py
│   ├── long_division_generator.py
│   ├── fraction_op_generator.py
│   └── ... (51 generator files)
├── tests/                    # Unit tests for all generators
│   ├── __init__.py
│   ├── test_long_division_generator.py
│   └── ... (51 test files)
├── README.md                 # This file
├── AGENTS.md                 # Guidelines for AI coding agents
├── TODO.md                   # Curriculum roadmap
└── pyproject.toml           # Package configuration
```

---

## Contributing

When adding a new generator:

1. Create `generators/my_new_generator.py` extending `ProblemGenerator`
2. Create `tests/test_my_new_generator.py` with unit tests
3. **IMPORTANT**: Add import and instance to `ALL_GENERATORS` in `dolphin_math_datagen.py`
4. Update `TODO.md` to mark the item as complete
5. Run `python dolphin_math_datagen.py --sample --generators MyNewGenerator` to verify output
6. Run `python -m unittest discover tests` to ensure all tests pass
