# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

357 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 3 | `A\|27\|2\|29` | arithmetic_sequence_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_number_ops_generator.py, conic_standard_form_generator.py, distance_formula_generator.py, ellipse_features_generator.py, evaluate_expression_generator.py, exponential_model_generator.py, fill_in_step_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, nets_surface_area_generator.py, order_of_operations_generator.py, parabola_features_generator.py, pascal_triangle_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, pythag_hyp_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, remainder_factor_theorem_generator.py, round_solids_generator.py, segment_partition_generator.py, sigma_notation_generator.py, simple_stats_generator.py, synthetic_division_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|x - 9 = 6` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-1 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-5 < 0\|Absolute value is always non-negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|x - 5 >= 13 -> x >= 18` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|\|2x + 9\| < 8` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for >` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|AND case\|-8 < 2x + 9 < 8` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|\|x - 9\| = 6` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|x - 9 = 6\|x - 9 = -6` | absolute_value_equation_generator.py |
| `AB_ADD_DGT` | 3 | `AB_ADD_DGT\|col_0\|0+1+0\|1` | abacus_addition_generator.py |
| `AB_CARRY` | 3 | `AB_CARRY\|col_1\|1\|col_2` | abacus_addition_generator.py |
| `AB_CARRY_FINAL` | 1 | `AB_CARRY_FINAL\|1` | abacus_addition_generator.py |
| `AB_INFO` | 1 | `AB_INFO\|Adding 4581 column by column` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 2 | `ACCEPT\|(3, -9)\|product -27 ✓, sum -6 ✓` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|9 × 5\|45` | factor_trinomial_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|817.63\|148.87` | number_comparison_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|angle1 + angle2 = 90°` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|complementary\|angle1 = 13°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|90 - 13\|77` | angle_relationships_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = (θ/360)·2πr` | arc_sector_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 11, central angle 150°\|sector area` | arc_sector_generator.py |
| `AREA` | 1, 3 | `AREA\|80` | geometry_area_perimeter_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = 1 ± (4/3)(x + 1)` | hyperbola_features_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|61 <= 100\|yes` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$25.00` | piecewise_evaluation_generator.py |
| `C` | 3 | `C\|3/2\|18\|27/18` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|x = 3` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CANCEL` | 2 | `CANCEL\|5y\|7y - 5` | rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1/2, ±1, ±3/2, ±2, ±3, ±4, ±6, ±12` | rational_root_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CBRT` | 2 | `CBRT\|y^3\|y` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CENTER` | 1 | `CENTER\|(3, 6)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_8(4) = log_2(4)/log_2(8)` | log_conversion_generator.py |
| `CHECK` | 3 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | arithmetic_sequence_generator.py, completing_square_generator.py, error_spotting_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, fill_in_step_generator.py, geometric_sequence_generator.py, horner_evaluation_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_equation_generator.py, long_division_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, recursive_explicit_generator.py, similar_triangles_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, tip_bill_split_generator.py, two_step_equation_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|17·0 + 1 = 1\|17·0 + 1 = 1` | special_solution_equation_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|inscribed angle 50°\|intercepted arc` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|A = π × 169\|169π` | circle_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|A = πr²` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|13\|radius` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|A = π × 13²` | circle_generator.py |
| `CMP` | 3 | `CMP\|9/3\|2/3\|>` | fraction_comparison_generator.py, graph_interpret_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|817.63\|148.87\|>` | number_comparison_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|3, -14, 13, 2` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|4\|-9\|-5` | equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_X` | 3 | `COMB_X\|-4x\|-4x\|-8x` | linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|6 - 4\|2` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|-8/(-4)\|2` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of -4 = -2\|(-2)^2 = 4` | completing_square_generator.py, conic_standard_form_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|3\|47` | divisibility_classification_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|x + 7 < -3 -> x < -10` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|5 < x + 4 < 11` | compound_inequality_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|(x + 2)^2 = -16(y + 1)\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|-4 + 3i\|-4 - 3i` | complex_division_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 1/2 < 1\|converges` | geometric_sequence_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 lb\|16 oz` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|2 lb\|32 oz` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|2\|1\|3` | decimal_mult_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|12·EF = 32·18` | similar_triangles_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(9 - 8i)(-3 - 8i)\|multiply` | complex_division_generator.py, complex_number_ops_generator.py |
| `D` | 3 | `D\|632\|99\|6` | arithmetic_sequence_generator.py, circle_angle_generator.py, circle_equation_generator.py, complex_number_ops_generator.py, conic_standard_form_generator.py, decimal_div_generator.py, dimensional_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, function_operations_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, linear_simple_generator.py, log_conversion_generator.py, long_division_generator.py, midpoint_generator.py, nets_surface_area_generator.py, order_of_operations_generator.py, parabola_features_generator.py, percent_problem_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, regular_polygon_area_generator.py, round_solids_generator.py, segment_partition_generator.py, similar_triangles_generator.py, simple_probability_generator.py, slope_two_points_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|8+0+0\|->8 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|17.98\|23.20` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|7.5/1.0\|7.5/10\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|7-1 (borrow_in 0)\|->6 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|0.1\|1/10` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1\|100.00%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|5/12\|repeating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|5/12\|0.416667` | repeating_decimal_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = deg den = 2\|y = 1/1` | rational_function_features_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|y = 3` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|1089\|1080\|9` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|-3 < 0\|no real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|3\|-4x+3\|-12x+9` | equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|-20y + 105 = -15` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | distance_formula_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|x\|- 2x^3 + 4x^2 - 5x` | multiplying_polynomials_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|89\|2\|1` | divisibility_classification_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|-5\|-8\|x=5/8` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|75\|10` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|36n^3\|6\|6n^3` | factor_gcf_generator.py, polynomial_long_division_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|radicand ≥ 0\|x - 5 ≥ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 5\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, rational_equation_generator.py |
| `E` | 3 | `E\|21\|2\|441` | arc_sector_generator.py, circle_equation_generator.py, complex_division_generator.py, conic_standard_form_generator.py, distance_formula_generator.py, ellipse_features_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, hyperbola_features_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, piecewise_evaluation_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, remainder_factor_theorem_generator.py, round_solids_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|3x + 1 = 4` | exponential_equation_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(-7, 6)\|(-5, 10)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 4 | `EQ_OP_BOTH\|divide\|4\|x\|-8` | absolute_value_equation_generator.py, completing_square_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_equation_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|divide\|x\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|-8` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 45/3` | completing_square_generator.py, complex_quadratic_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|10x = -70` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|68029 × 24289 ≈ 70000 × 20000\|1400000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|1400000000\|1652356381\|1652356381 ≈ 1400000000 ✓` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `EVAL` | 2 | `EVAL\|g(2)\|-15` | circle_equation_generator.py, complex_division_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, log_conversion_generator.py, log_properties_generator.py, parabola_features_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, remainder_factor_theorem_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|10 × 10` | exponent_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|10\|10\|100` | exponent_generator.py |
| `EXP_RULE_APPLY` | 4 | `EXP_RULE_APPLY\|negate\|3\|\|3` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|negative_exponent\|x^(-n) = 1/x^n` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|y^(-3)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|1/y^3` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|10\|2` | exponent_generator.py |
| `F` | 2 | `F\|9/9\|1` | fraction_op_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|9x^2 + 15x\|3x\|(3x + 5)` | conic_standard_form_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = -27\|m + n = -6` | factor_trinomial_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|107\|1\|0` | factors_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|107` | factors_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|3/2` | parallel_perpendicular_line_generator.py |
| `FLAG` | 2 | `FLAG\|4\|72 ÷ 8 = 9, not 8` | error_spotting_generator.py |
| `FOCUS` | 1 | `FOCUS\|(-2, -5)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: 9 * (-3)\|-27` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-8i) * (-3)\|24i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-8i) * (-8i)\|64i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: 9 * (-8i)\|-72i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(5 + √3)(1 + √3)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|difference_of_squares\|a^2 - b^2 = (a - b)(a + b)` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|16/-20\|-4/5` | arc_sector_generator.py, complex_division_generator.py, function_operations_generator.py, hyperbola_features_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|2/6\|0.3333333333` | fraction_decimal_percent_converter.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(g/h)(2)\|g(2)/h(2)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|f(t) = 3t + 3\|f(5)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `GCD_RESULT` | 1 | `GCD_RESULT\|2` | lcm_generator.py |
| `GCD_START` | 2 | `GCD_START\|35\|61` | gcf_generator.py, lcm_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|35\|61\|35` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|36, 12, 30\|6` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|6` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|n^5, n^3, n\|n` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude h = 7 to the hypotenuse; one segment p = 7\|the other segment q` | geometric_mean_generator.py |
| `GOAL` | 1 | `GOAL\|Convert to Slope-Intercept Form (y = mx + b)` | point_slope_generator.py, standard_form_conversion_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|Jan\|Feb\|-4` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|pictograph\|key:■=10` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Burgers\|12` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|Apr\|May\|3` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Monday\|19` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Monday\|19` | graph_interpret_generator.py |
| `GROUP` | 2 | `GROUP\|(9x^2 + 15x)\|(3x + 5)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `HA` | 1 | `HA\|y = 1` | rational_function_features_generator.py |
| `HOLE` | 1 | `HOLE\|x = -5` | rational_function_features_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|2x^4 + 3x^3 - 2x^2 - 4x + 5\|x = -4` | horner_evaluation_generator.py |
| `I` | 2 | `I\|3/2\|2/3` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|75/14\|5 5/14` | mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Dividing by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|subtract\|9\|-17 < 2x < -1` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|divide\|-7\|x\|3` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|≤\|3` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|-7x ≥ -21` | linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|2x ≤ -12` | domain_range_generator.py, two_step_inequality_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|56\|56` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|7\|negative\|-7` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|÷\|56\|8\|7` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|20 - (-11)\|20 + 11` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|div_different_signs\|Different signs: result is negative` | integer_operations_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^2\|-1` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|64i^2\|-64` | complex_division_generator.py, complex_number_ops_generator.py |
| `L` | 3 | `L\|2\|9\|18` | fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|54*50\|2\|1350` | lcm_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|parallel\|y = 3/2x - 6\|(4, 5)` | parallel_perpendicular_line_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|ln(e^(3x)) = ln(18)` | exponential_equation_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|log_b(x) = y ⟺ b^y = x` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|ln(1) = 0\|0` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|2x - 2 = x + 5` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|3log_5(x)\|log_5(x^3)` | log_properties_generator.py |
| `LOG_PRODUCT` | 2 | `LOG_PRODUCT\|log_5(x^3) + log_5(y)\|log_5(x^3y)` | log_equation_generator.py, log_properties_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_5(x^3y) - log_5(z)\|log_5(x^3y/z)` | log_properties_generator.py |
| `LOG_SETUP` | 2 | `LOG_SETUP\|3log_5(x) + log_5(y) - log_5(z)\|condense` | log_properties_generator.py |
| `M` | 2, 3 | `M\|6\|99\|594` | arc_sector_generator.py, arithmetic_sequence_generator.py, circle_angle_generator.py, conic_standard_form_generator.py, decimal_div_generator.py, dimensional_analysis_generator.py, error_spotting_generator.py, evaluate_expression_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, fill_in_step_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, log_conversion_generator.py, long_division_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, multi_step_unit_conversion_generator.py, nets_surface_area_generator.py, order_of_operations_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, remainder_factor_theorem_generator.py, round_solids_generator.py, segment_partition_generator.py, similar_triangles_generator.py, synthetic_division_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, unit_conversion_generator.py, volume_rect_prism_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|69\|8\|8.625` | simple_stats_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|13\|13` | simple_stats_generator.py |
| `MEDIAN_PICK` | 3 | `MEDIAN_PICK\|16\|\|16` | simple_stats_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|5 9/10\|59/10` | mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MODE` | 2 | `MODE\|3\|2` | simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P(1 + r)^t` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 1000 · (1 + 0.1)^3` | exponential_model_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|2\|1` | simple_stats_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^6 * x^1 = x^(6+1)\|x^7` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|12 / 4\|3` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|4 * -2\|-8` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(4x^6)(-2x)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^3 / x^2 = x^(3-2)\|x^1 = x` | monomial_mult_div_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|+4x\|left\|-4x+9-4x = +4` | completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|12\|(-4/3)x\|-16x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `NEED` | 2 | `NEED\|line 2 gives the base ratio 11:2\|line 4 multiplies 11 by 12` | fill_in_step_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|2 right triangles with legs 6 and 8; rectangles 6 by 5, 8 by 5, and 10 by 5\|total surface area` | nets_surface_area_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = 3/2\|Parallel lines have the same slope` | parallel_perpendicular_line_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|X ~ N(505, 5)\|P(507 < X < 509.5)` | normal_table_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|5x + 26 = 6x + 16` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|corresponding\|Corresponding angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-1x = -10\|x = 10` | angle_relationships_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|row 5` | pascal_triangle_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|0.1\|200\|20` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|90%\|0.9` | exponential_model_generator.py, fill_in_step_generator.py, fraction_decimal_percent_converter.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, tip_bill_split_generator.py |
| `PERIM` | 1 | `PERIM\|32` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|17` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|102\|2\|51` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Trains\|6` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|■\|10` | graph_interpret_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|4060686\|3\|4060.686` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 2 | `PLACE_DP_Q\|75\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|y = ±7\|y = 7 or y = -7` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 6 = 2(x + 7)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|2x^3 - x^2 - 13x - 15\|x - 3` | polynomial_long_division_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|4x^3 + 8x^2 - 8x + 4` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(- 15x^7 + 3x^6 + 6x^5 - 6x^4) / (-3x^3)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(-15x^7) / (-3x^3) + (3x^6) / (-3x^3) + (6x^5) / (-3x^3) + (-6x^4) / (-3x^3)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(4x^3) + (8x^2) + (-1x -7x) + (9 -5)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(x + 2)(-2x^2 + 4x - 5)` | multiplying_polynomials_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(4x^3 - x + 9) + (8x^2 - 7x - 5)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2 | `POLY_SUB\|(2x^3 - x^2) - (2x^3 - 6x^2)\|5x^2` | polynomial_long_division_generator.py |
| `PRIME` | 1 | `PRIME\|89` | divisibility_classification_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(second spades\|first was spades)\|4/17 = 12/51` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Coin flip and die roll, looking for heads and 5` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(heads)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Coin flip and die roll are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/6\|1/12` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|4\|5` | simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | *(not observed in sampling)* | compound_probability_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|9/3 = x/5` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|d² = 9 + 16 = 25\|25` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 2 | `PYTHAG_CONTEXT\|rectangle_diagonal\|length=3, width=4` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|length=3\|width=4\|diagonal=?` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|324\|18` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 3 | `PYTHAG_SETUP\|c=30\|a=24\|b=?` | pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 900 - 576\|324` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|24\|576` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|24² + b² = 30²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|33\|3\|6\|6` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|33\|3\|6\|5` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|(3 - √6)/(3 - √6)` | radical_rationalize_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|28:16\|4\|7:4` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Flour (cups): 28, 49, 70, ?\|Sugar (cups): 16, 28, 40, 44` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 15 / 0.1` | percent_problem_generator.py |
| `REJECT` | 2 | `REJECT\|(1, -27)\|sum is -26, need -6` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `REWRITE` | 1 | `REWRITE\|8 + 90` | circle_equation_generator.py, completing_square_generator.py, complex_division_generator.py, complex_number_ops_generator.py, conic_standard_form_generator.py, domain_range_generator.py, evaluate_expression_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, inverse_function_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, midpoint_generator.py, normal_table_generator.py, order_of_operations_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, synthetic_division_generator.py |
| `ROOT` | 2 | `ROOT\|5625\|75` | completing_square_generator.py, factor_special_forms_generator.py, pythag_hyp_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, round_solids_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|7\|√7` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|343\|49\|7` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|√343` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1 | `ROOT_SIMPLIFY\|7√7` | complex_quadratic_generator.py, distance_formula_generator.py, exponent_generator.py, geometric_mean_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|68867\|100\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|68867\|68900` | place_value_rounding_generator.py |
| `S` | 3 | `S\|632\|594\|38` | arithmetic_sequence_generator.py, circle_angle_generator.py, circle_equation_generator.py, complex_number_ops_generator.py, decimal_div_generator.py, distance_formula_generator.py, ellipse_features_generator.py, exponential_model_generator.py, fraction_op_generator.py, function_operations_generator.py, geometric_sequence_generator.py, graph_interpret_generator.py, hyperbola_features_generator.py, linear_simple_generator.py, long_division_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, normal_table_generator.py, order_of_operations_generator.py, parabola_features_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, segment_partition_generator.py, slope_two_points_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(2)² = 2π × 4\|8π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|11 × 7\|77` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 2 × 15\|60π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=11, w=7, h=4` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(77 + 44 + 28)\|298` | round_solids_generator.py, volume_3d_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|150\|50\|3.0` | scaling_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|150 meters\|scaled_dimension` | scaling_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|6\|20\|120` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 centimeter\|50 meters\|50` | scaling_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|4.6\|-6` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|right\|6` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|divide_coefficients\|24.0\|3.0\|8.0` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|(24.0 × 10^10) ÷ (3.0 × 10^4)` | exponent_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(1, -3), B(-8, 24); ratio 5:4 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (θ/360)·πr^2` | arc_sector_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|a_12 = 4 + (12 - 1)·2` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|4, 6, 8, 10, ...\|sum of first 12 terms` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|part = 0.1 * 200` | percent_problem_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|7 + 10 + 13 + 16 + 19 + 22` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=2)^(7) (3k + 1)\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=2\|3(2) + 1\|7` | sigma_notation_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|4\|3\|12` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|27\|9\|3` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|square\|9\|27` | scaling_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; AB = 12, DE = 32, BC = 18\|find EF` | similar_triangles_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|7` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = 7x` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|2` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(8, -8)\|(-10, -3)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (-3 - (-8)) / (-10 - 8)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SORT` | 2 | `SORT\|1,7,1,5,15,18,17,5\|1,1,5,5,7,15,17,18` | simple_stats_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|1 = 1\|identity: true for every x` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|18x = 15x + 3x\|9x^2 + 15x + 3x + 5` | factor_trinomial_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|y^2 = 49\|y = ±7` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-36)\|6i` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(3x - 20) = x - 6\|3x - 20 = (x - 6)^2` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|490\|49 × 10\|49` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|1\|1^2 = 1\|perfect square` | discriminant_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|13\|13` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(60 + 75) / 2\|67.5` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|9` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|47\|34\|13` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|477 / 9\|53` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|48\|4` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|76\|5\|15.2` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|99` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|170 / 5\|34` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|positions 4 and 5\|60, 75` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|19` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|48\|4` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|18, 37, 51, 60, 75, 81, 97, 99` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|99 - 19\|80` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|72, 52, 51, 40, 73, 32, 77, 38, 42` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|72 + 52 + 51 + 40 + 73 + 32 + 77 + 38 + 42\|477` | statistics_generator.py |
| `SUBST` | 3 | `SUBST\|x\|-5\|2(-5)+5y+7` | evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, piecewise_evaluation_generator.py, recursive_explicit_generator.py, remainder_factor_theorem_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = y^3 + 2` | inverse_function_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|3x^3 - 14x^2 + 13x + 2\|r = 3` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|3` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|3, -5, -2, -4` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: -1x = 6` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with y only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = 4y + -21` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * -1, Eq2 * -1` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|2x + 4y = -52\|-3x - 4y = 58` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x - 4y = -21\|-5x + 0y = -15` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=6 into x = 4y + -21` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|g(-1)\|-4` | function_table_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|h(5)\|18` | function_evaluation_generator.py, normal_table_generator.py, pascal_triangle_generator.py |
| `THEOREM` | 2 | `THEOREM\|factor theorem\|x + 2 is a factor iff P(-2) = 0` | circle_angle_generator.py, geometric_mean_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|(-(5), (-4))\|(-5, -4)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (-y, x)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2 | `TRANSFORM_SETUP\|P(-4, 5)\|rotation 90° counterclockwise about the origin, then rotation 270° counterclockwise about the origin` | transformation_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|37\|48\|exterior` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|exterior = 37 + 48\|85` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|Exterior angle = sum of remote interior angles` | angle_relationships_generator.py |
| `TRY` | 2 | `TRY\|(1, -27)\|1·(-27)=-27, 1+(-27)=-26` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|9.0 hours\|6\|1.5 hours` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|2\|40` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|6\|kilometers\|9.0 hours` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|2,3,6,10\|40,60,120,200` | unit_rate_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√5 ≠ √6\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNROLL` | 2 | `UNROLL\|-1, -9, -17, -25\|arithmetic, d = -8` | recursive_explicit_generator.py |
| `VA` | 1 | `VA\|x = 2` | rational_function_features_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py |
| `VERTEX` | 1 | `VERTEX\|(-2, -1)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `VOLUME` | 1 | `VOLUME\|385` | volume_rect_prism_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 7 × 7\|24.5` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 3 × 11 × 6\|198` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = l × w × h` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|rectangular_prism\|l=3, w=11, h=6` | volume_3d_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, angle_relationships_generator.py, arc_sector_generator.py, arithmetic_sequence_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, completing_square_generator.py, complex_division_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conic_standard_form_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, dimensional_analysis_generator.py, discriminant_generator.py, distance_formula_generator.py, divisibility_classification_generator.py, domain_range_generator.py, ellipse_features_generator.py, equation_from_two_points_generator.py, error_spotting_generator.py, evaluate_expression_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, fill_in_step_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, gcf_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, integer_operations_generator.py, inverse_function_generator.py, lcm_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, long_division_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, monomial_mult_div_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, nets_surface_area_generator.py, normal_table_generator.py, number_comparison_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, pascal_triangle_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, point_slope_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, prime_factorization_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, round_solids_generator.py, scaling_generator.py, segment_partition_generator.py, sigma_notation_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplify_expression_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, statistics_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, unit_conversion_generator.py, unit_rate_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|(x + 6)(x - 5) = 0\|x + 6 = 0 or x - 5 = 0` | domain_range_generator.py, log_equation_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(507 - 505)/5\|0.40` | normal_table_generator.py |
