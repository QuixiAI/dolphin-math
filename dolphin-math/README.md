# Dolphin Math Data Generator
<img width="410" alt="image" src="https://github.com/user-attachments/assets/f8a5d3d2-7820-4f7c-a5d3-fbac667e7084" />

## Purpose

This project, generates synthetic math problems covering various arithmetic and algebra topics. Crucially, it also generates detailed, step-by-step solutions intended to mimic the process a human would follow when solving the problem manually (like a "visible scratchpad").

The output is designed for training language models to perform multi-step mathematical reasoning.

It works for both SFT and RL.  You should generate separate datasets for SFT and RL.  SFT teaches it the syntax, RL teaches it to git gud at it.

## Features

Generates problems and detailed steps for the following types:

*   **Basic Arithmetic:**
    *   Long Division (with remainder)
    *   Multi-digit Addition (standard column with carries)
    *   Multi-digit Subtraction (standard column with borrows)
    *   Multi-digit Multiplication (standard column with partials)
    *   Mixed Number Operations (+, -, *, /)
    *   Comparing Fractions (LCD and compare)
    *   Fraction/Decimal/Percent Conversions
    *   Factors, Prime Factorization, GCF (Euclid), and LCM (via GCD)
    *   Order of Operations (PEMDAS with rewrite steps)
    *   Place Value & Rounding; Comparing/Ordering Numbers
    *   Geometry Basics: Perimeter/Area of rectangles, triangles, parallelograms, trapezoids, general polygons; Volume of rectangular prisms
    *   Unit Conversions (length/weight/time/money), Basic Data/Stats (mean/median/mode), Simple Probability (single event)
    *   Graph Interpretation (bar charts, line graphs, pictographs)
    *   Decimal Multiplication
    *   Decimal Addition
    *   Decimal Subtraction
    *   Decimal Division
    *   Fraction Addition (common and uncommon denominators)
    *   Fraction Subtraction (common and uncommon denominators)
    *   Fraction Multiplication
    *   Fraction Division
*   **Algebra:**
    *   Simple Linear Equations (e.g., `ax + b = c`)
    *   Complex Linear Equations (e.g., `ax + b = cx + d`)
    *   Quadratic Equations (using the quadratic formula)
    *   Simplifying Algebraic Expressions (with distribution)
    *   Evaluating Algebraic Expressions (substituting variable values)
    *   Proportional Relationships
*   **Geometry:**
    *   Pythagorean Theorem (finding hypotenuse)
*   **Percentages:**
    *   Finding the part (e.g., "What is 25% of 80?")
    *   Finding the percent (e.g., "15 is what percent of 50?")
    *   Finding the whole (e.g., "20 is 50% of what number?")
*   **Tools/Methods:**
    *   Abacus-style Addition (column-by-column with carries)

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

## Op-Code Legend

The `steps` field in the output JSON contains a list of strings, each representing a step in the solution. Steps are formatted as `OP_CODE|arg1|arg2|...`.

*   **Arithmetic:**
    *   `D`: Divide (dividend, divisor, quotient_digit)
    *   `M`: Multiply (factor1, factor2, product)
    *   `S`: Subtract (minuend, subtrahend, difference)
    *   `A`: Add (addend1, addend2, sum)
    *   `B`: Bring down (remainder_before, digit_down, new_num_to_divide)
    *   `R`: Remainder (final_remainder)
    *   `C`: Convert fraction for LCD (orig_frac_str, lcd, converted_frac_str)
    *   `L`: LCD calculation (denominator1, denominator2, lcd)
    *   `I`: Invert fraction (orig_frac_str, inverted_frac_str)
    *   `F`: Fraction simplification (unsimplified_frac_str, simplified_frac_str)
*   **Decimal Add/Sub:**
    *   `DEC_ALIGN`: Align numbers by decimal point (num1_aligned, num2_aligned)
    *   `DEC_ADD_COL`: Add column (col_name, details_str, result_str)
    *   `DEC_SUB_COL`: Subtract column (col_name, details_str, result_str)
    *   `DEC_CARRY_FINAL`: Final carry digit from leftmost column (carry_digit)
*   **Integer Column Addition:**
    *   `INT_ALIGN`: Zero-pad numbers for column alignment
    *   `ADD_COL`: Column addition (col_name, details_str, result_str_with_carry)
    *   `CARRY_FINAL`: Final carry digit from leftmost column (carry_digit)
*   **Decimal Multiplication:**
    *   `MUL_SETUP`: Setup integer multiplication (int1_str, int2_str)
    *   `MUL_PARTIAL`: Multiply by digit for partial product (digit, top_int_str, partial_product_shifted_str)
    *   `ADD_PARTIALS`: Sum the partial products (sum_expression_str, result_sum_str)
    *   `COUNT_DP`: Count total decimal places in original factors (dp1, dp2, total_dp)
    *   `PLACE_DP`: Place decimal point in the final integer sum (sum_int_str, total_dp, final_result_str)
*   **Decimal Division:**
    *   `DEC_SHIFT`: Shift decimal points (orig_expr, shifted_expr, shift_places)
    *   `DIV_SETUP`: Setup long division (integer_dividend, integer_divisor)
    *   `PLACE_DP_Q`: Place decimal in quotient (quotient_digits_str, dp_position_from_left_in_shifted_dividend)
    *   *(Reuses B, D, M, S from Arithmetic)*
*   **Integer Column Add/Sub:**
    *   `INT_ALIGN`: Zero-pad numbers for column alignment
    *   `ADD_COL`: Column addition (col_name, details_str, result_str_with_carry)
    *   `CARRY_FINAL`: Final carry digit from leftmost column (carry_digit)
    *   `SUB_COL`: Column subtraction (col_name, details_str, result_str_with_borrow)
    *   `BORROW`: Borrow from the next higher place value (col_name, from_left, 1)
*   **Integer Multiplication:**
    *   `MUL_SETUP`: Setup integer multiplication (top_str, bottom_str)
    *   `MUL_PARTIAL`: Multiply by digit for partial product (digit, top_int_str, partial_product_shifted_str)
    *   `ADD_PARTIALS`: Sum the partial products (sum_expression_str, result_sum_str)
*   **Mixed Numbers:**
    *   `MIX_IMPROPER`: Convert mixed number to improper fraction (mixed_str, improper_str)
    *   `L`: LCD calculation
    *   `C`: Convert to common denominator (orig_frac_str, lcd, converted_frac_str)
    *   `I`: Invert fraction (for division)
    *   `A`/`S`/`M`: Numerator operations (add, subtract, multiply) shown with fraction context
    *   `F`: Simplify fraction (always emitted)
    *   `IMPROPER_TO_MIX`: Convert improper fraction to mixed form when |num| >= den
*   **Fraction Comparison:**
    *   `CMP`: Compare two converted fractions (`lhs_frac`, `rhs_frac`, relation)
*   **Conversions:**
    *   `FRAC_TO_DEC`: Convert fraction to decimal
    *   `DEC_TO_FRAC`: Convert decimal to fraction
    *   `DEC_TO_PERCENT`: Convert decimal to percent (two decimals)
*   **Factors & Multiples:**
    *   `FACT_CHECK`: Check divisibility (n, divisor, remainder)
    *   `FACT_PAIR`: Record a factor pair
    *   `PF_STEP`: Prime-factor division step (n, divisor, quotient)
    *   `PF_PRIME`: Mark number as prime (no further division)
    *   `GCD_START`: Start Euclid with (a, b)
    *   `GCD_STEP`: Euclid step (a, b, remainder)
    *   `GCD_RESULT`: Final gcd
    *   `LCM_FROM_GCD`: Compute LCM from product and gcd
*   **Order of Operations:**
    *   `REWRITE`: Show the expression after applying the highest-precedence operation completed
*   **Geometry (Perimeter/Area):**
    *   `PERIM`: Perimeter value for the shape
    *   `AREA`: Area value for the shape
    *   `VOLUME`: Volume value for rectangular prisms
*   **Place Value & Rounding:**
    *   `ROUND_CHECK`: Inspect rounding digit and neighbor
    *   `ROUND_RESULT`: Show original and rounded value
    *   `ALIGN_NUM`/`CMP_NUM`: Align and compare whole/decimal numbers
*   **Divisibility/Classification:**
    *   `DIV_CHECK`: Divisibility check (n, divisor, remainder)
    *   `PRIME`: Mark prime
    *   `COMPOSITE_FACTOR`: Show a found factor pair
*   **Unit Conversions:**
    *   `CONV_FACTOR`: Conversion factor from one unit to another
    *   `CONV_RESULT`: Final converted value
*   **Data & Statistics:**
    *   `SORT`: Sorted dataset
    *   `MEAN_DIV`: Divide sum by count
    *   `MEDIAN_PICK`/`MEDIAN_PAIR`: Median selection
    *   `MODE_COUNT`/`MODE`: Frequency counting and mode result
*   **Probability:**
    *   `PROB_SETUP`: State favorable/total outcomes
*   **Percentages:**
    *   `PERCENT_TO_DEC`: Convert percent to decimal (percent_str, decimal_val)
    *   `SETUP_PERCENT_EQ`: Show the equation setup (equation_str)
    *   `REARRANGE_EQ`: Show rearranged equation (rearranged_equation_str)
    *   `PERCENT_CALC_PART`: Calculate the part (percent_dec, whole, part_result) - *Only for find_part*
    *   `DEC_TO_PERCENT`: Convert decimal result back to percent (decimal_val, percent_str) - *Only for find_percent*
    *   *(Uses division steps internally for find_percent/find_whole)*
*   **Algebra:**
    *   `DISC`: Discriminant calculation (b_squared, four_ac, discriminant)
    *   `ROOT`: Square root calculation (number, root)
    *   `Q1`/`Q2`: Quadratic formula roots (neg_b, sqrt_disc, two_a, root_value)
    *   `DIST`: Distribute term (factor, expr_in_parens, result_expr)
    *   `REWRITE`: Rewrite expression/equation after step (new_form_string)
    *   `COMB_X`: Combine X terms (term1, term2, result_term)
    *   `COMB_CONST`: Combine Constant terms (const1, const2, result_const)
    *   `SUBST`: Substitute value (var_name, value, resulting_expr)
    *   `MOVE_TERM`: Move term across equals sign (term_moved, target_side, resulting_equation_str)
    *   `DIV_COEFF`: Divide by coefficient (numerator, denominator, result_str)
*   **Geometry:**
    *   `E`: Exponent/Power (base, exponent, result)
    *   *(Reuses ROOT)*
*   **Algebra+:**
    *   `PROP_SETUP`: Setup proportion (proportion_str)
*   **Tools/Methods (Abacus):**
    *   `AB_SET`: Set initial number (number)
    *   `AB_INFO`: Informational text (text)
    *   `AB_ADD_DGT`: Add digits in a column (col_name, details_str, column_sum)
    *   `AB_CARRY`: Show carry propagation (from_col, carry_value, to_col)
    *   `AB_CARRY_FINAL`: Final carry from leftmost column (carry_value)
*   **Graph Interpretation (Bar/Line/Pictograph):**
    *   `GRAPH_DATA`: Record graph type and data (graph_type, data_str)
    *   `GRAPH_READ`: Read value from graph (category/time, value)
    *   `GRAPH_MIN`/`GRAPH_MAX`: Identify minimum/maximum (category, value)
    *   `GRAPH_CHANGE`: Track change between points (from, to, change_value)
    *   `GRAPH_MAX_CHANGE`: Identify largest change (from, to, change_value)
    *   `PICTO_KEY`: Pictograph symbol key (symbol, value_per_symbol)
    *   `PICTO_COUNT`: Count symbols for category (category, count)
*   **Final Answer:**
    *   `Z`: Contains the final formatted answer string (final_answer_str)

## Dependencies

*   Python 3 (tested with 3.9+)
