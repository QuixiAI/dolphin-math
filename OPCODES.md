# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

609 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 3 | `A\|27\|2\|29` | angle_measure_generator.py, arithmetic_sequence_generator.py, base_conversion_generator.py, binomial_probability_generator.py, calendar_arithmetic_generator.py, chi_square_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, distance_formula_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_characteristic_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, five_number_summary_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, manual_square_root_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, modular_arithmetic_generator.py, nets_surface_area_generator.py, order_of_operations_generator.py, parabola_features_generator.py, pascal_triangle_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, probability_addition_rule_generator.py, pythag_hyp_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, regression_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, round_solids_generator.py, segment_partition_generator.py, sigma_notation_generator.py, simple_stats_generator.py, standard_deviation_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py, z_score_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|x - 8 = 5` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-9 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-5 < 0\|Absolute value is always non-negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|3x - 9 >= 6 -> x >= 5` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|\|x - 4\| <= 7` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for <` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|AND case\|-7 <= x - 4 <= 7` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|\|x - 8\| = 5` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|x - 8 = 5\|x - 8 = -5` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|8\|8` | taxicab_geometry_generator.py |
| `AB_ADD_DGT` | 3 | `AB_ADD_DGT\|col_0\|0+1+0\|1` | abacus_addition_generator.py |
| `AB_CARRY` | 3 | `AB_CARRY\|col_1\|1\|col_2` | abacus_addition_generator.py |
| `AB_CARRY_FINAL` | 1 | `AB_CARRY_FINAL\|1` | abacus_addition_generator.py |
| `AB_INFO` | 1 | `AB_INFO\|Adding 4581 column by column` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 2 | `ACCEPT\|(-1, -6)\|product 6 ✓, sum -7 ✓` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|9 × 4\|36` | factor_trinomial_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_FORMULA` | 1 | `ADD_FORMULA\|P(A ∪ B) = P(A) + P(B) - P(A ∩ B)` | probability_addition_rule_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ADD_SETUP` | 2 | `ADD_SETUP\|P(A) = 16/20, P(B) = 3/20, P(A ∩ B) = 3/20\|P(A ∪ B)` | probability_addition_rule_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|817.63\|148.87` | number_comparison_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(-1)\|1` | sinusoid_features_generator.py |
| `ANGLE_EVAL` | 2 | `ANGLE_EVAL\|theta=0..2*pi\|2*pi` | triple_integral_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|radians = degrees · π/180` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|7x + 55 = 90` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|complementary\|(2x + 15)° + (5x + 40)° = 90°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|7x = 35\|x = 5` | angle_relationships_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|8x^3\|2x^4` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate √84\|linearize f(x) = √x at a = 81` | linear_approx_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = (θ/360)·2πr` | arc_sector_generator.py |
| `ARC_LENGTH` | 3 | `ARC_LENGTH\|int_0^T speed dt\|17*4\|68` | curve_geometry_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 5, central angle 60°\|sector area` | arc_sector_generator.py |
| `AREA` | 1, 3 | `AREA\|80` | geometry_area_perimeter_generator.py |
| `AREA_INT` | 3 | `AREA_INT\|A = int y dx\|2*6^2/2\|36` | centroid_generator.py |
| `AREA_SCALE` | 3 | `AREA_SCALE\|uv rectangle area\|8*6\|48` | jacobian_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 and y = 2x + 8\|area between the curves` | area_between_curves_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = 1 ± (15/8)(x - 3)` | hyperbola_features_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BASE_ADD_COL` | 3 | `BASE_ADD_COL\|col 0\|B + 1 + carry 0\|12 -> digit C, carry 0` | base_arithmetic_generator.py |
| `BASE_ARITH_SETUP` | 2 | `BASE_ARITH_SETUP\|base 16\|4FE * 9` | base_arithmetic_generator.py |
| `BASE_CARRY` | 2 | `BASE_CARRY\|carry 2\|digit 2, carry 0` | base_arithmetic_generator.py |
| `BASE_MUL_COL` | 3 | `BASE_MUL_COL\|col 0\|E * 9 + carry 0\|126 -> digit E, carry 7` | base_arithmetic_generator.py |
| `BASE_SETUP` | 2 | `BASE_SETUP\|11101101_2\|decimal` | base_conversion_generator.py |
| `BAYES_CELL` | 3 | `BAYES_CELL\|true positive\|20 * 4/5\|16` | conditional_probability_generator.py |
| `BAYES_FORMULA` | 1 | `BAYES_FORMULA\|P(disease=no given negative) = TN/(TN + FN)` | conditional_probability_generator.py |
| `BAYES_SETUP` | 3 | `BAYES_SETUP\|disease=yes 20, disease=no 100\|sensitivity 4/5, specificity 9/10\|P(disease=no given test negative)` | conditional_probability_generator.py |
| `BINOM_FORMULA` | 1 | `BINOM_FORMULA\|P(X ≥ 1) = 1 - (1-p)^n` | binomial_probability_generator.py |
| `BINOM_SETUP` | 2 | `BINOM_SETUP\|n = 3, p = 2/5\|P(X ≥ 1)` | binomial_probability_generator.py |
| `BIT_ROW` | 2, 3 | `BIT_ROW\|bit 0\|0 XOR 1\|1` | bitwise_ops_generator.py |
| `BIT_RULE` | 2 | `BIT_RULE\|XOR\|1 when exactly one bit is 1` | bitwise_ops_generator.py |
| `BIT_SETUP` | 2 | `BIT_SETUP\|0010 XOR 0111\|4-bit mask` | bitwise_ops_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|0 < 1\|yes` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$3.75` | piecewise_evaluation_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|group 69\|current = 69` | composite_arithmetic_generator.py, manual_square_root_generator.py |
| `C` | 3 | `C\|3/2\|18\|27/18` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|x = 2` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CAL_DIVMOD` | 3 | `CAL_DIVMOD\|111\|7\|15 R6` | calendar_arithmetic_generator.py |
| `CAL_SETUP` | 3 | `CAL_SETUP\|2027-08-20\|Friday, offset 76 days\|weekday` | calendar_arithmetic_generator.py |
| `CANCEL` | 2 | `CANCEL\|6x\|9x + 1` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py, trig_identity_verify_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1, ±5` | rational_root_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CBRT` | 2 | `CBRT\|64n^3\|4n` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CEIL` | 2 | `CEIL\|34.4064\|35` | confidence_interval_generator.py |
| `CENTER` | 1 | `CENTER\|(-5, 6)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py |
| `CENTROID_COORD` | 3 | `CENTROID_COORD\|xbar = M_y/A\|(144)/(36)\|4` | centroid_generator.py |
| `CENTROID_SETUP` | 3 | `CENTROID_SETUP\|0 <= y <= 2*x\|0 <= x <= 6\|centroid` | centroid_generator.py |
| `CHAIN_RATE` | 2 | `CHAIN_RATE\|dx/dt\|1` | multivar_chain_rule_generator.py |
| `CHAIN_SUM` | 3 | `CHAIN_SUM\|f_x*dx/dt + f_y*dy/dt\|1*1 + 18*(-2)\|-35` | multivar_chain_rule_generator.py |
| `CHAIN_VALUE` | 3 | `CHAIN_VALUE\|x(-3)\|(-3) + 3\|0` | multivar_chain_rule_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_25(125) = log_5(125)/log_5(25)` | log_conversion_generator.py |
| `CHAR_DIAG` | 2 | `CHAR_DIAG\|diagonal of λI - A\|(λ + 1), (λ + 3)` | eigenvalue_generator.py |
| `CHAR_POLY` | 2 | `CHAR_POLY\|p(λ) = λ^2 + 4λ + 3\|(λ + 3)*(λ + 1)` | eigenvalue_generator.py |
| `CHAR_SETUP` | 2 | `CHAR_SETUP\|p(λ) = det(λI - A)\|triangular determinant` | eigenvalue_generator.py |
| `CHECK` | 2, 3 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | area_between_curves_generator.py, arithmetic_sequence_generator.py, base_arithmetic_generator.py, bitwise_ops_generator.py, chi_square_generator.py, completing_square_generator.py, conditional_probability_generator.py, cramers_rule_generator.py, eigenvalue_generator.py, error_spotting_generator.py, expected_value_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, gradient_generator.py, hessian_classify_generator.py, horner_evaluation_generator.py, hypothesis_test_generator.py, inverse_function_generator.py, lagrange_multiplier_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_fractional_generator.py, log_equation_generator.py, long_division_generator.py, lu_decomposition_generator.py, manual_square_root_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, modular_arithmetic_generator.py, partial_derivative_generator.py, power_series_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, recursive_explicit_generator.py, series_convergence_generator.py, similar_triangles_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, two_step_equation_generator.py, z_score_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|5·0 + 0 = 0\|5·0 + 0 = 0` | special_solution_equation_generator.py |
| `CHI_FORMULA` | 1 | `CHI_FORMULA\|E = (row·col)/N; χ² = Σ (O - E)^2/E` | chi_square_generator.py |
| `CHI_SETUP` | 2 | `CHI_SETUP\|row 1: 44, 6; row 2: 6, 44; N = 100\|independence; df = 1, critical value = 3.841` | chi_square_generator.py |
| `CHI_TERM` | 3 | `CHI_TERM\|44 - 25 = 19\|19^2 = 361\|361/25 = 14.44` | chi_square_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|inscribed angle 71°\|intercepted arc` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|C = 18π\|18π` | circle_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|C = πd` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|18\|diameter` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|C = π × 18` | circle_generator.py |
| `CIRCULATION_SUM` | 2 | `CIRCULATION_SUM\|(-3)*10^2*pi\|-300*pi` | vector_theorem_generator.py |
| `CI_FORMULA` | 1 | `CI_FORMULA\|x̄ ± E` | confidence_interval_generator.py |
| `CI_SETUP` | 2 | `CI_SETUP\|p̂ = 0.5, n = 25, z* = 1.28\|margin of error` | confidence_interval_generator.py |
| `CMP` | 3 | `CMP\|9/3\|2/3\|>` | fraction_comparison_generator.py, graph_interpret_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|817.63\|148.87\|>` | number_comparison_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|1, 2, -3, 29` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[-2, -2], [-3, -4]]` | determinant_generator.py |
| `COL_BASIS` | 2 | `COL_BASIS\|original columns 1, 2\|[[4, -3, 7], [-1, 1, -3]]` | subspace_basis_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|-5\|+9\|4` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_FORMULA` | 1 | `COMB_FORMULA\|C(n, r) = P(n, r)/r!` | permutation_combination_generator.py |
| `COMB_SETUP` | 2 | `COMB_SETUP\|C(14, 2)\|n!/(r!·(n-r)!)` | permutation_combination_generator.py |
| `COMB_X` | 3 | `COMB_X\|-2x\|-2x\|-4x` | derivative_product_quotient_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|-10 - (-8)\|-2` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|6/2\|3` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of 10 = 5\|5^2 = 25` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|3\|47` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|area = length × width with mixed numbers\|convert, multiply, simplify` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|2x - 3 < -7 -> x < -2` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|-23 < 4x - 7 < -7` | compound_inequality_generator.py |
| `COND_COUNT` | 2 | `COND_COUNT\|club=yes and commute=bus\|18` | conditional_probability_generator.py |
| `COND_FORMULA` | 1 | `COND_FORMULA\|P(A given B) = count(A and B)/count(B)` | conditional_probability_generator.py |
| `COND_SETUP` | 2 | `COND_SETUP\|yes/bike 16, no/bike 21, yes/bus 18, no/bus 24\|P(club=yes given commute=bus)` | conditional_probability_generator.py |
| `COND_TOTAL` | 2 | `COND_TOTAL\|commute=bus total\|18 + 24 = 42` | conditional_probability_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|(y - 5)^2 = 20x\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|6 + 4i\|6 - 4i` | complex_division_generator.py |
| `CONSTRAINT_SUBST` | 3 | `CONSTRAINT_SUBST\|x + y = 20\|x = 2*20/5\|8` | lagrange_multiplier_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 1/4 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 lb\|16 oz` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|2 lb\|32 oz` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `CORR_FORMULA` | 1 | `CORR_FORMULA\|r = Sxy/√(Sxx·Syy)` | regression_generator.py |
| `COUNT` | 2 | `COUNT\|A = [4, 5, 6]\|3/6` | probability_addition_rule_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|2\|1\|3` | decimal_mult_generator.py |
| `CRIT_EQS` | 2 | `CRIT_EQS\|f_x = 0\|10*x - 3*y + 19 = 0` | hessian_classify_generator.py |
| `CRIT_SOLVE` | 3 | `CRIT_SOLVE\|det\|10*(-4) - (-3)^2\|-49` | hessian_classify_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|27·BC = 12·27` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CURL_COMPONENT` | 3 | `CURL_COMPONENT\|i\|-2 - 0\|-2` | div_curl_generator.py |
| `CURVATURE_FORMULA` | 2 | `CURVATURE_FORMULA\|circle\|kappa = 1/R` | curve_geometry_generator.py |
| `CURVE_GEOM_SETUP` | 3 | `CURVE_GEOM_SETUP\|r(t) = <8*t + 4, -15*t + 3>\|0 <= t <= 4\|arc length` | curve_geometry_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 - 9x^2 + 24x - 5\|critical points and their nature` | curve_analysis_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(7 - 3i) - (3 + i)\|subtract` | complex_division_generator.py, complex_number_ops_generator.py |
| `CYL_BOUNDS` | 2 | `CYL_BOUNDS\|z\|0..11` | triple_integral_generator.py |
| `CYL_CONVERT` | 2 | `CYL_CONVERT\|5*z dV\|5*z*r dz dr dtheta` | triple_integral_generator.py |
| `D` | 3 | `D\|632\|99\|6` | antiderivative_generator.py, arithmetic_sequence_generator.py, circle_angle_generator.py, circle_equation_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, decimal_div_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, function_operations_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, hypothesis_test_generator.py, kinematics_generator.py, limit_evaluation_generator.py, linear_simple_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, manual_square_root_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, nets_surface_area_generator.py, optimization_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, percent_problem_generator.py, permutation_combination_generator.py, physics_formula_generator.py, polar_parametric_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, regression_generator.py, regular_polygon_area_generator.py, riemann_sum_generator.py, right_triangle_trig_generator.py, round_solids_generator.py, segment_partition_generator.py, series_convergence_generator.py, similar_triangles_generator.py, simple_probability_generator.py, sinusoid_features_generator.py, slope_two_points_generator.py, special_right_triangle_generator.py, standard_deviation_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py, z_score_generator.py |
| `DATE_ORDINAL` | 2 | `DATE_ORDINAL\|2024-02-24\|738940` | calendar_arithmetic_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|8+0+0\|->8 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|17.98\|23.20` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|7.5/1.0\|7.5/10\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|7-1 (borrow_in 0)\|->6 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|0.1\|1/10` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1\|100.00%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|7/10\|terminating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|7/10\|0.7` | repeating_decimal_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = deg den = 2\|y = 1/1` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, multivar_chain_rule_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = 3x^2 - 4x + x^(-2)\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = a11·M11 - a12·M12 + a13·M13` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|24\|3\|9` | standard_deviation_generator.py |
| `DIFF_SETUP` | 3 | `DIFF_SETUP\|f(x,y) = 3*x^2 + 2*y^2 - 2*x*y - 3*x + y\|point (1, 3)\|dx=-1/4, dy=-1/2` | multivar_chain_rule_generator.py |
| `DIFF_SUM` | 3 | `DIFF_SUM\|f_x*dx + f_y*dy\|(-3)*(-1/4) + 11*(-1/2)\|-4.75` | multivar_chain_rule_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|x = -5` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|144\|80\|64` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|88 > 0\|two real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|3\|3x-4\|9x-12` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|7y + -24 = 46` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|-2x\|8x^3 + 4x^2 + 4x` | multiplying_polynomials_generator.py |
| `DIVMOD` | 4 | `DIVMOD\|149\|2\|74\|r=1` | base_conversion_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|89\|2\|1` | divisibility_classification_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|4\|-4\|x=-1` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|75\|10` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_SUM` | 3 | `DIV_SUM\|P_x + Q_y + R_z\|-1 + 4 + 2\|5` | div_curl_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|45x^4\|5\|9x^4` | factor_gcf_generator.py, polynomial_long_division_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|radicand ≥ 0\|x + 1 ≥ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 2\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, probability_addition_rule_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOT` | 2, 3 | `DOT\|(15, 33) · (0, 1)\|15*0 + 33*1\|33` | gradient_generator.py, line_integral_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|u·v = x1·x2 + y1·y2` | dot_product_generator.py |
| `DOUBLE_SETUP` | 2, 3 | `DOUBLE_SETUP\|integrand x^2 + y^2\|upper-half disk radius 6` | double_integral_generator.py |
| `E` | 3 | `E\|14\|2\|196` | arc_sector_generator.py, circle_equation_generator.py, complex_division_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, distance_formula_generator.py, ellipse_features_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, finance_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, mean_value_theorem_generator.py, optimization_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, round_solids_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EIGENVALUE` | 2 | `EIGENVALUE\|λ = -3\|p(-3) = 0` | eigenvalue_generator.py |
| `EIGENVECTOR` | 2 | `EIGENVECTOR\|A + 3I times v = 0\|[3, -2]` | eigenvalue_generator.py |
| `EIGEN_MATRIX` | 2 | `EIGEN_MATRIX\|A + 3I\|[[2, 3], [0, 0]]` | eigenvalue_generator.py |
| `ELIMINATE_LAMBDA` | 2 | `ELIMINATE_LAMBDA\|f_x = f_y\|2*y = 3*x` | lagrange_multiplier_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|2x = 5` | exponential_equation_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(-7, 1)\|(-4, 1)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 4 | `EQ_OP_BOTH\|subtract\|1\|x\|6` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|multiply\|s\|to both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|6` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 36/2` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|2x = -6` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|24742 × 23211 ≈ 20000 × 20000\|400000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|4.7 × 10^6\|4680000\|rounded estimate` | fermi_estimation_generator.py, long_division_generator.py, multi_digit_multiplication_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|χ = V - E + F` | euler_characteristic_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|0\|the torus has a hole: χ = 0, not 2` | euler_characteristic_generator.py |
| `EULER_SETUP` | 2 | `EULER_SETUP\|polyhedral torus grid: V = 30, E = 60, F = 30\|V - E + F` | euler_characteristic_generator.py |
| `EVAL` | 1, 2, 3 | `EVAL\|p(3)\|-18` | arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, lagrange_multiplier_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EVAL_PARTIAL` | 3 | `EVAL_PARTIAL\|f_x\|4*1 - 4*2 - 3\|-7` | gradient_generator.py, multivar_chain_rule_generator.py |
| `EV_FORMULA` | 1 | `EV_FORMULA\|E[X] = Σ x·P(x)` | expected_value_generator.py |
| `EV_SETUP` | 2 | `EV_SETUP\|P(win $11) = 1/2; P(win $5) = 1/4; P(win $2) = 1/4\|fair? cost = $5` | expected_value_generator.py |
| `EXP_CELL` | 2 | `EXP_CELL\|(50·50)/100\|25` | chi_square_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|(-3) × (-3) × (-3)` | exponent_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|-3\|-3\|9` | exponent_generator.py |
| `EXP_RULE_APPLY` | 4 | `EXP_RULE_APPLY\|add\|5\|4\|9` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|zero_exponent\|x^0 = 1 (for x ≠ 0)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|(2x)^0` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|1` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|-3\|3` | exponent_generator.py |
| `F` | 2 | `F\|9/9\|1` | composite_arithmetic_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|9n^2 + 12n\|3n\|(3n + 4)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = 6\|m + n = -7` | factor_trinomial_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|107\|1\|0` | factors_generator.py |
| `FACT_FORMULA` | 1 | `FACT_FORMULA\|5! = 1·2·3·4·5` | permutation_combination_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|107` | factors_generator.py |
| `FACT_SETUP` | 2 | `FACT_SETUP\|5!\|expand the factorial` | permutation_combination_generator.py |
| `FERMI_FACTOR` | 2 | `FERMI_FACTOR\|people\|52000` | fermi_estimation_generator.py |
| `FERMI_SETUP` | 2 | `FERMI_SETUP\|town daily water use\|gallons/day` | fermi_estimation_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|1/5` | parallel_perpendicular_line_generator.py |
| `FIN_FORMULA` | 1 | `FIN_FORMULA\|I = P*r*t; A = P + I` | finance_generator.py |
| `FIN_SETUP` | 3 | `FIN_SETUP\|simple interest P = 500\|r = 8%, t = 4\|interest and balance` | finance_generator.py |
| `FLAG` | 2 | `FLAG\|4\|6 × 10 = 60, not 80` | error_spotting_generator.py |
| `FLUX_SUM` | 2 | `FLUX_SUM\|(3 + 1 - 2)*420\|840` | vector_theorem_generator.py |
| `FOCUS` | 1 | `FOCUS\|(5, 5)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: (-8) * 7\|-56` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-2i) * 7\|-14i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-2i) * (-2i)\|4i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: (-8) * (-2i)\|16i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(1 + √15)(5 + √15)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py, trig_identity_verify_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|sum_of_cubes\|a^3 + b^3 = (a + b)(a^2 - ab + b^2)` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FRAC_BUILD` | 2 | `FRAC_BUILD\|56/300\|14/75` | conditional_probability_generator.py, geometric_probability_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|-11/-12\|11/12` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, frequency_table_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, probability_addition_rule_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|2/6\|0.3333333333` | fraction_decimal_percent_converter.py |
| `FREQ_SETUP` | 2 | `FREQ_SETUP\|table — Soccer: 9, Tennis: 7, Golf: 10, Track: 2\|most frequent category` | frequency_table_generator.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(p - q)(3)\|p(3) - q(3)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|g(x) = -5x^2 - 6x - 1\|g(-2)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `GCD_RESULT` | 1 | `GCD_RESULT\|2` | lcm_generator.py |
| `GCD_START` | 2 | `GCD_START\|35\|61` | gcf_generator.py, lcm_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|35\|61\|35` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|45, 15, 40\|5` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|5` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|y^5, y^3, y^2\|y^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GEOM_FORMULA` | 1 | `GEOM_FORMULA\|P(X=k) = (1-p)^(k-1) * p` | geometric_distribution_generator.py |
| `GEOM_SETUP` | 2 | `GEOM_SETUP\|p = 4/5, q = 1/5\|P(X = 2)` | geometric_distribution_generator.py |
| `GEO_PROB_FORMULA` | 1 | `GEO_PROB_FORMULA\|probability = favorable area / total area` | geometric_probability_generator.py |
| `GEO_PROB_SETUP` | 2 | `GEO_PROB_SETUP\|rectangle 20 by 15\|shaded rectangle 14 by 4` | geometric_probability_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude to hypotenuse; the altitude splits the hypotenuse into p = 7 and q = 10\|altitude h` | geometric_mean_generator.py |
| `GOAL` | 1 | `GOAL\|Convert to Slope-Intercept Form (y = mx + b)` | point_slope_generator.py, standard_form_conversion_generator.py |
| `GRAD_RESULT` | 2 | `GRAD_RESULT\|grad g\|(1, 1)` | lagrange_multiplier_generator.py |
| `GRAD_SETUP` | 3 | `GRAD_SETUP\|f(x,y) = 2*x^2 + y^2 - 4*x*y - 3*x + 5*y\|point (1, 2)\|tangent` | gradient_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|Jan\|Feb\|0` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|bar_chart\|English:44,Music:8,Art:26,Math:22,History:45,Science:12` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|2019\|28` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|Feb\|Mar\|2` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Week 2\|23` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Science\|12` | graph_interpret_generator.py |
| `GROUP` | 2 | `GROUP\|(9n^2 + 12n)\|(3n + 4)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `HA` | 1 | `HA\|y = 1` | rational_function_features_generator.py |
| `HESSIAN_DET` | 3 | `HESSIAN_DET\|D = f_xx*f_yy - f_xy^2\|10*(-4) - (-3)^2\|-49` | hessian_classify_generator.py |
| `HESSIAN_SETUP` | 2 | `HESSIAN_SETUP\|f(x,y) = 5*x^2 - 2*y^2 - 3*x*y + 19*x + 9*y\|find and classify the critical point` | hessian_classify_generator.py |
| `HESSIAN_TEST` | 3 | `HESSIAN_TEST\|D = -49\|f_xx = 10\|saddle point` | hessian_classify_generator.py |
| `HOLE` | 1 | `HOLE\|x = -2` | rational_function_features_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|-x^4 + x^3 - 4x^2 - 5x + 2\|x = 3` | horner_evaluation_generator.py |
| `HT_SETUP` | 2 | `HT_SETUP\|H0: μ = 90; Ha: μ ≠ 90\|n = 25, x̄ = 98, s = 5, critical value = 1.96` | hypothesis_test_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|k-faces of the n-cube: C(n,k) · 2^(n-k)` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|3-cube\|number of square faces (k = 2)` | hypercube_counting_generator.py |
| `I` | 2 | `I\|3/2\|2/3` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `IDENTIFY` | 2 | `IDENTIFY\|order does not matter\|use C(n, r)` | permutation_combination_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: sin^4 A - cos^4 A = sin^2 A - cos^2 A\|transform the left side` | trig_identity_verify_generator.py |
| `IDENT_MATCH` | 1 | `IDENT_MATCH\|sin^2 A - cos^2 A = sin^2 A - cos^2 A` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1 | `IDENT_SUB\|sin^2 A + cos^2 A = 1` | parametric_calculus_generator.py, trig_identity_verify_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of x^2\|2x` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|x^2 + y^2 = 25\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|75/14\|5 5/14` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Dividing by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|add\|4\|-3 <= 1x <= 11` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|multiply\|7\|x\|7` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|≥\|7` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x/7 ≥ 1` | linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|x/3 > 5` | domain_range_generator.py, two_step_inequality_generator.py |
| `INNER_ANTIDERIV` | 2 | `INNER_ANTIDERIV\|dr\|r^4/4` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_EVAL` | 2, 3 | `INNER_EVAL\|r=0..6\|6^4/4\|324` | double_integral_generator.py, triple_integral_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|power rule\|∫ x^n dx = x^(n+1)/(n+1) + C` | antiderivative_generator.py, definite_integral_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ (8x^3 - 12x^2) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INTERCEPT_FORMULA` | 1 | `INTERCEPT_FORMULA\|a = ȳ - b·x̄` | regression_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|-14\|14` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|24\|negative\|-24` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|-\|14\|14\|0` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|-14 - (-14)\|-14 + 14` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|subtract_rule\|Subtracting is adding the opposite` | integer_operations_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 - 2x + 6 on [2, 4]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^2\|-1` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|4i^2\|-4` | complex_division_generator.py, complex_number_ops_generator.py |
| `JACOBIAN` | 2 | `JACOBIAN\|dA\|r dr dtheta` | double_integral_generator.py |
| `JAC_DET` | 3 | `JAC_DET\|x_u*y_v - x_v*y_u\|5*2 - (-2)*5\|20` | jacobian_generator.py |
| `JAC_MATRIX` | 2 | `JAC_MATRIX\|[[x_u, x_v], [y_u, y_v]]\|[[5, -2], [5, 2]]` | jacobian_generator.py |
| `JAC_SETUP` | 3 | `JAC_SETUP\|x = 5*u - 2*v\|y = 5*u + 2*v\|d(x,y)/d(u,v)` | jacobian_generator.py |
| `KIN_FORMULA` | 1 | `KIN_FORMULA\|d = v*t` | kinematics_generator.py |
| `KIN_SETUP` | 3 | `KIN_SETUP\|v = 77 ft/s\|t = 4 seconds\|distance` | kinematics_generator.py |
| `L` | 3 | `L\|2\|9\|18` | fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LAGRANGE_EQ` | 2 | `LAGRANGE_EQ\|f_x = lambda\|2*x*y^3` | lagrange_multiplier_generator.py |
| `LAGRANGE_SETUP` | 3 | `LAGRANGE_SETUP\|f(x,y) = x^2*y^3\|constraint x + y = 20\|maximize` | lagrange_multiplier_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|54*50\|2\|1350` | lcm_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→-4⁺ of abs(x + 4)/(x + 4)\|one-sided: approach from the right` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINE_INTEGRAL` | 3 | `LINE_INTEGRAL\|int_0^1 dot dt\|76/2 - 26\|12` | line_integral_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|perpendicular\|y = 1/5x - 3\|(10, 6)` | parallel_perpendicular_line_generator.py |
| `LINE_SETUP` | 2 | `LINE_SETUP\|F(x,y) = <5*x - 3*y, -4*x + 4*y>\|from (-2, -1) to (4, 3)` | line_integral_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|ln(e^(3x)) = ln(42)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|log_5(1/625) = y ⟺ 5^y = 1/625` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|e^(ln x) = x (inverse functions)\|5` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|2x - 7 = x - 5` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|2log_10(x)\|log_10(x^2)` | log_diff_higher_order_generator.py, log_properties_generator.py |
| `LOG_PRODUCT` | 2 | `LOG_PRODUCT\|log_10(x^2) + log_10(y^2)\|log_10(x^2y^2)` | log_equation_generator.py, log_properties_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_10(x^2y^2) - log_10(z^4)\|log_10(x^2y^2/z^4)` | log_properties_generator.py |
| `LOG_SETUP` | 2 | `LOG_SETUP\|2log_10(x) + 2log_10(y) - 4log_10(z)\|condense` | log_properties_generator.py |
| `LUHN_DIGIT` | 3 | `LUHN_DIGIT\|digit 9\|double\|18 -> 9` | modular_arithmetic_generator.py |
| `LU_ENTRY` | 3 | `LU_ENTRY\|u11\|a11 = -2\|-2` | lu_decomposition_generator.py |
| `LU_RESULT` | 2 | `LU_RESULT\|L\|[[1, 0, 0], [2, 1, 0], [1, -2, 1]]` | lu_decomposition_generator.py |
| `LU_SETUP` | 2 | `LU_SETUP\|A = [[-2, -5, -5], [-4, -12, -13], [-2, -1, 2]]\|unit lower L` | lu_decomposition_generator.py |
| `M` | 2, 3 | `M\|6\|99\|594` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_sequence_generator.py, binomial_probability_generator.py, chain_rule_generator.py, circle_angle_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, decimal_div_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, dot_product_generator.py, error_spotting_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, five_number_summary_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, graph_interpret_generator.py, horner_evaluation_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, kinematics_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, multi_step_unit_conversion_generator.py, nets_surface_area_generator.py, optimization_generator.py, order_of_operations_generator.py, parametric_calculus_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, recursive_explicit_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, right_triangle_trig_generator.py, round_solids_generator.py, row_reduction_generator.py, segment_partition_generator.py, similar_triangles_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py, z_score_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2 + z^2)` | vector_ops_generator.py |
| `MAT_ENTRY` | 2 | `MAT_ENTRY\|(1,1)\|24` | matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[6, -4], [3, -2]]\|4A` | determinant_generator.py, eigenvalue_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py, subspace_basis_generator.py |
| `MAX` | 2 | `MAX\|8, 11\|11` | taxicab_geometry_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|71\|7\|10.142857142857142` | composite_arithmetic_generator.py, five_number_summary_generator.py, regression_generator.py, simple_stats_generator.py, standard_deviation_generator.py |
| `MEASURE_FAVORABLE` | 2 | `MEASURE_FAVORABLE\|shaded area\|14 * 4 = 56` | geometric_probability_generator.py |
| `MEASURE_TOTAL` | 2 | `MEASURE_TOTAL\|whole area\|20 * 15 = 300` | geometric_probability_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|9\|12` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEDIAN_PICK` | 2, 3 | `MEDIAN_PICK\|16\|\|16` | five_number_summary_generator.py, simple_stats_generator.py |
| `METRIC` | 2 | `METRIC\|taxicab vs Chebyshev\|sum of absolute differences vs their max` | taxicab_geometry_generator.py |
| `MIDDLE_EVAL` | 3 | `MIDDLE_EVAL\|r=0..5\|5^2/2\|25/2` | triple_integral_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = -6` | sinusoid_features_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|5 9/10\|59/10` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MODE` | 2 | `MODE\|2\|1` | frequency_table_generator.py, simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P(1 - r)^t` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 4000 · (1 - 0.5)^2` | exponential_model_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|1\|1` | simple_stats_generator.py |
| `MOD_REDUCE` | 3 | `MOD_REDUCE\|169\|mod 11\|4` | calendar_arithmetic_generator.py, modular_arithmetic_generator.py |
| `MOD_SETUP` | 2 | `MOD_SETUP\|ISBN-10 modulus 11\|prefix 207534500` | modular_arithmetic_generator.py |
| `MOD_SOLVE` | 2 | `MOD_SOLVE\|d ≡ -4 mod 11\|7` | modular_arithmetic_generator.py |
| `MOD_TERM` | 2 | `MOD_TERM\|10 * 2\|20` | modular_arithmetic_generator.py |
| `MOE_FORMULA` | 1 | `MOE_FORMULA\|E = z*·√(p̂(1-p̂)/n)` | confidence_interval_generator.py |
| `MOMENT_X` | 3 | `MOMENT_X\|M_x = 1/2 int y^2 dx\|2^2*6^3/6\|144` | centroid_generator.py |
| `MOMENT_Y` | 3 | `MOMENT_Y\|M_y = int x*y dx\|2*6^3/3\|144` | centroid_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^6 * x^1 = x^(6+1)\|x^7` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|-8 / -1\|8` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|-7 * 5\|-35` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(-8x^9) / (-1x^5)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^9 / x^5 = x^(9-5)\|x^4` | monomial_mult_div_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|+2x\|left\|-2x-9-2x = -5` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|10\|-8.2x\|-82x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 + 5x - 1 on [-2, 4]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `MV_CHAIN_SETUP` | 3 | `MV_CHAIN_SETUP\|z = f(x,y) = 4*x^2 + 2*y^2 + x*y - 3*x + 2*y\|x = t + 3, y = -2*t - 2\|t = -3` | multivar_chain_rule_generator.py |
| `NCR` | 2 | `NCR\|C(3,2)\|3` | binomial_probability_generator.py, hypercube_counting_generator.py |
| `NEED` | 2 | `NEED\|the equation is 9x - 14 = -68\|line 3 shows 9x = -54` | fill_in_step_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|1 square 2 by 2; 4 triangles with base 2 and height 5\|total surface area` | nets_surface_area_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = -5\|Perpendicular lines have negative reciprocal slopes` | parallel_perpendicular_line_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(-3)\|1/3` | tangent_line_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|A: 124 in N(112, 5)\|compare relative standing` | normal_table_generator.py, z_score_generator.py |
| `NULL_REL` | 2 | `NULL_REL\|x1 + 2*x3 - 3*x4 = 0\|x1 = -2*x3 + 3*x4` | subspace_basis_generator.py |
| `NULL_VECTOR` | 2 | `NULL_VECTOR\|x3=1, x4=0\|[-2, 0, 1, 0]` | subspace_basis_generator.py |
| `ODE_SETUP` | 2 | `ODE_SETUP\|dy/dx = y^2, y(0) = 2\|solve` | euler_method_generator.py, logistic_growth_generator.py, separable_ode_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|x + y = 9, x, y > 0\|maximize P = x·y^2` | optimization_generator.py |
| `OUTER_ANTIDERIV` | 2 | `OUTER_ANTIDERIV\|dx\|5*x^2 + 110*x` | double_integral_generator.py |
| `OUTER_EVAL` | 3 | `OUTER_EVAL\|y=0..25\|8*5*5^2/2\|500` | double_integral_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|2x + 26 = 6x - 38` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|alternate_interior\|Alternate interior angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-4x = -64\|x = 16` | angle_relationships_generator.py |
| `PARAM_PATH` | 3 | `PARAM_PATH\|r(t)\|(6*t - 2, 4*t - 1)\|0 <= t <= 1` | line_integral_generator.py |
| `PARAM_SETUP` | 2 | `PARAM_SETUP\|x = 2 cos t, y = 2 sin t\|eliminate t` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|x/(x + 2)^2 = A/(x + 2) + B/(x + 2)^2` | partial_fractions_generator.py |
| `PARTIAL_RESULT` | 2 | `PARTIAL_RESULT\|f_x\|32*x^3*y^3 + 3*y^4` | div_curl_generator.py, gradient_generator.py, hessian_classify_generator.py, jacobian_generator.py, lagrange_multiplier_generator.py, line_integral_generator.py, multivar_chain_rule_generator.py, partial_derivative_generator.py, vector_theorem_generator.py |
| `PARTIAL_RULE` | 3 | `PARTIAL_RULE\|3*x*y^4\|d/dx\|3*y^4` | partial_derivative_generator.py |
| `PARTIAL_SETUP` | 2 | `PARTIAL_SETUP\|f(x,y) = 8*x^4*y^3 + 3*x*y^4\|f_xx` | partial_derivative_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = 2x, dv = e^(-x) dx\|du = 2 dx, v = -e^(-x)` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|row 8` | pascal_triangle_generator.py |
| `PATH_DERIV` | 2 | `PATH_DERIV\|r'(t)\|(6, 4)` | curve_geometry_generator.py, line_integral_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|0.75\|200\|150` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|90%\|0.9` | composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, fraction_decimal_percent_converter.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, tip_bill_split_generator.py |
| `PERIM` | 1 | `PERIM\|32` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|60°` | sinusoid_features_generator.py |
| `PERM_FORMULA` | 1 | `PERM_FORMULA\|P(n, r) = n·(n-1)···(n-r+1), 5 factors` | permutation_combination_generator.py |
| `PERM_SETUP` | 2 | `PERM_SETUP\|P(8, 5)\|n!/(n-r)!` | permutation_combination_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|17` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|102\|2\|51` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|20° right` | sinusoid_features_generator.py |
| `PHYS_FORMULA` | 1 | `PHYS_FORMULA\|P = W/t` | physics_formula_generator.py |
| `PHYS_SETUP` | 3 | `PHYS_SETUP\|W = 1314 joules\|t = 9 seconds\|power` | physics_formula_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Cars\|8` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|♦\|5` | graph_interpret_generator.py |
| `PIVOT_COLS` | 2 | `PIVOT_COLS\|columns 1, 2\|rank = 2` | subspace_basis_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|4060686\|3\|4060.686` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 2 | `PLACE_DP_Q\|75\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `PLACE_VALUE` | 2 | `PLACE_VALUE\|1 * 2^0\|1` | base_conversion_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|y = ±2\|y = 2 or y = -2` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_FROM_LAMBDA` | 3 | `POINT_FROM_LAMBDA\|x\|6*5/2\|15` | lagrange_multiplier_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 1 = 0(x + 7)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_BOUNDS` | 2 | `POLAR_BOUNDS\|r\|0..6` | double_integral_generator.py |
| `POLAR_CONVERT` | 2 | `POLAR_CONVERT\|x^2 + y^2\|r^2` | double_integral_generator.py |
| `POLAR_EVAL` | 3 | `POLAR_EVAL\|theta range * radial integral\|pi * 324\|324*pi` | double_integral_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|x = r cos θ, y = r sin θ` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2 | `POLAR_SETUP\|(r, θ) = (2, 30°)\|rectangular coordinates` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|4x^3 - 6x^2 - 14x + 14\|2x - 5` | polynomial_long_division_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|-6x^3 - 8x^2 - 9x` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(- 24x^4 - 32x^3) / (-8x^3)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(-24x^4) / (-8x^3) + (-32x^3) / (-8x^3)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(-6x^3) + (-8x^2) + (-7x -2x)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(-2x - 4)(-4x^2 - 2x - 2)` | multiplying_polynomials_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(-6x^3 - 8x^2 - 7x) + (-2x)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2 | `POLY_SUB\|(4x^3 - 6x^2) - (4x^3 - 10x^2)\|4x^2` | polynomial_long_division_generator.py |
| `POTENTIAL_BUILD` | 3 | `POTENTIAL_BUILD\|integrate P dx\|3*x^2 - 5*x*y - 2*x + g(y)\|g'(y) remains` | line_integral_generator.py |
| `POTENTIAL_RESULT` | 2 | `POTENTIAL_RESULT\|phi(x,y)\|3*x^2 + 4*y^2 - 5*x*y - 2*x - 3*y` | line_integral_generator.py |
| `POW` | 2 | `POW\|(3/5)^3\|0.216` | binomial_probability_generator.py, geometric_distribution_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|3x^2\|6x` | chain_rule_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `PRIME` | 1 | `PRIME\|89` | divisibility_classification_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(blue\|first was red)\|3/5` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Coin flip and die roll, looking for tails and 1` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(tails)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Coin flip and die roll are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/6\|1/12` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|8\|9` | simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | *(not observed in sampling)* | compound_probability_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|12/2 = x/3` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|d² = 900 + 1600 = 2500\|2500` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 2 | `PYTHAG_CONTEXT\|rectangle_diagonal\|length=30, width=40` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|length=30\|width=40\|diagonal=?` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|400\|20` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 3 | `PYTHAG_SETUP\|c=29\|a=21\|b=?` | pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 841 - 441\|400` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|21\|441` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|21² + b² = 29²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|-12\|8\|4\|-1` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|-12\|8\|4\|-5` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|54°\|quadrant I` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|11,12,12,15,17,18,20\|15` | five_number_summary_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RATE_MONTHLY` | 2 | `RATE_MONTHLY\|18% / 12\|0.015` | finance_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|circle: dr/dt = 5 cm/s; r = 12 cm\|dA/dt` | related_rates_generator.py |
| `RATIO` | 2 | `RATIO\|2*y = 3*x\|y = 3/2*x` | lagrange_multiplier_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|√6/√6` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|60:55\|5\|12:11` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Red (liters): 60, 72, 96, 132\|Blue (liters): 55, 66, 88, ?` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RAW_FORMULA` | 1 | `RAW_FORMULA\|x = μ + z·σ` | z_score_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 90 / 0.5` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|13/5` | trig_six_functions_generator.py |
| `REGION_MEASURE` | 3 | `REGION_MEASURE\|disk area\|10^2*pi\|100*pi` | vector_theorem_generator.py |
| `REGION_REWRITE` | 2 | `REGION_REWRITE\|0 <= y <= 25\|y/5 <= x <= 5` | double_integral_generator.py |
| `REG_ROW` | 3 | `REG_ROW\|x-x̄=-2\|y-ȳ=-4\|product=8` | regression_generator.py |
| `REG_SETUP` | 2 | `REG_SETUP\|points: (1, 29), (2, 31), (3, 37), (4, 33), (5, 35)\|least-squares line` | regression_generator.py |
| `REJECT` | 2 | `REJECT\|(-1, -42)\|sum is -43, need -13` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `RESID_SETUP` | 2 | `RESID_SETUP\|point (2, 52), line ŷ = 47.8 - 0.6x\|residual = observed − predicted` | regression_generator.py |
| `REVERSE` | 2 | `REVERSE\|1,0,1,0,1,0,0,1\|10010101` | base_arithmetic_generator.py, base_conversion_generator.py, bitwise_ops_generator.py |
| `REWRITE` | 1 | `REWRITE\|8 + 90` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, chain_rule_generator.py, circle_equation_generator.py, completing_square_generator.py, complex_division_generator.py, complex_number_ops_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, evaluate_expression_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, frequency_table_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logistic_growth_generator.py, matrix_inverse_generator.py, midpoint_generator.py, normal_table_generator.py, optimization_generator.py, order_of_operations_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, permutation_combination_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, quadratic_factoring_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, series_convergence_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py |
| `RIEMANN_SETUP` | 2 | `RIEMANN_SETUP\|f(x) = x^2 + 4 on [0, 8], n = 4\|left Riemann sum` | riemann_sum_generator.py |
| `ROOT` | 2 | `ROOT\|2601\|51` | completing_square_generator.py, confidence_interval_generator.py, factor_special_forms_generator.py, hypothesis_test_generator.py, pythag_hyp_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, regression_generator.py, round_solids_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|5` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|125\|perfect_cube\|5` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|∛125` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1 | `ROOT_SIMPLIFY\|4√6` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|68867\|100\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|68867\|68900` | place_value_rounding_generator.py |
| `ROW_OP` | 2 | `ROW_OP\|R2 → R2 - 3·R1\|[0, 1, 0, 3]` | row_reduction_generator.py, subspace_basis_generator.py |
| `RREF_RESULT` | 2 | `RREF_RESULT\|RREF(A)\|[[1, 0, 2, -3], [0, 1, 0, -1], [0, 0, 0, 0]]` | subspace_basis_generator.py |
| `RSQ_FORMULA` | 1 | `RSQ_FORMULA\|r^2 = Sxy^2/(Sxx·Syy)` | regression_generator.py |
| `S` | 3 | `S\|632\|594\|38` | angle_measure_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, binomial_probability_generator.py, calendar_arithmetic_generator.py, circle_angle_generator.py, circle_equation_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, determinant_generator.py, distance_formula_generator.py, ellipse_features_generator.py, euler_characteristic_generator.py, euler_method_generator.py, expected_value_generator.py, exponential_model_generator.py, finance_generator.py, five_number_summary_generator.py, fraction_op_generator.py, function_operations_generator.py, geometric_distribution_generator.py, geometric_sequence_generator.py, graph_interpret_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, kinematics_generator.py, linear_simple_generator.py, logistic_growth_generator.py, long_division_generator.py, manual_square_root_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, normal_table_generator.py, optimization_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, probability_addition_rule_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, regression_generator.py, related_rates_generator.py, riemann_sum_generator.py, row_reduction_generator.py, segment_partition_generator.py, series_convergence_generator.py, slope_two_points_generator.py, solid_revolution_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py, vector_ops_generator.py, z_score_generator.py |
| `SAMPLE_SIZE_FORMULA` | 1 | `SAMPLE_SIZE_FORMULA\|n = (z*/E)^2·p̂(1-p̂)` | confidence_interval_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(2)² = 2π × 4\|8π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|12 × 5\|60` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 2 × 5\|20π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=12, w=5, h=5` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(60 + 60 + 25)\|290` | round_solids_generator.py, volume_3d_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|10\|10\|1.0` | scaling_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|1.5 inches\|actual_dimension` | scaling_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|1.5\|50\|75.0` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 inch\|50 feet\|50` | scaling_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|4.0\|5` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|left\|5` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|multiply_coefficients\|2.3\|2.1\|4.83` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|(2.3 × 10^3) × (2.1 × 10^5)` | exponent_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f''(2) = -6 < 0\|local maximum at x = 2` | curve_analysis_generator.py, optimization_generator.py |
| `SECOND_PARTIAL` | 2 | `SECOND_PARTIAL\|f_xx\|10` | hessian_classify_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(-4, 1), B(-32, 22); ratio 4:3 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (θ/360)·πr^2` | arc_sector_generator.py |
| `SELECT_RELEVANT` | 2 | `SELECT_RELEVANT\|base = 99, rate = 25%\|ignore 32 (irrelevant)` | percent_word_problem_generator.py, proportion_word_problem_generator.py |
| `SEPARATE` | 1 | `SEPARATE\|y^(-2) dy = dx` | separable_ode_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|a_27 = -8 + (27 - 1)·-2` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|-8, -10, -12, -14, ...\|27th term` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ 1/(n^2 + 3), n ≥ 1\|converge or diverge?` | power_series_generator.py, series_convergence_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|90 = 0.5 * whole` | percent_problem_generator.py |
| `SIGFIG_ROUND` | 3 | `SIGFIG_ROUND\|4680000\|2 significant figures\|4.7 × 10^6` | fermi_estimation_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|2 + 4 + 8 + 16 + 32` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=1)^(5) 2^k\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=1\|2^1\|2` | sigma_notation_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|arcsin of a negative\|negative angle` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|4\|2\|8` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|10\|5\|2` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|triangle\|4,5,5\|10 (others unknown)` | scaling_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; DE = 27, AB = 12, EF = 27\|find BC` | similar_triangles_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = -cos(6x - 120°) - 6\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, regression_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|4` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = 3 + 4x` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|0` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(8, 1)\|(6, 1)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (1 - 1) / (6 - 8)` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|tan x = √3/3\|30°, 210°` | trig_equation_generator.py |
| `SORT` | 2 | `SORT\|8,17,12,2,18,6,8\|2,6,8,8,12,17,18` | five_number_summary_generator.py, simple_stats_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|0 = 0\|identity: true for every x` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPEED` | 2, 3 | `SPEED\|sqrt(a^2 + b^2)\|sqrt(8^2 + (-15)^2)\|17` | curve_geometry_generator.py |
| `SPHERICAL_BOUNDS` | 2 | `SPHERICAL_BOUNDS\|rho\|0..12` | triple_integral_generator.py |
| `SPHERICAL_CONVERT` | 2 | `SPHERICAL_CONVERT\|6 dV\|6*rho^2*sin(phi) drho dphi dtheta` | triple_integral_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|15n = 12n + 3n\|9n^2 + 12n + 3n + 4` | factor_trinomial_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|y^2 = 4\|y = ±2` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_DIGIT` | 2 | `SQRT_DIGIT\|8\|root = 8` | manual_square_root_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-100)\|10i` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQRT_SETUP` | 2 | `SQRT_SETUP\|N = 693889\|groups 69, 38, 89` | manual_square_root_generator.py |
| `SQRT_TRIAL` | 3 | `SQRT_TRIAL\|x = 8\|(0 + 8)*8 = 64\|fits` | manual_square_root_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(6x + 55) = 5\|6x + 55 = 25` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|72\|36 × 2\|36` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|88\|9^2 = 81, 10^2 = 100\|not a perfect square` | discriminant_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|-8\|8` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(61 + 81) / 2\|71.0` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|8` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|26\|34\|-8` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|440 / 8\|55` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|12\|2` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|48\|7\|6.86` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|94` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|238 / 7\|34` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|position 5\|73` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|25` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|64\|3` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|17, 22, 61, 73, 73, 92, 94, 97, 97` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|94 - 25\|69` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|74, 69, 48, 58, 65, 41, 43, 42` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|74 + 69 + 48 + 58 + 65 + 41 + 43 + 42\|440` | statistics_generator.py |
| `SUBST` | 2, 3 | `SUBST\|x\|-3\|4(-3)+y-3` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SUM` | 2 | `SUM\|29 + 31 + 37 + 33 + 35\|165` | regression_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = 5y - 1` | inverse_function_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|x^3 + 2x^2 - 3x + 29\|r = -4` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|1` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|1, -2, 5, 9` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: 1y = -9` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with x only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = 1y + -8` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * -4` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|12x - 4y = 120\|-12x + 5y = -129` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x - 1y = -8\|3x + 4y = 46` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=10 into x = 1y + -8` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|g(-1)\|8` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|g(-1)\|15` | dot_product_generator.py, function_evaluation_generator.py, normal_table_generator.py, pascal_triangle_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py |
| `TANGENT_PLANE` | 2 | `TANGENT_PLANE\|z = z0 + fx(x-a) + fy(y-b)\|z = 5 - 7*(x - 1) + 5*(y - 2)` | gradient_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = e^x, center a = 0\|Maclaurin polynomial of degree 4` | taylor_series_generator.py |
| `TERM` | 2 | `TERM\|i=0: 1·(7/10)^0·(3/10)^3\|0.027` | binomial_probability_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|direct comparison\|compare with Σ 1/n^2` | power_series_generator.py, series_convergence_generator.py |
| `TEST_STAT_FORMULA` | 1 | `TEST_STAT_FORMULA\|t = (x̄ - μ0)/(s/√n)` | hypothesis_test_generator.py |
| `THEOREM` | 2 | `THEOREM\|factor theorem\|x - 1 is a factor iff P(1) = 0` | circle_angle_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `THEOREM_REWRITE` | 2 | `THEOREM_REWRITE\|circulation\|surface integral of curl F dot n` | vector_theorem_generator.py |
| `THEOREM_SETUP` | 3 | `THEOREM_SETUP\|Stokes\|F=<3*y, 0, 0>\|disk radius 10 in z=0` | vector_theorem_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|(-(7), (6))\|(-7, 6)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (-x, y)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2 | `TRANSFORM_SETUP\|P(7, 6)\|reflection over the y-axis, then reflection over the x-axis` | transformation_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|sin\|opposite/hypotenuse` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle: opposite side = 16, hypotenuse = 40; given sin 24° ≈ 0.4\|angle A` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRIPLE_EVAL` | 3 | `TRIPLE_EVAL\|z_part * r_part * angle\|5*121/2*25/2*2*pi\|15125/2*pi` | triple_integral_generator.py |
| `TRIPLE_SETUP` | 3 | `TRIPLE_SETUP\|integrand 5*z\|cylinder radius 5, height 11\|cylindrical` | triple_integral_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|60\|67\|exterior` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|exterior = 60 + 67\|127` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|Exterior angle = sum of remote interior angles` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|30-60-90 triangle, shorter leg = 3\|longer leg and hypotenuse` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRY` | 2 | `TRY\|(-1, -6)\|(-1)·(-6)=6, (-1)+(-6)=-7` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `TWOS_SETUP` | 2 | `TWOS_SETUP\|8-bit two's complement\|offset = 2^8 = 256` | base_conversion_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|0°\|(1, 0)` | unit_circle_generator.py |
| `UNIT_ATTACH` | 3 | `UNIT_ATTACH\|308\|feet\|308 feet` | kinematics_generator.py, physics_formula_generator.py |
| `UNIT_CONVERT` | 2 | `UNIT_CONVERT\|6 minutes\|360 seconds` | physics_formula_generator.py |
| `UNIT_NORMAL` | 2 | `UNIT_NORMAL\|T'(0)/norm T'(0)\|<-1, 0>` | curve_geometry_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|$20.00\|10\|$2.00` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|1\|8` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|10\|pounds\|$20.00` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|1,4,7,8\|8,32,56,64` | unit_rate_generator.py |
| `UNIT_TANGENT` | 2 | `UNIT_TANGENT\|r'(0)/speed\|<0, 1>` | curve_geometry_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√5 ≠ √13\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNROLL` | 2 | `UNROLL\|-1, 7, 15, 23\|arithmetic, d = 8` | recursive_explicit_generator.py |
| `VA` | 1 | `VA\|x = 1` | rational_function_features_generator.py |
| `VAR_FORMULA` | 1 | `VAR_FORMULA\|Var(X) = Σ P(x)·(x - μ)^2` | expected_value_generator.py |
| `VAR_ROW` | 3 | `VAR_ROW\|0 - 5.4 = -5.4\|(-5.4)^2 = 29.16\|1/5·29.16 = 5.832` | expected_value_generator.py |
| `VECTOR_SETUP` | 2 | `VECTOR_SETUP\|F(x,y,z) = <-x + 3*y - 3*z, -4*x + 4*y, 2*x - 2*y + 2*z>\|divergence and curl` | div_curl_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|u = ⟨-5, 4⟩, v = ⟨-6, -1⟩\|5u + 5v` | dot_product_generator.py, vector_ops_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py |
| `VERTEX` | 1 | `VERTEX\|(0, 5)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `VOLUME` | 1 | `VOLUME\|385` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|region between y = x (outer) and y = x^2 (inner) on [0, 1], about the x-axis\|washer method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 12 × 8\|48.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 3 × 11 × 5\|165` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = l × w × h` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|rectangular_prism\|l=3, w=11, h=5` | volume_3d_generator.py |
| `WEEKDAY_SCAN` | 2, 3 | `WEEKDAY_SCAN\|index 3\|Thursday` | calendar_arithmetic_generator.py |
| `WORK_DIFF` | 3 | `WORK_DIFF\|phi(end) - phi(start)\|77 - 77\|0` | line_integral_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, angle_measure_generator.py, angle_relationships_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, arithmetic_sequence_generator.py, base_arithmetic_generator.py, base_conversion_generator.py, binomial_probability_generator.py, bitwise_ops_generator.py, calendar_arithmetic_generator.py, centroid_generator.py, chain_rule_generator.py, chi_square_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, completing_square_generator.py, complex_division_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, curve_geometry_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, discriminant_generator.py, distance_formula_generator.py, div_curl_generator.py, divisibility_classification_generator.py, domain_range_generator.py, dot_product_generator.py, double_integral_generator.py, eigenvalue_generator.py, ellipse_features_generator.py, equation_from_two_points_generator.py, error_spotting_generator.py, euler_characteristic_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, five_number_summary_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, gcf_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_generator.py, graph_interpret_generator.py, hessian_classify_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, implicit_diff_generator.py, improper_integral_generator.py, integer_operations_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, jacobian_generator.py, kinematics_generator.py, lagrange_multiplier_generator.py, lcm_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logistic_growth_generator.py, long_division_generator.py, lu_decomposition_generator.py, manual_square_root_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, modular_arithmetic_generator.py, monomial_mult_div_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, multivar_chain_rule_generator.py, nets_surface_area_generator.py, normal_table_generator.py, number_comparison_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, optimization_generator.py, order_of_operations_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, parametric_calculus_generator.py, partial_derivative_generator.py, partial_fractions_generator.py, pascal_triangle_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, point_slope_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, power_series_generator.py, prime_factorization_generator.py, probability_addition_rule_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, recursive_explicit_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, riemann_sum_generator.py, right_triangle_trig_generator.py, round_solids_generator.py, row_reduction_generator.py, scaling_generator.py, segment_partition_generator.py, separable_ode_generator.py, series_convergence_generator.py, sigma_notation_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, statistics_generator.py, subspace_basis_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transformation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, triple_integral_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, u_substitution_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, vector_ops_generator.py, vector_theorem_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py, z_score_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|(y + 8)(y + 6) = 0\|y + 8 = 0 or y + 6 = 0` | area_between_curves_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(124 - 112)/5\|2.4` | normal_table_generator.py, z_score_generator.py |
| `ZSCORE_FORMULA` | 1 | `ZSCORE_FORMULA\|z = (x - μ)/σ` | z_score_generator.py |
