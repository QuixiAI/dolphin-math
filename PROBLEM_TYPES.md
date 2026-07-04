# Problem Types

Every problem type this dataset can generate. For each type: a one-line description, the grade band and coarse difficulty (1–5, read relative to the band), the internal operation variants, and one real worked example (the pipe-delimited `steps` are the model's scratchpad).

**284 problem types.** This file is generated — do not hand-edit. Regenerate with `uv run python tools/gen_problem_types.py`.

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
