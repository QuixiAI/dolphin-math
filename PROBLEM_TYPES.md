# Problem Types

Every problem type this dataset can generate. For each type: a one-line description, the grade band and coarse difficulty (1–5, read relative to the band), the internal operation variants, and one real worked example (the pipe-delimited `steps` are the model's scratchpad).

**448 problem types.** This file is generated — do not hand-edit. Regenerate with `uv run python tools/gen_problem_types.py`.

## Elementary (grades 3–5)

### Long Division — `LongDivisionGenerator`  ·  elementary · difficulty 3

Generates long division problems (e.g., 1234 / 56).

**Variants:** `long_division`, `long_division_estimated`

```
Problem: 6321 / 99
Steps:
  D|632|99|6
  M|6|99|594
  S|632|594|38
  B|38|1|381
  D|381|99|3
  M|3|99|297
  S|381|297|84
  Z|63 R84
Answer: 63 R84
```

### Multi Digit Addition — `MultiDigitAdditionGenerator`  ·  elementary · difficulty 2

Generates standard column-form multi-digit addition with carries.

**Variants:** `multi_digit_addition`

```
Problem: 50504 + 99356
Steps:
  INT_ALIGN|50504|99356
  ADD_COL|col_1|4+6+0|->0 (carry 1)
  ADD_COL|col_2|0+5+1|->6 (carry 0)
  ADD_COL|col_3|5+3+0|->8 (carry 0)
  ADD_COL|col_4|0+9+0|->9 (carry 0)
  ADD_COL|col_5|5+9+0|->4 (carry 1)
  CARRY_FINAL|1
  Z|149860
Answer: 149860
```

### Multi Digit Subtraction — `MultiDigitSubtractionGenerator`  ·  elementary · difficulty 2

Generates standard column-form multi-digit subtraction with borrowing.

**Variants:** `multi_digit_subtraction`

```
Problem: 50504 - 49683
Steps:
  INT_ALIGN|50504|49683
  SUB_COL|col_1|4-3-borrow0|->1 (borrow_out 0)
  BORROW|col_2|from_left|1
  SUB_COL|col_2|0-8-borrow0|->2 (borrow_out 1)
  BORROW|col_3|from_left|1
  SUB_COL|col_3|5-6-borrow1|->8 (borrow_out 1)
  BORROW|col_4|from_left|1
  SUB_COL|col_4|0-9-borrow1|->0 (borrow_out 1)
  SUB_COL|col_5|5-4-borrow1|->0 (borrow_out 0)
  Z|821
Answer: 821
```

### Multi Digit Multiplication — `MultiDigitMultiplicationGenerator`  ·  elementary · difficulty 3

Generates standard column-form multi-digit integer multiplication.

**Variants:** `multi_digit_multiplication`, `multi_digit_multiplication_estimated`

```
Problem: 99356 * 50504
Steps:
  MUL_SETUP|99356|50504
  MUL_PARTIAL|4|99356|397424
  MUL_PARTIAL|0|99356|0
  MUL_PARTIAL|5|99356|49678000
  MUL_PARTIAL|0|99356|0
  MUL_PARTIAL|5|99356|4967800000
  ADD_PARTIALS|397424 + 0 + 49678000 + 0 + 4967800000|5017875424
  Z|5017875424
Answer: 5017875424
```

### Abacus Addition — `AbacusAdditionGenerator`  ·  elementary · difficulty 2

Generates addition problems solved using abacus-like steps.

**Variants:** `abacus_addition`

```
Problem: 6321 + 6900
Steps:
  AB_SET|6321
  AB_INFO|Adding 6900 column by column
  AB_ADD_DGT|col_0|1+0+0|1
  AB_ADD_DGT|col_1|2+0+0|2
  AB_ADD_DGT|col_2|3+9+0|12
  AB_CARRY|col_2|1|col_3
  AB_ADD_DGT|col_3|6+6+1|13
  AB_CARRY|col_3|1|col_4
  AB_CARRY_FINAL|1
  Z|13221
Answer: 13221
```

### Decimal Add Sub — `DecimalAddSubGenerator`  ·  elementary · difficulty 3

Generates decimal addition or subtraction problems with detailed, column-by-column steps including carrying/borrowing.

**Variants:** `decimal_add`, `decimal_sub`

```
Problem: 84.37 + 4.14
Steps:
  DEC_ALIGN|84.37|04.14
  DEC_ADD_COL|frac_0|7+4+0|->1 (carry 1)
  DEC_ADD_COL|frac_1|3+1+1|->5 (carry 0)
  DEC_ADD_COL|int_1|4+4+0|->8 (carry 0)
  DEC_ADD_COL|int_2|8+0+0|->8 (carry 0)
  Z|88.51
Answer: 88.51
```

### Decimal Mult — `DecimalMultGenerator`  ·  elementary · difficulty 3

Generates decimal multiplication problems with detailed, long-multiplication steps.

**Variants:** `decimal_mul`

```
Problem: 84.37 * 4.14
Steps:
  MUL_SETUP|8437|414
  MUL_PARTIAL|4|8437|33748
  MUL_PARTIAL|1|8437|84370
  MUL_PARTIAL|4|8437|3374800
  ADD_PARTIALS|33748+84370+3374800|3492918
  COUNT_DP|2|2|4
  PLACE_DP|3492918|4|349.2918
  Z|349.2918
Answer: 349.2918
```

### Decimal Div — `DecimalDivGenerator`  ·  elementary · difficulty 3

Generates decimal division problems with detailed, long-division steps after shifting decimals.

**Variants:** `decimal_div`

```
Problem: 84.37 / 0.5
Steps:
  DEC_SHIFT|84.37/0.5|843.7/05|1
  DIV_SETUP|8437|5
  D|8|5|1
  M|1|5|5
  S|8|5|3
  B|3|4|34
  D|34|5|6
  M|6|5|30
  S|34|30|4
  B|4|3|43
  D|43|5|8
  M|8|5|40
  S|43|40|3
  B|3|7|37
  D|37|5|7
  M|7|5|35
  S|37|35|2
  B|2|0|20
  D|20|5|4
  M|4|5|20
  S|20|20|0
  PLACE_DP_Q|16874|3
  Z|168.74
Answer: 168.74
```

### Fraction Op — `FractionOpGenerator`  ·  elementary · difficulty 3

Generates fraction arithmetic problems (+, -, *, /).

**Variants:** `fraction_add`, `fraction_div`, `fraction_mul`, `fraction_sub`

```
Problem: 7/8 + 1/6
Steps:
  L|8|6|24
  C|7/8|24|21/24
  C|1/6|24|4/24
  A|21|4|25
  Z|25/24
Answer: 25/24
```

### Fraction Comparison — `FractionComparisonGenerator`  ·  elementary · difficulty 3

Compares two fractions using common denominator (human LCD method).

**Variants:** `fraction_compare`

```
Problem: Compare: 7/8 ? 1/6
Steps:
  L|8|6|24
  C|7/8|24|21/24
  C|1/6|24|4/24
  CMP|21/24|4/24|>
  Z|7/8 > 1/6
Answer: 7/8 > 1/6
```

### Mixed Number Operations Random — `MixedNumberOperationsRandom`  ·  elementary · difficulty 3

Wrapper generator that randomly picks +, -, *, / mixed-number operation. Useful for sampling/dataset inclusion without listing each op separately.

**Variants:** `mixed_number_add`, `mixed_number_div`, `mixed_number_mult`, `mixed_number_sub`

```
Problem: 3 1/2 / 4 7/9
Steps:
  MIX_IMPROPER|3 1/2|7/2
  MIX_IMPROPER|4 7/9|43/9
  I|43/9|9/43
  M|7/2|9/43|63/86
  F|63/86|63/86
  Z|63/86
Answer: 63/86
```

### Mixed Number Operation — `MixedNumberOperationGenerator`  ·  elementary · difficulty 3

Generates mixed number operations (+, -, *, /) with step-by-step conversions.

**Variants:** `mixed_number_add`, `mixed_number_div`, `mixed_number_mult`, `mixed_number_sub`

```
Problem: 3 1/8 + 2 8/10
Steps:
  MIX_IMPROPER|3 1/8|25/8
  MIX_IMPROPER|2 8/10|28/10
  L|8|10|40
  C|25/8|40|125/40
  C|28/10|40|112/40
  A|125|112|237
  F|237/40|237/40
  IMPROPER_TO_MIX|237/40|5 37/40
  Z|5 37/40
Answer: 5 37/40
```

### Fraction Decimal Percent Converter — `FractionDecimalPercentConverter`  ·  elementary · difficulty 3

Converts between fraction, decimal, and percent with clear human steps.

**Variants:** `convert_dec_to_frac`, `convert_frac_to_dec`, `convert_frac_to_percent`, `convert_percent_to_dec`, `convert_percent_to_frac`

```
Problem: Convert 75% to decimal
Steps:
  PERCENT_TO_DEC|75%|0.75
  Z|0.75
Answer: 0.75
```

### Factors — `FactorsGenerator`  ·  elementary · difficulty 1

Lists all factors of a number using trial division up to sqrt(n).

**Variants:** `factors_list`

```
Problem: List factors of 110
Steps:
  FACT_CHECK|110|1|0
  FACT_PAIR|1|110
  FACT_CHECK|110|2|0
  FACT_PAIR|2|55
  FACT_CHECK|110|3|2
  FACT_CHECK|110|4|2
  FACT_CHECK|110|5|0
  FACT_PAIR|5|22
  FACT_CHECK|110|6|2
  FACT_CHECK|110|7|5
  FACT_CHECK|110|8|6
  FACT_CHECK|110|9|2
  FACT_CHECK|110|10|0
  FACT_PAIR|10|11
  Z|1, 2, 5, 10, 11, 22, 55, 110
Answer: 1, 2, 5, 10, 11, 22, 55, 110
```

### Prime Factorization — `PrimeFactorizationGenerator`  ·  elementary · difficulty 2

Generates prime factorization using repeated division (factor tree style).

**Variants:** `prime_factorization`

```
Problem: Prime factorize 122
Steps:
  PF_STEP|122|2|61
  PF_PRIME|61
  Z|2 × 61
Answer: 2 × 61
```

### GCF — `GCFGenerator`  ·  elementary · difficulty 2

Computes greatest common factor using Euclidean algorithm.

**Variants:** `gcf`

```
Problem: Find GCF of 118 and 119
Steps:
  GCD_START|118|119
  GCD_STEP|118|119|118
  GCD_STEP|119|118|1
  GCD_STEP|118|1|0
  Z|1
Answer: 1
```

### LCM — `LCMGenerator`  ·  elementary · difficulty 2

Computes least common multiple using Euclidean algorithm + formula.

**Variants:** `lcm`

```
Problem: Find LCM of 108 and 117
Steps:
  GCD_START|108|117
  GCD_STEP|108|117|108
  GCD_STEP|117|108|9
  GCD_STEP|108|9|0
  GCD_RESULT|9
  LCM_FROM_GCD|108*117|9|1404
  Z|1404
Answer: 1404
```

### Order Of Operations — `OrderOfOperationsGenerator`  ·  elementary · difficulty 3

Evaluates PEMDAS expressions with human-like steps.

**Variants:** `order_of_operations`, `order_of_operations_decimals`, `order_of_operations_mixed_numbers`

```
Problem: Compute 7 + 30 / (1 + 5)
Steps:
  A|1|5|6
  REWRITE|7 + 30 / 6
  D|30|6|5
  REWRITE|7 + 5
  A|7|5|12
  Z|12
Answer: 12
```

### Place Value Rounding — `PlaceValueRoundingGenerator`  ·  elementary · difficulty 1

Rounds whole numbers or decimals to a specified place with digit inspection steps.

**Variants:** `round_to_10`, `round_to_100`, `round_to_1000`, `round_to_hundredth`, `round_to_tenth`

```
Problem: Round 98.6 to the nearest hundredth
Steps:
  ROUND_CHECK|0|0|<5
  ROUND_RESULT|98.60|98.60
  Z|98.60
Answer: 98.60
```

### Number Comparison — `NumberComparisonGenerator`  ·  elementary · difficulty 1

Compares whole numbers or decimals by place value.

**Variants:** `number_compare`

```
Problem: Compare: 757.9 ? 420.59
Steps:
  ALIGN_NUM|757.9|420.59
  CMP_NUM|757.9|420.59|>
  Z|757.9 > 420.59
Answer: 757.9 > 420.59
```

### Divisibility Classification — `DivisibilityClassificationGenerator`  ·  elementary · difficulty 2

Checks divisibility by small primes and classifies as prime/composite.

**Variants:** `divisibility_classify`

```
Problem: Classify 108 as prime or composite
Steps:
  DIV_CHECK|108|2|0
  DIV_CHECK|108|3|0
  DIV_CHECK|108|5|3
  DIV_CHECK|108|7|3
  DIV_CHECK|108|11|9
  DIV_CHECK|108|13|4
  COMPOSITE_FACTOR|2|54
  Z|composite
Answer: composite
```

### Geometry Area Perimeter — `GeometryAreaPerimeterGenerator`  ·  elementary · difficulty 3

Computes perimeter and area for basic shapes with human-style steps.

**Variants:** `geometry_parallelogram`, `geometry_rectangle`, `geometry_trapezoid`, `geometry_triangle`

```
Problem: Trapezoid bases 10, 4, legs 10, height 7: find perimeter and area
Steps:
  A|10|4|14
  M|2|10|20
  A|14|20|34
  PERIM|34
  A|10|4|14
  D|14|2|7.0
  M|7.0|7|49.0
  AREA|49.0
  Z|Perimeter=34, Area=49.0
Answer: Perimeter=34, Area=49.0
```

### Polygon Perimeter — `PolygonPerimeterGenerator`  ·  elementary · difficulty 2

Computes perimeter of an n-sided polygon by summing side lengths.

**Variants:** `polygon_perimeter`

```
Problem: Find perimeter of polygon with sides: 14, 8, 2, 6, 10, 9
Steps:
  A|14|8|22
  A|22|2|24
  A|24|6|30
  A|30|10|40
  A|40|9|49
  PERIM|49
  Z|49
Answer: 49
```

### Volume Rect Prism — `VolumeRectPrismGenerator`  ·  elementary · difficulty 3

Computes volume of a rectangular prism with explicit multiplication steps.

**Variants:** `volume_rect_prism`

```
Problem: Find volume of rectangular prism: L=15, W=8, H=14
Steps:
  M|15|8|120
  M|120|14|1680
  VOLUME|1680
  Z|1680
Answer: 1680
```

### Unit Conversion — `UnitConversionGenerator`  ·  elementary · difficulty 2

Performs one-step unit conversions with factor-label style steps.

**Variants:** `convert_dollar_to_cent`, `convert_ft_to_in`, `convert_hr_to_min`, `convert_kg_to_g`, `convert_km_to_m`, `convert_lb_to_oz`, `convert_m_to_cm`, `convert_min_to_sec`

```
Problem: Convert 3 dollar to cent
Steps:
  CONV_FACTOR|1 dollar|100 cent
  M|3|100|300
  CONV_RESULT|3 dollar|300 cent
  Z|300 cent
Answer: 300 cent
```

### Multi Step Unit Conversion — `MultiStepUnitConversionGenerator`  ·  elementary · difficulty 3

Performs multi-step conversions for area (square units) and volume (cubic units) using repeated factor-label multiplication.

**Variants:** `convert_area`, `convert_volume`

```
Problem: Convert 2 km^3 to m^3
Steps:
  CONV_FACTOR|1 km|1000 m
  M|2|1000|2000
  CONV_FACTOR|1 km|1000 m
  M|2000|1000|2000000
  CONV_FACTOR|1 km|1000 m
  M|2000000|1000|2000000000
  CONV_RESULT|2 km^3|2000000000 m^3
  Z|2000000000 m^3
Answer: 2000000000 m^3
```

### Rate Conversion — `RateConversionGenerator`  ·  elementary · difficulty 3

Converts rates like mph -> ft/s (and reverse) using factor-label steps with explicit numerator/denominator conversions.

**Variants:** `convert_rate`

```
Problem: Convert 20 m/s to km/hr
Steps:
  CONV_FACTOR|1 s|3600 hr
  M|20|3600|72000
  CONV_FACTOR|1 m|1000 km
  D|72000|1000|72
  CONV_RESULT|20 m/s|72 km/hr
  Z|72 km/hr
Answer: 72 km/hr
```

### Temperature Conversion — `TemperatureConversionGenerator`  ·  elementary · difficulty 3

Converts between Fahrenheit, Celsius, and Kelvin using explicit add/subtract and multiply/divide steps.

**Variants:** `convert_temperature`

```
Problem: Convert 154 K to C
Steps:
  S|154|273.15|-119.14999999999998
  CONV_RESULT|154 K|-119.15 C
  Z|-119.15 C
Answer: -119.15 C
```

### Dimensional Analysis — `DimensionalAnalysisGenerator`  ·  elementary · difficulty 3

Performs multi-factor dimensional analysis across dosing (mg/kg), flow rates, pressure, and rate conversions with explicit factor-label multiplications/divisions.

**Variants:** `dimensional_analysis`

```
Problem: Pressure conversion: Convert 12 kPa to atm
Steps:
  CONV_FACTOR|101.325 kPa|1 atm
  M|12|1.0|12.0
  D|12.0|101.325|0.11843079200592153
  CONV_RESULT|12 kPa|0.1184 atm
  Z|0.1184 atm
Answer: 0.1184 atm
```

### Percent Word Problem — `PercentWordProblemGenerator`  ·  elementary · difficulty 3

Percent increase/decrease, markup, discount, and tax word problems with explicit arithmetic. Supports multiple phrasings per scenario (A4) and an optional distractor quantity the scratchpad must first filter out (A6).

**Variants:** `percent_word_problem`, `percent_word_problem_distractor`

```
Problem: An item priced at $86 is 5% off. What is the sale price?
Steps:
  PERCENT_TO_DEC|5%|0.05
  M|86|0.05|4.3
  S|86|4.3|81.7
  Z|81.7
Answer: 81.7
```

### Repeating Decimal — `RepeatingDecimalGenerator`  ·  elementary · difficulty 3

Determines whether a fraction converts to a terminating or repeating decimal and shows the decimal expansion.

**Variants:** `repeating_decimal`

```
Problem: Determine if 7/9 is terminating or repeating, and give the decimal.
Steps:
  F|7/9|7/9
  PF_PRIME|9
  DEC_TYPE|7/9|repeating
  DEC_VALUE|7/9|0.777778
  Z|0.777778 (repeating)
Answer: 0.777778 (repeating)
```

### Proportion Word Problem — `ProportionWordProblemGenerator`  ·  elementary · difficulty 3

Proportion word problems (rates like mi/hr, $/lb, cups/serving) solved by cross-multiplication. Supports several phrasings per scenario (A4) and an optional distractor quantity the scratchpad must first filter out (A6). Rates are integers by construction, so every answer is exact.

**Variants:** `proportion_word_problem`, `proportion_word_problem_distractor`

```
Problem: A ratio table pairs input 3 with output 3. What output goes with input 10?
Steps:
  PROP_SETUP|3/3 = x/10
  M|3|10|30
  EQ_SETUP|x = 30/3
  D|30|3|10
  Z|10
Answer: 10
```

### Simple Stats — `SimpleStatsGenerator`  ·  elementary · difficulty 2

Computes mean, median, and mode for small integer datasets.

**Variants:** `mean`, `median`, `mode`

```
Problem: Find median of [2, 9, 10, 13, 14, 16, 16, 17]
Steps:
  SORT|14,2,9,17,16,13,10,16|2,9,10,13,14,16,16,17
  MEDIAN_PAIR|13|14
  MEAN_DIV|27|2|13.5
  Z|13.5
Answer: 13.5
```

### Simple Probability — `SimpleProbabilityGenerator`  ·  elementary · difficulty 1

Single-event probability with uniform outcomes.

**Variants:** `probability_simple`

```
Problem: If an event has 7 favorable outcomes out of 9 equally likely outcomes, what is P?
Steps:
  PROB_SETUP|7|9
  D|7|9|0.78
  F|7/9|0.78
  Z|0.78
Answer: 0.78
```

### Graph Interpret — `GraphInterpretGenerator`  ·  elementary · difficulty 1

Generates problems for reading and interpreting bar charts, line graphs, and pictographs. Problems include finding values, comparing categories, calculating totals, differences, and identifying min/max.

**Variants:** `bar_chart_compare`, `bar_chart_difference`, `bar_chart_max`, `bar_chart_min`, `bar_chart_read`, `bar_chart_total`, `line_graph_decrease`, `line_graph_increase`, `line_graph_max`, `line_graph_min`, `line_graph_range`, `line_graph_read`, `pictograph_compare`, `pictograph_difference`, `pictograph_max`, `pictograph_read`, `pictograph_total`

```
Problem: Line Graph Data:
  2018: 18
  2019: 21
  2020: 23
  2021: 24
  2022: 31

Question: Between which two consecutive time periods was there the largest decrease?
Steps:
  GRAPH_DATA|line_graph|2018:18,2019:21,2020:23,2021:24,2022:31
  GRAPH_READ|2018|18
  GRAPH_READ|2019|21
  S|18|21|-3
  GRAPH_CHANGE|2018|2019|3
  GRAPH_READ|2019|21
  GRAPH_READ|2020|23
  S|21|23|-2
  GRAPH_CHANGE|2019|2020|2
  GRAPH_READ|2020|23
  GRAPH_READ|2021|24
  S|23|24|-1
  GRAPH_CHANGE|2020|2021|1
  GRAPH_READ|2021|24
  GRAPH_READ|2022|31
  S|24|31|-7
  GRAPH_CHANGE|2021|2022|7
  Z|No decrease occurred
Answer: No decrease occurred
```

### Composite Arithmetic — `CompositeArithmeticGenerator`  ·  elementary · difficulty 4

One scratchpad that chains 2-3 elementary skills, the way a real word problem forces several tools in sequence (A5). Each variant opens with a COMPOSITE_SETUP naming the plan, then works each sub-skill with its own established op-codes.

**Variants:** `composite_arithmetic_area_mixed`, `composite_arithmetic_mean_long_division`, `composite_arithmetic_percent_of_total`

```
Problem: A rectangle measures 4 1/2 feet by 5 4/5 feet. Find its area.
Steps:
  COMPOSITE_SETUP|area = length × width with mixed numbers|convert, multiply, simplify
  MIX_IMPROPER|4 1/2|9/2
  MIX_IMPROPER|5 4/5|29/5
  M|9/2|29/5|261/10
  IMPROPER_TO_MIX|261/10|26 1/10
  EVAL|area|26 1/10 square feet
  Z|26 1/10 square feet
Answer: 26 1/10 square feet
```

## Middle School (grades 6–8)

### Integer Operations — `IntegerOperationsGenerator`  ·  middle · difficulty 3

Generates integer operation problems involving positive and negative numbers. Covers addition, subtraction, multiplication, and division with explicit sign rule steps.

**Variants:** `integer_addition`, `integer_division`, `integer_multiplication`, `integer_subtraction`

```
Problem: Calculate: (8) ÷ (8)
Steps:
  INT_SIGN_RULE|div_same_signs|Same signs: positive ÷ positive = positive, or negative ÷ negative = positive
  INT_ABS|8|8
  INT_ABS|8|8
  INT_OP|÷|8|8|1
  INT_APPLY_SIGN|1|positive|1
  Z|1
Answer: 1
```

### Unit Rate — `UnitRateGenerator`  ·  middle · difficulty 3

Generates unit rate calculation problems.

**Variants:** `unit_rate`

```
Problem: If 8 shirts cost $40.00, what is the cost of 1 shirt?
Steps:
  UNIT_RATE_SETUP|8|shirts|$40.00
  UNIT_RATE_DIV|$40.00|8|$5.00
  Z|$5.00
Answer: $5.00
```

### Unit Rate From Table — `UnitRateFromTableGenerator`  ·  middle · difficulty 3

Generates unit rate problems where students find rate from a table of values.

**Variants:** `unit_rate_table`

```
Problem: Find the unit rate (total cost in dollars per pound) from the table:
| pounds of fruit | total cost in dollars |
|-----------------|-----------------------|
| 1 | 10 |
| 4 | 40 |
| 5 | 50 |
| 8 | 80 |

Steps:
  UNIT_RATE_TABLE|1,4,5,8|10,40,50,80
  UNIT_RATE_PICK|1|10
  UNIT_RATE_DIV|10|1|10
  Z|10
Answer: 10
```

### Ratio Table — `RatioTableGenerator`  ·  middle · difficulty 3

Generates ratio-table problems: a table of equivalent ratios with one missing entry. The scratchpad follows the pencil-and-paper procedure: read the table, reduce a complete column to the simplest ratio, find the scale factor for the incomplete column, multiply to fill the blank, and verify by cross-multiplication.

**Variants:** `ratio_table`

```
Problem: A car travels at a constant speed. The table shows equivalent ratios. Find the missing value.
Distance (miles): 50, ?, 70, 80
Time (hours): 45, 54, 63, 72
Steps:
  RATIO_TABLE|Distance (miles): 50, ?, 70, 80|Time (hours): 45, 54, 63, 72
  RATIO_BASE|50:45|5|10:9
  D|54|9|6
  M|10|6|60
  CHECK|cross_products|50×54=2700|45×60=2700
  Z|60
Answer: 60
```

### Tip Bill Split — `TipBillSplitGenerator`  ·  middle · difficulty 3

Generates tip and bill-splitting problems (consumer percent math).

**Variants:** `find_tip_percent`, `tip_split`, `tip_total`

```
Problem: The dinner bill at Casa Verde comes to $28.00 for 6 friends. They add a 20% tip and split the total evenly. How much does each person pay?
Steps:
  PERCENT_TO_DEC|20%|0.20
  M|28.00|0.20|5.60
  A|28.00|5.60|33.60
  D|33.60|6|5.60
  CHECK|split|5.60×6=33.60|28.00+5.60=33.60
  Z|$5.60
Answer: $5.60
```

### Scaling — `ScalingGenerator`  ·  middle · difficulty 3

Generates scale factor problems.

**Variants:** `scale_find_actual`, `scale_find_scaled`

```
Problem: A blueprint has a scale of 1 centimeter = 5 meters. If a wall is actually 25 meters long, how long is it on the blueprint?
Steps:
  SCALE_SETUP|1 centimeter|5 meters|5
  SCALE_IDENTIFY|25 meters|scaled_dimension
  SCALE_DIV|25|5|5.0
  Z|5 centimeters
Answer: 5 centimeters
```

### Similar Figures Scale — `SimilarFiguresScaleGenerator`  ·  middle · difficulty 3

Generates scale factor problems involving similar figures.

**Variants:** `similar_missing_side`, `similar_scale_factor`

```
Problem: Parallelograms ABCD and EFGH are similar with sides 9 and 3 units in ABCD. If the 9-unit side corresponds to 22.5 units in EFGH, what is the length of the side corresponding to 3 units?
Steps:
  SIMILAR_SETUP|parallelogram|9,3|22.5 (others unknown)
  SIMILAR_SCALE|22.5|9|2.5
  SIMILAR_APPLY|3|2.5|7.5
  Z|7.5
Answer: 7.5
```

### Proportional Relationship — `ProportionalRelationshipGenerator`  ·  middle · difficulty 3

Generates proportional relationship problems (a/b = c/x or a/b = x/c).

**Variants:** `proportional_relationship`

```
Problem: If 7 is to 7, what is proportional to 14?
Steps:
  PROP_SETUP|7/7 = x/14
  M|7x|7*14=98
  D|98|7|14
  Z|14
Answer: 14
```

### One Step Equation — `OneStepEquationGenerator`  ·  middle · difficulty 3

Generates one-step linear equations.

**Variants:** `one_step_equation_add`, `one_step_equation_div`, `one_step_equation_mult`, `one_step_equation_sub`

```
Problem: Solve for x: x/8 = -9
Steps:
  EQ_SETUP|x/8 = -9
  EQ_OP_BOTH|multiply|8|x|-72
  EQ_RESULT|x|-72
  Z|-72
Answer: -72
```

### Two Step Equation — `TwoStepEquationGenerator`  ·  middle · difficulty 4

Generates two-step linear equations.

**Variants:** `two_step_equation`

```
Problem: Solve for x: x/8 + 7 = 0
Steps:
  EQ_SETUP|x/8 + 7 = 0
  EQ_OP_BOTH|subtract|7|x/8|-7
  EQ_SIMPLIFY|x/8 = -7
  EQ_OP_BOTH|multiply|8|x|-56
  EQ_RESULT|x|-56
  CHECK|substitute|(-56)/8 + 7 = 0|0
  Z|-56
Answer: -56
```

### Linear Simple — `LinearSimpleGenerator`  ·  middle · difficulty 4

Generates simple linear equation problems (e.g., mx + b = y).

**Variants:** `linear_eq_simple`

```
Problem: Solve 4x-9 = 3
Steps:
  S|3|-9|12
  D|12|4|x=3
  Z|x=3
Answer: x=3
```

### Linear Complex — `LinearComplexGenerator`  ·  middle · difficulty 4

Generates linear equations with variables on both sides (ax + b = cx + d).

**Variants:** `linear_eq_complex`

```
Problem: Solve: -5x+7 = -x+6
Steps:
  MOVE_TERM|-1x|left|-5x+7+x = +6
  COMB_X|-5x|+x|-4x
  REWRITE|-4x+7 = +6
  MOVE_TERM|+7|right|-4x = +6-7
  COMB_CONST|6|-7|-1
  REWRITE|-4x = -1
  DIV_COEFF|-1|-4|x=1/4
  Z|x=1/4
Answer: x=1/4
```

### Simplify Expression — `SimplifyExpressionGenerator`  ·  middle · difficulty 4

Generates algebraic expression simplification problems.

**Variants:** `simplify_expression`

```
Problem: Simplify: 3(2x-5)-x+4
Steps:
  DIST|3|2x-5|6x-15
  REWRITE|6x-15-x+4
  COMB_X|6x|-1x|5x
  COMB_CONST|-15|+4|-11
  Z|5x-11
Answer: 5x-11
```

### Evaluate Expression — `EvaluateExpressionGenerator`  ·  middle · difficulty 4

Generates algebraic expression evaluation problems.

**Variants:** `evaluate_expression`

```
Problem: Evaluate 2x+2y-8 for x=-1, y=3
Steps:
  SUBST|x|-1|2(-1)+2y-8
  M|2|-1|-2
  SUBST|y|3|2(-1)+2(3)-8
  M|2|3|6
  REWRITE|-2+6-8
  A|-2|6|4
  A|4|-8|-4
  Z|-4
Answer: -4
```

### One Step Inequality — `OneStepInequalityGenerator`  ·  middle · difficulty 3

Generates one-step linear inequalities.

**Variants:** `one_step_inequality`

```
Problem: Solve the inequality: x/-6 ≥ 8
Steps:
  INEQ_SETUP|x/-6 ≥ 8
  INEQ_OP_BOTH|multiply|-6|x|-48
  INEQ_FLIP|Multiplying by negative number reverses inequality
  INEQ_RESULT|x|≤|-48
  Z|x ≤ -48
Answer: x ≤ -48
```

### Two Step Inequality — `TwoStepInequalityGenerator`  ·  middle · difficulty 4

Generates two-step linear inequalities.

**Variants:** `two_step_inequality`

```
Problem: Solve the inequality: x/-4 + 8 ≥ 12
Steps:
  INEQ_SETUP|x/-4 + 8 ≥ 12
  INEQ_OP_BOTH|subtract|8|x/-4|4
  INEQ_SIMPLIFY|x/-4 ≥ 4
  INEQ_OP_BOTH|multiply|-4|x|-16
  INEQ_FLIP|Multiplying by negative number reverses inequality
  INEQ_RESULT|x|≤|-16
  Z|x ≤ -16
Answer: x ≤ -16
```

### Linear Fractional — `LinearFractionalGenerator`  ·  middle · difficulty 4

Linear equations and inequalities with fraction or decimal coefficients, solved the way it's taught: clear the fractions/decimals first (multiply every term by the LCD or by 10), then solve the resulting integer two-step problem. Inequalities flip when dividing by a negative.

**Variants:** `linear_eq_decimals`, `linear_eq_fractions`, `linear_ineq_decimals`, `linear_ineq_fractions`

```
Problem: Solve for x: 0.8x - 8.9 = -12.1
Steps:
  EQ_SETUP|0.8x - 8.9 = -12.1
  MUL_TERM|10|0.8x|8x
  MUL_TERM|10|- 8.9|-89
  MUL_TERM|10|-12.1|-121
  REWRITE|8x - 89 = -121
  EQ_OP_BOTH|add|89|8x|-32
  EQ_SIMPLIFY|8x = -32
  EQ_OP_BOTH|divide|8|x|-4
  EQ_RESULT|x|-4
  CHECK|substitute|0.8(-4) - 8.9 = -12.1|-12.1
  Z|-4
Answer: -4
```

### Special Solution Equation — `SpecialSolutionEquationGenerator`  ·  middle · difficulty 4

Linear equations with variables on both sides whose outcome may be a unique solution, an identity (all real numbers), or a contradiction (no solution). All three outcomes are mixed so the classification must be earned by simplifying, never guessed.

**Variants:** `linear_eq_contradiction`, `linear_eq_identity`, `linear_eq_unique`

```
Problem: Solve for x: 5(x + 3) + 9x + 6 = 14x + 21
Steps:
  EQ_SETUP|5(x + 3) + 9x + 6 = 14x + 21
  DIST|5|x + 3|5x + 15
  COMB_X|5x|9x|14x
  COMB_CONST|15|6|21
  REWRITE|14x + 21 = 14x + 21
  MOVE_TERM|14x|left|21 = 21
  SPECIAL_SOLUTION|21 = 21|identity: true for every x
  CHECK_POINT|x=0|14·0 + 21 = 21|14·0 + 21 = 21
  CHECK_POINT|x=1|14·1 + 21 = 35|14·1 + 21 = 35
  Z|All real numbers
Answer: All real numbers
```

### Exponent Evaluation — `ExponentEvaluationGenerator`  ·  middle · difficulty 3

Generates exponent evaluation problems (compute a^n).

**Variants:** `exponent_evaluation`

```
Problem: Evaluate: 8^2
Steps:
  EXP_SETUP|8|2
  EXP_EXPAND|8 × 8
  EXP_PARTIAL|8|8|64
  Z|64
Answer: 64
```

### Exponent Rules — `ExponentRulesGenerator`  ·  middle · difficulty 4

Generates exponent rule problems.

**Variants:** `exponent_negative_rule`, `exponent_power_rule`, `exponent_product_rule`, `exponent_quotient_rule`, `exponent_zero_rule`

```
Problem: Simplify: b^(-2)
Steps:
  EXP_RULE_SETUP|b^(-2)
  EXP_RULE_IDENTIFY|negative_exponent|x^(-n) = 1/x^n
  EXP_RULE_APPLY|negate|2||2
  EXP_RULE_SIMPLIFY|1/b^2
  Z|1/b^2
Answer: 1/b^2
```

### Exponent Mixed Rules — `ExponentMixedRulesGenerator`  ·  middle · difficulty 4

Simplifies expressions that need TWO exponent rules in sequence (product/quotient/power), where inputs may carry negative exponents and the result may come out positive, negative (rewrite as 1/x^n), or zero (rewrite as 1). The outcome class is sampled first so all three appear evenly — the finishing rule must be earned, never assumed.

**Variants:** `exponent_mixed_rules`

```
Problem: Simplify (answer with positive exponents): m^5 · m^4 · m^(-4)
Steps:
  EXP_RULE_SETUP|m^5 · m^4 · m^(-4)
  EXP_RULE_IDENTIFY|product_rule|x^a · x^b = x^(a+b)
  EXP_RULE_APPLY|add|5|4|9
  REWRITE|m^9 · m^(-4)
  EXP_RULE_IDENTIFY|product_rule|x^a · x^b = x^(a+b)
  EXP_RULE_APPLY|add|9|-4|5
  REWRITE|m^5
  EXP_RULE_SIMPLIFY|m^5
  Z|m^5
Answer: m^5
```

### Scientific Notation — `ScientificNotationGenerator`  ·  middle · difficulty 4

Generates scientific notation problems.

**Variants:** `scientific_notation_convert_from`, `scientific_notation_convert_to`, `scientific_notation_divide`, `scientific_notation_multiply`

```
Problem: Divide: (25.0 × 10^5) ÷ (5.0 × 10^3)
Steps:
  SCI_SETUP|(25.0 × 10^5) ÷ (5.0 × 10^3)
  SCI_OPERATION|divide_coefficients|25.0|5.0|5.0
  SCI_OPERATION|subtract_exponents|5|3|2
  Z|5.0 × 10^2
Answer: 5.0 × 10^2
```

### Roots And Radicals — `RootsAndRadicalsGenerator`  ·  middle · difficulty 4

Generates square root, cube root, and radical simplification problems.

**Variants:** `cube_root_perfect`, `simplify_radical`, `square_root_perfect`

```
Problem: Evaluate: ∛512
Steps:
  ROOT_SETUP|∛512
  ROOT_IDENTIFY|512|perfect_cube|8
  ROOT_EXTRACT|8
  Z|8
Answer: 8
```

### Angle Relationships — `AngleRelationshipsGenerator`  ·  middle · difficulty 4

Generates angle relationship problems.

**Variants:** `complementary_angles`, `complementary_angles_algebraic`, `supplementary_angles`, `supplementary_angles_algebraic`, `vertical_angles`

```
Problem: Two angles are supplementary. One angle measures 127°. What is the measure of the other angle?
Steps:
  ANGLE_SETUP|supplementary|angle1 = 127°
  ANGLE_RELATION|angle1 + angle2 = 180°
  ANGLE_SOLVE|180 - 127|53
  Z|53°
Answer: 53°
```

### Angles With Parallel Lines — `AnglesWithParallelLinesGenerator`  ·  middle · difficulty 4

Generates problems involving angles formed by parallel lines and a transversal.

**Variants:** `parallel_alternate_exterior_angles`, `parallel_alternate_interior_angles`, `parallel_co_interior_angles`, `parallel_corresponding_angles`

```
Problem: Two parallel lines are cut by a transversal. Co-interior angles measure (2x + 21)° and (4x + 21)°. Find x.
Steps:
  PARALLEL_SETUP|co_interior|Co-interior angles are supplementary (sum to 180°)
  PARALLEL_RELATION|(2x + 21) + (4x + 21) = 180
  PARALLEL_SOLVE|6x + 42 = 180|x = 23
  Z|23
Answer: 23
```

### Triangle Angle Sum — `TriangleAngleSumGenerator`  ·  middle · difficulty 4

Generates triangle angle sum problems (angles sum to 180°).

**Variants:** `exterior_angle_theorem`, `triangle_angle_sum`, `triangle_angle_sum_algebraic`

```
Problem: In a triangle, the angles measure (1x + 12)°, (3x + 9)°, and (4x - 25)°. Find the value of x.
Steps:
  TRI_ANGLE_SETUP|1x + 12|3x + 9|4x - 25
  TRI_ANGLE_SUM|(1x + 12) + (3x + 9) + (4x - 25) = 180
  TRI_ANGLE_SOLVE|8x + -4 = 180|x = 23
  Z|23
Answer: 23
```

### Circle Area Circumference — `CircleAreaCircumferenceGenerator`  ·  middle · difficulty 4

Generates circle area and circumference problems.

**Variants:** `circle_area`, `circle_circumference`

```
Problem: Find the circumference of a circle with diameter 17 units.
Steps:
  CIRCLE_SETUP|17|diameter
  CIRCLE_FORMULA|C = πd
  CIRCLE_SUBSTITUTE|C = π × 17
  CIRCLE_CALCULATE|C = 17π|17π
  Z|17π units
Answer: 17π units
```

### Volume Prism — `VolumePrismGenerator`  ·  middle · difficulty 4

Generates volume of prism problems.

**Variants:** `volume_rectangular_prism`, `volume_triangular_prism`

```
Problem: Find the volume of a triangular prism. The triangular base has a base of 10 units and height of 3 units. The prism has a length of 9 units.
Steps:
  VOL_SETUP|triangular_prism|b=10, h_tri=3, length=9
  VOL_FORMULA|V = Base Area × length
  VOL_BASE_AREA|Base Area = (1/2) × 10 × 3|15.0
  VOL_CALCULATE|V = 15.0 × 9|135.0
  Z|135 cubic units
Answer: 135 cubic units
```

### Volume Cylinder — `VolumeCylinderGenerator`  ·  middle · difficulty 4

Generates volume of cylinder problems.

**Variants:** `volume_cylinder`

```
Problem: Find the volume of a cylinder with radius 8 units and height 6 units.
Steps:
  VOL_SETUP|cylinder|r=8, h=6
  VOL_FORMULA|V = πr²h
  VOL_BASE_AREA|r² = 8² = 64|64
  VOL_CALCULATE|V = π × 64 × 6|384π
  Z|384π cubic units
Answer: 384π cubic units
```

### Surface Area Prism — `SurfaceAreaPrismGenerator`  ·  middle · difficulty 4

Generates surface area of prism problems.

**Variants:** `surface_area_rectangular_prism`

```
Problem: Find the surface area of a rectangular prism with length 9 units, width 9 units, and height 3 units.
Steps:
  SA_SETUP|rectangular_prism|l=9, w=9, h=3
  SA_FORMULA|SA = 2(lw + lh + wh)
  SA_FACES|top/bottom|9 × 9|81
  SA_FACES|front/back|9 × 3|27
  SA_FACES|left/right|9 × 3|27
  SA_TOTAL|SA = 2(81 + 27 + 27)|270
  Z|270 square units
Answer: 270 square units
```

### Surface Area Cylinder — `SurfaceAreaCylinderGenerator`  ·  middle · difficulty 4

Generates surface area of cylinder problems.

**Variants:** `surface_area_cylinder`

```
Problem: Find the surface area of a cylinder with radius 8 units and height 11 units.
Steps:
  SA_SETUP|cylinder|r=8, h=11
  SA_FORMULA|SA = 2πr² + 2πrh
  SA_BASES|2π(8)² = 2π × 64|128π
  SA_LATERAL|2π × 8 × 11|176π
  SA_TOTAL|SA = 128π + 176π|304π
  Z|304π square units
Answer: 304π square units
```

### Round Solids — `RoundSolidsGenerator`  ·  middle · difficulty 4

Volume and surface area of pyramids, cones, and spheres — the round and pointed solids missing from the prism/cylinder generators. Everything is exact: π stays symbolic, cone slants come from Pythagorean triples, and volumes divisible by 3 are arranged by construction (a sphere volume may keep the /3: '500π/3 cubic units').

**Variants:** `surface_area_cone`, `surface_area_pyramid`, `surface_area_sphere`, `volume_cone`, `volume_pyramid`, `volume_sphere`

```
Problem: Find the surface area of a square pyramid with base side 8 units and slant height 3 units.
Steps:
  SA_FORMULA|SA = b² + 2bl (square base, slant height l)
  E|8|2|64
  M|8|3|24
  M|2|24|48
  A|64|48|112
  Z|112 square units
Answer: 112 square units
```

### Pythag Hyp — `PythagHypGenerator`  ·  middle · difficulty 4

Generates Pythagorean theorem problems (finding hypotenuse).

**Variants:** `pythag_hyp`

```
Problem: Find hypotenuse: legs 60 and 32
Steps:
  E|60|2|3600
  E|32|2|1024
  A|3600|1024|4624
  ROOT|4624|68
  Z|68
Answer: 68
```

### Pythagorean Leg — `PythagoreanLegGenerator`  ·  middle · difficulty 4

Generates Pythagorean theorem problems to find a leg.

**Variants:** `pythagorean_find_leg`

```
Problem: In a right triangle, the hypotenuse is 40 units and one leg is 24 units. Find the length of the other leg.
Steps:
  PYTHAG_SETUP|c=40|a=24|b=?
  PYTHAG_FORMULA|a² + b² = c²
  PYTHAG_SUBSTITUTE|24² + b² = 40²
  PYTHAG_SQUARE|24|576
  PYTHAG_SQUARE|40|1600
  PYTHAG_SOLVE|b² = 1600 - 576|1024
  PYTHAG_ROOT|1024|32
  Z|32 units
Answer: 32 units
```

### Pythagorean Word Problem — `PythagoreanWordProblemGenerator`  ·  middle · difficulty 4

Generates word problems involving the Pythagorean theorem.

**Variants:** `pythagorean_word_problem`

```
Problem: A rectangle has a length of 30 units and a width of 40 units. What is the length of its diagonal?
Steps:
  PYTHAG_CONTEXT|rectangle_diagonal|length=30, width=40
  PYTHAG_MODEL|length=30|width=40|diagonal=?
  PYTHAG_FORMULA|d² = l² + w²
  PYTHAG_SUBSTITUTE|d² = 30² + 40²
  PYTHAG_CALCULATE|d² = 900 + 1600 = 2500|2500
  PYTHAG_CALCULATE|d = √2500|50
  Z|50 units
Answer: 50 units
```

### Mean — `MeanGenerator`  ·  middle · difficulty 3

Generates mean (average) calculation problems.

**Variants:** `mean`

```
Problem: Find the mean of the following data set: 50, 33, 62, 81, 47, 56, 63, 56
Steps:
  STAT_SETUP|50, 33, 62, 81, 47, 56, 63, 56
  STAT_SUM|50 + 33 + 62 + 81 + 47 + 56 + 63 + 56|448
  STAT_COUNT|8
  STAT_DIVIDE|448 / 8|56
  Z|56
Answer: 56
```

### Median — `MedianGenerator`  ·  middle · difficulty 3

Generates median calculation problems.

**Variants:** `median`

```
Problem: Find the median of the following data set: 63, 15, 43, 75, 72, 61, 48, 71
Steps:
  STAT_SETUP|63, 15, 43, 75, 72, 61, 48, 71
  STAT_ORDER|15, 43, 48, 61, 63, 71, 72, 75
  STAT_MIDDLE|positions 4 and 5|61, 63
  STAT_AVERAGE|(61 + 63) / 2|62.0
  Z|62
Answer: 62
```

### Mode — `ModeGenerator`  ·  middle · difficulty 3

Generates mode calculation problems.

**Variants:** `mode`, `mode_bimodal`, `mode_none`

```
Problem: Find the mode of the following data set: 44, 73, 43, 73, 88, 44, 88, 43, 76, 15, 44, 76, 88, 44, 15, 88
Steps:
  STAT_SETUP|44, 73, 43, 73, 88, 44, 88, 43, 76, 15, 44, 76, 88, 44, 15, 88
  STAT_FREQUENCY|15|2
  STAT_FREQUENCY|43|2
  STAT_FREQUENCY|44|4
  STAT_FREQUENCY|73|2
  STAT_FREQUENCY|76|2
  STAT_FREQUENCY|88|4
  STAT_MODE|44 and 88|4
  Z|44 and 88
Answer: 44 and 88
```

### Range — `RangeGenerator`  ·  middle · difficulty 3

Generates range calculation problems.

**Variants:** `range`

```
Problem: Find the range of the following data set: 59, 63, 15, 43, 75, 72, 61, 48, 71, 55, 84, 37
Steps:
  STAT_SETUP|59, 63, 15, 43, 75, 72, 61, 48, 71, 55, 84, 37
  STAT_MIN|15
  STAT_MAX|84
  STAT_RANGE|84 - 15|69
  Z|69
Answer: 69
```

### Mean Absolute Deviation — `MeanAbsoluteDeviationGenerator`  ·  middle · difficulty 4

Generates Mean Absolute Deviation (MAD) problems.

**Variants:** `mean_absolute_deviation`

```
Problem: Find the Mean Absolute Deviation (MAD) of the following data set: 57, 30, 42, 39, 37, 59
Steps:
  STAT_SETUP|57, 30, 42, 39, 37, 59
  STAT_MEAN|264 / 6|44
  STAT_DEVIATION|57|44|13
  STAT_ABS_DEV|13|13
  STAT_DEVIATION|30|44|-14
  STAT_ABS_DEV|-14|14
  STAT_DEVIATION|42|44|-2
  STAT_ABS_DEV|-2|2
  STAT_DEVIATION|39|44|-5
  STAT_ABS_DEV|-5|5
  STAT_DEVIATION|37|44|-7
  STAT_ABS_DEV|-7|7
  STAT_DEVIATION|59|44|15
  STAT_ABS_DEV|15|15
  STAT_MAD|56|6|9.33
  Z|9.33
Answer: 9.33
```

### Compound Probability Independent — `CompoundProbabilityIndependentGenerator`  ·  middle · difficulty 4

Generates compound probability problems with independent events.

**Variants:** `compound_probability_independent`

```
Problem: A bag contains 1 red, 5 blue, 5 green, 3 yellow marbles. A marble is drawn, replaced, and another marble is drawn. What is the probability of drawing a yellow marble first and a yellow marble second?
Steps:
  PROB_DESCRIBE|Draw with replacement: yellow then yellow
  PROB_IDENTIFY|P(yellow)|3/14
  PROB_IDENTIFY|P(yellow)|3/14
  PROB_INDEPENDENT|Drawing with replacement means independent events
  PROB_MULTIPLY|3/14|3/14|9/196
  Z|9/196
Answer: 9/196
```

### Compound Probability Dependent — `CompoundProbabilityDependentGenerator`  ·  middle · difficulty 4

Generates compound probability problems with dependent events.

**Variants:** `compound_probability_dependent`

```
Problem: Two cards are drawn from a standard deck without replacement. What is the probability that both cards are spades?
Steps:
  PROB_DESCRIBE|Draw two spades cards without replacement
  PROB_IDENTIFY|P(first spades)|1/4 = 13/52
  PROB_DEPENDENT|Drawing without replacement means dependent events
  PROB_CONDITIONAL|P(second spades|first was spades)|4/17 = 12/51
  PROB_MULTIPLY|13/52|12/51|1/17
  Z|1/17
Answer: 1/17
```

### Geometric Probability — `GeometricProbabilityGenerator`  ·  middle · difficulty 4

Geometric probability as a ratio of measures: interval length to total length, rectangle area to total area, or sector angle to full-circle angle. All inputs are integers and all final probabilities are exact.

**Variants:** `geometric_probability_interval`, `geometric_probability_rectangle`, `geometric_probability_sector`

```
Problem: A point is chosen uniformly at random in a 18 by 6 rectangle. A shaded rectangle inside it is 9 by 5. What is the probability that the point lands in the shaded rectangle? Give an exact answer.
Steps:
  GEO_PROB_SETUP|rectangle 18 by 6|shaded rectangle 9 by 5
  MEASURE_TOTAL|whole area|18 * 6 = 108
  MEASURE_FAVORABLE|shaded area|9 * 5 = 45
  GEO_PROB_FORMULA|probability = favorable area / total area
  FRAC_BUILD|45/108|5/12
  CHECK|45 <= 108|probability is at most 1
  Z|5/12
Answer: 5/12
```

### Finance — `FinanceGenerator`  ·  middle · difficulty 4

Everyday financial arithmetic: simple interest, annual compounding, loan payment breakdowns, and budget percentage splits. Amounts are constructed so dollar-and-cent answers are exact.

**Variants:** `finance_budget_split`, `finance_compound_interest`, `finance_loan_payment`, `finance_simple_interest`

```
Problem: A monthly income of $3800 is split into needs 50%, savings 20%, and fun 30%. Find the dollar amount for each category.
Steps:
  FIN_SETUP|income = 3800|needs 50%, savings 20%, fun 30%|budget amounts
  FIN_FORMULA|category amount = income * category percent
  PERCENT_TO_DEC|50%|0.5
  M|3800|0.5|1900
  PERCENT_TO_DEC|20%|0.2
  M|3800|0.2|760
  PERCENT_TO_DEC|30%|0.3
  M|3800|0.3|1140
  A|1900|760|2660
  A|2660|1140|3800
  Z|needs $1900.00; savings $760.00; fun $1140.00
Answer: needs $1900.00; savings $760.00; fun $1140.00
```

### Kinematics — `KinematicsGenerator`  ·  middle · difficulty 4

Basic kinematics formula chains with consistent units: distance from d = vt, speed from v = d/t, time from t = d/v, and acceleration from a = (v_f - v_i)/t.

**Variants:** `kinematics_acceleration`, `kinematics_distance`, `kinematics_speed`, `kinematics_time`

```
Problem: A cart's velocity changes from 1 meters per second to 41 meters per second in 8 seconds. Find the acceleration.
Steps:
  KIN_SETUP|v_i = 1 m/s|v_f = 41 m/s, t = 8 s|acceleration
  KIN_FORMULA|a = (v_f - v_i)/t
  S|41|1|40
  D|40|8|5
  UNIT_ATTACH|5|m/s^2|5 m/s^2
  Z|5 m/s^2
Answer: 5 m/s^2
```

### Physics Formula — `PhysicsFormulaGenerator`  ·  middle · difficulty 4

Work, force, power, and energy formula chains with unit-consistent arithmetic. Minute-based variants explicitly convert minutes to seconds before using watts = joules/second.

**Variants:** `physics_formula_energy`, `physics_formula_force`, `physics_formula_power_minutes`, `physics_formula_power_seconds`, `physics_formula_work`

```
Problem: A machine does 7020 joules of work in 1 minute. Find the power in watts.
Steps:
  PHYS_SETUP|W = 7020 joules|t = 1 minute|power
  UNIT_CONVERT|1 minute|60 seconds
  PHYS_FORMULA|P = W/t
  D|7020|60|117
  UNIT_ATTACH|117|watts|117 watts
  Z|117 watts
Answer: 117 watts
```

### Base Conversion — `BaseConversionGenerator`  ·  middle · difficulty 3

Binary and hexadecimal conversions by place value and repeated division, plus 8-bit two's complement representation for negative integers.

**Variants:** `base_conversion_binary_to_decimal`, `base_conversion_decimal_to_binary`, `base_conversion_decimal_to_hex`, `base_conversion_hex_to_decimal`, `base_conversion_twos_complement`

```
Problem: Convert decimal 3120 to hexadecimal.
Steps:
  BASE_SETUP|3120_10|hexadecimal
  DIVMOD|3120|16|195|r=0
  DIVMOD|195|16|12|r=3
  DIVMOD|12|16|0|r=12
  REVERSE|0,3,C|C30
  Z|C30
Answer: C30
```

### Base Arithmetic — `BaseArithmeticGenerator`  ·  middle · difficulty 4

Column arithmetic in base 2, 8, and 16. Addition works right-to-left with in-base carries; multiplication uses a one-digit multiplier and carries through each column.

**Variants:** `base_arithmetic_addition`, `base_arithmetic_multiplication`

```
Problem: In base 16, multiply A7_16 by 6_16.
Steps:
  BASE_ARITH_SETUP|base 16|A7 * 6
  BASE_MUL_COL|col 0|7 * 6 + carry 0|42 -> digit A, carry 2
  BASE_MUL_COL|col 1|A * 6 + carry 2|62 -> digit E, carry 3
  BASE_CARRY|carry 3|digit 3, carry 0
  REVERSE|A,E,3|3EA
  CHECK|167 * 6|1002|3EA
  Z|3EA_16
Answer: 3EA_16
```

### Bitwise Ops — `BitwiseOpsGenerator`  ·  middle · difficulty 3

Bitwise AND, OR, and XOR as truth tables and 4-bit masking operations. Masking traces compute each bit independently, then reassemble the result.

**Variants:** `bitwise_ops_mask`, `bitwise_ops_truth_table`

```
Problem: Apply bitwise OR to 4-bit value 0001_2 with mask 1000_2. Give the binary and decimal result.
Steps:
  BIT_SETUP|0001 OR 1000|4-bit mask
  BIT_RULE|OR|1 when at least one bit is 1
  BIT_ROW|bit 0|1 OR 0|1
  BIT_ROW|bit 1|0 OR 0|0
  BIT_ROW|bit 2|0 OR 0|0
  BIT_ROW|bit 3|0 OR 1|1
  REVERSE|1,0,0,1|1001
  CHECK|1 OR 8|9|1001
  Z|1001_2 = 9
Answer: 1001_2 = 9
```

### Modular Arithmetic — `ModularArithmeticGenerator`  ·  middle · difficulty 4

Applied modular arithmetic: clock arithmetic, ISBN-10 check digits, and Luhn check digits. Each variant shows the modular reduction that makes the procedure useful.

**Variants:** `modular_arithmetic_clock`, `modular_arithmetic_isbn10`, `modular_arithmetic_luhn`

```
Problem: Find the ISBN-10 check digit for prefix 604876475.
Steps:
  MOD_SETUP|ISBN-10 modulus 11|prefix 604876475
  MOD_TERM|10 * 6|60
  MOD_TERM|9 * 0|0
  A|60|0|60
  MOD_TERM|8 * 4|32
  A|60|32|92
  MOD_TERM|7 * 8|56
  A|92|56|148
  MOD_TERM|6 * 7|42
  A|148|42|190
  MOD_TERM|5 * 6|30
  A|190|30|220
  MOD_TERM|4 * 4|16
  A|220|16|236
  MOD_TERM|3 * 7|21
  A|236|21|257
  MOD_TERM|2 * 5|10
  A|257|10|267
  MOD_REDUCE|267|mod 11|3
  MOD_SOLVE|d ≡ -3 mod 11|8
  CHECK|267 + 8|275|multiple of 11
  Z|8
Answer: 8
```

### Manual Square Root — `ManualSquareRootGenerator`  ·  middle · difficulty 4

By-hand square root procedures: the classic digit-by-digit paired-groups algorithm for perfect squares, and one divide-and-average iteration.

**Variants:** `manual_square_root_digit_by_digit`, `manual_square_root_divide_average`

```
Problem: Use one divide-and-average step to estimate sqrt(408) starting from x0 = 30. What is the next estimate?
Steps:
  SQRT_SETUP|N = 408|x0 = 30
  D|408|30|13.6
  A|30|13.6|43.6
  D|43.6|2|21.8
  CHECK|divide-and-average|(x + N/x)/2|21.8
  Z|21.8
Answer: 21.8
```

### Calendar Arithmetic — `CalendarArithmeticGenerator`  ·  middle · difficulty 3

Calendar arithmetic with explicit day counts and modulo-7 weekday logic: days between dates, weekday after an offset, and counting a weekday in an inclusive date range.

**Variants:** `calendar_arithmetic_count_weekday`, `calendar_arithmetic_days_between`, `calendar_arithmetic_weekday_after`

```
Problem: 2028-04-01 is a Saturday. What weekday is it after 114 days?
Steps:
  CAL_SETUP|2028-04-01|Saturday, offset 114 days|weekday
  A|5|114|119
  MOD_REDUCE|119|mod 7|0
  WEEKDAY_SCAN|index 0|Monday
  Z|Monday
Answer: Monday
```

### Pascal Triangle — `PascalTriangleGenerator`  ·  middle · difficulty 3

Builds Pascal's triangle row by row - each entry as an explicit addition of the two above it - then reads off the requested value.

**Variants:** `pascal_triangle_ncr`, `pascal_triangle_row`

```
Problem: Use Pascal's triangle to find 9C1 (row 0 is 1).
Steps:
  PASCAL_SETUP|9C1
  PASCAL_ROW|0|1
  PASCAL_ROW|1|1, 1
  A|1|1|2
  PASCAL_ROW|2|1, 2, 1
  A|1|2|3
  A|2|1|3
  PASCAL_ROW|3|1, 3, 3, 1
  A|1|3|4
  A|3|3|6
  A|3|1|4
  PASCAL_ROW|4|1, 4, 6, 4, 1
  A|1|4|5
  A|4|6|10
  A|6|4|10
  A|4|1|5
  PASCAL_ROW|5|1, 5, 10, 10, 5, 1
  A|1|5|6
  A|5|10|15
  A|10|10|20
  A|10|5|15
  A|5|1|6
  PASCAL_ROW|6|1, 6, 15, 20, 15, 6, 1
  A|1|6|7
  A|6|15|21
  A|15|20|35
  A|20|15|35
  A|15|6|21
  A|6|1|7
  PASCAL_ROW|7|1, 7, 21, 35, 35, 21, 7, 1
  A|1|7|8
  A|7|21|28
  A|21|35|56
  A|35|35|70
  A|35|21|56
  A|21|7|28
  A|7|1|8
  PASCAL_ROW|8|1, 8, 28, 56, 70, 56, 28, 8, 1
  A|1|8|9
  A|8|28|36
  A|28|56|84
  A|56|70|126
  A|70|56|126
  A|56|28|84
  A|28|8|36
  A|8|1|9
  PASCAL_ROW|9|1, 9, 36, 84, 126, 126, 84, 36, 9, 1
  TABLE_LOOKUP|row 9, entry 1|9
  Z|9
Answer: 9
```

### Nets Surface Area — `NetsSurfaceAreaGenerator`  ·  middle · difficulty 4

Surface area from a net described textually as a list of faces. Each face's area is computed, pairs are doubled explicitly, and the areas are accumulated left to right.

**Variants:** `net_surface_area`

```
Problem: A net consists of: 1 square 8 by 8; 4 triangles with base 8 and height 3. All lengths are in the same unit. Find the total surface area.
Steps:
  NET_SETUP|1 square 8 by 8; 4 triangles with base 8 and height 3|total surface area
  M|8|8|64
  M|8|3|24
  D|24|2|12
  M|4|12|48
  A|64|48|112
  Z|112 square units
Answer: 112 square units
```

### Taxicab Geometry — `TaxicabGeometryGenerator`  ·  middle · difficulty 3

Taxicab and Chebyshev metrics with middle-school arithmetic: distances, the lattice-point counts of taxicab 'circles' (diamonds) and Chebyshev 'circles' (squares), and a head-to-head comparison of the two metrics on one pair of points.

**Variants:** `taxicab_cheb_circle`, `taxicab_cheb_distance`, `taxicab_compare`, `taxicab_taxi_circle`, `taxicab_taxi_distance`

```
Problem: In Chebyshev geometry, how many lattice points lie at distance exactly 8 from the origin?
Steps:
  METRIC|Chebyshev circle|all points with max(abs(x), abs(y)) = 8
  REWRITE|the 'circle' is a square with side 16; its border contains 8·8 lattice points
  M|8|8|64
  Z|64
Answer: 64
```

### Euler Characteristic — `EulerCharacteristicGenerator`  ·  middle · difficulty 3

Euler characteristic V - E + F: compute it for named polyhedra (sphere-family solids give 2), recover a missing count from V - E + F = 2, and see the torus break the rule with 0.

**Variants:** `euler_characteristic_compute`, `euler_characteristic_find_missing`, `euler_characteristic_torus`

```
Problem: A convex polyhedron has 10 edges and 6 faces. How many vertices does it have?
Steps:
  EULER_SETUP|convex polyhedron: E = 10, F = 6|V
  EULER_FORMULA|V - E + F = 2
  A|2|10|12
  S|12|6|6
  Z|V = 6
Answer: V = 6
```

### Five Number Summary — `FiveNumberSummaryGenerator`  ·  middle · difficulty 3

Five-number summary, IQR, and the 1.5×IQR outlier fence, worked on small integer data sets sized so both quartiles are actual data points (halves have odd length). Planted outliers sit far above the fence by construction.

**Variants:** `five_number_summary_iqr`, `five_number_summary_outliers`, `five_number_summary_summary`

```
Problem: Find the interquartile range of the data set: 36, 27, 13, 13, 35, 24, 7, 37, 37, 42, 30, 18, 21, 23.
Steps:
  SORT|36,27,13,13,35,24,7,37,37,42,30,18,21,23|7,13,13,18,21,23,24,27,30,35,36,37,37,42
  MEDIAN_PAIR|24|27
  MEAN_DIV|51|2|25.5
  QUARTILE|Q1|7,13,13,18,21,23,24|18
  QUARTILE|Q3|27,30,35,36,37,37,42|36
  S|36|18|18
  Z|18
Answer: 18
```

### Standard Deviation — `StandardDeviationGenerator`  ·  middle · difficulty 4

Variance and standard deviation by hand with the classic deviation table: mean first, one DEV_ROW per value with x, x - mean, and (x - mean)^2, then the sum of squares divided by n (population) or n - 1 (sample). Data are built from integer deviations that sum to zero, so the mean is always an integer.

**Variants:** `standard_deviation_population_std`, `standard_deviation_population_variance`, `standard_deviation_sample_variance`

```
Problem: Find the sample variance of the data set: 27, 16, 20, 23, 24. Give an exact answer.
Steps:
  A|27|16|43
  A|43|20|63
  A|63|23|86
  A|86|24|110
  MEAN_DIV|110|5|22
  DEV_ROW|27|5|25
  DEV_ROW|16|-6|36
  DEV_ROW|20|-2|4
  DEV_ROW|23|1|1
  DEV_ROW|24|2|4
  A|25|36|61
  A|61|4|65
  A|65|1|66
  A|66|4|70
  EVAL|n - 1|4
  D|70|4|35/2
  Z|35/2
Answer: 35/2
```

### Frequency Table — `FrequencyTableGenerator`  ·  middle · difficulty 3

Reading frequency tables and histograms: total the counts, find the mode, compute an exact relative frequency, read a cumulative count, and count values above a histogram threshold. Every table is embedded in the problem text so the answer is recomputable from it alone.

**Variants:** `frequency_table_above`, `frequency_table_cumulative`, `frequency_table_mode`, `frequency_table_relative`, `frequency_table_total`

```
Problem: A histogram of scores has these bin counts — 70-79: 5, 80-89: 9, 90-99: 8, 100-109: 7. What is the cumulative count of scores through the 90-99 bin?
Steps:
  FREQ_SETUP|histogram — 70-79: 5, 80-89: 9, 90-99: 8, 100-109: 7|cumulative count up to 90-99
  A|5|9|14
  A|14|8|22
  Z|22
Answer: 22
```

### Permutation Combination — `PermutationCombinationGenerator`  ·  middle · difficulty 4

Factorials, permutations, and combinations with the factorial arithmetic written out as running products — the by-hand way. Combinations reuse the permutation count and divide by r!. All answers are exact integers.

**Variants:** `permutation_combination_combination`, `permutation_combination_factorial`, `permutation_combination_permutation`, `permutation_combination_word`

```
Problem: In how many ways can 2 people be seated in a row of 2 chairs, chosen from a group of 10?
Steps:
  PERM_SETUP|arrange 2 of 10|order matters
  IDENTIFY|order matters|use P(n, r)
  PERM_FORMULA|P(n, r) = n·(n-1)···(n-r+1), 2 factors
  REWRITE|10 · 9
  M|10|9|90
  Z|90
Answer: 90
```

### Binomial Probability — `BinomialProbabilityGenerator`  ·  middle · difficulty 4

Binomial probabilities for small n, built the by-hand way: P(X = k) = C(n,k)·p^k·(1-p)^(n-k), with the combination and each power shown explicitly. Probabilities are small fractions, so every answer is exact.

**Variants:** `binomial_probability_at_least_one`, `binomial_probability_at_most`, `binomial_probability_exact_k`, `binomial_probability_mean`, `binomial_probability_variance`

```
Problem: A binomial experiment has n = 5 trials with success probability p = 3/10. Find the expected number of successes.
Steps:
  BINOM_SETUP|n = 5, p = 3/10|E[X]
  BINOM_FORMULA|E[X] = n·p
  M|5|3/10|1.5
  Z|1.5
Answer: 1.5
```

### Probability Addition Rule — `ProbabilityAdditionRuleGenerator`  ·  middle · difficulty 4

The addition rule P(A ∪ B) = P(A) + P(B) − P(A ∩ B), for both mutually exclusive events (intersection 0) and overlapping ones, plus the rearrangement that solves for the intersection. A concrete die variant reads the events as sets and counts outcomes. All probabilities are exact fractions.

**Variants:** `probability_addition_die`, `probability_addition_find_intersection`, `probability_addition_mutually_exclusive`, `probability_addition_overlapping`

```
Problem: A fair die is rolled. Let A be the event that the roll is at least 4 ([4, 5, 6]) and B the event that it is less than 3 ([1, 2]). Find P(A or B).
Steps:
  ADD_SETUP|fair die; A = [4, 5, 6], B = [1, 2]|P(A ∪ B)
  COUNT|A = [4, 5, 6]|3/6
  COUNT|B = [1, 2]|2/6
  COUNT|A ∩ B = []|0/6
  ADD_FORMULA|P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
  A|3/6|2/6|5/6
  S|5/6|0/6|5/6
  Z|5/6
Answer: 5/6
```

### Error Spotting — `ErrorSpottingGenerator`  ·  middle · difficulty 4

Critic-format problems: a worked scratchpad with exactly ONE seeded arithmetic mistake is given in the problem text (numbered lines, normal pipe dialect). Every given line after the mistake is consistent with it — the error propagates the way a real student's would. The task: verify line by line, flag the wrong one, redo the work from that point.

**Variants:** `error_spotting_equation`, `error_spotting_ratio`

```
Problem: The worked solution below contains exactly one arithmetic mistake. Check it line by line, identify the wrong line, and redo the work from that point.
Problem: A recipe mixes flour and sugar in a fixed ratio. Find the missing value.
Flour (cups): 54, ?
Sugar (cups): 48, 72
1) RATIO_TABLE|Flour (cups): 54, ?|Sugar (cups): 48, 72
2) RATIO_BASE|54:48|6|9:8
3) D|72|8|9
4) M|9|9|72
5) Z|72
Steps:
  VERIFY|1|ok
  VERIFY|2|ok
  VERIFY|3|ok
  FLAG|4|9 × 9 = 81, not 72
  M|9|9|81
  CHECK|cross_products|54×72=3888|48×81=3888
  Z|step 4; 81
Answer: step 4; 81
```

### Fill In Step — `FillInStepGenerator`  ·  middle · difficulty 3

Critic-format problems: a complete worked scratchpad is shown with one line blanked out (____); the task is to reconstruct the missing line exactly. The answer is the missing step verbatim, in pipe format.

**Variants:** `fill_in_step_equation`, `fill_in_step_ratio`, `fill_in_step_tip`

```
Problem: One line of the worked solution below has been blanked out (____). Reconstruct the missing line exactly.
Problem: A recipe mixes flour and sugar in a fixed ratio. Find the missing value.
Flour (cups): 54, ?
Sugar (cups): 48, 72
1) RATIO_TABLE|Flour (cups): 54, ?|Sugar (cups): 48, 72
2) RATIO_BASE|54:48|6|9:8
3) ____
4) M|9|9|81
5) Z|81
Steps:
  NEED|line 2 gives the base ratio 9:8|line 4 multiplies 9 by 9
  CHECK|arithmetic|72 ÷ 8 = 9|9
  Z|D|72|8|9
Answer: D|72|8|9
```

## High School

### Quadratic — `QuadraticGenerator`  ·  high · difficulty 5

Generates quadratic equation problems (ax^2 + bx + c = 0).

**Variants:** `quadratic_eq`

```
Problem: Solve x^2-6x = 0
Steps:
  DISC|36|0|36
  ROOT|36|6
  Q1|6|6|2|6
  Q2|6|6|2|0
  Z|x=6, x=0
Answer: x=6, x=0
```

### Percent Problem — `PercentProblemGenerator`  ·  high · difficulty 4

Generates various types of percentage problems with detailed division steps.

**Variants:** `percent_find_part`, `percent_find_percent`, `percent_find_whole`

```
Problem: 9 is what percent of 10?
Steps:
  SETUP_PERCENT_EQ|percent_dec = 9 / 10
  DEC_SHIFT|9/10|9/10|0
  DIV_SETUP|9|10
  D|90|10|9
  M|9|10|90
  S|90|90|0
  PLACE_DP_Q|9|1
  DEC_TO_PERCENT|0.9|90.00%
  Z|90.00%
Answer: 90.00%
```

### Literal Equation — `LiteralEquationGenerator`  ·  high · difficulty 4

Generates literal equations (equations with multiple variables) to solve for a specific variable.

**Variants:** `literal_eq_formula_area`, `literal_eq_formula_linear_y`, `literal_eq_formula_perimeter`, `literal_eq_one_step_add`, `literal_eq_one_step_div`, `literal_eq_one_step_mult`, `literal_eq_one_step_sub`, `literal_eq_two_step_linear`

```
Problem: Solve for l: P = 2l + 2w
Steps:
  EQ_SETUP|P = 2l + 2w
  EQ_OP_NOTE|subtract|2w|from both sides
  REWRITE|2l = P - 2w
  EQ_OP_NOTE|divide|2|from both sides
  REWRITE|l = (P - 2w)/2
  Z|(P - 2w)/2
Answer: (P - 2w)/2
```

### Absolute Value Equation — `AbsoluteValueEquationGenerator`  ·  high · difficulty 5

Generates absolute value equations: |ax + b| = c

**Variants:** `absolute_value_eq`

```
Problem: Solve: |5x + 3| = 0
Steps:
  ABS_SETUP||5x + 3| = 0
  ABS_SPLIT|Single case|5x + 3 = 0
  EQ_OP_BOTH|subtract|3|5x|-3
  EQ_OP_BOTH|divide|5|x|-3/5
  Z|x = -3/5
Answer: x = -3/5
```

### Absolute Value Inequality — `AbsoluteValueInequalityGenerator`  ·  high · difficulty 5

Generates absolute value inequalities: |ax + b| < c, |ax + b| > c, etc.

**Variants:** `absolute_value_ineq`

```
Problem: Solve: |x - 2| >= 17
Steps:
  ABS_INEQ_SETUP||x - 2| >= 17
  ABS_INEQ_SPLIT|OR case|x - 2 >= 17 OR x - 2 <= -17
  ABS_INEQ_PART|Part 1|x - 2 >= 17 -> x >= 19
  ABS_INEQ_PART|Part 2|x - 2 <= -17 -> x <= -15
  Z|x >= 19 OR x <= -15
Answer: x >= 19 OR x <= -15
```

### Compound Inequality — `CompoundInequalityGenerator`  ·  high · difficulty 4

Generates compound inequalities.

**Variants:** `compound_inequality`

```
Problem: Solve: 3x - 9 < -27 OR 3x - 9 > 9
Steps:
  COMP_INEQ_SETUP|3x - 9 < -27 OR 3x - 9 > 9
  COMP_INEQ_PART|Part 1|3x - 9 < -27 -> x < -6
  COMP_INEQ_PART|Part 2|3x - 9 > 9 -> x > 6
  Z|x < -6 OR x > 6
Answer: x < -6 OR x > 6
```

### Slope Two Points — `SlopeTwoPointsGenerator`  ·  high · difficulty 4

Generates problems to find the slope between two points (x1, y1) and (x2, y2).

**Variants:** `slope_two_points`

```
Problem: Find the slope of the line passing through (2, 3) and (2, 6)
Steps:
  SLOPE_SETUP|(2, 3)|(2, 6)
  SLOPE_FORMULA|m = (y2 - y1) / (x2 - x1)
  SLOPE_SUBST|m = (6 - 3) / (2 - 2)
  S|6|3|3
  S|2|2|0
  SLOPE_UNDEFINED|Division by zero
  Z|Undefined
Answer: Undefined
```

### Slope Intercept Form — `SlopeInterceptFormGenerator`  ·  high · difficulty 4

Generates problems to identify slope and y-intercept from an equation.

**Variants:** `slope_intercept_identify`

```
Problem: Identify the slope and y-intercept of the line: y = 2x + 3
Steps:
  SLOPE_INT_SETUP|y = 2x + 3
  SLOPE_INT_MATCH|Compare to Slope-Intercept Form|y = mx + b
  SLOPE_INT_IDENTIFY|Slope (m)|2
  SLOPE_INT_IDENTIFY|y-intercept (b)|3
  Z|m=2, b=3
Answer: m=2, b=3
```

### Equation From Two Points — `EquationFromTwoPointsGenerator`  ·  high · difficulty 5

Generates problems to find the equation of a line passing through two points. Target form: Slope-Intercept (y = mx + b).

**Variants:** `equation_from_two_points`

```
Problem: Find the equation of the line passing through (2, 3) and (4, -7)
Steps:
  EQ_2PT_SETUP|(2, 3)|(4, -7)
  SLOPE_FORMULA|m = (y2 - y1) / (x2 - x1)
  SLOPE_SUBST|m = (-7 - 3) / (4 - 2)
  SLOPE_RESULT|-5
  POINT_SLOPE_SETUP|y - 3 = -5(x - 2)
  DIST|-5|(x - 2)|-5x +10
  EQ_OP_NOTE|add|3|to isolate y
  Z|y = -5x + 13
Answer: y = -5x + 13
```

### Point Slope — `PointSlopeGenerator`  ·  high · difficulty 4

Generates problems involving Point-Slope form.

**Variants:** `point_slope_convert`

```
Problem: Convert to Slope-Intercept Form: y - 3 = 3(x - 2)
Steps:
  POINT_SLOPE_SETUP|y - 3 = 3(x - 2)
  GOAL|Convert to Slope-Intercept Form (y = mx + b)
  DIST|3|(x - 2)|3x -6
  EQ_OP_NOTE|add|3|to isolate y
  Z|y = 3x - 3
Answer: y = 3x - 3
```

### Standard Form Conversion — `StandardFormConversionGenerator`  ·  high · difficulty 4

Generates problems converting between Standard Form (Ax + By = C) and Slope-Intercept Form (y = mx + b).

**Variants:** `slope_intercept_to_standard`, `standard_to_slope_intercept`

```
Problem: Convert to Standard Form: y = 1x - 2/5
Steps:
  EQ_SETUP|y = 1x - 2/5
  GOAL|Convert to Standard Form (Ax + By = C, integers)
  EQ_OP_NOTE|multiply|5|to clear fractions
  REWRITE|5y = 5x - 2
  MOVE_TERM|5x|to left side|-5x + 5y = -2
  EQ_OP_NOTE|multiply|-1|to make A positive
  Z|5x - 5y = 2
Answer: 5x - 5y = 2
```

### Parallel Perpendicular Line — `ParallelPerpendicularLineGenerator`  ·  high · difficulty 5

Generates problems to find the equation of a line parallel or perpendicular to a given line, passing through a specific point.

**Variants:** `parallel_perpendicular_line`

```
Problem: Find the equation of the line perpendicular to y = 3x + 2 that passes through (3, -9)
Steps:
  LINE_RELATION_SETUP|perpendicular|y = 3x + 2|(3, -9)
  FIND_SLOPE|Given slope (m1)|3
  NEW_SLOPE|New slope (m2) = -1/3|Perpendicular lines have negative reciprocal slopes
  POINT_SLOPE_SETUP|y + 9 = -1/3(x - 3)
  DIST|-1/3|(x - 3)|-1/3x +3/3
  EQ_OP_NOTE|subtract|9|to isolate y
  Z|y = -1/3x - 8
Answer: y = -1/3x - 8
```

### Systems Substitution — `SystemsSubstitutionGenerator`  ·  high · difficulty 5

Generates systems of linear equations to be solved by substitution.

**Variants:** `systems_substitution`

```
Problem: Solve the system:
1) y = 3x - 3
2) 2x + 1y = 7
Steps:
  SYS_SETUP|y = 3x - 3|2x + 1y = 7
  SYS_SUBST|Substitute (3x - 3) for y in Eq 2
  SYS_EQ_NEW|New equation with x only
  DIST_COMBINE|5x + -3 = 7
  EQ_OP_BOTH|subtract|-3|5x|10
  EQ_OP_BOTH|divide|5|x|2
  SYS_SUBST_BACK|Substitute x=2 into Eq 1
  CALC|y = 3
  Z|x=2, y=3
Answer: x=2, y=3
```

### Systems Elimination — `SystemsEliminationGenerator`  ·  high · difficulty 5

Generates systems of linear equations to be solved by elimination.

**Variants:** `systems_elimination`

```
Problem: Solve the system by elimination:
1) -1x + 5y = 13
2) 2x + 5y = 19
Steps:
  SYS_SETUP|-1x + 5y = 13|2x + 5y = 19
  SYS_MULT|Eq2 * -1
  SYS_REWRITE|-1x + 5y = 13|-2x - 5y = -19
  SYS_ADD|Add equations: -3x = -6
  EQ_OP_BOTH|divide|-3|x|2
  SYS_SUBST_BACK|Substitute into Eq 1
  CALC|-1(2) + 5y = 13
  EQ_OP_BOTH|subtract|-2|5y|15
  EQ_OP_BOTH|divide|5|y|3
  CHECK|substitute|22 + 53 = 19|19
  Z|x=2, y=3
Answer: x=2, y=3
```

### Polynomial Add Sub — `PolynomialAddSubGenerator`  ·  high · difficulty 4

Generates problems for adding and subtracting polynomials.

**Variants:** `polynomial_add_sub`

```
Problem: (-6x^2 + 7) - (-6x)
Steps:
  POLY_SETUP|(-6x^2 + 7) - (-6x)
  POLY_DIST_NEG|Distribute negative sign to second polynomial
  POLY_GROUP_LIKE|(-6x^2) + (6x) + (7)
  POLY_COMBINE|-6x^2 + 6x + 7
  Z|-6x^2 + 6x + 7
Answer: -6x^2 + 6x + 7
```

### Monomial Mult Div — `MonomialMultDivGenerator`  ·  high · difficulty 4

Generates problems for multiplying and dividing monomials.

**Variants:** `monomial_div`, `monomial_mult`

```
Problem: Simplify: (4x^8) / (4x^5)
Steps:
  MONO_SETUP|(4x^8) / (4x^5)
  MONO_DIV_COEFF|4 / 4|1
  MONO_SUB_EXP|x^8 / x^5 = x^(8-5)|x^3
  Z|1x^3
Answer: 1x^3
```

### Factor GCF — `FactorGCFGenerator`  ·  high · difficulty 4

Factors the greatest common factor out of a 2- or 3-term polynomial.

**Variants:** `factor_gcf`

```
Problem: Factor out the greatest common factor: 18t^4 + 14t^2 + 16t
Steps:
  POLY_SETUP|18t^4 + 14t^2 + 16t
  GCF_COEFF|18, 14, 16|2
  GCF_VAR|t^4, t^2, t|t
  GCF_RESULT|2t
  DIV_TERM|18t^4|2t|9t^3
  DIV_TERM|14t^2|2t|7t
  DIV_TERM|16t|2t|8
  REWRITE|2t(9t^3 + 7t + 8)
  CHECK|distribute|2t·(9t^3) + 2t·(7t) + 2t·(8)|18t^4 + 14t^2 + 16t
  Z|2t(9t^3 + 7t + 8)
Answer: 2t(9t^3 + 7t + 8)
```

### Factor Trinomial — `FactorTrinomialGenerator`  ·  high · difficulty 4

Factors trinomials with visible trial-and-error (A2).

**Variants:** `factor_trinomial`, `factor_trinomial_general`

```
Problem: Factor: y^2 - 3y - 40
Steps:
  POLY_SETUP|y^2 - 3y - 40
  FACTOR_PAIR_GOAL|m·n = -40|m + n = -3
  TRY|(1, -40)|1·(-40)=-40, 1+(-40)=-39
  REJECT|(1, -40)|sum is -39, need -3
  TRY|(2, -20)|2·(-20)=-40, 2+(-20)=-18
  REJECT|(2, -20)|sum is -18, need -3
  TRY|(4, -10)|4·(-10)=-40, 4+(-10)=-6
  REJECT|(4, -10)|sum is -6, need -3
  TRY|(5, -8)|5·(-8)=-40, 5+(-8)=-3
  ACCEPT|(5, -8)|product -40 ✓, sum -3 ✓
  REWRITE|(y - 8)(y + 5)
  CHECK|foil|y^2 + 5y - 8y - 40|y^2 - 3y - 40
  Z|(y - 8)(y + 5)
Answer: (y - 8)(y + 5)
```

### Factor Special Forms — `FactorSpecialFormsGenerator`  ·  high · difficulty 4

Factors the special forms by pattern recognition: - difference of squares: a² − b² = (a − b)(a + b) - perfect-square trinomials: a² ± 2ab + b² = (a ± b)² - sum / difference of cubes: a³ ± b³ = (a ± b)(a² ∓ ab + b²)

**Variants:** `factor_difference_of_cubes`, `factor_difference_of_squares`, `factor_perfect_square`, `factor_sum_of_cubes`

```
Problem: Factor: n^3 - 27
Steps:
  POLY_SETUP|n^3 - 27
  FORM_IDENTIFY|difference_of_cubes|a^3 - b^3 = (a - b)(a^2 + ab + b^2)
  CBRT|n^3|n
  CBRT|27|3
  E|n|2|n^2
  M|n|3|3n
  E|3|2|9
  REWRITE|(n - 3)(n^2 + 3n + 9)
  CHECK|expand|n^3 + 3n^2 + 9n - 3n^2 - 9n - 27|n^3 - 27
  Z|(n - 3)(n^2 + 3n + 9)
Answer: (n - 3)(n^2 + 3n + 9)
```

### Factor Grouping — `FactorGroupingGenerator`  ·  high · difficulty 5

Factors four-term cubics by grouping. Built from (ax + b)(cx² + d) with each factor primitive and the quadratic factor irreducible over the integers, so the grouping answer is the complete factorization.

**Variants:** `factor_by_grouping`

```
Problem: Factor by grouping: 4y^3 + 2y^2 + 14y + 7
Steps:
  POLY_SETUP|4y^3 + 2y^2 + 14y + 7
  GROUP|(4y^3 + 2y^2)|(14y + 7)
  FACTOR_GROUP|4y^3 + 2y^2|2y^2|(2y + 1)
  FACTOR_GROUP|14y + 7|7|(2y + 1)
  REWRITE|(2y + 1)(2y^2 + 7)
  CHECK|expand|4y^3 + 14y + 2y^2 + 7|4y^3 + 2y^2 + 14y + 7
  Z|(2y + 1)(2y^2 + 7)
Answer: (2y + 1)(2y^2 + 7)
```

### Quadratic Factoring — `QuadraticFactoringGenerator`  ·  high · difficulty 5

Solves quadratics by factoring and the zero-product property.

**Variants:** `quadratic_by_factoring`, `quadratic_by_factoring_gcf`

```
Problem: Solve: y^2 + 9y = -8
Steps:
  EQ_SETUP|y^2 + 9y = -8
  MOVE_TERM|-8|left|y^2 + 9y + 8 = 0
  FACTOR_PAIR_GOAL|m·n = 8|m + n = 9
  TRY|(1, 8)|1·8=8, 1+8=9
  ACCEPT|(1, 8)|product 8 ✓, sum 9 ✓
  REWRITE|(y + 8)(y + 1) = 0
  ZERO_PRODUCT|(y + 8)(y + 1) = 0|y + 8 = 0 or y + 1 = 0
  EQ_RESULT|y|-8
  EQ_RESULT|y|-1
  CHECK|substitute|(-8)^2 + 9·(-8) + 8 = 0|0
  CHECK|substitute|(-1)^2 + 9·(-1) + 8 = 0|0
  Z|y = -8 or y = -1
Answer: y = -8 or y = -1
```

### Quadratic Square Root — `QuadraticSquareRootGenerator`  ·  high · difficulty 4

Solves quadratics with no linear term by taking square roots of both sides — remembering the ± and expanding it into both branches.

**Variants:** `quadratic_by_square_roots`

```
Problem: Solve: (y + 1)^2 = 4
Steps:
  EQ_SETUP|(y + 1)^2 = 4
  ROOT|4|2
  SQRT_BOTH_SIDES|(y + 1)^2 = 4|y + 1 = ±2
  PLUS_MINUS|y + 1 = ±2|y + 1 = 2 or y + 1 = -2
  EQ_OP_BOTH|subtract|1|y|1
  EQ_RESULT|y|1
  EQ_OP_BOTH|subtract|1|y|-3
  EQ_RESULT|y|-3
  CHECK|substitute|((-3) + 1)^2 = 4|4
  CHECK|substitute|(1 + 1)^2 = 4|4
  Z|y = -3 or y = 1
Answer: y = -3 or y = 1
```

### Completing Square — `CompletingSquareGenerator`  ·  high · difficulty 5

Completing the square, both uses: - solve: x² + bx + c = 0 (b even) — move c, add (b/2)² to both sides, recognize the PST, then the square-root machinery finishes it; the right side may be a perfect square (integer roots) or square-free (exact h ± √k answers) - vertex: y = x² + bx + c — add and subtract (b/2)² to reach y = (x + h)² + v

**Variants:** `completing_the_square`, `vertex_form_by_completing_square`

```
Problem: Write in vertex form: y = y^2 - 14y - 1
Steps:
  EQ_SETUP|y = y^2 - 14y - 1
  COMPLETE_SQUARE|half of -14 = -7|(-7)^2 = 49
  REWRITE|y = (y^2 - 14y + 49) - 49 - 1
  FORM_IDENTIFY|perfect_square_trinomial|a^2 - 2ab + b^2 = (a - b)^2
  REWRITE|y = (y - 7)^2 - 50
  Z|y = (y - 7)^2 - 50
Answer: y = (y - 7)^2 - 50
```

### Discriminant — `DiscriminantGenerator`  ·  high · difficulty 4

Discriminant analysis: compute Δ = b² − 4ac and classify the number and type of solutions. The outcome class is sampled first so all four appear evenly, and the answer is composite (Principle 8): 'Δ = 49; two rational solutions' — naming the class without computing Δ earns nothing.

**Variants:** `discriminant_analysis`

```
Problem: Without solving, use the discriminant to determine the number and type of solutions: 5x^2 + 7x + 4 = 0
Steps:
  EQ_SETUP|5x^2 + 7x + 4 = 0
  DISC|49|80|-31
  DISC_CLASSIFY|-31 < 0|no real solutions
  Z|Δ = -31; no real solutions
Answer: Δ = -31; no real solutions
```

### Radical Variable Simplify — `RadicalVariableSimplifyGenerator`  ·  high · difficulty 4

Simplifies radicals with variables: √(50x³) → 5x√(2x).

**Variants:** `simplify_radical_variables`

```
Problem: Simplify: √(490y)
Steps:
  ROOT_SETUP|√(490y)
  SQUARE_FACTOR|490|49 × 10|49
  ROOT|49|7
  REWRITE|7√(10y)
  CHECK|square_back|(7√(10y))^2 = 49 · 10y = 490y|490y
  Z|7√(10y)
Answer: 7√(10y)
```

### Radical Add Sub — `RadicalAddSubGenerator`  ·  high · difficulty 4

Adds and subtracts radicals: simplify every term to its like-radicand form first, then combine coefficients. About one case in five has genuinely unlike radicands after simplification — the honest answer is the simplified-but-uncombined expression (the judgment must be earned).

**Variants:** `radical_add_sub`

```
Problem: Simplify: 3√176 + 4√99
Steps:
  ROOT_SETUP|3√176 + 4√99
  SQUARE_FACTOR|176|16 × 11|16
  ROOT|16|4
  REWRITE|12√11 + 4√99
  SQUARE_FACTOR|99|9 × 11|9
  ROOT|9|3
  REWRITE|12√11 + 12√11
  A|12√11|12√11|24√11
  Z|24√11
Answer: 24√11
```

### Radical Multiply — `RadicalMultiplyGenerator`  ·  high · difficulty 4

Multiplies radicals: √a · √b = √(ab), then simplify what appears.

**Variants:** `radical_multiply`

```
Problem: Multiply and simplify: (1 + √13)(3 + √13)
Steps:
  ROOT_SETUP|(1 + √13)(3 + √13)
  FOIL_SETUP|(1 + √13)(3 + √13)
  M|1|3|3
  M|1|√13|√13
  M|√13|3|3√13
  M|√13|√13|13
  REWRITE|3 + √13 + 3√13 + 13
  A|3|13|16
  A|√13|3√13|4√13
  REWRITE|16 + 4√13
  Z|16 + 4√13
Answer: 16 + 4√13
```

### Radical Rationalize — `RadicalRationalizeGenerator`  ·  high · difficulty 5

Divides radicals and rationalizes denominators.

**Variants:** `radical_rationalize`

```
Problem: Rationalize the denominator and simplify: √117/√13
Steps:
  ROOT_SETUP|√117/√13
  FORM_IDENTIFY|quotient_of_radicals|√a/√b = √(a/b)
  D|117|13|9
  REWRITE|√9
  ROOT|9|3
  REWRITE|3
  Z|3
Answer: 3
```

### Rational Exponent — `RationalExponentGenerator`  ·  high · difficulty 4

Rational exponents ↔ radicals.

**Variants:** `rational_exponent_evaluate`, `rational_exponent_from_radical`, `rational_exponent_to_radical`

```
Problem: Write with a rational exponent: √(t^5)
Steps:
  EXP_RULE_SETUP|√(t^5)
  FORM_IDENTIFY|rational_exponent|ⁿ√(a^m) = a^(m/n)
  REWRITE|t^(5/2)
  Z|t^(5/2)
Answer: t^(5/2)
```

### Radical Equation — `RadicalEquationGenerator`  ·  high · difficulty 5

Solves radical equations. Squaring both sides produces CANDIDATES, not solutions — every candidate is tested in the ORIGINAL equation with TRY/ACCEPT/REJECT, and extraneous roots are rejected with the disagreement shown (the A1 discipline this skill exists to teach).

**Variants:** `radical_equation`

```
Problem: Solve: √(3x - 18) = x - 6
Steps:
  EQ_SETUP|√(3x - 18) = x - 6
  SQUARE_BOTH_SIDES|√(3x - 18) = x - 6|3x - 18 = (x - 6)^2
  E|(x - 6)|2|x^2 - 12x + 36
  REWRITE|3x - 18 = x^2 - 12x + 36
  MOVE_TERM|3x - 18|right|x^2 - 15x + 54 = 0
  FACTOR_PAIR_GOAL|m·n = 54|m + n = -15
  TRY|(-1, -54)|(-1)·(-54)=54, (-1)+(-54)=-55
  REJECT|(-1, -54)|sum is -55, need -15
  TRY|(-2, -27)|(-2)·(-27)=54, (-2)+(-27)=-29
  REJECT|(-2, -27)|sum is -29, need -15
  TRY|(-3, -18)|(-3)·(-18)=54, (-3)+(-18)=-21
  REJECT|(-3, -18)|sum is -21, need -15
  TRY|(-6, -9)|(-6)·(-9)=54, (-6)+(-9)=-15
  ACCEPT|(-6, -9)|product 54 ✓, sum -15 ✓
  REWRITE|(x - 6)(x - 9) = 0
  ZERO_PRODUCT|(x - 6)(x - 9) = 0|x = 6 or x = 9
  TRY|x = 6|lhs: √0 = 0, rhs: 0
  ACCEPT|x = 6|both sides 0 ✓
  TRY|x = 9|lhs: √9 = 3, rhs: 3
  ACCEPT|x = 9|both sides 3 ✓
  Z|x = 6 or x = 9
Answer: x = 6 or x = 9
```

### Rational Expr Simplify — `RationalExprSimplifyGenerator`  ·  high · difficulty 4

Simplifies rational expressions by factoring and cancelling. The full factor-pair trial-and-error runs for every trinomial — numerator and denominator alike — then the shared factor cancels.

**Variants:** `rational_expr_simplify`

```
Problem: Simplify: (y^2 + 6y - 7)/(y^2 - y - 56)
Steps:
  POLY_SETUP|(y^2 + 6y - 7)/(y^2 - y - 56)
  FACTOR_PAIR_GOAL|m·n = -7|m + n = 6
  TRY|(-1, 7)|(-1)·7=-7, (-1)+7=6
  ACCEPT|(-1, 7)|product -7 ✓, sum 6 ✓
  REWRITE|((y + 7)(y - 1))/(y^2 - y - 56)
  FACTOR_PAIR_GOAL|m·n = -56|m + n = -1
  TRY|(1, -56)|1·(-56)=-56, 1+(-56)=-55
  REJECT|(1, -56)|sum is -55, need -1
  TRY|(2, -28)|2·(-28)=-56, 2+(-28)=-26
  REJECT|(2, -28)|sum is -26, need -1
  TRY|(4, -14)|4·(-14)=-56, 4+(-14)=-10
  REJECT|(4, -14)|sum is -10, need -1
  TRY|(7, -8)|7·(-8)=-56, 7+(-8)=-1
  ACCEPT|(7, -8)|product -56 ✓, sum -1 ✓
  REWRITE|((y + 7)(y - 1))/((y + 7)(y - 8))
  CANCEL|(y + 7)|(y - 1)/(y - 8)
  Z|(y - 1)/(y - 8)
Answer: (y - 1)/(y - 8)
```

### Rational Expr Mult Div — `RationalExprMultDivGenerator`  ·  high · difficulty 5

Multiplies and divides rational expressions. Built from binomial constants so that after factoring both trinomials and multiplying across, exactly two factors cancel, leaving a binomial over a binomial:

**Variants:** `rational_expr_divide`, `rational_expr_multiply`

```
Problem: Simplify: (y^2 + 12y + 35)/(y^2 + 4y - 32) ÷ (y + 5)/(y + 8)
Steps:
  POLY_SETUP|(y^2 + 12y + 35)/(y^2 + 4y - 32) ÷ (y + 5)/(y + 8)
  FORM_IDENTIFY|divide_fractions|a/b ÷ c/d = a/b · d/c
  I|(y + 5)/(y + 8)|(y + 8)/(y + 5)
  FACTOR_PAIR_GOAL|m·n = 35|m + n = 12
  TRY|(1, 35)|1·35=35, 1+35=36
  REJECT|(1, 35)|sum is 36, need 12
  TRY|(5, 7)|5·7=35, 5+7=12
  ACCEPT|(5, 7)|product 35 ✓, sum 12 ✓
  REWRITE|((y + 5)(y + 7))/(y^2 + 4y - 32) · (y + 8)/(y + 5)
  FACTOR_PAIR_GOAL|m·n = -32|m + n = 4
  TRY|(-1, 32)|(-1)·32=-32, (-1)+32=31
  REJECT|(-1, 32)|sum is 31, need 4
  TRY|(-2, 16)|(-2)·16=-32, (-2)+16=14
  REJECT|(-2, 16)|sum is 14, need 4
  TRY|(-4, 8)|(-4)·8=-32, (-4)+8=4
  ACCEPT|(-4, 8)|product -32 ✓, sum 4 ✓
  REWRITE|((y + 5)(y + 7))/((y + 8)(y - 4)) · (y + 8)/(y + 5)
  FORM_IDENTIFY|multiply_fractions|a/b · c/d = ac/(bd)
  REWRITE|((y + 5)(y + 7)(y + 8))/((y + 8)(y - 4)(y + 5))
  CANCEL|(y + 5)|((y + 7)(y + 8))/((y + 8)(y - 4))
  CANCEL|(y + 8)|(y + 7)/(y - 4)
  Z|(y + 7)/(y - 4)
Answer: (y + 7)/(y - 4)
```

### Rational Expr Add Sub — `RationalExprAddSubGenerator`  ·  high · difficulty 5

Adds and subtracts rational expressions.

**Variants:** `rational_expr_add_sub`

```
Problem: Simplify: 5/(9y) + 8/(8y)
Steps:
  POLY_SETUP|5/(9y) + 8/(8y)
  L|9|8|72
  C|5/9y|8|40/72y
  C|8/8y|9|72/72y
  A|40|72|112
  REWRITE|112/(72y)
  F|112/(72y)|14/(9y)
  Z|14/(9y)
Answer: 14/(9y)
```

### Rational Equation — `RationalEquationGenerator`  ·  high · difficulty 5

Solves rational equations. The domain restriction is noted FIRST, the denominators are cleared, and every candidate is tested against the original — a candidate equal to a restricted value is rejected as extraneous, even when it is the only candidate (No solution).

**Variants:** `rational_equation`

```
Problem: Solve: x^2/(x - 8) = 64/(x - 8)
Steps:
  EQ_SETUP|x^2/(x - 8) = 64/(x - 8)
  DOMAIN_NOTE|x ≠ 8|denominator cannot be zero
  MUL_TERM|(x - 8)|x^2/(x - 8)|x^2
  MUL_TERM|(x - 8)|64/(x - 8)|64
  REWRITE|x^2 = 64
  ROOT|64|8
  SQRT_BOTH_SIDES|x^2 = 64|x = ±8
  PLUS_MINUS|x = ±8|x = 8 or x = -8
  TRY|x = 8|x = 8 makes x - 8 = 0
  REJECT|x = 8|makes a denominator zero — extraneous
  TRY|x = -8|lhs: -4, rhs: -4
  ACCEPT|x = -8|both sides -4 ✓
  Z|x = -8
Answer: x = -8
```

### Function Evaluation — `FunctionEvaluationGenerator`  ·  high · difficulty 3

Evaluates functions from rules and from tables: f(3) = ?

**Variants:** `function_evaluation_rule`, `function_evaluation_table`

```
Problem: Given g(x) = 5x^2 - 2x + 3, find g(-1).
Steps:
  FUNC_SETUP|g(x) = 5x^2 - 2x + 3|g(-1)
  SUBST|x|-1|5(-1)^2 - 2(-1) + 3
  E|(-1)|2|1
  M|5|1|5
  M|-2|-1|2
  A|5|2|7
  A|7|3|10
  Z|10
Answer: 10
```

### Function Table — `FunctionTableGenerator`  ·  high · difficulty 3

Builds a value table from a rule: evaluate f at each listed input.

**Variants:** `function_table`

```
Problem: Complete the table for g(x) = x^2 + 8 at x = -2, -1, 0, 1. Give the g(x) values in order.
Steps:
  FUNC_SETUP|g(x) = x^2 + 8|x = -2, -1, 0, 1
  SUBST|x|-2|(-2)^2 + 8
  E|(-2)|2|4
  A|4|8|12
  TABLE_ENTRY|g(-2)|12
  SUBST|x|-1|(-1)^2 + 8
  E|(-1)|2|1
  A|1|8|9
  TABLE_ENTRY|g(-1)|9
  SUBST|x|0|(0)^2 + 8
  E|(0)|2|0
  A|0|8|8
  TABLE_ENTRY|g(0)|8
  SUBST|x|1|(1)^2 + 8
  E|(1)|2|1
  A|1|8|9
  TABLE_ENTRY|g(1)|9
  Z|12, 9, 8, 9
Answer: 12, 9, 8, 9
```

### Piecewise Evaluation — `PiecewiseEvaluationGenerator`  ·  high · difficulty 4

Evaluates piecewise and step functions: pick the branch, then compute.

**Variants:** `piecewise_billing`, `piecewise_evaluation`, `piecewise_shipping`, `piecewise_tax`

```
Problem: A tax is 5% on the first $15000 of income and 20% on income above $15000. Find the tax on an income of $9500.
Steps:
  FUNC_SETUP|5% on first $15000 of income, 20% on income above $15000|income $9500
  BRANCH_TEST|9500 <= 15000|yes
  PERCENT_TO_DEC|5%|0.05
  M|9500|0.05|475
  Z|$475
Answer: $475
```

### Function Operations — `FunctionOperationsGenerator`  ·  high · difficulty 4

Function arithmetic evaluated at a point: (f + g)(k), (f - g)(k), (f · g)(k), (f/g)(k).

**Variants:** `function_op_add`, `function_op_divide`, `function_op_multiply`, `function_op_subtract`

```
Problem: Given g(x) = x^2 + 8 and h(x) = 5x + 4, find (g/h)(-2).
Steps:
  FUNC_SETUP|g(x) = x^2 + 8; h(x) = 5x + 4|(g/h)(-2)
  FUNC_OP|(g/h)(-2)|g(-2)/h(-2)
  SUBST|x|-2|(-2)^2 + 8
  E|(-2)|2|4
  A|4|8|12
  EVAL|g(-2)|12
  SUBST|x|-2|5(-2) + 4
  M|5|-2|-10
  A|-10|4|-6
  EVAL|h(-2)|-6
  D|12|-6|-2
  Z|-2
Answer: -2
```

### Function Composition — `FunctionCompositionGenerator`  ·  high · difficulty 4

Function composition, numeric and symbolic: f(g(2)) and f(g(x)).

**Variants:** `function_composition_numeric`, `function_composition_symbolic`

```
Problem: Given g(x) = 5x + 4 and f(x) = 2x + 7, find (g ∘ f)(x) as a simplified expression.
Steps:
  FUNC_SETUP|g(x) = 5x + 4; f(x) = 2x + 7|(g ∘ f)(x)
  FUNC_OP|(g ∘ f)(x)|g(f(x))
  SUBST|x|2x + 7|5(2x + 7) + 4
  DIST|5|2x + 7|10x + 35
  A|35|4|39
  REWRITE|10x + 39
  Z|10x + 39
Answer: 10x + 39
```

### Domain Range — `DomainRangeGenerator`  ·  high · difficulty 4

Finds the domain of a function from its equation: exclude zero denominators, require radicands nonnegative (strictly positive when the radical is itself a denominator).

**Variants:** `function_domain`

```
Problem: Find the domain of g(x) = √(2x - 16).
Steps:
  FUNC_SETUP|g(x) = √(2x - 16)|domain
  DOMAIN_COND|radicand ≥ 0|2x - 16 ≥ 0
  INEQ_OP_BOTH|add|16|2x|16
  INEQ_SIMPLIFY|2x ≥ 16
  INEQ_OP_BOTH|divide|2|x|8
  INEQ_RESULT|x|≥|8
  Z|x ≥ 8
Answer: x ≥ 8
```

### Inverse Function — `InverseFunctionGenerator`  ·  high · difficulty 4

Finds an inverse function by the algebraic method: write y = f(x), swap x and y, solve for y. Every record ends with an A1-style composition check that f(f⁻¹(x)) collapses back to x.

**Variants:** `inverse_function`

```
Problem: Find the inverse of g(x) = (x - 1)/2.
Steps:
  FUNC_SETUP|g(x) = (x - 1)/2|inverse
  REWRITE|y = (x - 1)/2
  SWAP_VARS|x = (y - 1)/2
  EQ_OP_BOTH|multiply|2|2x|y - 1
  EQ_OP_BOTH|add|1|2x + 1|y
  REWRITE|g⁻¹(x) = 2x + 1
  CHECK|compose|g(g⁻¹(x)) = ((2x + 1) - 1)/2 = 2x/2|x
  Z|2x + 1
Answer: 2x + 1
```

### Arithmetic Sequence — `ArithmeticSequenceGenerator`  ·  high · difficulty 4

Arithmetic sequences from four shown terms: the nth term, which term equals a given value, and the partial sum.

**Variants:** `arithmetic_sequence_nth_term`, `arithmetic_sequence_partial_sum`, `arithmetic_sequence_which_term`

```
Problem: The arithmetic sequence 4, -4, -12, -20, ... continues. Which term of the sequence equals -132?
Steps:
  SEQ_SETUP|4, -4, -12, -20, ...|which term equals -132
  COMMON_DIFF|-4 - 4|-8
  CHECK|difference|-12 - (-4) = -8|-8
  SEQ_FORMULA|a_n = a_1 + (n - 1)d
  SEQ_APPLY|-132 = 4 + (n - 1)·-8
  S|-132|4|-136
  D|-136|-8|17
  A|17|1|18
  Z|18
Answer: 18
```

### Geometric Sequence — `GeometricSequenceGenerator`  ·  high · difficulty 4

Geometric sequences from four shown terms: the nth term, the partial sum (integer ratios), and the infinite sum when |r| < 1.

**Variants:** `geometric_sequence_infinite_sum`, `geometric_sequence_nth_term`, `geometric_sequence_partial_sum`

```
Problem: The geometric sequence -6, -18, -54, -162, ... continues. Find the sum of the first 5 terms.
Steps:
  SEQ_SETUP|-6, -18, -54, -162, ...|sum of first 5 terms
  COMMON_RATIO|-18/(-6)|3
  CHECK|ratio|-54/(-18) = 3|3
  SEQ_FORMULA|S_n = a_1(r^n - 1)/(r - 1)
  SEQ_APPLY|S_5 = -6·(3^5 - 1)/(3 - 1)
  E|3|5|243
  S|243|1|242
  M|-6|242|-1452
  S|3|1|2
  D|-1452|2|-726
  Z|-726
Answer: -726
```

### Recursive Explicit — `RecursiveExplicitGenerator`  ·  high · difficulty 4

Converts between recursive and explicit sequence definitions, both directions, for arithmetic and geometric sequences.

**Variants:** `explicit_to_recursive`, `recursive_to_explicit`

```
Problem: The sequence is defined by a_n = 1·2^(n-1). Write a recursive definition.
Steps:
  SEQ_SETUP|a_n = 1·2^(n-1)|recursive definition
  SUBST|n|1|1·2^0
  E|2|0|1
  M|1|1|1
  EVAL|a_1|1
  SUBST|n|2|1·2^1
  E|2|1|2
  M|1|2|2
  EVAL|a_2|2
  COMMON_RATIO|2/1|2
  REWRITE|a_1 = 1; a_n = 2·a_(n-1)
  CHECK|term 3|explicit 1·2^2 = 4, recursion 2·2 = 4|4
  Z|a_1 = 1; a_n = 2·a_(n-1)
Answer: a_1 = 1; a_n = 2·a_(n-1)
```

### Sigma Notation — `SigmaNotationGenerator`  ·  high · difficulty 4

Expands sigma notation term by term and evaluates the sum for small upper bounds. Lower bounds other than 1 (including 0) appear so the index range itself is exercised.

**Variants:** `sigma_notation_linear`, `sigma_notation_power`, `sigma_notation_square`

```
Problem: Expand and evaluate: Σ_(k=0)^(4) 3k^2.
Steps:
  SIGMA_SETUP|Σ_(k=0)^(4) 3k^2|expand and evaluate
  SIGMA_TERM|k=0|3(0)^2|0
  SIGMA_TERM|k=1|3(1)^2|3
  SIGMA_TERM|k=2|3(2)^2|12
  SIGMA_TERM|k=3|3(3)^2|27
  SIGMA_TERM|k=4|3(4)^2|48
  SIGMA_EXPAND|0 + 3 + 12 + 27 + 48
  A|0|3|3
  A|3|12|15
  A|15|27|42
  A|42|48|90
  Z|90
Answer: 90
```

### Complex Number Ops — `ComplexNumberOpsGenerator`  ·  high · difficulty 4

Complex number arithmetic: powers of i, addition, subtraction, and multiplication.

**Variants:** `complex_add`, `complex_multiply`, `complex_power_i`, `complex_subtract`

```
Problem: Multiply: (5 - 8i)(-1 + 8i).
Steps:
  CX_SETUP|(5 - 8i)(-1 + 8i)|multiply
  FOIL_SETUP|(5 - 8i)(-1 + 8i)
  FOIL_F|First: 5 * (-1)|-5
  FOIL_O|Outer: 5 * 8i|40i
  FOIL_I|Inner: (-8i) * (-1)|8i
  FOIL_L|Last: (-8i) * 8i|-64i^2
  I_SQUARE|-64i^2|64
  A|-5|64|59
  A|40|8|48
  Z|59 + 48i
Answer: 59 + 48i
```

### Complex Division — `ComplexDivisionGenerator`  ·  high · difficulty 5

Divides complex numbers by multiplying numerator and denominator by the conjugate. The numerator is FOILed in full with the i^2 substitution; the denominator uses c^2 + d^2 with both squares computed. Each part of the quotient is reduced to lowest terms.

**Variants:** `complex_division`

```
Problem: Divide: (1 + i)/(-6 - 2i). Give the answer in standard form.
Steps:
  CX_SETUP|(1 + i)/(-6 - 2i)|divide
  CONJUGATE|-6 - 2i|-6 + 2i
  REWRITE|multiply numerator and denominator by -6 + 2i
  FOIL_SETUP|(1 + i)(-6 + 2i)
  FOIL_F|First: 1 * (-6)|-6
  FOIL_O|Outer: 1 * 2i|2i
  FOIL_I|Inner: i * (-6)|-6i
  FOIL_L|Last: i * 2i|2i^2
  I_SQUARE|2i^2|-2
  A|-6|-2|-8
  A|2|-6|-4
  EVAL|numerator|-8 - 4i
  REWRITE|(-6 - 2i)(-6 + 2i) = 6^2 + 2^2
  E|6|2|36
  E|2|2|4
  A|36|4|40
  EVAL|denominator|40
  REWRITE|(-8 - 4i)/40
  FRAC_REDUCE|-8/40|-1/5
  FRAC_REDUCE|-4/40|-1/10
  Z|-1/5 - (1/10)i
Answer: -1/5 - (1/10)i
```

### Complex Quadratic — `ComplexQuadraticGenerator`  ·  high · difficulty 5

Solves monic quadratics with negative discriminant by the quadratic formula, producing complex conjugate roots.

**Variants:** `quadratic_complex_roots`

```
Problem: Solve: x^2 - 12x + 47 = 0.
Steps:
  EQ_SETUP|x^2 - 12x + 47 = 0|solve
  DISC|(-12)^2 - 4(1)(47)|-44
  DISC_CLASSIFY|-44 < 0|two complex conjugate roots
  SQRT_NEG|√(-44)|i√44
  ROOT_SIMPLIFY|2i√11
  Q1|12|2i√11|2|6 + i√11
  Q2|12|2i√11|2|6 - i√11
  Z|x = 6 + i√11 or x = 6 - i√11
Answer: x = 6 + i√11 or x = 6 - i√11
```

### Polynomial Long Division — `PolynomialLongDivisionGenerator`  ·  high · difficulty 5

Polynomial long division: cubic dividend by a linear divisor, the long-division scratchpad in algebra form. The dividend is built as quotient·divisor + remainder, so every DIV_TERM is exact and all dividend coefficients are nonzero.

**Variants:** `polynomial_long_division`

```
Problem: Divide: (2x^3 + 14x^2 + 23x + 16) ÷ (x + 5).
Steps:
  POLYDIV_SETUP|2x^3 + 14x^2 + 23x + 16|x + 5
  DIV_TERM|2x^3|x|2x^2
  MUL_TERM|2x^2|x + 5|2x^3 + 10x^2
  POLY_SUB|(2x^3 + 14x^2) - (2x^3 + 10x^2)|4x^2
  B|23x
  DIV_TERM|4x^2|x|4x
  MUL_TERM|4x|x + 5|4x^2 + 20x
  POLY_SUB|(4x^2 + 23x) - (4x^2 + 20x)|3x
  B|16
  DIV_TERM|3x|x|3
  MUL_TERM|3|x + 5|3x + 15
  POLY_SUB|(3x + 16) - (3x + 15)|1
  R|1
  Z|2x^2 + 4x + 3 + 1/(x + 5)
Answer: 2x^2 + 4x + 3 + 1/(x + 5)
```

### Synthetic Division — `SyntheticDivisionGenerator`  ·  high · difficulty 4

Synthetic division by (x - r): write the coefficient row (with a 0 placeholder for any missing term), bring down the lead, then the multiply-add rhythm across the columns. The bottom row is read back as the quotient and remainder.

**Variants:** `synthetic_division`

```
Problem: Use synthetic division to divide (x^4 - x^3 + 2x^2 - 5x - 8) by (x - 2).
Steps:
  SYNDIV_SETUP|x^4 - x^3 + 2x^2 - 5x - 8|r = 2
  COEFFS|1, -1, 2, -5, -8
  SYN_DROP|1
  M|2|1|2
  A|-1|2|1
  M|2|1|2
  A|2|2|4
  M|2|4|8
  A|-5|8|3
  M|2|3|6
  A|-8|6|-2
  SYN_ROW|1, 1, 4, 3, -2
  REWRITE|x^3 + x^2 + 4x + 3
  R|-2
  Z|x^3 + x^2 + 4x + 3 - 2/(x - 2)
Answer: x^3 + x^2 + 4x + 3 - 2/(x - 2)
```

### Horner Evaluation — `HornerEvaluationGenerator`  ·  high · difficulty 4

Evaluates a polynomial at x = r by Horner's method: write the nested form, then run the multiply-add rhythm across the coefficients. The record closes with a CHECK evaluating one term directly (A1) so the nested result is corroborated.

**Variants:** `horner_evaluation`

```
Problem: Use Horner's method to evaluate P(x) = 2x^3 - x^2 + 3x + 1 at x = 3.
Steps:
  HORNER_SETUP|2x^3 - x^2 + 3x + 1|x = 3
  REWRITE|((2x - 1)x + 3)x + 1
  COEFFS|2, -1, 3, 1
  SYN_DROP|2
  M|3|2|6
  A|6|-1|5
  M|3|5|15
  A|15|3|18
  M|3|18|54
  A|54|1|55
  EVAL|P(3)|55
  CHECK|leading term|2·(3)^3 = 54|54
  Z|55
Answer: 55
```

### Remainder Factor Theorem — `RemainderFactorTheoremGenerator`  ·  high · difficulty 4

Remainder and factor theorems on cubics.

**Variants:** `factor_theorem_check`, `factor_theorem_find_k`, `remainder_theorem`

```
Problem: Is x - 1 a factor of P(x) = x^3 + 3x^2 - 2x - 5?
Steps:
  THEOREM|factor theorem|x - 1 is a factor iff P(1) = 0
  SUBST|x|1|(1)^3 + 3(1)^2 - 2(1) - 5
  E|(1)|3|1
  E|(1)|2|1
  M|3|1|3
  M|-2|1|-2
  A|1|3|4
  A|4|-2|2
  A|2|-5|-3
  EVAL|P(1)|-3
  Z|No
Answer: No
```

### Rational Root — `RationalRootGenerator`  ·  high · difficulty 5

Rational root theorem: list every candidate ±p/q (p dividing the constant, q dividing the leading coefficient), then test candidates in order of size until one gives P = 0 (A2 trial-and-error).

**Variants:** `rational_root_search`

```
Problem: Use the rational root theorem to find a rational root of P(x) = x^3 - x^2 - 12x + 18.
Steps:
  THEOREM|rational root theorem|candidates: ± (divisors of 18) / (divisors of 1)
  CANDIDATES|±1, ±2, ±3, ±6, ±9, ±18
  TRY|x = 1|P(1) = 6
  REJECT|x = 1|P(1) = 6 ≠ 0
  TRY|x = -1|P(-1) = 28
  REJECT|x = -1|P(-1) = 28 ≠ 0
  TRY|x = 2|P(2) = -2
  REJECT|x = 2|P(2) = -2 ≠ 0
  TRY|x = -2|P(-2) = 30
  REJECT|x = -2|P(-2) = 30 ≠ 0
  TRY|x = 3|P(3) = 0
  ACCEPT|x = 3|P(3) = 0
  Z|x = 3
Answer: x = 3
```

### Polynomial Zeros — `PolynomialZerosGenerator`  ·  high · difficulty 5

Finds all zeros of a monic cubic from one given zero: synthetic division deflates to a quadratic (the R = 0 cell confirms the given zero), then the quadratic is finished off.

**Variants:** `polynomial_all_zeros`

```
Problem: Given that x = 1 is a zero, find all zeros of P(x) = x^3 - 3x^2 - x + 3.
Steps:
  EQ_SETUP|x^3 - 3x^2 - x + 3 = 0|find all zeros; given x = 1
  SYNDIV_SETUP|x^3 - 3x^2 - x + 3|r = 1
  COEFFS|1, -3, -1, 3
  SYN_DROP|1
  M|1|1|1
  A|-3|1|-2
  M|1|-2|-2
  A|-1|-2|-3
  M|1|-3|-3
  A|3|-3|0
  SYN_ROW|1, -2, -3, 0
  R|0
  REWRITE|x^2 - 2x - 3 = 0
  FACTOR_PAIR_GOAL|m·n = -3|m + n = -2
  TRY|(1, -3)|1·(-3)=-3, 1+(-3)=-2
  ACCEPT|(1, -3)|product -3 ✓, sum -2 ✓
  REWRITE|(x + 1)(x - 3) = 0
  ZERO_PRODUCT|(x + 1)(x - 3) = 0|x + 1 = 0 or x - 3 = 0
  Z|x = -1, x = 1, x = 3
Answer: x = -1, x = 1, x = 3
```

### Rational Function Features — `RationalFunctionFeaturesGenerator`  ·  high · difficulty 4

Reads the features of a rational function by hand: factor top and bottom, cancel a shared factor into a hole, the remaining denominator zeros become vertical asymptotes, and the horizontal asymptote comes from comparing degrees.

**Variants:** `rational_function_features`

```
Problem: Find the vertical asymptotes, holes, and horizontal asymptote of g(x) = (x^2 + x - 2)/(x^2 - x - 6).
Steps:
  FUNC_SETUP|g(x) = (x^2 + x - 2)/(x^2 - x - 6)|asymptotes and holes
  FACTOR_PAIR_GOAL|m·n = -2|m + n = 1
  TRY|(-1, 2)|(-1)·2=-2, (-1)+2=1
  ACCEPT|(-1, 2)|product -2 ✓, sum 1 ✓
  REWRITE|numerator = (x - 1)(x + 2)
  FACTOR_PAIR_GOAL|m·n = -6|m + n = -1
  TRY|(1, -6)|1·(-6)=-6, 1+(-6)=-5
  REJECT|(1, -6)|sum is -5, need -1
  TRY|(2, -3)|2·(-3)=-6, 2+(-3)=-1
  ACCEPT|(2, -3)|product -6 ✓, sum -1 ✓
  REWRITE|denominator = (x + 2)(x - 3)
  CANCEL|(x + 2)|(x - 1)/(x - 3)
  HOLE|x = -2
  VA|x = 3
  DEGREE_COMPARE|deg num = deg den = 2|y = 1/1
  HA|y = 1
  Z|VA: x = 3; hole at x = -2; HA: y = 1
Answer: VA: x = 3; hole at x = -2; HA: y = 1
```

### Exponential Model — `ExponentialModelGenerator`  ·  high · difficulty 4

Exponential models kept exact by hand: compound growth and decay with terminating-decimal bases, half-life as literal repeated halving, and continuous compounding left in exact Pe^rt form.

**Variants:** `exponential_continuous`, `exponential_decay`, `exponential_growth`, `exponential_half_life`

```
Problem: An investment of $2000 earns 5% interest compounded continuously. Give its exact value in dollars after 2 years.
Steps:
  MODEL|A = Pe^(rt)
  PERCENT_TO_DEC|5%|0.05
  M|0.05|2|0.1
  MODEL_APPLY|A = 2000e^0.1
  Z|2000e^0.1
Answer: 2000e^0.1
```

### Log Conversion — `LogConversionGenerator`  ·  high · difficulty 4

Exponential <-> logarithmic form, evaluating logs by asking 'the base to what power?', change of base, and the ln identities.

**Variants:** `log_change_of_base`, `log_evaluate`, `log_exp_to_log`, `log_ln_identity`, `log_log_to_exp`

```
Problem: Use the change of base formula to evaluate log_27(81).
Steps:
  CHANGE_BASE|log_27(81) = log_3(81)/log_3(27)
  E|3|4|81
  EVAL|log_3(81)|4
  E|3|3|27
  EVAL|log_3(27)|3
  D|4|3|4/3
  Z|4/3
Answer: 4/3
```

### Log Properties — `LogPropertiesGenerator`  ·  high · difficulty 4

Log properties: expand a single log into a sum, or condense a sum into a single log, using the product, quotient, and power rules - each rule application is its own step. Numeric factors b^k are evaluated with the power shown.

**Variants:** `log_condense`, `log_expand`

```
Problem: Write as a single logarithm: 4log_10(x) + 4log_10(y) - 3log_10(z).
Steps:
  LOG_SETUP|4log_10(x) + 4log_10(y) - 3log_10(z)|condense
  LOG_POWER|4log_10(x)|log_10(x^4)
  LOG_POWER|4log_10(y)|log_10(y^4)
  LOG_POWER|3log_10(z)|log_10(z^3)
  LOG_PRODUCT|log_10(x^4) + log_10(y^4)|log_10(x^4y^4)
  LOG_QUOTIENT|log_10(x^4y^4) - log_10(z^3)|log_10(x^4y^4/z^3)
  Z|log_10(x^4y^4/z^3)
Answer: log_10(x^4y^4/z^3)
```

### Exponential Equation — `ExponentialEquationGenerator`  ·  high · difficulty 5

Solves exponential equations: by matching bases when the right side is a power of the base (equate exponents, solve the linear), and by taking logs when it is not (the answer stays exact, e.g. x = log_5(17) or x = ln(10)/2).

**Variants:** `exponential_eq_common_base`, `exponential_eq_ln`, `exponential_eq_log`, `exponential_eq_same_base`

```
Problem: Solve: e^(4x) = 7. Give the exact answer.
Steps:
  EQ_SETUP|e^(4x) = 7|solve; exact answer
  LOG_BOTH_SIDES|ln(e^(4x)) = ln(7)
  LOG_IDENT|ln(e^(4x)) = 4x|4x
  EQ_OP_BOTH|divide|4|x|ln(7)/4
  Z|x = ln(7)/4
Answer: x = ln(7)/4
```

### Log Equation — `LogEquationGenerator`  ·  high · difficulty 5

Solves logarithmic equations with an explicit domain check on every candidate - the extraneous-solution trap is the point (A1).

**Variants:** `log_eq_basic`, `log_eq_both_sides`, `log_eq_product`

```
Problem: Solve: log_3(x) + log_3(x + 6) = 3.
Steps:
  EQ_SETUP|log_3(x) + log_3(x + 6) = 3|solve
  DOMAIN_NOTE|x > 0 and x + 6 > 0|arguments must be positive
  LOG_PRODUCT|log_3(x) + log_3(x + 6)|log_3(x(x + 6))
  LOG_FORM|log_3(x(x + 6)) = 3 ⟺ x(x + 6) = 3^3
  E|3|3|27
  REWRITE|x^2 + 6x - 27 = 0
  FACTOR_PAIR_GOAL|m·n = -27|m + n = 6
  TRY|(-1, 27)|(-1)·27=-27, (-1)+27=26
  REJECT|(-1, 27)|sum is 26, need 6
  TRY|(-3, 9)|(-3)·9=-27, (-3)+9=6
  ACCEPT|(-3, 9)|product -27 ✓, sum 6 ✓
  REWRITE|(x - 3)(x + 9) = 0
  ZERO_PRODUCT|(x - 3)(x + 9) = 0|x - 3 = 0 or x + 9 = 0
  TRY|x = 3|arguments 3 > 0 and 9 > 0
  ACCEPT|x = 3|both logs defined
  TRY|x = -9|log_3(-9) undefined
  REJECT|x = -9|argument negative, extraneous
  Z|x = 3
Answer: x = 3
```

### Parabola Features — `ParabolaFeaturesGenerator`  ·  high · difficulty 5

Vertex, focus, and directrix from the standard form of a parabola: identify the form and orientation, solve 4p, then shift from the vertex with explicit coordinate arithmetic.

**Variants:** `parabola_features`

```
Problem: Find the vertex, focus, and directrix of (x + 6)^2 = 8(y + 2).
Steps:
  CONIC_SETUP|(x + 6)^2 = 8(y + 2)|vertex, focus, directrix
  FORM_IDENTIFY|(x - h)^2 = 4p(y - k)|vertical parabola, opens up
  D|8|4|2
  EVAL|p|2
  VERTEX|(-6, -2)
  A|-2|2|0
  FOCUS|(-6, 0)
  S|-2|2|-4
  DIRECTRIX|y = -4
  Z|vertex (-6, -2); focus (-6, 0); directrix y = -4
Answer: vertex (-6, -2); focus (-6, 0); directrix y = -4
```

### Ellipse Features — `EllipseFeaturesGenerator`  ·  high · difficulty 5

Center, vertices, and foci of an ellipse in standard form. The larger denominator names the major axis; c^2 = a^2 - b^2 is computed explicitly, with integer c from Pythagorean triples and exact √ forms otherwise.

**Variants:** `ellipse_features`

```
Problem: Find the center, vertices, and foci of the ellipse x^2/4 + (y - 6)^2/9 = 1.
Steps:
  CONIC_SETUP|x^2/4 + (y - 6)^2/9 = 1|center, vertices, foci
  FORM_IDENTIFY|(x - h)^2/a^2 + (y - k)^2/b^2 = 1 (ellipse)|major axis vertical (9 > 4)
  CENTER|(0, 6)
  E|3|2|9
  EVAL|a|3
  E|2|2|4
  EVAL|b|2
  S|6|3|3
  A|6|3|9
  VERTEX|(0, 3)
  VERTEX|(0, 9)
  S|9|4|5
  EVAL|c^2|5
  EVAL|c|√5
  FOCUS|(0, 6 - √5)
  FOCUS|(0, 6 + √5)
  Z|center (0, 6); vertices (0, 3) and (0, 9); foci (0, 6 - √5) and (0, 6 + √5)
Answer: center (0, 6); vertices (0, 3) and (0, 9); foci (0, 6 - √5) and (0, 6 + √5)
```

### Hyperbola Features — `HyperbolaFeaturesGenerator`  ·  high · difficulty 5

Center, vertices, foci, and asymptotes of a hyperbola in standard form. The positive term names the transverse axis; c^2 = a^2 + b^2 (the plus is the classic contrast with the ellipse), and the asymptote slope is reduced to lowest terms.

**Variants:** `hyperbola_features`

```
Problem: Find the center, vertices, foci, and asymptotes of the hyperbola (y - 6)^2/1 - x^2/9 = 1.
Steps:
  CONIC_SETUP|(y - 6)^2/1 - x^2/9 = 1|center, vertices, foci, asymptotes
  FORM_IDENTIFY|hyperbola in standard form|opens up-down (y term positive)
  CENTER|(0, 6)
  E|1|2|1
  EVAL|a|1
  E|3|2|9
  EVAL|b|3
  S|6|1|5
  A|6|1|7
  VERTEX|(0, 5)
  VERTEX|(0, 7)
  A|1|9|10
  EVAL|c^2|10
  EVAL|c|√10
  FOCUS|(0, 6 - √10)
  FOCUS|(0, 6 + √10)
  ASYMPTOTE|y = 6 ± (1/3)x
  Z|center (0, 6); vertices (0, 5) and (0, 7); foci (0, 6 - √10) and (0, 6 + √10); asymptotes y = 6 ± (1/3)x
Answer: center (0, 6); vertices (0, 5) and (0, 7); foci (0, 6 - √10) and (0, 6 + √10); asymptotes y = 6 ± (1/3)x
```

### Conic Standard Form — `ConicStandardFormGenerator`  ·  high · difficulty 5

General form -> standard form by completing the square.

**Variants:** `conic_standard_form_circle`, `conic_standard_form_ellipse`

```
Problem: Write in standard form: 4x^2 + 25y^2 - 8x - 200y + 304 = 0.
Steps:
  CONIC_SETUP|4x^2 + 25y^2 - 8x - 200y + 304 = 0|standard form
  MOVE_TERM|constant to the right|4x^2 - 8x + 25y^2 - 200y = -304
  FACTOR_GROUP|4x^2 - 8x|4|(x^2 - 2x)
  FACTOR_GROUP|25y^2 - 200y|25|(y^2 - 8y)
  COMPLETE_SQUARE|half of -2 = -1|(-1)^2 = 1
  M|4|1|4
  COMPLETE_SQUARE|half of -8 = -4|(-4)^2 = 16
  M|25|16|400
  A|-304|4|-300
  A|-300|400|100
  REWRITE|4(x - 1)^2 + 25(y - 4)^2 = 100
  D|100|4|25
  D|100|25|4
  REWRITE|(x - 1)^2/25 + (y - 4)^2/4 = 1
  FORM_IDENTIFY|ellipse|center (1, 4)
  Z|(x - 1)^2/25 + (y - 4)^2/4 = 1
Answer: (x - 1)^2/25 + (y - 4)^2/4 = 1
```

### Regular Polygon Area — `RegularPolygonAreaGenerator`  ·  high · difficulty 4

Area of a regular polygon from its apothem: A = (1/2)·a·P. The perimeter is computed first, then the product, then the halving. The given apothem is the true value rounded to the nearest half so the numbers stay realistic for the named polygon.

**Variants:** `regular_polygon_area`

```
Problem: A regular octagon has side length 10 and apothem 12. Find its area.
Steps:
  POLY_SETUP|regular octagon: n = 8, side 10, apothem 12|area
  POLY_FORMULA|A = (1/2)·a·P
  M|8|10|80
  EVAL|P|80
  M|12|80|960
  D|960|2|480
  Z|480 square units
Answer: 480 square units
```

### Similar Triangles — `SimilarTrianglesGenerator`  ·  high · difficulty 4

Similar triangles: set up the ratio of corresponding sides, cross multiply, and solve for the missing side. A CHECK confirms the scale factor agrees on both known pairs (A1).

**Variants:** `similar_triangles`

```
Problem: Triangle ABC is similar to triangle DEF, with AB = 15, DE = 35, BC = 15. Find EF.
Steps:
  SIM_SETUP|△ABC ~ △DEF; AB = 15, DE = 35, BC = 15|find EF
  PROP_SETUP|15/35 = 15/EF
  CROSS_MULT|15·EF = 35·15
  M|35|15|525
  D|525|15|35
  CHECK|scale factor|35/15 = 7/3, 35/15 = 7/3|7/3
  Z|EF = 35
Answer: EF = 35
```

### Geometric Mean — `GeometricMeanGenerator`  ·  high · difficulty 4

Geometric mean relationships in a right triangle with the altitude drawn to the hypotenuse: h = √(p·q), leg = √(p·c), and the reverse solve q = h²/p. Radical answers are simplified.

**Variants:** `geometric_mean_altitude`, `geometric_mean_find_segment`, `geometric_mean_leg`

```
Problem: In a right triangle, the altitude to the hypotenuse splits it into segments p = 8 and q = 2. Find the leg adjacent to the segment of length 8.
Steps:
  GEO_SETUP|right triangle, altitude to hypotenuse; segments p = 8 (adjacent to the leg) and q = 2|the leg adjacent to p
  A|8|2|10
  THEOREM|geometric mean (leg)|leg = √(p·c)
  M|8|10|80
  ROOT_SIMPLIFY|√80 = 4√5
  Z|leg = 4√5
Answer: leg = 4√5
```

### Distance Formula — `DistanceFormulaGenerator`  ·  high · difficulty 3

Distance between two points: state the formula, compute both differences, square them (negatives parenthesized), add, and simplify the root. Pythagorean pairs give integers; other pairs give simplified radicals.

**Variants:** `distance_formula`

```
Problem: Find the distance between (3, 4) and (-8, -1).
Steps:
  DIST_FORMULA|d = √((x2 - x1)^2 + (y2 - y1)^2)
  S|-8|3|-11
  S|-1|4|-5
  E|(-11)|2|121
  E|(-5)|2|25
  A|121|25|146
  ROOT_SIMPLIFY|√146 = √146
  Z|d = √146
Answer: d = √146
```

### Midpoint — `MidpointGenerator`  ·  high · difficulty 3

Midpoint of a segment, both directions: - midpoint: average the coordinates (parities matched so the midpoint is a lattice point) - endpoint: given one endpoint and the midpoint, double back to the missing endpoint

**Variants:** `midpoint_endpoint`, `midpoint_midpoint`

```
Problem: The midpoint of a segment is (5, -7) and one endpoint is (8, -9). Find the other endpoint.
Steps:
  MID_FORMULA|M = ((x1 + x2)/2, (y1 + y2)/2)
  REWRITE|x2 = 2·mx - x1; y2 = 2·my - y1
  M|2|5|10
  S|10|8|2
  M|2|-7|-14
  S|-14|-9|-5
  Z|(2, -5)
Answer: (2, -5)
```

### Segment Partition — `SegmentPartitionGenerator`  ·  high · difficulty 4

Partition a segment in a given ratio m:n from the first endpoint: P = A + (m/(m+n))·(B - A), each coordinate worked as difference, scaled fraction, then shift. Differences are divisible by m + n by construction, so every step stays in integers.

**Variants:** `segment_partition`

```
Problem: Point P divides the segment from A(-7, 0) to B(25, 24) in the ratio 4:4 (measured from A). Find P.
Steps:
  SECTION_SETUP|A(-7, 0), B(25, 24); ratio 4:4 from A|point P
  SECTION_FORMULA|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))
  A|4|4|8
  S|25|-7|32
  M|4|32|128
  D|128|8|16
  A|-7|16|9
  S|24|0|24
  M|4|24|96
  D|96|8|12
  A|0|12|12
  Z|(9, 12)
Answer: (9, 12)
```

### Transformation — `TransformationGenerator`  ·  high · difficulty 3

Coordinate-rule transformations of a point: translations, reflections (axes and y = x), rotations about the origin (90/180/270 CCW), dilations, and two-step compositions applied in order. Each transform states its rule before applying it; translations and dilations show the arithmetic.

**Variants:** `transformation_composition`, `transformation_single`

```
Problem: Find the image of P(5, 6) under a rotation 90° counterclockwise about the origin followed by a reflection over the line y = x.
Steps:
  TRANSFORM_SETUP|P(5, 6)|rotation 90° counterclockwise about the origin, then reflection over the line y = x
  TRANSFORM_RULE|(x, y) → (-y, x)
  TRANSFORM_APPLY|(-(6), (5))|(-6, 5)
  TRANSFORM_RULE|(x, y) → (y, x)
  TRANSFORM_APPLY|((5), (-6))|(5, -6)
  Z|(5, -6)
Answer: (5, -6)
```

### Arc Sector — `ArcSectorGenerator`  ·  high · difficulty 4

Arc length and sector area, kept exact in terms of π: reduce the angle fraction θ/360 first, then apply it to 2πr or πr².

**Variants:** `arc_measure`, `sector_measure`

```
Problem: A circle has radius 8. Find the area of the sector with central angle 30°. Give the exact answer in terms of π.
Steps:
  ARC_SETUP|circle r = 8, central angle 30°|sector area
  SECTOR_FORMULA|A = (θ/360)·πr^2
  FRAC_REDUCE|30/360|1/12
  E|8|2|64
  M|1/12|64|16/3
  Z|16π/3
Answer: 16π/3
```

### Circle Angle — `CircleAngleGenerator`  ·  high · difficulty 4

Central and inscribed angle relationships: an inscribed angle is half the central angle (equivalently half the intercepted arc), and an angle inscribed in a semicircle is right (Thales).

**Variants:** `circle_angle_arc_from_inscribed`, `circle_angle_central_from_inscribed`, `circle_angle_inscribed_from_central`, `circle_angle_semicircle`

```
Problem: A triangle is inscribed in a circle with one side a diameter. One of its acute angles measures 63°. Find the other acute angle.
Steps:
  CIRCLE_ANGLE_SETUP|triangle inscribed in a circle with one side a diameter; one acute angle is 63°|the other acute angle
  THEOREM|Thales|the angle opposite the diameter is 90°
  S|90|63|27
  Z|27°
Answer: 27°
```

### Circle Equation — `CircleEquationGenerator`  ·  high · difficulty 5

Equation of a circle in standard form, from three kinds of given information. (The general-form-to-standard direction lives in ConicStandardFormGenerator.)

**Variants:** `circle_equation_center_point`, `circle_equation_center_radius`, `circle_equation_diameter`

```
Problem: Write the equation of the circle with center (6, 0) that passes through (0, -2).
Steps:
  CIRCLE_SETUP|center (6, 0), passes through (0, -2)|equation of the circle
  S|0|6|-6
  S|-2|0|-2
  E|(-6)|2|36
  E|(-2)|2|4
  A|36|4|40
  EVAL|r^2|40
  REWRITE|(x - 6)^2 + y^2 = 40
  Z|(x - 6)^2 + y^2 = 40
Answer: (x - 6)^2 + y^2 = 40
```

### Hypercube Counting — `HypercubeCountingGenerator`  ·  high · difficulty 4

Counting the pieces of an n-cube and measuring in R^4.

**Variants:** `hypercube_count`, `hypercube_diagonal`, `hypercube_distance4d`

```
Problem: Find the distance between P(1, -5, -1, 3) and Q(2, 1, -1, 2) in 4-dimensional space.
Steps:
  HYPERCUBE_SETUP|points P(1, -5, -1, 3) and Q(2, 1, -1, 2) in R^4|distance
  DIST_FORMULA|d = √(Σ (q_i - p_i)^2), four coordinates
  S|2|1|1
  E|1|2|1
  S|1|-5|6
  E|6|2|36
  S|-1|-1|0
  E|0|2|0
  S|2|3|-1
  E|(-1)|2|1
  A|1|36|37
  A|37|0|37
  A|37|1|38
  ROOT_SIMPLIFY|√38 = √38
  Z|d = √38
Answer: d = √38
```

### Right Triangle Trig — `RightTriangleTrigGenerator`  ·  high · difficulty 4

SOH-CAH-TOA with every needed trig value supplied in the problem (Principle 5 - no calculator).

**Variants:** `right_triangle_trig_find_angle`, `right_triangle_trig_find_side`, `right_triangle_trig_write_ratio`

```
Problem: In a right triangle, one acute angle measures 24° and the hypotenuse is 10. Given that sin 24° ≈ 0.4, find the opposite side.
Steps:
  TRIG_SETUP|right triangle, angle 24°, hypotenuse = 10; given sin 24° ≈ 0.4|the opposite side
  TRIG_RATIO|sin|opposite/hypotenuse
  REWRITE|x/10 = 0.4
  M|10|0.4|4
  Z|4
Answer: 4
```

### Special Right Triangle — `SpecialRightTriangleGenerator`  ·  high · difficulty 4

30-60-90 and 45-45-90 triangles by their side ratios, every direction, with the rationalizing step shown when dividing by √2.

**Variants:** `special_right_triangle_30_from_hyp`, `special_right_triangle_30_from_long`, `special_right_triangle_30_from_short`, `special_right_triangle_45_from_hyp`, `special_right_triangle_45_from_leg`

```
Problem: The hypotenuse of a 30-60-90 triangle is 16. Find both legs. Give exact answers.
Steps:
  TRI_SETUP|30-60-90 triangle, hypotenuse = 16|both legs
  THEOREM|30-60-90 ratios|short : long : hypotenuse = 1 : √3 : 2
  D|16|2|8
  REWRITE|longer leg = 8√3
  Z|shorter leg = 8; longer leg = 8√3
Answer: shorter leg = 8; longer leg = 8√3
```

### Angle Measure — `AngleMeasureGenerator`  ·  high · difficulty 4

Angle measure conversions and normalizations: degrees to exact radian fractions of π and back, coterminal angles brought into [0°, 360°) by whole turns, and reference angles by quadrant rule.

**Variants:** `angle_coterminal`, `angle_deg_to_rad`, `angle_rad_to_deg`, `angle_reference`

```
Problem: Find the reference angle of 350°.
Steps:
  QUADRANT|350°|quadrant IV
  ANGLE_FORMULA|quadrant IV: reference = 360° - θ
  S|360|350|10
  Z|10°
Answer: 10°
```

### Unit Circle — `UnitCircleGenerator`  ·  high · difficulty 4

Exact unit-circle values and inverse trig, worked the way the unit circle is taught: quadrant, reference angle, sign rule, table value. Quadrantal angles read straight off the circle point. Radian inputs convert to degrees first.

**Variants:** `unit_circle_evaluate`, `unit_circle_inverse`

```
Problem: Evaluate arccos(-1). Give the answer in degrees.
Steps:
  TRIG_SETUP|arccos(-1)|angle in degrees
  DOMAIN_NOTE|arccos range|[0°, 180°]
  TABLE_LOOKUP|cos 0°|1
  SIGN_RULE|arccos of a negative|second-quadrant angle
  S|180|0|180
  Z|180°
Answer: 180°
```

### Sinusoid Features — `SinusoidFeaturesGenerator`  ·  high · difficulty 4

Amplitude, period, phase shift, and midline from a sinusoid equation. The unfactored form A·cos(Bx - φ) forces the classic factor-out step: the phase shift is φ/B, not φ.

**Variants:** `sinusoid_features_factored`, `sinusoid_features_radians`, `sinusoid_features_unfactored`

```
Problem: State the amplitude, period, phase shift, and midline of y = 2sin(6x - 120°) - 2.
Steps:
  SINUSOID_SETUP|y = 2sin(6x - 120°) - 2|amplitude, period, phase shift, midline
  AMPLITUDE|abs(2)|2
  D|360|6|60
  PERIOD|60°
  REWRITE|6x - 120° = 6(x - 20°)
  D|120|6|20
  PHASE_SHIFT|20° right
  MIDLINE|y = -2
  Z|amplitude 2; period 60°; phase shift 20° right; midline y = -2
Answer: amplitude 2; period 60°; phase shift 20° right; midline y = -2
```

### Trig Six Functions — `TrigSixFunctionsGenerator`  ·  high · difficulty 4

All six trig functions from one given ratio and a quadrant. The missing side comes from the Pythagorean identity (or the hypotenuse from the two legs when tangent is given), the sign of each derived function comes from the quadrant, and the three reciprocals are flipped explicitly.

**Variants:** `trig_six_given_cos`, `trig_six_given_sin`, `trig_six_given_tan`

```
Problem: Given cos θ = 7/25 with θ in quadrant IV, find all six trigonometric functions of θ.
Steps:
  TRIG_SETUP|cos θ = 7/25, θ in quadrant IV|all six trig functions
  THEOREM|Pythagorean identity|sin^2 θ + cos^2 θ = 1
  E|7/25|2|49/625
  S|1|49/625|576/625
  REWRITE|sin θ = ±24/25
  SIGN_RULE|sin, quadrant IV|negative
  EVAL|sin θ|-24/25
  D|-24/25|7/25|-24/7
  EVAL|tan θ|-24/7
  RECIPROCAL|csc θ = 1/sin θ|-25/24
  RECIPROCAL|sec θ = 1/cos θ|25/7
  RECIPROCAL|cot θ = 1/tan θ|-7/24
  Z|sin θ = -24/25; cos θ = 7/25; tan θ = -24/7; csc θ = -25/24; sec θ = 25/7; cot θ = -7/24
Answer: sin θ = -24/25; cos θ = 7/25; tan θ = -24/7; csc θ = -25/24; sec θ = 25/7; cot θ = -7/24
```

### Trig Identity Eval — `TrigIdentityEvalGenerator`  ·  high · difficulty 5

Exact evaluations through identities.

**Variants:** `trig_identity_double`, `trig_identity_half`, `trig_identity_sum_diff`

```
Problem: Given sin θ = -24/25 with θ in quadrant IV, find sin 2θ and cos 2θ.
Steps:
  TRIG_SETUP|sin θ = -24/25, θ in quadrant IV|sin 2θ and cos 2θ
  THEOREM|Pythagorean identity|cos θ = ±7/25
  SIGN_RULE|cos, quadrant IV|positive
  EVAL|cos θ|7/25
  THEOREM|double angle|sin 2θ = 2 sin θ cos θ
  M|2|-24/25|-48/25
  M|-48/25|7/25|-336/625
  EVAL|sin 2θ|-336/625
  THEOREM|double angle|cos 2θ = 1 - 2 sin^2 θ
  E|-24/25|2|576/625
  M|2|576/625|1152/625
  S|1|1152/625|-527/625
  EVAL|cos 2θ|-527/625
  Z|sin 2θ = -336/625; cos 2θ = -527/625
Answer: sin 2θ = -336/625; cos 2θ = -527/625
```

### Trig Identity Verify — `TrigIdentityVerifyGenerator`  ·  high · difficulty 5

Verifies trig identities along a canonical transformation path: start from the more complex side, substitute known identities, simplify, and close with an explicit match of both sides. The final answer is always 'Identity verified' (A0 for this format).

**Variants:** `trig_identity_verify`

```
Problem: Verify the identity: cos A · cot A = csc A - sin A.
Steps:
  IDENTITY_SETUP|verify: cos A · cot A = csc A - sin A|transform the right side
  IDENT_SUB|csc A = 1/sin A
  REWRITE|(1 - sin^2 A)/sin A
  IDENT_SUB|1 - sin^2 A = cos^2 A
  REWRITE|cos^2 A/sin A
  REWRITE|cos A · (cos A/sin A)
  IDENT_SUB|cos A/sin A = cot A
  IDENT_MATCH|cos A · cot A = cos A · cot A
  Z|Identity verified
Answer: Identity verified
```

### Trig Equation — `TrigEquationGenerator`  ·  high · difficulty 5

Trig equations over [0°, 360°).

**Variants:** `trig_equation_linear`, `trig_equation_quadratic`

```
Problem: Solve 2cos^2 x - cos x - 1 = 0 for 0° ≤ x < 360°.
Steps:
  EQ_SETUP|2cos^2 x - cos x - 1 = 0|solve on [0°, 360°)
  SUBST|u|cos x|2u^2 - u - 1 = 0
  REWRITE|(2cos x + 1)(cos x - 1) = 0
  ZERO_PRODUCT|(2cos x + 1)(cos x - 1) = 0|cos x = -1/2 or cos x = 1
  TABLE_LOOKUP|cos reference for 1/2|60°
  SIGN_RULE|cos negative|quadrants II and III
  SOLUTIONS|cos x = -1/2|120°, 240°
  SOLUTIONS|cos x = 1|0°
  Z|x = 0°, 120°, 240°
Answer: x = 0°, 120°, 240°
```

### Triangle Solve — `TriangleSolveGenerator`  ·  high · difficulty 5

Law of Sines and Law of Cosines with every trig value given in the problem and integer results by construction. The SSA ambiguous case is excluded (AAS only for the sine law).

**Variants:** `triangle_solve_cosines_angle`, `triangle_solve_cosines_side`, `triangle_solve_sines_aas`

```
Problem: In triangle ABC, a = 4, b = 5, and the included angle C = 37°. Given cos 37° = 0.8, find side c.
Steps:
  TRI_SETUP|a = 4, b = 5, C = 37°; given cos 37° = 0.8|side c
  THEOREM|law of cosines|c^2 = a^2 + b^2 - 2ab cos C
  E|4|2|16
  E|5|2|25
  A|16|25|41
  M|2|4|8
  M|8|5|40
  M|40|0.8|32
  S|41|32|9
  E|3|2|9
  EVAL|c|3
  Z|c = 3
Answer: c = 3
```

### Triangle Area SAS — `TriangleAreaSASGenerator`  ·  high · difficulty 4

Triangle area from two sides and the included angle: Area = (1/2)·a·b·sin C, with the sine value given in the problem (Principle 5) and the product kept exact. Obtuse included angles (150°) appear so the formula is seen to work past 90°.

**Variants:** `triangle_area_sas`

```
Problem: A triangle has sides a = 9 and b = 3 with included angle C = 90°. Given sin 90° = 1, find its area.
Steps:
  TRI_SETUP|a = 9, b = 3, included angle C = 90°; given sin 90° = 1|area
  TRI_AREA_FORMULA|Area = (1/2)·a·b·sin C
  M|9|3|27
  M|27|1|27
  D|27|2|13.5
  Z|13.5 square units
Answer: 13.5 square units
```

### Polar Parametric — `PolarParametricGenerator`  ·  high · difficulty 5

Polar <-> rectangular for points and equations, and parametric -> rectangular elimination.

**Variants:** `parametric_to_rect`, `polar_eq_to_rect`, `polar_to_rect_point`, `rect_to_polar_point`

```
Problem: Eliminate the parameter: x = 8 cos t, y = 8 sin t.
Steps:
  PARAM_SETUP|x = 8 cos t, y = 8 sin t|eliminate t
  THEOREM|Pythagorean identity|cos^2 t + sin^2 t = 1
  REWRITE|(x/8)^2 + (y/8)^2 = 1
  E|8|2|64
  REWRITE|x^2 + y^2 = 64
  Z|x^2 + y^2 = 64
Answer: x^2 + y^2 = 64
```

### Vector Ops — `VectorOpsGenerator`  ·  high · difficulty 4

Vector arithmetic in components: linear combinations a·u + b·v worked component by component, magnitudes via the root of the sum of squares, and unit vectors from Pythagorean-triple vectors so the components come out as exact fractions.

**Variants:** `vector_combine`, `vector_magnitude`, `vector_unit_vector`

```
Problem: Find the magnitude of v = ⟨-1, -7⟩. Give an exact answer.
Steps:
  VEC_SETUP|v = ⟨-1, -7⟩|magnitude
  MAG_FORMULA|magnitude = √(x^2 + y^2)
  E|(-1)|2|1
  E|(-7)|2|49
  A|1|49|50
  ROOT_SIMPLIFY|√50 = 5√2
  Z|5√2
Answer: 5√2
```

### Dot Product — `DotProductGenerator`  ·  high · difficulty 4

Dot products and angles between vectors.

**Variants:** `dot_product_angle`, `dot_product_dot`, `dot_product_perp`

```
Problem: Are u = ⟨1, -6⟩ and v = ⟨-6, -1⟩ perpendicular?
Steps:
  VEC_SETUP|u = ⟨1, -6⟩, v = ⟨-6, -1⟩|perpendicular?
  DOT_FORMULA|u ⊥ v exactly when u·v = 0
  M|1|-6|-6
  M|-6|-1|6
  A|-6|6|0
  EVAL|u·v|0
  Z|Yes
Answer: Yes
```

### Matrix Ops — `MatrixOpsGenerator`  ·  high · difficulty 4

Matrix arithmetic with every entry's work shown.

**Variants:** `matrix_add_sub`, `matrix_multiply`, `matrix_multiply_vector`, `matrix_scalar`

```
Problem: Given A = [[1, -5], [-1, 3]] and v = [[2], [1]], compute Av. Show the row-by-column work.
Steps:
  MAT_SETUP|A = [[1, -5], [-1, 3]], v = [[2], [1]]|Av
  M|1|2|2
  M|-5|1|-5
  A|2|-5|-3
  MAT_ENTRY|(1,1)|-3
  M|-1|2|-2
  M|3|1|3
  A|-2|3|1
  MAT_ENTRY|(2,1)|1
  Z|[[-3], [1]]
Answer: [[-3], [1]]
```

### Determinant — `DeterminantGenerator`  ·  high · difficulty 4

Determinants: 2×2 directly (ad - bc), 3×3 by cofactor expansion along the first row with each 2×2 minor worked in full and the alternating signs applied in the combining chain.

**Variants:** `determinant_three`, `determinant_two`

```
Problem: Find the determinant of A = [[2, -4, 0], [4, 3, 2], [0, 3, 1]] by cofactor expansion along the first row.
Steps:
  MAT_SETUP|A = [[2, -4, 0], [4, 3, 2], [0, 3, 1]]|det(A) by cofactor expansion along row 1
  DET_FORMULA|det = a11·M11 - a12·M12 + a13·M13
  COFACTOR|(1,1) sign +|minor [[3, 2], [3, 1]]
  M|3|1|3
  M|2|3|6
  S|3|6|-3
  M|2|-3|-6
  EVAL|term 1|-6
  COFACTOR|(1,2) sign -|minor [[4, 2], [0, 1]]
  M|4|1|4
  M|2|0|0
  S|4|0|4
  M|-4|4|-16
  EVAL|term 2|-16
  COFACTOR|(1,3) sign +|minor [[4, 3], [0, 3]]
  M|4|3|12
  M|3|0|0
  S|12|0|12
  M|0|12|0
  EVAL|term 3|0
  S|-6|-16|10
  A|10|0|10
  Z|10
Answer: 10
```

### Matrix Inverse — `MatrixInverseGenerator`  ·  high · difficulty 4

Inverse of a 2×2 matrix by the adjugate formula: compute the determinant, check invertibility, swap/negate, then divide each entry. Unimodular matrices give integer inverses; general ones give exact fractions; singular matrices are detected and refused.

**Variants:** `matrix_inverse_general`, `matrix_inverse_singular`, `matrix_inverse_unimodular`

```
Problem: Find the inverse of A = [[6, 0], [-6, -2]], if it exists.
Steps:
  MAT_SETUP|A = [[6, 0], [-6, -2]]|A⁻¹
  DET_FORMULA|det = ad - bc
  M|6|-2|-12
  M|0|-6|0
  S|-12|0|-12
  EVAL|det|-12
  CHECK|invertible|det = -12 ≠ 0|invertible
  INV_FORMULA|A⁻¹ = (1/det)·[[d, -b], [-c, a]]
  REWRITE|adjugate = [[-2, 0], [6, 6]]
  D|-2|-12|1/6
  D|0|-12|0
  D|6|-12|-1/2
  D|6|-12|-1/2
  Z|[[1/6, 0], [-1/2, -1/2]]
Answer: [[1/6, 0], [-1/2, -1/2]]
```

### Cramers Rule — `CramersRuleGenerator`  ·  high · difficulty 5

2×2 linear systems by Cramer's rule: the coefficient determinant D (checked nonzero), the column-replaced determinants Dx and Dy each worked in full, and the two divisions. Systems are built from an integer solution so the quotients are exact.

**Variants:** `cramers_rule`

```
Problem: Solve the system using Cramer's rule: x + y = 3; -6x - 2y = -14.
Steps:
  EQ_SETUP|x + y = 3; -6x - 2y = -14|solve by Cramer's rule
  DET_FORMULA|D = det [[1, 1], [-6, -2]]
  M|1|-2|-2
  M|1|-6|-6
  S|-2|-6|4
  EVAL|D|4
  CHECK|solvable|D = 4 ≠ 0|unique solution
  REWRITE|Dx: replace the x-column with the constants: [[3, 1], [-14, -2]]
  M|3|-2|-6
  M|1|-14|-14
  S|-6|-14|8
  EVAL|Dx|8
  REWRITE|Dy: replace the y-column with the constants: [[1, 3], [-6, -14]]
  M|1|-14|-14
  M|3|-6|-18
  S|-14|-18|4
  EVAL|Dy|4
  D|8|4|2
  D|4|4|1
  Z|x = 2, y = 1
Answer: x = 2, y = 1
```

### Row Reduction — `RowReductionGenerator`  ·  high · difficulty 5

Gaussian elimination on an augmented matrix — the tabular scratchpad: each row operation names its multiplier and shows the new row, the triangular form is written out, and back-substitution finishes with explicit arithmetic. Systems are built as L·U with unit pivots, so every multiplier and every intermediate entry is a small integer.

**Variants:** `row_reduction_three`, `row_reduction_two`

```
Problem: Solve the system with augmented matrix [[1, 3, 0, 2], [-1, -2, -3, -11], [2, 7, -2, -2]] using row reduction.
Steps:
  MAT_SETUP|augmented matrix [[1, 3, 0, 2], [-1, -2, -3, -11], [2, 7, -2, -2]]|solve by row reduction
  ROW_OP|R2 → R2 + R1|[0, 1, -3, -9]
  ROW_OP|R3 → R3 - 2·R1|[0, 1, -2, -6]
  ROW_OP|R3 → R3 - R2|[0, 0, 1, 3]
  REWRITE|triangular form [[1, 3, 0, 2], [0, 1, -3, -9], [0, 0, 1, 3]]
  EVAL|z|3
  M|-3|3|-9
  S|-9|-9|0
  EVAL|y|0
  M|3|0|0
  S|2|0|2
  EVAL|x|2
  Z|x = 2, y = 0, z = 3
Answer: x = 2, y = 0, z = 3
```

### Limit Evaluation — `LimitEvaluationGenerator`  ·  high · difficulty 4

Limits by the standard toolbox, one technique per record.

**Variants:** `limit_direct`, `limit_factor_cancel`, `limit_infinity`, `limit_one_sided`, `limit_rationalize`

```
Problem: Evaluate lim x→∞ of (-6x^2 + 3x + 2)/(3x^2 + x - 1).
Steps:
  LIMIT_SETUP|lim x→∞ of (-6x^2 + 3x + 2)/(3x^2 + x - 1)|compare degrees
  DEGREE_COMPARE|deg num = deg den = 2|ratio of leading coefficients -6/3
  D|-6|3|-2
  Z|-2
Answer: -2
```

### Derivative Limit Def — `DerivativeLimitDefGenerator`  ·  high · difficulty 5

The limit definition of the derivative, worked in full: substitute x + h, expand the square, subtract f(x) (watching the constant and x² terms cancel), factor h out of every surviving term, cancel it, and send h to 0.

**Variants:** `derivative_limit_at_point`, `derivative_limit_general`

```
Problem: Use the limit definition of the derivative to find f'(4) for f(x) = 3x^2 - 6x - 2.
Steps:
  LIMIT_SETUP|f(x) = 3x^2 - 6x - 2; f'(4) = lim h→0 (f(4+h) - f(4))/h|expand and simplify
  E|4|2|16
  M|3|16|48
  M|-6|4|-24
  A|24|-2|22
  EVAL|f(4)|22
  SUBST|x|4 + h|3(4 + h)^2 - 6(4 + h) - 2
  REWRITE|f(4+h) - f(4) = 3h^2 + 18h
  FACTOR_GROUP|3h^2 + 18h|h|(18 + 3h)
  CANCEL|h|18 + 3h
  SUBST|h|0|18 + 3(0)
  A|18|0|18
  REWRITE|f'(4) = 18
  Z|f'(4) = 18
Answer: f'(4) = 18
```

### Derivative Power Rule — `DerivativePowerRuleGenerator`  ·  high · difficulty 4

The power rule over sums: every term differentiated with its coefficient product shown, the linear term dropping to a constant, and the constant term explicitly sent to 0. A variant mixes in negative exponents.

**Variants:** `derivative_power_negative_power`, `derivative_power_polynomial`

```
Problem: Differentiate f(x) = 6x^3 + 7x^2 - 3x + 1.
Steps:
  DERIV_SETUP|f(x) = 6x^3 + 7x^2 - 3x + 1|f'(x)
  DERIV_RULE|power rule|d/dx of c·x^n = c·n·x^(n-1)
  M|6|3|18
  POWER_RULE|6x^3|18x^2
  M|7|2|14
  POWER_RULE|7x^2|14x
  POWER_RULE|-3x|-3
  POWER_RULE|1|0 (constant rule)
  REWRITE|f'(x) = 18x^2 + 14x - 3
  Z|f'(x) = 18x^2 + 14x - 3
Answer: f'(x) = 18x^2 + 14x - 3
```

### Derivative Product Quotient — `DerivativeProductQuotientGenerator`  ·  high · difficulty 5

Product and quotient rules with the expansion and combination worked out.

**Variants:** `derivative_product_rule`, `derivative_quotient_rule`

```
Problem: Differentiate y = (3x - 6)/(x + 3).
Steps:
  DERIV_SETUP|y = (3x - 6)/(x + 3)|y'
  DERIV_RULE|quotient rule|(f/g)' = (f'g - fg')/g^2
  POWER_RULE|(3x - 6)|3
  POWER_RULE|(x + 3)|1
  REWRITE|y' = (3(x + 3) - (3x - 6))/(x + 3)^2
  DIST|3|x + 3|3x + 9
  DIST|-1|3x - 6|-3x + 6
  COMB_X|3x|-3x|0
  COMB_CONST|9|6|15
  REWRITE|y' = 15/(x + 3)^2
  Z|y' = 15/(x + 3)^2
Answer: y' = 15/(x + 3)^2
```

### Chain Rule — `ChainRuleGenerator`  ·  high · difficulty 5

The chain rule with an explicit substitution for every layer.

**Variants:** `chain_rule_linear_power`, `chain_rule_nested`, `chain_rule_quadratic_power`

```
Problem: Differentiate y = (x^2 + x - 8)^3.
Steps:
  DERIV_SETUP|y = (x^2 + x - 8)^3|y'
  DERIV_RULE|chain rule|dy/dx = dy/du · du/dx
  SUBST|u|x^2 + x - 8|y = u^3
  POWER_RULE|u^3|3u^2
  POWER_RULE|x^2 + x - 8|2x + 1
  REWRITE|y' = 3(x^2 + x - 8)^2(2x + 1)
  Z|y' = 3(x^2 + x - 8)^2(2x + 1)
Answer: y' = 3(x^2 + x - 8)^2(2x + 1)
```

### Derivative Transcendental — `DerivativeTranscendentalGenerator`  ·  high · difficulty 5

Derivatives of trig, exponential, and logarithmic functions with a linear inner function, the chain factor shown every time.

**Variants:** `derivative_transcendental_exp`, `derivative_transcendental_log`, `derivative_transcendental_trig`

```
Problem: Differentiate y = e^(2x).
Steps:
  DERIV_SETUP|y = e^(2x)|y'
  DERIV_RULE|d/dx e^u = e^u·u'|u = 2x
  POWER_RULE|2x|2
  M|1|2|2
  REWRITE|y' = 2 e^(2x)
  Z|y' = 2 e^(2x)
Answer: y' = 2 e^(2x)
```

### Implicit Diff — `ImplicitDiffGenerator`  ·  high · difficulty 5

Implicit differentiation with every term differentiated by name - y-terms carry the chain factor y', product terms use the product rule - then y' is isolated.

**Variants:** `implicit_diff_circle`, `implicit_diff_cubes`, `implicit_diff_full_quad`, `implicit_diff_product`

```
Problem: Find dy/dx for x^2 + xy + y^2 = 27.
Steps:
  IMPLICIT_SETUP|x^2 + xy + y^2 = 27|dy/dx
  IMPLICIT_DIFF|d/dx of x^2|2x
  IMPLICIT_DIFF|d/dx of xy|y + x·y' (product rule)
  IMPLICIT_DIFF|d/dx of y^2|2y·y'
  REWRITE|2x + y + x·y' + 2y·y' = 0
  REWRITE|(x + 2y)·y' = -(2x + y)
  EQ_OP_BOTH|divide|x + 2y|y'|-(2x + y)/(x + 2y)
  REWRITE|dy/dx = -(2x + y)/(x + 2y)
  Z|dy/dx = -(2x + y)/(x + 2y)
Answer: dy/dx = -(2x + y)/(x + 2y)
```

### Log Diff Higher Order — `LogDiffHigherOrderGenerator`  ·  high · difficulty 5

Two extensions of the derivative toolbox.

**Variants:** `derivative_order_2`, `derivative_order_3`, `log_differentiation`

```
Problem: Find the second derivative of f(x) = 3x^4 - 2x^3 - 3x - 2.
Steps:
  DERIV_SETUP|f(x) = 3x^4 - 2x^3 - 3x - 2|f''(x)
  M|3|4|12
  POWER_RULE|3x^4|12x^3
  M|-2|3|-6
  POWER_RULE|-2x^3|-6x^2
  POWER_RULE|-3x|-3
  REWRITE|f'(x) = 12x^3 - 6x^2 - 3
  M|12|3|36
  POWER_RULE|12x^3|36x^2
  M|-6|2|-12
  POWER_RULE|-6x^2|-12x
  REWRITE|f''(x) = 36x^2 - 12x
  Z|f''(x) = 36x^2 - 12x
Answer: f''(x) = 36x^2 - 12x
```

### Tangent Line — `TangentLineGenerator`  ·  high · difficulty 4

Tangent and normal lines to a quadratic at a lattice point: evaluate f(a), differentiate, evaluate f'(a), then build the line from point-slope form and simplify to slope-intercept. Normal lines flip to the negative reciprocal first.

**Variants:** `normal_line`, `tangent_line`

```
Problem: Find the equation of the tangent line to f(x) = -x^2 - 6x at x = 1.
Steps:
  DERIV_SETUP|f(x) = -x^2 - 6x, at x = 1|tangent line
  SUBST|x|1|-1^2 - 61
  E|1|2|1
  M|-1|1|-1
  M|-6|1|-6
  A|-7|0|-7
  EVAL|f(1)|-7
  POWER_RULE|-x^2 - 6x|-2x - 6
  SUBST|x|1|-21 - 6
  M|-2|1|-2
  A|-2|-6|-8
  EVAL|f'(1)|-8
  REWRITE|y - (-7) = -8(x - 1)
  DIST|-8|x - 1|-8x + 8
  A|8|-7|1
  REWRITE|y = -8x + 1
  Z|y = -8x + 1
Answer: y = -8x + 1
```

### Related Rates — `RelatedRatesGenerator`  ·  high · difficulty 5

Related rates on the four classic setups, each with the relation stated, differentiated through d/dt, values substituted, and the target rate isolated - all arithmetic exact (π stays symbolic).

**Variants:** `related_rates_circle`, `related_rates_cone`, `related_rates_cube`, `related_rates_ladder`

```
Problem: Water pours into a conical tank (radius equals half the depth) at 2 m³/min. How fast is the depth rising when the water is 8 m deep? Give an exact answer.
Steps:
  RATE_SETUP|conical tank, radius = height/2; water in at dV/dt = 2 m³/min; depth h = 8 m|dh/dt
  REWRITE|V = (1/3)πr^2·h with r = h/2, so V = πh^3/12
  IMPLICIT_DIFF|d/dt of V = πh^3/12|dV/dt = (πh^2/4)·dh/dt
  SUBST|(h, dV/dt)|(8, 2)|2 = (π(8)^2/4)·dh/dt
  E|8|2|64
  EQ_OP_BOTH|multiply|4|8|π·64·dh/dt
  EQ_OP_BOTH|divide|64π|dh/dt|1/(8π)
  FRAC_REDUCE|8/64|1/8
  Z|dh/dt = 1/(8π) m/min
Answer: dh/dt = 1/(8π) m/min
```

### Linear Approx — `LinearApproxGenerator`  ·  high · difficulty 4

Linear approximation L(x) = f(a) + f'(a)(x - a) at the nearest nice point, with the tangent line built and evaluated exactly.

**Variants:** `linear_approx_cbrt`, `linear_approx_power`, `linear_approx_sqrt`

```
Problem: Use a linear approximation to estimate ∛28. Give the answer as a fraction.
Steps:
  APPROX_SETUP|estimate ∛28|linearize f(x) = ∛x at a = 27
  DERIV_RULE|d/dx ∛x = 1/(3·∛x²)|f'(27) = 1/27
  EVAL|f(27)|3
  EVAL|f'(27)|1/27
  REWRITE|L(x) = 3 + (1/27)(x - 27)
  SUBST|x|28|3 + (1/27)(1)
  M|1/27|1|1/27
  A|3|1/27|82/27
  Z|∛28 ≈ 82/27
Answer: ∛28 ≈ 82/27
```

### LHopital — `LHopitalGenerator`  ·  high · difficulty 5

L'Hôpital's rule with the 0/0 form checked before every application - including a variant that needs the rule twice.

**Variants:** `lhopital_double`, `lhopital_exp_log`, `lhopital_rational`, `lhopital_sin`

```
Problem: Evaluate lim x→0 of (1 - cos(5x))/x^2 using L'Hôpital's rule.
Steps:
  LIMIT_SETUP|lim x→0 of (1 - cos(5x))/x^2|L'Hôpital's rule
  CHECK|substitution|1 - cos 0 = 0 and 0^2 = 0|indeterminate 0/0
  DERIV_RULE|L'Hôpital|replace with f'(x)/g'(x)
  POWER_RULE|1 - cos(5x)|5 sin(5x)
  POWER_RULE|x^2|2x
  REWRITE|lim x→0 of 5 sin(5x)/(2x)
  CHECK|substitution|5 sin 0 = 0 and 2·0 = 0|still 0/0 — apply the rule again
  POWER_RULE|5 sin(5x)|25 cos(5x)
  POWER_RULE|2x|2
  REWRITE|lim x→0 of 25 cos(5x)/2
  SUBST|x|0|25 cos 0/2 = 25/2
  Z|25/2
Answer: 25/2
```

### Curve Analysis — `CurveAnalysisGenerator`  ·  high · difficulty 5

Curve analysis on cubics engineered to have integer critical points (f' = 3(x - p)(x - q), p + q even so all coefficients and the inflection point are integers).

**Variants:** `curve_analysis_critical`, `curve_analysis_inflection`

```
Problem: Find the inflection point of f(x) = x^3 - 6x^2 + 9x and state where the curve is concave up and concave down.
Steps:
  CURVE_SETUP|f(x) = x^3 - 6x^2 + 9x|inflection point and concavity
  POWER_RULE|x^3|3x^2
  POWER_RULE|-6x^2|-12x
  POWER_RULE|9x|9
  REWRITE|f'(x) = 3x^2 - 12x + 9
  REWRITE|f''(x) = 6x - 12
  EQ_OP_BOTH|add|12|6x|12
  D|12|6|2
  SECOND_DERIV_TEST|f'' < 0 for x < 2, f'' > 0 for x > 2|concavity changes
  Z|inflection at x = 2; concave down on (-∞, 2), concave up on (2, ∞)
Answer: inflection at x = 2; concave down on (-∞, 2), concave up on (2, ∞)
```

### Optimization — `OptimizationGenerator`  ·  high · difficulty 5

Optimization word problems built so every critical point is an integer: model, expand, differentiate, solve V' = 0 (rejecting the degenerate root by name), confirm with the second derivative test, and report the optimum.

**Variants:** `optimization_barn_fence`, `optimization_box`, `optimization_product`

```
Problem: An open-top box is made from a 24 by 24 sheet by cutting squares of side x from the corners and folding. What x maximizes the volume, and what is that volume?
Steps:
  OPT_SETUP|square sheet 24 by 24; cut corners x and fold|maximize volume
  REWRITE|V = x(24 - 2x)^2
  REWRITE|V = 4x^3 - 96x^2 + 576x
  POWER_RULE|4x^3 - 96x^2 + 576x|12x^2 - 192x + 576
  REWRITE|V' = (2x - 24)(6x - 24)
  ZERO_PRODUCT|(2x - 24)(6x - 24) = 0|x = 12 or x = 4
  REJECT|x = 12|width 24 - 2(12) = 0, degenerate box
  ACCEPT|x = 4|the only usable critical point
  SUBST|x|4|V = 4(24 - 8)^2
  S|24|8|16
  E|16|2|256
  M|4|256|1024
  Z|x = 4; maximum volume 1024
Answer: x = 4; maximum volume 1024
```

### Mean Value Theorem — `MeanValueTheoremGenerator`  ·  high · difficulty 4

MVT and IVT applications.

**Variants:** `ivt_application`, `mvt_application`

```
Problem: Does the Intermediate Value Theorem guarantee that f(x) = x^3 + 3x - 8 has a root in [-2, 2]?
Steps:
  IVT_SETUP|f(x) = x^3 + 3x - 8 on [-2, 2]|does the IVT guarantee a root?
  SUBST|x|-2|(-2)^3 + 3(-2) - 8
  E|(-2)|3|-8
  M|3|-2|-6
  A|-14|-8|-22
  EVAL|f(-2)|-22
  SUBST|x|2|2^3 + 32 - 8
  E|2|3|8
  M|3|2|6
  A|14|-8|6
  EVAL|f(2)|6
  CHECK|sign change|one endpoint is negative and the other positive|opposite signs
  THEOREM|Intermediate Value Theorem|a continuous function takes every value between its endpoint values
  Z|Yes — a root exists in (-2, 2)
Answer: Yes — a root exists in (-2, 2)
```

### Antiderivative — `AntiderivativeGenerator`  ·  high · difficulty 4

Antiderivatives with the divide-by-new-exponent arithmetic shown per term, and + C always attached.

**Variants:** `antiderivative_exp`, `antiderivative_power`, `antiderivative_trig`

```
Problem: Find ∫ 1/x dx.
Steps:
  INTEG_SETUP|∫ 1/x dx|antiderivative
  INTEG_RULE|log rule|∫ (1/x) dx = ln(abs(x)) + C
  ANTIDERIV|1/x|ln(abs(x))
  REWRITE|ln(abs(x)) + C
  Z|ln(abs(x)) + C
Answer: ln(abs(x)) + C
```

### USubstitution — `USubstitutionGenerator`  ·  high · difficulty 5

u-substitution with the du bookkeeping written out: name u, state du, trade the dx for du (with the constant adjustment), integrate in u, then substitute back. Coefficients are constructed so every constant stays an integer.

**Variants:** `u_substitution_exp_inner`, `u_substitution_log_form`, `u_substitution_poly_inner`, `u_substitution_power_form`

```
Problem: Find ∫ (3(2x + 4))/(x^2 + 4x + 4) dx.
Steps:
  INTEG_SETUP|∫ (3(2x + 4))/(x^2 + 4x + 4) dx|u-substitution
  SUBST|u|x^2 + 4x + 4|du = (2x + 4) dx
  REWRITE|∫ 3/u du
  INTEG_RULE|log rule|∫ (1/u) du = ln(abs(u)) + C
  ANTIDERIV|3/u|3 ln(abs(u))
  SUBST|u|x^2 + 4x + 4|3 ln(abs(x^2 + 4x + 4))
  Z|3 ln(abs(x^2 + 4x + 4)) + C
Answer: 3 ln(abs(x^2 + 4x + 4)) + C
```

### Definite Integral — `DefiniteIntegralGenerator`  ·  high · difficulty 4

Definite integrals by the FTC, and average value: antiderivative term by term (coefficients divisible so F has integer coefficients), F evaluated at both limits with full arithmetic, then subtracted; the average-value variant divides by the width.

**Variants:** `definite_integral_average`, `definite_integral_ftc`

```
Problem: Find the average value of f(x) = 4x^3 - 3x^2 on [1, 2].
Steps:
  INTEG_SETUP|∫ from 1 to 2 of (4x^3 - 3x^2) dx|average value = integral/(b - a)
  INTEG_RULE|power rule|∫ x^n dx = x^(n+1)/(n+1)
  D|4|4|1
  ANTIDERIV|4x^3|x^4
  D|-3|3|-1
  ANTIDERIV|-3x^2|-x^3
  REWRITE|F(x) = x^4 - x^3
  E|2|4|16
  E|2|3|8
  M|-1|8|-8
  A|16|-8|8
  EVAL|F(2)|8
  E|1|4|1
  E|1|3|1
  M|-1|1|-1
  A|1|-1|0
  EVAL|F(1)|0
  S|8|0|8
  S|2|1|1
  D|8|1|8
  Z|8
Answer: 8
```

### Riemann Sum — `RiemannSumGenerator`  ·  high · difficulty 4

Riemann sums and the trapezoidal rule as pure tables: Δx computed, every sample point evaluated in its own step, the values summed left to right, and the final scaling by Δx (or Δx/2).

**Variants:** `riemann_left`, `riemann_midpoint`, `riemann_right`, `riemann_trapezoid`

```
Problem: Approximate ∫ from 2 to 10 of (x^2 - 5) dx using the trapezoidal rule with n = 4.
Steps:
  RIEMANN_SETUP|f(x) = x^2 - 5 on [2, 10], n = 4|trapezoid rule
  S|10|2|8
  D|8|4|2
  EVAL|Δx|2
  EVAL|f(2)|-1
  EVAL|f(4)|11
  EVAL|f(6)|31
  EVAL|f(8)|59
  EVAL|f(10)|95
  M|2|11|22
  M|2|31|62
  M|2|59|118
  A|-1|22|21
  A|21|62|83
  A|83|118|201
  A|201|95|296
  M|1|296|296
  Z|296
Answer: 296
```

### Area Between Curves — `AreaBetweenCurvesGenerator`  ·  high · difficulty 5

Area between curves with integer intersections by construction: set the curves equal, factor to find the bounds, check which curve is on top at the midpoint, integrate the difference with exact fractions.

**Variants:** `area_between_line_parabola`, `area_between_parabola_pair`

```
Problem: Find the area between y = x^2 and y = 98 - x^2.
Steps:
  AREA_SETUP|y = x^2 and y = 98 - x^2|area between the curves
  EQ_SETUP|x^2 = 98 - x^2|find intersections
  EQ_OP_BOTH|add|x^2|2x^2|98
  EQ_OP_BOTH|divide|2|x^2|49
  REWRITE|x = ±7
  CHECK|midpoint x = 0|upper = 98, lower = 0|98 - x^2 is on top
  REWRITE|A = ∫ from -7 to 7 of (98 - 2x^2) dx
  ANTIDERIV|98 - 2x^2|F(x) = 98x - (2/3)x^3
  EVAL|F(7)|1372/3
  EVAL|F(-7)|-1372/3
  S|1372/3|-1372/3|2744/3
  Z|2744/3
Answer: 2744/3
```

### Solid Revolution — `SolidRevolutionGenerator`  ·  high · difficulty 5

Volumes with exact π answers: disks, washers, shells, and square cross-sections, each with its formula stated, the integrand squared/expanded, and the FTC evaluation in exact fractions.

**Variants:** `volume_cross_section`, `volume_disk`, `volume_shell`, `volume_washer`

```
Problem: The base of a solid is the region under y = 5 - x on [0, 5]. Cross-sections perpendicular to the x-axis are squares. Find the volume.
Steps:
  VOLUME_SETUP|base: region under y = 5 - x on [0, 5]; cross-sections perpendicular to the x-axis are squares|cross-section method
  VOL_FORMULA|V = ∫ [side(x)]^2 dx
  REWRITE|[(5 - x)]^2 = x^2 - 10x + 25
  ANTIDERIV|x^2 - 10x + 25|F(x) = (1/3)x^3 - 5x^2 + 25x
  EVAL|F(5)|125/3
  EVAL|F(0)|0
  S|125/3|0|125/3
  Z|125/3
Answer: 125/3
```

### Separable ODE — `SeparableODEGenerator`  ·  high · difficulty 5

Separable differential equations solved by the full ritual: separate, integrate both sides, resolve the constant from the initial condition, and isolate y. Answers stay exact and symbolic.

**Variants:** `separable_ode_exponential`, `separable_ode_find_k`, `separable_ode_power`, `separable_ode_reciprocal`

```
Problem: Solve dy/dx = y^2 with y(0) = 4.
Steps:
  ODE_SETUP|dy/dx = y^2, y(0) = 4|solve
  SEPARATE|y^(-2) dy = dx
  INTEG_RULE|both sides|∫ y^(-2) dy = ∫ dx
  ANTIDERIV|y^(-2) dy|-1/y
  ANTIDERIV|dx|x + C
  REWRITE|-1/y = x + C
  SUBST|x|0|-1/4 = C
  REWRITE|-1/y = x - 1/4
  REWRITE|y = 4/(1 - 4x)
  Z|y = 4/(1 - 4x)
Answer: y = 4/(1 - 4x)
```

### Integration By Parts — `IntegrationByPartsGenerator`  ·  high · difficulty 5

Integration by parts with the u/dv choice and both du and v written out, the boundary term formed, and the leftover integral finished.

**Variants:** `integration_by_parts_ln`, `integration_by_parts_x_exp`, `integration_by_parts_x_trig`

```
Problem: Find ∫ 2x cos(x) dx.
Steps:
  INTEG_SETUP|∫ 2x cos(x) dx|integration by parts
  PARTS_FORMULA|∫ u dv = uv - ∫ v du
  PARTS_CHOOSE|u = 2x, dv = cos(x) dx|du = 2 dx, v = sin(x)
  REWRITE|2x(sin(x)) - ∫ 2(sin(x)) dx
  ANTIDERIV|2(sin(x))|-2cos(x)
  REWRITE|2x sin(x) + 2cos(x)
  Z|2x sin(x) + 2cos(x) + C
Answer: 2x sin(x) + 2cos(x) + C
```

### Partial Fractions — `PartialFractionsGenerator`  ·  high · difficulty 5

Partial fraction decomposition of proper rationals with linear factors, solved by clearing denominators and substituting the roots (the cover-up idea made explicit), then integrated term by term when the item asks for the integral. All constants are integers by construction.

**Variants:** `partial_fractions_decompose`, `partial_fractions_integrate`, `partial_fractions_repeated`

```
Problem: Find ∫ (-x - 9)/(x(x - 3)) dx.
Steps:
  INTEG_SETUP|∫ (-x - 9)/(x(x - 3)) dx|partial fractions
  PARTFRAC_SETUP|(-x - 9)/(x(x - 3)) = A/x + B/(x - 3)
  REWRITE|-x - 9 = A(x - 3) + Bx
  SUBST|x|0|-(0) - 9 = A((0) - 3)
  EVAL|-9 = -3A
  EQ_OP_BOTH|divide|-3|A|3
  SUBST|x|3|-(3) - 9 = B(3)
  EVAL|-12 = 3B
  EQ_OP_BOTH|divide|3|B|-4
  REWRITE|(-x - 9)/(x(x - 3)) = 3/x - 4/(x - 3)
  INTEG_RULE|term by term|∫ 3/x dx - ∫ 4/(x - 3) dx
  ANTIDERIV|3/x dx|3ln(abs(x))
  ANTIDERIV|-4/(x - 3) dx|-4ln(abs(x - 3)) + C
  REWRITE|3ln(abs(x)) - 4ln(abs(x - 3)) + C
  Z|3ln(abs(x)) - 4ln(abs(x - 3)) + C
Answer: 3ln(abs(x)) - 4ln(abs(x - 3)) + C
```

### Improper Integral — `ImproperIntegralGenerator`  ·  high · difficulty 5

Improper integrals rewritten as limits, integrated, and collapsed by sending the bound to its limit. Coefficients are constructed so every antiderivative has an integer coefficient; convergent answers are exact integers or fractions, divergent ones say so.

**Variants:** `improper_integral_divergent`, `improper_integral_exponential`, `improper_integral_p_integral`, `improper_integral_zero_bound`

```
Problem: Evaluate ∫ from 1 to ∞ of (7/x) dx or state that it diverges.
Steps:
  INTEG_SETUP|∫ from 1 to ∞ of (7/x) dx|improper integral
  LIMIT_SETUP|lim b→∞ ∫ from 1 to b of (7/x) dx
  ANTIDERIV|7/x dx|7ln(abs(x))
  EVAL|ln(1) = 0
  EVAL|(7ln(b)) - (7ln(1)) = 7ln(b)
  EVAL|lim b→∞ 7ln(b) = ∞
  Z|diverges
Answer: diverges
```

### Euler Method — `EulerMethodGenerator`  ·  high · difficulty 5

Euler's method for dy/dx = ax + by as a pure scratchpad table: each row records x and y, then the slope is evaluated explicitly, scaled by h, and added on. Step sizes are terminating decimals so every value in the table is exact.

**Variants:** `euler_method_three_step`, `euler_method_two_step`

```
Problem: Use Euler's method with step size h = 0.2 to approximate y(0.6) for dy/dx = -2x with y(0) = 5.
Steps:
  ODE_SETUP|dy/dx = -2x, y(0) = 5|Euler's method with h = 0.2
  TABLE_ENTRY|x = 0|y = 5
  EVAL|f(0, 5)|-2(0) = 0
  M|0.2|0|0
  TABLE_ENTRY|x = 0.2|y = 5
  EVAL|f(0.2, 5)|-2(0.2) = -0.4
  M|0.2|-0.4|-0.08
  S|5|0.08|4.92
  TABLE_ENTRY|x = 0.4|y = 4.92
  EVAL|f(0.4, 4.92)|-2(0.4) = -0.8
  M|0.2|-0.8|-0.16
  S|4.92|0.16|4.76
  TABLE_ENTRY|x = 0.6|y = 4.76
  Z|4.76
Answer: 4.76
```

### Logistic Growth — `LogisticGrowthGenerator`  ·  high · difficulty 5

Logistic differential equations dP/dt = kP(1 - P/L) worked with the standard facts: the carrying capacity is the limit, growth is fastest at L/2 with maximum rate kL/4, and the solution is P = L/(1 + Ae^(-kt)) with A = (L - P(0))/P(0). All numbers are exact terminating decimals or integers by construction.

**Variants:** `logistic_growth_half_capacity`, `logistic_growth_limit`, `logistic_growth_max_rate`, `logistic_growth_rate_at`, `logistic_growth_solution`

```
Problem: A population satisfies dP/dt = 0.2P(1 - P/400). Compute dP/dt when P = 160.
Steps:
  ODE_SETUP|dP/dt = 0.2P(1 - P/400)|evaluate dP/dt at P = 160
  SUBST|P|160|0.2(160)(1 - 160/400)
  D|160|400|0.4
  S|1|0.4|0.6
  M|0.2|160|32
  M|32|0.6|19.2
  Z|19.2
Answer: 19.2
```

### Parametric Calculus — `ParametricCalculusGenerator`  ·  high · difficulty 5

Parametric derivatives and arc length, and polar area, all exact. Arc-length curves are built so the speed is a perfect square: x = 3mt^2, y = mt^3 - 3mt gives speed 3m(t^2 + 1). Polar circles r = 2a·cos(θ) use the half-angle identity and land on πa².

**Variants:** `parametric_calculus_arc_length`, `parametric_calculus_dydx`, `parametric_calculus_polar_circle`, `parametric_calculus_polar_sector`

```
Problem: Find the area enclosed by the polar curve r = 8cos(θ) for -π/2 ≤ θ ≤ π/2.
Steps:
  POLAR_SETUP|r = 8cos(θ) for -π/2 ≤ θ ≤ π/2|enclosed area
  POLAR_AREA_FORMULA|A = (1/2) ∫ r^2 dθ
  EVAL|r^2|64cos^2(θ)
  M|1/2|64|32
  IDENT_SUB|cos^2(θ) = (1 + cos(2θ))/2
  M|32|1/2|16
  REWRITE|A = ∫ 16(1 + cos(2θ)) dθ
  ANTIDERIV|16(1 + cos(2θ)) dθ|16θ + 8sin(2θ)
  EVAL|sin(π) = 0, sin(-π) = 0
  SUBST|θ|π/2|16(π/2) + 8sin(π) = 8π
  SUBST|θ|-π/2|16(-π/2) + 8sin(-π) = -8π
  S|8π|-8π|16π
  Z|16π
Answer: 16π
```

### Arc Length — `ArcLengthGenerator`  ·  high · difficulty 5

Rectangular arc length L = ∫ √(1 + (dy/dx)²) dx over families where 1 + (dy/dx)² is a perfect square, so every answer is exact: Pythagorean-slope lines, y = x³/(3c) + c/(4x) (the classic "17/12" family), and the catenary (e^x + e^(-x))/2.

**Variants:** `arc_length_catenary`, `arc_length_cubic_reciprocal`, `arc_length_line`

```
Problem: Find the arc length of y = x^3/6 + 1/(2x) on [1, 2].
Steps:
  ARCLEN_FORMULA|L = ∫ √(1 + (dy/dx)^2) dx
  EVAL|dy/dx|x^2/2 - 1/(2x^2)
  EVAL|(dy/dx)^2 = x^4/4 - 1/2 + 1/(4x^4)
  EVAL|1 + (dy/dx)^2 = x^4/4 + 1/2 + 1/(4x^4)
  REWRITE|x^4/4 + 1/2 + 1/(4x^4) = (x^2/2 + 1/(2x^2))^2
  EVAL|√((x^2/2 + 1/(2x^2))^2) = x^2/2 + 1/(2x^2)
  INTEG_SETUP|∫ from 1 to 2 of (x^2/2 + 1/(2x^2)) dx|arc length
  ANTIDERIV|(x^2/2 + 1/(2x^2)) dx|x^3/6 - 1/(2x)
  SUBST|x|2|8/6 - 2/8 = 32/24 - 6/24 = 26/24
  FRAC_REDUCE|26/24|13/12
  SUBST|x|1|1/6 - 2/4 = 2/12 - 6/12 = -4/12
  FRAC_REDUCE|-4/12|-1/3
  EVAL|13/12 - (-1/3) = 13/12 - (-4/12) = 17/12
  Z|17/12
Answer: 17/12
```

### Series Convergence — `SeriesConvergenceGenerator`  ·  high · difficulty 5

Convergence tests where the scratchpad's first move is CHOOSING the right test: nth-term, geometric, p-series, ratio, alternating (absolute vs conditional), and direct/limit comparison. Geometric sums are exact fractions.

**Variants:** `series_convergence_alternating`, `series_convergence_comparison`, `series_convergence_geometric`, `series_convergence_nth_term`, `series_convergence_p_series`, `series_convergence_ratio`

```
Problem: Determine whether Σ 8^n/n! for n ≥ 1 converges or diverges.
Steps:
  SERIES_SETUP|Σ 8^n/n!, n ≥ 1|converge or diverge?
  TEST_CHOOSE|ratio test|factorial present
  REWRITE|a_(n+1)/a_n = (8^(n+1)/(n+1)!)·(n!/8^n)
  CANCEL|8^(n+1)/8^n = 8|(n+1)!/n! = n + 1
  REWRITE|a_(n+1)/a_n = 8/(n + 1)
  LIMIT_SETUP|lim n→∞ 8/(n + 1) = 0
  CHECK|ratio test|0 < 1|converges
  Z|converges
Answer: converges
```

### Power Series — `PowerSeriesGenerator`  ·  high · difficulty 5

Radius and interval of convergence by the ratio test, with the endpoints checked one at a time. The five families produce every bracket combination plus the degenerate radii: 1/c^n (open), 1/(n·c^n) (half-open), 1/(n^2·c^n) (closed), n!·(x-a)^n (R = 0), (x-a)^n/n! (R = ∞).

**Variants:** `power_series_closed`, `power_series_half_open`, `power_series_infinite`, `power_series_open`, `power_series_zero_radius`

```
Problem: Find the radius and interval of convergence of Σ n!·(x - 1)^n for n ≥ 1.
Steps:
  SERIES_SETUP|Σ n!·(x - 1)^n, n ≥ 1|radius and interval of convergence
  TEST_CHOOSE|ratio test|power series
  CANCEL|(n+1)!/n! = n + 1|abs(x - 1)^(n+1)/abs(x - 1)^n = abs(x - 1)
  REWRITE|abs(a_(n+1)/a_n) = (n + 1)·abs(x - 1)
  LIMIT_SETUP|lim n→∞ (n + 1)·abs(x - 1) = ∞ for abs(x - 1) > 0
  CHECK|ratio test|L = ∞ unless x = 1|converges only at x = 1
  Z|R = 0, x = 1 only
Answer: R = 0, x = 1 only
```

### Taylor Series — `TaylorSeriesGenerator`  ·  high · difficulty 5

Taylor and Maclaurin polynomials: build them from a derivative table, use them to approximate nearby values with exact decimal arithmetic, and bound the error with the Lagrange remainder (M = 1 for sin/cos; M is supplied in the problem for e^x, Principle 5).

**Variants:** `taylor_series_approximate`, `taylor_series_centered`, `taylor_series_error_bound`, `taylor_series_maclaurin`

```
Problem: The Taylor polynomial P_1 of f(x) = cos(x) around 0 is used at x = 1/3. Bound the error with the Lagrange remainder.
Steps:
  TAYLOR_SETUP|f(x) = cos(x), P_1 around 0|bound the error at x = 1/3
  THEOREM|Lagrange error bound|abs(R_n) ≤ M·abs(x - a)^(n+1)/(n+1)!
  CHECK|derivative bound|derivatives of cos(x) are bounded by 1|M = 1
  E|1/3|2|1/9
  EVAL|(1 + 1)!|2
  D|1/9|2|1/18
  Z|1/18
Answer: 1/18
```

### ZScore — `ZScoreGenerator`  ·  high · difficulty 4

Z-scores and standardization: convert a raw value to its z-score, recover a raw value from a z-score, compare standings across two distributions, and flag unusual values with the |z| > 2 rule. All z-scores are exact terminating decimals by construction.

**Variants:** `z_score_compare`, `z_score_raw_from_z`, `z_score_standardize`, `z_score_unusual`

```
Problem: A distribution has mean 45 and standard deviation 8. Using the |z| > 2 rule, is the value 37 unusual? (answer usual or unusual)
Steps:
  NORM_SETUP|X ~ N(45, 8)|is x = 37 unusual?
  ZSCORE_FORMULA|z = (x - μ)/σ
  S|37|45|-8
  D|-8|8|-1
  CHECK|abs(z) > 2 rule|abs(-1) ≤ 2|usual
  Z|usual
Answer: usual
```

### Regression — `RegressionGenerator`  ·  high · difficulty 5

Least-squares linear regression by the deviation formulas: b = Sxy/Sxx, a = ȳ - b·x̄, r = Sxy/√(Sxx·Syy), r² and residuals. Data are built so x̄, ȳ, Sxx and √(Sxx·Syy) are integers, making every reported value an exact terminating decimal.

**Variants:** `regression_correlation`, `regression_line`, `regression_predict`, `regression_r_squared`, `regression_residual`

```
Problem: The least-squares line for a data set is ŷ = 32.6 - 0.2x. Find the residual at the point (3, 32).
Steps:
  RESID_SETUP|point (3, 32), line ŷ = 32.6 - 0.2x|residual = observed − predicted
  M|-0.2|3|-0.6
  A|32.6|-0.6|32
  S|32|32|0
  Z|0
Answer: 0
```

### Expected Value — `ExpectedValueGenerator`  ·  high · difficulty 4

Expected value and variance of small discrete distributions, and the expected value of simple games. Probabilities share a denominator dividing 100, so E[X], Var(X) and dollar payoffs are all exact.

**Variants:** `expected_value_expected_value`, `expected_value_fair_game`, `expected_value_variance`, `expected_value_winnings`

```
Problem: A game costs $6 to play. You win $5 with probability 1/4, win $3 with probability 1/4, win $2 with probability 1/2. Is the game fair, favorable, or unfavorable to the player?
Steps:
  EV_SETUP|P(win $5) = 1/4; P(win $3) = 1/4; P(win $2) = 1/2|fair? cost = $6
  M|5|1/4|1.25
  M|3|1/4|0.75
  M|2|1/2|1
  A|1.25|0.75|2
  A|2|1|3
  S|3|6|-3
  CHECK|net vs 0|-3 < 0|unfavorable
  Z|unfavorable
Answer: unfavorable
```

### Confidence Interval — `ConfidenceIntervalGenerator`  ·  high · difficulty 5

Confidence intervals for a mean or a proportion, margins of error, and minimum sample sizes — with the critical value z* given in the problem (Principle 5). Sample sizes are perfect squares and the margins are chosen so √n is an integer and every quantity is an exact terminating decimal.

**Variants:** `confidence_interval_mean_ci`, `confidence_interval_mean_margin`, `confidence_interval_prop_margin`, `confidence_interval_sample_size_mean`, `confidence_interval_sample_size_prop`

```
Problem: You want a margin of error of 0.5 for a confidence interval for the mean, with population standard deviation σ = 3. Using z* = 2.05, find the minimum sample size.
Steps:
  CI_SETUP|σ = 3, E = 0.5, z* = 2.05|minimum sample size for the mean
  SAMPLE_SIZE_FORMULA|n = (z*·σ/E)^2
  M|2.05|3|6.15
  D|6.15|0.5|12.3
  E|12.3|2|151.29
  CEIL|151.29|152
  Z|152
Answer: 152
```

### Hypothesis Test — `HypothesisTestGenerator`  ·  high · difficulty 5

Two-sided significance tests — a one-proportion z-test and a one-sample t-test — with the critical value given in the problem (Principle 5). The null proportion is 0.5 and n is a perfect square, and the t-test's standard error is constructed to divide evenly, so every test statistic is an exact terminating decimal.

**Variants:** `hypothesis_test_prop_z_decision`, `hypothesis_test_prop_z_stat`, `hypothesis_test_t_decision`, `hypothesis_test_t_stat`

```
Problem: In a two-sided one-sample t-test of H0: μ = 85, a sample of size 25 has mean x̄ = 89 and standard deviation s = 10. Using a critical value of 2.576, state the conclusion (reject H0 or fail to reject H0).
Steps:
  HT_SETUP|H0: μ = 85; Ha: μ ≠ 85|n = 25, x̄ = 89, s = 10, critical value = 2.576
  TEST_STAT_FORMULA|t = (x̄ - μ0)/(s/√n)
  ROOT|√25|5
  D|10|5|2
  S|89|85|4
  D|4|2|2
  CHECK|abs(stat) vs critical value|2 ≤ 2.576|fail to reject H0
  Z|fail to reject H0
Answer: fail to reject H0
```

### Chi Square — `ChiSquareGenerator`  ·  high · difficulty 5

Chi-square tests worked cell by cell: a goodness-of-fit test against a uniform model, and a 2×2 test of independence with an expected-count table. Data are built so every expected count and every χ² contribution is exact; the critical value is supplied in the problem (Principle 5).

**Variants:** `chi_square_gof_decision`, `chi_square_gof_stat`, `chi_square_independence_decision`, `chi_square_independence_stat`

```
Problem: A 2×2 contingency table has counts 15, 35 in row 1 and 5, 45 in row 2 (N = 100). Test the two variables for independence. Using a critical value of 3.841 (df = 1), state the conclusion (reject H0 or fail to reject H0).
Steps:
  CHI_SETUP|row 1: 15, 35; row 2: 5, 45; N = 100|independence; df = 1, critical value = 3.841
  CHI_FORMULA|E = (row·col)/N; χ² = Σ (O - E)^2/E
  EXP_CELL|(50·20)/100|10
  EXP_CELL|(50·80)/100|40
  EXP_CELL|(50·20)/100|10
  EXP_CELL|(50·80)/100|40
  CHI_TERM|15 - 10 = 5|5^2 = 25|25/10 = 2.5
  CHI_TERM|35 - 40 = -5|(-5)^2 = 25|25/40 = 0.625
  CHI_TERM|5 - 10 = -5|(-5)^2 = 25|25/10 = 2.5
  CHI_TERM|45 - 40 = 5|5^2 = 25|25/40 = 0.625
  A|2.5|0.625|3.125
  A|3.125|2.5|5.625
  A|5.625|0.625|6.25
  CHECK|χ² vs critical value|6.25 > 3.841|reject H0
  Z|reject H0
Answer: reject H0
```

### Conditional Probability — `ConditionalProbabilityGenerator`  ·  high · difficulty 5

Conditional probability from a two-way table and Bayes-style diagnostic test questions built from sensitivity and specificity. Counts are small integers, so each answer is exact.

**Variants:** `conditional_probability_bayes_negative`, `conditional_probability_bayes_positive`, `conditional_probability_table`

```
Problem: A screening test is used for 104 people. Disease=yes count is 40 and disease=no count is 64. Sensitivity P(test positive given disease=yes) = 7/10. Specificity P(test negative given disease=no) = 3/4. Find P(disease=yes given test positive). Give an exact answer.
Steps:
  BAYES_SETUP|disease=yes 40, disease=no 64|sensitivity 7/10, specificity 3/4|P(disease=yes given test positive)
  BAYES_CELL|true positive|40 * 7/10|28
  BAYES_CELL|false negative|40 - 28|12
  BAYES_CELL|true negative|64 * 3/4|48
  BAYES_CELL|false positive|64 - 48|16
  A|28|16|44
  BAYES_FORMULA|P(disease=yes given positive) = TP/(TP + FP)
  FRAC_BUILD|28/44|7/11
  CHECK|positive tests|posterior denominator = 44
  Z|7/11
Answer: 7/11
```

### Geometric Distribution — `GeometricDistributionGenerator`  ·  high · difficulty 4

Geometric distribution for the trial number of the first success. The scratchpad shows repeated failures followed by success, complement rules, tail probabilities, and the expected waiting time.

**Variants:** `geometric_distribution_after_k`, `geometric_distribution_at_most`, `geometric_distribution_exact_k`, `geometric_distribution_mean`

```
Problem: A geometric experiment has success probability p = 4/5. Let X be the trial number of the first success. Find the expected trial number of the first success.
Steps:
  GEOM_SETUP|p = 4/5|E[X]
  GEOM_FORMULA|E[X] = 1/p
  D|1|4/5|1.25
  Z|1.25
Answer: 1.25
```

### Fermi Estimation — `FermiEstimationGenerator`  ·  high · difficulty 4

Fermi-style estimates where the assumptions are supplied in the prompt, multiplied explicitly, and rounded to two significant figures.

**Variants:** `fermi_estimation_cafeteria`, `fermi_estimation_stadium`, `fermi_estimation_water_use`

```
Problem: Estimate seats in a stadium with 40 sections, 18 rows per section, and 18 seats per row. Round to 2 significant figures.
Steps:
  FERMI_SETUP|stadium seats|seats
  FERMI_FACTOR|sections|40
  FERMI_FACTOR|rows per section|18
  FERMI_FACTOR|seats per row|18
  M|40|18|720
  M|720|18|12960
  SIGFIG_ROUND|12960|2 significant figures|1.3 × 10^4
  ESTIMATE_CHECK|1.3 × 10^4|12960|rounded estimate
  Z|1.3 × 10^4 seats
Answer: 1.3 × 10^4 seats
```

### Normal Table — `NormalTableGenerator`  ·  high · difficulty 4

Normal-distribution probabilities with the z-table excerpt supplied in the problem text (Principle 5: no lookups the problem doesn't provide). The scratchpad standardizes, reads the provided table, and applies the complement / symmetry / between rule explicitly.

**Variants:** `normal_above`, `normal_below`, `normal_between`

```
Problem: Package weights are normally distributed with mean 482 grams and standard deviation 9 grams. What is the probability of a value between 498.2 and 499.1 grams?
Standard normal table, Φ(z) = P(Z < z): z=1.80: 0.9641; z=1.90: 0.9713; z=2.00: 0.9772; z=2.20: 0.9861
Steps:
  NORM_SETUP|X ~ N(482, 9)|P(498.2 < X < 499.1)
  ZSCORE|(498.2 - 482)/9|1.80
  ZSCORE|(499.1 - 482)/9|1.90
  TABLE_LOOKUP|Φ(1.80)|0.9641
  TABLE_LOOKUP|Φ(1.90)|0.9713
  REWRITE|P(498.2 < X < 499.1) = Φ(1.90) - Φ(1.80)
  S|0.9713|0.9641|0.0072
  Z|0.0072
Answer: 0.0072
```

### Multiplying Binomials — `MultiplyingBinomialsGenerator`  ·  high · difficulty 5

Generates problems for multiplying two binomials using FOIL. (ax + b)(cx + d)

**Variants:** `multiply_binomials_foil`

```
Problem: Multiply: (3x + 4)(-8x - 1)
Steps:
  FOIL_SETUP|(3x + 4)(-8x - 1)
  FOIL_F|First: (3x) * (-8x)|-24x^2
  FOIL_O|Outer: (3x) * (-1)|-3x
  FOIL_I|Inner: (4) * (-8x)|-32x
  FOIL_L|Last: (4) * (-1)|-4
  POLY_COMBINE|Combine Like Terms: -3x + -32x = -35x
  Z|-24x^2 - 35x - 4
Answer: -24x^2 - 35x - 4
```

### Multiplying Polynomials — `MultiplyingPolynomialsGenerator`  ·  high · difficulty 5

Generates problems for multiplying polynomials (e.g., Binomial * Trinomial). (ax + b)(cx^2 + dx + e)

**Variants:** `multiply_poly_distribute`

```
Problem: Multiply: (x + 1)(-5x^2 - x + 3)
Steps:
  POLY_MULT_SETUP|(x + 1)(-5x^2 - x + 3)
  DIST_TERM|x|- 5x^3 - 1x^2 + 3x
  DIST_TERM|+1|- 5x^2 - 1x + 3
  POLY_GROUP_LIKE|-5x^3 + (-1x^2 - 5x^2) + (3x - 1x) + 3
  Z|- 5x^3 - 6x^2 + 2x + 3
Answer: - 5x^3 - 6x^2 + 2x + 3
```

### Polynomial Div Monomial — `PolynomialDivMonomialGenerator`  ·  high · difficulty 5

Generates problems for dividing a polynomial by a monomial. (ax^n + bx^m + ...) / (dx^k)

**Variants:** `poly_div_monomial`

```
Problem: Divide: (3x^5 + 9x^4) / (3x^2)
Steps:
  POLY_DIV_SETUP|(3x^5 + 9x^4) / (3x^2)
  POLY_DIV_SPLIT|(3x^5) / (3x^2) + (9x^4) / (3x^2)
  Z|1x^3 + 3x^2
Answer: 1x^3 + 3x^2
```

### Stoichiometry — `StoichiometryGenerator`  ·  high · difficulty 4

Balanced-equation and stoichiometric conversion practice.

**Variants:** `stoichiometry_balance_equation`, `stoichiometry_limiting_reagent`, `stoichiometry_mass_to_mass`, `stoichiometry_mass_to_volume`

```
Problem: Given balanced equation N2 + 3 H2 -> 2 NH3, initial amounts are N2=1 mol and H2=5 mol. Find the limiting reactant and maximum NH3 produced.
Steps:
  STOICH_SETUP|limiting_reagent|N2 + 3 H2 -> 2 NH3|given=N2=1 mol, H2=5 mol
  STOICH_RATIO|N2->NH3|2/1=2
  M|1|2|2
  STOICH_RATIO|H2->NH3|2/3=2/3
  M|5|2/3|10/3
  LIMIT_CHECK|NH3 from N2=2 mol|NH3 from H2=10/3 mol
  LIMITING_REAGENT|N2|NH3=2 mol
  Z|limiting=N2; NH3=2 mol
Answer: limiting=N2; NH3=2 mol
```

### Solution Chem — `SolutionChemGenerator`  ·  high · difficulty 3

Exact solution-concentration arithmetic for dilution and mixing.

**Variants:** `solution_chem_dilution_final_molarity`, `solution_chem_dilution_stock_volume`, `solution_chem_mixing_molarity`

```
Problem: A stock solution has molarity M1=8 M. Prepare V2=311 mL at M2=1/3 M. Find stock volume V1.
Steps:
  SOLUTION_SETUP|dilution_stock_volume|M1=8|M2=1/3, V2=311
  SOLUTION_FORMULA|M1*V1=M2*V2
  M|1/3|311|311/3
  D|311/3|8|311/24
  Z|V1=311/24 mL
Answer: V1=311/24 mL
```

### PHCalculation — `PHCalculationGenerator`  ·  high · difficulty 4

Exact pH and pOH arithmetic with powers of ten or supplied log values.

**Variants:** `ph_calculation_hydronium_power`, `ph_calculation_hydronium_with_log`, `ph_calculation_hydroxide_power`, `ph_calculation_hydroxide_with_log`

```
Problem: A solution has [OH-]=8*10^-2 M. Use provided log10(8)=0.9 to find pOH and pH with pH+pOH=14.
Steps:
  PH_SETUP|hydroxide_with_log|[OH-]=8*10^-2|log10(8)=0.9
  PH_FORMULA|pOH=-log10([OH-]), pH=14-pOH
  LOG_PRODUCT|log10(8*10^-2)=log10(8)-2
  S|0.9|2|-1.1
  S|0|-1.1|1.1
  S|14|1.1|12.9
  Z|pOH=1.1; pH=12.9
Answer: pOH=1.1; pH=12.9
```

### Gas Stoichiometry — `GasStoichiometryGenerator`  ·  high · difficulty 4

Stoichiometry chained through PV=nRT with R supplied as 1.

**Variants:** `gas_stoichiometry_gas_to_mass`, `gas_stoichiometry_mass_to_gas_pressure`, `gas_stoichiometry_mass_to_gas_volume`

```
Problem: Given balanced equation 2 H2O2 -> 2 H2O + O2, 306 g H2O2 reacts. At P=1 atm and T=9 K with R=1, what volume V of O2 gas forms? Molar mass H2O2=34 g/mol.
Steps:
  GAS_STOICH_SETUP|mass_to_gas_volume|2 H2O2 -> 2 H2O + O2|given=306 g H2O2, gas=O2
  MOLAR_MASS|H2O2|34 g/mol
  D|306|34|9
  STOICH_RATIO|H2O2->O2|1/2=1/2
  M|9|1/2|9/2
  GAS_FORMULA|PV=nRT so V=nT/P with R=1
  M|9/2|9|81/2
  D|81/2|1|81/2
  Z|V O2=81/2 L
Answer: V O2=81/2 L
```

## College

### Partial Derivative — `PartialDerivativeGenerator`  ·  college · difficulty 2

Partial derivatives of two-variable polynomials, including second partials and mixed partials with Clairaut equality as a check.

**Variants:** `partial_derivative_first_x`, `partial_derivative_first_y`, `partial_derivative_mixed_xy`, `partial_derivative_second_xx`, `partial_derivative_second_yy`

```
Problem: Let f(x,y) = 4*x^4*y^4 + 8*x^4*y. Find f_yy.
Steps:
  PARTIAL_SETUP|f(x,y) = 4*x^4*y^4 + 8*x^4*y|f_yy
  PARTIAL_RULE|8*x^4*y|d/dy|8*x^4
  PARTIAL_RULE|4*x^4*y^4|d/dy|16*x^4*y^3
  PARTIAL_RESULT|f_y|16*x^4*y^3 + 8*x^4
  PARTIAL_RULE|8*x^4|d/dy|0
  PARTIAL_RULE|16*x^4*y^3|d/dy|48*x^4*y^2
  PARTIAL_RESULT|f_yy|48*x^4*y^2
  Z|48*x^4*y^2
Answer: 48*x^4*y^2
```

### Gradient — `GradientGenerator`  ·  college · difficulty 2

Gradient, directional derivative, and tangent plane computations for quadratic functions f(x,y).

**Variants:** `gradient_directional`, `gradient_gradient`, `gradient_tangent`

```
Problem: For f(x,y) = 4*x^2 + y^2 + 2*x + y, find the directional derivative at (3, 2) in direction u = (-3/5, 4/5).
Steps:
  GRAD_SETUP|f(x,y) = 4*x^2 + y^2 + 2*x + y|point (3, 2)|directional
  PARTIAL_RESULT|f_x|8*x + 2
  PARTIAL_RESULT|f_y|2*y + 1
  EVAL_PARTIAL|f_x|8*3 + 2|26
  EVAL_PARTIAL|f_y|2*2 + 1|5
  DOT|(26, 5) · (-3/5, 4/5)|26*(-3/5) + 5*4/5|-11.6
  Z|-11.6
Answer: -11.6
```

### Multivar Chain Rule — `MultivarChainRuleGenerator`  ·  college · difficulty 3

Multivariable chain rule and total differential computations for quadratic functions f(x,y).

**Variants:** `multivar_chain_rule_partial_s`, `multivar_chain_rule_path_derivative`, `multivar_chain_rule_total_diff`

```
Problem: Let z = f(x,y) = 4*x^2 + y^2 + 2*x + y, where x = 3*s - t + 4 and y = 4*s - t - 2. Find dz/ds at (s, t) = (2, -1).
Steps:
  MV_CHAIN_SETUP|z = f(x,y) = 4*x^2 + y^2 + 2*x + y|x = 3*s - t + 4, y = 4*s - t - 2|(s,t) = (2, -1)
  DERIV_RULE|partial chain rule|dz/ds = f_x*x_s + f_y*y_s
  CHAIN_VALUE|x(2,-1)|3*2 + (-1)*(-1) + 4|11
  CHAIN_VALUE|y(2,-1)|4*2 + (-1)*(-1) + (-2)|7
  PARTIAL_RESULT|f_x|8*x + 2
  PARTIAL_RESULT|f_y|2*y + 1
  EVAL_PARTIAL|f_x|8*11 + 2|90
  EVAL_PARTIAL|f_y|2*7 + 1|15
  CHAIN_RATE|x_s|3
  CHAIN_RATE|y_s|4
  CHAIN_SUM|f_x*x_s + f_y*y_s|90*3 + 15*4|330
  Z|330
Answer: 330
```

### Hessian Classify — `HessianClassifyGenerator`  ·  college · difficulty 3

Critical points of quadratic two-variable functions classified by the second-partials / Hessian determinant test.

**Variants:** `hessian_classify_local_max`, `hessian_classify_local_min`, `hessian_classify_saddle`

```
Problem: For f(x,y) = -2*x^2 - 5*y^2 + 16*x + 30*y, find the critical point and classify it using the Hessian test.
Steps:
  HESSIAN_SETUP|f(x,y) = -2*x^2 - 5*y^2 + 16*x + 30*y|find and classify the critical point
  PARTIAL_RESULT|f_x|-4*x + 16
  PARTIAL_RESULT|f_y|-10*y + 30
  CRIT_EQS|f_x = 0|-4*x + 16 = 0
  CRIT_EQS|f_y = 0|-10*y + 30 = 0
  CRIT_SOLVE|det|(-4)*(-10) - 0^2|40
  CRIT_SOLVE|x|160/40|4
  CRIT_SOLVE|y|120/40|3
  CHECK|gradient at (4, 3)|f_x = 0, f_y = 0|critical point
  SECOND_PARTIAL|f_xx|-4
  SECOND_PARTIAL|f_xy|0
  SECOND_PARTIAL|f_yy|-10
  HESSIAN_DET|D = f_xx*f_yy - f_xy^2|(-4)*(-10) - 0^2|40
  HESSIAN_TEST|D = 40|f_xx = -4|local maximum
  Z|critical point (4, 3): local maximum
Answer: critical point (4, 3): local maximum
```

### Lagrange Multiplier — `LagrangeMultiplierGenerator`  ·  college · difficulty 4

One-constraint Lagrange multiplier computations with exact integer optimizers.

**Variants:** `lagrange_multiplier_product_sum`, `lagrange_multiplier_quadratic_line`

```
Problem: Maximize f(x,y) = x^2*y subject to x + y = 12, with x > 0 and y > 0, using Lagrange multipliers.
Steps:
  LAGRANGE_SETUP|f(x,y) = x^2*y|constraint x + y = 12|maximize
  PARTIAL_RESULT|f_x|2*x*y
  PARTIAL_RESULT|f_y|x^2
  GRAD_RESULT|grad g|(1, 1)
  LAGRANGE_EQ|f_x = lambda|2*x*y
  LAGRANGE_EQ|f_y = lambda|x^2
  ELIMINATE_LAMBDA|f_x = f_y|2*y = x
  RATIO|2*y = x|y = x/2
  CONSTRAINT_SUBST|x + y = 12|x = 2*12/3|8
  CONSTRAINT_SUBST|x + y = 12|y = 12/3|4
  EVAL|f(8,4)|8^2*4|256
  CHECK|boundary|product is 0 at x = 0 or y = 0|interior maximum
  Z|maximum at (8, 4); value 256
Answer: maximum at (8, 4); value 256
```

### Double Integral — `DoubleIntegralGenerator`  ·  college · difficulty 3

Double integrals with iterated rectangular bounds, triangular order reversal, and polar conversion.

**Variants:** `double_integral_polar_sector`, `double_integral_rectangle_iterated`, `double_integral_reverse_triangle`

```
Problem: Reverse the order and evaluate int_x=0..8 int_y=0..5*x 2 dy dx.
Steps:
  DOUBLE_SETUP|integrand 2|x:0..8|y:0..5*x
  REGION_REWRITE|0 <= y <= 40|y/5 <= x <= 8
  INNER_ANTIDERIV|dx|2*x
  INNER_EVAL|x=y/5..8|2*(8 - y/5)
  OUTER_EVAL|y=0..40|2*5*8^2/2|320
  Z|reversed y:0..40, x:y/5..8; value 320
Answer: reversed y:0..40, x:y/5..8; value 320
```

### Triple Integral — `TripleIntegralGenerator`  ·  college · difficulty 4

Triple integrals in cylindrical and spherical coordinates.

**Variants:** `triple_integral_cylindrical`, `triple_integral_spherical`

```
Problem: Convert to spherical and evaluate the triple integral of 1 over the ball x^2 + y^2 + z^2 <= 64.
Steps:
  TRIPLE_SETUP|integrand 1|ball radius 8|spherical
  SPHERICAL_CONVERT|1 dV|rho^2*sin(phi) drho dphi dtheta
  SPHERICAL_BOUNDS|rho|0..8
  SPHERICAL_BOUNDS|phi|0..pi
  SPHERICAL_BOUNDS|theta|0..2*pi
  INNER_ANTIDERIV|drho|rho^3/3
  INNER_EVAL|rho=0..8|8^3/3|512/3
  MIDDLE_EVAL|phi=0..pi|int sin(phi) dphi = 2|2
  ANGLE_EVAL|theta=0..2*pi|2*pi
  TRIPLE_EVAL|rho_part * phi_part * angle|512/3*2*2*pi|2048/3*pi
  Z|value 2048/3*pi
Answer: value 2048/3*pi
```

### Jacobian — `JacobianGenerator`  ·  college · difficulty 3

Jacobian determinants and linear change-of-variables area scaling.

**Variants:** `jacobian_area_scale`, `jacobian_determinant`

```
Problem: Use x = 2*u - 5*v, y = -u + 4*v to find the area of the image of 0 <= u <= 9, 0 <= v <= 8.
Steps:
  JAC_SETUP|x = 2*u - 5*v|y = -u + 4*v|d(x,y)/d(u,v)
  PARTIAL_RESULT|x_u|2
  PARTIAL_RESULT|x_v|-5
  PARTIAL_RESULT|y_u|-1
  PARTIAL_RESULT|y_v|4
  JAC_MATRIX|[[x_u, x_v], [y_u, y_v]]|[[2, -5], [-1, 4]]
  JAC_DET|x_u*y_v - x_v*y_u|2*4 - (-5)*(-1)|3
  AREA_SCALE|uv rectangle area|9*8|72
  AREA_SCALE|image area|abs(3)*72|216
  Z|image area 216
Answer: image area 216
```

### Div Curl — `DivCurlGenerator`  ·  college · difficulty 2

Divergence and curl of linear vector fields.

**Variants:** `div_curl_plane`, `div_curl_space`

```
Problem: For F(x,y,z) = <6*x - 6*z, -2*x + 2*y + z, 6*y - 2*z>, compute the divergence and curl.
Steps:
  VECTOR_SETUP|F(x,y,z) = <6*x - 6*z, -2*x + 2*y + z, 6*y - 2*z>|divergence and curl
  PARTIAL_RESULT|P_x|6
  PARTIAL_RESULT|Q_y|2
  PARTIAL_RESULT|R_z|-2
  DIV_SUM|P_x + Q_y + R_z|6 + 2 - 2|6
  PARTIAL_RESULT|R_y|6
  PARTIAL_RESULT|Q_z|1
  CURL_COMPONENT|i|6 - 1|5
  PARTIAL_RESULT|P_z|-6
  PARTIAL_RESULT|R_x|0
  CURL_COMPONENT|j|-6 - 0|-6
  PARTIAL_RESULT|Q_x|-2
  PARTIAL_RESULT|P_y|0
  CURL_COMPONENT|k|-2 - 0|-2
  Z|divergence 6; curl <5, -6, -2>
Answer: divergence 6; curl <5, -6, -2>
```

### Line Integral — `LineIntegralGenerator`  ·  college · difficulty 4

Work line integrals and conservative-field potential functions.

**Variants:** `line_integral_potential_work`, `line_integral_segment_work`

```
Problem: For F(x,y) = <8*x - y + 3, 2*y - x + 2>, find a potential function and compute the work from (2, 0) to (3, 1).
Steps:
  LINE_SETUP|F(x,y) = <8*x - y + 3, 2*y - x + 2>|from (2, 0) to (3, 1)
  PARTIAL_RESULT|P_y|-1
  PARTIAL_RESULT|Q_x|-1
  CHECK|P_y = Q_x|-1 = -1|conservative
  POTENTIAL_BUILD|integrate P dx|4*x^2 - x*y + 3*x + g(y)|g'(y) remains
  POTENTIAL_BUILD|match Q|g'(y) = 2*y + 2|y^2 + 2*y
  POTENTIAL_RESULT|phi(x,y)|4*x^2 + y^2 - x*y + 3*x + 2*y
  EVAL|phi(3,1)|45
  EVAL|phi(2,0)|22
  WORK_DIFF|phi(end) - phi(start)|45 - 22|23
  Z|potential 4*x^2 + y^2 - x*y + 3*x + 2*y; work 23
Answer: potential 4*x^2 + y^2 - x*y + 3*x + 2*y; work 23
```

### Vector Theorem — `VectorTheoremGenerator`  ·  college · difficulty 5

Green's theorem, divergence theorem, and Stokes' theorem computations using the easier side of the theorem.

**Variants:** `vector_theorem_divergence_box`, `vector_theorem_green_rectangle`, `vector_theorem_stokes_disk`

```
Problem: Use the divergence theorem to compute the outward flux of F=<x, -5*y, -z> through the box 0 <= x <= 10, 0 <= y <= 9, 0 <= z <= 8.
Steps:
  THEOREM_SETUP|divergence theorem|F=<x, -5*y, -z>|box 10 by 9 by 8
  PARTIAL_RESULT|P_x|1
  PARTIAL_RESULT|Q_y|-5
  PARTIAL_RESULT|R_z|-1
  THEOREM_REWRITE|outward flux|triple integral of div F
  REGION_MEASURE|volume|10*9*8|720
  FLUX_SUM|(1 - 5 - 1)*720|-3600
  Z|outward flux -3600
Answer: outward flux -3600
```

### Curve Geometry — `CurveGeometryGenerator`  ·  college · difficulty 3

Curve geometry: arc length, curvature, unit tangent, and unit normal.

**Variants:** `curve_geometry_arc_line`, `curve_geometry_circle_tn`

```
Problem: For r(t) = <15*cos(t), 15*sin(t)>, find curvature, unit tangent, and unit normal at t = 0.
Steps:
  CURVE_GEOM_SETUP|r(t) = <15*cos(t), 15*sin(t)>|at t = 0|curvature, T, N
  PATH_DERIV|r'(t)|<-15*sin(t), 15*cos(t)>
  SPEED|norm r'(0)|15
  UNIT_TANGENT|r'(0)/speed|<0, 1>
  CURVATURE_FORMULA|circle|kappa = 1/R
  UNIT_NORMAL|T'(0)/norm T'(0)|<-1, 0>
  Z|curvature 1/15; T(0)=<0, 1>; N(0)=<-1, 0>
Answer: curvature 1/15; T(0)=<0, 1>; N(0)=<-1, 0>
```

### Centroid — `CentroidGenerator`  ·  college · difficulty 4

Centroids of plane regions using area and moment integrals.

**Variants:** `centroid_line_region`, `centroid_parabola_region`

```
Problem: Find the centroid of the region under y = 7*x^2 from x = 0 to x = 2 using moments.
Steps:
  CENTROID_SETUP|0 <= y <= 7*x^2|0 <= x <= 2|centroid
  AREA_INT|A = int y dx|7*2^3/3|56/3
  MOMENT_Y|M_y = int x*y dx|7*2^4/4|28
  MOMENT_X|M_x = 1/2 int y^2 dx|7^2*2^5/10|784/5
  CENTROID_COORD|xbar = M_y/A|(28)/(56/3)|3/2
  CENTROID_COORD|ybar = M_x/A|(784/5)/(56/3)|42/5
  Z|centroid (3/2, 42/5)
Answer: centroid (3/2, 42/5)
```

### LUDecomposition — `LUDecompositionGenerator`  ·  college · difficulty 3

3x3 LU decomposition with a unit lower-triangular L using Doolittle's method and no pivoting.

**Variants:** `lu_decomposition`

```
Problem: Find an LU decomposition A = L*U with unit lower triangular L for A = [[-1, 1, -1], [-2, 6, 0], [-2, -14, -7]].
Steps:
  LU_SETUP|A = [[-1, 1, -1], [-2, 6, 0], [-2, -14, -7]]|unit lower L
  LU_ENTRY|u11|a11 = -1|-1
  LU_ENTRY|u12|a12 = 1|1
  LU_ENTRY|u13|a13 = -1|-1
  LU_ENTRY|l21|(-2)/(-1)|2
  LU_ENTRY|l31|(-2)/(-1)|2
  LU_ENTRY|u22|6 - 2*1|4
  LU_ENTRY|u23|0 - 2*(-1)|2
  LU_ENTRY|l32|((-14) - 2*1)/4|-4
  LU_ENTRY|u33|(-7) - 2*(-1) - (-4)*2|3
  LU_RESULT|L|[[1, 0, 0], [2, 1, 0], [2, -4, 1]]
  LU_RESULT|U|[[-1, 1, -1], [0, 4, 2], [0, 0, 3]]
  CHECK|L*U|[[-1, 1, -1], [-2, 6, 0], [-2, -14, -7]]|matches A
  Z|L=[[1, 0, 0], [2, 1, 0], [2, -4, 1]]; U=[[-1, 1, -1], [0, 4, 2], [0, 0, 3]]
Answer: L=[[1, 0, 0], [2, 1, 0], [2, -4, 1]]; U=[[-1, 1, -1], [0, 4, 2], [0, 0, 3]]
```

### Subspace Basis — `SubspaceBasisGenerator`  ·  college · difficulty 3

RREF, rank, null-space basis, and column-space basis for 3x4 integer matrices. Problems are constructed from a known RREF and integer row additions, so the row-reduction path uses exact integer arithmetic.

**Variants:** `subspace_basis_rank2`, `subspace_basis_rank3`

```
Problem: Find the RREF, rank, null space basis, and column space basis for A = [[0, -1, -1, 4], [1, 1, 0, -2], [1, 0, 0, 2]].
Steps:
  MAT_SETUP|A = [[0, -1, -1, 4], [1, 1, 0, -2], [1, 0, 0, 2]]|RREF, rank, null space, column space
  ROW_OP|R3 -> R3 - R1|[1, 1, 1, -2]
  ROW_OP|R1 -> R1 + R3|[1, 0, 0, 2]
  ROW_OP|R3 -> R3 - R2|[0, 0, 1, 0]
  ROW_OP|R2 -> R2 - R1|[0, 1, 0, -4]
  RREF_RESULT|RREF(A)|[[1, 0, 0, 2], [0, 1, 0, -4], [0, 0, 1, 0]]
  PIVOT_COLS|columns 1, 2, 3|rank = 3
  NULL_REL|x1 + 2*x4 = 0|x1 = -2*x4
  NULL_REL|x2 - 4*x4 = 0|x2 = 4*x4
  NULL_REL|x3 = 0|x3 = 0
  NULL_VECTOR|x4=1|[-2, 4, 0, 1]
  COL_BASIS|original columns 1, 2, 3|[[0, 1, 1], [-1, 1, 0], [-1, 0, 0]]
  Z|rank 3; null basis [[-2, 4, 0, 1]]; column basis [[0, 1, 1], [-1, 1, 0], [-1, 0, 0]]
Answer: rank 3; null basis [[-2, 4, 0, 1]]; column basis [[0, 1, 1], [-1, 1, 0], [-1, 0, 0]]
```

### Eigenvalue — `EigenvalueGenerator`  ·  college · difficulty 3

Eigenvalues and eigenvectors for 2x2 and 3x3 upper-triangular matrices with distinct integer eigenvalues. The characteristic polynomial is shown from det(lambda I - A), then each eigenspace solves (A - lambda I)v = 0.

**Variants:** `eigenvalues_three`, `eigenvalues_two`

```
Problem: Find the characteristic polynomial, eigenvalues, and eigenvectors of A = [[1, 4, 3], [0, -5, 1], [0, 0, -1]].
Steps:
  MAT_SETUP|A = [[1, 4, 3], [0, -5, 1], [0, 0, -1]]|characteristic polynomial and eigenvectors
  CHAR_SETUP|p(λ) = det(λI - A)|triangular determinant
  CHAR_DIAG|diagonal of λI - A|(λ - 1), (λ + 5), (λ + 1)
  CHAR_POLY|p(λ) = λ^3 + 5λ^2 - λ - 5|(λ + 5)*(λ + 1)*(λ - 1)
  EIGENVALUE|λ = -5|p(-5) = 0
  EIGEN_MATRIX|A + 5I|[[6, 4, 3], [0, 0, 1], [0, 0, 4]]
  EIGENVECTOR|A + 5I times v = 0|[2, -3, 0]
  CHECK|A*[2, -3, 0]|[-10, 15, 0]|-5*v = [-10, 15, 0]
  EIGENVALUE|λ = -1|p(-1) = 0
  EIGEN_MATRIX|A + 1I|[[2, 4, 3], [0, -4, 1], [0, 0, 0]]
  EIGENVECTOR|A + 1I times v = 0|[8, -1, -4]
  CHECK|A*[8, -1, -4]|[-8, 1, 4]|-1*v = [-8, 1, 4]
  EIGENVALUE|λ = 1|p(1) = 0
  EIGEN_MATRIX|A - 1I|[[0, 4, 3], [0, -6, 1], [0, 0, -2]]
  EIGENVECTOR|A - 1I times v = 0|[1, 0, 0]
  CHECK|A*[1, 0, 0]|[1, 0, 0]|1*v = [1, 0, 0]
  Z|p(λ)=λ^3 + 5λ^2 - λ - 5 = (λ + 5)*(λ + 1)*(λ - 1); eigenpairs λ=-5: span([2, -3, 0]), λ=-1: span([8, -1, -4]), λ=1: span([1, 0, 0])
Answer: p(λ)=λ^3 + 5λ^2 - λ - 5 = (λ + 5)*(λ + 1)*(λ - 1); eigenpairs λ=-5: span([2, -3, 0]), λ=-1: span([8, -1, -4]), λ=1: span([1, 0, 0])
```

### Diagonalization — `DiagonalizationGenerator`  ·  college · difficulty 4

Diagonalize a 2x2 matrix with two distinct integer eigenvalues and use A^k = P*D^k*P^-1 to compute a matrix power. Matrices are built from a unimodular eigenvector matrix so every displayed matrix stays integral.

**Variants:** `diagonalization_power`

```
Problem: Diagonalize A = [[4, -2], [1, 1]] and compute A^4.
Steps:
  MAT_SETUP|A = [[4, -2], [1, 1]], k = 4|diagonalize and compute A^k
  CHAR_POLY|p(λ) = λ^2 - 5λ + 6|(λ - 2)*(λ - 3)
  EIGENVALUE|λ = 2|p(2) = 0
  EIGENVECTOR|λ = 2|[1, 1]
  CHECK|A*[1, 1]|[2, 2]|2*v = [2, 2]
  EIGENVALUE|λ = 3|p(3) = 0
  EIGENVECTOR|λ = 3|[2, 1]
  CHECK|A*[2, 1]|[6, 3]|3*v = [6, 3]
  DIAG_FORM|P = [[1, 2], [1, 1]]|D = [[2, 0], [0, 3]]|P^-1 = [[-1, 2], [1, -1]]
  CHECK|P*D*P^-1|[[4, -2], [1, 1]]|matches A
  E|2|4|16
  E|3|4|81
  D_POWER|D^4|[[16, 0], [0, 81]]
  POWER_FORM|A^4 = P*D^4*P^-1
  POWER_ENTRY|(1,1)|(-16) + 162|146
  POWER_ENTRY|(1,2)|16*2 + (-162)|-130
  POWER_ENTRY|(2,1)|(-16) + 81|65
  POWER_ENTRY|(2,2)|16*2 + (-81)|-49
  CHECK|direct A^4|[[146, -130], [65, -49]]|matches diagonalization
  Z|P=[[1, 2], [1, 1]], D=[[2, 0], [0, 3]], P^-1=[[-1, 2], [1, -1]], A^4=[[146, -130], [65, -49]]
Answer: P=[[1, 2], [1, 1]], D=[[2, 0], [0, 3]], P^-1=[[-1, 2], [1, -1]], A^4=[[146, -130], [65, -49]]
```

### Gram Schmidt — `GramSchmidtGenerator`  ·  college · difficulty 4

Gram-Schmidt orthogonalization for two vectors in R2 or three vectors in R3. The requested output is an exact orthogonal basis, not a normalized basis, so no radicals are needed.

**Variants:** `gram_schmidt_three`, `gram_schmidt_two`

```
Problem: Apply Gram-Schmidt to vectors [[2, 1, 0], [0, 5, 0], [4, -3, -1]] and give an orthogonal basis, not normalized.
Steps:
  GS_SETUP|vectors [[2, 1, 0], [0, 5, 0], [4, -3, -1]]|orthogonal basis, not normalized
  GS_VECTOR|u1 = v1|[2, 1, 0]
  GS_VECTOR|start v2|[0, 5, 0]
  DOT|v2·u1|5|5
  DOT|u1·u1|2*2 + 1|5
  PROJ_COEFF|v2 on u1|5/5|1
  PROJ_VECTOR|u1|[2, 1, 0]
  GS_SUBTRACT|remove projection on u1|[-2, 4, 0]
  GS_VECTOR|u2|[-2, 4, 0]
  GS_VECTOR|start v3|[4, -3, -1]
  DOT|v3·u1|4*2 + (-3)|5
  DOT|u1·u1|2*2 + 1|5
  PROJ_COEFF|v3 on u1|5/5|1
  PROJ_VECTOR|u1|[2, 1, 0]
  GS_SUBTRACT|remove projection on u1|[2, -4, -1]
  DOT|v3·u2|4*(-2) + (-3)*4|-20
  DOT|u2·u2|(-2)*(-2) + 4*4|20
  PROJ_COEFF|v3 on u2|-20/20|-1
  PROJ_VECTOR|-u2|[2, -4, 0]
  GS_SUBTRACT|remove projection on u2|[0, 0, -1]
  GS_VECTOR|u3|[0, 0, -1]
  CHECK|u1·u2|0|orthogonal
  CHECK|u1·u3|0|orthogonal
  CHECK|u2·u3|0|orthogonal
  Z|orthogonal basis [[2, 1, 0], [-2, 4, 0], [0, 0, -1]]
Answer: orthogonal basis [[2, 1, 0], [-2, 4, 0], [0, 0, -1]]
```

### Least Squares — `LeastSquaresGenerator`  ·  college · difficulty 4

Least-squares line fitting by normal equations. Centered x-values make X^T X diagonal, and residuals are constructed orthogonal to the columns of X so the fitted line, projection, and residual are exact integers.

**Variants:** `least_squares_four_point_line`, `least_squares_three_point_line`

```
Problem: Use normal equations to find the least-squares line y = a + bx for points [(-3, 26), (-1, 22), (1, 16), (3, 8)].
Steps:
  LS_SETUP|points [(-3, 26), (-1, 22), (1, 16), (3, 8)]|model y = a + bx
  DESIGN_MATRIX|X = [[1, -3], [1, -1], [1, 1], [1, 3]]|y = [26, 22, 16, 8]
  NORMAL_EQ|X^T X|[[4, 0], [0, 20]]
  NORMAL_EQ|X^T y|[72, -60]
  D|72|4|18
  D|-60|20|-3
  LS_LINE|a = 18, b = -3|ŷ = 18 - 3x
  PROJECTION|X*beta|[27, 21, 15, 9]
  RESIDUAL|y - X*beta|[-1, 1, 1, -1]
  CHECK|X^T residual|[0, 0]|orthogonal
  Z|ŷ = 18 - 3x; projection [27, 21, 15, 9]; residual [-1, 1, 1, -1]
Answer: ŷ = 18 - 3x; projection [27, 21, 15, 9]; residual [-1, 1, 1, -1]
```

### Integrating Factor — `IntegratingFactorGenerator`  ·  college · difficulty 3

First-order linear differential equations solved by an integrating factor. Coefficients are chosen so the particular coefficient and integration constant are exact integers.

**Variants:** `integrating_factor_constant_rhs`, `integrating_factor_exponential_rhs`

```
Problem: Solve y' + 4y = 8e^(4x) with y(0) = 2 using an integrating factor.
Steps:
  ODE_SETUP|y' + 4y = 8e^(4x), y(0) = 2|integrating factor
  IFACTOR|mu = e^(∫ 4 dx)|e^(4x)
  MULTIPLY_IF|e^(4x)y' + 4e^(4x)y|8e^(8x)
  REWRITE|(e^(4x)y)' = 8e^(8x)
  A|4|4|8
  D|8|8|1
  ANTIDERIV|8e^(8x) dx|e^(8x) + C
  SOLVE_Y|e^(4x)y = e^(8x) + C|y = e^(4x) + Ce^(-4x)
  SUBST|x|0|2 = 1 + C
  S|2|1|1
  Z|y = e^(4x) + e^(-4x)
Answer: y = e^(4x) + e^(-4x)
```

### Exact ODE — `ExactODEGenerator`  ·  college · difficulty 3

Exact first-order differential equations M dx + N dy = 0.

**Variants:** `exact_ode_exact_test`, `exact_ode_not_exact_test`, `exact_ode_solve_exact`

```
Problem: Test whether (4*x - y + 2) dx + (4*x + y + 1) dy = 0 is exact.
Steps:
  ODE_SETUP|(4*x - y + 2) dx + (4*x + y + 1) dy = 0|test exactness
  PARTIAL_RESULT|M_y|-1
  PARTIAL_RESULT|N_x|4
  CHECK|M_y != N_x|-1 != 4|not exact
  Z|not exact because M_y = -1 and N_x = 4
Answer: not exact because M_y = -1 and N_x = 4
```

### ODESubstitution — `ODESubstitutionGenerator`  ·  college · difficulty 4

First-order ODE substitutions.

**Variants:** `ode_substitution_bernoulli`, `ode_substitution_homogeneous`

```
Problem: Solve dy/dx = y/x + 2 with y(1) = -5 using y = vx (x > 0).
Steps:
  ODE_SETUP|dy/dx = y/x + 2, y(1) = -5|homogeneous substitution
  SUBSTITUTION|y = vx|dy/dx = v + x dv/dx
  SUBST|y/x = v|v + x dv/dx = v + 2
  REWRITE|x dv/dx = 2
  SEPARATE|dv = 2 dx/x
  INTEG_RULE|both sides|∫ dv = ∫ 2 dx/x
  ANTIDERIV|dv|v
  ANTIDERIV|2 dx/x|2 ln(x) + C
  REWRITE|v = 2 ln(x) + C
  BACK_SUB|v = y/x|y/x = 2 ln(x) + C
  EVAL|ln(1)|0
  SUBST|x=1|y=-5|-5 = C
  SOLVE_Y|y/x = 2 ln(x) - 5|y = x(2 ln(x) - 5)
  Z|y = x(2 ln(x) - 5)
Answer: y = x(2 ln(x) - 5)
```

### Second Order ODE — `SecondOrderODEGenerator`  ·  college · difficulty 3

Homogeneous second-order constant-coefficient ODEs.

**Variants:** `second_order_ode_complex_roots`, `second_order_ode_distinct_real`, `second_order_ode_repeated_root`

```
Problem: Solve y'' - 6y' + 9y = 0 with y(0) = -4 and y'(0) = -11.
Steps:
  ODE_SETUP|y'' - 6y' + 9y = 0|y(0) = -4, y'(0) = -11
  CHAR_EQ|assume y=e^(rx)|r^2 - 6r + 9 = 0
  FACTOR|r^2 - 6r + 9|(r - 3)^2 = 0
  CHAR_ROOTS|r = 3|repeated
  SOL_FORM|y = (C1 + C2x)e^(3x)
  SUBST|x=0|C1 = -4
  DERIV_FORM|y'|(C2 + 3(C1 + C2x))e^(3x)
  SUBST|x=0|C2 + 3C1 = -11
  M|3|-4|-12
  S|-11|-12|1
  SOLVE_CONST|C1 = -4|C2 = 1
  Z|y = (-4 + x)e^(3x)
Answer: y = (-4 + x)e^(3x)
```

### Undetermined Coeff — `UndeterminedCoeffGenerator`  ·  college · difficulty 4

Undetermined coefficients for nonhomogeneous constant-coefficient ODEs.

**Variants:** `undetermined_coeff_constant_forcing`, `undetermined_coeff_exponential_forcing`

```
Problem: Solve y'' + y' - 12y = -10e^x with y(0) = 6 and y'(0) = 9 by undetermined coefficients.
Steps:
  ODE_SETUP|y'' + y' - 12y = -10e^x|y(0) = 6, y'(0) = 9
  CHAR_EQ|assume y=e^(rx)|r^2 + r - 12 = 0
  FACTOR|r^2 + r - 12|(r + 4)(r - 3) = 0
  CHAR_ROOTS|r1 = -4, r2 = 3|complementary
  HOM_SOL|y_h|y_h = C1e^(-4x) + C2e^(3x)
  UC_GUESS|exponential forcing|y_p = Ae^x
  APPLY_OPERATOR|L[Ae^x]|A(1 + 1 - 12)e^x
  M|1|1|1
  M|1|1|1
  A|1|1|2
  A|2|-12|-10
  D|-10|-10|1
  PARTICULAR|y_p|e^x
  SOL_FORM|y = C1e^(-4x) + C2e^(3x) + e^x
  SUBST|x=0|C1 + C2 + 1 = 6
  S|6|1|5
  DERIV_FORM|y'|-4C1e^(-4x) + 3C2e^(3x) + e^x
  M|1|1|1
  S|9|1|8
  SUBST|x=0|-4C1 + 3C2 = 8
  M|3|5|15
  S|8|15|-7
  S|-4|3|-7
  D|-7|-7|1
  S|5|1|4
  SOLVE_CONST|C1 = 1|C2 = 4
  Z|y = e^(-4x) + 4e^(3x) + e^x
Answer: y = e^(-4x) + 4e^(3x) + e^x
```

### Variation Parameters — `VariationParametersGenerator`  ·  college · difficulty 5

Variation of parameters for second-order constant-coefficient ODEs. The forcing is exponential and not part of the complementary solution, so the Wronskian and u1/u2 integrals are exact by hand.

**Variants:** `variation_parameters_exponential_forcing`

```
Problem: Solve y'' - 7y' + 12y = -60e^(-x) by variation of parameters.
Steps:
  ODE_SETUP|y'' - 7y' + 12y = -60e^(-x)|variation of parameters
  CHAR_EQ|assume y=e^(rx)|r^2 - 7r + 12 = 0
  FACTOR|r^2 - 7r + 12|(r - 3)(r - 4) = 0
  CHAR_ROOTS|r1 = 3, r2 = 4|fundamental solutions
  HOM_SOL|y1, y2|y1 = e^(3x), y2 = e^(4x)
  DERIV_FORM|y1', y2'|y1' = 3e^(3x), y2' = 4e^(4x)
  WRONSKIAN|y1*y2' - y1'*y2|e^(7x)
  VOP_FORM|u1' = -y2*g/W|60/1 * e^(-4x)
  D|60|1|60
  VOP_FORM|u2' = y1*g/W|-60/1 * e^(-5x)
  D|-60|1|-60
  ANTIDERIV|60e^(-4x) dx|-15e^(-4x)
  D|60|-4|-15
  ANTIDERIV|-60e^(-5x) dx|12e^(-5x)
  D|-60|-5|12
  A|-15|12|-3
  PARTICULAR|u1*y1 + u2*y2|-3e^(-x)
  SOL_FORM|y = C1e^(3x) + C2e^(4x) - 3e^(-x)
  Z|y = C1e^(3x) + C2e^(4x) - 3e^(-x)
Answer: y = C1e^(3x) + C2e^(4x) - 3e^(-x)
```

### Laplace IVP — `LaplaceIVPGenerator`  ·  college · difficulty 4

Laplace-transform IVPs with the transform table supplied in the problem.

**Variants:** `laplace_ivp_first_order_exp`

```
Problem: Use Laplace transforms to solve y' + 4y = -32e^(4t), y(0) = -6. Table: L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); L^-1{1/(s-k)} = e^(kt).
Steps:
  ODE_SETUP|y' + 4y = -32e^(4t), y(0) = -6|Laplace transform
  LAPLACE_TABLE|L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); L^-1{1/(s-k)} = e^(kt)
  LAPLACE|L[y' + 4y]|(sY + 6) + 4Y
  LAPLACE|L[-32e^(4t)]|-32/(s - 4)
  SOLVE_Y|(s + 4)Y + 6 = -32/(s - 4)|Y = (-6(s - 4) - 32)/((s + 4)(s - 4))
  PARTIAL_FRAC|Y(s)|-2/(s + 4) - 4/(s - 4)
  A|4|4|8
  M|-6|-8|48
  A|48|-32|16
  D|16|-8|-2
  D|-32|8|-4
  INVERSE_LAPLACE|-2/(s + 4)|-2e^(-4t)
  INVERSE_LAPLACE|-4/(s - 4)|-4e^(4t)
  Z|y = -2e^(-4t) - 4e^(4t)
Answer: y = -2e^(-4t) - 4e^(4t)
```

### ODESystem — `ODESystemGenerator`  ·  college · difficulty 5

Linear systems x' = A x solved by eigenvalues and eigenvectors.

**Variants:** `ode_system_two_by_two_distinct`

```
Problem: Solve x' = A x for A = [[2, 2], [-1, 5]] with x(0) = [-7, -3] using eigenvalues.
Steps:
  ODE_SETUP|A = [[2, 2], [-1, 5]]|x(0) = [-7, -3]
  TRACE|2 + 5|7
  M|2|5|10
  M|2|-1|-2
  S|10|-2|12
  DET2|ad - bc|12
  CHAR_EQ|det(A - rI)|r^2 - 7r + 12 = 0
  EIGENPAIR|lambda = 3|[2, 1]
  CHECK|A*[2, 1]|[6, 3]|3v = [6, 3]
  EIGENPAIR|lambda = 4|[1, 1]
  CHECK|A*[1, 1]|[4, 4]|4v = [4, 4]
  SOL_FORM|x(t)|C1e^(3t)[2, 1] + C2e^(4t)[1, 1]
  INITIAL_SYSTEM|C1[2, 1] + C2[1, 1]|[-7, -3]
  SOLVE_CONST|C1 = -4|C2 = 1
  Z|x(t) = [-8e^(3t) + e^(4t), -4e^(3t) + e^(4t)]
Answer: x(t) = [-8e^(3t) + e^(4t), -4e^(3t) + e^(4t)]
```

### Stability — `StabilityGenerator`  ·  college · difficulty 3

Equilibria and stability for autonomous ODEs dy/dt = f(y).

**Variants:** `stability_factored_polynomial`

```
Problem: For dy/dt = (y + 5)(y + 1)(y - 1), find equilibria and classify stability by sign analysis.
Steps:
  ODE_SETUP|dy/dt = (y + 5)(y + 1)(y - 1)|equilibria and stability
  EQUILIBRIA|f(y) = 0|y=-5, y=-1, y=1
  SIGN_TEST|(-inf, -5)|y = -6|f(y) = -35 (negative)|down
  SIGN_TEST|(-5, -1)|y = -3|f(y) = 16 (positive)|up
  SIGN_TEST|(-1, 1)|y = 0|f(y) = -5 (negative)|down
  SIGN_TEST|(1, inf)|y = 2|f(y) = 21 (positive)|up
  STABILITY|y=-5|left down, right up|unstable
  STABILITY|y=-1|left up, right down|stable
  STABILITY|y=1|left down, right up|unstable
  Z|equilibria: y=-5 unstable; y=-1 stable; y=1 unstable
Answer: equilibria: y=-5 unstable; y=-1 stable; y=1 unstable
```

### Set Operations — `SetOperationsGenerator`  ·  college · difficulty 2

Finite set algebra, power sets, and Cartesian products.

**Variants:** `set_operations_algebra`, `set_operations_cartesian_product`, `set_operations_power_set`

```
Problem: Find the power set P(S) for S = {a, c, d}.
Steps:
  SET_SETUP|S = {a, c, d}|power set
  E|2|3|8
  SUBSET_SIZE|0|{}
  SUBSET_SIZE|1|{a}, {c}, {d}
  SUBSET_SIZE|2|{a, c}, {a, d}, {c, d}
  SUBSET_SIZE|3|{a, c, d}
  POWER_SET_RESULT|{{}, {a}, {c}, {d}, {a, c}, {a, d}, {c, d}, {a, c, d}}
  Z|P(S) = {{}, {a}, {c}, {d}, {a, c}, {a, d}, {c, d}, {a, c, d}}
Answer: P(S) = {{}, {a}, {c}, {d}, {a, c}, {a, d}, {c, d}, {a, c, d}}
```

### Relation Check — `RelationCheckGenerator`  ·  college · difficulty 2

Relation property checks on small finite sets.

**Variants:** `relation_check_property_check`

```
Problem: For A = {1, 2, 3, 4} and R = {(1, 3), (2, 3), (3, 4), (4, 3)}, determine whether R is reflexive, symmetric, antisymmetric, and transitive.
Steps:
  REL_SETUP|A = {1, 2, 3, 4}|R = {(1, 3), (2, 3), (3, 4), (4, 3)}
  REFLEXIVE_CHECK|(1, 1)|missing
  REFLEXIVE_CHECK|(2, 2)|missing
  REFLEXIVE_CHECK|(3, 3)|missing
  REFLEXIVE_CHECK|(4, 4)|missing
  PROPERTY_RESULT|reflexive|no
  SYMMETRIC_CHECK|(1, 3)|reverse (3, 1)|missing
  SYMMETRIC_CHECK|(2, 3)|reverse (3, 2)|missing
  SYMMETRIC_CHECK|(3, 4)|reverse (4, 3)|present
  SYMMETRIC_CHECK|(4, 3)|reverse (3, 4)|present
  PROPERTY_RESULT|symmetric|no
  ANTISYM_CHECK|(1, 3)|reverse (3, 1)|ok
  ANTISYM_CHECK|(2, 3)|reverse (3, 2)|ok
  ANTISYM_CHECK|(3, 4)|reverse (4, 3)|violation
  ANTISYM_CHECK|(4, 3)|reverse (3, 4)|violation
  PROPERTY_RESULT|antisymmetric|no
  TRANSITIVE_CHECK|(1, 3) and (3, 4)|need (1, 4)|missing
  TRANSITIVE_CHECK|(2, 3) and (3, 4)|need (2, 4)|missing
  TRANSITIVE_CHECK|(3, 4) and (4, 3)|need (3, 3)|missing
  TRANSITIVE_CHECK|(4, 3) and (3, 4)|need (4, 4)|missing
  PROPERTY_RESULT|transitive|no
  Z|reflexive no; symmetric no; antisymmetric no; transitive no
Answer: reflexive no; symmetric no; antisymmetric no; transitive no
```

### Inclusion Exclusion — `InclusionExclusionGenerator`  ·  college · difficulty 3

Inclusion-exclusion counting for two and three finite sets.

**Variants:** `inclusion_exclusion_three_sets`, `inclusion_exclusion_two_sets`

```
Problem: In a survey, n(A) = 38, n(B) = 25, n(C) = 31, n(A intersect B) = 14, n(A intersect C) = 13, n(B intersect C) = 12, and n(A intersect B intersect C) = 5. How many are in A union B union C?
Steps:
  IE_SETUP|n(A)=38, n(B)=25, n(C)=31|n(AB)=14, n(AC)=13, n(BC)=12, n(ABC)=5
  IE_FORMULA|n(A union B union C)|n(A)+n(B)+n(C) - n(AB)-n(AC)-n(BC) + n(ABC)
  A|38|25|63
  A|63|31|94
  A|14|13|27
  A|27|12|39
  S|94|39|55
  A|55|5|60
  Z|n(A union B union C) = 60
Answer: n(A union B union C) = 60
```

### Stars And Bars — `StarsAndBarsGenerator`  ·  college · difficulty 3

Stars and bars counts and multinomial coefficients.

**Variants:** `stars_and_bars_multinomial`, `stars_and_bars_nonnegative`, `stars_and_bars_positive`

```
Problem: How many positive integer solutions are there to x1 + ... + x5 = 8?
Steps:
  SB_SETUP|x1+...+x5 = 8|xi >= 1
  SHIFT|yi = xi - 1|y1+...+y5 = 3
  SB_FORMULA|C(n-1, k-1)
  S|8|5|3
  S|8|1|7
  S|5|1|4
  COMB_SETUP|C(7, 4)|n!/(r!(n-r)!)
  REWRITE|numerator|7 * 6 * 5 * 4
  M|7|6|42
  M|42|5|210
  M|210|4|840
  REWRITE|denominator|1 * 2 * 3 * 4
  M|1|2|2
  M|2|3|6
  M|6|4|24
  D|840|24|35
  Z|solutions = 35
Answer: solutions = 35
```

### Derangement — `DerangementGenerator`  ·  college · difficulty 3

Derangement counts by the recurrence D_n=(n-1)(D_(n-1)+D_(n-2)).

**Variants:** `derangement_recurrence`

```
Problem: How many derangements are there of 10 distinct forms?
Steps:
  DERANGE_SETUP|n = 10|no item fixed
  RECURRENCE|D_n|(n-1)(D_(n-1)+D_(n-2))
  INITIAL|D_0 = 1|D_1 = 0
  A|0|1|1
  M|1|1|1
  DERANGE_VALUE|D_2|1
  A|1|0|1
  M|2|1|2
  DERANGE_VALUE|D_3|2
  A|2|1|3
  M|3|3|9
  DERANGE_VALUE|D_4|9
  A|9|2|11
  M|4|11|44
  DERANGE_VALUE|D_5|44
  A|44|9|53
  M|5|53|265
  DERANGE_VALUE|D_6|265
  A|265|44|309
  M|6|309|1854
  DERANGE_VALUE|D_7|1854
  A|1854|265|2119
  M|7|2119|14833
  DERANGE_VALUE|D_8|14833
  A|14833|1854|16687
  M|8|16687|133496
  DERANGE_VALUE|D_9|133496
  A|133496|14833|148329
  M|9|148329|1334961
  DERANGE_VALUE|D_10|1334961
  Z|D_10 = 1334961
Answer: D_10 = 1334961
```

### Recurrence — `RecurrenceGenerator`  ·  college · difficulty 4

Linear recurrences solved by characteristic roots.

**Variants:** `recurrence_constant`, `recurrence_homogeneous`

```
Problem: For n >= 2, a_n = 2 a_(n-1) + 8 a_(n-2) - 36, with a_0 = 0 and a_1 = -6. Use the characteristic-root method to find a_8.
Steps:
  REC_SETUP|a_n = 2 a_(n-1) + 8 a_(n-2) - 36|a_0 = 0, a_1 = -6
  CHAR_POLY|lambda^2 - (2)lambda - (8) = 0|(lambda - (4))(lambda - (-2)) = 0
  CHAR_ROOTS|lambda = 4, -2|distinct
  PARTICULAR_TRY|a_n = K|constant forcing
  A|2|8|10
  S|1|10|-9
  D|-36|-9|4
  PARTICULAR_CHECK|K = 4|2K + 8K - 36 = K
  S|0|4|-4
  S|-6|4|-10
  SHIFT|b_n = a_n - K|b_0 = -4, b_1 = -10
  GENERAL|a_n|C1(4)^n + C2(-2)^n + 4
  INITIAL_EQ|C1 + C2|-4
  INITIAL_EQ|4C1 - 2C2|-10
  M|-2|-4|8
  S|-10|8|-18
  S|4|-2|6
  D|-18|6|-3
  S|-4|-3|-1
  CONST_SOLVE|C1 = -3|C2 = -1
  POW|(4)^8|65536
  M|-3|65536|-196608
  POW|(-2)^8|256
  M|-1|256|-256
  A|-196608|-256|-196864
  A|-196864|4|-196860
  Z|a_8 = -196860
Answer: a_8 = -196860
```

### Boolean Algebra — `BooleanAlgebraGenerator`  ·  college · difficulty 3

Boolean truth-table normal forms and Karnaugh-map simplification.

**Variants:** `boolean_algebra_cnf`, `boolean_algebra_dnf`, `boolean_algebra_kmap`

```
Problem: Truth table for f(A,B,C): 000->0, 001->0, 010->1, 011->0, 100->0, 101->1, 110->0, 111->1. Write a conjunctive normal form (CNF).
Steps:
  BOOL_SETUP|variables A, B, C|CNF from f=0 rows
  TRUTH_ROW|A=0, B=0, C=0|f=0
  MAXTERM|000|A OR B OR C
  TRUTH_ROW|A=0, B=0, C=1|f=0
  MAXTERM|001|A OR B OR NOT C
  TRUTH_ROW|A=0, B=1, C=0|f=1
  TRUTH_ROW|A=0, B=1, C=1|f=0
  MAXTERM|011|A OR NOT B OR NOT C
  TRUTH_ROW|A=1, B=0, C=0|f=0
  MAXTERM|100|NOT A OR B OR C
  TRUTH_ROW|A=1, B=0, C=1|f=1
  TRUTH_ROW|A=1, B=1, C=0|f=0
  MAXTERM|110|NOT A OR NOT B OR C
  TRUTH_ROW|A=1, B=1, C=1|f=1
  CNF_FORM|(A OR B OR C) AND (A OR B OR NOT C) AND (A OR NOT B OR NOT C) AND (NOT A OR B OR C) AND (NOT A OR NOT B OR C)
  Z|CNF = (A OR B OR C) AND (A OR B OR NOT C) AND (A OR NOT B OR NOT C) AND (NOT A OR B OR C) AND (NOT A OR NOT B OR C)
Answer: CNF = (A OR B OR C) AND (A OR B OR NOT C) AND (A OR NOT B OR NOT C) AND (NOT A OR B OR C) AND (NOT A OR NOT B OR C)
```

### Graph Counting — `GraphCountingGenerator`  ·  college · difficulty 3

Graph counting by degree sums and adjacency-matrix powers.

**Variants:** `graph_counting_degree_sequence`, `graph_counting_walk_count`

```
Problem: For the directed graph with adjacency matrix A = [[0, 1, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1], [1, 1, 1, 0]], how many walks of length 2 go from vertex 4 to vertex 2?
Steps:
  GRAPH_SETUP|directed adjacency matrix|4 vertices
  MATRIX_ROW|row 1|0, 1, 0, 0
  MATRIX_ROW|row 2|0, 0, 0, 0
  MATRIX_ROW|row 3|1, 0, 0, 1
  MATRIX_ROW|row 4|1, 1, 1, 0
  WALK_GOAL|length 2|4 to 2
  M|1|1|1
  WALK_TERM|via 1|A[4,1]*A[1,2]|1
  A|0|1|1
  M|1|0|0
  WALK_TERM|via 2|A[4,2]*A[2,2]|0
  A|1|0|1
  M|1|0|0
  WALK_TERM|via 3|A[4,3]*A[3,2]|0
  A|1|0|1
  M|0|1|0
  WALK_TERM|via 4|A[4,4]*A[4,2]|0
  A|1|0|1
  WALK_ENTRY|A^2[4,2]|1
  Z|walks = 1
Answer: walks = 1
```

### Dijkstra — `DijkstraGenerator`  ·  college · difficulty 4

Dijkstra shortest paths with a full distance-table trace.

**Variants:** `dijkstra_trace`

```
Problem: Use Dijkstra's algorithm on the weighted undirected graph with vertices A, B, C, D, E and edges AB=1, AD=3, BC=9, BD=7, CD=5, CE=8, DE=2. Start at E and find shortest distances to all vertices.
Steps:
  GRAPH_SETUP|weighted undirected graph|vertices A, B, C, D, E
  EDGE_WEIGHT|AB|1
  EDGE_WEIGHT|AD|3
  EDGE_WEIGHT|BC|9
  EDGE_WEIGHT|BD|7
  EDGE_WEIGHT|CD|5
  EDGE_WEIGHT|CE|8
  EDGE_WEIGHT|DE|2
  DIJKSTRA_INIT|start E|A=inf, B=inf, C=inf, D=inf, E=0
  SELECT_MIN|E|0
  A|0|8|8
  RELAX|E->C|update inf to 8|via weight 8
  A|0|2|2
  RELAX|E->D|update inf to 2|via weight 2
  DIST_TABLE|visited E|A=inf, B=inf, C=8, D=2, E=0
  SELECT_MIN|D|2
  A|2|3|5
  RELAX|D->A|update inf to 5|via weight 3
  A|2|7|9
  RELAX|D->B|update inf to 9|via weight 7
  A|2|5|7
  RELAX|D->C|update 8 to 7|via weight 5
  DIST_TABLE|visited E, D|A=5, B=9, C=7, D=2, E=0
  SELECT_MIN|A|5
  A|5|1|6
  RELAX|A->B|update 9 to 6|via weight 1
  DIST_TABLE|visited E, D, A|A=5, B=6, C=7, D=2, E=0
  SELECT_MIN|B|6
  A|6|9|15
  RELAX|B->C|keep 7|candidate 15
  DIST_TABLE|visited E, D, A, B|A=5, B=6, C=7, D=2, E=0
  SELECT_MIN|C|7
  DIST_TABLE|visited E, D, A, B, C|A=5, B=6, C=7, D=2, E=0
  Z|distances = A:5, B:6, C:7, D:2, E:0
Answer: distances = A:5, B:6, C:7, D:2, E:0
```

### MST — `MSTGenerator`  ·  college · difficulty 4

Minimum spanning tree traces by Kruskal and Prim.

**Variants:** `mst_kruskal`, `mst_prim`

```
Problem: Find a minimum spanning tree for the weighted undirected graph with vertices A, B, C, D, E and edges AB=2, AC=7, AD=17, AE=16, BC=9, BD=21, BE=13, CD=12, CE=10 using Prim's algorithm starting at A.
Steps:
  MST_SETUP|weighted undirected graph|vertices A, B, C, D, E
  EDGE_WEIGHT|AB|2
  EDGE_WEIGHT|AC|7
  EDGE_WEIGHT|AD|17
  EDGE_WEIGHT|AE|16
  EDGE_WEIGHT|BC|9
  EDGE_WEIGHT|BD|21
  EDGE_WEIGHT|BE|13
  EDGE_WEIGHT|CD|12
  EDGE_WEIGHT|CE|10
  PRIM_START|A
  PRIM_CANDIDATES|visited A|AB=2, AC=7, AE=16, AD=17
  EDGE_CHOOSE|AB|weight 2|add B
  A|0|2|2
  MST_ADD|AB|total 2
  MST_SET|AB
  PRIM_CANDIDATES|visited A, B|AC=7, BC=9, BE=13, AE=16, AD=17, BD=21
  EDGE_CHOOSE|AC|weight 7|add C
  A|2|7|9
  MST_ADD|AC|total 9
  MST_SET|AB, AC
  PRIM_CANDIDATES|visited A, B, C|CE=10, CD=12, BE=13, AE=16, AD=17, BD=21
  EDGE_CHOOSE|CE|weight 10|add E
  A|9|10|19
  MST_ADD|CE|total 19
  MST_SET|AB, AC, CE
  PRIM_CANDIDATES|visited A, B, C, E|CD=12, AD=17, BD=21
  EDGE_CHOOSE|CD|weight 12|add D
  A|19|12|31
  MST_ADD|CD|total 31
  MST_SET|AB, AC, CD, CE
  Z|MST weight = 31; edges = AB, AC, CD, CE
Answer: MST weight = 31; edges = AB, AC, CD, CE
```

### Graph Traversal — `GraphTraversalGenerator`  ·  college · difficulty 3

BFS/DFS visit orders and topological sorting traces.

**Variants:** `graph_traversal_bfs`, `graph_traversal_dfs`, `graph_traversal_topo`

```
Problem: Run DFS from B on the undirected graph with vertices A, B, C, D, E and edges AB, AE, BC, BD, BE, CD, CE, DE. Visit neighbors in alphabetical order.
Steps:
  GRAPH_SETUP|undirected graph|vertices A, B, C, D, E
  ADJ_LIST|A|B, E
  ADJ_LIST|B|A, C, D, E
  ADJ_LIST|C|B, D, E
  ADJ_LIST|D|B, C, E
  ADJ_LIST|E|A, B, C, D
  VISIT|B|B
  DFS_EDGE|B->A|tree
  VISIT|A|B, A
  DFS_EDGE|A->B|skip visited
  DFS_EDGE|A->E|tree
  VISIT|E|B, A, E
  DFS_EDGE|E->A|skip visited
  DFS_EDGE|E->B|skip visited
  DFS_EDGE|E->C|tree
  VISIT|C|B, A, E, C
  DFS_EDGE|C->B|skip visited
  DFS_EDGE|C->D|tree
  VISIT|D|B, A, E, C, D
  DFS_EDGE|D->B|skip visited
  DFS_EDGE|D->C|skip visited
  DFS_EDGE|D->E|skip visited
  DFS_EDGE|C->E|skip visited
  DFS_EDGE|E->D|skip visited
  DFS_EDGE|B->C|skip visited
  DFS_EDGE|B->D|skip visited
  DFS_EDGE|B->E|skip visited
  Z|DFS order = B, A, E, C, D
Answer: DFS order = B, A, E, C, D
```

### Euler Circuit — `EulerCircuitGenerator`  ·  college · difficulty 3

Euler path and circuit construction with degree-parity checks.

**Variants:** `euler_circuit`, `euler_path`

```
Problem: Use Hierholzer's algorithm to find an Euler path in the connected undirected graph with vertices A, B, C, D, E and edges AB, AC, AD, AE, BD, BE, CD. Start at B; when extending the current walk, choose the alphabetically first unused neighbor.
Steps:
  GRAPH_SETUP|connected undirected graph|vertices A, B, C, D, E
  EDGE_LIST|AB, AC, AD, AE, BD, BE, CD
  CHECK|connected|yes
  EDGE_COUNT|unused|7
  ADJ_LIST|A|B, C, D, E
  DEGREE|A|4
  ADJ_LIST|B|A, D, E
  DEGREE|B|3
  ADJ_LIST|C|A, D
  DEGREE|C|2
  ADJ_LIST|D|A, B, C
  DEGREE|D|3
  ADJ_LIST|E|A, B
  DEGREE|E|2
  ODD_VERTICES|B, D|2
  CHECK|degree parity|2 odd vertices -> Euler path
  EULER_START|B|alphabetically first odd vertex
  EULER_STACK|initial|B
  EULER_TRAVERSE|B->A|AB|stack B-A
  S|7|1|6
  EULER_TRAVERSE|A->C|AC|stack B-A-C
  S|6|1|5
  EULER_TRAVERSE|C->D|CD|stack B-A-C-D
  S|5|1|4
  EULER_TRAVERSE|D->A|AD|stack B-A-C-D-A
  S|4|1|3
  EULER_TRAVERSE|A->E|AE|stack B-A-C-D-A-E
  S|3|1|2
  EULER_TRAVERSE|E->B|BE|stack B-A-C-D-A-E-B
  S|2|1|1
  EULER_TRAVERSE|B->D|BD|stack B-A-C-D-A-E-B-D
  S|1|1|0
  EULER_BACKTRACK|D|route suffix D|stack B-A-C-D-A-E-B
  EULER_BACKTRACK|B|route suffix D-B|stack B-A-C-D-A-E
  EULER_BACKTRACK|E|route suffix D-B-E|stack B-A-C-D-A
  EULER_BACKTRACK|A|route suffix D-B-E-A|stack B-A-C-D
  EULER_BACKTRACK|D|route suffix D-B-E-A-D|stack B-A-C
  EULER_BACKTRACK|C|route suffix D-B-E-A-D-C|stack B-A
  EULER_BACKTRACK|A|route suffix D-B-E-A-D-C-A|stack B
  EULER_BACKTRACK|B|route suffix D-B-E-A-D-C-A-B|stack empty
  EULER_ROUTE|B-A-C-D-A-E-B-D|uses 7 edges
  Z|Euler path = B-A-C-D-A-E-B-D
Answer: Euler path = B-A-C-D-A-E-B-D
```

### DPTable — `DPTableGenerator`  ·  college · difficulty 4

Dynamic-programming table filling for common discrete math algorithms.

**Variants:** `dp_table_coin_change`, `dp_table_edit_distance`, `dp_table_knapsack`, `dp_table_lcs`

```
Problem: Fill the coin-change DP table for coins 1, 2, 5 and target 7, counting combinations with unlimited coins. How many ways are there?
Steps:
  DP_SETUP|coin change|target 7
  DP_COINS|1, 2, 5
  DP_ROW|i=0|1, 0, 0, 0, 0, 0, 0, 0
  DP_CELL|i=1,amount=0|base empty set|1
  A|0|1|1
  DP_CELL|i=1,amount=1|without 0, with 1|1
  A|0|1|1
  DP_CELL|i=1,amount=2|without 0, with 1|1
  A|0|1|1
  DP_CELL|i=1,amount=3|without 0, with 1|1
  A|0|1|1
  DP_CELL|i=1,amount=4|without 0, with 1|1
  A|0|1|1
  DP_CELL|i=1,amount=5|without 0, with 1|1
  A|0|1|1
  DP_CELL|i=1,amount=6|without 0, with 1|1
  A|0|1|1
  DP_CELL|i=1,amount=7|without 0, with 1|1
  DP_ROW|i=1|1, 1, 1, 1, 1, 1, 1, 1
  DP_CELL|i=2,amount=0|base empty set|1
  DP_CELL|i=2,amount=1|no coin 2|1
  A|1|1|2
  DP_CELL|i=2,amount=2|without 1, with 1|2
  A|1|1|2
  DP_CELL|i=2,amount=3|without 1, with 1|2
  A|1|2|3
  DP_CELL|i=2,amount=4|without 1, with 2|3
  A|1|2|3
  DP_CELL|i=2,amount=5|without 1, with 2|3
  A|1|3|4
  DP_CELL|i=2,amount=6|without 1, with 3|4
  A|1|3|4
  DP_CELL|i=2,amount=7|without 1, with 3|4
  DP_ROW|i=2|1, 1, 2, 2, 3, 3, 4, 4
  DP_CELL|i=3,amount=0|base empty set|1
  DP_CELL|i=3,amount=1|no coin 5|1
  DP_CELL|i=3,amount=2|no coin 5|2
  DP_CELL|i=3,amount=3|no coin 5|2
  DP_CELL|i=3,amount=4|no coin 5|3
  A|3|1|4
  DP_CELL|i=3,amount=5|without 3, with 1|4
  A|4|1|5
  DP_CELL|i=3,amount=6|without 4, with 1|5
  A|4|2|6
  DP_CELL|i=3,amount=7|without 4, with 2|6
  DP_ROW|i=3|1, 1, 2, 2, 3, 4, 5, 6
  Z|ways = 6
Answer: ways = 6
```

### Algorithm Trace — `AlgorithmTraceGenerator`  ·  college · difficulty 3

Deterministic algorithm state traces after a fixed number of steps.

**Variants:** `algorithm_trace_binary_search`, `algorithm_trace_insertion_sort`, `algorithm_trace_merge_sort`

```
Problem: Trace insertion sort on values 3, 17, 33, 32, 26, 20 for 4 passes. What is the array after those passes?
Steps:
  ALG_SETUP|insertion sort|passes 4|values 3, 17, 33, 32, 26, 20
  INSERT_KEY|pass 1|17|index 1
  COMPARE|arr[0]=3|key 17|stop
  INSERT_PLACE|index 1|3, 17, 33, 32, 26, 20
  ARRAY_STATE|pass 1|3, 17, 33, 32, 26, 20
  INSERT_KEY|pass 2|33|index 2
  COMPARE|arr[1]=17|key 33|stop
  INSERT_PLACE|index 2|3, 17, 33, 32, 26, 20
  ARRAY_STATE|pass 2|3, 17, 33, 32, 26, 20
  INSERT_KEY|pass 3|32|index 3
  COMPARE|arr[2]=33|key 32|shift
  SHIFT|2->3|3, 17, 33, 33, 26, 20
  COMPARE|arr[1]=17|key 32|stop
  INSERT_PLACE|index 2|3, 17, 32, 33, 26, 20
  ARRAY_STATE|pass 3|3, 17, 32, 33, 26, 20
  INSERT_KEY|pass 4|26|index 4
  COMPARE|arr[3]=33|key 26|shift
  SHIFT|3->4|3, 17, 32, 33, 33, 20
  COMPARE|arr[2]=32|key 26|shift
  SHIFT|2->3|3, 17, 32, 32, 33, 20
  COMPARE|arr[1]=17|key 26|stop
  INSERT_PLACE|index 2|3, 17, 26, 32, 33, 20
  ARRAY_STATE|pass 4|3, 17, 26, 32, 33, 20
  Z|array = [3, 17, 26, 32, 33, 20]
Answer: array = [3, 17, 26, 32, 33, 20]
```

### DFASimulation — `DFASimulationGenerator`  ·  college · difficulty 3

DFA simulation with a complete state-sequence trace.

**Variants:** `dfa_simulation_contains_11`, `dfa_simulation_ends_with_one`, `dfa_simulation_even_zeros`

```
Problem: Simulate the DFA with states q0, q1; alphabet 0, 1; start q0; accepting states q1; transitions q0:0->q0,1->q1; q1:0->q0,1->q1 on input 0111111. Give the state sequence and accept/reject result.
Steps:
  DFA_SETUP|states q0, q1|alphabet 0, 1|start q0
  DFA_ACCEPT|q1
  DFA_TRANSITION|q0|0|q0
  DFA_TRANSITION|q0|1|q1
  DFA_TRANSITION|q1|0|q0
  DFA_TRANSITION|q1|1|q1
  DFA_INPUT|0111111
  DFA_STATE|start|q0
  DFA_READ|pos 1|0
  DFA_STEP|q0|0|q0
  DFA_STATE|after 1|q0->q0
  DFA_READ|pos 2|1
  DFA_STEP|q0|1|q1
  DFA_STATE|after 2|q0->q0->q1
  DFA_READ|pos 3|1
  DFA_STEP|q1|1|q1
  DFA_STATE|after 3|q0->q0->q1->q1
  DFA_READ|pos 4|1
  DFA_STEP|q1|1|q1
  DFA_STATE|after 4|q0->q0->q1->q1->q1
  DFA_READ|pos 5|1
  DFA_STEP|q1|1|q1
  DFA_STATE|after 5|q0->q0->q1->q1->q1->q1
  DFA_READ|pos 6|1
  DFA_STEP|q1|1|q1
  DFA_STATE|after 6|q0->q0->q1->q1->q1->q1->q1
  DFA_READ|pos 7|1
  DFA_STEP|q1|1|q1
  DFA_STATE|after 7|q0->q0->q1->q1->q1->q1->q1->q1
  CHECK|q1 in accepting states|accepted
  Z|accepted; states = q0->q0->q1->q1->q1->q1->q1->q1
Answer: accepted; states = q0->q0->q1->q1->q1->q1->q1->q1
```

### Extended Euclid — `ExtendedEuclidGenerator`  ·  college · difficulty 3

Extended Euclidean algorithm with explicit Bezout coefficient rows.

**Variants:** `extended_euclid`

```
Problem: Use the extended Euclidean algorithm to find gcd(444, 366) and coefficients x,y with 444x + 366y = gcd.
Steps:
  EXT_GCD_SETUP|444|366
  BACK_SUB_ROW|r=444|x=1|y=0
  BACK_SUB_ROW|r=366|x=0|y=1
  EUCLID_DIV|444|366|1|78
  M|1|366|366
  S|444|366|78
  M|1|0|0
  S|1|0|1
  M|1|1|1
  S|0|1|-1
  BACK_SUB_ROW|r=78|x=1|y=-1
  EUCLID_DIV|366|78|4|54
  M|4|78|312
  S|366|312|54
  M|4|1|4
  S|0|4|-4
  M|4|-1|-4
  S|1|-4|5
  BACK_SUB_ROW|r=54|x=-4|y=5
  EUCLID_DIV|78|54|1|24
  M|1|54|54
  S|78|54|24
  M|1|-4|-4
  S|1|-4|5
  M|1|5|5
  S|-1|5|-6
  BACK_SUB_ROW|r=24|x=5|y=-6
  EUCLID_DIV|54|24|2|6
  M|2|24|48
  S|54|48|6
  M|2|5|10
  S|-4|10|-14
  M|2|-6|-12
  S|5|-12|17
  BACK_SUB_ROW|r=6|x=-14|y=17
  EUCLID_DIV|24|6|4|0
  M|4|6|24
  S|24|24|0
  M|4|-14|-56
  S|5|-56|61
  M|4|17|68
  S|-6|68|-74
  BACK_SUB_ROW|r=0|x=61|y=-74
  M|444|-14|-6216
  M|366|17|6222
  A|-6216|6222|6
  BEZOUT_CHECK|444*-14 + 366*17|6
  CHECK|gcd is last nonzero remainder|6
  Z|gcd = 6; x = -14; y = 17
Answer: gcd = 6; x = -14; y = 17
```

### Modular Inverse — `ModularInverseGenerator`  ·  college · difficulty 3

Modular inverses and linear congruence solving.

**Variants:** `linear_congruence`, `modular_inverse`

```
Problem: Solve the linear congruence 52x congruent to 8 modulo 20.
Steps:
  MOD_SETUP|linear congruence|a=52|b=8|modulus=20
  GCD_RESULT|gcd(52,20)|4
  CHECK|4 divides 8|solutions exist
  D|52|4|13
  D|8|4|2
  D|20|4|5
  CONGRUENCE_REDUCE|13x congruent to 2|mod 5
  EXT_GCD_SETUP|13|5
  BACK_SUB_ROW|r=13|x=1|y=0
  BACK_SUB_ROW|r=5|x=0|y=1
  EUCLID_DIV|13|5|2|3
  M|2|5|10
  S|13|10|3
  M|2|0|0
  S|1|0|1
  M|2|1|2
  S|0|2|-2
  BACK_SUB_ROW|r=3|x=1|y=-2
  EUCLID_DIV|5|3|1|2
  M|1|3|3
  S|5|3|2
  M|1|1|1
  S|0|1|-1
  M|1|-2|-2
  S|1|-2|3
  BACK_SUB_ROW|r=2|x=-1|y=3
  EUCLID_DIV|3|2|1|1
  M|1|2|2
  S|3|2|1
  M|1|-1|-1
  S|1|-1|2
  M|1|3|3
  S|-2|3|-5
  BACK_SUB_ROW|r=1|x=2|y=-5
  EUCLID_DIV|2|1|2|0
  M|2|1|2
  S|2|2|0
  M|2|2|4
  S|-1|4|-5
  M|2|-5|-10
  S|3|-10|13
  BACK_SUB_ROW|r=0|x=-5|y=13
  GCD_RESULT|gcd(13,5)|1
  MOD_NORMALIZE|2|mod 5|2
  MOD_INVERSE|13 mod 5|2
  M|2|2|4
  MOD_REDUCE|4|mod 5|4
  CONGRUENCE_SOLUTIONS|base 4|step 5|4, 9, 14, 19
  Z|solutions mod 20 = 4, 9, 14, 19
Answer: solutions mod 20 = 4, 9, 14, 19
```

### CRT — `CRTGenerator`  ·  college · difficulty 4

Chinese Remainder Theorem construction for pairwise-coprime moduli.

**Variants:** `crt`

```
Problem: Solve the CRT system x congruent to 1 modulo 3; x congruent to 4 modulo 7; x congruent to 7 modulo 13. Give the least nonnegative solution modulo the product.
Steps:
  CRT_SETUP|3 congruences
  CRT_TOTAL_MODULUS|3, 7, 13|273
  CRT_CONGRUENCE|i=1|x=1|mod 3
  CRT_CONGRUENCE|i=2|x=4|mod 7
  CRT_CONGRUENCE|i=3|x=7|mod 13
  D|273|3|91
  CRT_FACTOR|i=1|M_i=91|mod 3
  MOD_INVERSE|91 mod 3|1
  M|1|91|91
  M|91|1|91
  CRT_TERM|i=1|91
  A|0|91|91
  D|273|7|39
  CRT_FACTOR|i=2|M_i=39|mod 7
  MOD_INVERSE|39 mod 7|2
  M|4|39|156
  M|156|2|312
  CRT_TERM|i=2|312
  A|91|312|403
  D|273|13|21
  CRT_FACTOR|i=3|M_i=21|mod 13
  MOD_INVERSE|21 mod 13|5
  M|7|21|147
  M|147|5|735
  CRT_TERM|i=3|735
  A|403|735|1138
  MOD_REDUCE|1138|mod 273|46
  MOD_REDUCE|46|mod 3|1
  CRT_CHECK|i=1|1|1
  MOD_REDUCE|46|mod 7|4
  CRT_CHECK|i=2|4|4
  MOD_REDUCE|46|mod 13|7
  CRT_CHECK|i=3|7|7
  Z|x = 46 mod 273
Answer: x = 46 mod 273
```

### Mod Exp — `ModExpGenerator`  ·  college · difficulty 3

Fast modular exponentiation by left-to-right square-and-multiply.

**Variants:** `mod_exp`

```
Problem: Use square-and-multiply to compute 33^56 modulo 49.
Steps:
  MODEXP_SETUP|base 33|exponent 56|modulus 49
  MOD_REDUCE|33|mod 49|33
  BINARY_EXPONENT|56|111000
  M|1|1|1
  MOD_REDUCE|1|mod 49|1
  MODEXP_SQUARE|bit 1=1|1
  M|1|33|33
  MOD_REDUCE|33|mod 49|33
  MODEXP_MULTIPLY|bit 1=1|33
  MODEXP_STATE|after bit 1|33
  M|33|33|1089
  MOD_REDUCE|1089|mod 49|11
  MODEXP_SQUARE|bit 2=1|11
  M|11|33|363
  MOD_REDUCE|363|mod 49|20
  MODEXP_MULTIPLY|bit 2=1|20
  MODEXP_STATE|after bit 2|20
  M|20|20|400
  MOD_REDUCE|400|mod 49|8
  MODEXP_SQUARE|bit 3=1|8
  M|8|33|264
  MOD_REDUCE|264|mod 49|19
  MODEXP_MULTIPLY|bit 3=1|19
  MODEXP_STATE|after bit 3|19
  M|19|19|361
  MOD_REDUCE|361|mod 49|18
  MODEXP_SQUARE|bit 4=0|18
  MODEXP_MULTIPLY|bit 4=0|skip
  MODEXP_STATE|after bit 4|18
  M|18|18|324
  MOD_REDUCE|324|mod 49|30
  MODEXP_SQUARE|bit 5=0|30
  MODEXP_MULTIPLY|bit 5=0|skip
  MODEXP_STATE|after bit 5|30
  M|30|30|900
  MOD_REDUCE|900|mod 49|18
  MODEXP_SQUARE|bit 6=0|18
  MODEXP_MULTIPLY|bit 6=0|skip
  MODEXP_STATE|after bit 6|18
  Z|33^56 mod 49 = 18
Answer: 33^56 mod 49 = 18
```

### Totient — `TotientGenerator`  ·  college · difficulty 3

Euler totient computation and Fermat/Euler power reductions.

**Variants:** `totient_euler_power`, `totient_fermat_power`, `totient_totient`

```
Problem: Use Euler's theorem to reduce 7^96 modulo 48.
Steps:
  FACTOR_SETUP|48
  FACTOR_FOUND|2|4
  FACTOR_FOUND|3|1
  FACTOR_FORM|48|2^4 * 3
  D|48|2|24
  S|2|1|1
  M|24|1|24
  PHI_STEP|p=2|24
  D|24|3|8
  S|3|1|2
  M|8|2|16
  PHI_STEP|p=3|16
  TOTIENT_RESULT|phi(48)|16
  GCD_RESULT|gcd(7,48)|1
  CHECK|gcd = 1|Euler applies
  MOD_REDUCE|96|mod 16|0
  POWER_REDUCE|7^96|7^0 mod 48
  MOD_POWER|7^0|mod 48|1
  Z|7^96 mod 48 = 1
Answer: 7^96 mod 48 = 1
```

### Continued Fraction — `ContinuedFractionGenerator`  ·  college · difficulty 4

Simple continued fractions and convergents for positive rationals.

**Variants:** `continued_fraction`

```
Problem: Find the simple continued fraction for 541/110 and list all convergents.
Steps:
  CF_SETUP|541/110
  EUCLID_DIV|541|110|4|101
  M|4|110|440
  S|541|440|101
  CF_PARTIAL|a_0|4
  EUCLID_DIV|110|101|1|9
  M|1|101|101
  S|110|101|9
  CF_PARTIAL|a_1|1
  EUCLID_DIV|101|9|11|2
  M|11|9|99
  S|101|99|2
  CF_PARTIAL|a_2|11
  EUCLID_DIV|9|2|4|1
  M|4|2|8
  S|9|8|1
  CF_PARTIAL|a_3|4
  EUCLID_DIV|2|1|2|0
  M|2|1|2
  S|2|2|0
  CF_PARTIAL|a_4|2
  CF_RESULT|[4; 1, 11, 4, 2]
  CONV_INIT|h_-2=0,h_-1=1|k_-2=1,k_-1=0
  M|4|1|4
  A|4|0|4
  M|4|0|0
  A|0|1|1
  CONV_STEP|i=0|h=4|k=1
  CONVERGENT|i=0|4/1
  M|1|4|4
  A|4|1|5
  M|1|1|1
  A|1|0|1
  CONV_STEP|i=1|h=5|k=1
  CONVERGENT|i=1|5/1
  M|11|5|55
  A|55|4|59
  M|11|1|11
  A|11|1|12
  CONV_STEP|i=2|h=59|k=12
  CONVERGENT|i=2|59/12
  M|4|59|236
  A|236|5|241
  M|4|12|48
  A|48|1|49
  CONV_STEP|i=3|h=241|k=49
  CONVERGENT|i=3|241/49
  M|2|241|482
  A|482|59|541
  M|2|49|98
  A|98|12|110
  CONV_STEP|i=4|h=541|k=110
  CONVERGENT|i=4|541/110
  Z|continued fraction = [4; 1, 11, 4, 2]; convergents = 4/1, 5/1, 59/12, 241/49, 541/110
Answer: continued fraction = [4; 1, 11, 4, 2]; convergents = 4/1, 5/1, 59/12, 241/49, 541/110
```

### RSA — `RSAGenerator`  ·  college · difficulty 4

RSA key generation, encryption, and decryption with small primes.

**Variants:** `rsa`

```
Problem: For RSA primes p=23 and q=29 with public exponent e=17 and message m=43, compute n, phi(n), d, encrypt, and decrypt.
Steps:
  RSA_SETUP|p=23|q=29|message=43
  M|23|29|667
  S|23|1|22
  S|29|1|28
  M|22|28|616
  GCD_RESULT|gcd(17,616)|1
  EXT_GCD_SETUP|17|616
  BACK_SUB_ROW|r=17|x=1|y=0
  BACK_SUB_ROW|r=616|x=0|y=1
  EUCLID_DIV|17|616|0|17
  M|0|616|0
  S|17|0|17
  M|0|0|0
  S|1|0|1
  M|0|1|0
  S|0|0|0
  BACK_SUB_ROW|r=17|x=1|y=0
  EUCLID_DIV|616|17|36|4
  M|36|17|612
  S|616|612|4
  M|36|1|36
  S|0|36|-36
  M|36|0|0
  S|1|0|1
  BACK_SUB_ROW|r=4|x=-36|y=1
  EUCLID_DIV|17|4|4|1
  M|4|4|16
  S|17|16|1
  M|4|-36|-144
  S|1|-144|145
  M|4|1|4
  S|0|4|-4
  BACK_SUB_ROW|r=1|x=145|y=-4
  EUCLID_DIV|4|1|4|0
  M|4|1|4
  S|4|4|0
  M|4|145|580
  S|-36|580|-616
  M|4|-4|-16
  S|1|-16|17
  BACK_SUB_ROW|r=0|x=-616|y=17
  MOD_NORMALIZE|145|mod 616|145
  MOD_INVERSE|17 mod 616|145
  M|17|145|2465
  MOD_REDUCE|2465|mod 616|1
  CHECK|e*d mod phi|1
  RSA_PUBLIC_KEY|n=667|e=17
  RSA_PRIVATE_KEY|d=145
  MOD_POWER|43^17|mod 667|214
  RSA_ENCRYPT|43|214
  MOD_POWER|214^145|mod 667|43
  RSA_DECRYPT|214|43
  CHECK|decrypted message|43
  Z|n = 667; phi = 616; d = 145; ciphertext = 214; decrypted = 43
Answer: n = 667; phi = 616; d = 145; ciphertext = 214; decrypted = 43
```

### Diffie Hellman — `DiffieHellmanGenerator`  ·  college · difficulty 3

Diffie-Hellman key exchange over a small prime field.

**Variants:** `diffie_hellman`

```
Problem: For Diffie-Hellman with prime p=41, generator g=30, Alice secret a=4, and Bob secret b=18, compute both public keys and the shared secret.
Steps:
  DH_SETUP|p=41|g=30
  DH_SECRET|Alice|4
  DH_SECRET|Bob|18
  MOD_POWER|30^4|mod 41|4
  DH_PUBLIC|Alice|4
  MOD_POWER|30^18|mod 41|21
  DH_PUBLIC|Bob|21
  MOD_POWER|21^4|mod 41|18
  DH_SHARED|Alice|18
  MOD_POWER|4^18|mod 41|18
  DH_SHARED|Bob|18
  CHECK|shared secrets match|18
  Z|Alice public = 4; Bob public = 21; shared secret = 18
Answer: Alice public = 4; Bob public = 21; shared secret = 18
```

### Cayley Table — `CayleyTableGenerator`  ·  college · difficulty 3

Cayley tables and element orders for small finite groups.

**Variants:** `cayley_table_d3`, `cayley_table_units`, `cayley_table_zn`

```
Problem: Build the Cayley table for U(28) under multiplication modulo 28 and find the order of element 17.
Steps:
  GROUP_SETUP|U(28)|multiplication mod n
  CAYLEY_HEADER|1, 3, 5, 9, 11, 13, 15, 17, 19, 23, 25, 27
  CAYLEY_ROW|row 1|1, 3, 5, 9, 11, 13, 15, 17, 19, 23, 25, 27
  CAYLEY_ROW|row 3|3, 9, 15, 27, 5, 11, 17, 23, 1, 13, 19, 25
  CAYLEY_ROW|row 5|5, 15, 25, 17, 27, 9, 19, 1, 11, 3, 13, 23
  CAYLEY_ROW|row 9|9, 27, 17, 25, 15, 5, 23, 13, 3, 11, 1, 19
  CAYLEY_ROW|row 11|11, 5, 27, 15, 9, 3, 25, 19, 13, 1, 23, 17
  CAYLEY_ROW|row 13|13, 11, 9, 5, 3, 1, 27, 25, 23, 19, 17, 15
  CAYLEY_ROW|row 15|15, 17, 19, 23, 25, 27, 1, 3, 5, 9, 11, 13
  CAYLEY_ROW|row 17|17, 23, 1, 13, 19, 25, 3, 9, 15, 27, 5, 11
  CAYLEY_ROW|row 19|19, 1, 11, 3, 13, 23, 5, 15, 25, 17, 27, 9
  CAYLEY_ROW|row 23|23, 13, 3, 11, 1, 19, 9, 27, 17, 25, 15, 5
  CAYLEY_ROW|row 25|25, 19, 13, 1, 23, 17, 11, 5, 27, 15, 9, 3
  CAYLEY_ROW|row 27|27, 25, 23, 19, 17, 15, 13, 11, 9, 5, 3, 1
  ORDER_START|17|identity 1
  M|1|17|17
  MOD_REDUCE|17|mod 28|17
  ORDER_STEP|k=1|17
  M|17|17|289
  MOD_REDUCE|289|mod 28|9
  ORDER_STEP|k=2|9
  M|9|17|153
  MOD_REDUCE|153|mod 28|13
  ORDER_STEP|k=3|13
  M|13|17|221
  MOD_REDUCE|221|mod 28|25
  ORDER_STEP|k=4|25
  M|25|17|425
  MOD_REDUCE|425|mod 28|5
  ORDER_STEP|k=5|5
  M|5|17|85
  MOD_REDUCE|85|mod 28|1
  ORDER_STEP|k=6|1
  ELEMENT_ORDER|17|6
  Z|order(17) = 6
Answer: order(17) = 6
```

### Cyclic Group — `CyclicGroupGenerator`  ·  college · difficulty 3

Cyclic subgroups and generator checks in small modular groups.

**Variants:** `cyclic_group_units`, `cyclic_group_zn`

```
Problem: Find the cyclic subgroup generated by 17 in U(28) under multiplication modulo 28. Is it a generator of the group?
Steps:
  GROUP_SETUP|U(28)|multiplication mod n|group size 12
  CYCLIC_START|17|identity 1
  M|1|17|17
  MOD_REDUCE|17|mod 28|17
  SUBGROUP_ELEM|k=1|17
  M|17|17|289
  MOD_REDUCE|289|mod 28|9
  SUBGROUP_ELEM|k=2|9
  M|9|17|153
  MOD_REDUCE|153|mod 28|13
  SUBGROUP_ELEM|k=3|13
  M|13|17|221
  MOD_REDUCE|221|mod 28|25
  SUBGROUP_ELEM|k=4|25
  M|25|17|425
  MOD_REDUCE|425|mod 28|5
  SUBGROUP_ELEM|k=5|5
  M|5|17|85
  MOD_REDUCE|85|mod 28|1
  SUBGROUP_ELEM|k=6|1
  CYCLIC_SUBGROUP|{1, 17, 9, 13, 25, 5}|6
  CHECK|subgroup size = group size|no
  Z|<17> = {1, 17, 9, 13, 25, 5}; generator = no
Answer: <17> = {1, 17, 9, 13, 25, 5}; generator = no
```

### Permutation Group — `PermutationGroupGenerator`  ·  college · difficulty 3

Permutation composition, cycle notation, order, and parity.

**Variants:** `permutation_group`

```
Problem: In S_5, let sigma=[5, 3, 2, 1, 4] and tau=[1, 5, 2, 3, 4], where each list gives images of 1..5. Compute sigma after tau, then give cycle notation, order, and parity.
Steps:
  PERM_SETUP|n=5|sigma=[5, 3, 2, 1, 4]|tau=[1, 5, 2, 3, 4]
  PERM_COMPOSE|i=1|tau(i)=1|sigma(tau(i))=5
  PERM_COMPOSE|i=2|tau(i)=5|sigma(tau(i))=4
  PERM_COMPOSE|i=3|tau(i)=2|sigma(tau(i))=3
  PERM_COMPOSE|i=4|tau(i)=3|sigma(tau(i))=2
  PERM_COMPOSE|i=5|tau(i)=4|sigma(tau(i))=1
  PERM_RESULT|[5, 4, 3, 2, 1]
  CYCLE_TRACE|start 1|1->5->1
  CYCLE|(1 5)
  CYCLE_TRACE|start 2|2->4->2
  CYCLE|(2 4)
  CYCLE_LENGTHS|2, 2
  GCD_RESULT|gcd(1,2)|1
  LCM_STEP|1|2|2
  GCD_RESULT|gcd(2,2)|2
  LCM_STEP|2|2|2
  S|2|1|1
  A|0|1|1
  S|2|1|1
  A|1|1|2
  PARITY|transpositions 2|even
  Z|composition = [5, 4, 3, 2, 1]; cycles = (1 5)(2 4); order = 2; parity = even
Answer: composition = [5, 4, 3, 2, 1]; cycles = (1 5)(2 4); order = 2; parity = even
```

### Euler Formula — `EulerFormulaGenerator`  ·  college · difficulty 3

Euler's formula conversions among rectangular, polar, and exponential complex forms, including Euler's identity.

**Variants:** `euler_formula_identity`, `euler_formula_polar_to_forms`, `euler_formula_rect_to_forms`

```
Problem: Convert z = 2 cis(270 deg) to rectangular and exponential form.
Steps:
  EULER_SETUP|polar to rectangular/exponential|r=2|theta=270 deg
  EULER_FORMULA|e^(i theta)=cos theta+i sin theta
  TABLE_LOOKUP|cos 270 deg|0
  TABLE_LOOKUP|sin 270 deg|-1
  SCALE_EXACT|2*cos|0
  SCALE_EXACT|2*sin|-2
  RECT_FORM|-2i
  EXP_FORM|2 e^(i*3pi/2)
  Z|rectangular = -2i; exponential = 2 e^(i*3pi/2)
Answer: rectangular = -2i; exponential = 2 e^(i*3pi/2)
```

### De Moivre — `DeMoivreGenerator`  ·  college · difficulty 3

De Moivre powers, roots of unity, and roots of arbitrary complex numbers.

**Variants:** `de_moivre_arbitrary_roots`, `de_moivre_power`, `de_moivre_roots_unity`

```
Problem: Find all 8-th roots of unity in polar form.
Steps:
  DEMOIVRE_SETUP|roots_of_unity|n=8
  M|360|0|0
  D|0|8|0
  ROOT_ANGLE|k=0|0 deg
  ROOT|cis(0 deg)
  M|360|1|360
  D|360|8|45
  ROOT_ANGLE|k=1|45 deg
  ROOT|cis(45 deg)
  M|360|2|720
  D|720|8|90
  ROOT_ANGLE|k=2|90 deg
  ROOT|cis(90 deg)
  M|360|3|1080
  D|1080|8|135
  ROOT_ANGLE|k=3|135 deg
  ROOT|cis(135 deg)
  M|360|4|1440
  D|1440|8|180
  ROOT_ANGLE|k=4|180 deg
  ROOT|cis(180 deg)
  M|360|5|1800
  D|1800|8|225
  ROOT_ANGLE|k=5|225 deg
  ROOT|cis(225 deg)
  M|360|6|2160
  D|2160|8|270
  ROOT_ANGLE|k=6|270 deg
  ROOT|cis(270 deg)
  M|360|7|2520
  D|2520|8|315
  ROOT_ANGLE|k=7|315 deg
  ROOT|cis(315 deg)
  Z|roots = cis(0 deg), cis(45 deg), cis(90 deg), cis(135 deg), cis(180 deg), cis(225 deg), cis(270 deg), cis(315 deg)
Answer: roots = cis(0 deg), cis(45 deg), cis(90 deg), cis(135 deg), cis(180 deg), cis(225 deg), cis(270 deg), cis(315 deg)
```

### Complex Locus — `ComplexLocusGenerator`  ·  college · difficulty 3

Complex loci converted to Cartesian equations.

**Variants:** `complex_locus_bisector`, `complex_locus_circle`

```
Problem: Identify the locus |z - (1,-5)| = |z - (-1,3)|, where z=x+iy. Give the Cartesian equation and type.
Steps:
  LOCUS_SETUP|z=x+iy|p=(1,-5)|q=(-1,3)
  DIST_FORMULA|(x - 1)^2+(y + 5)^2 = (x + 1)^2+(y - 3)^2
  EXPAND|cancel x^2 and y^2
  S|-1|1|-2
  M|2|-2|-4
  S|3|-5|8
  M|2|8|16
  E|1|2|1
  E|-5|2|25
  A|1|25|26
  E|-1|2|1
  E|3|2|9
  A|1|9|10
  S|26|10|16
  LINE_EQ|-4x + 16y + 16 = 0
  Z|-4x + 16y + 16 = 0; type = line
Answer: -4x + 16y + 16 = 0; type = line
```

### Fractal Iteration — `FractalIterationGenerator`  ·  college · difficulty 3

Mandelbrot/Julia escape iteration z <- z^2 + c with exact rational arithmetic and |z| > 2 checks.

**Variants:** `fractal_iteration_julia`, `fractal_iteration_mandelbrot`

```
Problem: Trace the julia iteration z <- z^2 + c for 5 iterations from z0=(-3/2,-1/2) with c=(1/2,0). Report the first step with |z| > 2, if any.
Steps:
  FRACTAL_SETUP|julia|z0=(-3/2,-1/2)|c=(1/2,0)|N=5
  E|-3/2|2|9/4
  E|-1/2|2|1/4
  S|9/4|1/4|2
  M|2|-3/2|-3
  M|-3|-1/2|3/2
  A|2|1/2|5/2
  A|3/2|0|3/2
  ITERATE|n=1|z=(5/2,3/2)
  E|5/2|2|25/4
  E|3/2|2|9/4
  A|25/4|9/4|17/2
  ESCAPE_CHECK|n=1|norm2=17/2|escaped
  Z|escaped at step 1
Answer: escaped at step 1
```

### Cauchy Riemann — `CauchyRiemannGenerator`  ·  college · difficulty 3

Cauchy-Riemann verification and harmonic conjugates for polynomial real/imaginary parts.

**Variants:** `cauchy_riemann_harmonic_conjugate`, `cauchy_riemann_verify`

```
Problem: For a=3, b=-5, c=-1, let u=a(x^2-y^2)+b*x-c*y. Find a harmonic conjugate v with constant 0.
Steps:
  HARMONIC_SETUP|u=3x^2 - 3y^2 - 5x + y
  PARTIAL|u_x|6x - 5
  PARTIAL|u_y|-6y + 1
  INTEGRATE|v_y = u_x|v=6xy - x - 5y + phi(x)
  PARTIAL|v_x|6y - 1
  CHECK|v_x = -u_y|yes
  Z|v = 6xy - x - 5y
Answer: v = 6xy - x - 5y
```

### Great Circle — `GreatCircleGenerator`  ·  college · difficulty 3

Great-circle distances from latitude and longitude using the spherical law of cosines with all needed trig/arccos values supplied.

**Variants:** `great_circle_distance`

```
Problem: On a sphere of radius 18, point A is at latitude 90 deg, longitude -150 deg, and point B is at latitude 30 deg, longitude -90 deg. The longitude difference is 60 deg. Given sin(lat1)=1, sin(lat2)=1/2, cos(lat1)=0, cos(lat2)=sqrt(3)/2, cos(delta)=1/2, and arccos(1/2)=pi/3, find the great-circle distance.
Steps:
  GREAT_CIRCLE_SETUP|R=18|A=(90,-150)|B=(30,-90)
  SPHERICAL_COSINES|cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)
  TRIG_VALUE|sin(lat1)=1|sin(lat2)=1/2|cos(dlon)=1/2
  TRIG_VALUE|cos(lat1)=0|cos(lat2)=sqrt(3)/2
  M|1|1/2|1/2
  M|0|sqrt(3)/2|0
  M|0|1/2|0
  A|1/2|0|1/2
  ARCCOS|cos(c)=1/2|c=pi/3
  M|18|pi/3|6pi
  Z|distance = 6pi
Answer: distance = 6pi
```

### Spherical Excess — `SphericalExcessGenerator`  ·  college · difficulty 3

Spherical triangle area by Girard's theorem: area = (A + B + C - 180 degrees) in radians times R^2.

**Variants:** `spherical_excess_area`

```
Problem: A spherical triangle on a sphere of radius 14 has angles 120 deg, 30 deg, and 90 deg. Use Girard's theorem to find its exact area in terms of pi.
Steps:
  SPHERICAL_EXCESS_SETUP|R=14|angles=120,30,90
  THEOREM|Girard|area = (A+B+C-180 deg)/180 * pi * R^2
  A|120|30|150
  A|150|90|240
  S|240|180|60
  D|60|180|1/3
  E|14|2|196
  M|1/3|196|196/3
  Z|area = 196pi/3
Answer: area = 196pi/3
```

### Hyperbolic Function — `HyperbolicFunctionGenerator`  ·  college · difficulty 3

Evaluate sinh, cosh, and tanh from supplied exact e^x and e^-x values, then verify cosh^2(x) - sinh^2(x) = 1.

**Variants:** `hyperbolic_function_eval`

```
Problem: Given e^x = 27/10 and e^(-x) = 10/27, compute sinh x, cosh x, and tanh x.
Steps:
  HYPERBOLIC_SETUP|e^x=27/10|e^(-x)=10/27
  FORMULA|sinh x = (e^x - e^(-x))/2
  S|27/10|10/27|629/270
  D|629/270|2|629/540
  FORMULA|cosh x = (e^x + e^(-x))/2
  A|27/10|10/27|829/270
  D|829/270|2|829/540
  FORMULA|tanh x = sinh x / cosh x
  D|629/540|829/540|629/829
  E|829/540|2|687241/291600
  E|629/540|2|395641/291600
  S|687241/291600|395641/291600|1
  CHECK|cosh^2 x - sinh^2 x|1|identity holds
  Z|sinh x = 629/540, cosh x = 829/540, tanh x = 629/829
Answer: sinh x = 629/540, cosh x = 829/540, tanh x = 629/829
```

### Angle Defect — `AngleDefectGenerator`  ·  college · difficulty 3

Hyperbolic triangle area from angle defect: area = (180 degrees - A - B - C) in radians times R^2.

**Variants:** `hyperbolic_angle_defect_area`

```
Problem: A hyperbolic triangle with curvature radius 14 has angles 60 deg, 15 deg, and 45 deg. Use the angle defect formula to find its exact area in terms of pi.
Steps:
  ANGLE_DEFECT_SETUP|R=14|angles=60,15,45
  THEOREM|hyperbolic angle defect|area = (180 deg - (A+B+C))/180 * pi * R^2
  A|60|15|75
  A|75|45|120
  S|180|120|60
  D|60|180|1/3
  E|14|2|196
  M|1/3|196|196/3
  Z|area = 196pi/3
Answer: area = 196pi/3
```

### Hermitian Check — `HermitianCheckGenerator`  ·  college · difficulty 3

Hermitian and unitary verification for 2x2 matrices.

**Variants:** `hermitian_check_hermitian`, `hermitian_check_unitary`

```
Problem: Check whether U=[[4/5,-3/5],[3/5,4/5]] is unitary.
Steps:
  MATRIX_SETUP|unitary|U=[[4/5,-3/5],[3/5,4/5]]
  ADJOINT|U^dagger=[[4/5,3/5],[-3/5,4/5]]
  E|4/5|2|16/25
  E|3/5|2|9/25
  A|16/25|9/25|1
  M|4/5|-3/5|-12/25
  M|3/5|4/5|12/25
  A|-12/25|12/25|0
  CHECK|U^dagger U|I|unitary
  Z|unitary yes; U^dagger U = I
Answer: unitary yes; U^dagger U = I
```

### Tensor Product — `TensorProductGenerator`  ·  college · difficulty 3

Build a 4x4 operator from a 2x2 diagonal tensor product and apply it to a product state.

**Variants:** `tensor_product_diagonal_apply`

```
Problem: Let A=diag(1,1), B=diag(-5,-1), u=[4,3], and v=[2,0]. Build A tensor B and apply it to u tensor v.
Steps:
  TENSOR_SETUP|A=diag(1,1)|B=diag(-5,-1)|u=[4,3], v=[2,0]
  TENSOR_RULE|diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)
  M|1|-5|-5
  M|1|-1|-1
  M|1|-5|-5
  M|1|-1|-1
  TENSOR_STATE|u tensor v|[8,0,6,0]
  M|4|2|8
  M|4|0|0
  M|3|2|6
  M|3|0|0
  M|-5|8|-40
  M|-1|0|0
  M|-5|6|-30
  M|-1|0|0
  Z|A tensor B = diag(-5,-1,-5,-1); output = [-40,0,-30,0]
Answer: A tensor B = diag(-5,-1,-5,-1); output = [-40,0,-30,0]
```

### Quantum Gate — `QuantumGateGenerator`  ·  college · difficulty 3

Apply H, X, Y, Z, and CNOT gates to basis states, with exact measurement probabilities.

**Variants:** `quantum_gate_cnot`, `quantum_gate_single`

```
Problem: Apply the CNOT gate to ket10 and give measurement probabilities.
Steps:
  QUANTUM_SETUP|gate=CNOT|input=ket10
  GATE_MATRIX|CNOT|ket00bra00+ket01bra01+ket11bra10+ket10bra11
  XOR|control=1|target=0|1
  APPLY_GATE|CNOT|ket10|ket11
  MEASURE_PROB|computational basis|P(11)=1|all other outcomes 0
  Z|state = ket11; P(11) = 1
Answer: state = ket11; P(11) = 1
```

### Conservation Law — `ConservationLawGenerator`  ·  college · difficulty 3

Charge, baryon number, and lepton-family bookkeeping for reactions.

**Variants:** `conservation_law_allowed`, `conservation_law_forbidden`

```
Problem: Audit conservation of Q, B, Le, Lmu for reaction p + gamma -> e+ + pi0 + gamma. Quantum numbers: p(Q=1,B=1,Le=0,Lmu=0); gamma(Q=0,B=0,Le=0,Lmu=0); e+(Q=1,B=0,Le=-1,Lmu=0); pi0(Q=0,B=0,Le=0,Lmu=0).
Steps:
  CONSERVATION_SETUP|p + gamma -> e+ + pi0 + gamma|check=Q,B,Le,Lmu
  PARTICLE_TABLE|p(Q=1,B=1,Le=0,Lmu=0); gamma(Q=0,B=0,Le=0,Lmu=0); e+(Q=1,B=0,Le=-1,Lmu=0); pi0(Q=0,B=0,Le=0,Lmu=0)
  QN_ADD|Q|left|0 + p(1)|1
  QN_ADD|Q|left|1 + gamma(0)|1
  QN_ADD|Q|right|0 + e+(1)|1
  QN_ADD|Q|right|1 + pi0(0)|1
  QN_ADD|Q|right|1 + gamma(0)|1
  CONSERVE_CHECK|Q|left=1,right=1|conserved
  QN_ADD|B|left|0 + p(1)|1
  QN_ADD|B|left|1 + gamma(0)|1
  QN_ADD|B|right|0 + e+(0)|0
  QN_ADD|B|right|0 + pi0(0)|0
  QN_ADD|B|right|0 + gamma(0)|0
  CONSERVE_CHECK|B|left=1,right=0|violated
  QN_ADD|Le|left|0 + p(0)|0
  QN_ADD|Le|left|0 + gamma(0)|0
  QN_ADD|Le|right|0 + e+(-1)|-1
  QN_ADD|Le|right|-1 + pi0(0)|-1
  QN_ADD|Le|right|-1 + gamma(0)|-1
  CONSERVE_CHECK|Le|left=0,right=-1|violated
  QN_ADD|Lmu|left|0 + p(0)|0
  QN_ADD|Lmu|left|0 + gamma(0)|0
  QN_ADD|Lmu|right|0 + e+(0)|0
  QN_ADD|Lmu|right|0 + pi0(0)|0
  QN_ADD|Lmu|right|0 + gamma(0)|0
  CONSERVE_CHECK|Lmu|left=0,right=0|conserved
  Z|forbidden - B changes by -1; Le changes by -1
Answer: forbidden - B changes by -1; Le changes by -1
```

### Quark Composition — `QuarkCompositionGenerator`  ·  college · difficulty 3

Hadron electric charge from quark constituents.

**Variants:** `quark_composition_antibaryon`, `quark_composition_baryon`, `quark_composition_meson`

```
Problem: Given quark charges u=2/3, d=-1/3, s=-1/3, c=2/3, b=-1/3 and antiquarks have opposite charge, compute the electric charge of an antibaryon with constituents anti_c anti_u anti_s.
Steps:
  QUARK_SETUP|antibaryon|anti_c anti_u anti_s|u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge
  QUARK_CHARGE|anti_c|-2/3
  A|0|-2/3|-2/3
  QUARK_CHARGE|anti_u|-2/3
  A|-2/3|-2/3|-4/3
  QUARK_CHARGE|anti_s|1/3
  A|-4/3|1/3|-1
  Z|Q = -1
Answer: Q = -1
```

### Bisection — `BisectionGenerator`  ·  college · difficulty 2

Bisection tables for f(x)=x^2-n with exact rational midpoints.

**Variants:** `bisection_interval`

```
Problem: Use bisection for f(x)=x^2-109 on [10, 11] for 3 iterations. Give the final bracket.
Steps:
  BISECTION_SETUP|f(x)=x^2-109|interval=[10, 11]|iterations=3
  M|10|10|100
  S|100|109|-9
  SIGN|left|-9|negative
  M|11|11|121
  S|121|109|12
  SIGN|right|12|positive
  A|10|11|21
  D|21|2|21/2
  M|21/2|21/2|441/4
  S|441/4|109|5/4
  SIGN|mid1|5/4|positive
  M|-9|5/4|-45/4
  SIGN|product_1|-45/4|negative
  BISECT_UPDATE|1|product < 0|[10, 21/2]
  A|10|21/2|41/2
  D|41/2|2|41/4
  M|41/4|41/4|1681/16
  S|1681/16|109|-63/16
  SIGN|mid2|-63/16|negative
  M|-9|-63/16|567/16
  SIGN|product_2|567/16|positive
  BISECT_UPDATE|2|product > 0|[41/4, 21/2]
  A|41/4|21/2|83/4
  D|83/4|2|83/8
  M|83/8|83/8|6889/64
  S|6889/64|109|-87/64
  SIGN|mid3|-87/64|negative
  M|-63/16|-87/64|5481/1024
  SIGN|product_3|5481/1024|positive
  BISECT_UPDATE|3|product > 0|[83/8, 21/2]
  Z|root in [83/8, 21/2]
Answer: root in [83/8, 21/2]
```

### Newton Raphson — `NewtonRaphsonGenerator`  ·  college · difficulty 3

Newton-Raphson tables for f(x)=x^2-n with exact rational iterates.

**Variants:** `newton_raphson_sqrt`

```
Problem: Use Newton-Raphson on f(x)=x^2-56 with x0=8 for 3 iterations. Give the final iterate.
Steps:
  NEWTON_SETUP|f(x)=x^2-56|f'(x)=2x|x0=8,iterations=3
  M|8|8|64
  S|64|56|8
  M|2|8|16
  D|8|16|1/2
  S|8|1/2|15/2
  NEWTON_UPDATE|1|x_0=8|x_1=15/2
  M|15/2|15/2|225/4
  S|225/4|56|1/4
  M|2|15/2|15
  D|1/4|15|1/60
  S|15/2|1/60|449/60
  NEWTON_UPDATE|2|x_1=15/2|x_2=449/60
  M|449/60|449/60|201601/3600
  S|201601/3600|56|1/3600
  M|2|449/60|449/30
  D|1/3600|449/30|1/53880
  S|449/60|1/53880|403201/53880
  NEWTON_UPDATE|3|x_2=449/60|x_3=403201/53880
  Z|x_3 = 403201/53880
Answer: x_3 = 403201/53880
```

### Fixed Point — `FixedPointGenerator`  ·  college · difficulty 3

Fixed-point iteration for affine contractions g(x)=a*x+b.

**Variants:** `fixed_point_affine`

```
Problem: Use fixed-point iteration x=g(x) with g(x)=2/9*x-7/3 from x0=3/4 for 4 iterations. First check abs(g')<1.
Steps:
  FIXED_POINT_SETUP|g(x)=2/9*x-7/3|x0=3/4|iterations=4
  DERIVATIVE|g'(x)|2/9
  ABS|2/9|2/9
  COMPARE|2/9|< 1|converges
  M|2/9|3/4|1/6
  A|1/6|-7/3|-13/6
  FIXED_POINT_UPDATE|1|x_0=3/4|x_1=-13/6
  M|2/9|-13/6|-13/27
  A|-13/27|-7/3|-76/27
  FIXED_POINT_UPDATE|2|x_1=-13/6|x_2=-76/27
  M|2/9|-76/27|-152/243
  A|-152/243|-7/3|-719/243
  FIXED_POINT_UPDATE|3|x_2=-76/27|x_3=-719/243
  M|2/9|-719/243|-1438/2187
  A|-1438/2187|-7/3|-6541/2187
  FIXED_POINT_UPDATE|4|x_3=-719/243|x_4=-6541/2187
  Z|x_4 = -6541/2187
Answer: x_4 = -6541/2187
```

### Interpolation — `InterpolationGenerator`  ·  college · difficulty 4

Three-point polynomial interpolation by Lagrange and Newton forms.

**Variants:** `interpolation_lagrange`, `interpolation_newton`

```
Problem: Use Newton divided differences through points (-1,-5), (2,7), (3,23) to find P(1).
Steps:
  INTERP_SETUP|newton|points=(-1,-5), (2,7), (3,23)|x=1
  S|7|-5|12
  S|2|-1|3
  D|12|3|4
  NEWTON_DD|f[x0,x1]|4
  S|23|7|16
  S|3|2|1
  D|16|1|16
  NEWTON_DD|f[x1,x2]|16
  S|16|4|12
  S|3|-1|4
  D|12|4|3
  NEWTON_DD|f[x0,x1,x2]|3
  S|1|-1|2
  M|4|2|8
  S|1|2|-1
  M|2|-1|-2
  M|3|-2|-6
  A|-5|8|3
  A|3|-6|-3
  Z|P(1) = -3
Answer: P(1) = -3
```

### Finite Difference — `FiniteDifferenceGenerator`  ·  college · difficulty 3

Finite-difference tables and derivative estimates.

**Variants:** `finite_difference_central_derivative`, `finite_difference_forward_derivative`, `finite_difference_table`

```
Problem: Use the forward difference with h=4, f(-1)=-5, and f(3)=23 to estimate f'(-1).
Steps:
  FINITE_DIFF_SETUP|forward_derivative|x0=-1,h=4|f0=-5,f1=23
  S|23|-5|28
  D|28|4|7
  Z|forward f'(-1) = 7
Answer: forward f'(-1) = 7
```

### Runge Kutta — `RungeKuttaGenerator`  ·  college · difficulty 4

One-step RK2 midpoint and classical RK4 tables for dy/dx = ax + by.

**Variants:** `runge_kutta_rk2`, `runge_kutta_rk4`

```
Problem: Use RK4 with step size h = 1/4 to approximate y(1/4) for dy/dx = x - 2y with y(0) = 5.
Steps:
  ODE_SETUP|dy/dx = x - 2y, y(0) = 5|RK4, h = 1/4
  D|1/4|2|1/8
  RK_STAGE|k1|x=0|y=5
  EVAL|f(0,5)|(0) - 2(5) = -10
  A|0|1/8|1/8
  M|1/8|-10|-5/4
  S|5|5/4|15/4
  RK_STAGE|k2|x=1/8|y=15/4
  EVAL|f(1/8,15/4)|(1/8) - 2(15/4) = -59/8
  M|1/8|-59/8|-59/64
  S|5|59/64|261/64
  RK_STAGE|k3|x=1/8|y=261/64
  EVAL|f(1/8,261/64)|(1/8) - 2(261/64) = -257/32
  A|0|1/4|1/4
  M|1/4|-257/32|-257/128
  S|5|257/128|383/128
  RK_STAGE|k4|x=1/4|y=383/128
  EVAL|f(1/4,383/128)|(1/4) - 2(383/128) = -367/64
  M|2|-59/8|-59/4
  M|2|-257/32|-257/16
  A|-10|-59/4|-99/4
  A|-99/4|-257/16|-653/16
  A|-653/16|-367/64|-2979/64
  RK_COMBINE|k1+2k2+2k3+k4|-2979/64
  D|1/4|6|1/24
  M|1/24|-2979/64|-993/512
  S|5|993/512|1567/512
  Z|1567/512
Answer: 1567/512
```

### Continuous Distribution — `ContinuousDistributionGenerator`  ·  college · difficulty 3

Normalize f(x)=k*x on [0,a], then compute probability, mean, variance.

**Variants:** `continuous_distribution_linear_pdf`

```
Problem: For pdf f(x)=k*x on 0<=x<=14, first normalize k, then compute P(12<X<14), mean, and variance.
Steps:
  CONT_DIST_SETUP|f(x)=k*x|support=[0,14]|interval=(12,14)
  POWER_INTEGRAL|int_0^a x dx|a^2/2
  E|14|2|196
  D|196|2|98
  D|1|98|1/98
  POWER_INTEGRAL|int_b^c x dx|(c^2-b^2)/2
  E|14|2|196
  E|12|2|144
  S|196|144|52
  M|1/98|52|26/49
  D|26/49|2|13/49
  POWER_INTEGRAL|E[X]|k*a^3/3
  E|14|3|2744
  M|1/98|2744|28
  D|28|3|28/3
  POWER_INTEGRAL|E[X^2]|k*a^4/4
  E|14|4|38416
  M|1/98|38416|392
  D|392|4|98
  M|28/3|28/3|784/9
  S|98|784/9|98/9
  Z|k = 1/98, P = 13/49, mean = 28/3, variance = 98/9
Answer: k = 1/98, P = 13/49, mean = 28/3, variance = 98/9
```

### Named Distribution — `NamedDistributionGenerator`  ·  college · difficulty 3

Poisson, exponential, uniform, and normal distribution arithmetic.

**Variants:** `named_distribution_exponential`, `named_distribution_normal`, `named_distribution_poisson`, `named_distribution_uniform`

```
Problem: For X~Normal(mu=-1, sigma=1), compute P(X<0). Use supplied Phi(1)=8413/10000.
Steps:
  DIST_SETUP|normal|mu=-1,sigma=1|x=0
  S|0|-1|1
  D|1|1|1
  LOOKUP_SUPPLIED|Phi(1)|8413/10000
  Z|P(X<0) = 8413/10000
Answer: P(X<0) = 8413/10000
```

### Joint Distribution — `JointDistributionGenerator`  ·  college · difficulty 4

Binary joint distributions with marginals, conditionals, independence, covariance, and exact correlation.

**Variants:** `joint_distribution_binary`

```
Problem: For binary variables X,Y with P(X=0,Y=0)=215/1089, P(X=0,Y=1)=115/1089, P(X=1,Y=0)=115/1089, and P(X=1,Y=1)=644/1089, compute the marginals, P(Y=1 given X=1), independence, covariance, and correlation.
Steps:
  JOINT_SETUP|X,Y in {0,1}|p00=215/1089, p01=115/1089|p10=115/1089, p11=644/1089
  MARGINAL|P(X=0)=p00+p01
  A|215/1089|115/1089|10/33
  MARGINAL|P(X=1)=p10+p11
  A|115/1089|644/1089|23/33
  MARGINAL|P(Y=0)=p00+p10
  A|215/1089|115/1089|10/33
  MARGINAL|P(Y=1)=p01+p11
  A|115/1089|644/1089|23/33
  COND_FORMULA|P(Y=1 given X=1)=P(X=1,Y=1)/P(X=1)
  D|644/1089|23/33|28/33
  INDEP_FORMULA|independent iff P11=P(X=1)P(Y=1)
  M|23/33|23/33|529/1089
  INDEP_CHECK|P11=644/1089|product=529/1089|no
  EXPECTATION|E[X]=23/33|E[Y]=23/33|E[XY]=644/1089
  COV_FORMULA|Cov=E[XY]-E[X]E[Y]
  S|644/1089|529/1089|115/1089
  S|1|23/33|10/33
  M|23/33|10/33|230/1089
  S|1|23/33|10/33
  M|23/33|10/33|230/1089
  CORR_FORMULA|rho=Cov/sqrt(VarX*VarY)
  M|230/1089|230/1089|52900/1185921
  ROOT|sqrt(52900/1185921)|230/1089
  D|115/1089|230/1089|1/2
  Z|P_X(0)=10/33, P_X(1)=23/33; P_Y(0)=10/33, P_Y(1)=23/33; P(Y=1 given X=1)=28/33; independent=no; covariance=115/1089; correlation=1/2
Answer: P_X(0)=10/33, P_X(1)=23/33; P_Y(0)=10/33, P_Y(1)=23/33; P(Y=1 given X=1)=28/33; independent=no; covariance=115/1089; correlation=1/2
```

### Markov Chain — `MarkovChainGenerator`  ·  college · difficulty 4

Markov chain transition, steady-state, and absorbing-chain calculations.

**Variants:** `markov_chain_absorbing`, `markov_chain_n_step`, `markov_chain_steady_state`

```
Problem: For a two-state Markov chain with P01=1/9 and P10=5/7, find the steady-state distribution.
Steps:
  MARKOV_SETUP|two_state|P00=8/9, P01=1/9|P10=5/7, P11=2/7
  STEADY_EQUATION|pi0*pi01=pi1*pi10|pi0+pi1=1
  A|1/9|5/7|52/63
  D|5/7|52/63|45/52
  D|1/9|52/63|7/52
  M|45/52|1/9|5/52
  M|7/52|5/7|5/52
  CHECK|flow01=5/52|flow10=5/52
  Z|pi0=45/52, pi1=7/52
Answer: pi0=45/52, pi1=7/52
```

### Simplex — `SimplexGenerator`  ·  college · difficulty 5

Two-pivot simplex tableau for a bounded two-variable LP.

**Variants:** `simplex_two_variable_tableau`

```
Problem: Use the simplex method to maximize z = 4x + 2y subject to x <= 14, y <= 15, x >= 0, y >= 0.
Steps:
  SIMPLEX_SETUP|max z=4x+2y|x<=14|y<=15
  TABLEAU|initial|s1: x + s1 = 14|s2: y + s2 = 15
  TABLEAU|z row|-4x - 2y + z = 0
  ENTER|x|most negative reduced cost -4
  D|14|1|14
  RATIO|s1 row|14/1|14
  PIVOT|row=s1|column=x|pivot=1
  ROW_OP|z <- z + 4*s1
  M|4|14|56
  TABLEAU|after x pivot|x=14 - s1|z row: -2y + 4s1 + z = 56
  ENTER|y|remaining negative reduced cost -2
  D|15|1|15
  RATIO|s2 row|15/1|15
  PIVOT|row=s2|column=y|pivot=1
  ROW_OP|z <- z + 2*s2
  M|2|15|30
  A|56|30|86
  TABLEAU|final|x=14, y=15|z=86
  CHECK|reduced costs for x,y are 0|optimal tableau
  Z|x=14, y=15, max z=86
Answer: x=14, y=15, max z=86
```

### LPCorner — `LPCornerGenerator`  ·  college · difficulty 3

Corner-point method for a two-variable linear program.

**Variants:** `lp_corner_point`

```
Problem: Use the corner-point method to maximize z = 5x + 9y subject to 0 <= x <= 15, 0 <= y <= 16, and x + y <= 17.
Steps:
  LP_CORNER_SETUP|max z=5x+9y|0<=x<=15, 0<=y<=16|x+y<=17
  VERTEX_SOLVE|x=0|y=0
  VERTEX|(0,0)
  VERTEX_SOLVE|x=15|y=0
  VERTEX|(15,0)
  VERTEX_SOLVE|x=15|x+y=17
  S|17|15|2
  VERTEX|(15,2)
  VERTEX_SOLVE|y=16|x+y=17
  S|17|16|1
  VERTEX|(1,16)
  VERTEX_SOLVE|x=0|y=16
  VERTEX|(0,16)
  OBJECTIVE|at (0,0)
  M|5|0|0
  M|9|0|0
  A|0|0|0
  OBJECTIVE|at (15,0)
  M|5|15|75
  M|9|0|0
  A|75|0|75
  OBJECTIVE|at (15,2)
  M|5|15|75
  M|9|2|18
  A|75|18|93
  OBJECTIVE|at (1,16)
  M|5|1|5
  M|9|16|144
  A|5|144|149
  OBJECTIVE|at (0,16)
  M|5|0|0
  M|9|16|144
  A|0|144|144
  CHECK|max value 149|at (1,16)
  Z|optimal vertex=(1,16), max z=149
Answer: optimal vertex=(1,16), max z=149
```

### Gradient Descent — `GradientDescentGenerator`  ·  college · difficulty 3

Fixed-step gradient descent on diagonal quadratic bowls.

**Variants:** `gradient_descent_quadratic`

```
Problem: Starting at (-2,7) for f(x,y)=1/2*(4x^2+4y^2), run 3 gradient-descent steps with step size eta=1/6.
Steps:
  GD_SETUP|f(x,y)=1/2*(4x^2+4y^2)|start=(-2,7)|eta=1/6
  GRADIENT_FORMULA|grad=(4x,4y)
  M|4|-2|-8
  M|4|7|28
  M|1/6|-8|-4/3
  S|-2|-4/3|-2/3
  M|1/6|28|14/3
  S|7|14/3|7/3
  ITERATE|k=1|(-2/3,7/3)
  M|4|-2/3|-8/3
  M|4|7/3|28/3
  M|1/6|-8/3|-4/9
  S|-2/3|-4/9|-2/9
  M|1/6|28/3|14/9
  S|7/3|14/9|7/9
  ITERATE|k=2|(-2/9,7/9)
  M|4|-2/9|-8/9
  M|4|7/9|28/9
  M|1/6|-8/9|-4/27
  S|-2/9|-4/27|-2/27
  M|1/6|28/9|14/27
  S|7/9|14/27|7/27
  ITERATE|k=3|(-2/27,7/27)
  E|-2/27|2|4/729
  M|4|4/729|16/729
  E|7/27|2|49/729
  M|4|49/729|196/729
  A|16/729|196/729|212/729
  D|212/729|2|106/729
  Z|x_3=-2/27, y_3=7/27, f(x_3,y_3)=106/729
Answer: x_3=-2/27, y_3=7/27, f(x_3,y_3)=106/729
```

### Game Theory — `GameTheoryGenerator`  ·  college · difficulty 4

Mixed equilibrium for zero-sum 2x2 games.

**Variants:** `game_theory_zero_sum_2x2`

```
Problem: For the zero-sum 2x2 payoff matrix [[3,11],[13,10]] for the row player, compute expected payoffs, the mixed-strategy equilibrium, and the game value.
Steps:
  GAME_SETUP|payoffs=(3,11;13,10)|row player maximizes, column player minimizes
  MIX_FORMULA|q=(d-b)/(a-b-c+d)|p=(d-c)/(a-b-c+d)
  S|10|11|-1
  S|10|13|-3
  S|3|11|-8
  A|-8|-3|-11
  D|-1|-11|1/11
  D|-3|-11|3/11
  EXPECTED_PAYOFF|row1 against q
  M|1/11|3|3/11
  S|1|1/11|10/11
  M|10/11|11|10
  A|3/11|10|113/11
  EXPECTED_PAYOFF|row2 against q
  M|1/11|13|13/11
  M|10/11|10|100/11
  A|13/11|100/11|113/11
  EXPECTED_PAYOFF|col1 against p
  M|3/11|3|9/11
  S|1|3/11|8/11
  M|8/11|13|104/11
  A|9/11|104/11|113/11
  EXPECTED_PAYOFF|col2 against p
  M|3/11|11|3
  M|8/11|10|80/11
  A|3|80/11|113/11
  VALUE_FORMULA|v=(ad-bc)/(a-b-c+d)
  M|3|10|30
  M|11|13|143
  S|30|143|-113
  D|-113|-11|113/11
  CHECK|row payoffs=113/11|column payoffs=113/11
  Z|row mix=(3/11,8/11); column mix=(1/11,10/11); value=113/11
Answer: row mix=(3/11,8/11); column mix=(1/11,10/11); value=113/11
```

### Convolution — `ConvolutionGenerator`  ·  college · difficulty 3

Discrete convolution of short finite sequences.

**Variants:** `discrete_convolution`

```
Problem: Compute the discrete convolution of x=[0,4,8,7] and h=[6,4,7,5].
Steps:
  CONV_SETUP|x=[0,4,8,7]|h=[6,4,7,5]
  CONV_WINDOW|n=0|x0*h0
  M|0|6|0
  CONV_SUM|n=0|0
  CONV_WINDOW|n=1|x0*h1 + x1*h0
  M|0|4|0
  M|4|6|24
  A|0|24|24
  CONV_WINDOW|n=2|x0*h2 + x1*h1 + x2*h0
  M|0|7|0
  M|4|4|16
  M|8|6|48
  A|0|16|16
  A|16|48|64
  CONV_WINDOW|n=3|x0*h3 + x1*h2 + x2*h1 + x3*h0
  M|0|5|0
  M|4|7|28
  M|8|4|32
  M|7|6|42
  A|0|28|28
  A|28|32|60
  A|60|42|102
  CONV_WINDOW|n=4|x1*h3 + x2*h2 + x3*h1
  M|4|5|20
  M|8|7|56
  M|7|4|28
  A|20|56|76
  A|76|28|104
  CONV_WINDOW|n=5|x2*h3 + x3*h2
  M|8|5|40
  M|7|7|49
  A|40|49|89
  CONV_WINDOW|n=6|x3*h3
  M|7|5|35
  CONV_SUM|n=6|35
  Z|y=[0,24,64,102,104,89,35]
Answer: y=[0,24,64,102,104,89,35]
```

### DFT — `DFTGenerator`  ·  college · difficulty 4

Length-2 and length-4 discrete Fourier transforms with exact twiddles.

**Variants:** `dft_length_2`, `dft_length_4`

```
Problem: Compute the length-4 DFT of x=[7,-5,2,9].
Steps:
  DFT_SETUP|N=4|x=[7,-5,2,9]
  TWIDDLE|W4=-i|W4^2=-1|W4^3=i
  DFT_BIN|X0=x0+x1+x2+x3
  A|7|-5|2
  A|2|2|4
  A|4|9|13
  DFT_BIN|X1=(x0-x2)+(x3-x1)i
  S|7|2|5
  S|9|-5|14
  DFT_BIN|X1=5+14i
  DFT_BIN|X2=x0-x1+x2-x3
  S|7|-5|12
  A|12|2|14
  S|14|9|5
  DFT_BIN|X3=(x0-x2)+(x1-x3)i
  S|7|2|5
  S|-5|9|-14
  DFT_BIN|X3=5-14i
  Z|X=[13,5+14i,5,5-14i]
Answer: X=[13,5+14i,5,5-14i]
```

### Fourier Series — `FourierSeriesGenerator`  ·  college · difficulty 4

Fourier sine coefficients for square and sawtooth waves.

**Variants:** `fourier_series_sawtooth`, `fourier_series_square`

```
Problem: For the 2pi-periodic sawtooth f(x)=7*x on (-pi,pi), compute b_1 by integration.
Steps:
  FOURIER_SETUP|sawtooth|A=7|n=1
  SYMMETRY|odd function|a0=0, a_n=0
  INTEGRAL|b_n=(1/pi)*int_-pi^pi A*x*sin(nx) dx
  INTEGRATION_BY_PARTS|u=x|dv=sin(nx)dx
  PARITY|(-1)^(n+1)=1
  M|2|7|14
  M|14|1|14
  D|14|1|14
  FOURIER_COEF|b_1=14
  Z|a0=0, a_n=0, b_1=14
Answer: a0=0, a_n=0, b_1=14
```

### Signal Arithmetic — `SignalArithmeticGenerator`  ·  college · difficulty 2

Sampling/Nyquist and dB arithmetic.

**Variants:** `signal_arithmetic_db_power`, `signal_arithmetic_nyquist`

```
Problem: For a power ratio P2/P1=10, use supplied log10(P2/P1)=1 to compute gain in dB.
Steps:
  SIGNAL_SETUP|dB power ratio|P2/P1=10
  DB_FORMULA|G_dB=10*log10(P2/P1)
  LOG_SUPPLIED|log10(10)|1
  M|10|1|10
  CHECK|positive is gain, negative is loss|10 dB
  Z|G=10 dB
Answer: G=10 dB
```

### Projectile Motion — `ProjectileMotionGenerator`  ·  college · difficulty 2

Projectile motion from velocity components with g=10 m/s^2.

**Variants:** `projectile_motion_components`

```
Problem: A projectile is launched from ground level with horizontal velocity 59 m/s and vertical velocity 29 m/s. Use g=10 m/s^2 to compute time of flight, range, and maximum height.
Steps:
  PROJECTILE_SETUP|vx=59|vy=29|g=10
  FORMULA|t_up=vy/g
  D|29|10|29/10
  FORMULA|T=2*t_up
  M|2|29/10|29/5
  FORMULA|range=vx*T
  M|59|29/5|1711/5
  FORMULA|h_max=vy^2/(2g)
  E|29|2|841
  M|2|10|20
  D|841|20|841/20
  Z|time=29/5 s; range=1711/5 m; max height=841/20 m
Answer: time=29/5 s; range=1711/5 m; max height=841/20 m
```

### Newtons Laws — `NewtonsLawsGenerator`  ·  college · difficulty 3

Newton's-law force systems: Atwood machines and frictional inclines.

**Variants:** `newtons_laws_atwood`, `newtons_laws_incline_friction`

```
Problem: A 26 kg block slides down an incline with supplied sin(theta)=5/13, cos(theta)=12/13, and friction coefficient mu=1/26. Use g=10 m/s^2 to find normal force, friction, and acceleration.
Steps:
  NEWTON_SETUP|incline_friction|m=26, mu=1/26|g=10
  NEWTON_SETUP|sin=5/13|cos=12/13
  M|26|10|260
  FORCE_COMPONENT|parallel=m*g*sin
  M|260|5/13|100
  FORCE_COMPONENT|normal=m*g*cos
  M|260|12/13|240
  FORCE_COMPONENT|friction=mu*N
  M|1/26|240|120/13
  FORCE_EQ|m*a=parallel-friction
  S|100|120/13|1180/13
  D|1180/13|26|590/169
  Z|N=240 N; friction=120/13 N; a=590/169 m/s^2
Answer: N=240 N; friction=120/13 N; a=590/169 m/s^2
```

### Collision — `CollisionGenerator`  ·  college · difficulty 3

Momentum and collision calculations in 1D and 2D.

**Variants:** `collision_elastic_1d`, `collision_inelastic_1d`, `collision_inelastic_2d`

```
Problem: In a 1D elastic collision, m1=13 kg has u1=11 m/s and m2=15 kg has u2=-13 m/s. Find final velocities v1 and v2.
Steps:
  COLLISION_SETUP|elastic_1d|m1=13, u1=11|m2=15, u2=-13
  A|13|15|28
  FORMULA|v1=((m1-m2)u1+2m2u2)/(m1+m2)
  S|13|15|-2
  M|-2|11|-22
  M|2|15|30
  M|30|-13|-390
  A|-22|-390|-412
  D|-412|28|-103/7
  FORMULA|v2=(2m1u1+(m2-m1)u2)/(m1+m2)
  M|2|13|26
  M|26|11|286
  S|15|13|2
  M|2|-13|-26
  A|286|-26|260
  D|260|28|65/7
  Z|v1=-103/7 m/s; v2=65/7 m/s
Answer: v1=-103/7 m/s; v2=65/7 m/s
```

### Energy Conservation — `EnergyConservationGenerator`  ·  college · difficulty 2

Work-energy theorem and mechanical energy conservation.

**Variants:** `energy_conservation_gravity_drop`, `energy_conservation_work_energy`

```
Problem: A 25 kg object is dropped from height 245 m. Use g=10 m/s^2 and energy conservation to find impact speed and initial potential energy.
Steps:
  ENERGY_SETUP|gravity_drop|m=25|h=245, g=10
  ENERGY_FORMULA|mgh=1/2*m*v^2
  M|25|10|250
  M|250|245|61250
  ENERGY_FORMULA|v^2=2gh
  M|2|10|20
  M|20|245|4900
  ROOT|4900|70
  Z|impact speed=70 m/s; potential energy=61250 J
Answer: impact speed=70 m/s; potential energy=61250 J
```

### Orbital Mechanics — `OrbitalMechanicsGenerator`  ·  college · difficulty 3

Circular motion, Newtonian gravitation, and Kepler's third law.

**Variants:** `orbital_mechanics_centripetal_force`, `orbital_mechanics_gravity_force`, `orbital_mechanics_kepler_third`

```
Problem: In a scaled gravitation problem, two masses m1=54 kg and m2=6 kg are 10 m apart with G=1. Find the gravitational force magnitude.
Steps:
  ORBIT_SETUP|gravity_force|m1=54, m2=6|r=10, G=1
  ORBIT_FORMULA|F=G*m1*m2/r^2
  M|54|6|324
  M|1|324|324
  E|10|2|100
  D|324|100|81/25
  Z|F_g=81/25 N
Answer: F_g=81/25 N
```

### Statics — `StaticsGenerator`  ·  college · difficulty 3

Static equilibrium for levers and simply supported beams.

**Variants:** `statics_lever_balance`, `statics_supported_beam`

```
Problem: A simply supported beam is 17 m long with supports at A and B. A 86 N point load acts 2 m from support A. Find reactions RA and RB.
Steps:
  STATICS_SETUP|supported_beam|W=86, L=17|x=2
  STATICS_FORMULA|sum_tau_left=0 => RB*L=W*x
  M|86|2|172
  D|172|17|172/17
  STATICS_FORMULA|sum_Fy=0 => RA+RB=W
  S|86|172/17|1290/17
  A|1290/17|172/17|86
  CHECK|vertical forces|86|load 86
  Z|RA=1290/17 N; RB=172/17 N
Answer: RA=1290/17 N; RB=172/17 N
```

### Rotational Dynamics — `RotationalDynamicsGenerator`  ·  college · difficulty 4

Rotational inertia and angular momentum conservation.

**Variants:** `rotational_dynamics_angular_momentum`, `rotational_dynamics_parallel_axis`

```
Problem: A rotating system has moment of inertia I1=27 kg*m^2 and angular speed omega1=2 rad/s. Its moment of inertia changes to I2=17 kg*m^2 with no external torque. Find the new angular speed.
Steps:
  ROT_SETUP|angular_momentum|I1=27, omega1=2|I2=17
  ROT_FORMULA|I1*omega1=I2*omega2
  M|27|2|54
  D|54|17|54/17
  M|17|54/17|54
  CHECK|angular momentum|54|initial 54
  Z|omega2=54/17 rad/s; L=54 kg*m^2/s
Answer: omega2=54/17 rad/s; L=54 kg*m^2/s
```

### SHM — `SHMGenerator`  ·  college · difficulty 3

Simple harmonic motion: angular frequency, period, and energy exchange.

**Variants:** `shm_mass_spring_energy`, `shm_pendulum_period`

```
Problem: A small-angle pendulum uses g=10 m/s^2 and length L=1/10 m. Find angular frequency and period.
Steps:
  SHM_SETUP|pendulum_period|g=10|L=1/10
  SHM_FORMULA|omega^2=g/L
  D|10|1/10|100
  ROOT|100|10
  SHM_FORMULA|T=2π/omega
  D|2|10|1/5
  PI_MULT|1/5|π|π/5
  Z|omega=10 rad/s; T=π/5 s
Answer: omega=10 rad/s; T=π/5 s
```

### Electrostatics — `ElectrostaticsGenerator`  ·  college · difficulty 3

Coulomb superposition for point charges on a line, with k=1 supplied.

**Variants:** `electrostatics_field_axis`, `electrostatics_potential_axis`

```
Problem: In scaled units with k=1, three point charges are at distances r1=9 m, r2=8 m, r3=7 m from the origin with charges q1=5 C, q2=-8 C, q3=-1 C. Find the electric potential at the origin.
Steps:
  ELEC_SETUP|potential_axis|q1=5, r1=9|q2=-8, r2=8
  ELEC_SETUP|q3=-1, r3=7|k=1
  ELEC_FORMULA|V=sum(q_i/r_i)
  D|5|9|5/9
  D|-8|8|-1
  A|5/9|-1|-4/9
  D|-1|7|-1/7
  A|-4/9|-1/7|-37/63
  Z|V=-37/63 V
Answer: V=-37/63 V
```

### Gauss Law — `GaussLawGenerator`  ·  college · difficulty 4

Gauss's law for spherical, cylindrical, and planar symmetry.

**Variants:** `gauss_law_line_charge`, `gauss_law_sheet_charge`, `gauss_law_sphere`

```
Problem: An infinite line charge has lambda=27 C/m. A cylindrical Gaussian surface has radius r=1 m and length L=5 m. Use epsilon0=1 to find the electric field.
Steps:
  GAUSS_SETUP|line_charge|lambda=27, r=1|L=5
  GAUSS_FORMULA|E*(2πrL)=lambda*L
  M|27|5|135
  M|2|1|2
  M|2|5|10
  D|135|10|27/2
  PI_DEN|27/2|π|27/(2π)
  Z|E=27/(2π) N/C outward-positive
Answer: E=27/(2π) N/C outward-positive
```

### Transient Circuit — `TransientCircuitGenerator`  ·  college · difficulty 4

RC and RL first-order transients with exact symbolic exponentials.

**Variants:** `transient_circuit_rc_charging`, `transient_circuit_rl_rise`

```
Problem: An RL circuit has R=7 ohm, L=7 H, source V=18 V, and starts with zero current. Find current at t=5 s in exact exponential form.
Steps:
  TRANSIENT_SETUP|rl_rise|R=7, L=7|V=18, t=5
  TRANSIENT_FORMULA|tau=L/R
  D|7|7|1
  TRANSIENT_FORMULA|I_inf=V/R
  D|18|7|18/7
  D|5|1|5
  TRANSIENT_FORMULA|I=I_inf*(1-e^(-t/tau))
  EXP_SUB|t/tau|5|e^-5
  TRANSIENT_FORMULA|I=18/7*(1-e^-5)
  Z|I=(18/7)*(1-e^-5) A
Answer: I=(18/7)*(1-e^-5) A
```

### Magnetism — `MagnetismGenerator`  ·  college · difficulty 4

Magnetic force and standard magnetic-field cases.

**Variants:** `magnetism_force`, `magnetism_loop_center`, `magnetism_straight_wire`

```
Problem: A long straight wire carries current I=54 A. At distance r=2 m, use mu0=1 to find the magnetic field magnitude B=mu0*I/(2πr).
Steps:
  MAG_SETUP|straight_wire|I=54, r=2|mu0=1
  MAG_FORMULA|B=mu0*I/(2πr)
  M|2|2|4
  D|54|4|27/2
  PI_DEN|27/2|π|27/(2π)
  Z|B=27/(2π) T
Answer: B=27/(2π) T
```

### Gas Law — `GasLawGenerator`  ·  college · difficulty 2

Ideal-gas and combined-gas law computations with R supplied as 1.

**Variants:** `gas_law_combined_pressure`, `gas_law_ideal_moles`

```
Problem: A gas changes from P1=25 atm, V1=29 L, T1=14 K to V2=2 L and T2=9 K. Use the combined gas law to find P2.
Steps:
  GAS_SETUP|combined_pressure|P1=25, V1=29, T1=14|V2=2, T2=9
  GAS_FORMULA|P1*V1/T1=P2*V2/T2
  GAS_FORMULA|P2=P1*V1*T2/(T1*V2)
  M|25|29|725
  M|725|9|6525
  M|14|2|28
  D|6525|28|6525/28
  Z|P2=6525/28 atm
Answer: P2=6525/28 atm
```

### First Law — `FirstLawGenerator`  ·  college · difficulty 3

First-law bookkeeping with DeltaU = Q - W, W done by the gas/system.

**Variants:** `first_law_adiabatic`, `first_law_isobaric`, `first_law_isochoric`, `first_law_isothermal`

```
Problem: An isobaric process has pressure P=14 Pa, volume changes from V1=2 m^3 to V2=6 m^3, and heat Q=50 J. Using W=P(V2-V1) and DeltaU=Q-W, find W and DeltaU.
Steps:
  FIRSTLAW_SETUP|isobaric|P=14, V1=2, V2=6|Q=50
  FIRSTLAW_FORMULA|W=P*(V2-V1)
  S|6|2|4
  M|14|4|56
  FIRSTLAW_FORMULA|DeltaU=Q-W
  S|50|56|-6
  Z|W=56 J; DeltaU=-6 J
Answer: W=56 J; DeltaU=-6 J
```

### Heat Engine — `HeatEngineGenerator`  ·  college · difficulty 3

Heat engines, Carnot limits, and refrigerator coefficients of performance.

**Variants:** `heat_engine_carnot_efficiency`, `heat_engine_engine_efficiency`, `heat_engine_refrigerator_cop`

```
Problem: A reversible engine operates between Th=919 K and Tc=488 K. Find the Carnot efficiency.
Steps:
  ENGINE_SETUP|carnot_efficiency|Th=919|Tc=488
  ENGINE_FORMULA|eta_C=1-Tc/Th=(Th-Tc)/Th
  S|919|488|431
  D|431|919|431/919
  Z|Carnot efficiency=431/919
Answer: Carnot efficiency=431/919
```

### Entropy Change — `EntropyChangeGenerator`  ·  college · difficulty 4

Entropy changes for ideal-gas processes and ideal mixing.

**Variants:** `entropy_change_constant_volume_heating`, `entropy_change_equal_gas_mixing`, `entropy_change_isothermal_expansion`

```
Problem: An ideal gas is heated at constant volume with n=7 mol, Cv=1, T1=5 K, and T2=50 K. Find DeltaS exactly.
Steps:
  ENTROPY_SETUP|constant_volume_heating|n=7, Cv=1|T1=5, T2=50
  ENTROPY_FORMULA|DeltaS=nCv*ln(T2/T1)
  M|7|1|7
  D|50|5|10
  LOG_TERM|7|ln(10)|7*ln(10)
  Z|DeltaS=7*ln(10) J/K
Answer: DeltaS=7*ln(10) J/K
```

### Calorimetry — `CalorimetryGenerator`  ·  college · difficulty 2

Calorimetry with sensible heat and phase changes.

**Variants:** `calorimetry_ice_to_water`, `calorimetry_phase_change`, `calorimetry_temperature_change`

```
Problem: A substance of mass m=25 kg undergoes a phase change with latent heat L=225 J/kg. Find heat q.
Steps:
  CAL_SETUP|phase_change|m=25|L=225
  CAL_FORMULA|q=m*L
  M|25|225|5625
  Z|q=5625 J
Answer: q=5625 J
```

### Blackbody — `BlackbodyGenerator`  ·  college · difficulty 3

Blackbody radiation computations with supplied constants.

**Variants:** `blackbody_stefan_power`, `blackbody_wien_peak`

```
Problem: A blackbody has area A=2 m^2 and temperature T=10 K. Using Stefan-Boltzmann constant sigma=7, find radiated power P.
Steps:
  BLACKBODY_SETUP|stefan_power|sigma=7, A=2|T=10
  BLACKBODY_FORMULA|P=sigma*A*T^4
  E|10|4|10000
  M|7|2|14
  M|14|10000|140000
  Z|P=140000 W
Answer: P=140000 W
```

### Quantum Formula — `QuantumFormulaGenerator`  ·  college · difficulty 3

Intro quantum formulas with supplied constants.

**Variants:** `quantum_formula_compton`, `quantum_formula_de_broglie`, `quantum_formula_photoelectric`

```
Problem: A particle has momentum p=3 kg*m/s. Using h=54, find its de Broglie wavelength.
Steps:
  QUANTUM_SETUP|de_broglie|h=54|p=3
  QUANTUM_FORMULA|lambda=h/p
  D|54|3|18
  Z|lambda=18 m
Answer: lambda=18 m
```

### Particle In Box — `ParticleInBoxGenerator`  ·  college · difficulty 3

One-dimensional particle-in-a-box energies and transition wavelengths.

**Variants:** `particle_in_box_energy_level`, `particle_in_box_transition_wavelength`

```
Problem: A particle in a 1D box transitions from n=5 to n=4. Use h=5, c=17, mass m=8, and length L=7 to find the emitted photon wavelength.
Steps:
  BOX_SETUP|transition_wavelength|n_low=4, n_high=5|h=5, c=17
  BOX_SETUP|m=8, L=7
  BOX_FORMULA|lambda=8*m*L^2*c/((n_high^2-n_low^2)*h)
  E|4|2|16
  E|5|2|25
  S|25|16|9
  E|7|2|49
  M|8|8|64
  M|64|49|3136
  M|3136|17|53312
  M|9|5|45
  D|53312|45|53312/45
  Z|lambda=53312/45 m
Answer: lambda=53312/45 m
```

### Hydrogen Atom — `HydrogenAtomGenerator`  ·  college · difficulty 3

Hydrogen-atom Rydberg transition and ionization arithmetic.

**Variants:** `hydrogen_atom_ionization_energy`, `hydrogen_atom_transition_energy`, `hydrogen_atom_transition_wavelength`

```
Problem: For hydrogen with R_L=9 1/m, an electron drops from n=5 to n=4. Use the Rydberg formula to find lambda.
Steps:
  HYDROGEN_SETUP|transition_wavelength|n_low=4, n_high=5|R_L=9 1/m
  HYDROGEN_FORMULA|1/lambda=R_L*(1/n_low^2-1/n_high^2)
  E|4|2|16
  E|5|2|25
  D|1|16|1/16
  D|1|25|1/25
  S|1/16|1/25|9/400
  M|9|9/400|81/400
  D|1|81/400|400/81
  Z|lambda=400/81 m
Answer: lambda=400/81 m
```

### Special Relativity — `SpecialRelativityGenerator`  ·  college · difficulty 3

Special-relativity time dilation, length contraction, and 1D Lorentz event transformations with exact supplied beta and gamma.

**Variants:** `special_relativity_length_contraction`, `special_relativity_lorentz_event`, `special_relativity_time_dilation`

```
Problem: A rod has proper length L0=54 m and moves with beta=9/41 where gamma=41/40. Find the contracted length L.
Steps:
  REL_SETUP|length_contraction|beta=9/41|gamma=41/40
  REL_FORMULA|L=L0/gamma
  D|54|41/40|2160/41
  Z|L=2160/41 m
Answer: L=2160/41 m
```

### Relativistic Energy — `RelativisticEnergyGenerator`  ·  college · difficulty 4

Relativistic rest energy, mass-shell energy, and velocity addition.

**Variants:** `relativistic_energy_energy_momentum`, `relativistic_energy_rest_energy`, `relativistic_energy_velocity_addition`

```
Problem: In c=1 units, a particle has momentum p=35 and mass m=12. Find E from E^2=p^2+m^2.
Steps:
  REL_ENERGY_SETUP|energy_momentum|c=1|p=35, m=12
  REL_ENERGY_FORMULA|E=sqrt(p^2+m^2)
  E|35|2|1225
  E|12|2|144
  A|1225|144|1369
  ROOT|sqrt(1369)|37
  Z|E=37
Answer: E=37
```

### Doppler — `DopplerGenerator`  ·  college · difficulty 3

Acoustic and relativistic Doppler shifts with exact arithmetic.

**Variants:** `doppler_acoustic_toward`, `doppler_relativistic_approach`

```
Problem: A light source approaches with beta=63/65 and emits f=141 Hz. Use the relativistic Doppler formula to find f_obs.
Steps:
  DOPPLER_SETUP|relativistic_approach|f=141|beta=63/65
  DOPPLER_FORMULA|f_obs=f*sqrt((1+beta)/(1-beta))
  E|8|2|64
  S|64|1|63
  A|64|1|65
  A|1|63/65|128/65
  S|1|63/65|2/65
  D|128/65|2/65|64
  ROOT|sqrt(64)|8
  M|141|8|1128
  Z|f_obs=1128 Hz
Answer: f_obs=1128 Hz
```

### Optics — `OpticsGenerator`  ·  college · difficulty 2

Exact geometric-optics arithmetic: Snell's law, thin lenses, and mirrors.

**Variants:** `optics_mirror_magnification`, `optics_snell`, `optics_thin_lens`

```
Problem: A thin lens has focal length f=26 cm and object distance d_o=80 cm. Find image distance d_i.
Steps:
  OPTICS_SETUP|thin_lens|f=26|d_o=80
  OPTICS_FORMULA|1/f=1/d_o+1/d_i
  D|1|26|1/26
  D|1|80|1/80
  S|1/26|1/80|27/1040
  D|1|27/1040|1040/27
  Z|d_i=1040/27 cm
Answer: d_i=1040/27 cm
```

### Interference — `InterferenceGenerator`  ·  college · difficulty 3

Exact wave-interference arithmetic for slits, gratings, and thin films.

**Variants:** `interference_diffraction_grating`, `interference_double_slit`, `interference_thin_film`

```
Problem: A diffraction grating has spacing d=24 m. For order m=4 and wavelength lambda=2 m, find sin(theta).
Steps:
  INTERFERENCE_SETUP|diffraction_grating|m=4, lambda=2|d=24
  INTERFERENCE_FORMULA|d*sin(theta)=m*lambda
  M|4|2|8
  D|8|24|1/3
  Z|sin(theta)=1/3
Answer: sin(theta)=1/3
```

### Standing Wave — `StandingWaveGenerator`  ·  college · difficulty 2

Exact standing-wave harmonic arithmetic for strings and pipes.

**Variants:** `standing_wave_closed_pipe`, `standing_wave_open_pipe`, `standing_wave_string_harmonic`

```
Problem: An open-open pipe has length L=14 m and sound speed v=30 m/s. Find wavelength lambda and frequency f for harmonic n=5.
Steps:
  STANDING_SETUP|open_pipe|n=5|L=14, v=30
  STANDING_BOUNDARY|open-open pipe allows n=1,2,3,...
  STANDING_FORMULA|lambda=2L/n, f=v/lambda
  M|2|14|28
  D|28|5|28/5
  D|30|28/5|75/14
  Z|lambda=28/5 m; f=75/14 Hz
Answer: lambda=28/5 m; f=75/14 Hz
```

### Entropy — `EntropyGenerator`  ·  college · difficulty 3

Shannon entropy and information content for dyadic distributions.

**Variants:** `entropy_counts_entropy`, `entropy_distribution_entropy`, `entropy_event_information`

```
Problem: An event has probability p=1/16384. Find its information content in bits.
Steps:
  INFO_SETUP|p=1/16384|I=-log2(p)
  LOG2|1/16384|-14
  S|0|-14|14
  Z|I=14 bits
Answer: I=14 bits
```

### Mutual Information — `MutualInformationGenerator`  ·  college · difficulty 4

Joint entropy, conditional entropy, and mutual information from joint tables.

**Variants:** `mutual_information_all_measures`, `mutual_information_conditional_entropy`, `mutual_information_joint_entropy`, `mutual_information_mutual_information`

```
Problem: For joint distribution P(X,Y) with rows X=0..1 and columns Y=0..3: rows=[[1/4,0,1/4,0];[0,1/4,0,1/4]]. Find H(X,Y), H(Y given X), and I(X;Y).
Steps:
  MI_SETUP|rows=[[1/4,0,1/4,0];[0,1/4,0,1/4]]|task=H(X,Y), H(Y given X), and I(X;Y)
  MARGINAL|P(X=0)=row0 sum
  A|1/4|0|1/4
  A|1/4|1/4|1/2
  A|1/2|0|1/2
  MARGINAL|P(X=1)=row1 sum
  A|0|1/4|1/4
  A|1/4|0|1/4
  A|1/4|1/4|1/2
  MARGINAL|P(Y=0)=col0 sum
  A|1/4|0|1/4
  MARGINAL|P(Y=1)=col1 sum
  A|0|1/4|1/4
  MARGINAL|P(Y=2)=col2 sum
  A|1/4|0|1/4
  MARGINAL|P(Y=3)=col3 sum
  A|0|1/4|1/4
  ENTROPY_SETUP|H(X)|-sum p log2(p)
  LOG2|1/2|-1
  M|1/2|1|1/2
  A|0|1/2|1/2
  LOG2|1/2|-1
  M|1/2|1|1/2
  A|1/2|1/2|1
  ENTROPY_SETUP|H(Y)|-sum p log2(p)
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|0|1/2|1/2
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|1/2|1/2|1
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|1|1/2|3/2
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|3/2|1/2|2
  ENTROPY_SETUP|H(X,Y)|-sum p log2(p)
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|0|1/2|1/2
  ENTROPY_SKIP|H(X,Y)|p=0
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|1/2|1/2|1
  ENTROPY_SKIP|H(X,Y)|p=0
  ENTROPY_SKIP|H(X,Y)|p=0
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|1|1/2|3/2
  ENTROPY_SKIP|H(X,Y)|p=0
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|3/2|1/2|2
  COND_ENTROPY|H(Y given X)=H(X,Y)-H(X)
  S|2|1|1
  MI_FORMULA|I=H(X)+H(Y)-H(X,Y)
  A|1|2|3
  S|3|2|1
  Z|H(X,Y)=2 bits; H(Y given X)=1 bit; I(X;Y)=1 bit
Answer: H(X,Y)=2 bits; H(Y given X)=1 bit; I(X;Y)=1 bit
```

### Huffman Coding — `HuffmanCodingGenerator`  ·  college · difficulty 4

Huffman tree construction with expected length, entropy, and Kraft check.

**Variants:** `huffman_coding`

```
Problem: Build a Huffman code for symbols with probabilities A=1/16, B=1/2, C=1/32, D=1/64, E=1/64, F=1/4, G=1/16, H=1/16. Report code lengths, expected length L, entropy H, and Kraft sum.
Steps:
  HUFFMAN_SETUP|A=1/16, B=1/2, C=1/32, D=1/64, E=1/64, F=1/4, G=1/16, H=1/16
  HUFFMAN_MERGE|D:1/64 + E:1/64|DE:1/32
  HUFFMAN_MERGE|C:1/32 + DE:1/32|CDE:1/16
  HUFFMAN_MERGE|A:1/16 + CDE:1/16|ACDE:1/8
  HUFFMAN_MERGE|G:1/16 + H:1/16|GH:1/8
  HUFFMAN_MERGE|ACDE:1/8 + GH:1/8|ACDEGH:1/4
  HUFFMAN_MERGE|ACDEGH:1/4 + F:1/4|ACDEFGH:1/2
  HUFFMAN_MERGE|ACDEFGH:1/2 + B:1/2|ABCDEFGH:1
  CODE_LENGTH|A|l=4
  CODE_LENGTH|B|l=1
  CODE_LENGTH|C|l=5
  CODE_LENGTH|D|l=6
  CODE_LENGTH|E|l=6
  CODE_LENGTH|F|l=2
  CODE_LENGTH|G|l=4
  CODE_LENGTH|H|l=4
  HUFFMAN_FORMULA|L=sum p_i*l_i
  M|1/16|4|1/4
  A|0|1/4|1/4
  M|1/2|1|1/2
  A|1/4|1/2|3/4
  M|1/32|5|5/32
  A|3/4|5/32|29/32
  M|1/64|6|3/32
  A|29/32|3/32|1
  M|1/64|6|3/32
  A|1|3/32|35/32
  M|1/4|2|1/2
  A|35/32|1/2|51/32
  M|1/16|4|1/4
  A|51/32|1/4|59/32
  M|1/16|4|1/4
  A|59/32|1/4|67/32
  ENTROPY_SETUP|H|-sum p log2(p)
  LOG2|1/16|-4
  M|1/16|4|1/4
  A|0|1/4|1/4
  LOG2|1/2|-1
  M|1/2|1|1/2
  A|1/4|1/2|3/4
  LOG2|1/32|-5
  M|1/32|5|5/32
  A|3/4|5/32|29/32
  LOG2|1/64|-6
  M|1/64|6|3/32
  A|29/32|3/32|1
  LOG2|1/64|-6
  M|1/64|6|3/32
  A|1|3/32|35/32
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|35/32|1/2|51/32
  LOG2|1/16|-4
  M|1/16|4|1/4
  A|51/32|1/4|59/32
  LOG2|1/16|-4
  M|1/16|4|1/4
  A|59/32|1/4|67/32
  KRAFT_FORMULA|sum 2^-l_i
  E|2|4|16
  D|1|16|1/16
  A|0|1/16|1/16
  E|2|1|2
  D|1|2|1/2
  A|1/16|1/2|9/16
  E|2|5|32
  D|1|32|1/32
  A|9/16|1/32|19/32
  E|2|6|64
  D|1|64|1/64
  A|19/32|1/64|39/64
  E|2|6|64
  D|1|64|1/64
  A|39/64|1/64|5/8
  E|2|2|4
  D|1|4|1/4
  A|5/8|1/4|7/8
  E|2|4|16
  D|1|16|1/16
  A|7/8|1/16|15/16
  E|2|4|16
  D|1|16|1/16
  A|15/16|1/16|1
  KRAFT_CHECK|sum=1|complete
  Z|lengths=A:4,B:1,C:5,D:6,E:6,F:2,G:4,H:4; L=67/32 bits; H=67/32 bits; Kraft=1
Answer: lengths=A:4,B:1,C:5,D:6,E:6,F:2,G:4,H:4; L=67/32 bits; H=67/32 bits; Kraft=1
```

### Hamming Code — `HammingCodeGenerator`  ·  college · difficulty 4

Hamming(7,4) encoding, syndrome computation, and single-error correction.

**Variants:** `hamming_code_correct`, `hamming_code_encode`, `hamming_code_syndrome`

```
Problem: A Hamming(7,4) even-parity word is received as r=0111011. Compute the syndrome and error position.
Steps:
  HAMMING_RECEIVED|r=0111011
  SYNDROME_CALC|s1=b1 xor b3 xor b5 xor b7|0 xor 1 xor 0 xor 1=0
  SYNDROME_CALC|s2=b2 xor b3 xor b6 xor b7|1 xor 1 xor 1 xor 1=0
  SYNDROME_CALC|s4=b4 xor b5 xor b6 xor b7|1 xor 0 xor 1 xor 1=1
  SYNDROME_VALUE|s1=0, s2=0, s4=1|position=4
  Z|syndrome=4; error_position=4
Answer: syndrome=4; error_position=4
```

### CRC — `CRCGenerator`  ·  college · difficulty 4

CRC remainder computation by polynomial long division over GF(2).

**Variants:** `crc_remainder`

```
Problem: Compute the CRC remainder for data 1011111 using generator polynomial 11001. Append 4 zeros before division.
Steps:
  CRC_SETUP|data=1011111|poly=11001|augmented=10111110000
  CRC_XOR|i=0|10111 xor 11001|01110
  CRC_XOR|i=1|11101 xor 11001|00100
  CRC_SKIP|i=2|leading bit 0
  CRC_XOR|i=3|10010 xor 11001|01011
  CRC_XOR|i=4|10110 xor 11001|01111
  CRC_XOR|i=5|11110 xor 11001|00111
  CRC_SKIP|i=6|leading bit 0
  CRC_REMAINDER|1110
  CRC_CHECK|codeword=10111111110|remainder=0000|valid
  Z|remainder=1110; codeword=10111111110
Answer: remainder=1110; codeword=10111111110
```

### Kraft Inequality — `KraftInequalityGenerator`  ·  college · difficulty 3

Kraft inequality and code-length feasibility for binary prefix codes.

**Variants:** `kraft_inequality_complete`, `kraft_inequality_incomplete`, `kraft_inequality_infeasible`

```
Problem: Use Kraft's inequality for a binary prefix code with requested lengths A=5, B=6, C=5. Decide whether the lengths are feasible; if feasible, give canonical codewords.
Steps:
  KRAFT_SETUP|A=5, B=6, C=5|binary prefix code
  KRAFT_FORMULA|sum 2^-l_i <= 1
  E|2|5|32
  D|1|32|1/32
  KRAFT_TERM|A|l=5|1/32
  A|0|1/32|1/32
  E|2|6|64
  D|1|64|1/64
  KRAFT_TERM|B|l=6|1/64
  A|1/32|1/64|3/64
  E|2|5|32
  D|1|32|1/32
  KRAFT_TERM|C|l=5|1/32
  A|3/64|1/32|5/64
  KRAFT_CHECK|sum=5/64|<=1|feasible
  S|1|5/64|59/64
  KRAFT_CLASSIFY|slack=59/64|incomplete
  CANONICAL_ORDER|A=5, C=5, B=6
  CANONICAL_SHIFT|code=0|left=5|0
  CODEWORD|A|l=5|00000
  A|0|1|1
  CANONICAL_SHIFT|code=1|left=0|1
  CODEWORD|C|l=5|00001
  A|1|1|2
  CANONICAL_SHIFT|code=2|left=1|4
  CODEWORD|B|l=6|000100
  A|4|1|5
  Z|Kraft=5/64; status=feasible_incomplete; slack=59/64; codes=A:00000,B:000100,C:00001
Answer: Kraft=5/64; status=feasible_incomplete; slack=59/64; codes=A:00000,B:000100,C:00001
```

### Naive Bayes — `NaiveBayesGenerator`  ·  college · difficulty 4

Naive Bayes classification from binary feature count tables.

**Variants:** `naive_bayes_three_feature`, `naive_bayes_two_feature`

```
Problem: Classify query known=1, offer=0, urgent=0 by naive Bayes with Laplace smoothing alpha=1. Feature-one counts: Spam N=14, known=6, offer=14, urgent=12; Ham N=13, known=13, offer=4, urgent=7. Use class priors from N.
Steps:
  NB_SETUP|query=known=1, offer=0, urgent=0|alpha=1|classes=Spam,Ham
  D|14|27|14/27
  NB_PRIOR|Spam|14/27
  NB_FEATURE_COUNT|Spam|known=1|count=6
  A|6|1|7
  A|14|2|16
  D|7|16|7/16
  NB_LIKELIHOOD|Spam|known=1|7/16
  S|14|14|0
  NB_FEATURE_COUNT|Spam|offer=0|count=0
  A|0|1|1
  A|14|2|16
  D|1|16|1/16
  NB_LIKELIHOOD|Spam|offer=0|1/16
  S|14|12|2
  NB_FEATURE_COUNT|Spam|urgent=0|count=2
  A|2|1|3
  A|14|2|16
  D|3|16|3/16
  NB_LIKELIHOOD|Spam|urgent=0|3/16
  D|13|27|13/27
  NB_PRIOR|Ham|13/27
  NB_FEATURE_COUNT|Ham|known=1|count=13
  A|13|1|14
  A|13|2|15
  D|14|15|14/15
  NB_LIKELIHOOD|Ham|known=1|14/15
  S|13|4|9
  NB_FEATURE_COUNT|Ham|offer=0|count=9
  A|9|1|10
  A|13|2|15
  D|10|15|2/3
  NB_LIKELIHOOD|Ham|offer=0|2/3
  S|13|7|6
  NB_FEATURE_COUNT|Ham|urgent=0|count=6
  A|6|1|7
  A|13|2|15
  D|7|15|7/15
  NB_LIKELIHOOD|Ham|urgent=0|7/15
  NB_SCORE|Spam|start=14/27
  M|14/27|7/16|49/216
  M|49/216|1/16|49/3456
  M|49/3456|3/16|49/18432
  NB_SCORE|Spam|score=49/18432
  NB_SCORE|Ham|start=13/27
  M|13/27|14/15|182/405
  M|182/405|2/3|364/1215
  M|364/1215|7/15|2548/18225
  NB_SCORE|Ham|score=2548/18225
  A|49/18432|2548/18225|5317529/37324800
  D|49/18432|5317529/37324800|2025/108521
  D|2548/18225|5317529/37324800|106496/108521
  CHECK|Spam vs Ham|49/18432 < 2548/18225|predict=Ham
  Z|class=Ham; P_Spam_given_x=2025/108521; P_Ham_given_x=106496/108521
Answer: class=Ham; P_Spam_given_x=2025/108521; P_Ham_given_x=106496/108521
```

### KMeans Step — `KMeansStepGenerator`  ·  college · difficulty 3

One complete k-means assignment/update iteration for two 2D centroids.

**Variants:** `kmeans_one_iteration`

```
Problem: Run one k-means iteration with points P1=(-2,-5), P2=(0,5), P3=(0,2), P4=(-1,2) and starting centroids C1=(5,2), C2=(4,-4). Use squared Euclidean distance for assignment, then update each centroid to its cluster mean.
Steps:
  KMEANS_SETUP|points=P1=(-2,-5), P2=(0,5), P3=(0,2), P4=(-1,2)|centroids=C1=(5,2), C2=(4,-4)
  S|-2|5|-7
  E|-7|2|49
  S|-5|2|-7
  E|-7|2|49
  A|49|49|98
  DIST2|P1|C1|98
  S|-2|4|-6
  E|-6|2|36
  S|-5|-4|-1
  E|-1|2|1
  A|36|1|37
  DIST2|P1|C2|37
  CHECK|P1|d2(C1)=98 > d2(C2)=37|assign=C2
  ASSIGN|P1|C2
  S|0|5|-5
  E|-5|2|25
  S|5|2|3
  E|3|2|9
  A|25|9|34
  DIST2|P2|C1|34
  S|0|4|-4
  E|-4|2|16
  S|5|-4|9
  E|9|2|81
  A|16|81|97
  DIST2|P2|C2|97
  CHECK|P2|d2(C1)=34 < d2(C2)=97|assign=C1
  ASSIGN|P2|C1
  S|0|5|-5
  E|-5|2|25
  S|2|2|0
  E|0|2|0
  A|25|0|25
  DIST2|P3|C1|25
  S|0|4|-4
  E|-4|2|16
  S|2|-4|6
  E|6|2|36
  A|16|36|52
  DIST2|P3|C2|52
  CHECK|P3|d2(C1)=25 < d2(C2)=52|assign=C1
  ASSIGN|P3|C1
  S|-1|5|-6
  E|-6|2|36
  S|2|2|0
  E|0|2|0
  A|36|0|36
  DIST2|P4|C1|36
  S|-1|4|-5
  E|-5|2|25
  S|2|-4|6
  E|6|2|36
  A|25|36|61
  DIST2|P4|C2|61
  CHECK|P4|d2(C1)=36 < d2(C2)=61|assign=C1
  ASSIGN|P4|C1
  CLUSTER_MEMBERS|C1|P2,P3,P4
  A|0|0|0
  A|0|5|5
  A|0|0|0
  A|5|2|7
  A|0|-1|-1
  A|7|2|9
  D|-1|3|-1/3
  D|9|3|3
  CENTROID_UPDATE|C1|(-1/3,3)
  CLUSTER_MEMBERS|C2|P1
  A|0|-2|-2
  A|0|-5|-5
  D|-2|1|-2
  D|-5|1|-5
  CENTROID_UPDATE|C2|(-2,-5)
  Z|assignments=P1:C2,P2:C1,P3:C1,P4:C1; C1_new=(-1/3,3); C2_new=(-2,-5)
Answer: assignments=P1:C2,P2:C1,P3:C1,P4:C1; C1_new=(-1/3,3); C2_new=(-2,-5)
```

### KNN — `KNNGenerator`  ·  college · difficulty 2

k-nearest-neighbor classification with an explicit squared-distance table.

**Variants:** `knn_classification`

```
Problem: Classify query q=(4,4) by 3-NN using squared Euclidean distance. Training points: P1=(-1,0,B), P2=(3,4,B), P3=(5,-1,B), P4=(-1,4,B), P5=(-5,0,B).
Steps:
  KNN_SETUP|q=(4,4)|k=3|training=P1=(-1,0,B), P2=(3,4,B), P3=(5,-1,B), P4=(-1,4,B), P5=(-5,0,B)
  S|4|-1|5
  E|5|2|25
  S|4|0|4
  E|4|2|16
  A|25|16|41
  KNN_DISTANCE|P1|label=B|d2=41
  S|4|3|1
  E|1|2|1
  S|4|4|0
  E|0|2|0
  A|1|0|1
  KNN_DISTANCE|P2|label=B|d2=1
  S|4|5|-1
  E|-1|2|1
  S|4|-1|5
  E|5|2|25
  A|1|25|26
  KNN_DISTANCE|P3|label=B|d2=26
  S|4|-1|5
  E|5|2|25
  S|4|4|0
  E|0|2|0
  A|25|0|25
  KNN_DISTANCE|P4|label=B|d2=25
  S|4|-5|9
  E|9|2|81
  S|4|0|4
  E|4|2|16
  A|81|16|97
  KNN_DISTANCE|P5|label=B|d2=97
  KNN_SORT|P2:1:B,P4:25:B,P3:26:B,P1:41:B,P5:97:B
  KNN_NEIGHBORS|P2:1:B,P4:25:B,P3:26:B
  LABEL_COUNT|A|0
  LABEL_COUNT|B|3
  CHECK|A vs B|0 < 3|predict=B
  Z|class=B; neighbors=P2:B,P4:B,P3:B
Answer: class=B; neighbors=P2:B,P4:B,P3:B
```

### Classifier Metrics — `ClassifierMetricsGenerator`  ·  college · difficulty 2

Precision, recall, and F1 from a binary confusion matrix.

**Variants:** `classifier_precision_recall_f1`

```
Problem: Given confusion matrix counts TP=25, FP=25, FN=29, TN=27, compute precision, recall, and F1 for the positive class.
Steps:
  METRICS_SETUP|TP=25, FP=25, FN=29, TN=27
  METRIC_FORMULA|precision=TP/(TP+FP)
  A|25|25|50
  D|25|50|1/2
  METRIC_FORMULA|recall=TP/(TP+FN)
  A|25|29|54
  D|25|54|25/54
  METRIC_FORMULA|F1=2PR/(P+R)
  M|1/2|25/54|25/108
  M|2|25/108|25/54
  A|1/2|25/54|26/27
  D|25/54|26/27|25/52
  Z|precision=1/2; recall=25/54; F1=25/52
Answer: precision=1/2; recall=25/54; F1=25/52
```

## Graduate

### Matrix Exponential — `MatrixExponentialGenerator`  ·  graduate · difficulty 3

Matrix exponential for diagonalizable 2x2 matrices: e^(At) = P*e^(Dt)*P^-1. Eigenvalues are small distinct integers and P is unimodular, so the symbolic entries are exact linear combinations of e^(lambda t) terms.

**Variants:** `matrix_exponential_diagonalizable`

```
Problem: Find e^(At) for A = [[5, -4], [2, -1]] by diagonalization.
Steps:
  MAT_SETUP|A = [[5, -4], [2, -1]]|compute e^(At)
  EIGENVALUE|λ = 1|diagonal entry of D
  EIGENVECTOR|λ = 1|[1, 1]
  CHECK|A*[1, 1]|[1, 1]|v = [1, 1]
  EIGENVALUE|λ = 3|diagonal entry of D
  EIGENVECTOR|λ = 3|[2, 1]
  CHECK|A*[2, 1]|[6, 3]|3*v = [6, 3]
  DIAG_FORM|P = [[1, 2], [1, 1]]|D = [[1, 0], [0, 3]]|P^-1 = [[-1, 2], [1, -1]]
  EXP_DIAG|e^(Dt)|[[e^t, 0], [0, e^(3t)]]
  EXP_FORM|e^(At) = P*e^(Dt)*P^-1
  EXP_ENTRY|(1,1)|-e^t + 2*e^(3t)|-e^t + 2*e^(3t)
  EXP_ENTRY|(1,2)|2*e^t - 2*e^(3t)|2*e^t - 2*e^(3t)
  EXP_ENTRY|(2,1)|-e^t + e^(3t)|-e^t + e^(3t)
  EXP_ENTRY|(2,2)|2*e^t - e^(3t)|2*e^t - e^(3t)
  CHECK|t = 0|[[1, 0], [0, 1]]|identity
  Z|e^(At)=[[-e^t + 2*e^(3t), 2*e^t - 2*e^(3t)], [-e^t + e^(3t), 2*e^t - e^(3t)]]
Answer: e^(At)=[[-e^t + 2*e^(3t), 2*e^t - 2*e^(3t)], [-e^t + e^(3t), 2*e^t - e^(3t)]]
```

### SVD — `SVDGenerator`  ·  graduate · difficulty 4

Singular value decomposition of symmetric 2x2 matrices via A^T A. Matrices have the form [[a, b], [b, a]], so A^T A has exact eigenvectors [1/sqrt(2), +/-1/sqrt(2)] and integer singular values.

**Variants:** `svd_symmetric_2x2`

```
Problem: Find an SVD A = U*Sigma*V^T for A = [[30, 13], [13, 30]] using A^T A.
Steps:
  MAT_SETUP|A = [[30, 13], [13, 30]]|SVD via A^T A
  ATA|A^T A|[[1069, 780], [780, 1069]]
  EIGENVALUE|λ1 = 1849|from (30 + 13)^2
  EIGENVECTOR|λ1 = 1849|[1/√2, 1/√2]
  ROOT|√1849|43
  AV_VECTOR|A*v1|[43/√2, 43/√2]
  U_VECTOR|u1 = A*v1/σ1|[1/√2, 1/√2]
  EIGENVALUE|λ2 = 289|from (30 - 13)^2
  EIGENVECTOR|λ2 = 289|[1/√2, -1/√2]
  ROOT|√289|17
  AV_VECTOR|A*v2|[17/√2, -17/√2]
  U_VECTOR|u2 = A*v2/σ2|[1/√2, -1/√2]
  CHECK|U*Sigma*V^T|[[30, 13], [13, 30]]|matches A
  Z|U=[[1/√2, 1/√2], [1/√2, -1/√2]]; Sigma=[[43, 0], [0, 17]]; V^T=[[1/√2, 1/√2], [1/√2, -1/√2]]
Answer: U=[[1/√2, 1/√2], [1/√2, -1/√2]]; Sigma=[[43, 0], [0, 17]]; V^T=[[1/√2, 1/√2], [1/√2, -1/√2]]
```

### Series Solution — `SeriesSolutionGenerator`  ·  graduate · difficulty 4

Power-series solutions of differential equations by coefficient matching.

**Variants:** `series_solution_first_order_exp`

```
Problem: Find the power-series solution through x^5 for y' = y with y(0) = 5880.
Steps:
  ODE_SETUP|y' = y, y(0) = 5880|power series through x^5
  SERIES_ASSUME|y|sum a_n x^n
  DERIV_SERIES|y'|sum (n+1)a_(n+1)x^n
  REWRITE|y|sum a_n x^n
  COEFF_MATCH|x^n|(n+1)a_(n+1) = a_n
  RECURRENCE|a_(n+1)|a_n/(n+1)
  INITIAL_COEFF|a_0|5880
  M|1|5880|5880
  D|5880|1|5880
  COEFF|a_1|5880
  M|1|5880|5880
  D|5880|2|2940
  COEFF|a_2|2940
  M|1|2940|2940
  D|2940|3|980
  COEFF|a_3|980
  M|1|980|980
  D|980|4|245
  COEFF|a_4|245
  M|1|245|245
  D|245|5|49
  COEFF|a_5|49
  Z|y = 5880 + 5880x + 2940x^2 + 980x^3 + 245x^4 + 49x^5 + O(x^6)
Answer: y = 5880 + 5880x + 2940x^2 + 980x^3 + 245x^4 + 49x^5 + O(x^6)
```

### Generating Function — `GeneratingFunctionGenerator`  ·  graduate · difficulty 4

Coefficient extraction from simple generating-function products.

**Variants:** `generating_function_binomial_product`, `generating_function_geometric_product`

```
Problem: Find the coefficient of x^18 in 1/((1 - x^3)(1 - x^5)).
Steps:
  GF_SETUP|[x^18]|1/((1 - x^3)(1 - x^5))
  GF_EXPAND|1/(1 - x^3)|sum x^(3i), i >= 0
  GF_EXPAND|1/(1 - x^5)|sum x^(5j), j >= 0
  M|3|0|0
  S|18|0|18
  GF_DIV_CHECK|18 / 5|not integer|reject
  M|3|1|3
  S|18|3|15
  D|15|5|3
  COEFF_PAIR|i=1, j=3|3i + 5j = 18|accepted
  A|0|1|1
  M|3|2|6
  S|18|6|12
  GF_DIV_CHECK|12 / 5|not integer|reject
  M|3|3|9
  S|18|9|9
  GF_DIV_CHECK|9 / 5|not integer|reject
  M|3|4|12
  S|18|12|6
  GF_DIV_CHECK|6 / 5|not integer|reject
  M|3|5|15
  S|18|15|3
  GF_DIV_CHECK|3 / 5|not integer|reject
  M|3|6|18
  S|18|18|0
  D|0|5|0
  COEFF_PAIR|i=6, j=0|3i + 5j = 18|accepted
  A|1|1|2
  Z|coefficient = 2
Answer: coefficient = 2
```

### Quadratic Residue — `QuadraticResidueGenerator`  ·  graduate · difficulty 4

Legendre symbol computation by Euler's criterion.

**Variants:** `quadratic_residue_legendre`

```
Problem: Use Euler's criterion to compute Legendre(99,29).
Steps:
  LEGENDRE_SETUP|a=99|p=29
  S|29|1|28
  D|28|2|14
  MOD_REDUCE|99|mod 29|12
  BINARY_EXPONENT|14|1110
  M|1|1|1
  MOD_REDUCE|1|mod 29|1
  MODEXP_SQUARE|bit 1=1|1
  M|1|12|12
  MOD_REDUCE|12|mod 29|12
  MODEXP_MULTIPLY|bit 1=1|12
  MODEXP_STATE|after bit 1|12
  M|12|12|144
  MOD_REDUCE|144|mod 29|28
  MODEXP_SQUARE|bit 2=1|28
  M|28|12|336
  MOD_REDUCE|336|mod 29|17
  MODEXP_MULTIPLY|bit 2=1|17
  MODEXP_STATE|after bit 2|17
  M|17|17|289
  MOD_REDUCE|289|mod 29|28
  MODEXP_SQUARE|bit 3=1|28
  M|28|12|336
  MOD_REDUCE|336|mod 29|17
  MODEXP_MULTIPLY|bit 3=1|17
  MODEXP_STATE|after bit 3|17
  M|17|17|289
  MOD_REDUCE|289|mod 29|28
  MODEXP_SQUARE|bit 4=0|28
  MODEXP_MULTIPLY|bit 4=0|skip
  MODEXP_STATE|after bit 4|28
  EULER_CRITERION|99^14 mod 29|28
  LEGENDRE_RESULT|28|-1|quadratic nonresidue
  Z|Legendre(99,29) = -1
Answer: Legendre(99,29) = -1
```

### Primality Test — `PrimalityTestGenerator`  ·  graduate · difficulty 4

Miller-Rabin primality test traces with supplied witnesses.

**Variants:** `primality_test_miller_rabin`

```
Problem: Use the Miller-Rabin test on n=221 with witnesses 4, 18.
Steps:
  MR_SETUP|n=221|witnesses 4, 18
  D|220|2|110
  D|110|2|55
  MR_DECOMPOSE|220|2^2 * 55
  MR_WITNESS|4
  MOD_POWER|4^55|mod 221|30
  M|30|30|900
  MOD_REDUCE|900|mod 221|16
  MR_SQUARE|r=1|16
  MR_WITNESS_RESULT|4|composite
  Z|composite; witness = 4
Answer: composite; witness = 4
```

### Coset — `CosetGenerator`  ·  graduate · difficulty 4

Left coset enumeration in small finite groups.

**Variants:** `coset_d3`, `coset_units`, `coset_zn`

```
Problem: In U(60) under multiplication modulo 60, let H=<43>. Enumerate the distinct left cosets aH.
Steps:
  GROUP_SETUP|U(60)|multiplication mod n|group size 16
  SUBGROUP_START|H=<43>|identity 1
  M|1|43|43
  MOD_REDUCE|43|mod 60|43
  SUBGROUP_ELEM|k=1|43
  M|43|43|1849
  MOD_REDUCE|1849|mod 60|49
  SUBGROUP_ELEM|k=2|49
  M|49|43|2107
  MOD_REDUCE|2107|mod 60|7
  SUBGROUP_ELEM|k=3|7
  M|7|43|301
  MOD_REDUCE|301|mod 60|1
  SUBGROUP_ELEM|k=4|1
  SUBGROUP|H={1, 43, 49, 7}|size 4
  COSET_START|rep 1|1H
  M|1|1|1
  MOD_REDUCE|1|mod 60|1
  COSET_ELEM|1H|1
  M|1|43|43
  MOD_REDUCE|43|mod 60|43
  COSET_ELEM|1H|43
  M|1|49|49
  MOD_REDUCE|49|mod 60|49
  COSET_ELEM|1H|49
  M|1|7|7
  MOD_REDUCE|7|mod 60|7
  COSET_ELEM|1H|7
  COSET|1H|{1, 43, 49, 7}
  COSET_SKIP|7|already listed
  COSET_START|rep 11|11H
  M|11|1|11
  MOD_REDUCE|11|mod 60|11
  COSET_ELEM|11H|11
  M|11|43|473
  MOD_REDUCE|473|mod 60|53
  COSET_ELEM|11H|53
  M|11|49|539
  MOD_REDUCE|539|mod 60|59
  COSET_ELEM|11H|59
  M|11|7|77
  MOD_REDUCE|77|mod 60|17
  COSET_ELEM|11H|17
  COSET|11H|{11, 53, 59, 17}
  COSET_START|rep 13|13H
  M|13|1|13
  MOD_REDUCE|13|mod 60|13
  COSET_ELEM|13H|13
  M|13|43|559
  MOD_REDUCE|559|mod 60|19
  COSET_ELEM|13H|19
  M|13|49|637
  MOD_REDUCE|637|mod 60|37
  COSET_ELEM|13H|37
  M|13|7|91
  MOD_REDUCE|91|mod 60|31
  COSET_ELEM|13H|31
  COSET|13H|{13, 19, 37, 31}
  COSET_SKIP|17|already listed
  COSET_SKIP|19|already listed
  COSET_START|rep 23|23H
  M|23|1|23
  MOD_REDUCE|23|mod 60|23
  COSET_ELEM|23H|23
  M|23|43|989
  MOD_REDUCE|989|mod 60|29
  COSET_ELEM|23H|29
  M|23|49|1127
  MOD_REDUCE|1127|mod 60|47
  COSET_ELEM|23H|47
  M|23|7|161
  MOD_REDUCE|161|mod 60|41
  COSET_ELEM|23H|41
  COSET|23H|{23, 29, 47, 41}
  COSET_SKIP|29|already listed
  COSET_SKIP|31|already listed
  COSET_SKIP|37|already listed
  COSET_SKIP|41|already listed
  COSET_SKIP|43|already listed
  COSET_SKIP|47|already listed
  COSET_SKIP|49|already listed
  COSET_SKIP|53|already listed
  COSET_SKIP|59|already listed
  D|16|4|4
  INDEX|G size 16|H size 4|4
  CHECK|cosets partition group|yes
  Z|cosets = 1H={1, 43, 49, 7}; 11H={11, 53, 59, 17}; 13H={13, 19, 37, 31}; 23H={23, 29, 47, 41}; index = 4
Answer: cosets = 1H={1, 43, 49, 7}; 11H={11, 53, 59, 17}; 13H={13, 19, 37, 31}; 23H={23, 29, 47, 41}; index = 4
```

### Finite Field — `FiniteFieldGenerator`  ·  graduate · difficulty 4

Polynomial arithmetic over prime fields and GF(2) polynomial division.

**Variants:** `finite_field_gf2_division`, `finite_field_zp`

```
Problem: Over GF(2), divide x^6 + x^4 + x^3 + x^2 + x + 1 by x^3 + x^2 + 1. Use XOR for coefficient arithmetic.
Steps:
  FIELD_SETUP|GF(2)[x]|addition is XOR
  POLYDIV_SETUP|x^6 + x^4 + x^3 + x^2 + x + 1|x^3 + x^2 + 1
  DIV_TERM|x^6|x^3|x^3
  GF2_XOR|quotient x^3|0 xor 1|1
  GF2_XOR|remainder x^3|1 xor 1|0
  GF2_XOR|remainder x^5|0 xor 1|1
  GF2_XOR|remainder x^6|1 xor 1|0
  POLY_REMAINDER|x^5 + x^4 + x^2 + x + 1
  DIV_TERM|x^5|x^3|x^2
  GF2_XOR|quotient x^2|0 xor 1|1
  GF2_XOR|remainder x^2|1 xor 1|0
  GF2_XOR|remainder x^4|1 xor 1|0
  GF2_XOR|remainder x^5|1 xor 1|0
  POLY_REMAINDER|x + 1
  QUOTIENT|x^3 + x^2
  R|x + 1
  Z|quotient = x^3 + x^2; remainder = x + 1
Answer: quotient = x^3 + x^2; remainder = x + 1
```

### Quaternion — `QuaternionGenerator`  ·  graduate · difficulty 4

Quaternion multiplication, conjugates, norms, inverses, and rotations.

**Variants:** `quaternion_arithmetic`, `quaternion_rotation`

```
Problem: Let q=(0,0,-1,0) and v=(0,-4,0,4) represent a unit quaternion and a pure-vector quaternion. Rotate v by q*v*q^-1.
Steps:
  QUAT_SETUP|q=(0,0,-1,0)|v=(0,-4,0,4)
  HAMILTON|i*i|-1
  HAMILTON|j*j|-1
  HAMILTON|k*k|-1
  HAMILTON|i*j|k
  HAMILTON|j*i|-k
  M|0|0|0
  A|0|0|0
  M|0|0|0
  A|0|0|0
  M|-1|-1|1
  A|0|1|1
  M|0|0|0
  A|1|0|1
  NORM_SQUARED|q|1
  CHECK|unit norm|yes
  CONJUGATE|q|(0,0,1,0)
  F|0|1|0
  F|0|1|0
  F|1|1|1
  F|0|1|0
  QUAT_INVERSE|q|(0,0,1,0)
  QUAT_MUL_START|q*v|q|v
  M|0|0|0
  A|0|0|0
  M|0|-4|0
  S|0|0|0
  A|0|0|0
  M|-1|0|0
  S|0|0|0
  A|0|0|0
  M|0|4|0
  S|0|0|0
  A|0|0|0
  QUAT_COMPONENT|q*v|real|0
  M|0|-4|0
  A|0|0|0
  M|0|0|0
  A|0|0|0
  M|-1|4|-4
  A|0|-4|-4
  M|0|0|0
  S|0|0|0
  A|-4|0|-4
  QUAT_COMPONENT|q*v|i|-4
  M|0|0|0
  A|0|0|0
  M|0|4|0
  S|0|0|0
  A|0|0|0
  M|-1|0|0
  A|0|0|0
  M|0|-4|0
  A|0|0|0
  QUAT_COMPONENT|q*v|j|0
  M|0|4|0
  A|0|0|0
  M|0|0|0
  A|0|0|0
  M|-1|-4|4
  S|0|4|-4
  A|0|-4|-4
  M|0|0|0
  A|-4|0|-4
  QUAT_COMPONENT|q*v|k|-4
  QUAT_RESULT|q*v|(0,-4,0,-4)
  QUAT_MUL_START|q*v*q^-1|q*v|q^-1
  M|0|0|0
  A|0|0|0
  M|-4|0|0
  S|0|0|0
  A|0|0|0
  M|0|1|0
  S|0|0|0
  A|0|0|0
  M|-4|0|0
  S|0|0|0
  A|0|0|0
  QUAT_COMPONENT|q*v*q^-1|real|0
  M|0|0|0
  A|0|0|0
  M|-4|0|0
  A|0|0|0
  M|0|0|0
  A|0|0|0
  M|-4|1|-4
  S|0|-4|4
  A|0|4|4
  QUAT_COMPONENT|q*v*q^-1|i|4
  M|0|1|0
  A|0|0|0
  M|-4|0|0
  S|0|0|0
  A|0|0|0
  M|0|0|0
  A|0|0|0
  M|-4|0|0
  A|0|0|0
  QUAT_COMPONENT|q*v*q^-1|j|0
  M|0|0|0
  A|0|0|0
  M|-4|1|-4
  A|0|-4|-4
  M|0|0|0
  S|0|0|0
  A|-4|0|-4
  M|-4|0|0
  A|-4|0|-4
  QUAT_COMPONENT|q*v*q^-1|k|-4
  QUAT_RESULT|q*v*q^-1|(0,4,0,-4)
  ROTATED_VECTOR|(4,0,-4)
  Z|qvq^-1 = (0,4,0,-4); vector = (4,0,-4)
Answer: qvq^-1 = (0,4,0,-4); vector = (4,0,-4)
```

### Complex Log — `ComplexLogGenerator`  ·  graduate · difficulty 4

Principal and multivalued complex logarithms, plus the principal power i^i = exp(i Log i).

**Variants:** `complex_log_log`, `complex_log_power_ii`

```
Problem: Find the principal Log and all logarithms of z = 49 cis(300 deg).
Steps:
  LOG_SETUP|z=49 cis(300 deg)
  S|300|360|-60
  ANGLE_WRAP|300 deg|-60 deg
  LOG_FORMULA|log z = ln r + i(arg + 2pi*k)
  PRINCIPAL_LOG|ln(49) - i*pi/3
  MULTIVALUED_LOG|ln(49) + i*(-pi/3 + 2pi*k)|k in Z
  Z|Log(z) = ln(49) - i*pi/3; log(z) = ln(49) + i*(-pi/3 + 2pi*k), k in Z
Answer: Log(z) = ln(49) - i*pi/3; log(z) = ln(49) + i*(-pi/3 + 2pi*k), k in Z
```

### Mobius Transform — `MobiusTransformGenerator`  ·  graduate · difficulty 4

Mobius transformation images, fixed points, and cross-ratios.

**Variants:** `mobius_transform_cross_ratio`, `mobius_transform_fixed_points`, `mobius_transform_image`

```
Problem: For T(z) = (-10)/(2z + 12), find the fixed points.
Steps:
  MOBIUS_SETUP|T(z)=(-10)/(2z + 12)|fixed points
  FIXED_EQ|z=(az+b)/(cz+d)
  EXPAND|c z^2 + (d-a)z - b = 0
  S|12|0|12
  S|0|-10|10
  QUADRATIC|2|12|10
  E|-5|2|25
  M|2|25|50
  M|12|-5|-60
  A|50|-60|-10
  A|-10|10|0
  CHECK|root -5|0
  FIXED_POINT|-5
  E|-1|2|1
  M|2|1|2
  M|12|-1|-12
  A|2|-12|-10
  A|-10|10|0
  CHECK|root -1|0
  FIXED_POINT|-1
  Z|fixed points = {-5, -1}
Answer: fixed points = {-5, -1}
```

### Residue — `ResidueGenerator`  ·  graduate · difficulty 4

Residues at simple and higher-order poles using local Laurent terms.

**Variants:** `residue_higher_order`, `residue_simple`

```
Problem: Find the residue at z=1 of f(z) = (-1 + (z-1) + 2(z-1)^2 + (z-1)^3)/(z-1)^2, whose numerator coefficients in powers of (z-1) are [-1, 1, 2, 1].
Steps:
  RESIDUE_SETUP|a=1|f=(-1 + (z-1) + 2(z-1)^2 + (z-1)^3)/(z-1)^2
  POLE_ORDER|2
  LAURENT_TERM|-1(z-1)^-2
  LAURENT_TERM|1(z-1)^-1
  LAURENT_TERM|2(z-1)^0
  LAURENT_TERM|1(z-1)^1
  RESIDUE|1
  Z|residue = 1
Answer: residue = 1
```

### Contour Integral — `ContourIntegralGenerator`  ·  graduate · difficulty 5

Contour integrals by the residue theorem over positively oriented circles centered at the origin.

**Variants:** `contour_integral_residue_theorem`

```
Problem: Evaluate the positively oriented contour integral over |z|=5 of f(z) = 3/(z-6) + 2/(z+8) + 1/(z+4).
Steps:
  CONTOUR_SETUP|abs(z)=5|positive orientation|f=3/(z-6) + 2/(z+8) + 1/(z+4)
  POLE_TEST|pole 6|abs(6) < 5|outside
  RESIDUE|pole 6|3|outside
  POLE_TEST|pole -8|abs(-8) < 5|outside
  RESIDUE|pole -8|2|outside
  POLE_TEST|pole -4|abs(-4) < 5|inside
  RESIDUE|pole -4|1|inside
  A|0|1|1
  RESIDUE_SUM|1
  M|2|1|2
  Z|integral = 2pi i
Answer: integral = 2pi i
```

### Laurent Series — `LaurentSeriesGenerator`  ·  graduate · difficulty 5

Taylor and Laurent coefficients for hand-friendly rational functions.

**Variants:** `laurent_series_geometric`, `laurent_series_pole`

```
Problem: Find the Taylor coefficients c_n for n=0..5 about z=2 of f(z) = -2/(z-7), written as sum c_n (z-2)^n.
Steps:
  LAURENT_SETUP|center a=2|w=(z-2)|f=-2/(z-7)
  REWRITE|(z-7) = w - 5|d=a-b=-5
  GEOMETRIC_FORMULA|c_n = A*(-1)^n/d^(n+1)|A=-2, d=-5
  E|-5|1|-5
  M|-2|1|-2
  D|-2|-5|2/5
  COEFF|c_0|2/5
  E|-5|2|25
  M|-2|-1|2
  D|2|25|2/25
  COEFF|c_1|2/25
  E|-5|3|-125
  M|-2|1|-2
  D|-2|-125|2/125
  COEFF|c_2|2/125
  E|-5|4|625
  M|-2|-1|2
  D|2|625|2/625
  COEFF|c_3|2/625
  E|-5|5|-3125
  M|-2|1|-2
  D|-2|-3125|2/3125
  COEFF|c_4|2/3125
  E|-5|6|15625
  M|-2|-1|2
  D|2|15625|2/15625
  COEFF|c_5|2/15625
  Z|c_0=2/5, c_1=2/25, c_2=2/125, c_3=2/625, c_4=2/3125, c_5=2/15625
Answer: c_0=2/5, c_1=2/25, c_2=2/125, c_3=2/625, c_4=2/3125, c_5=2/15625
```

### Spherical Triangle — `SphericalTriangleGenerator`  ·  graduate · difficulty 4

Mechanical spherical-triangle calculations with supplied exact trig values.

**Variants:** `spherical_triangle_cosines`, `spherical_triangle_sines`

```
Problem: In a spherical triangle, side a=150 deg, side b=90 deg, and angle A=150 deg. Given sin(a)=1/2, sin(b)=1, and sin(A)=1/2, use the spherical law of sines to find sin(B).
Steps:
  SPHERICAL_TRIANGLE_SETUP|a=150 deg, b=90 deg, A=150 deg|find sin(B)
  SPHERICAL_SINE_LAW|sin(A)/sin(a)=sin(B)/sin(b)
  TRIG_VALUE|sin(a)=1/2|sin(b)=1|sin(A)=1/2
  M|1|1/2|1/2
  D|1/2|1/2|1
  Z|sin(B) = 1
Answer: sin(B) = 1
```

### Hyperbolic Distance — `HyperbolicDistanceGenerator`  ·  graduate · difficulty 4

Poincare half-plane and disk distances in exact logarithmic form.

**Variants:** `hyperbolic_distance_disk_radial`, `hyperbolic_distance_half_plane`

```
Problem: In the Poincare disk, P=(0,0) and Q=(5/29,0) lie on a diameter. Use d=ln((1+r)/(1-r)) to find the hyperbolic distance.
Steps:
  HYPERBOLIC_DISTANCE_SETUP|disk|P=(0,0)|Q=(5/29,0)
  FORMULA|radial disk distance = ln((1+r)/(1-r))
  A|1|5/29|34/29
  S|1|5/29|24/29
  D|34/29|24/29|17/12
  LOG_EVAL|17/12|ln(17/12)
  Z|distance = ln(17/12)
Answer: distance = ln(17/12)
```

### Stereographic — `StereographicGenerator`  ·  graduate · difficulty 4

Stereographic projection between the plane and the unit sphere, using the north pole and the plane z=0.

**Variants:** `stereographic_plane_to_sphere`, `stereographic_sphere_to_plane`

```
Problem: Map sphere point (X,Y,Z)=(4/41,-24/41,33/41) with Z != 1 to the plane by inverse stereographic projection from the north pole.
Steps:
  STEREO_SETUP|sphere_to_plane|X=4/41|Y=-24/41|Z=33/41
  FORMULA|u=X/(1-Z); v=Y/(1-Z)
  S|1|33/41|8/41
  D|4/41|8/41|1/2
  D|-24/41|8/41|-3
  Z|plane point = (1/2, -3)
Answer: plane point = (1/2, -3)
```

### Fundamental Form — `FundamentalFormGenerator`  ·  graduate · difficulty 4

First fundamental form coefficients and patch area for standard parametrized surfaces.

**Variants:** `fundamental_form_cylinder_patch`, `fundamental_form_sphere_patch`

```
Problem: For the sphere r(theta,phi)=(8 sin phi cos theta,8 sin phi sin theta,8 cos phi), 0<=theta<=pi/6 and 90<=phi<=120. Given cos(90)=0 and cos(120)=-1/2, find E, F, G and the patch area.
Steps:
  FUNDAMENTAL_FORM_SETUP|sphere|R=8|theta in [0,pi/6], phi in [90,120]
  PARTIAL|r_theta=(-R sin phi sin theta,R sin phi cos theta,0)|r_phi=(R cos phi cos theta,R cos phi sin theta,-R sin phi)
  DOT|r_theta dot r_theta|64sin^2(phi)
  DOT|r_theta dot r_phi|0
  E|8|2|64
  DOT|r_phi dot r_phi|64
  AREA_INTEGRAL|sqrt(EG-F^2)=R^2 sin(phi)|area = R^2*theta*(cos phi1 - cos phi2)
  S|0|-1/2|1/2
  M|64|1/6|32/3
  M|32/3|1/2|16/3
  Z|E = 64sin^2(phi), F = 0, G = 64, area = 16pi/3
Answer: E = 64sin^2(phi), F = 0, G = 64, area = 16pi/3
```

### Christoffel — `ChristoffelGenerator`  ·  graduate · difficulty 5

Christoffel symbols for hand-friendly 2D diagonal metrics.

**Variants:** `christoffel_polar`, `christoffel_sphere`

```
Problem: For the sphere metric ds^2 = R^2 dphi^2 + R^2 sin^2(phi) dtheta^2 with R=109, compute the nonzero Christoffel symbols at phi=45 deg. Given sin(phi)=sqrt(2)/2 and cos(phi)=sqrt(2)/2.
Steps:
  CHRISTOFFEL_SETUP|sphere|g_phiphi=R^2, g_thetatheta=R^2 sin^2(phi)|R=109, phi=45 deg
  INVERSE_METRIC|g^phiphi=1/R^2|g^thetatheta=1/(R^2 sin^2(phi))
  CHRISTOFFEL_FORMULA|Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)
  E|109|2|11881
  TRIG_VALUE|sin(phi)=sqrt(2)/2|cos(phi)=sqrt(2)/2
  DERIV|d_phi g_thetatheta|2R^2 sin(phi)cos(phi)
  M|sqrt(2)/2|sqrt(2)/2|1/2
  M|-1|1/2|-1/2
  D|sqrt(2)/2|sqrt(2)/2|1
  Z|Gamma^phi_thetatheta = -1/2, Gamma^theta_phitheta = Gamma^theta_thetaphi = 1
Answer: Gamma^phi_thetatheta = -1/2, Gamma^theta_phitheta = Gamma^theta_thetaphi = 1
```

### Gaussian Curvature — `GaussianCurvatureGenerator`  ·  graduate · difficulty 5

Gaussian curvature for hand-friendly surfaces.

**Variants:** `gaussian_curvature_saddle`, `gaussian_curvature_sphere`

```
Problem: For the saddle surface z=(14x^2-2y^2)/2, find the Gaussian curvature at the origin using the graph curvature formula.
Steps:
  GAUSSIAN_CURVATURE_SETUP|saddle|z=(14x^2-2y^2)/2|point=(0,0)
  FORMULA|K=(f_xx f_yy - f_xy^2)/(1+f_x^2+f_y^2)^2
  DERIV|f_x=0, f_y=0|f_xx=14|f_yy=-2, f_xy=0
  M|14|-2|-28
  E|0|2|0
  S|-28|0|-28
  A|1|0|1
  E|1|2|1
  D|-28|1|-28
  CHECK|negative curvature|-28|saddle
  Z|K = -28
Answer: K = -28
```

### Gauss Bonnet — `GaussBonnetGenerator`  ·  graduate · difficulty 4

Gauss-Bonnet verification for closed surfaces: integral K dA = 2*pi*chi.

**Variants:** `gauss_bonnet_flat_torus`, `gauss_bonnet_sphere`

```
Problem: Verify Gauss-Bonnet for a flat rectangular torus of width 28 and height 4, with Euler characteristic 0.
Steps:
  GAUSS_BONNET_SETUP|flat_torus|width=28, height=4|chi=0
  THEOREM|integral K dA = 2*pi*chi
  M|28|4|112
  M|0|112|0
  M|2|0|0
  CHECK|integral K dA|0|2pi chi = 0
  Z|verified: integral K dA = 0 = 2pi chi
Answer: verified: integral K dA = 0 = 2pi chi
```

### Metric Arc Length — `MetricArcLengthGenerator`  ·  graduate · difficulty 4

Arc length from a metric along simple polar-coordinate paths.

**Variants:** `metric_arc_length_circle`, `metric_arc_length_radial`

```
Problem: In polar coordinates with metric ds^2=dr^2+r^2 dtheta^2, find the length of the path r=26 from theta=0 to theta=pi/2.
Steps:
  METRIC_ARC_SETUP|polar metric|ds^2=dr^2+r^2 dtheta^2|r=26, theta:0->pi/2
  METRIC_RESTRICT|dr=0|ds^2=r^2 dtheta^2
  E|26|2|676
  ROOT|676|26
  INTEGRAL_SETUP|L = integral from 0 to pi/2 of 26 dtheta
  M|26|1/2|13
  Z|length = 13pi
Answer: length = 13pi
```

### Function Inner Product — `FunctionInnerProductGenerator`  ·  graduate · difficulty 3

Function-space inner products for the sin/cos family on [0, 2pi].

**Variants:** `function_inner_product_cross_family`, `function_inner_product_same_family`

```
Problem: Compute the inner product of sin(49x) and cos(27x) on [0,2pi].
Steps:
  INNER_PRODUCT_SETUP|interval=[0,2pi]|f=sin(49x)|g=cos(27x)
  IDENTITY|sin(49x)*cos(27x)|1/2(sin(76x) + sin(22x))
  INTEGRAL|integral sin(76x) on [0,2pi]|0
  INTEGRAL|integral sin(22x) on [0,2pi]|0
  A|0|0|0
  D|0|2|0
  CHECK|sin-cos family|orthogonal
  Z|inner product = 0
Answer: inner product = 0
```

### Legendre Construction — `LegendreConstructionGenerator`  ·  graduate · difficulty 4

Construct P_2 or P_3 by Gram-Schmidt on {1, x, x^2, x^3} over [-1, 1], then scale to the standard Legendre leading coefficient.

**Variants:** `legendre_construction_p2`, `legendre_construction_p3`

```
Problem: Use Gram-Schmidt on {1, x, x^2, x^3} over [-1,1] to construct the Legendre polynomial P_3 with leading coefficient 5/2.
Steps:
  LEGENDRE_SETUP|target=P_3|inner product integral_-1^1 f(x)g(x) dx
  INTEGRAL|<x,x>|2/3
  INTEGRAL|<x^3,x>|2/5
  D|2/5|2/3|3/5
  PROJECTION|x^3 onto x|3/5
  POLY_SUB|x^3|3x/5|x^3 - 3x/5
  POLY_SCALE|x^3 - 3x/5|5/2|(5x^3 - 3x)/2
  Z|P_3(x) = (5x^3 - 3x)/2
Answer: P_3(x) = (5x^3 - 3x)/2
```

### Partial Trace — `PartialTraceGenerator`  ·  graduate · difficulty 4

Reduced density matrices by tracing out qubit B for two canonical two-qubit states.

**Variants:** `partial_trace_bell_phi_plus`, `partial_trace_product_plus_zero`

```
Problem: Trace out qubit B for product state plus0 = (ket00 + ket10)/sqrt(2).
Steps:
  DENSITY_SETUP|state=plus0|psi=(ket00 + ket10)/sqrt(2)
  OUTER_PRODUCT|rho=1/2(ket00bra00+ket00bra10+ket10bra00+ket10bra10)
  PARTIAL_TRACE|ket00bra00|ket0bra0
  PARTIAL_TRACE|ket00bra10|ket0bra1
  PARTIAL_TRACE|ket10bra00|ket1bra0
  PARTIAL_TRACE|ket10bra10|ket1bra1
  REDUCED_DENSITY|rho_A=[[1/2,1/2],[1/2,1/2]]
  CHECK|Tr(rho_A^2)|1|pure separable
  Z|rho_A = [[1/2,1/2],[1/2,1/2]]; entangled no
Answer: rho_A = [[1/2,1/2],[1/2,1/2]]; entangled no
```

### Density Matrix — `DensityMatrixGenerator`  ·  graduate · difficulty 4

Build a diagonal density matrix from a two-state ensemble, then compute expectation Tr(rho A) and purity Tr(rho^2).

**Variants:** `density_matrix_diagonal`

```
Problem: An ensemble has probability 13/15 of ket0 and the remaining probability of ket1. For observable A=diag(-9,-2), build rho, compute Tr(rho A), and compute Tr(rho^2).
Steps:
  DENSITY_SETUP|p0=13/15|p1=1-p0|A=diag(-9,-2)
  S|1|13/15|2/15
  DENSITY_MATRIX|rho=[[13/15,0],[0,2/15]]
  TRACE_EXPECT|Tr(rho A)=p0*a+p1*b
  M|13/15|-9|-39/5
  M|2/15|-2|-4/15
  A|-39/5|-4/15|-121/15
  E|13/15|2|169/225
  E|2/15|2|4/225
  A|169/225|4/225|173/225
  PURITY|Tr(rho^2)=173/225
  Z|rho = [[13/15,0],[0,2/15]]; expectation = -121/15; purity = 173/225
Answer: rho = [[13/15,0],[0,2/15]]; expectation = -121/15; purity = 173/225
```

### Von Neumann Entropy — `VonNeumannEntropyGenerator`  ·  graduate · difficulty 4

Von Neumann entropy from dyadic eigenvalues: S(rho) = -sum lambda_i log2(lambda_i).

**Variants:** `von_neumann_entropy_dyadic`

```
Problem: Compute the von Neumann entropy in bits for a density matrix with eigenvalues [1/4,1/4,1/4,1/4].
Steps:
  ENTROPY_SETUP|eigenvalues=[1/4,1/4,1/4,1/4]|S=-sum lambda log2(lambda)
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|0|1/2|1/2
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|1/2|1/2|1
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|1|1/2|3/2
  LOG2|1/4|-2
  M|1/4|2|1/2
  A|3/2|1/2|2
  Z|S = 2 bits
Answer: S = 2 bits
```

### Projector — `ProjectorGenerator`  ·  graduate · difficulty 3

Verify projector idempotence and completeness relations.

**Variants:** `projector_basis_completeness`, `projector_plus_projector`

```
Problem: Verify projector completeness for P0=[[1,0],[0,0]] and P1=[[0,0],[0,1]].
Steps:
  PROJECTOR_SETUP|P0=[[1,0],[0,0]]|P1=[[0,0],[0,1]]
  MATRIX_MULT|P0^2|[[1,0],[0,0]]
  MATRIX_MULT|P1^2|[[0,0],[0,1]]
  MATRIX_ADD|P0+P1|[[1,0],[0,1]]
  CHECK|sum_i Pi|[[1,0],[0,1]]|complete
  Z|complete yes; P0 + P1 = I
Answer: complete yes; P0 + P1 = I
```

### Uncertainty — `UncertaintyGenerator`  ·  graduate · difficulty 5

Uncertainty product for a particle in a 1D box with L=1 and hbar=1.

**Variants:** `uncertainty_particle_box`

```
Problem: For a particle in a 1D box with L=1 and hbar=1 in state n=99, use the supplied expectation formulas to compute Delta x Delta p exactly.
Steps:
  UNCERTAINTY_SETUP|particle in a box|L=1, hbar=1|n=99
  FORMULA|<x>=1/2|<x^2>=1/3 - 1/(2 n^2 pi^2)
  FORMULA|<p>=0|<p^2>=n^2 pi^2
  E|99|2|9801
  M|2|9801|19602
  VARIANCE|Delta x^2|1/12 - 1/(19602pi^2)
  VARIANCE|Delta p^2|9801pi^2
  PRODUCT|Delta x^2 * Delta p^2|9801pi^2/12 - 1/2
  CHECK|Heisenberg lower bound|>= 1/4|holds
  Z|Delta x Delta p = sqrt(9801pi^2/12 - 1/2)
Answer: Delta x Delta p = sqrt(9801pi^2/12 - 1/2)
```

### Matrix Group Check — `MatrixGroupCheckGenerator`  ·  graduate · difficulty 3

Matrix group membership checks for exact 2x2 rotation matrices.

**Variants:** `matrix_group_check_so2`, `matrix_group_check_su2`

```
Problem: Check whether M=[[112/113,-15/113],[15/113,112/113]] is a member of SU2.
Steps:
  MATRIX_GROUP_SETUP|SU2|M=[[112/113,-15/113],[15/113,112/113]]
  E|112/113|2|12544/12769
  E|15/113|2|225/12769
  A|12544/12769|225/12769|1
  CHECK|U^dagger U|I|metric preserved
  M|112/113|112/113|12544/12769
  M|-15/113|15/113|-225/12769
  S|12544/12769|-225/12769|1
  CHECK|det M|1|special
  Z|SU2 member yes; U^dagger U = I, det = 1
Answer: SU2 member yes; U^dagger U = I, det = 1
```

### Lie Exponential — `LieExponentialGenerator`  ·  graduate · difficulty 4

Exponentiate standard Lie algebra generators into exact rotation matrices.

**Variants:** `lie_exponential_so2`, `lie_exponential_so3`

```
Problem: Exponentiate the so(3) element theta=660 deg about the x-axis with K=[[0, 0, 0], [0, 0, -1], [0, 1, 0]].
Steps:
  LIE_EXP_SETUP|SO3|axis=x|theta=660 deg|K=[[0, 0, 0], [0, 0, -1], [0, 1, 0]]
  MOD_REDUCE|660|mod 360|300
  MATRIX_POWER|K^2|[[0, 0, 0], [0, -1, 0], [0, 0, -1]]
  RODRIGUES_FORM|e^(theta K)|I + sin(theta)K + (1-cos(theta))K^2
  TABLE_LOOKUP|cos 300 deg|1/2
  TABLE_LOOKUP|sin 300 deg|-sqrt3/2
  MAT_ENTRY|(1,1)|1|1
  MAT_ENTRY|(1,2)|0|0
  MAT_ENTRY|(1,3)|0|0
  MAT_ENTRY|(2,1)|0|0
  MAT_ENTRY|(2,2)|cos(theta)|1/2
  MAT_ENTRY|(2,3)|-sin(theta)|sqrt3/2
  MAT_ENTRY|(3,1)|0|0
  MAT_ENTRY|(3,2)|sin(theta)|-sqrt3/2
  MAT_ENTRY|(3,3)|cos(theta)|1/2
  CHECK|R^T R|I|orthogonal
  CHECK|det R|1|proper rotation
  Z|e^(theta K_x)=[[1, 0, 0], [0, 1/2, sqrt3/2], [0, -sqrt3/2, 1/2]]
Answer: e^(theta K_x)=[[1, 0, 0], [0, 1/2, sqrt3/2], [0, -sqrt3/2, 1/2]]
```

### Structure Constant — `StructureConstantGenerator`  ·  graduate · difficulty 4

Verify su(2) structure constants with explicit matrix commutators.

**Variants:** `structure_constant_su2`

```
Problem: For spin-1/2 generators Jx=[[0,1/2],[1/2,0]], Jy=[[0,-i/2],[i/2,0]], Jz=[[1/2,0],[0,-1/2]], compute [A,B] for A=-4Jy and B=Jz and verify the structure constant.
Steps:
  STRUCTURE_SETUP|A=-4Jy|B=Jz|epsilon_yzx=1
  MATRIX_VALUE|A|[[0, 2i], [-2i, 0]]
  MATRIX_VALUE|B|[[1/2, 0], [0, -1/2]]
  MATRIX_PRODUCT|AB|[[0, -i], [-i, 0]]
  MATRIX_PRODUCT|BA|[[0, i], [i, 0]]
  COMM_ENTRY|(1,1)|0 - 0|0
  COMM_ENTRY|(1,2)|-i - i|-2i
  COMM_ENTRY|(2,1)|-i - i|-2i
  COMM_ENTRY|(2,2)|0 - 0|0
  COMMUTATOR|[A,B]|[[0, -2i], [-2i, 0]]
  STRUCTURE_CONSTANT|epsilon_yzx|1|-4iJx
  MATRIX_VALUE|-4iJx|[[0, -2i], [-2i, 0]]
  CHECK|[A,B]|-4iJx|verified
  Z|[A,B] = -4iJx = [[0, -2i], [-2i, 0]]
Answer: [A,B] = -4iJx = [[0, -2i], [-2i, 0]]
```

### Pauli Algebra — `PauliAlgebraGenerator`  ·  graduate · difficulty 3

Pauli products, anticommutators, traces, and Gell-Mann trace identities.

**Variants:** `pauli_algebra_anticommutator`, `pauli_algebra_gellmann_trace`, `pauli_algebra_product`, `pauli_algebra_trace`

```
Problem: For Gell-Mann matrices lambda_1 through lambda_7, compute Tr(AB) for A=-4lambda_7 and B=lambda_4.
Steps:
  GELLMANN_SETUP|trace|A=-4lambda_7|B=lambda_4
  MATRIX_VALUE|A|[[0, 0, 0], [0, 0, 4i], [0, -4i, 0]]
  MATRIX_VALUE|B|[[0, 0, 1], [0, 0, 0], [1, 0, 0]]
  MATRIX_PRODUCT|AB|[[0, 0, 0], [4i, 0, 0], [0, 0, 0]]
  TRACE_ENTRY|(1,1)|0
  TRACE_ENTRY|(2,2)|0
  TRACE_ENTRY|(3,3)|0
  TRACE_SUM|0 + 0 + 0|0
  GELLMANN_IDENTITY|Tr(lambda_7 lambda_4)|2 delta_ab|0
  CHECK|Tr(AB)|0|verified
  Z|Tr(AB) = 0
Answer: Tr(AB) = 0
```

### Casimir — `CasimirGenerator`  ·  graduate · difficulty 4

Verify the spin-1 Casimir using ladder-operator products: J^2 = Jz^2 + (J+J- + J-J+)/2 = j(j+1) hbar^2 I.

**Variants:** `casimir_spin1`

```
Problem: Verify the spin-1 Casimir for hbar=19/4 using Jplus=hbar*sqrt2[[0,1,0],[0,0,1],[0,0,0]], Jminus=hbar*sqrt2[[0,0,0],[1,0,0],[0,1,0]], and Jz=hbar*[[1,0,0],[0,0,0],[0,0,-1]].
Steps:
  CASIMIR_SETUP|spin=1|hbar=19/4|J^2=Jz^2+(J+J-+J-J+)/2
  E|19/4|2|361/16
  MATRIX_PRODUCT|Jz^2|[[361/16, 0, 0], [0, 0, 0], [0, 0, 361/16]]
  MATRIX_PRODUCT|J+J-|[[361/8, 0, 0], [0, 361/8, 0], [0, 0, 0]]
  MATRIX_PRODUCT|J-J+|[[0, 0, 0], [0, 361/8, 0], [0, 0, 361/8]]
  MATRIX_ADD|J+J- + J-J+|[[361/8, 0, 0], [0, 361/4, 0], [0, 0, 361/8]]
  MATRIX_SCALE|1/2 ladder sum|[[361/16, 0, 0], [0, 361/8, 0], [0, 0, 361/16]]
  MATRIX_ADD|Jz^2 + ladder half|[[361/8, 0, 0], [0, 361/8, 0], [0, 0, 361/8]]
  A|1|1|2
  M|2|361/16|361/8
  CHECK|J^2|361/8I|verified
  Z|J^2 = 361/8I = [[361/8, 0, 0], [0, 361/8, 0], [0, 0, 361/8]]
Answer: J^2 = 361/8I = [[361/8, 0, 0], [0, 361/8, 0], [0, 0, 361/8]]
```

### Index Gymnastics — `IndexGymnasticsGenerator`  ·  graduate · difficulty 4

Levi-Civita contraction arithmetic: sum_i eps_ijk eps_ilm = delta_jl delta_km - delta_jm delta_kl.

**Variants:** `index_gymnastics_levi_civita`

```
Problem: Evaluate c * sum_i eps_i21 eps_i23 with c=2 for j=2, k=1, l=2, m=3 in 3D, and verify the Kronecker-delta identity.
Steps:
  INDEX_SETUP|c=2|j=2, k=1|l=2, m=3
  IDENTITY|sum_i eps_ijk eps_ilm|delta_jl delta_km - delta_jm delta_kl
  EPSILON_VALUE|eps_121|0
  EPSILON_VALUE|eps_123|1
  M|0|1|0
  EPSILON_VALUE|eps_221|0
  EPSILON_VALUE|eps_223|0
  M|0|0|0
  EPSILON_VALUE|eps_321|-1
  EPSILON_VALUE|eps_323|0
  M|-1|0|0
  A|0|0|0
  A|0|0|0
  DELTA_VALUE|delta_22|1
  DELTA_VALUE|delta_13|0
  DELTA_VALUE|delta_23|0
  DELTA_VALUE|delta_12|0
  M|1|0|0
  M|0|0|0
  S|0|0|0
  CHECK|epsilon contraction|0|identity
  M|2|0|0
  Z|2*sum_i eps_i21 eps_i23 = 0
Answer: 2*sum_i eps_i21 eps_i23 = 0
```

### BCH — `BCHGenerator`  ·  graduate · difficulty 5

Baker-Campbell-Hausdorff for nilpotent 3x3 elementary matrices.

**Variants:** `bch_nilpotent_second_order`

```
Problem: For nilpotent 3x3 matrices A=2E23 and B=-5E12, where Eij has a 1 in row i and column j, use BCH to second order to compute log(e^A e^B).
Steps:
  BCH_SETUP|A=2E23|B=-5E12|order=2
  MATRIX_EXP|e^A|I + A|[[1, 0, 0], [0, 1, 2], [0, 0, 1]]
  MATRIX_EXP|e^B|I + B|[[1, -5, 0], [0, 1, 0], [0, 0, 1]]
  MATRIX_PRODUCT|e^A e^B|[[1, -5, 0], [0, 1, 2], [0, 0, 1]]
  MATRIX_PRODUCT|AB|[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
  MATRIX_PRODUCT|BA|[[0, 0, -10], [0, 0, 0], [0, 0, 0]]
  MATRIX_SUB|AB - BA|[[0, 0, 10], [0, 0, 0], [0, 0, 0]]
  MATRIX_SCALE|1/2[A,B]|[[0, 0, 5], [0, 0, 0], [0, 0, 0]]
  MATRIX_ADD|A+B|[[0, -5, 0], [0, 0, 2], [0, 0, 0]]
  BCH_FORM|A+B+1/2[A,B]|[[0, -5, 5], [0, 0, 2], [0, 0, 0]]
  CHECK|[A,[A,B]] and [B,[A,B]]|0|truncates
  Z|log(e^A e^B) = [[0, -5, 5], [0, 0, 2], [0, 0, 0]]
Answer: log(e^A e^B) = [[0, -5, 5], [0, 0, 2], [0, 0, 0]]
```

### Young Tableaux — `YoungTableauxGenerator`  ·  graduate · difficulty 4

Young-tableaux arithmetic for representation dimensions and simple SU(3) tensor-product decompositions.

**Variants:** `young_tableaux_hook_length`, `young_tableaux_su3_decomposition`

```
Problem: Use SU(3) Young-tableau rules to decompose 8 x 3 and check dimensions.
Steps:
  SU3_SETUP|left=8|right=3
  TABLEAU_RULE|8 x 3|attach one box to the adjoint tableau|15 + 6bar + 3
  M|8|3|24
  REP_DIM|15|15
  A|0|15|15
  REP_DIM|6bar|6
  A|15|6|21
  REP_DIM|3|3
  A|21|3|24
  CHECK|dimension balance|24=24|ok
  Z|8 x 3 = 15 + 6bar + 3
Answer: 8 x 3 = 15 + 6bar + 3
```

### Clebsch Gordan — `ClebschGordanGenerator`  ·  graduate · difficulty 5

Exact Clebsch-Gordan table entries for 1/2 x 1/2 and 1 x 1/2.

**Variants:** `clebsch_gordan_coefficient`, `clebsch_gordan_probability`, `clebsch_gordan_state`

```
Problem: For Clebsch-Gordan coupling j1=1, j2=1/2 with phase=-, find the coefficient of ket(-1,+) for total J=3/2, M=3/2.
Steps:
  CG_SETUP|j1=1|j2=1/2|phase=-
  TARGET_STATE|J=3/2|M=3/2
  LADDER_RULE|J_- = J1_- + J2_-|lower from highest weights
  NORMALIZE|1|1
  CG_STATE|J=3/2, M=3/2|-ket(1,+)
  CHECK|normalization|1|ok
  CG_COEFF|ket(-1,+)|0
  Z|coefficient of ket(-1,+) = 0
Answer: coefficient of ket(-1,+) = 0
```

### Einstein Summation — `EinsteinSummationGenerator`  ·  graduate · difficulty 3

Numeric Einstein-summation bookkeeping for contractions and symmetrizing.

**Variants:** `einstein_summation_contraction`, `einstein_summation_symmetrize`, `einstein_summation_trace`

```
Problem: Given T_ij=[[6, 0, -6], [-2, 2, 1], [0, 6, -2]], compute the contraction T_ii.
Steps:
  EINSTEIN_SETUP|trace|T_ij=[[6, 0, -6], [-2, 2, 1], [0, 6, -2]]
  TRACE_ENTRY|T_11|6
  TRACE_ENTRY|T_22|2
  TRACE_ENTRY|T_33|-2
  A|6|2|8
  A|8|-2|6
  Z|T_ii = 6
Answer: T_ii = 6
```

### Index Raising — `IndexRaisingGenerator`  ·  graduate · difficulty 3

Raise and lower vector/covector components with diagonal metrics.

**Variants:** `index_raising_lower`, `index_raising_raise`

```
Problem: Raise w_i=[-2,2,1,0] using the diagonal Minkowski inverse metric g^ii=[-1,1,1,1].
Steps:
  INDEX_METRIC|raise|Minkowski|g^ii=[-1,1,1,1]
  M|-1|-2|2
  TENSOR_ENTRY|w^1|2
  M|1|2|2
  TENSOR_ENTRY|w^2|2
  M|1|1|1
  TENSOR_ENTRY|w^3|1
  M|1|0|0
  TENSOR_ENTRY|w^4|0
  Z|w^i = [2,2,1,0]
Answer: w^i = [2,2,1,0]
```

### Riemann Tensor — `RiemannTensorGenerator`  ·  graduate · difficulty 5

Riemann -> Ricci -> scalar curvature for a 2-sphere.

**Variants:** `riemann_tensor_sphere`

```
Problem: For a 2-sphere of radius R=100 at phi=90 deg with sin^2(phi)=1 and cos^2(phi)=0, compute R^phi_theta phi theta, the Ricci entries, and scalar curvature.
Steps:
  RIEMANN_SETUP|sphere|R=100|phi=90 deg
  CHRISTOFFEL_VALUE|Gamma^phi_thetatheta|0
  CHRISTOFFEL_VALUE|Gamma^theta_phitheta|0
  DERIV|d_phi Gamma^phi_thetatheta|1
  M|0|0|0
  S|1|0|1
  RIEMANN_ENTRY|R^phi_theta phi theta|1
  RIEMANN_ENTRY|R^theta_phi theta phi|1
  RICCI_ENTRY|R_phiphi|1
  RICCI_ENTRY|R_thetatheta|1
  E|100|2|10000
  D|1|10000|1/10000
  INVERSE_METRIC|g^phiphi=1/R^2|g^thetatheta=1/(R^2 sin^2(phi))
  CHECK|g^thetatheta R_thetatheta|1/10000|sin^2 cancels
  A|1/10000|1/10000|1/5000
  Z|scalar curvature = 1/5000
Answer: scalar curvature = 1/5000
```

### Four Vector — `FourVectorGenerator`  ·  graduate · difficulty 3

Four-vector arithmetic with signature (+,-,-,-).

**Variants:** `four_vector_dot_product`, `four_vector_mass_shell`

```
Problem: In units c=1, solve E^2 = p^2 + m^2 for momentum p=12 and mass m=35.
Steps:
  FOUR_VECTOR_SETUP|mass_shell|c=1|p=12, m=35
  E|12|2|144
  E|35|2|1225
  A|144|1225|1369
  ROOT|sqrt(1369)|37
  Z|E = 37
Answer: E = 37
```

### Schwarzschild — `SchwarzschildGenerator`  ·  graduate · difficulty 4

Schwarzschild radius and time-dilation plug-ins with supplied constants.

**Variants:** `schwarzschild_radius`, `schwarzschild_time_dilation`

```
Problem: Given Schwarzschild radius r_s=18 and radius r=50, compute the time dilation factor sqrt(1 - r_s/r).
Steps:
  SCHWARZSCHILD_SETUP|time_dilation|r_s=18|r=50
  D|18|50|9/25
  S|1|9/25|16/25
  ROOT|sqrt(16/25)|4/5
  Z|time dilation factor = 4/5
Answer: time dilation factor = 4/5
```

### Planck Units — `PlanckUnitsGenerator`  ·  graduate · difficulty 4

Planck length, time, and mass from supplied hbar, G, and c.

**Variants:** `planck_units_length`, `planck_units_mass`, `planck_units_time`

```
Problem: Given hbar=49, G=1, and c=9, compute the Planck time sqrt(hbar*G/c^5).
Steps:
  PLANCK_SETUP|time|hbar=49|G=1|c=9
  M|49|1|49
  E|9|5|59049
  D|49|59049|49/59049
  ROOT|sqrt(49/59049)|7/243
  Z|t_P = 7/243
Answer: t_P = 7/243
```

### Hawking — `HawkingGenerator`  ·  graduate · difficulty 4

Hawking temperature and Bekenstein-Hawking entropy evaluations.

**Variants:** `hawking_entropy`, `hawking_temperature`

```
Problem: Given k_B=7, c=1, A=37, hbar=9, and G=8, compute the Bekenstein-Hawking entropy S_BH=k_B*c^3*A/(4*hbar*G).
Steps:
  HAWKING_SETUP|entropy|S_BH=k_B*c^3*A/(4*hbar*G)|k_B=7,c=1,A=37,hbar=9,G=8
  E|1|3|1
  M|7|1|7
  M|7|37|259
  M|4|9|36
  M|36|8|288
  D|259|288|259/288
  Z|S_BH = 259/288
Answer: S_BH = 259/288
```

### Casimir Force — `CasimirForceGenerator`  ·  graduate · difficulty 3

Casimir force per area between parallel conducting plates.

**Variants:** `casimir_force_pressure`

```
Problem: Given hbar=13, c=14, and plate separation d=1, compute the Casimir force per area F/A=-π^2*hbar*c/(240*d^4).
Steps:
  CASIMIR_FORCE_SETUP|F/A=-π^2*hbar*c/(240*d^4)|hbar=13,c=14,d=1
  E|1|4|1
  M|240|1|240
  M|13|14|182
  D|182|240|91/120
  S|0|91/120|-91/120
  PI2_NUM|-91/120|π^2|-91π^2/120
  Z|F/A = -91π^2/120
Answer: F/A = -91π^2/120
```

### Natural Units — `NaturalUnitsGenerator`  ·  graduate · difficulty 4

Natural-unit conversion chains with hbar = c = 1.

**Variants:** `natural_units_energy`, `natural_units_length`, `natural_units_mass`, `natural_units_time`

```
Problem: In natural units with hbar=c=1, a time scale t=25/29 GeV^-1 is given. Compute length L=t, energy E=1/t, and mass m=E.
Steps:
  NATURAL_SETUP|time|hbar=1,c=1|t=25/29 GeV^-1
  UNIT_RULE|c=1|L=t|GeV^-1
  M|25/29|1|25/29
  UNIT_RULE|hbar=1|E=1/L|GeV
  D|1|25/29|29/25
  UNIT_RULE|c=1|m=E|mass uses GeV
  M|29/25|1|29/25
  M|29/25|25/29|1
  Z|L = 25/29 GeV^-1, E = 29/25 GeV, m = 29/25 GeV
Answer: L = 25/29 GeV^-1, E = 29/25 GeV, m = 29/25 GeV
```

### Invariant Mass — `InvariantMassGenerator`  ·  graduate · difficulty 4

Relativistic kinematics with exact invariant quantities.

**Variants:** `invariant_mass_cm_energy`, `invariant_mass_invariant_mass`, `invariant_mass_threshold`, `invariant_mass_two_body_momentum`

```
Problem: A parent of mass M=34 decays into two equal daughters m1=m2=8. Compute the two-body momentum p=sqrt((M^2-(m1+m2)^2)*(M^2-(m1-m2)^2))/(2*M).
Steps:
  KIN_SETUP|two_body_momentum|M=34|m1=8,m2=8|p
  KIN_FORMULA|p=sqrt((M^2-(m1+m2)^2)*(M^2-(m1-m2)^2))/(2*M)
  A|8|8|16
  S|8|8|0
  E|34|2|1156
  E|16|2|256
  E|0|2|0
  S|1156|256|900
  S|1156|0|1156
  M|900|1156|1040400
  ROOT|sqrt(1040400)|1020
  M|2|34|68
  D|1020|68|15
  Z|p = 15
Answer: p = 15
```

### Branching Ratio — `BranchingRatioGenerator`  ·  graduate · difficulty 3

Particle partial widths, branching ratios, and lifetimes.

**Variants:** `branching_ratio_branching_ratio`, `branching_ratio_combined`, `branching_ratio_lifetime`

```
Problem: Given hbar=14 and total width Gamma=2, compute the lifetime tau=hbar/Gamma.
Steps:
  WIDTH_SETUP|lifetime|hbar=14|Gamma=2
  D|14|2|7
  Z|tau = 7
Answer: tau = 7
```

### Cross Section — `CrossSectionGenerator`  ·  graduate · difficulty 3

Collider luminosity and cross-section arithmetic.

**Variants:** `cross_section_cross_section`, `cross_section_events_fb`, `cross_section_events_pb`, `cross_section_luminosity`

```
Problem: Given target N=216 events and cross section sigma=3 fb, compute required integrated luminosity L=N/sigma in fb^-1.
Steps:
  COLLIDER_SETUP|luminosity|N=216 events|sigma=3 fb
  D|216|3|72
  UNIT_ATTACH|72|fb^-1|L = 72 fb^-1
  Z|L = 72 fb^-1
Answer: L = 72 fb^-1
```

### Gamma Matrix — `GammaMatrixGenerator`  ·  graduate · difficulty 5

Small Dirac gamma-matrix algebra checks by explicit 4x4 multiplication.

**Variants:** `gamma_matrix_anticommutator_entry`, `gamma_matrix_trace`

```
Problem: Given gamma3=[[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]] and gamma1=[[0,-1,0,0],[1,0,0,0],[0,0,0,1],[0,0,-1,0]] with eta_31=0, compute Tr(gamma3*gamma1).
Steps:
  GAMMA_SETUP|trace|gamma3,gamma1|Tr(product)
  MATRIX_PRODUCT|gamma3gamma1|gamma3*gamma1
  DOT4|gamma3gamma1|(1,1)|0*0 + 0*1 + -1*0 + 0*0|0
  TRACE_ADD|gamma3gamma1|(1,1)|0 + 0|0
  DOT4|gamma3gamma1|(2,2)|0*-1 + 0*0 + 0*0 + -1*0|0
  TRACE_ADD|gamma3gamma1|(2,2)|0 + 0|0
  DOT4|gamma3gamma1|(3,3)|1*0 + 0*0 + 0*0 + 0*-1|0
  TRACE_ADD|gamma3gamma1|(3,3)|0 + 0|0
  DOT4|gamma3gamma1|(4,4)|0*0 + 1*0 + 0*1 + 0*0|0
  TRACE_ADD|gamma3gamma1|(4,4)|0 + 0|0
  TRACE_EXPECT|4*eta_31|0|0
  CHECK|trace theorem|computed=0|expected=0
  Z|Tr(gamma3*gamma1) = 0
Answer: Tr(gamma3*gamma1) = 0
```

### Grassmann — `GrassmannGenerator`  ·  graduate · difficulty 4

One-generator Grassmann arithmetic with theta^2 = 0.

**Variants:** `grassmann_exponential`, `grassmann_integrate`, `grassmann_multiply`, `grassmann_multiply_integrate`

```
Problem: Let theta^2=0 with Berezin rules int dtheta 1=0 and int dtheta theta=1. Compute int dtheta [(x)*(y)] for x=5 - 8theta and y=-1 + 8theta.
Steps:
  GRASSMANN_SETUP|multiply_integrate|x=5 - 8theta|y=-1 + 8theta
  M|5|-1|-5
  M|5|8|40
  M|-8|-1|8
  M|-8|8|-64
  NILPOTENT|theta^2=0|-64theta^2|0
  A|40|8|48
  GRASSMANN_RESULT|constant=-5|theta=48|-5 + 48theta
  BEREZIN_RULE|int dtheta 1|0
  BEREZIN_RULE|int dtheta theta|1
  M|-5|0|0
  M|48|1|48
  A|0|48|48
  Z|integral = 48
Answer: integral = 48
```

### Running Coupling — `RunningCouplingGenerator`  ·  graduate · difficulty 4

One-loop running coupling in reciprocal form.

**Variants:** `running_coupling_evolve`

```
Problem: At one loop, use 1/alpha(mu)=1/alpha0+beta*L with L=ln(mu/mu0) supplied. Given alpha0=2/29, beta=7, and L=1, compute alpha(mu).
Steps:
  RG_SETUP|one_loop|alpha0=2/29|beta=7,L=1
  D|1|2/29|29/2
  M|7|1|7
  A|29/2|7|43/2
  D|1|43/2|2/43
  M|2/43|43/2|1
  CHECK|reciprocal|alpha_mu*inv_alpha_mu|1
  Z|alpha(mu) = 2/43
Answer: alpha(mu) = 2/43
```

### MGF — `MGFGenerator`  ·  graduate · difficulty 4

Derive a discrete moment generating function and differentiate for moments.

**Variants:** `mgf_discrete_three_point`

```
Problem: A discrete random variable has P(X=0)=25/32, P(X=1)=1/8, and P(X=2)=3/32. Derive M(t), then use M'(0) and M''(0) to find E[X], E[X^2], and Var(X).
Steps:
  MGF_SETUP|P(X=0)=25/32|P(X=1)=1/8|P(X=2)=3/32
  MGF_TERM|x=0|p0*e^(0t)|25/32
  MGF_TERM|x=1|p1*e^t|1/8*e^t
  MGF_TERM|x=2|p2*e^(2t)|3/32*e^(2t)
  REWRITE|M(t)=25/32 + 1/8*e^t + 3/32*e^(2t)
  DERIVATIVE|M'(t)=1/8*e^t + 3/16*e^(2t)
  DERIVATIVE|M''(t)=1/8*e^t + 3/8*e^(2t)
  EVAL_AT_ZERO|e^0=1|e^(2*0)=1
  M|2|3/32|3/16
  A|1/8|3/16|5/16
  E|2|2|4
  M|4|3/32|3/8
  A|1/8|3/8|1/2
  M|5/16|5/16|25/256
  S|1/2|25/256|103/256
  Z|M(t)=25/32 + 1/8*e^t + 3/32*e^(2t); E[X]=5/16; E[X^2]=1/2; Var(X)=103/256
Answer: M(t)=25/32 + 1/8*e^t + 3/32*e^(2t); E[X]=5/16; E[X^2]=1/2; Var(X)=103/256
```

### RVTransform — `RVTransformGenerator`  ·  graduate · difficulty 5

Transform random variables with CDF and Jacobian methods.

**Variants:** `rv_transform_cdf_square`, `rv_transform_jacobian_sum_difference`

```
Problem: Let X,Y be independent Uniform(0,15). Define U=X+Y and V=X-Y. Use the Jacobian method to find the inverse map, transformed support, density f_UV(u,v), and f_UV at the point produced by x=1, y=8.
Steps:
  TRANSFORM_SETUP|jacobian|X,Y~Uniform(0,15)|U=X+Y,V=X-Y
  DENSITY|f_XY(x,y)|1/15^2
  E|15|2|225
  D|1|225|1/225
  INVERSE_MAP|x=(u+v)/2|y=(u-v)/2
  D|1|2|1/2
  JAC_MATRIX|dx/du=1/2, dx/dv=1/2|dy/du=1/2, dy/dv=-1/2
  M|1/2|-1/2|-1/4
  M|1/2|1/2|1/4
  S|-1/4|1/4|-1/2
  ABS|-1/2|1/2
  M|1/225|1/2|1/450
  M|2|15|30
  SUPPORT|0<=u+v<=30|0<=u-v<=30
  A|1|8|9
  S|1|8|-7
  A|9|-7|2
  S|9|-7|16
  CHECK|u+v=2|u-v=16|in support
  Z|inverse x=(u+v)/2, y=(u-v)/2; support=0<=u+v<=30 and 0<=u-v<=30; absJ=1/2; f_UV(u,v)=1/450; f_UV(9,-7)=1/450
Answer: inverse x=(u+v)/2, y=(u-v)/2; support=0<=u+v<=30 and 0<=u-v<=30; absJ=1/2; f_UV(u,v)=1/450; f_UV(9,-7)=1/450
```

### MLE — `MLEGenerator`  ·  graduate · difficulty 4

Maximum-likelihood estimates from log-likelihood score equations.

**Variants:** `mle_bernoulli`, `mle_exponential`, `mle_normal_mu`

```
Problem: For exponential data [7,1,5,9,8,7,5,8,6], write the log-likelihood for lambda, differentiate, and solve for the MLE lambda_hat.
Steps:
  MLE_SETUP|exponential|parameter=lambda|data=[7,1,5,9,8,7,5,8,6]
  COUNT|n|9
  SUM|sum x_i|7 + 1 + 5 + 9 + 8 + 7 + 5 + 8 + 6|56
  LOG_LIKELIHOOD|ell(lambda)=9*log(lambda)-56*lambda
  DERIVATIVE|score=9/lambda-56
  SCORE_EQ|9/lambda=56
  D|9|56|9/56
  CHECK|lambda_hat=9/56>0|valid rate parameter
  Z|ell(lambda)=9*log(lambda)-56*lambda; score=9/lambda-56; lambda_hat=9/56
Answer: ell(lambda)=9*log(lambda)-56*lambda; score=9/lambda-56; lambda_hat=9/56
```

### Method Of Moments — `MethodOfMomentsGenerator`  ·  graduate · difficulty 3

First-moment method-of-moments estimators.

**Variants:** `method_of_moments_exponential`, `method_of_moments_poisson`, `method_of_moments_uniform_zero_theta`

```
Problem: For data [1,5,9,8,7,5,8,6,10] from an Exponential(lambda) model, use E[X]=1/lambda to find the method-of-moments estimator lambda_hat.
Steps:
  MOM_SETUP|exponential|parameter=lambda|data=[1,5,9,8,7,5,8,6,10]
  COUNT|n|9
  SUM|sum x_i|1 + 5 + 9 + 8 + 7 + 5 + 8 + 6 + 10|59
  D|59|9|59/9
  SAMPLE_MOMENT|xbar|59/9
  MOM_EQUATION|E[X]=1/lambda|xbar=1/lambda
  REWRITE|lambda_hat=1/xbar
  D|9|59|9/59
  CHECK|lambda_hat=9/59>0|valid rate parameter
  Z|xbar=59/9; lambda_hat=9/59
Answer: xbar=59/9; lambda_hat=9/59
```

### Bayesian Update — `BayesianUpdateGenerator`  ·  graduate · difficulty 4

Mechanical conjugate Bayesian parameter updates.

**Variants:** `bayesian_update_beta_binomial`, `bayesian_update_normal_normal`

```
Problem: For data [-7,0,8,7,4,1] from Normal(mu, sigma^2=9) with prior mu~Normal(-1, tau^2=4), compute the conjugate posterior mean and variance.
Steps:
  BAYES_UPDATE_SETUP|normal_normal|prior=Normal(-1,4)|sigma^2=9
  BAYES_UPDATE_SETUP|data|[-7,0,8,7,4,1]
  COUNT|n|6
  SUM|sum x_i|-7 + 0 + 8 + 7 + 4 + 1|13
  PRIOR_PRECISION|1/tau^2
  D|1|4|1/4
  DATA_PRECISION|n/sigma^2
  D|6|9|2/3
  POST_PRECISION|prior precision + data precision
  A|1/4|2/3|11/12
  D|-1|4|-1/4
  D|13|9|13/9
  A|-1/4|13/9|43/36
  D|43/36|11/12|43/33
  D|1|11/12|12/11
  Z|posterior=Normal(mean=43/33, variance=12/11)
Answer: posterior=Normal(mean=43/33, variance=12/11)
```

### Order Statistics — `OrderStatisticsGenerator`  ·  graduate · difficulty 4

Uniform(0,1) order statistic pdf, moments, and exact pdf evaluation.

**Variants:** `order_statistics_uniform_pdf_moments`

```
Problem: For 8 iid Uniform(0,1) samples, find the pdf, mean, variance, and f(2/3) for the 7-th order statistic X_(7).
Steps:
  ORDER_SETUP|n=8|k=7|q=2/3
  FACT|8|40320
  S|7|1|6
  S|8|7|1
  FACT|6|720
  FACT|1|1
  M|720|1|720
  D|40320|720|56
  ORDER_PDF|f_{7:8}(x)=56*x^6*(1-x)^1
  S|1|2/3|1/3
  E|2/3|6|64/729
  E|1/3|1|1/3
  M|56|64/729|3584/729
  M|3584/729|1/3|3584/2187
  A|8|1|9
  D|7|9|7/9
  S|9|7|2
  M|7|2|14
  E|9|2|81
  A|9|1|10
  M|81|10|810
  D|14|810|7/405
  Z|f_{7:8}(x)=56*x^6*(1-x)^1; E[X_(7)]=7/9; Var(X_(7))=7/405; f_{7:8}(2/3)=3584/2187
Answer: f_{7:8}(x)=56*x^6*(1-x)^1; E[X_(7)]=7/9; Var(X_(7))=7/405; f_{7:8}(2/3)=3584/2187
```

### Transportation — `TransportationGenerator`  ·  graduate · difficulty 4

Northwest-corner transportation start and one stepping-stone improvement.

**Variants:** `transportation_nw_stepping_stone`

```
Problem: Use northwest-corner then one stepping-stone improvement for a 2x2 transportation problem with supply (14,8), demand (9,13), and costs [[15,3],[6,10]].
Steps:
  TRANSPORT_SETUP|supply=(14,8)|demand=(9,13)|costs=(15,3;6,10)
  CHECK|14+8|9+13|balanced
  NW_ALLOC|cell x11|min(14,9)|9
  S|14|9|5
  NW_ALLOC|cell x12|remaining row 1 supply|5
  NW_ALLOC|cell x22|remaining row 2 supply|8
  NW_ALLOC|x11=9, x12=5, x21=0, x22=8
  COST|initial
  M|9|15|135
  M|5|3|15
  M|0|6|0
  M|8|10|80
  A|135|15|150
  A|150|0|150
  A|150|80|230
  STEPPING_STONE|enter x21|+x21 -x22 +x12 -x11
  S|6|10|-4
  A|-4|3|-1
  S|-1|15|-16
  CHECK|delta=-16|improves cost
  THETA|min(8,9)|8
  A|0|8|8
  S|8|8|0
  A|5|8|13
  S|9|8|1
  NW_ALLOC|x11=1, x12=13, x21=8, x22=0
  COST|improved
  M|1|15|15
  M|13|3|39
  M|8|6|48
  M|0|10|0
  A|15|39|54
  A|54|48|102
  A|102|0|102
  Z|initial cost=230; improved x11=1, x12=13, x21=8, x22=0; final cost=102
Answer: initial cost=230; improved x11=1, x12=13, x21=8, x22=0; final cost=102
```

### ORFormula — `ORFormulaGenerator`  ·  graduate · difficulty 3

Operations-research formula chains for EOQ and M/M/1 queues.

**Variants:** `or_formula_eoq`, `or_formula_mm1`

```
Problem: For an M/M/1 queue with arrival rate lambda=14 and service rate mu=16, compute rho, L, W, Lq, and Wq.
Steps:
  OR_SETUP|M/M/1|lambda=14|mu=16
  CHECK|lambda=14 < mu=16|stable
  S|16|14|2
  FORMULA|rho=lambda/mu
  D|14|16|7/8
  FORMULA|L=lambda/(mu-lambda)
  D|14|2|7
  FORMULA|W=1/(mu-lambda)
  D|1|2|1/2
  FORMULA|Lq=lambda^2/(mu*(mu-lambda))
  E|14|2|196
  M|16|2|32
  D|196|32|49/8
  FORMULA|Wq=lambda/(mu*(mu-lambda))
  D|14|32|7/16
  Z|rho=7/8; L=7; W=1/2; Lq=49/8; Wq=7/16
Answer: rho=7/8; L=7; W=1/2; Lq=49/8; Wq=7/16
```

### ZTransform — `ZTransformGenerator`  ·  graduate · difficulty 4

Basic z-transform pairs and first-order difference equations.

**Variants:** `z_transform_difference`, `z_transform_geometric`

```
Problem: Solve y[n]-7y[n-1]=delta[n] with y[-1]=0 using z-transforms, and list y[0] through y[4].
Steps:
  ZT_SETUP|difference|y[n]-7y[n-1]=delta[n]|y[-1]=0
  SHIFT|Z{y[n-1]}=z^-1Y(z)
  REWRITE|(1-7z^-1)Y(z)=1
  REWRITE|Y(z)=1/(1-7z^-1)
  E|7|0|1
  E|7|1|7
  E|7|2|49
  E|7|3|343
  E|7|4|2401
  TERMS|y[0..4]=[1,7,49,343,2401]
  Z|Y(z)=1/(1-7z^-1); y[0..4]=[1,7,49,343,2401]
Answer: Y(z)=1/(1-7z^-1); y[0..4]=[1,7,49,343,2401]
```

### Transfer Function — `TransferFunctionGenerator`  ·  graduate · difficulty 4

Transfer functions from ODEs and simple feedback block diagrams.

**Variants:** `transfer_function_block_feedback`, `transfer_function_ode`

```
Problem: Reduce a unity negative-feedback block diagram with G1=7/(s+5) and G2=1/(s+9).
Steps:
  TF_SETUP|block_feedback|G1=7/(s+5), G2=1/(s+9)|H=1
  SERIES|G=G1*G2
  M|7|1|7
  A|5|9|14
  M|5|9|45
  TRANSFER|G(s)=7/(s^2+14s+45)
  FEEDBACK|T=G/(1+G)
  A|45|7|52
  TRANSFER|T(s)=7/(s^2+14s+52)
  Z|T(s)=7/(s^2+14s+52)
Answer: T(s)=7/(s^2+14s+52)
```

### Routh Hurwitz — `RouthHurwitzGenerator`  ·  graduate · difficulty 4

Cubic Routh-Hurwitz stability array.

**Variants:** `routh_hurwitz_cubic`

```
Problem: Build the Routh-Hurwitz array for p(s)=s^3+25s^2+27s+6 and determine stability.
Steps:
  ROUTH_SETUP|p(s)=s^3+25s^2+27s+6
  ROUTH_ROW|s^3|1, 27
  ROUTH_ROW|s^2|25, 6
  M|25|27|675
  S|675|6|669
  D|669|25|669/25
  ROUTH_ROW|s^1|669/25, 0
  ROUTH_ROW|s^0|6
  CHECK|first column=[1,25,669/25,6]|stable
  Z|first column=[1,25,669/25,6]; stable
Answer: first column=[1,25,669/25,6]; stable
```

### Lagrangian — `LagrangianGenerator`  ·  graduate · difficulty 4

Build L = T - V and apply the Euler-Lagrange equation.

**Variants:** `lagrangian_atwood`, `lagrangian_mass_spring`, `lagrangian_pendulum`

```
Problem: For a simple pendulum with mass m=7, length L=1, and g=10, write L=T-V and apply the Euler-Lagrange equation to find thetaddot.
Steps:
  LAG_SETUP|pendulum|m=7, L=1|g=10, q=theta
  ENERGY_TERM|T=1/2*m*L^2*thetadot^2
  E|1|2|1
  M|7|1|7
  ENERGY_TERM|V=m*g*L*(1-cos(theta))
  M|7|10|70
  M|70|1|70
  LAGRANGIAN|L=T-V
  PARTIAL|dL/dthetadot|m*L^2*thetadot
  TIME_DERIV|d/dt(m*L^2*thetadot)|m*L^2*thetaddot
  PARTIAL|dL/dtheta|-m*g*L*sin(theta)
  EL_EQUATION|mL^2*thetaddot+mgL*sin(theta)=0
  D|70|7|10
  EL_SOLVE|thetaddot|-10*sin(theta)
  Z|thetaddot=-10*sin(theta)
Answer: thetaddot=-10*sin(theta)
```

### Hamiltonian — `HamiltonianGenerator`  ·  graduate · difficulty 4

Hamilton's equations for mass-spring, pendulum, and Atwood systems.

**Variants:** `hamiltonian_atwood`, `hamiltonian_mass_spring`, `hamiltonian_pendulum`

```
Problem: For a pendulum Hamiltonian with mass m=7, length L=1, and g=10, write H and Hamilton's equations.
Steps:
  HAM_SETUP|pendulum|m=7, L=1|g=10, q=theta
  E|1|2|1
  M|7|1|7
  M|7|10|70
  M|70|1|70
  HAMILTONIAN|H=p_theta^2/(2mL^2)+mgL*(1-cos(theta))
  PARTIAL|dH/dp_theta|p_theta/(mL^2)
  HAM_EQ|thetadot=dH/dp_theta|thetadot=p_theta/7
  PARTIAL|dH/dtheta|mgL*sin(theta)
  HAM_EQ|p_thetadot=-dH/dtheta|p_thetadot=-70*sin(theta)
  D|70|7|10
  HAM_EQ|thetaddot=p_thetadot/(mL^2)|thetaddot=-10*sin(theta)
  Z|thetadot=p_theta/7; p_thetadot=-70*sin(theta); thetaddot=-10*sin(theta)
Answer: thetadot=p_theta/7; p_thetadot=-70*sin(theta); thetaddot=-10*sin(theta)
```

### ACCircuit — `ACCircuitGenerator`  ·  graduate · difficulty 4

AC circuit impedance, phasor current, and resonance.

**Variants:** `ac_circuit_resonance`, `ac_circuit_series_rlc`

```
Problem: A series RLC circuit has R=27 ohm, L=5 H, and C=1/5 F. Find the resonant angular frequency and impedance at resonance.
Steps:
  AC_SETUP|resonance|R=27, L=5|C=1/5
  AC_FORMULA|omega0^2=1/(L*C)
  M|5|1/5|1
  D|1|1|1
  ROOT|1|1
  AC_FORMULA|at resonance XL=XC so Z=R
  AC_COMPLEX|Z|27|0j
  Z|omega0=1 rad/s; Z=27 ohm
Answer: omega0=1 rad/s; Z=27 ohm
```

### Partition Function — `PartitionFunctionGenerator`  ·  graduate · difficulty 4

Two-level partition functions with supplied Boltzmann factors.

**Variants:** `partition_function_degenerate_two_level`, `partition_function_two_level`

```
Problem: A two-level system has ground degeneracy g0=4, excited degeneracy g1=1, excited energy epsilon=9, and Boltzmann factor b=1/10 for the excited level. Compute Z, excited occupancy, and mean energy.
Steps:
  PARTITION_SETUP|degenerate_two_level|g0=4, g1=1|epsilon=9, b=1/10
  PARTITION_FORMULA|Z=g0+g1*b
  M|1|1/10|1/10
  A|4|1/10|41/10
  D|4|41/10|40/41
  D|1/10|41/10|1/41
  PARTITION_FORMULA|mean_energy=epsilon*p_excited
  M|9|1/41|9/41
  Z|Z=41/10; p_excited=1/41; mean_energy=9/41
Answer: Z=41/10; p_excited=1/41; mean_energy=9/41
```

### Wavefunction — `WavefunctionGenerator`  ·  graduate · difficulty 4

Normalize simple wavefunctions and compute expectation values by integration.

**Variants:** `wavefunction_power_interval`

```
Problem: On 0<=x<=49, let psi(x)=N*(x/L)^6. Normalize it and compute <x> and <x^2>.
Steps:
  WAVE_SETUP|power_interval|psi=N*(x/L)^6|0<=x<=49
  WAVE_FORMULA|1=N^2*integral_0^L (x/L)^(2k) dx
  M|2|6|12
  A|12|1|13
  POWER_INTEGRAL|n=12|L/13
  D|13|49|13/49
  WAVE_FORMULA|N^2=13/49
  WAVE_FORMULA|<x>=N^2*integral_0^L x*(x/L)^(2k) dx
  A|12|2|14
  POWER_INTEGRAL|n=13|L^2/14
  M|13|49|637
  D|637|14|91/2
  WAVE_FORMULA|<x^2>=N^2*integral_0^L x^2*(x/L)^(2k) dx
  A|12|3|15
  POWER_INTEGRAL|n=14|L^3/15
  E|49|2|2401
  M|13|2401|31213
  D|31213|15|31213/15
  Z|N=sqrt(13/49); <x>=91/2; <x^2>=31213/15
Answer: N=sqrt(13/49); <x>=91/2; <x^2>=31213/15
```

### Spin Half — `SpinHalfGenerator`  ·  graduate · difficulty 4

Spin-1/2 calculations with Pauli matrices and exact probabilities.

**Variants:** `spin_half_apply_pauli`, `spin_half_eigenvalue`, `spin_half_measurement_probability`

```
Problem: Show that psi=(ket0 - ket1)/sqrt(2) is an eigenstate of sigma_x and find the eigenvalue.
Steps:
  SPIN_SETUP|eigenvalue|operator=sigma_x|psi=(ket0 - ket1)/sqrt(2)
  PAULI_MATRIX|sigma_x|[[0,1],[1,0]]
  APPLY_PAULI|sigma_x ket0|ket1
  APPLY_PAULI|sigma_x -ket1|-ket0
  REWRITE|sigma_x psi=(ket1 - ket0)/sqrt(2)
  REWRITE|sigma_x psi=-(ket0 - ket1)/sqrt(2)
  EIGEN_CHECK|sigma_x psi|-1*psi|lambda=-1
  Z|sigma_x psi=-1*psi; lambda=-1
Answer: sigma_x psi=-1*psi; lambda=-1
```

### Commutator — `CommutatorGenerator`  ·  graduate · difficulty 4

Operator commutators applied to monomial test functions.

**Variants:** `commutator_d_x`, `commutator_d_x_squared`, `commutator_x_p`

```
Problem: For test function f(x)=x^14, compute [D,x^2]f where D=d/dx.
Steps:
  COMM_SETUP|[D,x^2]f|f=x^14|D=d/dx
  COMM_FORMULA|[A,B]f=A(Bf)-B(Af)
  APPLY_OPERATOR|x^2 f|x^16
  A|14|2|16
  POWER_RULE|x^16|16*x^15
  POWER_RULE|x^14|14*x^13
  APPLY_OPERATOR|x^2 Df|14*x^15
  S|16|14|2
  COMM_RESULT|[D,x^2]f|2*x^15
  CHECK|identity|[D,x^2]=2x|matches 2x f
  Z|[D,x^2]f=2*x^15
Answer: [D,x^2]f=2*x^15
```

### Ladder Operator — `LadderOperatorGenerator`  ·  graduate · difficulty 5

Harmonic-oscillator ladder-operator algebra and energy levels.

**Variants:** `ladder_operator_commutator_energy`, `ladder_operator_number_energy`, `ladder_operator_single_step_energy`

```
Problem: For harmonic oscillator state ket25 with hbar=7 and omega=1, compute N=adag*a and E_25.
Steps:
  LADDER_SETUP|number_energy|state=ket25|hbar=7, omega=1
  LADDER_RULE|a ketn=sqrt(n) ket(n-1)|adag ketn=sqrt(n+1) ket(n+1)
  LADDER_APPLY|a ket25|sqrt(25) ket24
  LADDER_APPLY|adag sqrt(25) ket24|sqrt(25)*sqrt(25) ket25
  M|25|25|625
  ROOT|625|25
  NUMBER_OPERATOR|N ket25|25 ket25
  M|2|25|50
  A|50|1|51
  M|7|1|7
  M|7|51|357
  D|357|2|357/2
  ENERGY_LEVEL|E_25=hbar*omega*(n+1/2)|357/2
  Z|N ket25=25 ket25; E_25=357/2
Answer: N ket25=25 ket25; E_25=357/2
```

### Bra Ket — `BraKetGenerator`  ·  graduate · difficulty 4

Finite-dimensional bra-ket arithmetic with exact complex components.

**Variants:** `braket_inner_product`, `braket_time_evolution`

```
Problem: A diagonal Hamiltonian gives time-evolution phases [-i,-i,i] in its eigenbasis. For ket psi=[0,-2,1-i], compute U psi.
Steps:
  BRAKET_SETUP|time_evolution|psi=[0,-2,1-i]|phases=[-i,-i,i]
  BRAKET_FORMULA|U=diag(phases)
  CX_M|-i|0|0
  TIME_COMPONENT|k=1|0
  CX_M|-i|-2|2i
  TIME_COMPONENT|k=2|2i
  CX_M|i|1-i|1+i
  TIME_COMPONENT|k=3|1+i
  TIME_EVOLVE|U psi|[0,2i,1+i]
  Z|U psi=[0,2i,1+i]
Answer: U psi=[0,2i,1+i]
```

### Minkowski Interval — `MinkowskiIntervalGenerator`  ·  graduate · difficulty 4

Minkowski interval classification and rapidity addition.

**Variants:** `minkowski_interval_interval_classification`, `minkowski_interval_rapidity_addition`

```
Problem: Two collinear boosts have rapidities eta1=1/2 and eta2=-5/3. Compute the total rapidity.
Steps:
  MINKOWSKI_SETUP|rapidity_addition|eta1=1/2|eta2=-5/3
  MINKOWSKI_FORMULA|eta_total=eta1+eta2
  A|1/2|-5/3|-7/6
  RAPIDITY_SUM|collinear boosts|-7/6
  Z|eta_total=-7/6
Answer: eta_total=-7/6
```

### KLDivergence — `KLDivergenceGenerator`  ·  graduate · difficulty 4

KL divergence for small distributions with exact power-of-two ratios.

**Variants:** `kl_divergence_binary_forward`, `kl_divergence_binary_reverse`, `kl_divergence_ternary_forward`, `kl_divergence_ternary_reverse`

```
Problem: For distributions P=[64/255,1/2,127/510] and Q=[1/510,1/2,127/255], compute D_KL(Q to P) in bits.
Steps:
  KL_SETUP|P=[64/255,1/2,127/510]|Q=[1/510,1/2,127/255]|direction=Q to P
  KL_FORMULA|D=sum source_i*log2(source_i/target_i)
  D|1/510|64/255|1/128
  LOG2_RATIO|i=0|ratio=1/128|log=-7
  M|1/510|-7|-7/510
  A|0|-7/510|-7/510
  D|1/2|1/2|1
  LOG2_RATIO|i=1|ratio=1|log=0
  M|1/2|0|0
  A|-7/510|0|-7/510
  D|127/255|127/510|2
  LOG2_RATIO|i=2|ratio=2|log=1
  M|127/255|1|127/255
  A|-7/510|127/255|247/510
  Z|D_KL(Q to P)=247/510 bits
Answer: D_KL(Q to P)=247/510 bits
```

### Channel Capacity — `ChannelCapacityGenerator`  ·  graduate · difficulty 4

Binary symmetric channel entropy and capacity using supplied log values.

**Variants:** `channel_capacity_binary_entropy`, `channel_capacity_block_bits`, `channel_capacity_capacity`

```
Problem: A binary symmetric channel has crossover probability p=49/100. Use -log2(p)=1.029 and -log2(1-p)=0.971. Find capacity C=1-H_b(p).
Steps:
  BSC_SETUP|p=49/100|-log2(p)=1.029|-log2(1-p)=0.971
  S|1|49/100|51/100
  BSC_FORMULA|H_b=p*(-log2 p)+(1-p)*(-log2(1-p))
  M|49/100|1.029|0.50421
  M|51/100|0.971|0.49521
  A|0.50421|0.49521|0.99942
  BSC_FORMULA|C=1-H_b
  S|1|0.99942|0.00058
  Z|C=0.00058 bits/use
Answer: C=0.00058 bits/use
```

### Arithmetic Coding — `ArithmeticCodingGenerator`  ·  graduate · difficulty 5

Arithmetic coding interval narrowing with exact rational endpoints.

**Variants:** `arithmetic_coding`

```
Problem: Arithmetic-code message ACDDCD using symbol probabilities A=1/8, B=3/8, C=1/4, D=1/4. Find the final interval and midpoint code.
Steps:
  ARITH_SETUP|A=1/8, B=3/8, C=1/4, D=1/4|message=ACDDCD
  CUM_INTERVAL|A|[0,1/8)
  CUM_INTERVAL|B|[1/8,1/2)
  CUM_INTERVAL|C|[1/2,3/4)
  CUM_INTERVAL|D|[3/4,1)
  ARITH_SYMBOL|A|cum=[0,1/8)
  S|1|0|1
  M|1|0|0
  A|0|0|0
  M|1|1/8|1/8
  A|0|1/8|1/8
  ARITH_INTERVAL|[0,1/8)
  ARITH_SYMBOL|C|cum=[1/2,3/4)
  S|1/8|0|1/8
  M|1/8|1/2|1/16
  A|0|1/16|1/16
  M|1/8|3/4|3/32
  A|0|3/32|3/32
  ARITH_INTERVAL|[1/16,3/32)
  ARITH_SYMBOL|D|cum=[3/4,1)
  S|3/32|1/16|1/32
  M|1/32|3/4|3/128
  A|1/16|3/128|11/128
  M|1/32|1|1/32
  A|1/16|1/32|3/32
  ARITH_INTERVAL|[11/128,3/32)
  ARITH_SYMBOL|D|cum=[3/4,1)
  S|3/32|11/128|1/128
  M|1/128|3/4|3/512
  A|11/128|3/512|47/512
  M|1/128|1|1/128
  A|11/128|1/128|3/32
  ARITH_INTERVAL|[47/512,3/32)
  ARITH_SYMBOL|C|cum=[1/2,3/4)
  S|3/32|47/512|1/512
  M|1/512|1/2|1/1024
  A|47/512|1/1024|95/1024
  M|1/512|3/4|3/2048
  A|47/512|3/2048|191/2048
  ARITH_INTERVAL|[95/1024,191/2048)
  ARITH_SYMBOL|D|cum=[3/4,1)
  S|191/2048|95/1024|1/2048
  M|1/2048|3/4|3/8192
  A|95/1024|3/8192|763/8192
  M|1/2048|1|1/2048
  A|95/1024|1/2048|191/2048
  ARITH_INTERVAL|[763/8192,191/2048)
  A|763/8192|191/2048|1527/8192
  D|1527/8192|2|1527/16384
  Z|interval=[763/8192,191/2048); code=1527/16384
Answer: interval=[763/8192,191/2048); code=1527/16384
```

### Gradient Step — `GradientStepGenerator`  ·  graduate · difficulty 4

One gradient-descent step on linear-regression MSE loss.

**Variants:** `gradient_step_three_sample`, `gradient_step_two_sample`

```
Problem: For linear model y_hat = w0 + w1*x with samples [(3,6), (0,0), (-3,-7)], start at w=(0,-1). Use MSE L=(1/n) sum (y_hat-y)^2 and learning rate eta=1/7. Compute one gradient-descent update.
Steps:
  MSE_SETUP|model y_hat=w0+w1*x|samples=[(3,6), (0,0), (-3,-7)]|w=(0,-1), eta=1/7
  MSE_FORMULA|L=(1/n) sum r_i^2|grad=(2/n) sum r_i*[1,x_i]
  M|-1|3|-3
  A|0|-3|-3
  S|-3|6|-9
  E|-9|2|81
  A|0|81|81
  A|0|-9|-9
  M|-9|3|-27
  A|0|-27|-27
  MSE_SAMPLE|i=1|pred=-3|r=-9
  M|-1|0|0
  A|0|0|0
  S|0|0|0
  E|0|2|0
  A|81|0|81
  A|-9|0|-9
  M|0|0|0
  A|-27|0|-27
  MSE_SAMPLE|i=2|pred=0|r=0
  M|-1|-3|3
  A|0|3|3
  S|3|-7|10
  E|10|2|100
  A|81|100|181
  A|-9|10|1
  M|10|-3|-30
  A|-27|-30|-57
  MSE_SAMPLE|i=3|pred=3|r=10
  D|181|3|181/3
  M|2|1|2
  D|2|3|2/3
  M|2|-57|-114
  D|-114|3|-38
  MSE_GRADIENT|g0=2/3|g1=-38
  M|1/7|2/3|2/21
  S|0|2/21|-2/21
  M|1/7|-38|-38/7
  S|-1|-38/7|31/7
  GD_UPDATE|w_old=(0,-1)|eta=1/7|w_new=(-2/21,31/7)
  Z|loss=181/3; gradient=(2/3,-38); w_new=(-2/21,31/7)
Answer: loss=181/3; gradient=(2/3,-38); w_new=(-2/21,31/7)
```

### Perceptron — `PerceptronGenerator`  ·  graduate · difficulty 3

Perceptron updates over one ordered epoch of a small labeled dataset.

**Variants:** `perceptron_four_point_epoch`, `perceptron_three_point_epoch`

```
Problem: Run one perceptron epoch with eta=2, starting weights w=(0,2,-1) for samples [(1,1,-1), (0,2,1), (-1,2,1), (1,0,-1)]. Use bias feature x0=1, score=w0+w1*x1+w2*x2, and update when y*score <= 0.
Steps:
  PERCEPTRON_SETUP|eta=2|w=(0,2,-1)|samples=[(1,1,-1), (0,2,1), (-1,2,1), (1,0,-1)]
  PERCEPTRON_RULE|score=w0+w1*x1+w2*x2|if y*score <= 0 update
  PERCEPTRON_SAMPLE|i=1|x=(1,1)|y=-1
  M|2|1|2
  A|0|2|2
  M|-1|1|-1
  A|2|-1|1
  PERCEPTRON_SCORE|i=1|score=1
  M|-1|1|-1
  CHECK|i=1|y*score=-1|update
  M|2|-1|-2
  M|-2|1|-2
  A|0|-2|-2
  M|-2|1|-2
  A|2|-2|0
  M|-2|1|-2
  A|-1|-2|-3
  PERCEPTRON_UPDATE|i=1|w=(-2,0,-3)
  PERCEPTRON_SAMPLE|i=2|x=(0,2)|y=1
  M|0|0|0
  A|-2|0|-2
  M|-3|2|-6
  A|-2|-6|-8
  PERCEPTRON_SCORE|i=2|score=-8
  M|1|-8|-8
  CHECK|i=2|y*score=-8|update
  M|2|1|2
  M|2|1|2
  A|-2|2|0
  M|2|0|0
  A|0|0|0
  M|2|2|4
  A|-3|4|1
  PERCEPTRON_UPDATE|i=2|w=(0,0,1)
  PERCEPTRON_SAMPLE|i=3|x=(-1,2)|y=1
  M|0|-1|0
  A|0|0|0
  M|1|2|2
  A|0|2|2
  PERCEPTRON_SCORE|i=3|score=2
  M|1|2|2
  CHECK|i=3|y*score=2|keep
  PERCEPTRON_UPDATE|i=3|no change|w=(0,0,1)
  PERCEPTRON_SAMPLE|i=4|x=(1,0)|y=-1
  M|0|1|0
  A|0|0|0
  M|1|0|0
  A|0|0|0
  PERCEPTRON_SCORE|i=4|score=0
  M|-1|0|0
  CHECK|i=4|y*score=0|update
  M|2|-1|-2
  M|-2|1|-2
  A|0|-2|-2
  M|-2|1|-2
  A|0|-2|-2
  M|-2|0|0
  A|1|0|1
  PERCEPTRON_UPDATE|i=4|w=(-2,-2,1)
  Z|w_final=(-2,-2,1); updates=3
Answer: w_final=(-2,-2,1); updates=3
```

### Backprop — `BackpropGenerator`  ·  graduate · difficulty 5

One exact backpropagation step for a tiny 2-2-1 ReLU network.

**Variants:** `backprop_relu_step`

```
Problem: For a 2-2-1 ReLU network with x=(1,1), y=-4, eta=1/4, W1=[[0,2], [1,1]], b1=(0,1), v=(1,-1), c=2. Do one SGD backprop step using L=1/2*(y_hat-y)^2.
Steps:
  BACKPROP_SETUP|x=(1,1)|y=-4|eta=1/4
  PARAMS|W1=[[0,2], [1,1]]|b1=(0,1)|v=(1,-1), c=2
  M|0|1|0
  M|2|1|2
  A|0|2|2
  A|2|0|2
  HIDDEN_PRE|h1|z=2
  RELU|z=2|h=2|deriv=1
  M|1|1|1
  M|1|1|1
  A|1|1|2
  A|2|1|3
  HIDDEN_PRE|h2|z=3
  RELU|z=3|h=3|deriv=1
  M|1|2|2
  M|-1|3|-3
  A|2|-3|-1
  A|-1|2|1
  OUTPUT|y_hat=1
  S|1|-4|5
  E|5|2|25
  D|25|2|25/2
  BACKPROP_GRAD|dL/dy_hat|5
  M|5|2|10
  BACKPROP_GRAD|dv1|10
  M|5|3|15
  BACKPROP_GRAD|dv2|15
  BACKPROP_GRAD|dc|5
  M|5|1|5
  M|5|1|5
  BACKPROP_DELTA|h1|delta=5
  M|5|1|5
  BACKPROP_GRAD|dW1_11|5
  M|5|1|5
  BACKPROP_GRAD|dW1_12|5
  BACKPROP_GRAD|db1_1|5
  M|5|-1|-5
  M|-5|1|-5
  BACKPROP_DELTA|h2|delta=-5
  M|-5|1|-5
  BACKPROP_GRAD|dW1_21|-5
  M|-5|1|-5
  BACKPROP_GRAD|dW1_22|-5
  BACKPROP_GRAD|db1_2|-5
  M|1/4|5|5/4
  S|0|5/4|-5/4
  UPDATE|W1_11|-5/4
  M|1/4|5|5/4
  S|2|5/4|3/4
  UPDATE|W1_12|3/4
  M|1/4|5|5/4
  S|0|5/4|-5/4
  UPDATE|b1_1|-5/4
  M|1/4|-5|-5/4
  S|1|-5/4|9/4
  UPDATE|W1_21|9/4
  M|1/4|-5|-5/4
  S|1|-5/4|9/4
  UPDATE|W1_22|9/4
  M|1/4|-5|-5/4
  S|1|-5/4|9/4
  UPDATE|b1_2|9/4
  M|1/4|10|5/2
  S|1|5/2|-3/2
  UPDATE|v1|-3/2
  M|1/4|15|15/4
  S|-1|15/4|-19/4
  UPDATE|v2|-19/4
  M|1/4|5|5/4
  S|2|5/4|3/4
  UPDATE|c|3/4
  Z|y_hat=1; loss=25/2; W1_new=[[-5/4,3/4], [9/4,9/4]]; b1_new=(-5/4,9/4); v_new=(-3/2,-19/4); c_new=3/4
Answer: y_hat=1; loss=25/2; W1_new=[[-5/4,3/4], [9/4,9/4]]; b1_new=(-5/4,9/4); v_new=(-3/2,-19/4); c_new=3/4
```

### Information Gain — `InformationGainGenerator`  ·  graduate · difficulty 4

Decision-tree information gain from supplied entropy log constants.

**Variants:** `information_gain_best_split`

```
Problem: A dataset has 16 examples with pos=7 and neg=9. Candidate splits are texture: left pos=4, neg=4; right pos=3, neg=5 and source: left pos=7, neg=1; right pos=0, neg=8. Use self-info values I(p)=-log2(p): 1/8=3, 3/8=1.415, 7/16=1.193, 1/2=1, 9/16=0.83, 5/8=0.678, 7/8=0.193, 1=0. Compute information gain for each split and choose the better split.
Steps:
  IG_SETUP|parent pos=7, neg=9|total=16|splits=texture,source
  INFO_TABLE|1/8=3, 3/8=1.415, 7/16=1.193, 1/2=1, 9/16=0.83, 5/8=0.678, 7/8=0.193, 1=0
  ENTROPY_SETUP|parent|counts=7,9|total=16
  D|7|16|7/16
  INFO_VALUE|p=7/16|I=1.193
  M|7/16|1.193|0.5219375
  A|0|0.5219375|0.5219375
  D|9|16|9/16
  INFO_VALUE|p=9/16|I=0.83
  M|9/16|0.83|0.466875
  A|0.5219375|0.466875|0.9888125
  ENTROPY_VALUE|parent|0.9888125
  SPLIT_SETUP|texture|left pos=4, neg=4|right pos=3, neg=5
  ENTROPY_SETUP|texture_left|counts=4,4|total=8
  D|4|8|1/2
  INFO_VALUE|p=1/2|I=1
  M|1/2|1|0.5
  A|0|0.5|0.5
  D|4|8|1/2
  INFO_VALUE|p=1/2|I=1
  M|1/2|1|0.5
  A|0.5|0.5|1
  ENTROPY_VALUE|texture_left|1
  D|8|16|1/2
  M|1/2|1|0.5
  ENTROPY_SETUP|texture_right|counts=3,5|total=8
  D|3|8|3/8
  INFO_VALUE|p=3/8|I=1.415
  M|3/8|1.415|0.530625
  A|0|0.530625|0.530625
  D|5|8|5/8
  INFO_VALUE|p=5/8|I=0.678
  M|5/8|0.678|0.42375
  A|0.530625|0.42375|0.954375
  ENTROPY_VALUE|texture_right|0.954375
  D|8|16|1/2
  M|1/2|0.954375|0.4771875
  A|0.5|0.4771875|0.9771875
  S|0.9888125|0.9771875|0.011625
  INFO_GAIN|texture|0.011625
  SPLIT_SETUP|source|left pos=7, neg=1|right pos=0, neg=8
  ENTROPY_SETUP|source_left|counts=7,1|total=8
  D|7|8|7/8
  INFO_VALUE|p=7/8|I=0.193
  M|7/8|0.193|0.168875
  A|0|0.168875|0.168875
  D|1|8|1/8
  INFO_VALUE|p=1/8|I=3
  M|1/8|3|0.375
  A|0.168875|0.375|0.543875
  ENTROPY_VALUE|source_left|0.543875
  D|8|16|1/2
  M|1/2|0.543875|0.2719375
  ENTROPY_SETUP|source_right|counts=0,8|total=8
  ENTROPY_ZERO|source_right|count=0
  D|8|8|1
  INFO_VALUE|p=1|I=0
  M|1|0|0
  A|0|0|0
  ENTROPY_VALUE|source_right|0
  D|8|16|1/2
  M|1/2|0|0
  A|0.2719375|0|0.2719375
  S|0.9888125|0.2719375|0.716875
  INFO_GAIN|source|0.716875
  CHECK|texture vs source|0.011625 < 0.716875|choose=source
  Z|best=source; gain_texture=0.011625; gain_source=0.716875
Answer: best=source; gain_texture=0.011625; gain_source=0.716875
```

### Matrix Calculus — `MatrixCalculusGenerator`  ·  graduate · difficulty 4

Matrix-calculus gradients for linear and quadratic vector expressions.

**Variants:** `matrix_calculus_linear_form`, `matrix_calculus_quadratic_form`

```
Problem: For A=[[2,-4], [0,4]] and x=(2,1), compute grad_x(x^T A x) using (A+A^T)x.
Steps:
  MC_SETUP|expression=x^T A x|A=[[2,-4], [0,4]]|x=(2,1)
  GRADIENT_FORMULA|grad_x(x^T A x)=(A+A^T)x
  MATRIX_SUM|B=A+A^T
  A|2|2|4
  MAT_ENTRY|B11|4
  A|-4|0|-4
  MAT_ENTRY|B12|-4
  A|0|-4|-4
  MAT_ENTRY|B21|-4
  A|4|4|8
  MAT_ENTRY|B22|8
  M|4|2|8
  M|-4|1|-4
  A|8|-4|4
  GRAD_ENTRY|g1|4
  M|-4|2|-8
  M|8|1|8
  A|-8|8|0
  GRAD_ENTRY|g2|0
  Z|grad=(4,0)
Answer: grad=(4,0)
```
