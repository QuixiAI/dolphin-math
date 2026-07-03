# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

250 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 3 | `A\|25\|36\|61` | evaluate_expression_generator.py, fraction_op_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py, percent_word_problem_generator.py, polygon_perimeter_generator.py, pythag_hyp_generator.py, simple_stats_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|4x - 1 = 8` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-2 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-4 < 0\|Absolute value is always non-negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|2x + 10 > 7 -> x > -3/2` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|\|3x - 8\| <= 4` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for >` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|AND case\|-4 <= 3x - 8 <= 4` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|\|4x - 1\| = 8` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|4x - 1 = 8\|4x - 1 = -8` | absolute_value_equation_generator.py |
| `AB_ADD_DGT` | 3 | `AB_ADD_DGT\|col_0\|4+8+0\|12` | abacus_addition_generator.py |
| `AB_CARRY` | 3 | `AB_CARRY\|col_0\|1\|col_1` | abacus_addition_generator.py |
| `AB_CARRY_FINAL` | 1 | `AB_CARRY_FINAL\|1` | abacus_addition_generator.py |
| `AB_INFO` | 1 | `AB_INFO\|Adding 9828 column by column` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|514` | abacus_addition_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|7+1+0\|->8 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|295292 + 3691150 + 51676100 + 516761000 + 738230000\|1310653542` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|38.94\|419.49` | number_comparison_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|8x + -20 = 180` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|supplementary\|(6x + 10)° + (2x - 30)° = 180°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|8x = 200\|x = 25` | angle_relationships_generator.py |
| `AREA` | 1, 3 | `AREA\|75` | geometry_area_perimeter_generator.py |
| `B` | 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `C` | 3 | `C\|5/4\|20\|25/20` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py |
| `CALC` | 1 | `CALC\|x = -2` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CHECK` | 3 | `CHECK\|cross_products\|9×121=1089\|11×99=1089` | linear_fractional_generator.py, ratio_table_generator.py, special_solution_equation_generator.py, tip_bill_split_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|16·0 + 4 = 4\|16·0 + 9 = 9` | special_solution_equation_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|C = 19π\|19π` | circle_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|C = πd` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|19\|diameter` | circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|C = π × 19` | circle_generator.py |
| `CMP` | 3 | `CMP\|14/22\|33/22\|<` | fraction_comparison_generator.py, graph_interpret_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|38.94\|419.49\|<` | number_comparison_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|-4\|+7\|3` | equation_from_two_points_generator.py, linear_complex_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_X` | 3 | `COMB_X\|-x\|+2x\|x` | linear_complex_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|2\|44` | divisibility_classification_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|2x + 7 < -3 -> x < -5` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|0 < x - 2 < 3` | compound_inequality_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 hr\|60 min` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|47 hr\|2820 min` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|1\|2\|3` | decimal_mult_generator.py |
| `D` | 3 | `D\|632\|99\|6` | decimal_div_generator.py, dimensional_analysis_generator.py, geometry_area_perimeter_generator.py, linear_simple_generator.py, long_division_generator.py, order_of_operations_generator.py, percent_problem_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, rate_conversion_generator.py, ratio_table_generator.py, simple_probability_generator.py, slope_two_points_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|6+0+0\|->6 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|61.36\|04.30` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|57.7/8.0\|57.7/80\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|4-2 (borrow_in 0)\|->2 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|0.9\|9/10` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|3.5\|350.00%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|3/4\|terminating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|3/4\|0.75` | repeating_decimal_generator.py |
| `DISC` | 3 | `DISC\|64\|0\|64` | quadratic_generator.py |
| `DIST` | 3 | `DIST\|-3\|x+5\|-3x-15` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|-12y + -80 = -8` | systems_substitution_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|-2x\|6x^3 + 10x^2 - 2x` | multiplying_polynomials_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|88\|2\|0` | divisibility_classification_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|3\|1\|x=3` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|577\|80` | decimal_div_generator.py, percent_problem_generator.py |
| `E` | 3 | `E\|16\|2\|256` | pythag_hyp_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(10, 10)\|(13, 10)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 4 | `EQ_OP_BOTH\|subtract\|14\|x\|9` | absolute_value_equation_generator.py, linear_fractional_generator.py, one_step_equation_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|divide\|p\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|9` | linear_fractional_generator.py, one_step_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1 | `EQ_SETUP\|x = 150/5` | linear_fractional_generator.py, literal_equation_generator.py, one_step_equation_generator.py, proportion_word_problem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|x/6 = -7` | linear_fractional_generator.py, two_step_equation_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|(-5) × (-5) × (-5) × (-5) × (-5) × (-5)` | exponent_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|-5\|-5\|25` | exponent_generator.py |
| `EXP_RULE_APPLY` | 4 | `EXP_RULE_APPLY\|multiply\|2\|3\|6` | exponent_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|zero_exponent\|x^0 = 1 (for x ≠ 0)` | exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|m^0` | exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|1` | exponent_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|-5\|6` | exponent_generator.py |
| `F` | 2 | `F\|3/6\|1/2` | fraction_op_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py, repeating_decimal_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|31\|1\|0` | factors_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|31` | factors_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|-2` | parallel_perpendicular_line_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: (3x) * (6x)\|18x^2` | multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-3) * (6x)\|-18x` | multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-3) * (3)\|-9` | multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: (3x) * (3)\|9x` | multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(3x - 3)(6x + 3)` | multiplying_binomials_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|7/10\|0.7` | fraction_decimal_percent_converter.py |
| `GCD_RESULT` | 1 | `GCD_RESULT\|1` | lcm_generator.py |
| `GCD_START` | 2 | `GCD_START\|75\|134` | gcf_generator.py, lcm_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|75\|134\|75` | gcf_generator.py, lcm_generator.py |
| `GOAL` | 1 | `GOAL\|Convert to Slope-Intercept Form (y = mx + b)` | point_slope_generator.py, standard_form_conversion_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|Jan\|Feb\|-1` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|line_graph\|Week 1:15,Week 2:14,Week 3:10,Week 4:16,Week 5:19,Week 6:25,Week 7:23,Week 8:19` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Week 6\|25` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|Feb\|Mar\|7` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|min\|18` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Week 1\|15` | graph_interpret_generator.py |
| `I` | 2 | `I\|3/2\|2/3` | fraction_op_generator.py, mixed_number_operation_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|486/35\|13 31/35` | mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Multiplying by negative number reverses inequality` | linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|add\|8\|4 <= 3x <= 12` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|multiply\|4\|x\|28` | linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|≥\|28` | linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x/4 ≥ 7` | linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|x + 3 < 2` | two_step_inequality_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|17\|17` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|36767\|33851` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|8\|positive\|8` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|-\|17\|9\|8` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|19 - (-17)\|19 + 17` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|different_signs\|Different signs: subtract absolute values, take sign of larger absolute value` | integer_operations_generator.py |
| `L` | 3 | `L\|4\|5\|20` | fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|113*20\|1\|2260` | lcm_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|parallel\|y = -2x - 2\|(5, -9)` | parallel_perpendicular_line_generator.py |
| `M` | 2, 3 | `M\|6\|99\|594` | decimal_div_generator.py, dimensional_analysis_generator.py, evaluate_expression_generator.py, fraction_op_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, long_division_generator.py, mixed_number_operation_generator.py, multi_step_unit_conversion_generator.py, order_of_operations_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, rate_conversion_generator.py, ratio_table_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, unit_conversion_generator.py, volume_rect_prism_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|93\|7\|13.285714285714286` | simple_stats_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|9\|12` | simple_stats_generator.py |
| `MEDIAN_PICK` | 3 | `MEDIAN_PICK\|12\|\|12` | simple_stats_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|3 6/7\|27/7` | mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MODE` | 2 | `MODE\|1\|3, 6, 9, 10, 11, 16, 17, 18, 19` | simple_stats_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|3\|1` | simple_stats_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^6 * x^2 = x^(6+2)\|x^8` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|45 / 5\|9` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|-4 * -7\|28` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(45x^4) / (5x^4)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^4 / x^4 = x^(4-4)\|x^0 = 1` | monomial_mult_div_generator.py |
| `MOVE_TERM` | 3 | `MOVE_TERM\|-2x\|left\|-x-7+2x = -4` | linear_complex_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|4\|73823\|295292` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|73823\|17754` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|10\|9.3x\|93x` | linear_fractional_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = -2\|Parallel lines have the same slope` | parallel_perpendicular_line_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|(3x + 14) + (2x + 76) = 180` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|co_interior\|Co-interior angles are supplementary (sum to 180°)` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|5x + 90 = 180\|x = 18` | angle_relationships_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|0.1\|10\|1` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|90%\|0.9` | fraction_decimal_percent_converter.py, percent_problem_generator.py, percent_word_problem_generator.py, tip_bill_split_generator.py |
| `PERIM` | 1 | `PERIM\|44` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|3` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|72\|2\|36` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Birds\|6` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|▲\|10` | graph_interpret_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|2760333\|3\|2760.333` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 2 | `PLACE_DP_Q\|72125\|2` | decimal_div_generator.py, percent_problem_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 10 = 0(x - 10)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|3x^3 + 2x^2 + 5x - 15` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(- 14x^4 + 28x^3) / (-7x)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(-14x^4) / (-7x) + (28x^3) / (-7x)` | polynomial_div_monomial_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(3x^3) + (9x^2 -7x^2) + (5x) + (-8 -7)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(-2x + 4)(-3x^2 - 5x + 1)` | multiplying_polynomials_generator.py |
| `POLY_SETUP` | 1 | `POLY_SETUP\|(9x^2 + 5x - 8) + (3x^3 - 7x^2 - 7)` | polynomial_add_sub_generator.py |
| `PRIME` | 1 | `PRIME\|23` | divisibility_classification_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(blue\|first was red)\|5/7` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Coin flip and die roll, looking for heads and 1` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(heads)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Coin flip and die roll are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/6\|1/12` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|5\|8` | simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | *(not observed in sampling)* | compound_probability_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|25/5 = x/6` | proportion_word_problem_generator.py, proportional_relationship_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|h² = 25 - 9 = 16\|16` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 2 | `PYTHAG_CONTEXT\|ladder\|ladder=5ft, given=3ft` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|ground=3\|wall=4\|ladder=5` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|576\|24` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 3 | `PYTHAG_SETUP\|c=51\|a=45\|b=?` | pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 2601 - 2025\|576` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|45\|2025` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|45² + b² = 51²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|-8\|8\|4\|0` | quadratic_generator.py |
| `Q2` | 4 | `Q2\|-8\|8\|4\|-4` | quadratic_generator.py |
| `R` | 1 | `R\|28` | long_division_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|9:11\|1\|9:11` | ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Trees: 9, 63, 81, ?\|Rows: 11, 77, 99, 121` | ratio_table_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 5 / 0.1` | percent_problem_generator.py |
| `REWRITE` | 1 | `REWRITE\|12 + 36` | evaluate_expression_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, order_of_operations_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `ROOT` | 2 | `ROOT\|400\|20` | pythag_hyp_generator.py, quadratic_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|6` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|216\|perfect_cube\|6` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|∛216` | exponent_generator.py |
| `ROOT_SIMPLIFY` | 1 | `ROOT_SIMPLIFY\|7√7` | exponent_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|34441\|1000\|<5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|34441\|34000` | place_value_rounding_generator.py |
| `S` | 3 | `S\|632\|594\|38` | decimal_div_generator.py, fraction_op_generator.py, graph_interpret_generator.py, linear_simple_generator.py, long_division_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, slope_two_points_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(7)² = 2π × 49\|98π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|10 × 12\|120` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 7 × 11\|154π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=10, w=12, h=3` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(120 + 30 + 36)\|372` | volume_3d_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|25\|5\|5.0` | scaling_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|25 meters\|scaled_dimension` | scaling_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|1\|100\|100` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 centimeter\|5 meters\|5` | scaling_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|2.8\|-5` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|right\|5` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|multiply_coefficients\|2.3\|3.4\|7.819999999999999` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|(2.3 × 10^2) × (3.4 × 10^2)` | exponent_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|part = 0.1 * 10` | percent_problem_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|7\|2\|14` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|12.0\|8\|1.5` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|square\|8\|12.0` | scaling_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|9` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = 3 + 9x` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|0` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(-9, -1)\|(-5, -9)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (-9 - (-1)) / (-5 - (-9))` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SORT` | 2 | `SORT\|19,1,18,12,11\|1,11,12,18,19` | simple_stats_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|4 = 9\|contradiction: no value of x works` | special_solution_equation_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|14\|14` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(68 + 77) / 2\|72.5` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|8` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|38\|24\|14` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|248 / 8\|31` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|26\|2` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|50\|5\|10` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|73` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|120 / 5\|24` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|positions 5 and 6\|68, 77` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|36` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|57\|4` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|20, 30, 52, 61, 68, 77, 78, 79, 83, 97` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|73 - 36\|37` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|12, 43, 43, 53, 22, 10, 28, 37` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|12 + 43 + 43 + 53 + 22 + 10 + 28 + 37\|248` | statistics_generator.py |
| `SUBST` | 3 | `SUBST\|x\|3\|-4(3)-y-7` | evaluate_expression_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|1-6-borrow0\|->5 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: 10y = 80` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with y only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = 3y + 16` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * 4` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|8x + 12y = 160\|-8x - 2y = -80` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x - 3y = 16\|-5x + 3y = -8` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=-6 into x = 3y + 16` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|53\|33\|x` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|x = 180 - 53 - 33\|94` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|53 + 33 + x = 180` | angle_relationships_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|$3.00\|6\|$0.50` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|4\|48` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|6\|tickets\|$3.00` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|4,5,6,7\|48,60,72,84` | unit_rate_generator.py |
| `VOLUME` | 1 | `VOLUME\|550` | volume_rect_prism_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 8 × 5\|20.0` | volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 15 × 4 × 11\|660` | volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = l × w × h` | volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|rectangular_prism\|l=15, w=4, h=11` | volume_3d_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, angle_relationships_generator.py, circle_generator.py, compound_inequality_generator.py, compound_probability_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, dimensional_analysis_generator.py, divisibility_classification_generator.py, equation_from_two_points_generator.py, evaluate_expression_generator.py, exponent_generator.py, factors_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, gcf_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, integer_operations_generator.py, lcm_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, long_division_generator.py, mixed_number_operation_generator.py, monomial_mult_div_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, number_comparison_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, order_of_operations_generator.py, parallel_perpendicular_line_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, place_value_rounding_generator.py, point_slope_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, prime_factorization_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, quadratic_generator.py, rate_conversion_generator.py, ratio_table_generator.py, repeating_decimal_generator.py, scaling_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplify_expression_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, statistics_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, unit_conversion_generator.py, unit_rate_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py |
