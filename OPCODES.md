# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

431 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 3 | `A\|27\|2\|29` | angle_measure_generator.py, arithmetic_sequence_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, distance_formula_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_characteristic_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exponential_model_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, nets_surface_area_generator.py, order_of_operations_generator.py, parabola_features_generator.py, pascal_triangle_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, pythag_hyp_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, round_solids_generator.py, segment_partition_generator.py, sigma_notation_generator.py, simple_stats_generator.py, standard_deviation_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|x + 9 = 17` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-2 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-4 < 0\|Absolute value cannot be negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|x + 9 > 10 -> x > 1` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|\|x + 9\| > 10` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for <` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|OR case\|x + 9 > 10 OR x + 9 < -10` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|\|x + 9\| = 17` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|x + 9 = 17\|x + 9 = -17` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|1\|1` | taxicab_geometry_generator.py |
| `AB_ADD_DGT` | 3 | `AB_ADD_DGT\|col_0\|0+1+0\|1` | abacus_addition_generator.py |
| `AB_CARRY` | 3 | `AB_CARRY\|col_1\|1\|col_2` | abacus_addition_generator.py |
| `AB_CARRY_FINAL` | 1 | `AB_CARRY_FINAL\|1` | abacus_addition_generator.py |
| `AB_INFO` | 1 | `AB_INFO\|Adding 4581 column by column` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 2 | `ACCEPT\|(-4, -8)\|product 32 ✓, sum -12 ✓` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|3 × 2\|6` | factor_trinomial_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|817.63\|148.87` | number_comparison_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(-5)\|5` | sinusoid_features_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|degrees = radians · 180/π` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|angle1 + angle2 = 180°` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|supplementary\|angle1 = 116°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|180 - 116\|64` | angle_relationships_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|-9x^2\|-3x^3` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate ∛26\|linearize f(x) = ∛x at a = 27` | linear_approx_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = (θ/360)·2πr` | arc_sector_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 4, central angle 120°\|sector area` | arc_sector_generator.py |
| `AREA` | 1, 3 | `AREA\|80` | geometry_area_perimeter_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 and y = 32 - x^2\|area between the curves` | area_between_curves_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = 3 ± 4(x - 3)` | hyperbola_features_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|22000 <= 10000\|no` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$3.75` | piecewise_evaluation_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|7\|current = 7` | composite_arithmetic_generator.py |
| `C` | 3 | `C\|3/2\|18\|27/18` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|x = 2` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CANCEL` | 2 | `CANCEL\|(x - 3)\|(x + 4)/(x - 7)` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1, ±2, ±3, ±6` | rational_root_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CBRT` | 2 | `CBRT\|8x^3\|2x` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CENTER` | 1 | `CENTER\|(4, -5)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_8(4) = log_2(4)/log_2(8)` | log_conversion_generator.py |
| `CHECK` | 3 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | area_between_curves_generator.py, arithmetic_sequence_generator.py, completing_square_generator.py, cramers_rule_generator.py, error_spotting_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, geometric_sequence_generator.py, horner_evaluation_generator.py, inverse_function_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_fractional_generator.py, log_equation_generator.py, long_division_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, power_series_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, recursive_explicit_generator.py, series_convergence_generator.py, similar_triangles_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, two_step_equation_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|22·0 + 10 = 10\|22·0 + 10 = 10` | special_solution_equation_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|inscribed angle 72°\|intercepted arc` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|radius = diameter / 2 = 8 / 2\|4.0` | circle_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|A = πr²` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|8\|diameter` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|A = π × 4.0²` | circle_generator.py |
| `CMP` | 3 | `CMP\|9/3\|2/3\|>` | fraction_comparison_generator.py, graph_interpret_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|817.63\|148.87\|>` | number_comparison_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|3, 13, 8, 17` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[2, -4], [-2, -1]]` | determinant_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|-9\|-2\|-11` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_X` | 3 | `COMB_X\|3x\|+4x\|7x` | derivative_product_quotient_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|2 - 7\|-5` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|-9/(-27)\|1/3` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of 10 = 5\|5^2 = 25` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|3\|47` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|area = length × width with mixed numbers\|convert, multiply, simplify` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|4x + 9 < 5 -> x < -1` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|12 < 3x - 3 < 18` | compound_inequality_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|x^2 = 12(y + 4)\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|-4 - 5i\|-4 + 5i` | complex_division_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 1/3 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 lb\|16 oz` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|2 lb\|32 oz` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|2\|1\|3` | decimal_mult_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|16·EF = 32·24` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 - 12x^2 + 36x + 1\|inflection point and concavity` | curve_analysis_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(-3 + 4i) + (-4 + 2i)\|add` | complex_division_generator.py, complex_number_ops_generator.py |
| `D` | 3 | `D\|632\|99\|6` | antiderivative_generator.py, arithmetic_sequence_generator.py, circle_angle_generator.py, circle_equation_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, decimal_div_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, function_operations_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, limit_evaluation_generator.py, linear_simple_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, nets_surface_area_generator.py, optimization_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, percent_problem_generator.py, polar_parametric_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, regular_polygon_area_generator.py, riemann_sum_generator.py, right_triangle_trig_generator.py, round_solids_generator.py, segment_partition_generator.py, series_convergence_generator.py, similar_triangles_generator.py, simple_probability_generator.py, sinusoid_features_generator.py, slope_two_points_generator.py, special_right_triangle_generator.py, standard_deviation_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|8+0+0\|->8 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|17.98\|23.20` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|7.5/1.0\|7.5/10\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|7-1 (borrow_in 0)\|->6 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|0.1\|1/10` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1\|100.00%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|7/10\|terminating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|7/10\|0.7` | repeating_decimal_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = deg den = 2\|y = 5/2` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = 3x^3 + x - 4x^(-1)\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = ad - bc` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|10\|-4\|16` | standard_deviation_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|y = -7` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|4\|-96\|100` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|100 > 0\|two real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|-3\|4x-1\|-12x+3` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|-3y + 15 = 12` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|-5x\|10x^3 - 10x^2 - 25x` | multiplying_polynomials_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|89\|2\|1` | divisibility_classification_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|-11\|7\|x=-11/7` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|75\|10` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|18y^4\|6y\|3y^3` | factor_gcf_generator.py, polynomial_long_division_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|denominator ≠ 0\|x + 6 ≠ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 0\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|cos θ = (u·v)/(‖u‖ · ‖v‖)` | dot_product_generator.py |
| `E` | 3 | `E\|27\|2\|729` | arc_sector_generator.py, circle_equation_generator.py, complex_division_generator.py, conic_standard_form_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, distance_formula_generator.py, ellipse_features_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, mean_value_theorem_generator.py, optimization_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, round_solids_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|2x = 3` | exponential_equation_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(2, 5)\|(6, -1)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 4 | `EQ_OP_BOTH\|divide\|7\|x\|6` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|subtract\|b\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|6` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 75/3` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|7x = 63` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|66013 × 11549 ≈ 70000 × 10000\|700000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|700000000\|762384137\|762384137 ≈ 700000000 ✓` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|χ = V - E + F` | euler_characteristic_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|0\|the torus has a hole: χ = 0, not 2` | euler_characteristic_generator.py |
| `EULER_SETUP` | 2 | `EULER_SETUP\|polyhedral torus grid: V = 20, E = 40, F = 20\|V - E + F` | euler_characteristic_generator.py |
| `EVAL` | 1, 2 | `EVAL\|p(-5)\|21` | arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|4 × 4 × 4 × 4` | exponent_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|4\|4\|16` | exponent_generator.py |
| `EXP_RULE_APPLY` | 4 | `EXP_RULE_APPLY\|add\|7\|8\|15` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|product_rule\|x^a · x^b = x^(a+b)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|y^7 · y^8` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|y^15` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|4\|4` | exponent_generator.py |
| `F` | 2 | `F\|9/9\|1` | composite_arithmetic_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|3x^2 + x\|x\|(3x + 1)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = 32\|m + n = -12` | factor_trinomial_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|107\|1\|0` | factors_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|107` | factors_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|-4` | parallel_perpendicular_line_generator.py |
| `FLAG` | 2 | `FLAG\|4\|11 × 5 = 55, not 65` | error_spotting_generator.py |
| `FOCUS` | 1 | `FOCUS\|(0, -1)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: 3 * 4\|12` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-i) * 4\|-4i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-i) * 7i\|-7i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: 3 * 7i\|21i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(5 + √15)(6 + √15)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|perfect_square_trinomial\|a^2 - 2ab + b^2 = (a - b)^2` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|24/14\|12/7` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|2/6\|0.3333333333` | fraction_decimal_percent_converter.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(p - q)(-5)\|p(-5) - q(-5)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|g(x) = -3x^2 - 3x + 1\|g(-9)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `GCD_RESULT` | 1 | `GCD_RESULT\|2` | lcm_generator.py |
| `GCD_START` | 2 | `GCD_START\|35\|61` | gcf_generator.py, lcm_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|35\|61\|35` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|18, 30, 24\|6` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|6y` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|y^4, y^2, y\|y` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude to hypotenuse; segments p = 2 (adjacent to the leg) and q = 8\|the leg adjacent to p` | geometric_mean_generator.py |
| `GOAL` | 1 | `GOAL\|Convert to Slope-Intercept Form (y = mx + b)` | point_slope_generator.py, standard_form_conversion_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|2018\|2019\|-4` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|line_graph\|Jan:21,Feb:18,Mar:13,Apr:19,May:27` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|max\|27` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|2018\|2019\|-4` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|min\|13` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Jan\|21` | graph_interpret_generator.py |
| `GROUP` | 2 | `GROUP\|(3x^2 + x)\|(6x + 2)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `HA` | 1 | `HA\|y = 5/2` | rational_function_features_generator.py |
| `HOLE` | 1 | `HOLE\|x = -5` | rational_function_features_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|-3x^3 - x^2 - x - 4\|x = 3` | horner_evaluation_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|diagonal = s·√n` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|3-cube with side 2\|main diagonal` | hypercube_counting_generator.py |
| `I` | 2 | `I\|3/2\|2/3` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: sin^2 θ = (1 - cos θ)(1 + cos θ)\|transform the right side` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1 | `IDENT_SUB\|1 - cos^2 θ = sin^2 θ` | parametric_calculus_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of xy\|y + x·y' (product rule)` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|xy = 12\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|75/14\|5 5/14` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Dividing by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|add\|2\|-3 <= 3x <= 7` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|divide\|-5\|x\|-9` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|<\|-9` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|-5x > 45` | linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|x/-5 < 5` | domain_range_generator.py, two_step_inequality_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|power rule\|∫ x^n dx = x^(n+1)/(n+1) + C` | antiderivative_generator.py, definite_integral_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ (-9x^2 + 8x) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|-5\|5` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|9\|negative\|-9` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|+\|5\|4\|9` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|-5 - 4\|-5 + (-4)` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|subtract_rule\|Subtracting is adding the opposite` | integer_operations_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 - 3x - 3 on [-2, 1]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^3\|-i` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|-7i^2\|7` | complex_division_generator.py, complex_number_ops_generator.py |
| `L` | 3 | `L\|2\|9\|18` | fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|54*50\|2\|1350` | lcm_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→5 of (x^2 - 6x + 5)/(x - 5)\|0/0: factor and cancel` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|parallel\|y = -4x + 8\|(5, 7)` | parallel_perpendicular_line_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|ln(e^(4x)) = ln(13)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|b^y = x ⟺ log_b(x) = y` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|e^(ln x) = x (inverse functions)\|17` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|2x + 6 = x + 4` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|log_5(x^4)\|4log_5(x)` | log_diff_higher_order_generator.py, log_properties_generator.py |
| `LOG_PRODUCT` | 2 | `LOG_PRODUCT\|log_5(25x)\|log_5(25) + log_5(x)` | log_equation_generator.py, log_properties_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_5(25x/y)\|log_5(25x) - log_5(y)` | log_properties_generator.py |
| `LOG_SETUP` | 2 | `LOG_SETUP\|log_5(25x/y)\|expand` | log_properties_generator.py |
| `M` | 2, 3 | `M\|6\|99\|594` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_sequence_generator.py, chain_rule_generator.py, circle_angle_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, decimal_div_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, dot_product_generator.py, error_spotting_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hypercube_counting_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, multi_step_unit_conversion_generator.py, nets_surface_area_generator.py, optimization_generator.py, order_of_operations_generator.py, parametric_calculus_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, right_triangle_trig_generator.py, round_solids_generator.py, row_reduction_generator.py, segment_partition_generator.py, similar_triangles_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2)` | vector_ops_generator.py |
| `MAT_ENTRY` | 2 | `MAT_ENTRY\|(1,1)\|3` | matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[1, -4], [2, -5]]\|3A` | determinant_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py |
| `MAX` | 2 | `MAX\|1, 15\|15` | taxicab_geometry_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|79\|9\|8.777777777777779` | composite_arithmetic_generator.py, five_number_summary_generator.py, simple_stats_generator.py, standard_deviation_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|9\|15` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEDIAN_PICK` | 2, 3 | `MEDIAN_PICK\|5\|\|5` | five_number_summary_generator.py, simple_stats_generator.py |
| `METRIC` | 2 | `METRIC\|taxicab vs Chebyshev\|sum of absolute differences vs their max` | taxicab_geometry_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = 2` | sinusoid_features_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|5 9/10\|59/10` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MODE` | 2 | `MODE\|2\|8` | simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = Pe^(rt)` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 1500e^0.16` | exponential_model_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|3\|1` | simple_stats_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^6 * x^8 = x^(6+8)\|x^14` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|7 / 1\|7` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|7 * -4\|-28` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(7x^6)(-4x^8)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^2 / x^2 = x^(2-2)\|x^0 = 1` | monomial_mult_div_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|-4x\|left\|3x+2+4x = -9` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|12\|(1/3)x\|4x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 + 3x - 6 on [-4, 2]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `NCR` | 2 | `NCR\|C(6,1)\|6` | hypercube_counting_generator.py |
| `NEED` | 2 | `NEED\|line 3 shows 9x = -63\|line 5 shows x = -7` | fill_in_step_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|6 squares 12 by 12\|total surface area` | nets_surface_area_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = -4\|Parallel lines have the same slope` | parallel_perpendicular_line_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(7)\|-1/7` | tangent_line_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|X ~ N(40, 6)\|P(X < 52.6)` | normal_table_generator.py |
| `ODE_SETUP` | 2 | `ODE_SETUP\|dy/dt = 3y, y(0) = 2\|solve` | euler_method_generator.py, logistic_growth_generator.py, separable_ode_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|184 m of fence, barn forms the fourth side; sides x, x, and 184 - 2x\|maximize area` | optimization_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|4x + 29 = 6x - 1` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|alternate_exterior\|Alternate exterior angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-2x = -30\|x = 15` | angle_relationships_generator.py |
| `PARAM_SETUP` | 2 | `PARAM_SETUP\|x = 9 cos t, y = 9 sin t\|eliminate t` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|(x + 3)/(x - 2)^2 = A/(x - 2) + B/(x - 2)^2` | partial_fractions_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = ln(x), dv = -1 dx\|du = dx/x, v = -x` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|9C5` | pascal_triangle_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|0.9\|40\|36` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|90%\|0.9` | composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, fraction_decimal_percent_converter.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, tip_bill_split_generator.py |
| `PERIM` | 1 | `PERIM\|32` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|180°` | sinusoid_features_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|17` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|102\|2\|51` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|10° left` | sinusoid_features_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Pizza\|3` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|●\|10` | graph_interpret_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|4060686\|3\|4060.686` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 2 | `PLACE_DP_Q\|75\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|x = ±10\|x = 10 or x = -10` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 5 = -3/2(x - 2)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|x = r cos θ, y = r sin θ` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2 | `POLAR_SETUP\|(r, θ) = (4, 210°)\|rectangular coordinates` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|2y^3 + 14y^2 + 24y + 23\|y + 5` | polynomial_long_division_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|9x^3 + 3x^2 - 10x` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(16x^4 + 8x^4 + 32x^2 + 32x) / (8x)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(16x^4) / (8x) + (8x^4) / (8x) + (32x^2) / (8x) + (32x) / (8x)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(9x^3) + (3x^2) + (-1x -9x)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(-5x + 1)(-2x^2 + 2x + 5)` | multiplying_polynomials_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(-x) + (9x^3 + 3x^2 - 9x)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2 | `POLY_SUB\|(2y^3 + 14y^2) - (2y^3 + 10y^2)\|4y^2` | polynomial_long_division_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|3x^3\|9x^2` | chain_rule_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `PRIME` | 1 | `PRIME\|89` | divisibility_classification_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(blue\|first was red)\|3/8` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Coin flip and die roll, looking for tails and 4` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(tails)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Coin flip and die roll are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/6\|1/12` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|2\|4` | simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | *(not observed in sampling)* | compound_probability_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|15/3 = x/5` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|d² = 2500 - 1600 = 900\|900` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 2 | `PYTHAG_CONTEXT\|ladder\|ladder=50ft, given=40ft` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|ground=30\|wall=40\|ladder=50` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|1764\|42` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 3 | `PYTHAG_SETUP\|c=58\|a=40\|b=?` | pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 3364 - 1600\|1764` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|40\|1600` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|40² + b² = 58²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|-2\|10\|4\|2` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|-2\|10\|4\|-3` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|150°\|quadrant II` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|6,8,15,15,20,21,22\|15` | five_number_summary_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|conical tank, radius = height/2; water in at dV/dt = 3 m³/min; depth h = 4 m\|dh/dt` | related_rates_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|√7/√7` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|30:33\|3\|10:11` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Red (liters): 30, 60, 100, ?\|Blue (liters): 33, 66, 110, 121` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 60 / 0.4` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|41/40` | trig_six_functions_generator.py |
| `REJECT` | 2 | `REJECT\|(-1, -32)\|sum is -33, need -12` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `REWRITE` | 1 | `REWRITE\|8 + 90` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, chain_rule_generator.py, circle_equation_generator.py, completing_square_generator.py, complex_division_generator.py, complex_number_ops_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, evaluate_expression_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logistic_growth_generator.py, matrix_inverse_generator.py, midpoint_generator.py, normal_table_generator.py, optimization_generator.py, order_of_operations_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, quadratic_factoring_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, series_convergence_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py |
| `RIEMANN_SETUP` | 2 | `RIEMANN_SETUP\|f(x) = 4x + 4 on [2, 10], n = 4\|right Riemann sum` | riemann_sum_generator.py |
| `ROOT` | 2 | `ROOT\|15129\|123` | completing_square_generator.py, factor_special_forms_generator.py, pythag_hyp_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, round_solids_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|9` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|81\|perfect_square\|9` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|√81` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1 | `ROOT_SIMPLIFY\|4√5` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|68867\|100\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|68867\|68900` | place_value_rounding_generator.py |
| `ROW_OP` | 2 | `ROW_OP\|R2 → R2 - 3·R1\|[0, 1, -2]` | row_reduction_generator.py |
| `S` | 3 | `S\|632\|594\|38` | angle_measure_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, circle_angle_generator.py, circle_equation_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, determinant_generator.py, distance_formula_generator.py, ellipse_features_generator.py, euler_characteristic_generator.py, euler_method_generator.py, exponential_model_generator.py, five_number_summary_generator.py, fraction_op_generator.py, function_operations_generator.py, geometric_sequence_generator.py, graph_interpret_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, linear_simple_generator.py, logistic_growth_generator.py, long_division_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, normal_table_generator.py, optimization_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, related_rates_generator.py, riemann_sum_generator.py, row_reduction_generator.py, segment_partition_generator.py, series_convergence_generator.py, slope_two_points_generator.py, solid_revolution_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py, vector_ops_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(2)² = 2π × 4\|8π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|3 × 5\|15` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 2 × 15\|60π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=3, w=5, h=6` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(15 + 18 + 30)\|126` | round_solids_generator.py, volume_3d_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|80\|20\|4.0` | scaling_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|3 inches\|actual_dimension` | scaling_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|3\|12\|36` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 inch\|12 feet\|12` | scaling_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|9.8\|-3` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|left\|3` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|divide_coefficients\|8.0\|2.0\|4.0` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|(8.0 × 10^8) ÷ (2.0 × 10^3)` | exponent_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f'' < 0 for x < 4, f'' > 0 for x > 4\|concavity changes` | curve_analysis_generator.py, optimization_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(6, 0), B(-3, -6); ratio 1:2 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (θ/360)·πr^2` | arc_sector_generator.py |
| `SELECT_RELEVANT` | 2 | `SELECT_RELEVANT\|base = 99, rate = 25%\|ignore 32 (irrelevant)` | percent_word_problem_generator.py |
| `SEPARATE` | 1 | `SEPARATE\|dy/y = 3 dt` | separable_ode_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|a_14 = 7 + (14 - 1)·-5` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|7, 2, -3, -8, ...\|sum of first 14 terms` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ n/(n^2 + 1), n ≥ 1\|converge or diverge?` | power_series_generator.py, series_convergence_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|60 = 0.4 * whole` | percent_problem_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|1 + 2 + 4 + 8` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=0)^(3) 2^k\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=0\|2^0\|1` | sigma_notation_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|tan, quadrant I\|positive` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|6\|3\|18` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|27\|9\|3` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|parallelogram\|6,9\|27 (others unknown)` | scaling_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; AB = 16, DE = 32, BC = 24\|find EF` | similar_triangles_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = -5cos(2x + 20°) + 2\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|3` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = 3x + 1` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|-3/2` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(-9, -5)\|(3, 6)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (6 - (-5)) / (3 - (-9))` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|sin x = 0\|0°, 180°` | trig_equation_generator.py |
| `SORT` | 2 | `SORT\|14,1,4,9,8,18,5,13,7\|1,4,5,7,8,9,13,14,18` | five_number_summary_generator.py, simple_stats_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|10 = 10\|identity: true for every x` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|7x = x + 6x\|3x^2 + x + 6x + 2` | factor_trinomial_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|x^2 = 100\|x = ±10` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-100)\|10i` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(3x + 73) = 8\|3x + 73 = 64` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|40\|4 × 10\|4` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|100\|10^2 = 100\|perfect square` | discriminant_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|-6\|6` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(27 + 60) / 2\|43.5` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|6` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|34\|40\|-6` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|288 / 6\|48` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|18\|1` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|32\|7\|4.57` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|91` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|280 / 7\|40` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|positions 5 and 6\|27, 60` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|15` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|51\|3` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|13, 23, 25, 26, 27, 60, 71, 73, 86, 90` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|91 - 15\|76` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|69, 11, 72, 41, 54, 41` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|69 + 11 + 72 + 41 + 54 + 41\|288` | statistics_generator.py |
| `SUBST` | 3 | `SUBST\|x\|0\|-5(0)+y-7` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = (y - 4)/4` | inverse_function_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|3x^3 + 13x^2 + 8x + 17\|r = -4` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|3` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|3, 1, 4, 1` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: 10y = 60` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with x only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = -1y + 3` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * -1` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|4x + 5y = 54\|-4x + 5y = 6` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x + 1y = 3\|5x + 2y = 12` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=1 into x = -1y + 3` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|h(-3)\|1` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|f(4)\|27` | dot_product_generator.py, function_evaluation_generator.py, normal_table_generator.py, pascal_triangle_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = e^x, P_4 around 0\|bound the error at x = 2/3` | taylor_series_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|limit comparison\|behaves like Σ 1/n` | power_series_generator.py, series_convergence_generator.py |
| `THEOREM` | 2 | `THEOREM\|remainder theorem\|remainder on division by x + 3 is P(-3)` | circle_angle_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|((-4) - 4, (7) + 6)\|(-8, 13)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (x - 4, y + 6)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2 | `TRANSFORM_SETUP\|P(-4, 7)\|translation by (-4, 6)` | transformation_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|sin\|opposite/hypotenuse` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle: leg opposite A = 6, leg adjacent to A = 8, hypotenuse = 10\|sin A` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|63\|48\|x` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|x = 180 - 63 - 48\|69` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|63 + 48 + x = 180` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|30-60-90 triangle, longer leg = 5√3\|shorter leg and hypotenuse` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRY` | 2 | `TRY\|(-1, -32)\|(-1)·(-32)=32, (-1)+(-32)=-33` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|180°\|(-1, 0)` | unit_circle_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|$10.00\|4\|$2.50` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|5\|15` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|4\|liters\|$10.00` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|5,6,9\|15,18,27` | unit_rate_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√7 ≠ √11\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNROLL` | 2 | `UNROLL\|9, 14, 19, 24\|arithmetic, d = 5` | recursive_explicit_generator.py |
| `VA` | 1 | `VA\|x = -4` | rational_function_features_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|v = ⟨-18, 24⟩\|unit vector` | dot_product_generator.py, vector_ops_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py |
| `VERTEX` | 1 | `VERTEX\|(0, -4)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `VOLUME` | 1 | `VOLUME\|385` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|base: region under y = 2 - x on [0, 2]; cross-sections perpendicular to the x-axis are squares\|cross-section method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 6 × 10\|30.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 12 × 9 × 10\|1080` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = l × w × h` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|rectangular_prism\|l=12, w=9, h=10` | volume_3d_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, angle_measure_generator.py, angle_relationships_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, chain_rule_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, completing_square_generator.py, complex_division_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, discriminant_generator.py, distance_formula_generator.py, divisibility_classification_generator.py, domain_range_generator.py, dot_product_generator.py, ellipse_features_generator.py, equation_from_two_points_generator.py, error_spotting_generator.py, euler_characteristic_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, gcf_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, implicit_diff_generator.py, improper_integral_generator.py, integer_operations_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, lcm_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logistic_growth_generator.py, long_division_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, monomial_mult_div_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, nets_surface_area_generator.py, normal_table_generator.py, number_comparison_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, optimization_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, pascal_triangle_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, point_slope_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, power_series_generator.py, prime_factorization_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, riemann_sum_generator.py, right_triangle_trig_generator.py, round_solids_generator.py, row_reduction_generator.py, scaling_generator.py, segment_partition_generator.py, separable_ode_generator.py, series_convergence_generator.py, sigma_notation_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, statistics_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, u_substitution_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, vector_ops_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|(x + 6)(x - 2) = 0\|x + 6 = 0 or x - 2 = 0` | area_between_curves_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(52.6 - 40)/6\|2.10` | normal_table_generator.py |

## Warnings: unresolved dynamic op-codes

These step() call sites pass a non-literal op-code that the scanner could not resolve; their codes may be missing from the table above:

- trig_identity_verify_generator.py:115
- trig_identity_verify_generator.py:117
