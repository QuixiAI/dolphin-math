# Op-Code Legend

**Generated file — do not hand-edit.** Regenerate with `python tools/gen_opcode_legend.py` (verify freshness with `--check`).

The scratchpad vocabulary belongs to the model and evolves organically: generators may introduce new op-codes freely, and this legend is *descriptive*, not prescriptive. Steps are pipe-delimited strings (`CODE|field|field|...`, at most 4 payload fields) built with `helpers.step()`; the final step of every problem is `Z|<final_answer>`.

1443 distinct op-codes observed.

| Code | Payload fields | Example | Used by |
|---|---|---|---|
| `A` | 3 | `A\|27\|2\|29` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, base_conversion_generator.py, bayesian_update_generator.py, binomial_probability_generator.py, bisection_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, casimir_generator.py, cayley_table_generator.py, channel_capacity_generator.py, chi_square_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dft_generator.py, dijkstra_generator.py, distance_formula_generator.py, doppler_generator.py, dot_product_generator.py, dp_table_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, euler_characteristic_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, feature_map_generator.py, fill_in_step_generator.py, finance_generator.py, finite_field_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_table_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_mean_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, layer_norm_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, mst_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, nets_surface_area_generator.py, newtons_laws_generator.py, npv_irr_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, param_count_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pca_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_group_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, probability_addition_rule_generator.py, pythag_hyp_generator.py, quantization_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, recursive_explicit_generator.py, regression_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, segment_partition_generator.py, shm_generator.py, sigma_notation_generator.py, simple_stats_generator.py, simplex_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, transfer_function_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py, vector_ops_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `ABS` | 2 | `ABS\|-1/2\|1/2` | fixed_point_generator.py, matrix_norm_generator.py, rv_transform_generator.py |
| `ABSORB_EQ` | 2 | `ABSORB_EQ\|u0=p0A+p00*u0+p01*u1\|u1=p1A+p10*u0+p11*u1` | markov_chain_generator.py |
| `ABS_CASE` | 2 | `ABS_CASE\|Case 1\|x - 7 = 12` | absolute_value_equation_generator.py |
| `ABS_CHECK` | 2 | `ABS_CHECK\|-8 < 0\|Absolute value cannot be negative` | absolute_value_equation_generator.py |
| `ABS_ERROR` | 2 | `ABS_ERROR\|1\|0` | quantization_generator.py |
| `ABS_INEQ_CHECK` | 2 | `ABS_INEQ_CHECK\|-1 < 0\|Absolute value cannot be negative` | absolute_value_inequality_generator.py |
| `ABS_INEQ_PART` | 2 | `ABS_INEQ_PART\|Part 1\|x - 3 >= 1 -> x >= 4` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SETUP` | 1 | `ABS_INEQ_SETUP\|\|x + 5\| < 20` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPECIAL` | 2 | `ABS_INEQ_SPECIAL\|c = 0\|Check logic for <` | absolute_value_inequality_generator.py |
| `ABS_INEQ_SPLIT` | 2 | `ABS_INEQ_SPLIT\|AND case\|-20 < x + 5 < 20` | absolute_value_inequality_generator.py |
| `ABS_SETUP` | 1 | `ABS_SETUP\|\|x - 7\| = 12` | absolute_value_equation_generator.py |
| `ABS_SPLIT` | 2, 3 | `ABS_SPLIT\|Two cases\|x - 7 = 12\|x - 7 = -12` | absolute_value_equation_generator.py |
| `ABS_VAL` | 2 | `ABS_VAL\|16\|16` | taxicab_geometry_generator.py |
| `AB_ADD` | 3 | `AB_ADD\|+4000\|5230\|9230` | abacus_addition_generator.py |
| `AB_SET` | 1 | `AB_SET\|5230` | abacus_addition_generator.py |
| `ACCEPT` | 2 | `ACCEPT\|(5, -9)\|product -45 ✓, sum -4 ✓` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `ACT_DERIV` | 3 | `ACT_DERIV\|gelu\|0\|1/2` | activation_generator.py |
| `ACT_SETUP` | 3 | `ACT_SETUP\|activation=gelu\|x=5\|w1=3,b1=-15,w2=4,b2=-2` | activation_generator.py |
| `ACT_VALUE` | 3 | `ACT_VALUE\|gelu\|0\|0` | activation_generator.py |
| `AC_COMPLEX` | 3 | `AC_COMPLEX\|Z\|28\|0j` | ac_circuit_generator.py |
| `AC_FORMULA` | 1 | `AC_FORMULA\|omega0^2=1/(L*C)` | ac_circuit_generator.py |
| `AC_PRODUCT` | 2 | `AC_PRODUCT\|6 × (-5)\|-30` | factor_trinomial_generator.py |
| `AC_SETUP` | 3 | `AC_SETUP\|resonance\|R=28, L=6\|C=1/600` | ac_circuit_generator.py |
| `ADAM_SETUP` | 3 | `ADAM_SETUP\|theta=-6,g=10\|beta1=9/10,beta2=99/100\|lr=1/100,epsilon=0` | adam_step_generator.py |
| `ADAM_UPDATE` | 2 | `ADAM_UPDATE\|theta_new\|-601/100` | adam_step_generator.py |
| `ADD_COL` | 3 | `ADD_COL\|col_1\|0+0+0\|->0 (carry 0)` | multi_digit_addition_generator.py |
| `ADD_FORMULA` | 1 | `ADD_FORMULA\|P(A ∩ B) = P(A) + P(B) - P(A ∪ B)` | probability_addition_rule_generator.py |
| `ADD_PARTIALS` | 2 | `ADD_PARTIALS\|410370 + 3419750 + 61555500 + 68395000\|133780620` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `ADD_SETUP` | 2 | `ADD_SETUP\|P(A) = 4/10, P(B) = 6/10, P(A ∪ B) = 6/10\|P(A ∩ B)` | probability_addition_rule_generator.py |
| `ADJOINT` | 1 | `ADJOINT\|U^dagger=[[44/125,117/125],[-117/125,44/125]]` | hermitian_check_generator.py |
| `ADJ_LIST` | 2 | `ADJ_LIST\|A\|B, C, D` | euler_circuit_generator.py, graph_traversal_generator.py |
| `ALG_SETUP` | 3 | `ALG_SETUP\|insertion sort\|passes 6\|values 2, 13, 29, 30, 38, 6, 11` | algorithm_trace_generator.py |
| `ALIGN_NUM` | 2 | `ALIGN_NUM\|817.63\|148.87` | number_comparison_generator.py |
| `ALPHA` | 2 | `ALPHA\|alpha1\|11/34` | kernel_ridge_generator.py |
| `AMORT_ROW` | 3 | `AMORT_ROW\|1\|interest=$1536.00\|principal=$384.00,balance=$2688.00` | annuity_generator.py |
| `AMPLITUDE` | 2 | `AMPLITUDE\|abs(4)\|4` | sinusoid_features_generator.py |
| `ANALOGY_SETUP` | 3 | `ANALOGY_SETUP\|man=(-2,0)\|woman=(-4,0)\|king=(-2,-3)` | embedding_similarity_generator.py |
| `ANALOGY_VECTOR` | 2 | `ANALOGY_VECTOR\|king-man+woman\|(-4,-3)` | embedding_similarity_generator.py |
| `ANGLE` | 2 | `ANGLE\|theta\|pi` | positional_encoding_generator.py |
| `ANGLE_DEFECT_SETUP` | 2 | `ANGLE_DEFECT_SETUP\|R=2\|angles=15,60,90` | angle_defect_generator.py |
| `ANGLE_EVAL` | 2 | `ANGLE_EVAL\|theta=0..2*pi\|2*pi` | triple_integral_generator.py |
| `ANGLE_FORMULA` | 1 | `ANGLE_FORMULA\|add or subtract 360° until 0° ≤ θ < 360°` | angle_measure_generator.py |
| `ANGLE_RELATION` | 1 | `ANGLE_RELATION\|angle1 + angle2 = 180°` | angle_relationships_generator.py |
| `ANGLE_SETUP` | 2 | `ANGLE_SETUP\|supplementary\|angle1 = 48°` | angle_relationships_generator.py |
| `ANGLE_SOLVE` | 2 | `ANGLE_SOLVE\|180 - 48\|132` | angle_relationships_generator.py |
| `ANGLE_WRAP` | 2 | `ANGLE_WRAP\|240 deg\|-120 deg` | complex_log_generator.py |
| `ANNUITY_FORMULA` | 1 | `ANNUITY_FORMULA\|PV = PMT*(1 - (1+r)^(-n))/r` | annuity_generator.py |
| `ANNUITY_SETUP` | 2, 3 | `ANNUITY_SETUP\|ordinary annuity present value\|PMT=350,r=25%,n=2` | annuity_generator.py |
| `ANTICOMM_ENTRY` | 3 | `ANTICOMM_ENTRY\|(1,1)\|-3i + 3i\|0` | pauli_algebra_generator.py |
| `ANTIDERIV` | 2 | `ANTIDERIV\|-16x^3\|-4x^4` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, definite_integral_generator.py, improper_integral_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, ode_substitution_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py, variation_parameters_generator.py |
| `ANTIDERIVATIVE` | 1 | `ANTIDERIVATIVE\|-A*cos(nx)/n` | fourier_series_generator.py |
| `ANTISYM_CHECK` | 3 | `ANTISYM_CHECK\|(1, 3)\|reverse (3, 1)\|violation` | relation_check_generator.py |
| `APPLY_GATE` | 3 | `APPLY_GATE\|CNOT\|ket10\|ket11` | quantum_gate_generator.py |
| `APPLY_OPERATOR` | 2 | `APPLY_OPERATOR\|L[A]\|-3A = -3` | commutator_generator.py, undetermined_coeff_generator.py |
| `APPLY_PAULI` | 2 | `APPLY_PAULI\|sigma_y ket0\|i ket1` | spin_half_generator.py |
| `APPROX` | 2 | `APPROX\|12*d^2*L\|18874368` | param_count_generator.py |
| `APPROX_ENTRY` | 2 | `APPROX_ENTRY\|(1,1)\|16` | low_rank_approx_generator.py |
| `APPROX_SETUP` | 2 | `APPROX_SETUP\|estimate ∛29\|linearize f(x) = ∛x at a = 27` | linear_approx_generator.py |
| `ARCCOS` | 2 | `ARCCOS\|cos(c)=0\|c=pi/2` | great_circle_generator.py |
| `ARCLEN_FORMULA` | 1 | `ARCLEN_FORMULA\|L = ∫ √((dx/dt)^2 + (dy/dt)^2) dt` | arc_length_generator.py, parametric_calculus_generator.py |
| `ARC_FORMULA` | 1 | `ARC_FORMULA\|L = (θ/360)·2πr` | arc_sector_generator.py |
| `ARC_LENGTH` | 3 | `ARC_LENGTH\|int_0^T speed dt\|5*2\|10` | curve_geometry_generator.py |
| `ARC_SETUP` | 2 | `ARC_SETUP\|circle r = 8, central angle 210°\|sector area` | arc_sector_generator.py |
| `AREA` | 1, 3 | `AREA\|80` | geometry_area_perimeter_generator.py |
| `AREA_INT` | 3 | `AREA_INT\|A = int y dx\|3*5^2/2\|75/2` | centroid_generator.py |
| `AREA_INTEGRAL` | 2 | `AREA_INTEGRAL\|sqrt(EG-F^2)=R^2 sin(phi)\|area = R^2*theta*(cos phi1 - cos phi2)` | fundamental_form_generator.py |
| `AREA_SCALE` | 3 | `AREA_SCALE\|uv rectangle area\|8*7\|56` | jacobian_generator.py |
| `AREA_SETUP` | 2 | `AREA_SETUP\|y = x^2 and y = 7x - 10\|area between the curves` | area_between_curves_generator.py |
| `ARGUMENT` | 2 | `ARGUMENT\|(-6,6)\|135 deg` | complex_log_generator.py, euler_formula_generator.py |
| `ARITH_INTERVAL` | 1 | `ARITH_INTERVAL\|[1/2,3/4)` | arithmetic_coding_generator.py |
| `ARITH_SETUP` | 2 | `ARITH_SETUP\|A=1/2, B=1/4, C=1/4\|message=BACA` | arithmetic_coding_generator.py |
| `ARITH_SYMBOL` | 2 | `ARITH_SYMBOL\|B\|cum=[1/2,3/4)` | arithmetic_coding_generator.py |
| `ARRAY_STATE` | 2 | `ARRAY_STATE\|pass 1\|2, 13, 29, 30, 38, 6, 11` | algorithm_trace_generator.py |
| `ASSIGN` | 2 | `ASSIGN\|P1\|C2` | kmeans_step_generator.py |
| `ASYMPTOTE` | 1 | `ASYMPTOTE\|y = -1 ± (5/12)(x + 4)` | hyperbola_features_generator.py |
| `ATA` | 2 | `ATA\|A^T A\|[[1018, 918], [918, 1018]]` | svd_generator.py |
| `ATOM_CHECK` | 3 | `ATOM_CHECK\|Al\|left=4\|right=4` | stoichiometry_generator.py |
| `ATTN_OUTPUT` | 2 | `ATTN_OUTPUT\|1\|[[10/3,4/3]]` | attention_generator.py |
| `ATTN_SCORE` | 2 | `ATTN_SCORE\|1,1\|0` | attention_generator.py |
| `ATTN_SETUP` | 1, 3 | `ATTN_SETUP\|tokens=3,d=2\|Q=[[0,0], [0,0], [0,0]]\|K=[[0,0], [0,0], [0,0]]` | attention_generator.py |
| `AV_VECTOR` | 2 | `AV_VECTOR\|A*v1\|[44/√2, 44/√2]` | svd_generator.py |
| `B` | 1, 3 | `B\|38\|1\|381` | decimal_div_generator.py, long_division_generator.py, percent_problem_generator.py, polynomial_long_division_generator.py |
| `BACKPROP_DELTA` | 2 | `BACKPROP_DELTA\|h1\|delta=16` | backprop_generator.py |
| `BACKPROP_GRAD` | 2 | `BACKPROP_GRAD\|dL/dy_hat\|-8` | backprop_generator.py |
| `BACKPROP_SETUP` | 3 | `BACKPROP_SETUP\|x=(2,3)\|y=-1\|eta=1/7` | backprop_generator.py |
| `BACK_SUB` | 2 | `BACK_SUB\|v = y/x\|y/x = 3 ln(x) + C` | ode_substitution_generator.py |
| `BACK_SUB_ROW` | 3 | `BACK_SUB_ROW\|r=168\|x=1\|y=0` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `BALANCED_EQ` | 1 | `BALANCED_EQ\|4 Al + 3 O2 -> 2 Al2O3` | stoichiometry_generator.py |
| `BALANCE_COEFFS` | 2 | `BALANCE_COEFFS\|reactants=4,3\|products=2` | stoichiometry_generator.py |
| `BASE_ADD_COL` | 3 | `BASE_ADD_COL\|col 0\|A + 7 + carry 0\|17 -> digit 1, carry 1` | base_arithmetic_generator.py |
| `BASE_ARITH_SETUP` | 2 | `BASE_ARITH_SETUP\|base 16\|BAA + FA7` | base_arithmetic_generator.py |
| `BASE_CARRY` | 2 | `BASE_CARRY\|carry 1\|digit 1, carry 0` | base_arithmetic_generator.py |
| `BASE_MUL_COL` | 3 | `BASE_MUL_COL\|col 0\|1 * 7 + carry 0\|7 -> digit 7, carry 0` | base_arithmetic_generator.py |
| `BASE_SETUP` | 2 | `BASE_SETUP\|112_10\|binary` | base_conversion_generator.py |
| `BAYES_CELL` | 3 | `BAYES_CELL\|true positive\|50 * 7/10\|35` | conditional_probability_generator.py |
| `BAYES_FORMULA` | 1 | `BAYES_FORMULA\|P(disease=no given negative) = TN/(TN + FN)` | conditional_probability_generator.py |
| `BAYES_SETUP` | 3 | `BAYES_SETUP\|disease=yes 50, disease=no 60\|sensitivity 7/10, specificity 3/4\|P(disease=no given test negative)` | conditional_probability_generator.py |
| `BAYES_UPDATE_SETUP` | 2, 3 | `BAYES_UPDATE_SETUP\|beta_binomial\|prior=Beta(12,10)\|successes=6, trials=8` | bayesian_update_generator.py |
| `BCH_FORM` | 2 | `BCH_FORM\|A+B+1/2[A,B]\|[[0, -5, 25/2], [0, 0, 5], [0, 0, 0]]` | bch_generator.py |
| `BCH_SETUP` | 3 | `BCH_SETUP\|A=5E23\|B=-5E12\|order=2` | bch_generator.py |
| `BEREZIN_RULE` | 2 | `BEREZIN_RULE\|int dtheta 1\|0` | grassmann_generator.py |
| `BEZOUT_CHECK` | 2 | `BEZOUT_CHECK\|168*-6 + 78*13\|6` | extended_euclid_generator.py |
| `BIAS_CORRECT` | 2 | `BIAS_CORRECT\|m_hat\|10` | adam_step_generator.py |
| `BINARY_EXPONENT` | 2 | `BINARY_EXPONENT\|80\|1010000` | mod_exp_generator.py, quadratic_residue_generator.py |
| `BINOM_FORMULA` | 1 | `BINOM_FORMULA\|E[X] = n·p` | binomial_probability_generator.py |
| `BINOM_SETUP` | 2 | `BINOM_SETUP\|n = 18, p = 3/10\|E[X]` | binomial_probability_generator.py |
| `BISECTION_SETUP` | 3 | `BISECTION_SETUP\|f(x)=x^2-128\|interval=[11, 12]\|iterations=4` | bisection_generator.py |
| `BISECT_UPDATE` | 3 | `BISECT_UPDATE\|1\|product < 0\|[11, 23/2]` | bisection_generator.py |
| `BIT_ROW` | 2, 3 | `BIT_ROW\|bit 0\|0 XOR 0\|0` | bitwise_ops_generator.py |
| `BIT_RULE` | 2 | `BIT_RULE\|XOR\|1 when exactly one bit is 1` | bitwise_ops_generator.py |
| `BIT_SETUP` | 2 | `BIT_SETUP\|0010 XOR 0100\|4-bit mask` | bitwise_ops_generator.py |
| `BLACKBODY_FORMULA` | 1 | `BLACKBODY_FORMULA\|P=sigma*A*T^4` | blackbody_generator.py |
| `BLACKBODY_SETUP` | 3 | `BLACKBODY_SETUP\|stefan_power\|sigma=8, A=16\|T=20` | blackbody_generator.py |
| `BOND_FORMULA` | 1 | `BOND_FORMULA\|price=sum coupon/(1+y)^t + face/(1+y)^n` | bond_pricing_generator.py |
| `BOND_PRICE` | 1 | `BOND_PRICE\|$3456.00` | bond_pricing_generator.py |
| `BOND_SETUP` | 2 | `BOND_SETUP\|face=4800\|coupon=8%,ytm=50%,years=1` | bond_pricing_generator.py |
| `BOOL_SETUP` | 2 | `BOOL_SETUP\|variables A, B, C\|DNF from f=1 rows` | boolean_algebra_generator.py |
| `BORROW` | 3 | `BORROW\|col_1\|from_left\|1` | multi_digit_subtraction_generator.py |
| `BOX_FORMULA` | 1 | `BOX_FORMULA\|lambda=8*m*L^2*c/((n_high^2-n_low^2)*h)` | particle_in_box_generator.py |
| `BOX_SETUP` | 1, 3 | `BOX_SETUP\|transition_wavelength\|n_low=3, n_high=7\|h=12, c=12` | particle_in_box_generator.py |
| `BRAKET_FORMULA` | 1 | `BRAKET_FORMULA\|U=diag(phases)` | braket_generator.py |
| `BRAKET_SETUP` | 3 | `BRAKET_SETUP\|time_evolution\|psi=[1,2+i,-2]\|phases=[-i,-i,-i]` | braket_generator.py |
| `BRANCH_TEST` | 2 | `BRANCH_TEST\|80 <= 100\|yes` | piecewise_evaluation_generator.py |
| `BRANCH_USE` | 1 | `BRANCH_USE\|$20.00` | piecewise_evaluation_generator.py |
| `BRING_DOWN` | 2 | `BRING_DOWN\|group 16\|current = 16` | composite_arithmetic_generator.py, manual_square_root_generator.py |
| `BSC_FORMULA` | 1 | `BSC_FORMULA\|H_b=p*(-log2 p)+(1-p)*(-log2(1-p))` | channel_capacity_generator.py |
| `BSC_SETUP` | 3 | `BSC_SETUP\|p=23/100\|-log2(p)=2.12\|-log2(1-p)=0.377` | channel_capacity_generator.py |
| `BS_FORMULA` | 2 | `BS_FORMULA\|C=S*N(d1)-K*df*N(d2)\|P=K*df*N(-d2)-S*N(-d1)` | black_scholes_generator.py |
| `BS_RESULT` | 2 | `BS_RESULT\|call=27.25\|put=2.25` | black_scholes_generator.py |
| `BS_SETUP` | 3 | `BS_SETUP\|S=120,K=100\|df=0.95\|N_d1=0.9,N_d2=0.85` | black_scholes_generator.py |
| `C` | 3 | `C\|3/2\|18\|27/18` | fraction_comparison_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `CALC` | 1 | `CALC\|x = -10` | systems_elimination_generator.py, systems_substitution_generator.py |
| `CAL_DIVMOD` | 3 | `CAL_DIVMOD\|50\|7\|7 R1` | calendar_arithmetic_generator.py |
| `CAL_FORMULA` | 1 | `CAL_FORMULA\|q=m*L` | calorimetry_generator.py |
| `CAL_SETUP` | 3 | `CAL_SETUP\|2024-03-10\|Sunday, offset 73 days\|weekday` | calendar_arithmetic_generator.py, calorimetry_generator.py |
| `CANCEL` | 2 | `CANCEL\|5x\|9x - 4` | derivative_limit_def_generator.py, derivative_transcendental_generator.py, limit_evaluation_generator.py, power_series_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, series_convergence_generator.py, trig_identity_verify_generator.py |
| `CANDIDATES` | 1 | `CANDIDATES\|±1, ±2, ±3, ±6, ±9, ±18` | rational_root_generator.py |
| `CANONICAL_ORDER` | 1 | `CANONICAL_ORDER\|A=2, B=2, C=3, D=3, E=3, F=3` | kraft_inequality_generator.py |
| `CANONICAL_SHIFT` | 3 | `CANONICAL_SHIFT\|code=0\|left=2\|0` | kraft_inequality_generator.py |
| `CARRY_FINAL` | 1 | `CARRY_FINAL\|1` | multi_digit_addition_generator.py |
| `CARTESIAN_RESULT` | 1 | `CARTESIAN_RESULT\|{(b, 2), (b, 3), (c, 2), (c, 3)}` | set_operations_generator.py |
| `CART_PAIR` | 3 | `CART_PAIR\|b\|2\|(b, 2)` | set_operations_generator.py |
| `CASHFLOW_PV` | 2 | `CASHFLOW_PV\|coupon_t1\|256` | bond_pricing_generator.py |
| `CASIMIR_FORCE_SETUP` | 2 | `CASIMIR_FORCE_SETUP\|F/A=-π^2*hbar*c/(240*d^4)\|hbar=17,c=1,d=1` | casimir_force_generator.py |
| `CASIMIR_SETUP` | 3 | `CASIMIR_SETUP\|spin=1\|hbar=16\|J^2=Jz^2+(J+J-+J-J+)/2` | casimir_generator.py |
| `CAYLEY_HEADER` | 1 | `CAYLEY_HEADER\|1, 3, 5, 9, 11, 13, 15, 17, 19, 23, 25, 27` | cayley_table_generator.py |
| `CAYLEY_ROW` | 2 | `CAYLEY_ROW\|row 1\|1, 3, 5, 9, 11, 13, 15, 17, 19, 23, 25, 27` | cayley_table_generator.py |
| `CBRT` | 2 | `CBRT\|x^3\|x` | factor_special_forms_generator.py, inverse_function_generator.py, rational_exponent_generator.py |
| `CDF_EVENT` | 3 | `CDF_EVENT\|Y<=y\|X^2<=y\|X<=sqrt(y)` | rv_transform_generator.py |
| `CDF_FORMULA` | 2 | `CDF_FORMULA\|F_Y(y)=sqrt(y)/18\|0<=y<=324` | rv_transform_generator.py |
| `CEIL` | 2 | `CEIL\|530.8416\|531` | confidence_interval_generator.py |
| `CENTER` | 1, 2 | `CENTER\|(1, -2)` | circle_equation_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, pca_generator.py |
| `CENTROID_COORD` | 3 | `CENTROID_COORD\|xbar = M_y/A\|(125)/(75/2)\|10/3` | centroid_generator.py |
| `CENTROID_SETUP` | 3 | `CENTROID_SETUP\|0 <= y <= 3*x\|0 <= x <= 5\|centroid` | centroid_generator.py |
| `CENTROID_UPDATE` | 2 | `CENTROID_UPDATE\|C1\|(3,-2)` | kmeans_step_generator.py |
| `CF_PARTIAL` | 2 | `CF_PARTIAL\|a_0\|4` | continued_fraction_generator.py |
| `CF_RESULT` | 1 | `CF_RESULT\|[4; 15, 2, 4]` | continued_fraction_generator.py |
| `CF_SETUP` | 1 | `CF_SETUP\|565/139` | continued_fraction_generator.py |
| `CG_COEFF` | 2 | `CG_COEFF\|ket(-,-)\|0` | clebsch_gordan_generator.py |
| `CG_SETUP` | 3 | `CG_SETUP\|j1=1/2\|j2=1/2\|phase=-` | clebsch_gordan_generator.py |
| `CG_STATE` | 2 | `CG_STATE\|J=1, M=0\|-1/sqrt2*ket(+,-) - 1/sqrt2*ket(-,+)` | clebsch_gordan_generator.py |
| `CHAIN_DERIV` | 2 | `CHAIN_DERIV\|dy/dx\|6` | activation_generator.py |
| `CHAIN_RATE` | 2 | `CHAIN_RATE\|dx/dt\|-4` | multivar_chain_rule_generator.py |
| `CHAIN_SUM` | 3 | `CHAIN_SUM\|f_x*dx/dt + f_y*dy/dt\|5*(-4) + (-9)*(-3)\|7` | multivar_chain_rule_generator.py |
| `CHAIN_VALUE` | 3 | `CHAIN_VALUE\|x(1)\|(-4)*1 + 5\|1` | multivar_chain_rule_generator.py |
| `CHANGE_BASE` | 1 | `CHANGE_BASE\|log_64(8) = log_2(8)/log_2(64)` | log_conversion_generator.py |
| `CHAR_DIAG` | 2 | `CHAR_DIAG\|diagonal of λI - A\|(λ - 3), (λ - 4)` | eigenvalue_generator.py |
| `CHAR_EQ` | 2 | `CHAR_EQ\|assume y=e^(rx)\|r^2 + 2r - 8 = 0` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_POLY` | 2 | `CHAR_POLY\|p(λ) = λ^2 - 7λ + 12\|(λ - 3)*(λ - 4)` | diagonalization_generator.py, eigenvalue_generator.py, recurrence_generator.py |
| `CHAR_ROOTS` | 2 | `CHAR_ROOTS\|r1 = -4, r2 = 2\|distinct real` | recurrence_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `CHAR_SETUP` | 2 | `CHAR_SETUP\|p(λ) = det(λI - A)\|triangular determinant` | eigenvalue_generator.py |
| `CHECK` | 2, 3 | `CHECK\|multiply_back\|23×98+45=2299\|2299` | area_between_curves_generator.py, arithmetic_sequence_generator.py, base_arithmetic_generator.py, bch_generator.py, bitwise_ops_generator.py, casimir_generator.py, cauchy_riemann_generator.py, chi_square_generator.py, clebsch_gordan_generator.py, commutator_generator.py, completing_square_generator.py, conditional_probability_generator.py, coset_generator.py, cramers_rule_generator.py, cyclic_group_generator.py, dfa_simulation_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, eigenvalue_generator.py, embedding_similarity_generator.py, error_spotting_generator.py, euler_circuit_generator.py, exact_ode_generator.py, expected_value_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, feature_map_generator.py, fill_in_step_generator.py, five_number_summary_generator.py, function_inner_product_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gauss_bonnet_generator.py, gaussian_curvature_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, gradient_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, hamming_code_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, horner_evaluation_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, information_gain_generator.py, inverse_function_generator.py, kernel_perceptron_generator.py, kernel_validity_generator.py, kmeans_step_generator.py, knn_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, least_squares_generator.py, lhopital_generator.py, lie_exponential_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_fractional_generator.py, log_equation_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lu_decomposition_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, mle_generator.py, mobius_transform_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, naive_bayes_generator.py, ode_system_generator.py, or_formula_generator.py, partial_derivative_generator.py, partial_trace_generator.py, pauli_algebra_generator.py, pca_generator.py, perceptron_generator.py, positive_definite_generator.py, power_series_generator.py, projector_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, quaternion_generator.py, radical_variable_simplify_generator.py, ratio_table_generator.py, recursive_explicit_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, rsa_generator.py, running_coupling_generator.py, rv_transform_generator.py, series_convergence_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simplex_generator.py, special_solution_equation_generator.py, statics_generator.py, stereographic_generator.py, structure_constant_generator.py, svd_generator.py, svm_margin_generator.py, systems_elimination_generator.py, taylor_series_generator.py, tip_bill_split_generator.py, totient_generator.py, transportation_generator.py, two_step_equation_generator.py, uncertainty_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `CHECK_POINT` | 3 | `CHECK_POINT\|x=0\|13·0 + 7 = 7\|13·0 + 7 = 7` | special_solution_equation_generator.py |
| `CHINCHILLA` | 2 | `CHINCHILLA\|20N\|26000000000` | scaling_law_generator.py |
| `CHI_FORMULA` | 1 | `CHI_FORMULA\|χ² = Σ (O - E)^2/E` | chi_square_generator.py |
| `CHI_SETUP` | 2 | `CHI_SETUP\|observed: 24, 29, 23, 21, 28; expected: 25 each\|goodness of fit; df = 4, critical value = 9.488` | chi_square_generator.py |
| `CHI_TERM` | 3 | `CHI_TERM\|24 - 25 = -1\|(-1)^2 = 1\|1/25 = 0.04` | chi_square_generator.py |
| `CHRISTOFFEL_FORMULA` | 1 | `CHRISTOFFEL_FORMULA\|Gamma^i_jk = 1/2 g^im(d_j g_mk + d_k g_mj - d_m g_jk)` | christoffel_generator.py |
| `CHRISTOFFEL_SETUP` | 3 | `CHRISTOFFEL_SETUP\|polar\|g_rr=1, g_thetatheta=r^2\|r=4` | christoffel_generator.py |
| `CHRISTOFFEL_VALUE` | 2 | `CHRISTOFFEL_VALUE\|Gamma^phi_thetatheta\|-1/2` | riemann_tensor_generator.py |
| `CIRCLE_ANGLE_SETUP` | 2 | `CIRCLE_ANGLE_SETUP\|inscribed angle 73°\|central angle on the same arc` | circle_angle_generator.py |
| `CIRCLE_CALCULATE` | 2 | `CIRCLE_CALCULATE\|radius = diameter / 2 = 4 / 2\|2.0` | circle_generator.py |
| `CIRCLE_EQ` | 1 | `CIRCLE_EQ\|(x - 5)^2 + (y + 6)^2 = 4` | complex_locus_generator.py |
| `CIRCLE_FORMULA` | 1 | `CIRCLE_FORMULA\|A = πr²` | circle_generator.py |
| `CIRCLE_SETUP` | 2 | `CIRCLE_SETUP\|4\|diameter` | circle_equation_generator.py, circle_generator.py |
| `CIRCLE_SUBSTITUTE` | 1 | `CIRCLE_SUBSTITUTE\|A = π × 2.0²` | circle_generator.py |
| `CIRCULATION_SUM` | 2 | `CIRCULATION_SUM\|(2 - 0)*30\|60` | vector_theorem_generator.py |
| `CI_FORMULA` | 1 | `CI_FORMULA\|x̄ ± E` | confidence_interval_generator.py |
| `CI_SETUP` | 2 | `CI_SETUP\|σ = 9, E = 0.5, z* = 1.28\|minimum sample size for the mean` | confidence_interval_generator.py |
| `CLIFFORD_EXPECT` | 3 | `CLIFFORD_EXPECT\|2*eta=0\|I_entry=0\|0` | gamma_matrix_generator.py |
| `CLUSTER_MEMBERS` | 2 | `CLUSTER_MEMBERS\|C1\|P4` | kmeans_step_generator.py |
| `CMP` | 3 | `CMP\|9/3\|2/3\|>` | fraction_comparison_generator.py, graph_interpret_generator.py |
| `CMP_NUM` | 3 | `CMP_NUM\|817.63\|148.87\|>` | number_comparison_generator.py |
| `CNF_FORM` | 1 | `CNF_FORM\|(A OR NOT B OR NOT C) AND (NOT A OR B OR C) AND (NOT A OR B OR NOT C)` | boolean_algebra_generator.py |
| `CODEWORD` | 1, 3 | `CODEWORD\|1111111` | hamming_code_generator.py, kraft_inequality_generator.py |
| `CODE_LENGTH` | 2 | `CODE_LENGTH\|A\|l=2` | huffman_coding_generator.py |
| `COEFF` | 2 | `COEFF\|a_1\|4080` | laurent_series_generator.py, series_solution_generator.py |
| `COEFFS` | 1, 2 | `COEFFS\|3, 17, 6, -21` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `COEFF_MATCH` | 2 | `COEFF_MATCH\|x^n\|(n+1)a_(n+1) = a_n` | series_solution_generator.py |
| `COEFF_PAIR` | 3 | `COEFF_PAIR\|i=1, j=5\|3i + 4j = 23\|accepted` | generating_function_generator.py |
| `COFACTOR` | 2 | `COFACTOR\|(1,1) sign +\|minor [[-3, 1], [3, 3]]` | determinant_generator.py |
| `COLLIDER_SETUP` | 3 | `COLLIDER_SETUP\|cross_section\|N=14 events\|L=11 fb^-1` | cross_section_generator.py |
| `COLLISION_SETUP` | 3 | `COLLISION_SETUP\|elastic_1d\|m1=12, u1=-9\|m2=3, u2=19` | collision_generator.py |
| `COL_BASIS` | 2 | `COL_BASIS\|original columns 1, 2\|[[7, -3, -8], [-2, 1, 3]]` | subspace_basis_generator.py |
| `COMB_CONST` | 3 | `COMB_CONST\|7\|-2\|5` | derivative_product_quotient_generator.py, equation_from_two_points_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMB_FORMULA` | 1 | `COMB_FORMULA\|C(n, r) = P(n, r)/r!` | permutation_combination_generator.py |
| `COMB_SETUP` | 2 | `COMB_SETUP\|C(12, 4)\|n!/(r!·(n-r)!)` | permutation_combination_generator.py, stars_and_bars_generator.py |
| `COMB_X` | 3 | `COMB_X\|3x\|-5x\|-2x` | derivative_product_quotient_generator.py, linear_complex_generator.py, rational_expr_add_sub_generator.py, simplify_expression_generator.py, special_solution_equation_generator.py |
| `COMMON_DIFF` | 2 | `COMMON_DIFF\|-6 - (-3)\|-3` | arithmetic_sequence_generator.py, recursive_explicit_generator.py |
| `COMMON_RATIO` | 2 | `COMMON_RATIO\|-10/(-5)\|2` | geometric_sequence_generator.py, recursive_explicit_generator.py |
| `COMMUTATOR` | 2 | `COMMUTATOR\|[A,B]\|[[0, -6i], [-6i, 0]]` | structure_constant_generator.py |
| `COMM_ENTRY` | 3 | `COMM_ENTRY\|(1,1)\|0 - 0\|0` | structure_constant_generator.py |
| `COMM_FORMULA` | 1 | `COMM_FORMULA\|[A,B]f=A(Bf)-B(Af)` | commutator_generator.py |
| `COMM_RESULT` | 2 | `COMM_RESULT\|[x,p]f\|15i*x^18` | commutator_generator.py |
| `COMM_SETUP` | 3 | `COMM_SETUP\|[x,p]f\|f=x^18\|p=-i*hbar*D, hbar=15` | commutator_generator.py |
| `COMPARE` | 3 | `COMPARE\|arr[0]=2\|key 13\|stop` | algorithm_trace_generator.py, fixed_point_generator.py |
| `COMPLETE_SQUARE` | 2 | `COMPLETE_SQUARE\|half of -12 = -6\|(-6)^2 = 36` | completing_square_generator.py, conic_standard_form_generator.py, polar_parametric_generator.py |
| `COMPOSITE_FACTOR` | 2 | `COMPOSITE_FACTOR\|3\|47` | divisibility_classification_generator.py |
| `COMPOSITE_SETUP` | 2 | `COMPOSITE_SETUP\|area = length × width with mixed numbers\|convert, multiply, simplify` | composite_arithmetic_generator.py |
| `COMP_INEQ_PART` | 2 | `COMP_INEQ_PART\|Part 1\|x - 6 < -16 -> x < -10` | compound_inequality_generator.py |
| `COMP_INEQ_SETUP` | 1 | `COMP_INEQ_SETUP\|x - 6 < -16 OR x - 6 > -7` | compound_inequality_generator.py |
| `COND_COUNT` | 2 | `COND_COUNT\|club=no and commute=bus\|19` | conditional_probability_generator.py |
| `COND_ENTROPY` | 1 | `COND_ENTROPY\|H(Y given X)=H(X,Y)-H(X)` | mutual_information_generator.py |
| `COND_FORMULA` | 1 | `COND_FORMULA\|P(A given B) = count(A and B)/count(B)` | conditional_probability_generator.py, joint_distribution_generator.py |
| `COND_SETUP` | 2 | `COND_SETUP\|yes/bike 26, no/bike 8, yes/bus 16, no/bus 19\|P(club=no given commute=bus)` | conditional_probability_generator.py |
| `COND_TOTAL` | 2 | `COND_TOTAL\|commute=bus total\|16 + 19 = 35` | conditional_probability_generator.py |
| `CONGRUENCE_REDUCE` | 2 | `CONGRUENCE_REDUCE\|11x congruent to 1\|mod 6` | modular_inverse_generator.py |
| `CONGRUENCE_SOLUTIONS` | 3 | `CONGRUENCE_SOLUTIONS\|base 5\|step 6\|5, 11, 17` | modular_inverse_generator.py |
| `CONIC_SETUP` | 2 | `CONIC_SETUP\|(y + 2)^2 = -4(x - 2)\|vertex, focus, directrix` | conic_standard_form_generator.py, ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `CONJ` | 2 | `CONJ\|phi_1=1\|1` | braket_generator.py |
| `CONJUGATE` | 2 | `CONJUGATE\|5 + 2i\|5 - 2i` | complex_division_generator.py, quaternion_generator.py |
| `CONSERVATION_SETUP` | 2 | `CONSERVATION_SETUP\|gamma + pi0 + pi+ -> pi0 + nu_mu + mu+ + gamma\|check=Q,B,Le,Lmu` | conservation_law_generator.py |
| `CONSERVE_CHECK` | 3 | `CONSERVE_CHECK\|Q\|left=1,right=1\|conserved` | conservation_law_generator.py |
| `CONSTRAINT_SUBST` | 3 | `CONSTRAINT_SUBST\|x + y = 24\|x = 3*24/6\|12` | lagrange_multiplier_generator.py |
| `CONST_SOLVE` | 2 | `CONST_SOLVE\|C1 = -3\|C2 = -2` | recurrence_generator.py |
| `CONTOUR_SETUP` | 3 | `CONTOUR_SETUP\|abs(z)=7\|positive orientation\|f=3/(z+7) - 1/(z-8) - 6/(z-6)` | contour_integral_generator.py |
| `CONT_DIST_SETUP` | 3 | `CONT_DIST_SETUP\|f(x)=k*x\|support=[0,3]\|interval=(1,2)` | continuous_distribution_generator.py |
| `CONVERGENT` | 2 | `CONVERGENT\|i=0\|4/1` | continued_fraction_generator.py |
| `CONVERGE_CHECK` | 2 | `CONVERGE_CHECK\|abs(r) = 2/3 < 1\|converges` | geometric_sequence_generator.py, series_convergence_generator.py |
| `CONV_FACTOR` | 2 | `CONV_FACTOR\|1 lb\|16 oz` | cross_section_generator.py, dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, unit_conversion_generator.py |
| `CONV_INIT` | 2 | `CONV_INIT\|h_-2=0,h_-1=1\|k_-2=1,k_-1=0` | continued_fraction_generator.py |
| `CONV_RESULT` | 2 | `CONV_RESULT\|2 lb\|32 oz` | dimensional_analysis_generator.py, multi_step_unit_conversion_generator.py, rate_conversion_generator.py, temperature_conversion_generator.py, unit_conversion_generator.py |
| `CONV_SETUP` | 2 | `CONV_SETUP\|x=[0,6,5]\|h=[3,9,1,0]` | convolution_generator.py |
| `CONV_STEP` | 3 | `CONV_STEP\|i=0\|h=4\|k=1` | continued_fraction_generator.py |
| `CONV_SUM` | 2 | `CONV_SUM\|n=0\|0` | convolution_generator.py |
| `CONV_WINDOW` | 2 | `CONV_WINDOW\|n=0\|x0*h0` | convolution_generator.py |
| `CORRECT_BIT` | 3 | `CORRECT_BIT\|position=7\|0->1\|corrected=0100101` | hamming_code_generator.py |
| `CORR_FORMULA` | 1 | `CORR_FORMULA\|r = Sxy/√(Sxx·Syy)` | joint_distribution_generator.py, regression_generator.py |
| `COS` | 2 | `COS\|pi\|-1` | positional_encoding_generator.py |
| `COSET` | 2 | `COSET\|0+H\|{0, 10, 8, 6, 4, 2}` | coset_generator.py |
| `COSET_ELEM` | 2 | `COSET_ELEM\|0+H\|0` | coset_generator.py |
| `COSET_SKIP` | 2 | `COSET_SKIP\|2\|already listed` | coset_generator.py |
| `COSET_START` | 2 | `COSET_START\|rep 0\|0+H` | coset_generator.py |
| `COSINE` | 2 | `COSINE\|A,A\|1` | embedding_similarity_generator.py, lr_schedule_generator.py |
| `COST` | 1 | `COST\|initial` | transportation_generator.py |
| `COUNT` | 2 | `COUNT\|A = [2, 3, 5]\|3/6` | bayesian_update_generator.py, method_of_moments_generator.py, mle_generator.py, probability_addition_rule_generator.py, set_operations_generator.py |
| `COUNT_DP` | 3 | `COUNT_DP\|2\|1\|3` | decimal_mult_generator.py |
| `COUPON` | 1 | `COUPON\|384` | bond_pricing_generator.py |
| `COV_ENTRY` | 2 | `COV_ENTRY\|xx\|1/2` | pca_generator.py |
| `COV_FORMULA` | 1 | `COV_FORMULA\|Cov=E[XY]-E[X]E[Y]` | joint_distribution_generator.py |
| `CRC_CHECK` | 3 | `CRC_CHECK\|codeword=100111000\|remainder=0000\|valid` | crc_generator.py |
| `CRC_REMAINDER` | 1 | `CRC_REMAINDER\|1000` | crc_generator.py |
| `CRC_SETUP` | 3 | `CRC_SETUP\|data=10011\|poly=11101\|augmented=100110000` | crc_generator.py |
| `CRC_SKIP` | 2 | `CRC_SKIP\|i=2\|leading bit 0` | crc_generator.py |
| `CRC_XOR` | 3 | `CRC_XOR\|i=0\|10011 xor 11101\|01110` | crc_generator.py |
| `CRIT_EQS` | 2 | `CRIT_EQS\|f_x = 0\|10*x + 3*y - 36 = 0` | hessian_classify_generator.py |
| `CRIT_SOLVE` | 3 | `CRIT_SOLVE\|det\|10*10 - 3^2\|91` | hessian_classify_generator.py |
| `CROSS_ENTROPY` | 2 | `CROSS_ENTROPY\|target=3\|ln(5)` | perplexity_generator.py, softmax_gradient_generator.py |
| `CROSS_MULT` | 1 | `CROSS_MULT\|21·BC = 7·9` | similar_triangles_generator.py, triangle_solve_generator.py |
| `CROSS_RATIO` | 1 | `CROSS_RATIO\|-4` | mobius_transform_generator.py |
| `CROSS_RATIO_SETUP` | 4 | `CROSS_RATIO_SETUP\|z1=-8\|z2=-5\|z3=-2\|z4=-7` | mobius_transform_generator.py |
| `CRT_CHECK` | 3 | `CRT_CHECK\|i=1\|3\|3` | crt_generator.py |
| `CRT_CONGRUENCE` | 3 | `CRT_CONGRUENCE\|i=1\|x=3\|mod 5` | crt_generator.py |
| `CRT_FACTOR` | 3 | `CRT_FACTOR\|i=1\|M_i=7\|mod 5` | crt_generator.py |
| `CRT_SETUP` | 1 | `CRT_SETUP\|2 congruences` | crt_generator.py |
| `CRT_TERM` | 2 | `CRT_TERM\|i=1\|63` | crt_generator.py |
| `CRT_TOTAL_MODULUS` | 2 | `CRT_TOTAL_MODULUS\|5, 7\|35` | crt_generator.py |
| `CR_SETUP` | 2 | `CR_SETUP\|u=4x^2 - 4y^2 - 5x - 5y\|v=8xy + 5x - 5y` | cauchy_riemann_generator.py |
| `CUM_INTERVAL` | 2 | `CUM_INTERVAL\|A\|[0,1/2)` | arithmetic_coding_generator.py |
| `CURL_COMPONENT` | 3 | `CURL_COMPONENT\|Q_x - P_y\|1 + 2\|3` | div_curl_generator.py |
| `CURRENT_YIELD` | 1 | `CURRENT_YIELD\|1/9` | bond_pricing_generator.py |
| `CURVATURE_FORMULA` | 2 | `CURVATURE_FORMULA\|circle\|kappa = 1/R` | curve_geometry_generator.py |
| `CURVE_GEOM_SETUP` | 3 | `CURVE_GEOM_SETUP\|r(t) = <3*t + 5, 4*t - 2>\|0 <= t <= 2\|arc length` | curve_geometry_generator.py |
| `CURVE_SETUP` | 2 | `CURVE_SETUP\|f(x) = x^3 - 12x^2 + 45x + 3\|inflection point and concavity` | curve_analysis_generator.py |
| `CX_A` | 3 | `CX_A\|0\|-15/17\|-15/17` | braket_generator.py, spin_half_generator.py |
| `CX_M` | 3 | `CX_M\|0\|8/17\|0` | braket_generator.py, spin_half_generator.py |
| `CX_SETUP` | 2 | `CX_SETUP\|(3 + 7i) - (4 + 2i)\|subtract` | complex_division_generator.py, complex_number_ops_generator.py |
| `CYCLE` | 1 | `CYCLE\|(1 3 2)` | permutation_group_generator.py |
| `CYCLE_LENGTHS` | 1 | `CYCLE_LENGTHS\|3` | permutation_group_generator.py |
| `CYCLE_REJECT` | 2 | `CYCLE_REJECT\|CE\|endpoints already connected` | mst_generator.py |
| `CYCLE_TRACE` | 2 | `CYCLE_TRACE\|start 1\|1->3->2->1` | permutation_group_generator.py |
| `CYCLIC_START` | 2 | `CYCLIC_START\|5\|identity 1` | cyclic_group_generator.py |
| `CYCLIC_SUBGROUP` | 2 | `CYCLIC_SUBGROUP\|{1, 5}\|2` | cyclic_group_generator.py |
| `CYL_BOUNDS` | 2 | `CYL_BOUNDS\|z\|0..5` | triple_integral_generator.py |
| `CYL_CONVERT` | 2 | `CYL_CONVERT\|6*z dV\|6*z*r dz dr dtheta` | triple_integral_generator.py |
| `D` | 3 | `D\|632\|99\|6` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, antiderivative_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, bayesian_update_generator.py, bisection_generator.py, blackbody_generator.py, bond_pricing_generator.py, branching_ratio_generator.py, casimir_force_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, classifier_metrics_generator.py, collision_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, coset_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, dimensional_analysis_generator.py, doppler_generator.py, einstein_summation_generator.py, electrostatics_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, error_spotting_generator.py, exact_ode_generator.py, exponential_equation_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finite_difference_generator.py, flops_memory_generator.py, fourier_series_generator.py, function_inner_product_generator.py, function_operations_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, heat_engine_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypothesis_test_generator.py, information_gain_generator.py, integrating_factor_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_ridge_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, least_squares_generator.py, legendre_construction_generator.py, limit_evaluation_generator.py, linear_simple_generator.py, log_conversion_generator.py, logistic_growth_generator.py, long_division_generator.py, lr_schedule_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, midpoint_generator.py, mle_generator.py, modular_inverse_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_substitution_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, permutation_combination_generator.py, perplexity_generator.py, physics_formula_generator.py, planck_units_generator.py, polar_parametric_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, recurrence_generator.py, regression_generator.py, regular_polygon_area_generator.py, relativistic_energy_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, series_convergence_generator.py, series_solution_generator.py, shm_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simplex_generator.py, sinusoid_features_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, standard_deviation_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transient_circuit_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py, vector_ops_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py |
| `DATA_PRECISION` | 1 | `DATA_PRECISION\|n/sigma^2` | bayesian_update_generator.py |
| `DATE_ORDINAL` | 2 | `DATE_ORDINAL\|2026-12-16\|739966` | calendar_arithmetic_generator.py |
| `DB_FORMULA` | 1 | `DB_FORMULA\|G_dB=10*log10(P2/P1)` | signal_arithmetic_generator.py |
| `DECISION` | 2 | `DECISION\|f(x)\|-112` | kernel_perceptron_generator.py, svm_margin_generator.py |
| `DEC_ADD_COL` | 3 | `DEC_ADD_COL\|frac_0\|8+0+0\|->8 (carry 0)` | decimal_add_sub_generator.py |
| `DEC_ALIGN` | 2 | `DEC_ALIGN\|17.98\|23.20` | decimal_add_sub_generator.py |
| `DEC_CARRY_FINAL` | 1 | `DEC_CARRY_FINAL\|1` | decimal_add_sub_generator.py |
| `DEC_SHIFT` | 3 | `DEC_SHIFT\|7.5/1.0\|75/10\|1` | decimal_div_generator.py, percent_problem_generator.py |
| `DEC_SUB_COL` | 3 | `DEC_SUB_COL\|frac_0\|7-1 (borrow_in 0)\|->6 (borrow_out 0)` | decimal_add_sub_generator.py |
| `DEC_TO_FRAC` | 2 | `DEC_TO_FRAC\|0.1\|1/10` | fraction_decimal_percent_converter.py |
| `DEC_TO_PERCENT` | 2 | `DEC_TO_PERCENT\|1\|100.00%` | fraction_decimal_percent_converter.py, percent_problem_generator.py, tip_bill_split_generator.py |
| `DEC_TYPE` | 2 | `DEC_TYPE\|4/5\|terminating` | repeating_decimal_generator.py |
| `DEC_VALUE` | 2 | `DEC_VALUE\|4/5\|0.8` | repeating_decimal_generator.py |
| `DEGREE` | 2, 3 | `DEGREE\|A\|D\|1` | euler_circuit_generator.py, graph_counting_generator.py |
| `DEGREE_COMPARE` | 2 | `DEGREE_COMPARE\|deg num = deg den = 2\|y = 1/1` | limit_evaluation_generator.py, rational_function_features_generator.py, series_convergence_generator.py |
| `DEGREE_SEQUENCE` | 1 | `DEGREE_SEQUENCE\|3, 3, 3, 2, 1` | graph_counting_generator.py |
| `DELTA_VALUE` | 2 | `DELTA_VALUE\|delta_21\|0` | index_gymnastics_generator.py |
| `DEMOIVRE_POWER` | 1 | `DEMOIVRE_POWER\|16 cis(180 deg)` | de_moivre_generator.py |
| `DEMOIVRE_SETUP` | 2, 4 | `DEMOIVRE_SETUP\|power\|r=2\|theta=45 deg\|n=4` | de_moivre_generator.py |
| `DENSITY` | 2 | `DENSITY\|f_X(x)\|1/18` | rv_transform_generator.py |
| `DENSITY_MATRIX` | 1 | `DENSITY_MATRIX\|rho=[[3/8,0],[0,5/8]]` | density_matrix_generator.py |
| `DENSITY_SETUP` | 2, 3 | `DENSITY_SETUP\|state=plus0\|psi=(ket00 + ket10)/sqrt(2)` | density_matrix_generator.py, partial_trace_generator.py |
| `DEQUANT_VALUE` | 2 | `DEQUANT_VALUE\|1\|-36/25` | quantization_generator.py |
| `DERANGE_SETUP` | 2 | `DERANGE_SETUP\|n = 9\|no item fixed` | derangement_generator.py |
| `DERANGE_VALUE` | 2 | `DERANGE_VALUE\|D_2\|1` | derangement_generator.py |
| `DERIV` | 2, 3 | `DERIV\|d_r g_thetatheta = 2r\|at r=4\|8` | christoffel_generator.py, gaussian_curvature_generator.py, riemann_tensor_generator.py |
| `DERIVATIVE` | 1, 2 | `DERIVATIVE\|g'(x)\|-1/2` | fixed_point_generator.py, mgf_generator.py, mle_generator.py |
| `DERIV_FORM` | 2 | `DERIV_FORM\|y'\|-4C1e^(-4x) + 2C2e^(2x)` | second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `DERIV_RULE` | 2 | `DERIV_RULE\|power rule\|d/dx of c·x^n = c·n·x^(n-1)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, multivar_chain_rule_generator.py |
| `DERIV_SERIES` | 2 | `DERIV_SERIES\|y'\|sum (n+1)a_(n+1)x^n` | series_solution_generator.py |
| `DERIV_SETUP` | 2 | `DERIV_SETUP\|f(x) = 5x^5 + 7x^3 - 5x^2\|f'(x)` | chain_rule_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, log_diff_higher_order_generator.py, tangent_line_generator.py |
| `DESIGN_MATRIX` | 2 | `DESIGN_MATRIX\|X = [[1, -3], [1, -1], [1, 1], [1, 3]]\|y = [-3, 5, 9, 9]` | least_squares_generator.py |
| `DET` | 2 | `DET\|K\|-81` | kernel_ridge_generator.py, kernel_validity_generator.py |
| `DET2` | 2 | `DET2\|ad - bc\|-6` | ode_system_generator.py |
| `DET_FORMULA` | 1 | `DET_FORMULA\|det = ad - bc` | cramers_rule_generator.py, determinant_generator.py, matrix_inverse_generator.py |
| `DEV_ROW` | 3 | `DEV_ROW\|21\|2\|4` | standard_deviation_generator.py |
| `DFA_ACCEPT` | 1 | `DFA_ACCEPT\|q0` | dfa_simulation_generator.py |
| `DFA_INPUT` | 1 | `DFA_INPUT\|00001` | dfa_simulation_generator.py |
| `DFA_READ` | 2 | `DFA_READ\|pos 1\|0` | dfa_simulation_generator.py |
| `DFA_SETUP` | 3 | `DFA_SETUP\|states q0, q1\|alphabet 0, 1\|start q0` | dfa_simulation_generator.py |
| `DFA_STATE` | 2 | `DFA_STATE\|start\|q0` | dfa_simulation_generator.py |
| `DFA_STEP` | 3 | `DFA_STEP\|q0\|0\|q1` | dfa_simulation_generator.py |
| `DFA_TRANSITION` | 3 | `DFA_TRANSITION\|q0\|0\|q1` | dfa_simulation_generator.py |
| `DFS_EDGE` | 2 | `DFS_EDGE\|D->B\|tree` | graph_traversal_generator.py |
| `DFT_BIN` | 1 | `DFT_BIN\|X0=x0+x1` | dft_generator.py |
| `DFT_SETUP` | 2 | `DFT_SETUP\|N=2\|x=[2,5]` | dft_generator.py |
| `DH_PUBLIC` | 2 | `DH_PUBLIC\|Alice\|2` | diffie_hellman_generator.py |
| `DH_SECRET` | 2 | `DH_SECRET\|Alice\|14` | diffie_hellman_generator.py |
| `DH_SETUP` | 2 | `DH_SETUP\|p=41\|g=7` | diffie_hellman_generator.py |
| `DH_SHARED` | 2 | `DH_SHARED\|Alice\|2` | diffie_hellman_generator.py |
| `DIAG_FORM` | 3 | `DIAG_FORM\|P = [[1, 1], [2, 3]]\|D = [[-1, 0], [0, 3]]\|P^-1 = [[3, -1], [-2, 1]]` | diagonalization_generator.py, matrix_exponential_generator.py |
| `DIFF_ROW` | 2 | `DIFF_ROW\|Delta y\|[-1, -1, -1]` | finite_difference_generator.py |
| `DIFF_SETUP` | 3 | `DIFF_SETUP\|f(x,y) = 2*x^2 + 5*y^2 - 3*x*y - x - 4*y\|point (-1, 4)\|dx=1/2, dy=-1/4` | multivar_chain_rule_generator.py |
| `DIFF_SUM` | 3 | `DIFF_SUM\|f_x*dx + f_y*dy\|(-17)*1/2 + 39*(-1/4)\|-18.25` | multivar_chain_rule_generator.py |
| `DIJKSTRA_INIT` | 2 | `DIJKSTRA_INIT\|start D\|A=inf, B=inf, C=inf, D=0, E=inf, F=inf` | dijkstra_generator.py |
| `DIRECTRIX` | 1 | `DIRECTRIX\|x = 3` | parabola_features_generator.py |
| `DISC` | 2, 3 | `DISC\|36\|-864\|900` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `DISC_CLASSIFY` | 2 | `DISC_CLASSIFY\|-95 < 0\|no real solutions` | complex_quadratic_generator.py, discriminant_generator.py, polynomial_zeros_generator.py |
| `DIST` | 3 | `DIST\|-1\|-x-4\|x+4` | derivative_limit_def_generator.py, derivative_product_quotient_generator.py, equation_from_two_points_generator.py, function_composition_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, polar_parametric_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recursive_explicit_generator.py, simplify_expression_generator.py, solid_revolution_generator.py, special_solution_equation_generator.py, tangent_line_generator.py |
| `DIST2` | 2, 3 | `DIST2\|P1\|C1\|85` | embedding_similarity_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py |
| `DIST_COMBINE` | 1 | `DIST_COMBINE\|5y - 4 = -34` | systems_substitution_generator.py |
| `DIST_FORMULA` | 1 | `DIST_FORMULA\|d = √((x2 - x1)^2 + (y2 - y1)^2)` | complex_locus_generator.py, distance_formula_generator.py, hypercube_counting_generator.py |
| `DIST_SETUP` | 3 | `DIST_SETUP\|poisson\|lambda=1\|k=1` | named_distribution_generator.py |
| `DIST_TABLE` | 2 | `DIST_TABLE\|visited D\|A=inf, B=inf, C=5, D=0, E=inf, F=8` | dijkstra_generator.py |
| `DIST_TERM` | 2 | `DIST_TERM\|2x\|- 2x^3 - 8x^2 - 6x` | multiplying_polynomials_generator.py |
| `DIVIDE_EQ` | 2 | `DIVIDE_EQ\|divide by y^2\|y^(-2)dy/dx + 5y^(-1) = 15` | ode_substitution_generator.py |
| `DIVMOD` | 4 | `DIVMOD\|112\|2\|56\|r=0` | base_conversion_generator.py |
| `DIV_CHECK` | 3 | `DIV_CHECK\|89\|2\|1` | divisibility_classification_generator.py |
| `DIV_COEFF` | 3 | `DIV_COEFF\|5\|-2\|x=-5/2` | linear_complex_generator.py |
| `DIV_SETUP` | 2 | `DIV_SETUP\|75\|10` | decimal_div_generator.py, percent_problem_generator.py |
| `DIV_SUM` | 3 | `DIV_SUM\|P_x + Q_y\|-5 + 6\|1` | div_curl_generator.py |
| `DIV_TERM` | 3 | `DIV_TERM\|6x^5\|6x^2\|x^3` | factor_gcf_generator.py, finite_field_generator.py, polynomial_long_division_generator.py |
| `DNF_FORM` | 1 | `DNF_FORM\|(NOT A AND NOT B AND C) OR (NOT A AND B AND NOT C) OR (NOT A AND B AND C)` | boolean_algebra_generator.py |
| `DOMAIN_COND` | 2 | `DOMAIN_COND\|denominator ≠ 0\|x^2 - 7x + 12 ≠ 0` | domain_range_generator.py |
| `DOMAIN_NOTE` | 2 | `DOMAIN_NOTE\|x ≠ 0\|denominator cannot be zero` | domain_range_generator.py, log_equation_generator.py, logistic_growth_generator.py, probability_addition_rule_generator.py, rational_equation_generator.py, unit_circle_generator.py |
| `DOPPLER_FORMULA` | 1 | `DOPPLER_FORMULA\|f_obs=f*(v+v_observer)/(v-v_source)` | doppler_generator.py |
| `DOPPLER_SETUP` | 3 | `DOPPLER_SETUP\|acoustic_toward\|f=791, v=71\|v_observer=8, v_source=8` | doppler_generator.py |
| `DOT` | 2, 3 | `DOT\|(15, 20) · (3/5, 4/5)\|15*3/5 + 20*4/5\|25` | embedding_similarity_generator.py, feature_map_generator.py, fundamental_form_generator.py, gradient_generator.py, gram_schmidt_generator.py, kernel_evaluation_generator.py, line_integral_generator.py |
| `DOT4` | 4 | `DOT4\|gamma0gamma1\|(1,1)\|-1*0 + 0*0 + 0*1 + 0*0\|0` | gamma_matrix_generator.py |
| `DOT_FORMULA` | 1 | `DOT_FORMULA\|u·v = x1·x2 + y1·y2` | dot_product_generator.py |
| `DOUBLE_SETUP` | 2, 3 | `DOUBLE_SETUP\|integrand x^2 + y^2\|upper-half disk radius 6` | double_integral_generator.py |
| `DP_CELL` | 3 | `DP_CELL\|i=1,j=0\|base\|0` | dp_table_generator.py |
| `DP_COINS` | 1 | `DP_COINS\|1, 4, 6` | dp_table_generator.py |
| `DP_ITEMS` | 1 | `DP_ITEMS\|1:(w=2,v=6); 2:(w=1,v=10); 3:(w=5,v=6); 4:(w=3,v=8)` | dp_table_generator.py |
| `DP_ROW` | 2 | `DP_ROW\|i=0\|0, 0, 0, 0, 0, 0` | dp_table_generator.py |
| `DP_SETUP` | 2, 3 | `DP_SETUP\|LCS\|X=BCBA\|Y=BBDDB` | dp_table_generator.py |
| `D_POWER` | 2 | `D_POWER\|D^3\|[[-1, 0], [0, 27]]` | diagonalization_generator.py |
| `E` | 3 | `E\|6\|2\|36` | ac_circuit_generator.py, adam_step_generator.py, angle_defect_generator.py, annuity_generator.py, arc_sector_generator.py, backprop_generator.py, blackbody_generator.py, bond_pricing_generator.py, casimir_force_generator.py, casimir_generator.py, christoffel_generator.py, circle_equation_generator.py, complex_division_generator.py, complex_locus_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continuous_distribution_generator.py, de_moivre_generator.py, definite_integral_generator.py, density_matrix_generator.py, derivative_limit_def_generator.py, diagonalization_generator.py, distance_formula_generator.py, doppler_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, euler_formula_generator.py, exponential_equation_generator.py, exponential_model_generator.py, factor_special_forms_generator.py, feature_map_generator.py, finance_generator.py, four_vector_generator.py, fractal_iteration_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, invariant_mass_generator.py, kernel_evaluation_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, lagrangian_generator.py, laurent_series_generator.py, layer_norm_generator.py, limit_evaluation_generator.py, log_conversion_generator.py, log_equation_generator.py, log_properties_generator.py, low_rank_approx_generator.py, matrix_group_check_generator.py, matrix_norm_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, minkowski_interval_generator.py, mobius_transform_generator.py, named_distribution_generator.py, npv_irr_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_statistics_generator.py, particle_in_box_generator.py, pca_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polar_parametric_generator.py, portfolio_generator.py, projectile_motion_generator.py, pythag_hyp_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, set_operations_generator.py, shm_generator.py, spherical_excess_generator.py, spin_half_generator.py, stereographic_generator.py, svm_margin_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, uncertainty_generator.py, vector_ops_generator.py, wavefunction_generator.py, z_transform_generator.py |
| `EDGE_CHOOSE` | 3 | `EDGE_CHOOSE\|CE\|weight 4\|add C` | mst_generator.py |
| `EDGE_CONSIDER` | 2 | `EDGE_CONSIDER\|AE\|weight 1` | mst_generator.py |
| `EDGE_COUNT` | 2 | `EDGE_COUNT\|m\|6` | euler_circuit_generator.py, graph_counting_generator.py |
| `EDGE_LIST` | 1 | `EDGE_LIST\|AB, AC, AD, AE, BC, BD, BE, CD, CE, DE` | euler_circuit_generator.py |
| `EDGE_WEIGHT` | 2 | `EDGE_WEIGHT\|AB\|6` | dijkstra_generator.py, mst_generator.py |
| `EIGENPAIR` | 2 | `EIGENPAIR\|lambda = -3\|[2, 1]` | ode_system_generator.py |
| `EIGENVALUE` | 2 | `EIGENVALUE\|λ = 3\|p(3) = 0` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, svd_generator.py |
| `EIGENVALUES` | 2 | `EIGENVALUES\|A^T A\|64,25` | low_rank_approx_generator.py, matrix_norm_generator.py, pca_generator.py |
| `EIGENVECTOR` | 2 | `EIGENVECTOR\|A - 3I times v = 0\|[1, 0]` | diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, svd_generator.py |
| `EIGEN_CHECK` | 3 | `EIGEN_CHECK\|sigma_y psi\|-1*psi\|lambda=-1` | spin_half_generator.py |
| `EIGEN_MATRIX` | 2 | `EIGEN_MATRIX\|A - 3I\|[[0, 1], [0, 1]]` | eigenvalue_generator.py |
| `EINSTEIN_SETUP` | 2, 3 | `EINSTEIN_SETUP\|symmetrize\|T_ij=[[-3, -4], [2, -4]]` | einstein_summation_generator.py |
| `ELEC_FORMULA` | 1 | `ELEC_FORMULA\|V=sum(q_i/r_i)` | electrostatics_generator.py |
| `ELEC_SETUP` | 2, 3 | `ELEC_SETUP\|potential_axis\|q1=6, r1=8\|q2=-5, r2=8` | electrostatics_generator.py |
| `ELEMENT_ORDER` | 2 | `ELEMENT_ORDER\|9\|3` | cayley_table_generator.py |
| `ELEMENT_SCAN` | 3 | `ELEMENT_SCAN\|a\|in A=False, in B=False\|skip` | set_operations_generator.py |
| `ELIMINATE` | 1 | `ELIMINATE\|(m2-m1)g=(m1+m2)a` | newtons_laws_generator.py |
| `ELIMINATE_LAMBDA` | 2 | `ELIMINATE_LAMBDA\|f_x = f_y\|3*y = 3*x` | lagrange_multiplier_generator.py |
| `EL_EQUATION` | 1 | `EL_EQUATION\|d/dt(dL/dxdot)-dL/dx=0` | lagrangian_generator.py |
| `EL_SOLVE` | 2 | `EL_SOLVE\|xddot\|-12*x` | lagrangian_generator.py |
| `EMBED_SETUP` | 1 | `EMBED_SETUP\|A=(8,15), B=(5,12), C=(-3,4)` | embedding_similarity_generator.py |
| `ENERGY_FORMULA` | 1 | `ENERGY_FORMULA\|mgh=1/2*m*v^2` | energy_conservation_generator.py |
| `ENERGY_LEVEL` | 2 | `ENERGY_LEVEL\|E_27=hbar*omega*(n+1/2)\|385` | ladder_operator_generator.py |
| `ENERGY_SETUP` | 3 | `ENERGY_SETUP\|gravity_drop\|m=23\|h=180, g=10` | energy_conservation_generator.py |
| `ENERGY_TERM` | 1 | `ENERGY_TERM\|T=1/2*m*xdot^2` | lagrangian_generator.py |
| `ENGINE_FORMULA` | 1 | `ENGINE_FORMULA\|eta_C=1-Tc/Th=(Th-Tc)/Th` | heat_engine_generator.py |
| `ENGINE_SETUP` | 3 | `ENGINE_SETUP\|carnot_efficiency\|Th=758\|Tc=260` | heat_engine_generator.py |
| `ENQUEUE` | 3 | `ENQUEUE\|B\|from A\|B` | graph_traversal_generator.py |
| `ENTER` | 2 | `ENTER\|x\|most negative reduced cost -5` | simplex_generator.py |
| `ENTROPY_FORMULA` | 1 | `ENTROPY_FORMULA\|DeltaS_mix=-sum n_i ln(x_i)` | entropy_change_generator.py |
| `ENTROPY_SETUP` | 2, 3 | `ENTROPY_SETUP\|eigenvalues=[1/4,1/4,1/4,1/4]\|S=-sum lambda log2(lambda)` | entropy_change_generator.py, entropy_generator.py, huffman_coding_generator.py, information_gain_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `ENTROPY_SKIP` | 2 | `ENTROPY_SKIP\|H(X,Y)\|p=0` | mutual_information_generator.py |
| `ENTROPY_VALUE` | 2 | `ENTROPY_VALUE\|parent\|0.954375` | information_gain_generator.py |
| `ENTROPY_ZERO` | 2 | `ENTROPY_ZERO\|size_left\|count=0` | information_gain_generator.py |
| `EPSILON_VALUE` | 2 | `EPSILON_VALUE\|eps_123\|1` | index_gymnastics_generator.py |
| `EQUATE_EXP` | 1 | `EQUATE_EXP\|x + 4 = 2` | exponential_equation_generator.py |
| `EQUILIBRIA` | 2 | `EQUILIBRIA\|f(y) = 0\|y=-4, y=1, y=4` | stability_generator.py |
| `EQ_2PT_SETUP` | 2 | `EQ_2PT_SETUP\|(-9, 4)\|(-7, -6)` | equation_from_two_points_generator.py |
| `EQ_OP_BOTH` | 4 | `EQ_OP_BOTH\|multiply\|10\|x\|-40` | absolute_value_equation_generator.py, area_between_curves_generator.py, completing_square_generator.py, curve_analysis_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, implicit_diff_generator.py, inverse_function_generator.py, linear_fractional_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, mean_value_theorem_generator.py, one_step_equation_generator.py, optimization_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, separable_ode_generator.py, special_solution_equation_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_OP_NOTE` | 3 | `EQ_OP_NOTE\|subtract\|b\|from both sides` | equation_from_two_points_generator.py, literal_equation_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py, standard_form_conversion_generator.py |
| `EQ_RESULT` | 2 | `EQ_RESULT\|x\|-40` | completing_square_generator.py, error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, one_step_equation_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, special_solution_equation_generator.py, two_step_equation_generator.py |
| `EQ_SETUP` | 1, 2 | `EQ_SETUP\|x = 36/3` | area_between_curves_generator.py, completing_square_generator.py, complex_quadratic_generator.py, cramers_rule_generator.py, discriminant_generator.py, error_spotting_generator.py, exponential_equation_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_equation_generator.py, one_step_equation_generator.py, polynomial_zeros_generator.py, proportion_word_problem_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, rational_equation_generator.py, remainder_factor_theorem_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py, trig_equation_generator.py, two_step_equation_generator.py |
| `EQ_SIMPLIFY` | 1 | `EQ_SIMPLIFY\|3x = 18` | error_spotting_generator.py, fill_in_step_generator.py, linear_fractional_generator.py, two_step_equation_generator.py |
| `ESCAPE_CHECK` | 3 | `ESCAPE_CHECK\|n=1\|norm2=73/16\|escaped` | fractal_iteration_generator.py |
| `ESTIMATE` | 2 | `ESTIMATE\|23556 × 19779 ≈ 20000 × 20000\|400000000` | long_division_generator.py, multi_digit_multiplication_generator.py |
| `ESTIMATE_CHECK` | 3 | `ESTIMATE_CHECK\|1.2 × 10^4\|12288\|rounded estimate` | fermi_estimation_generator.py, long_division_generator.py, multi_digit_multiplication_generator.py |
| `EUCLID_DIV` | 4 | `EUCLID_DIV\|168\|78\|2\|12` | continued_fraction_generator.py, extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `EULER_BACKTRACK` | 3 | `EULER_BACKTRACK\|A\|route suffix A\|stack A-B-C-A-D-B-E` | euler_circuit_generator.py |
| `EULER_CRITERION` | 2 | `EULER_CRITERION\|103^18 mod 37\|36` | quadratic_residue_generator.py |
| `EULER_FORMULA` | 1 | `EULER_FORMULA\|χ = V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_NOTE` | 2 | `EULER_NOTE\|0\|the torus has a hole: χ = 0, not 2` | euler_characteristic_generator.py |
| `EULER_ROUTE` | 2 | `EULER_ROUTE\|A-B-C-A-D-B-E-C-D-E-A\|uses 10 edges` | euler_circuit_generator.py |
| `EULER_SETUP` | 2, 3 | `EULER_SETUP\|polyhedral torus grid: V = 36, E = 72, F = 36\|V - E + F` | euler_characteristic_generator.py, euler_formula_generator.py |
| `EULER_STACK` | 2 | `EULER_STACK\|initial\|A` | euler_circuit_generator.py |
| `EULER_START` | 2 | `EULER_START\|A\|alphabetically first vertex` | euler_circuit_generator.py |
| `EULER_TRAVERSE` | 3 | `EULER_TRAVERSE\|A->B\|AB\|stack A-B` | euler_circuit_generator.py |
| `EVAL` | 1, 2, 3 | `EVAL\|p(3)\|9` | arc_length_generator.py, area_between_curves_generator.py, circle_equation_generator.py, complex_division_generator.py, composite_arithmetic_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, determinant_generator.py, dot_product_generator.py, ellipse_features_generator.py, euler_method_generator.py, exact_ode_generator.py, five_number_summary_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, hyperbola_features_generator.py, improper_integral_generator.py, lagrange_multiplier_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_properties_generator.py, matrix_inverse_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, row_reduction_generator.py, runge_kutta_generator.py, solid_revolution_generator.py, standard_deviation_generator.py, tangent_line_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, vector_ops_generator.py |
| `EVAL_AT_ZERO` | 2 | `EVAL_AT_ZERO\|e^0=1\|e^(2*0)=1` | mgf_generator.py |
| `EVAL_PARTIAL` | 3 | `EVAL_PARTIAL\|f_x\|4*2 + 4*1 + 3\|15` | gradient_generator.py, multivar_chain_rule_generator.py |
| `EV_FORMULA` | 1 | `EV_FORMULA\|E[X] = Σ x·P(x)` | expected_value_generator.py |
| `EV_SETUP` | 2 | `EV_SETUP\|P(X=3) = 7/20; P(X=8) = 1/4; P(X=1) = 2/5\|Var(X)` | expected_value_generator.py |
| `EXACT_MATCH` | 2 | `EXACT_MATCH\|F_y = N\|g'(y) = 4*y + 1` | exact_ode_generator.py |
| `EXPAND` | 1 | `EXPAND\|cancel x^2 and y^2` | complex_locus_generator.py, mobius_transform_generator.py |
| `EXPECTATION` | 3 | `EXPECTATION\|E[X]=19/43\|E[Y]=19/43\|E[XY]=209/1849` | joint_distribution_generator.py |
| `EXPECTED_PAYOFF` | 1 | `EXPECTED_PAYOFF\|row1 against q` | game_theory_generator.py |
| `EXP_CELL` | 2 | `EXP_CELL\|(50·20)/100\|10` | chi_square_generator.py |
| `EXP_DIAG` | 2 | `EXP_DIAG\|e^(Dt)\|[[e^(-t), 0], [0, e^(2t)]]` | matrix_exponential_generator.py |
| `EXP_ENTRY` | 3 | `EXP_ENTRY\|(1,1)\|3*e^(-t) - 2*e^(2t)\|3*e^(-t) - 2*e^(2t)` | matrix_exponential_generator.py |
| `EXP_EXPAND` | 1 | `EXP_EXPAND\|(-4) × (-4)` | exponent_generator.py |
| `EXP_FORM` | 1 | `EXP_FORM\|e^(At) = P*e^(Dt)*P^-1` | euler_formula_generator.py, matrix_exponential_generator.py |
| `EXP_PARTIAL` | 3 | `EXP_PARTIAL\|-4\|-4\|16` | exponent_generator.py |
| `EXP_RULE_APPLY` | 4 | `EXP_RULE_APPLY\|subtract\|6\|5\|1` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_RULE_IDENTIFY` | 2 | `EXP_RULE_IDENTIFY\|zero_exponent\|x^0 = 1 (for x ≠ 0)` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SETUP` | 1 | `EXP_RULE_SETUP\|a^0` | exponent_generator.py, exponent_mixed_rules_generator.py, rational_exponent_generator.py |
| `EXP_RULE_SIMPLIFY` | 1 | `EXP_RULE_SIMPLIFY\|1` | exponent_generator.py, exponent_mixed_rules_generator.py |
| `EXP_SETUP` | 2 | `EXP_SETUP\|-4\|2` | exponent_generator.py |
| `EXP_SUB` | 3 | `EXP_SUB\|t/tau\|4\|e^-4` | transient_circuit_generator.py |
| `EXP_VALUE` | 2 | `EXP_VALUE\|exp(-z)\|1` | activation_generator.py |
| `EXT_GCD_SETUP` | 2 | `EXT_GCD_SETUP\|168\|78` | extended_euclid_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `F` | 2, 3 | `F\|9/9\|1` | composite_arithmetic_generator.py, fraction_op_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, order_of_operations_generator.py, quaternion_generator.py, radical_rationalize_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, repeating_decimal_generator.py, simple_probability_generator.py, slope_two_points_generator.py |
| `FACT` | 2 | `FACT\|12\|479001600` | named_distribution_generator.py, order_statistics_generator.py, young_tableaux_generator.py |
| `FACTOR` | 1, 2 | `FACTOR\|r^2 + 2r - 8\|(r + 4)(r - 2) = 0` | second_order_ode_generator.py, transfer_function_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `FACTOR_FORM` | 2 | `FACTOR_FORM\|35\|5 * 7` | totient_generator.py |
| `FACTOR_FOUND` | 2 | `FACTOR_FOUND\|5\|1` | totient_generator.py |
| `FACTOR_GROUP` | 3 | `FACTOR_GROUP\|6x^2 - 15x\|3x\|(2x - 5)` | conic_standard_form_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, factor_grouping_generator.py, factor_trinomial_generator.py |
| `FACTOR_PAIR_GOAL` | 2 | `FACTOR_PAIR_GOAL\|m·n = -45\|m + n = -4` | factor_trinomial_generator.py |
| `FACTOR_SETUP` | 1 | `FACTOR_SETUP\|35` | totient_generator.py |
| `FACT_CHECK` | 3 | `FACT_CHECK\|107\|1\|0` | factors_generator.py |
| `FACT_FORMULA` | 1 | `FACT_FORMULA\|5! = 1·2·3·4·5` | permutation_combination_generator.py |
| `FACT_PAIR` | 2 | `FACT_PAIR\|1\|107` | factors_generator.py |
| `FACT_SETUP` | 2 | `FACT_SETUP\|5!\|expand the factorial` | permutation_combination_generator.py |
| `FACT_VALUE` | 2 | `FACT_VALUE\|5!\|120` | stars_and_bars_generator.py |
| `FEATURE_MAP_SETUP` | 3 | `FEATURE_MAP_SETUP\|K(x,z)=(xz+2)^2\|phi(t)=(t^2,2t,2)\|x=-15,z=-8` | feature_map_generator.py |
| `FEATURE_VECTOR` | 2 | `FEATURE_VECTOR\|phi(x)\|(225,-30,2)` | feature_map_generator.py |
| `FEEDBACK` | 1 | `FEEDBACK\|T=G/(1+G)` | transfer_function_generator.py |
| `FERMAT_SETUP` | 3 | `FERMAT_SETUP\|prime 19\|base 15\|exponent 177` | totient_generator.py |
| `FERMI_FACTOR` | 2 | `FERMI_FACTOR\|sections\|24` | fermi_estimation_generator.py |
| `FERMI_SETUP` | 2 | `FERMI_SETUP\|stadium seats\|seats` | fermi_estimation_generator.py |
| `FIELD_SETUP` | 2 | `FIELD_SETUP\|Z_2[x]\|mod 2` | finite_field_generator.py |
| `FIND_SLOPE` | 2 | `FIND_SLOPE\|Given slope (m1)\|3` | parallel_perpendicular_line_generator.py |
| `FINITE_DIFF_SETUP` | 3 | `FINITE_DIFF_SETUP\|forward_derivative\|x0=2,h=1\|f0=12,f1=14` | finite_difference_generator.py |
| `FIN_FORMULA` | 1 | `FIN_FORMULA\|I = P*r*t; A = P + I` | finance_generator.py |
| `FIN_SETUP` | 3 | `FIN_SETUP\|simple interest P = 300\|r = 5%, t = 4\|interest and balance` | finance_generator.py |
| `FIRSTLAW_FORMULA` | 1 | `FIRSTLAW_FORMULA\|W=P*(V2-V1)` | first_law_generator.py |
| `FIRSTLAW_SETUP` | 3 | `FIRSTLAW_SETUP\|isobaric\|P=13, V1=8, V2=5\|Q=115` | first_law_generator.py |
| `FIXED_EQ` | 1 | `FIXED_EQ\|z=(az+b)/(cz+d)` | mobius_transform_generator.py |
| `FIXED_POINT` | 1 | `FIXED_POINT\|-5` | mobius_transform_generator.py |
| `FIXED_POINT_SETUP` | 3 | `FIXED_POINT_SETUP\|g(x)=-1/2*x-8/5\|x0=3/2\|iterations=3` | fixed_point_generator.py |
| `FIXED_POINT_UPDATE` | 3 | `FIXED_POINT_UPDATE\|1\|x_0=3/2\|x_1=-47/20` | fixed_point_generator.py |
| `FLAG` | 2 | `FLAG\|4\|11 × 9 = 99, not 90` | error_spotting_generator.py |
| `FLOOR_DIV` | 3 | `FLOOR_DIV\|6\|2\|3` | algorithm_trace_generator.py |
| `FLOPS_SETUP` | 2 | `FLOPS_SETUP\|rule=2mnk\|m=64,d=256,h=2048,o=128` | flops_memory_generator.py |
| `FLUX_SUM` | 2 | `FLUX_SUM\|(0 - 4 + 5)*360\|360` | vector_theorem_generator.py |
| `FOCUS` | 1 | `FOCUS\|(1, -2)` | ellipse_features_generator.py, hyperbola_features_generator.py, parabola_features_generator.py |
| `FOIL_F` | 2 | `FOIL_F\|First: (-7) * (-2)\|14` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_I` | 2 | `FOIL_I\|Inner: (-8i) * (-2)\|16i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_L` | 2 | `FOIL_L\|Last: (-8i) * 9i\|-72i^2` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_O` | 2 | `FOIL_O\|Outer: (-7) * 9i\|-63i` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py |
| `FOIL_SETUP` | 1 | `FOIL_SETUP\|(2 + √6)(6 + √6)` | complex_division_generator.py, complex_number_ops_generator.py, multiplying_binomials_generator.py, radical_multiply_generator.py, trig_identity_verify_generator.py |
| `FORCE_COMPONENT` | 1 | `FORCE_COMPONENT\|parallel=m*g*sin` | newtons_laws_generator.py |
| `FORCE_EQ` | 1 | `FORCE_EQ\|T-m1*g=m1*a` | newtons_laws_generator.py |
| `FORMULA` | 1, 2 | `FORMULA\|sinh x = (e^x - e^(-x))/2` | collision_generator.py, gaussian_curvature_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, or_formula_generator.py, projectile_motion_generator.py, stereographic_generator.py, uncertainty_generator.py |
| `FORM_IDENTIFY` | 2 | `FORM_IDENTIFY\|difference_of_squares\|a^2 - b^2 = (a - b)(a + b)` | completing_square_generator.py, conic_standard_form_generator.py, ellipse_features_generator.py, factor_special_forms_generator.py, hyperbola_features_generator.py, parabola_features_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py |
| `FOURIER_COEF` | 1 | `FOURIER_COEF\|b_9=14/9` | fourier_series_generator.py |
| `FOURIER_SETUP` | 3 | `FOURIER_SETUP\|sawtooth\|A=7\|n=9` | fourier_series_generator.py |
| `FOUR_VECTOR_SETUP` | 3 | `FOUR_VECTOR_SETUP\|signature=+---\|p=[3,1,-4,0]\|q=[8,1,-5,8]` | four_vector_generator.py |
| `FRACTAL_SETUP` | 4 | `FRACTAL_SETUP\|julia\|z0=(-1/2,-1)\|c=(3/2,1)\|N=6` | fractal_iteration_generator.py |
| `FRAC_BUILD` | 2 | `FRAC_BUILD\|20/33\|20/33` | conditional_probability_generator.py, geometric_probability_generator.py |
| `FRAC_REDUCE` | 2 | `FRAC_REDUCE\|-17/-16\|17/16` | angle_measure_generator.py, arc_length_generator.py, arc_sector_generator.py, complex_division_generator.py, frequency_table_generator.py, function_operations_generator.py, hyperbola_features_generator.py, implicit_diff_generator.py, improper_integral_generator.py, probability_addition_rule_generator.py, related_rates_generator.py, right_triangle_trig_generator.py |
| `FRAC_TO_DEC` | 2 | `FRAC_TO_DEC\|2/6\|0.3333333333` | fraction_decimal_percent_converter.py |
| `FREQ_SETUP` | 2 | `FREQ_SETUP\|table — Red: 3, Blue: 4, Green: 6, Yellow: 2\|total count` | frequency_table_generator.py |
| `FUNC_OP` | 2 | `FUNC_OP\|(p + q)(3)\|p(3) + q(3)` | function_composition_generator.py, function_operations_generator.py |
| `FUNC_SETUP` | 2 | `FUNC_SETUP\|x: -4, -3, -2, -1, 5; f(x): 17, 16, 5, -15, -9\|f(-4)` | domain_range_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, inverse_function_generator.py, piecewise_evaluation_generator.py, rational_function_features_generator.py |
| `FUNDAMENTAL_FORM_SETUP` | 3 | `FUNDAMENTAL_FORM_SETUP\|sphere\|R=2\|theta in [0,3pi/4], phi in [60,180]` | fundamental_form_generator.py |
| `GAME_SETUP` | 2 | `GAME_SETUP\|payoffs=(9,7;7,8)\|row player maximizes, column player minimizes` | game_theory_generator.py |
| `GAMMA_SETUP` | 3 | `GAMMA_SETUP\|trace\|gamma0,gamma1\|Tr(product)` | gamma_matrix_generator.py |
| `GAS_FORMULA` | 1 | `GAS_FORMULA\|P1*V1/T1=P2*V2/T2` | gas_law_generator.py, gas_stoichiometry_generator.py |
| `GAS_SETUP` | 3 | `GAS_SETUP\|combined_pressure\|P1=8, V1=9, T1=6\|V2=1, T2=15` | gas_law_generator.py |
| `GAS_STOICH_SETUP` | 3 | `GAS_STOICH_SETUP\|gas_to_mass\|2 H2 + O2 -> 2 H2O\|gas=H2, target=H2O` | gas_stoichiometry_generator.py |
| `GATE_MATRIX` | 2 | `GATE_MATRIX\|CNOT\|ket00bra00+ket01bra01+ket11bra10+ket10bra11` | quantum_gate_generator.py |
| `GAUSSIAN_CURVATURE_SETUP` | 2, 3 | `GAUSSIAN_CURVATURE_SETUP\|sphere\|R=133` | gaussian_curvature_generator.py |
| `GAUSS_BONNET_SETUP` | 3 | `GAUSS_BONNET_SETUP\|sphere\|R=5\|chi=2` | gauss_bonnet_generator.py |
| `GAUSS_FORMULA` | 1 | `GAUSS_FORMULA\|E*(2πrL)=lambda*L` | gauss_law_generator.py |
| `GAUSS_SETUP` | 3 | `GAUSS_SETUP\|line_charge\|lambda=9, r=9\|L=2` | gauss_law_generator.py |
| `GCD_RESULT` | 1, 2 | `GCD_RESULT\|2` | lcm_generator.py, modular_inverse_generator.py, permutation_group_generator.py, rsa_generator.py, totient_generator.py |
| `GCD_START` | 2 | `GCD_START\|35\|61` | gcf_generator.py, lcm_generator.py |
| `GCD_STEP` | 3 | `GCD_STEP\|35\|61\|35` | gcf_generator.py, lcm_generator.py |
| `GCF_COEFF` | 2 | `GCF_COEFF\|6, 12, 24\|6` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_RESULT` | 1 | `GCF_RESULT\|6x^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GCF_VAR` | 2 | `GCF_VAR\|x^5, x^3, x^2\|x^2` | factor_gcf_generator.py, quadratic_factoring_generator.py, rational_expr_simplify_generator.py |
| `GD_SETUP` | 3 | `GD_SETUP\|f(x,y)=1/2*(5x^2+5y^2)\|start=(7,4)\|eta=1/13` | gradient_descent_generator.py |
| `GD_UPDATE` | 3 | `GD_UPDATE\|w_old=(0,2)\|eta=1/7\|w_new=(-3/7,6/7)` | gradient_step_generator.py |
| `GELLMANN_IDENTITY` | 3 | `GELLMANN_IDENTITY\|Tr(lambda_7 lambda_2)\|2 delta_ab\|0` | pauli_algebra_generator.py |
| `GELLMANN_SETUP` | 3 | `GELLMANN_SETUP\|trace\|A=lambda_7\|B=-lambda_2` | pauli_algebra_generator.py |
| `GENERAL` | 2 | `GENERAL\|a_n\|C1(2)^n + C2(3)^n + 4` | recurrence_generator.py |
| `GEOMETRIC_FORMULA` | 2 | `GEOMETRIC_FORMULA\|c_n = A*(-1)^n/d^(n+1)\|A=5, d=5` | laurent_series_generator.py |
| `GEOM_FORMULA` | 1 | `GEOM_FORMULA\|P(X=k) = (1-p)^(k-1) * p` | geometric_distribution_generator.py |
| `GEOM_SETUP` | 2 | `GEOM_SETUP\|p = 3/10, q = 7/10\|P(X = 8)` | geometric_distribution_generator.py |
| `GEO_PROB_FORMULA` | 1 | `GEO_PROB_FORMULA\|probability = favorable length / total length` | geometric_probability_generator.py |
| `GEO_PROB_SETUP` | 2 | `GEO_PROB_SETUP\|number line from 0 to 33\|lands between 11 and 31` | geometric_probability_generator.py |
| `GEO_SETUP` | 2 | `GEO_SETUP\|right triangle, altitude to hypotenuse; segments p = 4 (adjacent to the leg) and q = 9\|the leg adjacent to p` | geometric_mean_generator.py |
| `GF2_XOR` | 3 | `GF2_XOR\|quotient x\|0 xor 1\|1` | finite_field_generator.py |
| `GF_DIV_CHECK` | 3 | `GF_DIV_CHECK\|23 / 4\|not integer\|reject` | generating_function_generator.py |
| `GF_EXPAND` | 2 | `GF_EXPAND\|1/(1 - x^3)\|sum x^(3i), i >= 0` | generating_function_generator.py |
| `GF_SETUP` | 2 | `GF_SETUP\|[x^23]\|1/((1 - x^3)(1 - x^4))` | generating_function_generator.py |
| `GOAL` | 1 | `GOAL\|Convert to Slope-Intercept Form (y = mx + b)` | point_slope_generator.py, standard_form_conversion_generator.py |
| `GRAD` | 2 | `GRAD\|1\|7/15` | softmax_gradient_generator.py |
| `GRADIENT_FORMULA` | 1 | `GRADIENT_FORMULA\|grad=(5x,5y)` | gradient_descent_generator.py, matrix_calculus_generator.py |
| `GRAD_ENTRY` | 2 | `GRAD_ENTRY\|g1\|6` | matrix_calculus_generator.py |
| `GRAD_RESULT` | 2 | `GRAD_RESULT\|grad g\|(1, 1)` | lagrange_multiplier_generator.py |
| `GRAD_SETUP` | 3 | `GRAD_SETUP\|f(x,y) = 2*x^2 + 3*y^2 + 4*x*y + 3*x + 6*y\|point (2, 1)\|directional` | gradient_generator.py |
| `GRAPH_CHANGE` | 3 | `GRAPH_CHANGE\|2018\|2019\|-1` | graph_interpret_generator.py |
| `GRAPH_DATA` | 2 | `GRAPH_DATA\|bar_chart\|Blue:34,Purple:32,Green:7,Red:26,Orange:7` | graph_interpret_generator.py |
| `GRAPH_MAX` | 2 | `GRAPH_MAX\|Sat\|29` | graph_interpret_generator.py |
| `GRAPH_MAX_CHANGE` | 3 | `GRAPH_MAX_CHANGE\|2023\|2024\|-2` | graph_interpret_generator.py |
| `GRAPH_MIN` | 2 | `GRAPH_MIN\|Red\|7` | graph_interpret_generator.py |
| `GRAPH_READ` | 2 | `GRAPH_READ\|Green\|7` | graph_interpret_generator.py |
| `GRAPH_SETUP` | 2 | `GRAPH_SETUP\|vertices A, B, C, D, E\|edges AD, BC, BD, BE, CD, CE` | dijkstra_generator.py, euler_circuit_generator.py, graph_counting_generator.py, graph_traversal_generator.py |
| `GRASSMANN_RESULT` | 3 | `GRASSMANN_RESULT\|constant=24\|theta=-45\|24 - 45theta` | grassmann_generator.py |
| `GRASSMANN_SETUP` | 3 | `GRASSMANN_SETUP\|multiply\|x=3 - 6theta\|y=8 + theta` | grassmann_generator.py |
| `GREAT_CIRCLE_SETUP` | 3 | `GREAT_CIRCLE_SETUP\|R=12\|A=(90,-90)\|B=(0,30)` | great_circle_generator.py |
| `GROUP` | 2 | `GROUP\|(6x^2 - 15x)\|(2x - 5)` | factor_grouping_generator.py, factor_trinomial_generator.py |
| `GROUP_MULT` | 3 | `GROUP_MULT\|e\|e\|e` | coset_generator.py |
| `GROUP_SETUP` | 2, 3 | `GROUP_SETUP\|U(28)\|multiplication mod n` | cayley_table_generator.py, coset_generator.py, cyclic_group_generator.py |
| `GS_SETUP` | 2 | `GS_SETUP\|vectors [[4, 2, 0], [13, 4, 0], [-3, -4, 1]]\|orthogonal basis, not normalized` | gram_schmidt_generator.py |
| `GS_SUBTRACT` | 2 | `GS_SUBTRACT\|remove projection on u1\|[1, -2, 0]` | gram_schmidt_generator.py |
| `GS_VECTOR` | 2 | `GS_VECTOR\|u1 = v1\|[4, 2, 0]` | gram_schmidt_generator.py |
| `HA` | 1 | `HA\|y = 1` | rational_function_features_generator.py |
| `HAMILTON` | 2 | `HAMILTON\|i*i\|-1` | quaternion_generator.py |
| `HAMILTONIAN` | 1 | `HAMILTONIAN\|H=p_theta^2/(2mL^2)+mgL*(1-cos(theta))` | hamiltonian_generator.py |
| `HAMMING_PLACE` | 2 | `HAMMING_PLACE\|positions 1,2,3,4,5,6,7\|p1,p2,d1,p4,d2,d3,d4` | hamming_code_generator.py |
| `HAMMING_RECEIVED` | 1 | `HAMMING_RECEIVED\|r=0100100` | hamming_code_generator.py |
| `HAMMING_SETUP` | 2 | `HAMMING_SETUP\|data=1111\|even parity` | hamming_code_generator.py |
| `HAM_EQ` | 2 | `HAM_EQ\|thetadot=dH/dp_theta\|thetadot=p_theta/36` | hamiltonian_generator.py |
| `HAM_SETUP` | 3 | `HAM_SETUP\|pendulum\|m=4, L=3\|g=10, q=theta` | hamiltonian_generator.py |
| `HARMONIC_SETUP` | 1 | `HARMONIC_SETUP\|u=3x^2 - 3y^2 + x - 3y` | cauchy_riemann_generator.py |
| `HAWKING_SETUP` | 3 | `HAWKING_SETUP\|temperature\|T_H=hbar*c^3/(8π*G*M*k_B)\|hbar=7,c=4,G=11,M=6,k_B=5` | hawking_generator.py |
| `HESSIAN_DET` | 3 | `HESSIAN_DET\|D = f_xx*f_yy - f_xy^2\|10*10 - 3^2\|91` | hessian_classify_generator.py |
| `HESSIAN_SETUP` | 2 | `HESSIAN_SETUP\|f(x,y) = 5*x^2 + 5*y^2 + 3*x*y - 36*x - 29*y\|find and classify the critical point` | hessian_classify_generator.py |
| `HESSIAN_TEST` | 3 | `HESSIAN_TEST\|D = 91\|f_xx = 10\|local minimum` | hessian_classify_generator.py |
| `HIDDEN_PRE` | 2 | `HIDDEN_PRE\|h1\|z=3` | backprop_generator.py |
| `HIT_EQ` | 2 | `HIT_EQ\|t0=1+p00*t0+p01*t1\|t1=1+p10*t0+p11*t1` | markov_chain_generator.py |
| `HOLE` | 1 | `HOLE\|x = 2` | rational_function_features_generator.py |
| `HOM_SOL` | 2 | `HOM_SOL\|y_h\|y_h = C1e^(-x) + C2e^(3x)` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `HOOK` | 4 | `HOOK\|(1,1)\|right=4\|below=4\|hook=9` | young_tableaux_generator.py |
| `HORNER_SETUP` | 2 | `HORNER_SETUP\|-2x^3 + 5x^2 - 3x + 3\|x = -2` | horner_evaluation_generator.py |
| `HT_SETUP` | 2 | `HT_SETUP\|H0: μ = 88; Ha: μ ≠ 88\|n = 100, x̄ = 83, s = 25, critical value = 2.576` | hypothesis_test_generator.py |
| `HUFFMAN_FORMULA` | 1 | `HUFFMAN_FORMULA\|L=sum p_i*l_i` | huffman_coding_generator.py |
| `HUFFMAN_MERGE` | 2 | `HUFFMAN_MERGE\|A:1/4 + B:1/4\|AB:1/2` | huffman_coding_generator.py |
| `HUFFMAN_SETUP` | 1 | `HUFFMAN_SETUP\|A=1/4, B=1/4, C=1/4, D=1/4` | huffman_coding_generator.py |
| `HYDROGEN_FORMULA` | 1 | `HYDROGEN_FORMULA\|Delta_E=R_E*(1/n_low^2-1/n_high^2)` | hydrogen_atom_generator.py |
| `HYDROGEN_SETUP` | 3 | `HYDROGEN_SETUP\|transition_energy\|n_low=1, n_high=8\|R_E=20 eV` | hydrogen_atom_generator.py |
| `HYPERBOLIC_DISTANCE_SETUP` | 3 | `HYPERBOLIC_DISTANCE_SETUP\|disk\|P=(0,0)\|Q=(7/39,0)` | hyperbolic_distance_generator.py |
| `HYPERBOLIC_SETUP` | 2 | `HYPERBOLIC_SETUP\|e^x=31/24\|e^(-x)=24/31` | hyperbolic_function_generator.py |
| `HYPERCUBE_FORMULA` | 1 | `HYPERCUBE_FORMULA\|k-faces of the n-cube: C(n,k) · 2^(n-k)` | hypercube_counting_generator.py |
| `HYPERCUBE_SETUP` | 2 | `HYPERCUBE_SETUP\|4-cube\|number of vertices (k = 0)` | hypercube_counting_generator.py |
| `I` | 2 | `I\|3/2\|2/3` | fraction_op_generator.py, mixed_number_operation_generator.py, rational_expr_mult_div_generator.py |
| `IDENTIFY` | 2 | `IDENTIFY\|order matters\|use P(n, r)` | permutation_combination_generator.py |
| `IDENTITY` | 2 | `IDENTITY\|cos(4x)*cos(13x)\|1/2(cos(9x) + cos(17x))` | function_inner_product_generator.py, index_gymnastics_generator.py |
| `IDENTITY_SETUP` | 2 | `IDENTITY_SETUP\|verify: (sin β + cos β)^2 = 1 + 2 sin β cos β\|transform the left side` | trig_identity_verify_generator.py |
| `IDENT_MATCH` | 1 | `IDENT_MATCH\|1 + 2 sin β cos β = 1 + 2 sin β cos β` | trig_identity_verify_generator.py |
| `IDENT_SUB` | 1 | `IDENT_SUB\|sin^2 β + cos^2 β = 1` | parametric_calculus_generator.py, trig_identity_verify_generator.py |
| `IE_FORMULA` | 2 | `IE_FORMULA\|n(A union B union C)\|n(A)+n(B)+n(C) - n(AB)-n(AC)-n(BC) + n(ABC)` | inclusion_exclusion_generator.py |
| `IE_SETUP` | 2 | `IE_SETUP\|n(A)=24, n(B)=22, n(C)=17\|n(AB)=6, n(AC)=6, n(BC)=5, n(ABC)=1` | inclusion_exclusion_generator.py |
| `IFACTOR` | 2 | `IFACTOR\|mu = e^(∫ 3 dx)\|e^(3x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `IG_SETUP` | 3 | `IG_SETUP\|parent pos=6, neg=10\|total=16\|splits=source,shape` | information_gain_generator.py |
| `IMAGE` | 2 | `IMAGE\|T(-2)\|-2` | mobius_transform_generator.py |
| `IMPLICIT_DIFF` | 2 | `IMPLICIT_DIFF\|d/dx of x^3\|3x^2` | implicit_diff_generator.py, log_diff_higher_order_generator.py, related_rates_generator.py |
| `IMPLICIT_SETUP` | 2 | `IMPLICIT_SETUP\|x^3 + y^3 = 91\|dy/dx` | implicit_diff_generator.py |
| `IMPROPER_TO_MIX` | 2 | `IMPROPER_TO_MIX\|75/14\|5 5/14` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `INDEGREE` | 2 | `INDEGREE\|A\|0` | graph_traversal_generator.py |
| `INDEGREE_UPDATE` | 2 | `INDEGREE_UPDATE\|B\|0` | graph_traversal_generator.py |
| `INDEP_CHECK` | 3 | `INDEP_CHECK\|P11=209/1849\|product=361/1849\|no` | joint_distribution_generator.py |
| `INDEP_FORMULA` | 1 | `INDEP_FORMULA\|independent iff P11=P(X=1)P(Y=1)` | joint_distribution_generator.py |
| `INDEX` | 3 | `INDEX\|G size 12\|H size 6\|2` | coset_generator.py |
| `INDEX_METRIC` | 3 | `INDEX_METRIC\|lower\|Minkowski\|g_ii=[-1,1,1,1]` | index_raising_generator.py |
| `INDEX_SETUP` | 3 | `INDEX_SETUP\|c=2\|j=2, k=3\|l=1, m=1` | index_gymnastics_generator.py |
| `INEQ_FLIP` | 1 | `INEQ_FLIP\|Dividing by negative number reverses inequality` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_OP_ALL` | 3 | `INEQ_OP_ALL\|subtract\|5\|-25 < 1x < 15` | absolute_value_inequality_generator.py, compound_inequality_generator.py |
| `INEQ_OP_BOTH` | 4 | `INEQ_OP_BOTH\|multiply\|3\|x\|-6` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_RESULT` | 3 | `INEQ_RESULT\|x\|<\|-6` | domain_range_generator.py, linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SETUP` | 1 | `INEQ_SETUP\|x/3 < -2` | linear_fractional_generator.py, one_step_inequality_generator.py, two_step_inequality_generator.py |
| `INEQ_SIMPLIFY` | 1 | `INEQ_SIMPLIFY\|-4x ≤ 28` | domain_range_generator.py, two_step_inequality_generator.py |
| `INFO_GAIN` | 2 | `INFO_GAIN\|source\|0` | information_gain_generator.py |
| `INFO_SETUP` | 2 | `INFO_SETUP\|p=1/32\|I=-log2(p)` | entropy_generator.py |
| `INFO_TABLE` | 1 | `INFO_TABLE\|1/8=3, 3/8=1.415, 5/8=0.678, 7/8=0.193` | information_gain_generator.py |
| `INFO_VALUE` | 2 | `INFO_VALUE\|p=3/8\|I=1.415` | information_gain_generator.py |
| `INITIAL` | 2 | `INITIAL\|D_0 = 1\|D_1 = 0` | derangement_generator.py |
| `INITIAL_COEFF` | 2 | `INITIAL_COEFF\|a_0\|4080` | series_solution_generator.py |
| `INITIAL_EQ` | 2 | `INITIAL_EQ\|C1 + C2\|-5` | recurrence_generator.py |
| `INITIAL_SYSTEM` | 2 | `INITIAL_SYSTEM\|C1[2, 1] + C2[1, 1]\|[-3, 0]` | ode_system_generator.py |
| `INNER_ANTIDERIV` | 2 | `INNER_ANTIDERIV\|dr\|r^4/4` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_EVAL` | 2, 3 | `INNER_EVAL\|r=0..6\|6^4/4\|324` | double_integral_generator.py, triple_integral_generator.py |
| `INNER_PRODUCT` | 2 | `INNER_PRODUCT\|inner(phi,psi)\|3-3i` | braket_generator.py |
| `INNER_PRODUCT_SETUP` | 3 | `INNER_PRODUCT_SETUP\|interval=[0,2pi]\|f=cos(4x)\|g=cos(13x)` | function_inner_product_generator.py |
| `INSERT_KEY` | 3 | `INSERT_KEY\|pass 1\|13\|index 1` | algorithm_trace_generator.py |
| `INSERT_PLACE` | 2 | `INSERT_PLACE\|index 1\|2, 13, 29, 30, 38, 6, 11` | algorithm_trace_generator.py |
| `INTEGRAL` | 1, 2 | `INTEGRAL\|integral cos(9x) on [0,2pi]\|0` | fourier_series_generator.py, function_inner_product_generator.py, legendre_construction_generator.py |
| `INTEGRAL_SETUP` | 1 | `INTEGRAL_SETUP\|L = integral from r0 to r1 of 1 dr` | metric_arc_length_generator.py |
| `INTEGRATE` | 2 | `INTEGRATE\|v_y = u_x\|v=6xy + 3x + y + phi(x)` | cauchy_riemann_generator.py |
| `INTEGRATION_BY_PARTS` | 2 | `INTEGRATION_BY_PARTS\|u=x\|dv=sin(nx)dx` | fourier_series_generator.py |
| `INTEG_RULE` | 2 | `INTEG_RULE\|power rule\|∫ x^n dx = x^(n+1)/(n+1) + C` | antiderivative_generator.py, definite_integral_generator.py, ode_substitution_generator.py, partial_fractions_generator.py, separable_ode_generator.py, solid_revolution_generator.py, u_substitution_generator.py |
| `INTEG_SETUP` | 2 | `INTEG_SETUP\|∫ (-16x^3 - 8x) dx\|antiderivative` | antiderivative_generator.py, arc_length_generator.py, definite_integral_generator.py, improper_integral_generator.py, integration_by_parts_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, u_substitution_generator.py |
| `INTERCEPT_FORMULA` | 1 | `INTERCEPT_FORMULA\|a = ȳ - b·x̄` | regression_generator.py |
| `INTERFERENCE_FORMULA` | 1 | `INTERFERENCE_FORMULA\|d*sin(theta)=m*lambda` | interference_generator.py |
| `INTERFERENCE_SETUP` | 3 | `INTERFERENCE_SETUP\|diffraction_grating\|m=5, lambda=16\|d=127` | interference_generator.py |
| `INTERP_SETUP` | 3 | `INTERP_SETUP\|newton\|points=(-1,4), (4,-41), (5,-62)\|x=-3` | interpolation_generator.py |
| `INTERVAL_CLASS` | 2 | `INTERVAL_CLASS\|s2=-392\|spacelike` | minkowski_interval_generator.py |
| `INT_ABS` | 2 | `INT_ABS\|8\|8` | integer_operations_generator.py |
| `INT_ALIGN` | 2 | `INT_ALIGN\|82320\|65750` | multi_digit_addition_generator.py, multi_digit_subtraction_generator.py |
| `INT_APPLY_SIGN` | 3 | `INT_APPLY_SIGN\|72\|negative\|-72` | integer_operations_generator.py |
| `INT_OP` | 4 | `INT_OP\|×\|8\|9\|72` | integer_operations_generator.py |
| `INT_REWRITE` | 2 | `INT_REWRITE\|15 - 17\|15 + (-17)` | integer_operations_generator.py |
| `INT_SIGN_RULE` | 2 | `INT_SIGN_RULE\|mult_different_signs\|Different signs: positive × negative = negative` | integer_operations_generator.py |
| `INVERSE_LAPLACE` | 2 | `INVERSE_LAPLACE\|-4/(s + 2)\|-4e^(-2t)` | laplace_ivp_generator.py |
| `INVERSE_MAP` | 2 | `INVERSE_MAP\|x=(u+v)/2\|y=(u-v)/2` | rv_transform_generator.py |
| `INVERSE_METRIC` | 2 | `INVERSE_METRIC\|g^rr=1\|g^thetatheta=1/r^2` | christoffel_generator.py, riemann_tensor_generator.py |
| `INV_FORMULA` | 1 | `INV_FORMULA\|A⁻¹ = (1/det)·[[d, -b], [-c, a]]` | matrix_inverse_generator.py |
| `IRR_SETUP` | 2 | `IRR_SETUP\|c0=-2000,c1=3000\|r0=1/5,iterations=2` | npv_irr_generator.py |
| `IRR_VALUE` | 2 | `IRR_VALUE\|f1\|500` | npv_irr_generator.py |
| `ITERATE` | 2 | `ITERATE\|n=1\|z=(3/4,2)` | fractal_iteration_generator.py, gradient_descent_generator.py |
| `IVT_SETUP` | 2 | `IVT_SETUP\|f(x) = x^3 - 2x + 2 on [2, 6]\|does the IVT guarantee a root?` | mean_value_theorem_generator.py |
| `I_CYCLE` | 2 | `I_CYCLE\|i^0\|1` | complex_number_ops_generator.py |
| `I_SQUARE` | 2 | `I_SQUARE\|-72i^2\|72` | complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py |
| `JACOBIAN` | 2 | `JACOBIAN\|dA\|r dr dtheta` | double_integral_generator.py |
| `JAC_DET` | 3 | `JAC_DET\|x_u*y_v - x_v*y_u\|4*4 - (-4)*1\|20` | jacobian_generator.py |
| `JAC_MATRIX` | 2 | `JAC_MATRIX\|[[x_u, x_v], [y_u, y_v]]\|[[4, -4], [1, 4]]` | jacobian_generator.py, rv_transform_generator.py |
| `JAC_SETUP` | 3 | `JAC_SETUP\|x = 4*u - 4*v\|y = u + 4*v\|d(x,y)/d(u,v)` | jacobian_generator.py |
| `JOINT_SETUP` | 3 | `JOINT_SETUP\|X,Y in {0,1}\|p00=424/1849, p01=608/1849\|p10=608/1849, p11=209/1849` | joint_distribution_generator.py |
| `KERNEL_BASE` | 3 | `KERNEL_BASE\|A,A\|dot+c=8+2\|10` | feature_map_generator.py, kernel_evaluation_generator.py |
| `KERNEL_EXPONENT` | 2 | `KERNEL_EXPONENT\|A,A\|0` | kernel_evaluation_generator.py |
| `KERNEL_SETUP` | 3 | `KERNEL_SETUP\|type=rbf\|points=A=(-3,0), B=(1,0)\|gamma=1` | kernel_evaluation_generator.py |
| `KERNEL_VALIDITY` | 1 | `KERNEL_VALIDITY\|psd=false` | kernel_validity_generator.py |
| `KERNEL_VALUE` | 2 | `KERNEL_VALUE\|A,A\|1` | feature_map_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py |
| `KIN_FORMULA` | 1 | `KIN_FORMULA\|t = d/v` | invariant_mass_generator.py, kinematics_generator.py |
| `KIN_SETUP` | 3, 4 | `KIN_SETUP\|d = 168 kilometers\|v = 56 km/hour\|time` | invariant_mass_generator.py, kinematics_generator.py |
| `KL_FORMULA` | 1 | `KL_FORMULA\|D=sum source_i*log2(source_i/target_i)` | kl_divergence_generator.py |
| `KL_SETUP` | 3 | `KL_SETUP\|P=[256/511,255/511]\|Q=[1/511,510/511]\|direction=Q to P` | kl_divergence_generator.py |
| `KMAP_GROUP` | 2 | `KMAP_GROUP\|00, 01\|NOT A` | boolean_algebra_generator.py |
| `KMAP_ROW` | 2 | `KMAP_ROW\|A=0\|1, 1` | boolean_algebra_generator.py |
| `KMAP_SETUP` | 2 | `KMAP_SETUP\|rows A=0,A=1\|columns B=0,B=1` | boolean_algebra_generator.py |
| `KMAP_SIMPLIFY` | 1 | `KMAP_SIMPLIFY\|NOT A` | boolean_algebra_generator.py |
| `KMEANS_SETUP` | 2 | `KMEANS_SETUP\|points=P1=(-5,3), P2=(-4,1), P3=(-1,4), P4=(3,-2)\|centroids=C1=(1,-4), C2=(-4,3)` | kmeans_step_generator.py |
| `KNN_DISTANCE` | 3 | `KNN_DISTANCE\|P1\|label=A\|d2=136` | knn_generator.py |
| `KNN_NEIGHBORS` | 1 | `KNN_NEIGHBORS\|P5:64:A,P3:65:A,P4:81:A` | knn_generator.py |
| `KNN_SETUP` | 3 | `KNN_SETUP\|q=(4,-5)\|k=3\|training=P1=(-2,5,A), P2=(-3,1,A), P3=(0,2,A), P4=(-5,-5,A), P5=(4,3,A)` | knn_generator.py |
| `KNN_SORT` | 1 | `KNN_SORT\|P5:64:A,P3:65:A,P4:81:A,P2:85:A,P1:136:A` | knn_generator.py |
| `KP_EXAMPLE` | 3 | `KP_EXAMPLE\|1\|x=-4,y=1\|alpha=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_SETUP` | 3 | `KP_SETUP\|kernel=linear\|data=[(-4,1), (4,-1), (7,1)]\|alpha0=(0,0,0)` | kernel_perceptron_generator.py |
| `KP_TERM` | 2 | `KP_TERM\|j=1\|0` | kernel_perceptron_generator.py |
| `KRAFT_CHECK` | 2, 3 | `KRAFT_CHECK\|sum=1\|complete` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_CLASSIFY` | 2 | `KRAFT_CLASSIFY\|slack=0\|complete` | kraft_inequality_generator.py |
| `KRAFT_FORMULA` | 1 | `KRAFT_FORMULA\|sum 2^-l_i` | huffman_coding_generator.py, kraft_inequality_generator.py |
| `KRAFT_SETUP` | 2 | `KRAFT_SETUP\|A=2, B=2, C=3, D=3, E=3, F=3\|binary prefix code` | kraft_inequality_generator.py |
| `KRAFT_TERM` | 3 | `KRAFT_TERM\|A\|l=2\|1/4` | kraft_inequality_generator.py |
| `KRR_SETUP` | 3 | `KRR_SETUP\|kernel=linear\|data=[(4,3), (-4,-2)]\|lambda=2,x*=5` | kernel_ridge_generator.py |
| `KV_CACHE` | 2 | `KV_CACHE\|values\|15728640` | flops_memory_generator.py |
| `L` | 3 | `L\|2\|9\|18` | fraction_comparison_generator.py, fraction_op_generator.py, linear_fractional_generator.py, mixed_number_operation_generator.py, rational_expr_add_sub_generator.py |
| `LABEL_COUNT` | 2 | `LABEL_COUNT\|A\|3` | knn_generator.py |
| `LADDER_APPLY` | 2 | `LADDER_APPLY\|adag ket27\|sqrt(28) ket28` | ladder_operator_generator.py |
| `LADDER_COMM` | 2 | `LADDER_COMM\|[a,adag] ketn\|ket27` | ladder_operator_generator.py |
| `LADDER_RULE` | 2 | `LADDER_RULE\|J_- = J1_- + J2_-\|lower from highest weights` | clebsch_gordan_generator.py, ladder_operator_generator.py |
| `LADDER_SETUP` | 3 | `LADDER_SETUP\|commutator_energy\|state=ket27\|hbar=7, omega=2` | ladder_operator_generator.py |
| `LAGRANGE_EQ` | 2 | `LAGRANGE_EQ\|f_x = lambda\|3*x^2*y^3` | lagrange_multiplier_generator.py |
| `LAGRANGE_FACTOR` | 3 | `LAGRANGE_FACTOR\|L_0\|j=1\|2` | interpolation_generator.py |
| `LAGRANGE_SETUP` | 3 | `LAGRANGE_SETUP\|f(x,y) = x^3*y^3\|constraint x + y = 24\|maximize` | lagrange_multiplier_generator.py |
| `LAGRANGIAN` | 1, 2 | `LAGRANGIAN\|L=T-V\|1/2*m*xdot^2 - 1/2*k*x^2` | lagrangian_generator.py |
| `LAG_SETUP` | 3 | `LAG_SETUP\|mass_spring\|m=1, k=12\|q=x` | lagrangian_generator.py |
| `LAPLACE` | 2 | `LAPLACE\|L[y' + 2y]\|(sY + 5) + 2Y` | laplace_ivp_generator.py, transfer_function_generator.py |
| `LAPLACE_TABLE` | 1 | `LAPLACE_TABLE\|L{y'} = sY - y(0); L{e^(kt)} = 1/(s-k); L^-1{1/(s-k)} = e^(kt)` | laplace_ivp_generator.py |
| `LAURENT_SETUP` | 3 | `LAURENT_SETUP\|center a=3\|w=(z-3)\|f=(-3 - 3(z-3) - 2(z-3)^2 - 4(z-3)^3 - 3(z-3)^4 + (z-3)^5 + 5(z-3)^6)/(z-3)^3` | laurent_series_generator.py |
| `LAURENT_TERM` | 1 | `LAURENT_TERM\|4(z-1)^-2` | residue_generator.py |
| `LAYERNORM_SETUP` | 3 | `LAYERNORM_SETUP\|x=(-13,11)\|gamma=(4,3)\|beta=(-3,-5)` | layer_norm_generator.py |
| `LCM_FROM_GCD` | 3 | `LCM_FROM_GCD\|54*50\|2\|1350` | lcm_generator.py |
| `LCM_STEP` | 3 | `LCM_STEP\|1\|3\|3` | permutation_group_generator.py |
| `LEADING_MINOR` | 2 | `LEADING_MINOR\|Delta1\|9` | positive_definite_generator.py |
| `LEGENDRE_RESULT` | 3 | `LEGENDRE_RESULT\|36\|-1\|quadratic nonresidue` | quadratic_residue_generator.py |
| `LEGENDRE_SETUP` | 2 | `LEGENDRE_SETUP\|a=103\|p=37` | legendre_construction_generator.py, quadratic_residue_generator.py |
| `LIE_EXP_FORM` | 2 | `LIE_EXP_FORM\|e^(theta J)\|cos(theta)I + sin(theta)J` | lie_exponential_generator.py |
| `LIE_EXP_SETUP` | 4 | `LIE_EXP_SETUP\|SO2\|theta=1020 deg\|J=[[0, -1], [1, 0]]\|goal=e^(theta J)` | lie_exponential_generator.py |
| `LIMITING_REAGENT` | 2 | `LIMITING_REAGENT\|CO\|CO2=12 mol` | stoichiometry_generator.py |
| `LIMIT_CHECK` | 2 | `LIMIT_CHECK\|CO2 from CO=12 mol\|CO2 from O2=16 mol` | stoichiometry_generator.py |
| `LIMIT_SETUP` | 1, 2 | `LIMIT_SETUP\|lim x→3⁻ of abs(x - 3)/(x - 3)\|one-sided: approach from the left` | derivative_limit_def_generator.py, improper_integral_generator.py, lhopital_generator.py, limit_evaluation_generator.py, power_series_generator.py, series_convergence_generator.py |
| `LINEAR_SYSTEM` | 2 | `LINEAR_SYSTEM\|a=4/5, b=-4/15\|c=-1/3, d=2/3` | markov_chain_generator.py |
| `LINE_EQ` | 1 | `LINE_EQ\|4x - 2y + 23 = 0` | complex_locus_generator.py |
| `LINE_INTEGRAL` | 3 | `LINE_INTEGRAL\|int_0^1 dot dt\|-208/2 + 70\|-34` | line_integral_generator.py |
| `LINE_RELATION_SETUP` | 3 | `LINE_RELATION_SETUP\|perpendicular\|y = 3x + 9\|(2, 10)` | parallel_perpendicular_line_generator.py |
| `LINE_SETUP` | 2 | `LINE_SETUP\|F(x,y) = <5*x - 5*y, -2*x - 4*y>\|from (-1, -2) to (1, 4)` | line_integral_generator.py |
| `LOCUS_SETUP` | 3 | `LOCUS_SETUP\|z=x+iy\|center=(5,-6)\|radius=2` | complex_locus_generator.py |
| `LOG2` | 2 | `LOG2\|1/4\|-2` | entropy_generator.py, huffman_coding_generator.py, mutual_information_generator.py, von_neumann_entropy_generator.py |
| `LOG2_RATIO` | 3 | `LOG2_RATIO\|i=0\|ratio=1/256\|log=-8` | kl_divergence_generator.py |
| `LOG_BOTH_SIDES` | 1 | `LOG_BOTH_SIDES\|log_10(10^x) = log_10(30)` | exponential_equation_generator.py, log_diff_higher_order_generator.py, separable_ode_generator.py |
| `LOG_EVAL` | 2 | `LOG_EVAL\|23/16\|ln(23/16)` | hyperbolic_distance_generator.py |
| `LOG_FORM` | 1 | `LOG_FORM\|log_3(243) = y ⟺ 3^y = 243` | log_conversion_generator.py, log_equation_generator.py |
| `LOG_FORMULA` | 1 | `LOG_FORMULA\|log z = ln r + i(arg + 2pi*k)` | complex_log_generator.py |
| `LOG_IDENT` | 2 | `LOG_IDENT\|ln(e) = 1\|1` | exponential_equation_generator.py, log_conversion_generator.py |
| `LOG_LIKELIHOOD` | 1 | `LOG_LIKELIHOOD\|ell(mu)=-(1/(2*8))*sum((x_i-mu)^2)+C` | mle_generator.py |
| `LOG_ONE_TO_ONE` | 1 | `LOG_ONE_TO_ONE\|2x - 1 = x - 6` | log_equation_generator.py |
| `LOG_POWER` | 2 | `LOG_POWER\|2log_2(y)\|log_2(y^2)` | log_diff_higher_order_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_PRODUCT` | 1, 2 | `LOG_PRODUCT\|log_2(x) + log_2(y^2)\|log_2(xy^2)` | log_equation_generator.py, log_properties_generator.py, ph_calculation_generator.py |
| `LOG_QUOTIENT` | 2 | `LOG_QUOTIENT\|log_2(xy^2) - log_2(z^3)\|log_2(xy^2/z^3)` | log_properties_generator.py |
| `LOG_SETUP` | 1, 2 | `LOG_SETUP\|log_2(x) + 2log_2(y) - 3log_2(z)\|condense` | complex_log_generator.py, log_properties_generator.py |
| `LOG_SOFTMAX` | 2 | `LOG_SOFTMAX\|1\|ln(7/15)` | softmax_gradient_generator.py |
| `LOG_SUPPLIED` | 2 | `LOG_SUPPLIED\|log10(1000)\|3` | signal_arithmetic_generator.py |
| `LOG_TERM` | 3 | `LOG_TERM\|16\|ln(2)\|16*ln(2)` | entropy_change_generator.py |
| `LOOKUP_SUPPLIED` | 2 | `LOOKUP_SUPPLIED\|e^-1\|3679/10000` | named_distribution_generator.py |
| `LORA_COUNT` | 2 | `LORA_COUNT\|r*(d_in+d_out)\|8192` | param_count_generator.py |
| `LOWRANK_SETUP` | 2 | `LOWRANK_SETUP\|A=[[16,0], [0,5]]\|rank=1` | low_rank_approx_generator.py |
| `LP_CORNER_SETUP` | 3 | `LP_CORNER_SETUP\|max z=2x+10y\|0<=x<=8, 0<=y<=22\|x+y<=25` | lp_corner_generator.py |
| `LR_PHASE` | 1 | `LR_PHASE\|warmup` | lr_schedule_generator.py |
| `LR_SETUP` | 3 | `LR_SETUP\|base=1/1000\|min=1/10000\|warmup=50,total=450,t=3` | lr_schedule_generator.py |
| `LR_VALUE` | 1 | `LR_VALUE\|3/50000` | lr_schedule_generator.py |
| `LS_LINE` | 2 | `LS_LINE\|a = 5, b = 2\|ŷ = 5 + 2x` | least_squares_generator.py |
| `LS_SETUP` | 2 | `LS_SETUP\|points [(-3, -3), (-1, 5), (1, 9), (3, 9)]\|model y = a + bx` | least_squares_generator.py |
| `LUHN_DIGIT` | 3 | `LUHN_DIGIT\|digit 2\|double\|4 -> 4` | modular_arithmetic_generator.py |
| `LU_ENTRY` | 3 | `LU_ENTRY\|u11\|a11 = -5\|-5` | lu_decomposition_generator.py |
| `LU_RESULT` | 2 | `LU_RESULT\|L\|[[1, 0, 0], [-1, 1, 0], [0, 3, 1]]` | lu_decomposition_generator.py |
| `LU_SETUP` | 2 | `LU_SETUP\|A = [[-5, 0, 2], [5, 2, -2], [0, 6, -5]]\|unit lower L` | lu_decomposition_generator.py |
| `M` | 2, 3 | `M\|6\|99\|594` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, arc_sector_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, calorimetry_generator.py, casimir_force_generator.py, casimir_generator.py, cayley_table_generator.py, chain_rule_generator.py, channel_capacity_generator.py, christoffel_generator.py, circle_angle_generator.py, classifier_metrics_generator.py, collision_generator.py, commutator_generator.py, complex_locus_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, cramers_rule_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, cyclic_group_generator.py, de_moivre_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dimensional_analysis_generator.py, doppler_generator.py, dot_product_generator.py, einstein_summation_generator.py, electrostatics_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, error_spotting_generator.py, euler_method_generator.py, evaluate_expression_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_special_forms_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_counting_generator.py, graph_interpret_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hawking_generator.py, hermitian_check_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, index_gymnastics_generator.py, index_raising_generator.py, information_gain_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, ladder_operator_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, long_division_generator.py, lp_corner_generator.py, lr_schedule_generator.py, magnetism_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, mixed_number_operation_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_inverse_generator.py, multi_step_unit_conversion_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, npv_irr_generator.py, ode_system_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, param_count_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, partition_function_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, planck_units_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positive_definite_generator.py, primality_test_generator.py, projectile_motion_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quaternion_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, recurrence_generator.py, recursive_explicit_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, series_solution_generator.py, set_operations_generator.py, shm_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simplex_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, stoichiometry_generator.py, svm_margin_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, unit_conversion_generator.py, vector_ops_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `MAG_FORMULA` | 1 | `MAG_FORMULA\|magnitude = √(x^2 + y^2)` | magnetism_generator.py, vector_ops_generator.py |
| `MAG_SETUP` | 3 | `MAG_SETUP\|loop_center\|I=25, R=13\|mu0=1` | magnetism_generator.py |
| `MARGIN` | 2 | `MARGIN\|2/norm(w)\|2/17` | svm_margin_generator.py |
| `MARGINAL` | 1 | `MARGINAL\|P(X=0)=p00+p01` | joint_distribution_generator.py, mutual_information_generator.py |
| `MARKOV_SETUP` | 3 | `MARKOV_SETUP\|two_state\|P00=1/5, P01=4/5\|P10=1/3, P11=2/3` | markov_chain_generator.py |
| `MATMUL_FLOPS` | 2 | `MATMUL_FLOPS\|XW1\|67108864` | flops_memory_generator.py |
| `MATRIX_ADD` | 2 | `MATRIX_ADD\|P0+P1\|[[1,0],[0,1]]` | bch_generator.py, casimir_generator.py, projector_generator.py |
| `MATRIX_ENTRY` | 1 | `MATRIX_ENTRY\|P2_01=P00*P01 + P01*P11` | markov_chain_generator.py |
| `MATRIX_ENTRY_SUM` | 3 | `MATRIX_ENTRY_SUM\|(3,4)\|-1 + 1\|0` | gamma_matrix_generator.py |
| `MATRIX_EXP` | 3 | `MATRIX_EXP\|e^A\|I + A\|[[1, 0, 0], [0, 1, 5], [0, 0, 1]]` | bch_generator.py |
| `MATRIX_GROUP_SETUP` | 2 | `MATRIX_GROUP_SETUP\|SO2\|M=[[45/53,-28/53],[28/53,45/53]]` | matrix_group_check_generator.py |
| `MATRIX_MULT` | 2, 3 | `MATRIX_MULT\|row1 dot col1\|1/4+1/4\|1/2` | projector_generator.py |
| `MATRIX_POWER` | 2 | `MATRIX_POWER\|J^2\|-I` | lie_exponential_generator.py |
| `MATRIX_PRODUCT` | 2 | `MATRIX_PRODUCT\|AB\|[[0, -3i], [-3i, 0]]` | bch_generator.py, casimir_generator.py, gamma_matrix_generator.py, pauli_algebra_generator.py, structure_constant_generator.py |
| `MATRIX_ROW` | 2 | `MATRIX_ROW\|row 1\|0, 1, 0` | graph_counting_generator.py |
| `MATRIX_SCALE` | 2 | `MATRIX_SCALE\|1/2 ladder sum\|[[256, 0, 0], [0, 512, 0], [0, 0, 256]]` | bch_generator.py, casimir_generator.py |
| `MATRIX_SETUP` | 2 | `MATRIX_SETUP\|unitary\|U=[[44/125,-117/125],[117/125,44/125]]` | hermitian_check_generator.py |
| `MATRIX_SUB` | 2 | `MATRIX_SUB\|AB - BA\|[[0, 0, 25], [0, 0, 0], [0, 0, 0]]` | bch_generator.py |
| `MATRIX_SUM` | 1 | `MATRIX_SUM\|B=A+A^T` | matrix_calculus_generator.py |
| `MATRIX_VALUE` | 2 | `MATRIX_VALUE\|A\|[[-2, 0], [0, 2]]` | pauli_algebra_generator.py, structure_constant_generator.py |
| `MAT_ENTRY` | 2, 3 | `MAT_ENTRY\|(1,1)\|5` | lie_exponential_generator.py, matrix_calculus_generator.py, matrix_ops_generator.py |
| `MAT_SETUP` | 2 | `MAT_SETUP\|A = [[5, -3], [-1, -1]], B = [[0, 1], [-6, -1]]\|A - B` | determinant_generator.py, diagonalization_generator.py, eigenvalue_generator.py, matrix_exponential_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, row_reduction_generator.py, subspace_basis_generator.py, svd_generator.py |
| `MAX` | 2, 3 | `MAX\|16, 6\|16` | dp_table_generator.py, matrix_norm_generator.py, taxicab_geometry_generator.py |
| `MAXTERM` | 2 | `MAXTERM\|011\|A OR NOT B OR NOT C` | boolean_algebra_generator.py |
| `MC_SETUP` | 3 | `MC_SETUP\|expression=x^T A x\|A=[[2,-4], [1,0]]\|x=(0,-2)` | matrix_calculus_generator.py |
| `MEAN` | 1 | `MEAN\|-1` | layer_norm_generator.py |
| `MEAN_DIV` | 3 | `MEAN_DIV\|63\|7\|9` | composite_arithmetic_generator.py, five_number_summary_generator.py, regression_generator.py, simple_stats_generator.py, standard_deviation_generator.py |
| `MEASURE_BASIS` | 3 | `MEASURE_BASIS\|z\|ket+z=ket0\|ket-z=ket1` | spin_half_generator.py |
| `MEASURE_FAVORABLE` | 2 | `MEASURE_FAVORABLE\|interval length\|31 - 11 = 20` | geometric_probability_generator.py |
| `MEASURE_PROB` | 3 | `MEASURE_PROB\|computational basis\|P(11)=1\|all other outcomes 0` | quantum_gate_generator.py |
| `MEASURE_TOTAL` | 2 | `MEASURE_TOTAL\|total length\|33` | geometric_probability_generator.py |
| `MEDIAN_PAIR` | 2 | `MEDIAN_PAIR\|9\|16` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEDIAN_PICK` | 2, 3 | `MEDIAN_PICK\|12\|\|12` | five_number_summary_generator.py, simple_stats_generator.py |
| `MEMORY_SETUP` | 3 | `MEMORY_SETUP\|kv_cache\|L=16,h=12,d_k=80\|seq=512,precision_bytes=1` | flops_memory_generator.py |
| `MEMORY_UNIT` | 2 | `MEMORY_UNIT\|MiB\|15` | flops_memory_generator.py |
| `MERGE_BEGIN` | 3 | `MERGE_BEGIN\|merge 1\|lo=1,mid=2,hi=3\|left 42; right 48` | algorithm_trace_generator.py |
| `MERGE_COMPARE` | 3 | `MERGE_COMPARE\|42\|48\|take left` | algorithm_trace_generator.py |
| `MERGE_DONE` | 3 | `MERGE_DONE\|merge 1\|range 1-2\|array 27, 42, 48, 24, 41, 21, 10` | algorithm_trace_generator.py |
| `MERGE_TAKE` | 2 | `MERGE_TAKE\|42\|merged 42` | algorithm_trace_generator.py |
| `METRIC` | 2 | `METRIC\|Chebyshev\|d = max(abs(x2 - x1), abs(y2 - y1))` | taxicab_geometry_generator.py |
| `METRICS_SETUP` | 1 | `METRICS_SETUP\|TP=24, FP=18, FN=19, TN=10` | classifier_metrics_generator.py |
| `METRIC_ARC_SETUP` | 3 | `METRIC_ARC_SETUP\|polar metric\|ds^2=dr^2+r^2 dtheta^2\|theta=120 deg, r:6->15` | metric_arc_length_generator.py |
| `METRIC_FORMULA` | 1 | `METRIC_FORMULA\|precision=TP/(TP+FP)` | classifier_metrics_generator.py |
| `METRIC_RESTRICT` | 2 | `METRIC_RESTRICT\|dtheta=0\|ds^2=dr^2` | metric_arc_length_generator.py |
| `MGF_SETUP` | 3 | `MGF_SETUP\|P(X=0)=17/24\|P(X=1)=3/16\|P(X=2)=5/48` | mgf_generator.py |
| `MGF_TERM` | 3 | `MGF_TERM\|x=0\|p0*e^(0t)\|17/24` | mgf_generator.py |
| `MIDDLE_EVAL` | 3 | `MIDDLE_EVAL\|r=0..6\|6^2/2\|18` | triple_integral_generator.py |
| `MIDLINE` | 1 | `MIDLINE\|y = 0` | sinusoid_features_generator.py |
| `MIDPOINT` | 2 | `MIDPOINT\|iter 1\|3` | algorithm_trace_generator.py |
| `MID_FORMULA` | 1 | `MID_FORMULA\|M = ((x1 + x2)/2, (y1 + y2)/2)` | circle_equation_generator.py, midpoint_generator.py |
| `MIN` | 2 | `MIN\|64,25\|25` | matrix_norm_generator.py |
| `MIN3` | 4 | `MIN3\|3\|1\|2\|1` | dp_table_generator.py |
| `MINKOWSKI_FORMULA` | 1 | `MINKOWSKI_FORMULA\|eta_total=eta1+eta2` | minkowski_interval_generator.py |
| `MINKOWSKI_SETUP` | 3 | `MINKOWSKI_SETUP\|rapidity_addition\|eta1=-2/3\|eta2=-3/2` | minkowski_interval_generator.py |
| `MINTERM` | 2 | `MINTERM\|001\|NOT A AND NOT B AND C` | boolean_algebra_generator.py |
| `MIX_FORMULA` | 2 | `MIX_FORMULA\|q=(d-b)/(a-b-c+d)\|p=(d-c)/(a-b-c+d)` | game_theory_generator.py |
| `MIX_IMPROPER` | 2 | `MIX_IMPROPER\|5 9/10\|59/10` | composite_arithmetic_generator.py, mixed_number_operation_generator.py, order_of_operations_generator.py |
| `MI_FORMULA` | 1 | `MI_FORMULA\|I=H(X)+H(Y)-H(X,Y)` | mutual_information_generator.py |
| `MI_SETUP` | 2 | `MI_SETUP\|rows=[[0,1/2];[1/2,0]]\|task=H(X,Y)` | mutual_information_generator.py |
| `MLE_SETUP` | 2, 3 | `MLE_SETUP\|normal_mu\|parameter=mu\|sigma^2=8` | mle_generator.py |
| `MOBIUS_SETUP` | 2 | `MOBIUS_SETUP\|T(z)=(75)/(3z)\|fixed points` | mobius_transform_generator.py |
| `MODE` | 2 | `MODE\|2\|9` | frequency_table_generator.py, simple_stats_generator.py |
| `MODEL` | 1 | `MODEL\|A = P(1 - r)^t` | exponential_model_generator.py |
| `MODEL_APPLY` | 1 | `MODEL_APPLY\|A = 800 · (1 - 0.2)^4` | exponential_model_generator.py |
| `MODEL_OUTPUT` | 1 | `MODEL_OUTPUT\|-2` | activation_generator.py |
| `MODEXP_MULTIPLY` | 2 | `MODEXP_MULTIPLY\|bit 1=1\|4` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_SETUP` | 3 | `MODEXP_SETUP\|base 4\|exponent 80\|modulus 31` | mod_exp_generator.py |
| `MODEXP_SQUARE` | 2 | `MODEXP_SQUARE\|bit 1=1\|1` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODEXP_STATE` | 2 | `MODEXP_STATE\|after bit 1\|4` | mod_exp_generator.py, quadratic_residue_generator.py |
| `MODE_COUNT` | 2 | `MODE_COUNT\|5\|1` | simple_stats_generator.py |
| `MOD_INVERSE` | 2 | `MOD_INVERSE\|85 mod 33\|7` | crt_generator.py, modular_inverse_generator.py, rsa_generator.py |
| `MOD_NORMALIZE` | 3 | `MOD_NORMALIZE\|7\|mod 33\|7` | modular_inverse_generator.py, rsa_generator.py |
| `MOD_POWER` | 3 | `MOD_POWER\|15^15\|mod 19\|8` | diffie_hellman_generator.py, primality_test_generator.py, rsa_generator.py, totient_generator.py |
| `MOD_REDUCE` | 3 | `MOD_REDUCE\|20\|mod 10\|0` | calendar_arithmetic_generator.py, cayley_table_generator.py, coset_generator.py, crt_generator.py, cyclic_group_generator.py, de_moivre_generator.py, finite_field_generator.py, lie_exponential_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, primality_test_generator.py, quadratic_residue_generator.py, rsa_generator.py, totient_generator.py |
| `MOD_SETUP` | 2, 3, 4 | `MOD_SETUP\|Luhn modulus 10\|prefix 2467020` | modular_arithmetic_generator.py, modular_inverse_generator.py |
| `MOD_SOLVE` | 2 | `MOD_SOLVE\|d ≡ -0 mod 10\|0` | modular_arithmetic_generator.py |
| `MOD_TERM` | 2 | `MOD_TERM\|10 * 4\|40` | modular_arithmetic_generator.py |
| `MOE_FORMULA` | 1 | `MOE_FORMULA\|E = z*·√(p̂(1-p̂)/n)` | confidence_interval_generator.py |
| `MOLAR_MASS` | 2 | `MOLAR_MASS\|H2O2\|34 g/mol` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `MOLAR_VOLUME` | 2 | `MOLAR_VOLUME\|1 mol gas\|24 L` | stoichiometry_generator.py |
| `MOMENT` | 2 | `MOMENT\|m1\|1` | adam_step_generator.py |
| `MOMENTUM` | 1 | `MOMENTUM\|x components` | collision_generator.py |
| `MOMENT_X` | 3 | `MOMENT_X\|M_x = 1/2 int y^2 dx\|3^2*5^3/6\|375/2` | centroid_generator.py |
| `MOMENT_Y` | 3 | `MOMENT_Y\|M_y = int x*y dx\|3*5^3/3\|125` | centroid_generator.py |
| `MOM_EQUATION` | 2 | `MOM_EQUATION\|E[X]=1/lambda\|xbar=1/lambda` | method_of_moments_generator.py |
| `MOM_SETUP` | 3 | `MOM_SETUP\|exponential\|parameter=lambda\|data=[6,4,5,7]` | method_of_moments_generator.py |
| `MONO_ADD_EXP` | 2 | `MONO_ADD_EXP\|x^1 * x^5 = x^(1+5)\|x^6` | monomial_mult_div_generator.py |
| `MONO_DIV_COEFF` | 2 | `MONO_DIV_COEFF\|-24 / 4\|-6` | monomial_mult_div_generator.py |
| `MONO_MULT_COEFF` | 2 | `MONO_MULT_COEFF\|5 * -6\|-30` | monomial_mult_div_generator.py |
| `MONO_SETUP` | 1 | `MONO_SETUP\|(5x)(-6x^5)` | monomial_mult_div_generator.py |
| `MONO_SUB_EXP` | 2 | `MONO_SUB_EXP\|x^9 / x^5 = x^(9-5)\|x^4` | monomial_mult_div_generator.py |
| `MOVE_TERM` | 2, 3 | `MOVE_TERM\|+5x\|left\|3x+2-5x = +7` | area_between_curves_generator.py, completing_square_generator.py, conic_standard_form_generator.py, linear_complex_generator.py, polar_parametric_generator.py, quadratic_factoring_generator.py, quadratic_square_root_generator.py, radical_equation_generator.py, special_solution_equation_generator.py, standard_form_conversion_generator.py |
| `MR_DECOMPOSE` | 2 | `MR_DECOMPOSE\|54\|2^1 * 27` | primality_test_generator.py |
| `MR_SETUP` | 2 | `MR_SETUP\|n=55\|witnesses 7, 12` | primality_test_generator.py |
| `MR_SQUARE` | 2 | `MR_SQUARE\|r=1\|52` | primality_test_generator.py |
| `MR_WITNESS` | 1 | `MR_WITNESS\|7` | primality_test_generator.py |
| `MR_WITNESS_RESULT` | 2 | `MR_WITNESS_RESULT\|7\|composite` | primality_test_generator.py |
| `MSE_FORMULA` | 2 | `MSE_FORMULA\|L=(1/n) sum r_i^2\|grad=(2/n) sum r_i*[1,x_i]` | gradient_step_generator.py |
| `MSE_GRADIENT` | 2 | `MSE_GRADIENT\|g0=3\|g1=8` | gradient_step_generator.py |
| `MSE_SAMPLE` | 3 | `MSE_SAMPLE\|i=1\|pred=4\|r=1` | gradient_step_generator.py |
| `MSE_SETUP` | 3 | `MSE_SETUP\|model y_hat=w0+w1*x\|samples=[(2,3), (3,4)]\|w=(0,2), eta=1/7` | gradient_step_generator.py |
| `MST_ADD` | 2 | `MST_ADD\|CE\|total 4` | mst_generator.py |
| `MST_SET` | 1 | `MST_SET\|CE` | mst_generator.py |
| `MST_SETUP` | 2 | `MST_SETUP\|weighted undirected graph\|vertices A, B, C, D, E` | mst_generator.py |
| `MULTIPLY_IF` | 2 | `MULTIPLY_IF\|e^(3x)y' + 3e^(3x)y\|6e^(3x)` | integrating_factor_generator.py, ode_substitution_generator.py |
| `MULTIVALUED_LOG` | 2 | `MULTIVALUED_LOG\|ln(2) + i*(3pi/4 + 2pi*k)\|k in Z` | complex_log_generator.py |
| `MULTI_FORMULA` | 2 | `MULTI_FORMULA\|n!/(a!b!c!...)\|5! / repeats` | stars_and_bars_generator.py |
| `MULTI_SETUP` | 2 | `MULTI_SETUP\|1 A, 2 B's, 1 C, 1 D\|total 5` | stars_and_bars_generator.py |
| `MUL_PARTIAL` | 3 | `MUL_PARTIAL\|6\|68395\|410370` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_SETUP` | 2 | `MUL_SETUP\|68395\|1956` | decimal_mult_generator.py, multi_digit_multiplication_generator.py |
| `MUL_TERM` | 3 | `MUL_TERM\|5\|(-4/5)x\|-4x` | linear_fractional_generator.py, polynomial_long_division_generator.py, rational_equation_generator.py |
| `MVT_SETUP` | 2 | `MVT_SETUP\|f(x) = x^2 - x - 7 on [-4, 2]\|find the c guaranteed by the MVT` | mean_value_theorem_generator.py |
| `MV_CHAIN_SETUP` | 3 | `MV_CHAIN_SETUP\|z = f(x,y) = 5*x^2 + y^2 - 5*x + 5*y\|x = -4*t + 5, y = -3*t - 4\|t = 1` | multivar_chain_rule_generator.py |
| `NATURAL_SETUP` | 3 | `NATURAL_SETUP\|length\|hbar=1,c=1\|L=14/13 GeV^-1` | natural_units_generator.py |
| `NB_FEATURE_COUNT` | 3 | `NB_FEATURE_COUNT\|Spam\|offer=0\|count=3` | naive_bayes_generator.py |
| `NB_LIKELIHOOD` | 3 | `NB_LIKELIHOOD\|Spam\|offer=0\|4/11` | naive_bayes_generator.py |
| `NB_PRIOR` | 2 | `NB_PRIOR\|Spam\|9/25` | naive_bayes_generator.py |
| `NB_SCORE` | 2 | `NB_SCORE\|Spam\|start=9/25` | naive_bayes_generator.py |
| `NB_SETUP` | 3 | `NB_SETUP\|query=offer=0, link=1, money=0\|alpha=1\|classes=Spam,Ham` | naive_bayes_generator.py |
| `NCR` | 2 | `NCR\|C(4,0)\|1` | binomial_probability_generator.py, generating_function_generator.py, hypercube_counting_generator.py |
| `NEAREST` | 2 | `NEAREST\|queen\|(-4,-3)` | embedding_similarity_generator.py |
| `NEED` | 2 | `NEED\|line 2 gives the base ratio 5:12\|line 4 multiplies 5 by 9` | fill_in_step_generator.py |
| `NEG_LOG` | 2 | `NEG_LOG\|p=1/16\|ln(16)` | perplexity_generator.py |
| `NET_SETUP` | 2 | `NET_SETUP\|1 square 6 by 6; 4 triangles with base 6 and height 6\|total surface area` | nets_surface_area_generator.py |
| `NEWTON_DD` | 2 | `NEWTON_DD\|f[x0,x1]\|-9` | interpolation_generator.py |
| `NEWTON_SETUP` | 2, 3 | `NEWTON_SETUP\|f(x)=x^2-58\|f'(x)=2x\|x0=8,iterations=2` | newton_raphson_generator.py, newtons_laws_generator.py |
| `NEWTON_STEP` | 2 | `NEWTON_STEP\|1\|11/25` | npv_irr_generator.py |
| `NEWTON_UPDATE` | 3 | `NEWTON_UPDATE\|1\|x_0=8\|x_1=61/8` | newton_raphson_generator.py |
| `NEW_SLOPE` | 2 | `NEW_SLOPE\|New slope (m2) = -1/3\|Perpendicular lines have negative reciprocal slopes` | parallel_perpendicular_line_generator.py |
| `NILPOTENT` | 3 | `NILPOTENT\|theta^2=0\|-6theta^2\|0` | grassmann_generator.py |
| `NLL` | 2 | `NLL\|197 tokens\|197*ln(16)` | perplexity_generator.py |
| `NORMALIZE` | 2 | `NORMALIZE\|1/2 + 1/2\|1` | clebsch_gordan_generator.py, layer_norm_generator.py |
| `NORMAL_EQ` | 2 | `NORMAL_EQ\|X^T X\|[[4, 0], [0, 20]]` | least_squares_generator.py |
| `NORMAL_SLOPE` | 2 | `NORMAL_SLOPE\|-1/(3)\|-1/3` | tangent_line_generator.py |
| `NORMAL_SYMMETRY` | 2 | `NORMAL_SYMMETRY\|N_neg_d1=0.1\|N_neg_d2=0.15` | black_scholes_generator.py |
| `NORM_CHECK` | 2 | `NORM_CHECK\|P(+z)+P(-z)\|1` | spin_half_generator.py |
| `NORM_SETUP` | 2 | `NORM_SETUP\|A: 7 in N(40, 25)\|compare relative standing` | matrix_norm_generator.py, normal_table_generator.py, z_score_generator.py |
| `NORM_SQUARED` | 2 | `NORM_SQUARED\|q\|1` | quaternion_generator.py |
| `NPV_SETUP` | 2 | `NPV_SETUP\|c0=-2500,c1=450,c2=1650,c3=100\|rate=25%` | npv_irr_generator.py |
| `NPV_TERM` | 2 | `NPV_TERM\|t=0\|-2500` | npv_irr_generator.py |
| `NULL_REL` | 2 | `NULL_REL\|x1 - 3*x3 - 2*x4 = 0\|x1 = 3*x3 + 2*x4` | subspace_basis_generator.py |
| `NULL_VECTOR` | 2 | `NULL_VECTOR\|x3=1, x4=0\|[3, 3, 1, 0]` | subspace_basis_generator.py |
| `NUMBER_OPERATOR` | 2 | `NUMBER_OPERATOR\|N ket23\|23 ket23` | ladder_operator_generator.py |
| `NW_ALLOC` | 1, 3 | `NW_ALLOC\|cell x11\|min(17,11)\|11` | transportation_generator.py |
| `NYQUIST` | 1 | `NYQUIST\|required rate = 2*f_max` | signal_arithmetic_generator.py |
| `OBJECTIVE` | 1 | `OBJECTIVE\|at (0,0)` | lp_corner_generator.py |
| `ODD_VERTICES` | 2 | `ODD_VERTICES\|none\|0` | euler_circuit_generator.py |
| `ODE_SETUP` | 2 | `ODE_SETUP\|dy/dx = y^2, y(0) = 2\|solve` | euler_method_generator.py, exact_ode_generator.py, integrating_factor_generator.py, laplace_ivp_generator.py, logistic_growth_generator.py, ode_substitution_generator.py, ode_system_generator.py, runge_kutta_generator.py, second_order_ode_generator.py, separable_ode_generator.py, series_solution_generator.py, stability_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `OPTICS_FORMULA` | 1 | `OPTICS_FORMULA\|n1*sin(theta1)=n2*sin(theta2)` | optics_generator.py |
| `OPTICS_SETUP` | 3 | `OPTICS_SETUP\|snell\|n1=1, n2=5\|sin(theta1)=3/5` | optics_generator.py |
| `OPT_SETUP` | 2 | `OPT_SETUP\|184 m of fence, barn forms the fourth side; sides x, x, and 184 - 2x\|maximize area` | optimization_generator.py |
| `ORBIT_FORMULA` | 1 | `ORBIT_FORMULA\|(T2/T1)^2=(a2/a1)^3` | orbital_mechanics_generator.py |
| `ORBIT_SETUP` | 3 | `ORBIT_SETUP\|kepler_third\|T1=66, a1=3\|a2=108` | orbital_mechanics_generator.py |
| `ORDER_PDF` | 1 | `ORDER_PDF\|f_{4:4}(x)=4*x^3` | order_statistics_generator.py |
| `ORDER_SETUP` | 3 | `ORDER_SETUP\|n=4\|k=4\|q=1/14` | order_statistics_generator.py |
| `ORDER_START` | 2 | `ORDER_START\|9\|identity 1` | cayley_table_generator.py |
| `ORDER_STEP` | 2 | `ORDER_STEP\|k=1\|9` | cayley_table_generator.py |
| `ORTHOGONALITY` | 2 | `ORTHOGONALITY\|lower multiplet\|orthogonal to higher J` | clebsch_gordan_generator.py |
| `OR_SETUP` | 3 | `OR_SETUP\|M/M/1\|lambda=16\|mu=21` | or_formula_generator.py |
| `OUTER_ANTIDERIV` | 2 | `OUTER_ANTIDERIV\|dx\|15*x^2 + 70*x` | double_integral_generator.py |
| `OUTER_EVAL` | 3 | `OUTER_EVAL\|y=0..4\|10*2*2^2/2\|40` | double_integral_generator.py |
| `OUTER_PRODUCT` | 1 | `OUTER_PRODUCT\|rho=1/2(ket00bra00+ket00bra10+ket10bra00+ket10bra10)` | partial_trace_generator.py |
| `OUTPUT` | 1 | `OUTPUT\|y_hat=-9` | backprop_generator.py |
| `PARALLEL_RELATION` | 1 | `PARALLEL_RELATION\|4x + 8 = 6x - 10` | angle_relationships_generator.py |
| `PARALLEL_SETUP` | 2 | `PARALLEL_SETUP\|alternate_interior\|Alternate interior angles are equal` | angle_relationships_generator.py |
| `PARALLEL_SOLVE` | 2 | `PARALLEL_SOLVE\|-2x = -18\|x = 9` | angle_relationships_generator.py |
| `PARAMS` | 3 | `PARAMS\|W1=[[-1,2], [-1,2]]\|b1=(-1,-2)\|v=(-2,-1), c=-1` | backprop_generator.py |
| `PARAM_PART` | 2 | `PARAM_PART\|attention_per_layer\|1048576` | param_count_generator.py |
| `PARAM_PATH` | 3 | `PARAM_PATH\|r(t)\|(2*t - 1, 6*t - 2)\|0 <= t <= 1` | line_integral_generator.py |
| `PARAM_SETUP` | 2, 3 | `PARAM_SETUP\|x = 9 cos t, y = 9 sin t\|eliminate t` | param_count_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py |
| `PARITY` | 1, 2 | `PARITY\|transpositions 2\|even` | fourier_series_generator.py, permutation_group_generator.py |
| `PARITY_CALC` | 2 | `PARITY_CALC\|p1=d1 xor d2 xor d4\|1 xor 1 xor 1=1` | hamming_code_generator.py |
| `PARTFRAC_SETUP` | 1 | `PARTFRAC_SETUP\|(-2x - 6)/((x - 3)(x + 1)) = A/(x - 3) + B/(x + 1)` | partial_fractions_generator.py |
| `PARTIAL` | 2 | `PARTIAL\|u_x\|6x + 1` | cauchy_riemann_generator.py, fundamental_form_generator.py, hamiltonian_generator.py, lagrangian_generator.py |
| `PARTIAL_FRAC` | 2 | `PARTIAL_FRAC\|Y(s)\|-4/(s + 2) - 1/(s - 1)` | laplace_ivp_generator.py |
| `PARTIAL_RESULT` | 2 | `PARTIAL_RESULT\|f_y\|12*x^4*y^2 + 32*x*y^3` | div_curl_generator.py, exact_ode_generator.py, gradient_generator.py, hessian_classify_generator.py, jacobian_generator.py, lagrange_multiplier_generator.py, line_integral_generator.py, multivar_chain_rule_generator.py, partial_derivative_generator.py, vector_theorem_generator.py |
| `PARTIAL_RULE` | 3 | `PARTIAL_RULE\|8*x*y^4\|d/dy\|32*x*y^3` | partial_derivative_generator.py |
| `PARTIAL_SETUP` | 2 | `PARTIAL_SETUP\|f(x,y) = 4*x^4*y^3 + 8*x*y^4\|f_yy` | partial_derivative_generator.py |
| `PARTIAL_TRACE` | 2 | `PARTIAL_TRACE\|ket00bra00\|ket0bra0` | partial_trace_generator.py |
| `PARTICLE_TABLE` | 1 | `PARTICLE_TABLE\|gamma(Q=0,B=0,Le=0,Lmu=0); pi0(Q=0,B=0,Le=0,Lmu=0); pi+(Q=1,B=0,Le=0,Lmu=0); nu_mu(Q=0,B=0,Le=0,Lmu=1); mu+(Q=1,B=0,Le=0,Lmu=-1)` | conservation_law_generator.py |
| `PARTICULAR` | 2 | `PARTICULAR\|y_p\|1` | undetermined_coeff_generator.py, variation_parameters_generator.py |
| `PARTICULAR_CHECK` | 2 | `PARTICULAR_CHECK\|K = 4\|5K - 6K + 8 = K` | recurrence_generator.py |
| `PARTICULAR_TRY` | 2 | `PARTICULAR_TRY\|a_n = K\|constant forcing` | recurrence_generator.py |
| `PARTITION_FORMULA` | 1 | `PARTITION_FORMULA\|Z=g0+g1*b` | partition_function_generator.py |
| `PARTITION_SETUP` | 3 | `PARTITION_SETUP\|degenerate_two_level\|g0=2, g1=1\|epsilon=17, b=1/8` | partition_function_generator.py |
| `PARTS_CHOOSE` | 2 | `PARTS_CHOOSE\|u = -2x, dv = e^x dx\|du = -2 dx, v = e^x` | integration_by_parts_generator.py |
| `PARTS_FORMULA` | 1 | `PARTS_FORMULA\|∫ u dv = uv - ∫ v du` | integration_by_parts_generator.py |
| `PASCAL_ROW` | 2 | `PASCAL_ROW\|0\|1` | pascal_triangle_generator.py |
| `PASCAL_SETUP` | 1 | `PASCAL_SETUP\|7C3` | pascal_triangle_generator.py |
| `PATH_DERIV` | 2 | `PATH_DERIV\|r'(t)\|(2, 6)` | curve_geometry_generator.py, line_integral_generator.py |
| `PAULI_IDENTITY` | 3 | `PAULI_IDENTITY\|sigma_y sigma_y\|delta_ij I\|6I` | pauli_algebra_generator.py |
| `PAULI_MATRIX` | 2 | `PAULI_MATRIX\|sigma_y\|[[0,-i],[i,0]]` | spin_half_generator.py |
| `PAULI_SETUP` | 3 | `PAULI_SETUP\|product\|A=-3sigma_y\|B=-2sigma_y` | pauli_algebra_generator.py |
| `PCA_SETUP` | 2 | `PCA_SETUP\|points=[(-2,0), (-4,0), (-3,5), (-3,-5)]\|population covariance` | pca_generator.py |
| `PC_VECTOR` | 2 | `PC_VECTOR\|e2\|(0,1)` | pca_generator.py |
| `PDF_FORMULA` | 1 | `PDF_FORMULA\|f_Y(y)=1/(36*sqrt(y))` | rv_transform_generator.py |
| `PD_SETUP` | 2 | `PD_SETUP\|A=[[9,-9], [-9,34]]\|Sylvester criterion` | positive_definite_generator.py |
| `PERCENT_CALC_PART` | 3 | `PERCENT_CALC_PART\|0.5\|50\|25` | percent_problem_generator.py |
| `PERCENT_TO_DEC` | 2 | `PERCENT_TO_DEC\|90%\|0.9` | annuity_generator.py, bond_pricing_generator.py, composite_arithmetic_generator.py, exponential_model_generator.py, fill_in_step_generator.py, finance_generator.py, fraction_decimal_percent_converter.py, npv_irr_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, piecewise_evaluation_generator.py, portfolio_generator.py, tip_bill_split_generator.py |
| `PERCEPTRON_RULE` | 2 | `PERCEPTRON_RULE\|score=w0+w1*x1+w2*x2\|if y*score <= 0 update` | perceptron_generator.py |
| `PERCEPTRON_SAMPLE` | 3 | `PERCEPTRON_SAMPLE\|i=1\|x=(-2,-1)\|y=1` | perceptron_generator.py |
| `PERCEPTRON_SCORE` | 2 | `PERCEPTRON_SCORE\|i=1\|score=-1` | perceptron_generator.py |
| `PERCEPTRON_SETUP` | 3 | `PERCEPTRON_SETUP\|eta=2\|w=(-1,1,-2)\|samples=[(-2,-1,1), (-2,-3,1), (-1,-1,1)]` | perceptron_generator.py |
| `PERCEPTRON_UPDATE` | 2, 3 | `PERCEPTRON_UPDATE\|i=1\|w=(1,-3,-4)` | perceptron_generator.py |
| `PERIM` | 1 | `PERIM\|32` | geometry_area_perimeter_generator.py, polygon_perimeter_generator.py |
| `PERIOD` | 1 | `PERIOD\|π/3` | sinusoid_features_generator.py |
| `PERM_COMPOSE` | 3 | `PERM_COMPOSE\|i=1\|tau(i)=1\|sigma(tau(i))=3` | permutation_group_generator.py |
| `PERM_FORMULA` | 1 | `PERM_FORMULA\|P(n, r) = n·(n-1)···(n-r+1), 4 factors` | permutation_combination_generator.py |
| `PERM_RESULT` | 1 | `PERM_RESULT\|[3, 1, 2, 4]` | permutation_group_generator.py |
| `PERM_SETUP` | 2, 3 | `PERM_SETUP\|arrange 4 of 8\|order matters` | permutation_combination_generator.py, permutation_group_generator.py |
| `PERPLEXITY` | 2 | `PERPLEXITY\|exp(CE)\|16` | perplexity_generator.py |
| `PERPLEXITY_SETUP` | 2 | `PERPLEXITY_SETUP\|tokens=197\|p=1/16` | perplexity_generator.py |
| `PE_ENTRY` | 2 | `PE_ENTRY\|0\|0` | positional_encoding_generator.py |
| `PE_SETUP` | 3 | `PE_SETUP\|position=51\|d=2\|theta=pi` | positional_encoding_generator.py |
| `PF_PRIME` | 1 | `PF_PRIME\|17` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PF_STEP` | 3 | `PF_STEP\|102\|2\|51` | prime_factorization_generator.py, repeating_decimal_generator.py |
| `PHASE_SHIFT` | 1 | `PHASE_SHIFT\|π/3 right` | sinusoid_features_generator.py |
| `PHI_STEP` | 2 | `PHI_STEP\|p=5\|28` | totient_generator.py |
| `PHYS_FORMULA` | 1 | `PHYS_FORMULA\|W = P*t` | physics_formula_generator.py |
| `PHYS_SETUP` | 3 | `PHYS_SETUP\|P = 44 watts\|t = 3 minutes\|energy` | physics_formula_generator.py |
| `PH_FORMULA` | 1 | `PH_FORMULA\|pH=-log10([H+])` | ph_calculation_generator.py |
| `PH_SETUP` | 2, 3 | `PH_SETUP\|hydronium_with_log\|[H+]=2*10^-7\|log10(2)=0.3` | ph_calculation_generator.py |
| `PI2_NUM` | 3 | `PI2_NUM\|-17/240\|π^2\|-17π^2/240` | casimir_force_generator.py |
| `PICTO_COUNT` | 2 | `PICTO_COUNT\|Pasta\|2` | graph_interpret_generator.py |
| `PICTO_KEY` | 2 | `PICTO_KEY\|●\|5` | graph_interpret_generator.py |
| `PIVOT` | 3 | `PIVOT\|row=s1\|column=x\|pivot=1` | simplex_generator.py |
| `PIVOT_COLS` | 2 | `PIVOT_COLS\|columns 1, 2\|rank = 2` | subspace_basis_generator.py |
| `PI_DEN` | 3 | `PI_DEN\|28/165\|π\|28/(165π)` | gauss_law_generator.py, hawking_generator.py, magnetism_generator.py |
| `PI_MULT` | 3 | `PI_MULT\|2/5\|π\|2π/5` | shm_generator.py |
| `PLACE_DP` | 3 | `PLACE_DP\|4060686\|3\|4060.686` | decimal_mult_generator.py |
| `PLACE_DP_Q` | 2, 3 | `PLACE_DP_Q\|75\|1\|7.5` | decimal_div_generator.py, percent_problem_generator.py |
| `PLACE_VALUE` | 2 | `PLACE_VALUE\|C * 16^0\|12` | base_conversion_generator.py |
| `PLANCK_SETUP` | 4 | `PLANCK_SETUP\|length\|hbar=81\|G=81\|c=9` | planck_units_generator.py |
| `PLUS_MINUS` | 2 | `PLUS_MINUS\|x - 7 = ±11\|x - 7 = 11 or x - 7 = -11` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `POINT_FROM_LAMBDA` | 3 | `POINT_FROM_LAMBDA\|x\|8*4/4\|8` | lagrange_multiplier_generator.py |
| `POINT_SLOPE_SETUP` | 1 | `POINT_SLOPE_SETUP\|y - 4 = -5(x + 9)` | equation_from_two_points_generator.py, parallel_perpendicular_line_generator.py, point_slope_generator.py |
| `POLAR_AREA_FORMULA` | 1 | `POLAR_AREA_FORMULA\|A = (1/2) ∫ r^2 dθ` | parametric_calculus_generator.py |
| `POLAR_BOUNDS` | 2 | `POLAR_BOUNDS\|r\|0..6` | double_integral_generator.py |
| `POLAR_CONVERT` | 2 | `POLAR_CONVERT\|x^2 + y^2\|r^2` | double_integral_generator.py |
| `POLAR_EVAL` | 3 | `POLAR_EVAL\|theta range * radial integral\|pi * 324\|324*pi` | double_integral_generator.py |
| `POLAR_FORM` | 1 | `POLAR_FORM\|6sqrt2 cis(135 deg)` | euler_formula_generator.py |
| `POLAR_FORMULA` | 1 | `POLAR_FORMULA\|r = √(x^2 + y^2), tan θ = y/x` | polar_parametric_generator.py |
| `POLAR_SETUP` | 2 | `POLAR_SETUP\|(x, y) = (6, 6)\|polar (r ≥ 0, 0° ≤ θ < 360°)` | parametric_calculus_generator.py, polar_parametric_generator.py |
| `POLES` | 1 | `POLES\|s=-1, -8` | transfer_function_generator.py |
| `POLE_ORDER` | 1 | `POLE_ORDER\|2` | residue_generator.py |
| `POLE_TEST` | 3 | `POLE_TEST\|pole -7\|abs(-7) < 7\|outside` | contour_integral_generator.py |
| `POLYDIV_SETUP` | 2 | `POLYDIV_SETUP\|3x^3 + 9x^2 - 7x + 23\|x + 4` | finite_field_generator.py, polynomial_long_division_generator.py |
| `POLY_ACCUM` | 2 | `POLY_ACCUM\|x^0\|1` | finite_field_generator.py |
| `POLY_ADD_START` | 1 | `POLY_ADD_START\|max degree 2` | finite_field_generator.py |
| `POLY_COEFF` | 3 | `POLY_COEFF\|sum\|x^0\|0` | finite_field_generator.py |
| `POLY_COMBINE` | 1 | `POLY_COMBINE\|-x^3 + 4x^2 + 6x + 9` | multiplying_binomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_DIST_NEG` | 1 | `POLY_DIST_NEG\|Distribute negative sign to second polynomial` | polynomial_add_sub_generator.py |
| `POLY_DIV_SETUP` | 1 | `POLY_DIV_SETUP\|(20x^3 - 5x^3) / (-5x^3)` | polynomial_div_monomial_generator.py |
| `POLY_DIV_SPLIT` | 1 | `POLY_DIV_SPLIT\|(20x^3) / (-5x^3) + (-5x^3) / (-5x^3)` | polynomial_div_monomial_generator.py |
| `POLY_FORMULA` | 1 | `POLY_FORMULA\|A = (1/2)·a·P` | regular_polygon_area_generator.py |
| `POLY_GROUP_LIKE` | 1 | `POLY_GROUP_LIKE\|(-1x^3) + (4x^2) + (6x) + (9)` | multiplying_polynomials_generator.py, polynomial_add_sub_generator.py |
| `POLY_INPUT` | 2 | `POLY_INPUT\|f(x)\|x^2 + 1` | finite_field_generator.py |
| `POLY_MULT_SETUP` | 1 | `POLY_MULT_SETUP\|(2x - 3)(-x^2 - 4x - 3)` | multiplying_polynomials_generator.py |
| `POLY_MUL_START` | 2 | `POLY_MUL_START\|degree 2\|degree 2` | finite_field_generator.py |
| `POLY_REMAINDER` | 1 | `POLY_REMAINDER\|x^2 + x + 1` | finite_field_generator.py |
| `POLY_SCALE` | 3 | `POLY_SCALE\|x^3 - 3x/5\|5/2\|(5x^3 - 3x)/2` | legendre_construction_generator.py |
| `POLY_SETUP` | 1, 2 | `POLY_SETUP\|(-x^3 + 4x^2 + 9) + (6x)` | factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, polynomial_add_sub_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, regular_polygon_area_generator.py |
| `POLY_SUB` | 2, 3 | `POLY_SUB\|(3x^3 + 9x^2) - (3x^3 + 12x^2)\|-3x^2` | legendre_construction_generator.py, polynomial_long_division_generator.py |
| `PORT_FORMULA` | 2 | `PORT_FORMULA\|E=wA*rA+wB*rB\|Var=wA^2*varA+wB^2*varB+2*wA*wB*cov` | portfolio_generator.py |
| `PORT_RESULT` | 2 | `PORT_RESULT\|expected_return=13/150\|variance=109/3600` | portfolio_generator.py |
| `PORT_SETUP` | 3 | `PORT_SETUP\|wA=2/3,wB=1/3\|rA=6%,rB=14%\|varA=0.0625,varB=0.0225,cov=0` | portfolio_generator.py |
| `POSTERIOR_PARAM` | 1 | `POSTERIOR_PARAM\|alpha' = alpha + successes` | bayesian_update_generator.py |
| `POST_PRECISION` | 1 | `POST_PRECISION\|prior precision + data precision` | bayesian_update_generator.py |
| `POTENTIAL_BUILD` | 3 | `POTENTIAL_BUILD\|integrate P dx\|2*x^2 + 4*x*y - 3*x + g(y)\|g'(y) remains` | exact_ode_generator.py, line_integral_generator.py |
| `POTENTIAL_RESULT` | 2 | `POTENTIAL_RESULT\|phi(x,y)\|2*x^2 + 2*y^2 + 4*x*y - 3*x + 5*y` | exact_ode_generator.py, line_integral_generator.py |
| `POW` | 2 | `POW\|(3/5)^5\|0.07776` | binomial_probability_generator.py, geometric_distribution_generator.py, recurrence_generator.py |
| `POWER_ENTRY` | 3 | `POWER_ENTRY\|(1,1)\|(-3) + 27*(-2)\|-57` | diagonalization_generator.py |
| `POWER_FORM` | 1 | `POWER_FORM\|A^3 = P*D^3*P^-1` | diagonalization_generator.py |
| `POWER_INTEGRAL` | 2 | `POWER_INTEGRAL\|int_0^a x dx\|a^2/2` | continuous_distribution_generator.py, wavefunction_generator.py |
| `POWER_REDUCE` | 2 | `POWER_REDUCE\|15^177\|15^15 mod 19` | totient_generator.py |
| `POWER_RULE` | 2 | `POWER_RULE\|5x^5\|25x^4` | chain_rule_generator.py, commutator_generator.py, curve_analysis_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, lhopital_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, mean_value_theorem_generator.py, optimization_generator.py, tangent_line_generator.py |
| `POWER_SETUP` | 2 | `POWER_SETUP\|i^i\|principal logarithm` | complex_log_generator.py |
| `POWER_SET_RESULT` | 1 | `POWER_SET_RESULT\|{{}, {a}, {b}, {c}, {e}, {a, b}, {a, c}, {a, e}, {b, c}, {b, e}, {c, e}, {a, b, c}, {a, b, e}, {a, c, e}, {b, c, e}, {a, b, c, e}}` | set_operations_generator.py |
| `POWER_SHIFT` | 3 | `POWER_SHIFT\|k=0\|0-3\|-3` | laurent_series_generator.py |
| `PREDICT` | 2 | `PREDICT\|x*\|50/17` | kernel_ridge_generator.py |
| `PRIME` | 1 | `PRIME\|89` | divisibility_classification_generator.py |
| `PRIM_CANDIDATES` | 2 | `PRIM_CANDIDATES\|visited E\|CE=4, AE=20, BE=21, DE=22` | mst_generator.py |
| `PRIM_START` | 1 | `PRIM_START\|E` | mst_generator.py |
| `PRINCIPAL_LOG` | 1 | `PRINCIPAL_LOG\|Log(i) = i*pi/2` | complex_log_generator.py |
| `PRINCIPAL_MINOR` | 2 | `PRINCIPAL_MINOR\|K11\|11` | kernel_validity_generator.py |
| `PRIOR_PRECISION` | 1 | `PRIOR_PRECISION\|1/tau^2` | bayesian_update_generator.py |
| `PROBABILITY` | 2 | `PROBABILITY\|P(+z)\|49/625` | spin_half_generator.py |
| `PROB_CONDITIONAL` | 2 | `PROB_CONDITIONAL\|P(second clubs\|first was clubs)\|4/17 = 12/51` | compound_probability_generator.py |
| `PROB_DEPENDENT` | 1 | `PROB_DEPENDENT\|Drawing without replacement means dependent events` | compound_probability_generator.py |
| `PROB_DESCRIBE` | 1 | `PROB_DESCRIBE\|Coin flip and die roll, looking for heads and 2` | compound_probability_generator.py |
| `PROB_IDENTIFY` | 2 | `PROB_IDENTIFY\|P(heads)\|1/2` | compound_probability_generator.py |
| `PROB_INDEPENDENT` | 1 | `PROB_INDEPENDENT\|Coin flip and die roll are independent events` | compound_probability_generator.py |
| `PROB_MULTIPLY` | 3 | `PROB_MULTIPLY\|1/2\|1/6\|1/12` | compound_probability_generator.py |
| `PROB_SETUP` | 2 | `PROB_SETUP\|6\|6` | simple_probability_generator.py |
| `PROB_SIMPLIFY` | 2 | *(not observed in sampling)* | compound_probability_generator.py |
| `PROB_WEIGHT` | 2 | `PROB_WEIGHT\|1/sqrt2^2\|1/2` | clebsch_gordan_generator.py |
| `PRODUCT` | 2 | `PRODUCT\|Delta x^2 * Delta p^2\|3600pi^2/12 - 1/2` | uncertainty_generator.py |
| `PROJECT` | 2 | `PROJECT\|P1\|0` | pca_generator.py |
| `PROJECTILE_SETUP` | 3 | `PROJECTILE_SETUP\|vx=51\|vy=13\|g=10` | projectile_motion_generator.py |
| `PROJECTION` | 2 | `PROJECTION\|X*beta\|[-1, 3, 7, 11]` | least_squares_generator.py, legendre_construction_generator.py |
| `PROJECTOR_SETUP` | 2 | `PROJECTOR_SETUP\|P_plus=ket+bra+\|P=[[1/2,1/2],[1/2,1/2]]` | projector_generator.py |
| `PROJ_COEFF` | 3 | `PROJ_COEFF\|v2 on u1\|60/20\|3` | gram_schmidt_generator.py |
| `PROJ_VECTOR` | 2 | `PROJ_VECTOR\|3*u1\|[12, 6, 0]` | gram_schmidt_generator.py |
| `PROPERTY_RESULT` | 2 | `PROPERTY_RESULT\|reflexive\|no` | relation_check_generator.py |
| `PROP_SETUP` | 1 | `PROP_SETUP\|9/3 = x/4` | proportion_word_problem_generator.py, proportional_relationship_generator.py, similar_triangles_generator.py, triangle_solve_generator.py |
| `PSD_SETUP` | 2 | `PSD_SETUP\|K=[[11,-13], [-13,8]]\|criterion=all principal minors >= 0` | kernel_validity_generator.py |
| `PURITY` | 1 | `PURITY\|Tr(rho^2)=17/32` | density_matrix_generator.py |
| `PYTHAG_CALCULATE` | 2 | `PYTHAG_CALCULATE\|d² = 225 + 400 = 625\|625` | pythag_leg_generator.py |
| `PYTHAG_CONTEXT` | 2 | `PYTHAG_CONTEXT\|displacement\|east=15m, north=20m` | pythag_leg_generator.py |
| `PYTHAG_FORMULA` | 1 | `PYTHAG_FORMULA\|a² + b² = c²` | pythag_leg_generator.py |
| `PYTHAG_MODEL` | 3 | `PYTHAG_MODEL\|east=15\|north=20\|distance=?` | pythag_leg_generator.py |
| `PYTHAG_ROOT` | 2 | `PYTHAG_ROOT\|196\|14` | pythag_leg_generator.py |
| `PYTHAG_SETUP` | 3 | `PYTHAG_SETUP\|c=50\|a=48\|b=?` | pythag_leg_generator.py |
| `PYTHAG_SOLVE` | 2 | `PYTHAG_SOLVE\|b² = 2500 - 2304\|196` | pythag_leg_generator.py |
| `PYTHAG_SQUARE` | 2 | `PYTHAG_SQUARE\|48\|2304` | pythag_leg_generator.py |
| `PYTHAG_SUBSTITUTE` | 1 | `PYTHAG_SUBSTITUTE\|48² + b² = 50²` | pythag_leg_generator.py |
| `Q1` | 4 | `Q1\|6\|30\|6\|6` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `Q2` | 4 | `Q2\|6\|30\|6\|-4` | complex_quadratic_generator.py, polynomial_zeros_generator.py, quadratic_generator.py |
| `QN_ADD` | 4 | `QN_ADD\|Q\|left\|0 + gamma(0)\|0` | conservation_law_generator.py |
| `QUADRANT` | 2 | `QUADRANT\|84°\|quadrant I` | angle_measure_generator.py, polar_parametric_generator.py, unit_circle_generator.py |
| `QUADRATIC` | 3 | `QUADRATIC\|3\|0\|-75` | mobius_transform_generator.py |
| `QUANTUM_FORMULA` | 1 | `QUANTUM_FORMULA\|K_max=h*f-phi` | quantum_formula_generator.py |
| `QUANTUM_SETUP` | 2, 3 | `QUANTUM_SETUP\|gate=CNOT\|input=ket10` | quantum_formula_generator.py, quantum_gate_generator.py |
| `QUANT_SETUP` | 3 | `QUANT_SETUP\|x=(-36/25,-9/50,153/100)\|scale=1/25\|zero_point=7` | quantization_generator.py |
| `QUANT_VALUE` | 2 | `QUANT_VALUE\|1\|-29` | quantization_generator.py |
| `QUARK_CHARGE` | 2 | `QUARK_CHARGE\|u\|2/3` | quark_composition_generator.py |
| `QUARK_SETUP` | 3 | `QUARK_SETUP\|meson\|u anti_b\|u=2/3,d=-1/3,s=-1/3,c=2/3,b=-1/3; anti=-charge` | quark_composition_generator.py |
| `QUARTILE` | 3 | `QUARTILE\|Q1\|5,6,8,10,13\|8` | five_number_summary_generator.py |
| `QUAT_COMPONENT` | 3 | `QUAT_COMPONENT\|q*v\|real\|-1` | quaternion_generator.py |
| `QUAT_INVERSE` | 2 | `QUAT_INVERSE\|q\|(0,0,-1,0)` | quaternion_generator.py |
| `QUAT_MUL_START` | 3 | `QUAT_MUL_START\|q*v\|q\|v` | quaternion_generator.py |
| `QUAT_RESULT` | 2 | `QUAT_RESULT\|q*v\|(-1,3,0,1)` | quaternion_generator.py |
| `QUAT_SETUP` | 2 | `QUAT_SETUP\|q=(0,0,1,0)\|v=(0,-1,1,3)` | quaternion_generator.py |
| `QUEUE_STATE` | 2 | `QUEUE_STATE\|initial\|A` | graph_traversal_generator.py |
| `QUOTIENT` | 1 | `QUOTIENT\|x` | finite_field_generator.py |
| `R` | 1 | `R\|21` | complex_number_ops_generator.py, finite_field_generator.py, long_division_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `RAPIDITY_SUM` | 2 | `RAPIDITY_SUM\|collinear boosts\|-13/6` | minkowski_interval_generator.py |
| `RATE_MONTHLY` | 2 | `RATE_MONTHLY\|24% / 12\|0.02` | finance_generator.py |
| `RATE_SETUP` | 2 | `RATE_SETUP\|10 ft ladder; the base slides away at 4 ft/s; base is 6 ft from the wall\|dy/dt` | related_rates_generator.py |
| `RATIO` | 2, 3 | `RATIO\|3*y = 3*x\|y = x` | lagrange_multiplier_generator.py, simplex_generator.py |
| `RATIONALIZE` | 1 | `RATIONALIZE\|(2 - √2)/(2 - √2)` | dot_product_generator.py, limit_evaluation_generator.py, radical_rationalize_generator.py, special_right_triangle_generator.py |
| `RATIO_BASE` | 3 | `RATIO_BASE\|35:15\|5\|7:3` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RATIO_TABLE` | 2 | `RATIO_TABLE\|Water (oz): ?, 35, 49, 84\|Concentrate (oz): 9, 15, 21, 36` | error_spotting_generator.py, fill_in_step_generator.py, ratio_table_generator.py |
| `RAW_FORMULA` | 1 | `RAW_FORMULA\|x = μ + z·σ` | z_score_generator.py |
| `REARRANGE_EQ` | 1 | `REARRANGE_EQ\|whole = 120 / 0.2` | percent_problem_generator.py |
| `RECIPROCAL` | 2 | `RECIPROCAL\|csc θ = 1/sin θ\|-5/3` | trig_six_functions_generator.py |
| `RECOVER_DATA` | 2 | `RECOVER_DATA\|positions 3,5,6,7\|0101` | hamming_code_generator.py |
| `RECT_FORM` | 1 | `RECT_FORM\|-3i` | de_moivre_generator.py, euler_formula_generator.py |
| `RECURRENCE` | 2 | `RECURRENCE\|a_(n+1)\|a_n/(n+1)` | derangement_generator.py, series_solution_generator.py |
| `REC_SETUP` | 2 | `REC_SETUP\|a_n = 5 a_(n-1) - 6 a_(n-2) + 8\|a_0 = -1, a_1 = -8` | recurrence_generator.py |
| `REDUCED_DENSITY` | 1 | `REDUCED_DENSITY\|rho_A=[[1/2,1/2],[1/2,1/2]]` | partial_trace_generator.py |
| `REFLEXIVE_CHECK` | 2 | `REFLEXIVE_CHECK\|(1, 1)\|missing` | relation_check_generator.py |
| `REGION_MEASURE` | 3 | `REGION_MEASURE\|volume\|4*9*10\|360` | vector_theorem_generator.py |
| `REGION_REWRITE` | 2 | `REGION_REWRITE\|0 <= y <= 4\|y/2 <= x <= 2` | double_integral_generator.py |
| `REG_ROW` | 3 | `REG_ROW\|x-x̄=-2\|y-ȳ=1\|product=-2` | regression_generator.py |
| `REG_SETUP` | 2 | `REG_SETUP\|points: (1, 69), (2, 67), (3, 70), (4, 66), (5, 68)\|coefficient of determination r^2` | regression_generator.py |
| `REJECT` | 2 | `REJECT\|(1, -45)\|sum is -44, need -4` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, optimization_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `RELAX` | 3 | `RELAX\|D->C\|update inf to 5\|via weight 5` | dijkstra_generator.py |
| `RELU` | 3 | `RELU\|z=3\|h=3\|deriv=1` | backprop_generator.py |
| `REL_ENERGY_FORMULA` | 1 | `REL_ENERGY_FORMULA\|E=m*c^2` | relativistic_energy_generator.py |
| `REL_ENERGY_SETUP` | 3 | `REL_ENERGY_SETUP\|rest_energy\|m=9\|c=20` | relativistic_energy_generator.py |
| `REL_FORMULA` | 1 | `REL_FORMULA\|ct_prime=gamma*(ct-beta*x), x_prime=gamma*(x-beta*ct)` | special_relativity_generator.py |
| `REL_SETUP` | 2, 3 | `REL_SETUP\|A = {1, 2, 3}\|R = {(1, 3), (3, 1)}` | relation_check_generator.py, special_relativity_generator.py |
| `REP_DIM` | 2 | `REP_DIM\|6bar\|6` | young_tableaux_generator.py |
| `RESIDUAL` | 2 | `RESIDUAL\|y - X*beta\|[-2, 2, 2, -2]` | least_squares_generator.py |
| `RESIDUE` | 1, 3 | `RESIDUE\|-8` | contour_integral_generator.py, residue_generator.py |
| `RESIDUE_SETUP` | 2 | `RESIDUE_SETUP\|a=1\|f=(4 - 8(z-1) + 4(z-1)^2 + 2(z-1)^3)/(z-1)^2` | residue_generator.py |
| `RESIDUE_SUM` | 1 | `RESIDUE_SUM\|-6` | contour_integral_generator.py |
| `RESID_SETUP` | 2 | `RESID_SETUP\|point (3, 64), line ŷ = 67.4 - 0.8x\|residual = observed − predicted` | regression_generator.py |
| `REVERSE` | 2 | `REVERSE\|0,0,0,0,1,1,1\|1110000` | base_arithmetic_generator.py, base_conversion_generator.py, bitwise_ops_generator.py |
| `REWRITE` | 1, 2 | `REWRITE\|8 + 90` | antiderivative_generator.py, arc_length_generator.py, area_between_curves_generator.py, chain_rule_generator.py, circle_equation_generator.py, completing_square_generator.py, complex_division_generator.py, complex_log_generator.py, complex_number_ops_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, cramers_rule_generator.py, curve_analysis_generator.py, definite_integral_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, domain_range_generator.py, dot_product_generator.py, euler_formula_generator.py, evaluate_expression_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, frequency_table_generator.py, function_composition_generator.py, function_operations_generator.py, horner_evaluation_generator.py, implicit_diff_generator.py, improper_integral_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, inverse_function_generator.py, laurent_series_generator.py, lhopital_generator.py, limit_evaluation_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logistic_growth_generator.py, matrix_inverse_generator.py, method_of_moments_generator.py, mgf_generator.py, midpoint_generator.py, mle_generator.py, normal_table_generator.py, ode_substitution_generator.py, optimization_generator.py, order_of_operations_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, permutation_combination_generator.py, polar_parametric_generator.py, polynomial_zeros_generator.py, power_series_generator.py, quadratic_factoring_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, recursive_explicit_generator.py, regression_generator.py, related_rates_generator.py, right_triangle_trig_generator.py, row_reduction_generator.py, separable_ode_generator.py, series_convergence_generator.py, series_solution_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, solid_revolution_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spin_half_generator.py, standard_form_conversion_generator.py, stars_and_bars_generator.py, synthetic_division_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, u_substitution_generator.py, vector_ops_generator.py, z_transform_generator.py |
| `RG_SETUP` | 3 | `RG_SETUP\|one_loop\|alpha0=1/31\|beta=1,L=1/4` | running_coupling_generator.py |
| `RICCI_ENTRY` | 2 | `RICCI_ENTRY\|R_phiphi\|1` | riemann_tensor_generator.py |
| `RIDGE_ENTRY` | 2 | `RIDGE_ENTRY\|K\|[[16,-16], [-16,16]]` | kernel_ridge_generator.py |
| `RIEMANN_ENTRY` | 2 | `RIEMANN_ENTRY\|R^phi_theta phi theta\|1/2` | riemann_tensor_generator.py |
| `RIEMANN_SETUP` | 2, 3 | `RIEMANN_SETUP\|f(x) = 2x + 2 on [-2, 2], n = 4\|right Riemann sum` | riemann_sum_generator.py, riemann_tensor_generator.py |
| `RK_COMBINE` | 2 | `RK_COMBINE\|k1+2k2+2k3+k4\|-21/4` | runge_kutta_generator.py |
| `RK_STAGE` | 3 | `RK_STAGE\|k1\|x=0\|y=1` | runge_kutta_generator.py |
| `RODRIGUES_FORM` | 2 | `RODRIGUES_FORM\|e^(theta K)\|I + sin(theta)K + (1-cos(theta))K^2` | lie_exponential_generator.py |
| `ROOT` | 1, 2, 3 | `ROOT\|289\|17` | ac_circuit_generator.py, adam_step_generator.py, completing_square_generator.py, confidence_interval_generator.py, de_moivre_generator.py, doppler_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, factor_special_forms_generator.py, four_vector_generator.py, fundamental_form_generator.py, hypothesis_test_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, ladder_operator_generator.py, layer_norm_generator.py, low_rank_approx_generator.py, matrix_norm_generator.py, metric_arc_length_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, planck_units_generator.py, pythag_hyp_generator.py, quadratic_generator.py, quadratic_square_root_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rational_equation_generator.py, rational_exponent_generator.py, regression_generator.py, relativistic_energy_generator.py, round_solids_generator.py, rv_transform_generator.py, schwarzschild_generator.py, shm_generator.py, svd_generator.py, svm_margin_generator.py |
| `ROOT_ANGLE` | 2 | `ROOT_ANGLE\|k=0\|0 deg` | de_moivre_generator.py |
| `ROOT_EXTRACT` | 2 | `ROOT_EXTRACT\|8` | exponent_generator.py |
| `ROOT_IDENTIFY` | 3 | `ROOT_IDENTIFY\|64\|perfect_square\|8` | exponent_generator.py |
| `ROOT_SETUP` | 1 | `ROOT_SETUP\|√64` | exponent_generator.py, radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `ROOT_SIMPLIFY` | 1, 2 | `ROOT_SIMPLIFY\|3√7` | complex_quadratic_generator.py, distance_formula_generator.py, dot_product_generator.py, euler_formula_generator.py, exponent_generator.py, geometric_mean_generator.py, hypercube_counting_generator.py, polar_parametric_generator.py, vector_ops_generator.py |
| `ROTATED_VECTOR` | 1 | `ROTATED_VECTOR\|(1,1,-3)` | quaternion_generator.py |
| `ROT_FORMULA` | 1 | `ROT_FORMULA\|I1*omega1=I2*omega2` | rotational_dynamics_generator.py |
| `ROT_SETUP` | 3 | `ROT_SETUP\|angular_momentum\|I1=19, omega1=25\|I2=21` | rotational_dynamics_generator.py |
| `ROUND` | 2 | `ROUND\|-29\|-29` | quantization_generator.py |
| `ROUNDTRIP_ERROR` | 2 | `ROUNDTRIP_ERROR\|sum_abs\|3/100` | quantization_generator.py |
| `ROUND_CHECK` | 3 | `ROUND_CHECK\|68867\|100\|>=5` | place_value_rounding_generator.py |
| `ROUND_RESULT` | 2 | `ROUND_RESULT\|68867\|68900` | place_value_rounding_generator.py |
| `ROUTH_ROW` | 2 | `ROUTH_ROW\|s^3\|1, 2` | routh_hurwitz_generator.py |
| `ROUTH_SETUP` | 1 | `ROUTH_SETUP\|p(s)=s^3+11s^2+2s+62` | routh_hurwitz_generator.py |
| `ROW_OP` | 1, 2 | `ROW_OP\|R2 → R2 + 2·R1\|[0, 1, 2, 9]` | row_reduction_generator.py, simplex_generator.py, subspace_basis_generator.py |
| `RREF_RESULT` | 2 | `RREF_RESULT\|RREF(A)\|[[1, 0, -3, -2], [0, 1, -3, -4], [0, 0, 0, 0]]` | subspace_basis_generator.py |
| `RSA_DECRYPT` | 2 | `RSA_DECRYPT\|153\|97` | rsa_generator.py |
| `RSA_ENCRYPT` | 2 | `RSA_ENCRYPT\|97\|153` | rsa_generator.py |
| `RSA_PRIVATE_KEY` | 1 | `RSA_PRIVATE_KEY\|d=101` | rsa_generator.py |
| `RSA_PUBLIC_KEY` | 2 | `RSA_PUBLIC_KEY\|n=203\|e=5` | rsa_generator.py |
| `RSA_SETUP` | 3 | `RSA_SETUP\|p=7\|q=29\|message=97` | rsa_generator.py |
| `RSQ_FORMULA` | 1 | `RSQ_FORMULA\|r^2 = Sxy^2/(Sxx·Syy)` | regression_generator.py |
| `S` | 3 | `S\|632\|594\|38` | ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, angle_defect_generator.py, angle_measure_generator.py, annuity_generator.py, arc_length_generator.py, area_between_curves_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, backprop_generator.py, bayesian_update_generator.py, binomial_probability_generator.py, bisection_generator.py, black_scholes_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, casimir_force_generator.py, channel_capacity_generator.py, circle_angle_generator.py, circle_equation_generator.py, collision_generator.py, commutator_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, composite_arithmetic_generator.py, confidence_interval_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, cramers_rule_generator.py, decimal_div_generator.py, definite_integral_generator.py, density_matrix_generator.py, determinant_generator.py, dft_generator.py, distance_formula_generator.py, doppler_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, entropy_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_method_generator.py, expected_value_generator.py, exponential_model_generator.py, extended_euclid_generator.py, finance_generator.py, finite_difference_generator.py, first_law_generator.py, five_number_summary_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_op_generator.py, function_inner_product_generator.py, function_operations_generator.py, fundamental_form_generator.py, game_theory_generator.py, gaussian_curvature_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_sequence_generator.py, gradient_descent_generator.py, gradient_step_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, hamiltonian_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, information_gain_generator.py, integrating_factor_generator.py, interpolation_generator.py, invariant_mass_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrangian_generator.py, layer_norm_generator.py, linear_simple_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, modular_inverse_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, normal_table_generator.py, npv_irr_generator.py, ode_substitution_generator.py, ode_system_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, parametric_calculus_generator.py, particle_in_box_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, permutation_group_generator.py, ph_calculation_generator.py, piecewise_evaluation_generator.py, positive_definite_generator.py, probability_addition_rule_generator.py, quadratic_residue_generator.py, quantization_generator.py, quantum_formula_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_rationalize_generator.py, rational_expr_add_sub_generator.py, recurrence_generator.py, regression_generator.py, related_rates_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, rotational_dynamics_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, rv_transform_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, series_convergence_generator.py, shm_generator.py, signal_arithmetic_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, special_relativity_generator.py, spherical_excess_generator.py, spin_half_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, stereographic_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tip_bill_split_generator.py, totient_generator.py, transformation_generator.py, transportation_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, vector_ops_generator.py, z_score_generator.py |
| `SAMPLE_MOMENT` | 2 | `SAMPLE_MOMENT\|xbar\|11/2` | method_of_moments_generator.py |
| `SAMPLE_SIZE_FORMULA` | 1 | `SAMPLE_SIZE_FORMULA\|n = (z*·σ/E)^2` | confidence_interval_generator.py |
| `SA_BASES` | 2 | `SA_BASES\|2π(10)² = 2π × 100\|200π` | volume_3d_generator.py |
| `SA_FACES` | 3 | `SA_FACES\|top/bottom\|3 × 11\|33` | volume_3d_generator.py |
| `SA_FORMULA` | 1 | `SA_FORMULA\|SA = 2(lw + lh + wh)` | round_solids_generator.py, volume_3d_generator.py |
| `SA_LATERAL` | 2 | `SA_LATERAL\|2π × 10 × 6\|120π` | volume_3d_generator.py |
| `SA_SETUP` | 2 | `SA_SETUP\|rectangular_prism\|l=3, w=11, h=12` | volume_3d_generator.py |
| `SA_TOTAL` | 2 | `SA_TOTAL\|SA = 2(33 + 36 + 132)\|402` | round_solids_generator.py, volume_3d_generator.py |
| `SB_FORMULA` | 1 | `SB_FORMULA\|C(n+k-1, k-1)` | stars_and_bars_generator.py |
| `SB_SETUP` | 2 | `SB_SETUP\|x1+...+x5 = 7\|xi >= 0` | stars_and_bars_generator.py |
| `SCALE_DIV` | 3 | `SCALE_DIV\|72\|12\|6.0` | scaling_generator.py |
| `SCALE_EXACT` | 2 | `SCALE_EXACT\|3*cos\|0` | de_moivre_generator.py, euler_formula_generator.py |
| `SCALE_IDENTIFY` | 2 | `SCALE_IDENTIFY\|72 feet\|scaled_dimension` | scaling_generator.py |
| `SCALE_MULT` | 3 | `SCALE_MULT\|3.5\|10\|35.0` | scaling_generator.py |
| `SCALE_SETUP` | 3 | `SCALE_SETUP\|1 inch\|12 feet\|12` | scaling_generator.py |
| `SCALE_SHIFT` | 2 | `SCALE_SHIFT\|1\|-7` | layer_norm_generator.py |
| `SCALING_COMPUTE` | 2 | `SCALING_COMPUTE\|6ND\|15600000000000000000` | scaling_law_generator.py |
| `SCALING_SETUP` | 3 | `SCALING_SETUP\|N=1300000000\|D=2000000000\|F=20000000000000000` | scaling_law_generator.py |
| `SCHWARZSCHILD_SETUP` | 3, 4 | `SCHWARZSCHILD_SETUP\|radius\|G=5\|M=117\|c=3` | schwarzschild_generator.py |
| `SCI_IDENTIFY` | 2 | `SCI_IDENTIFY\|1.3\|2` | exponent_generator.py |
| `SCI_MOVE_DECIMAL` | 2 | `SCI_MOVE_DECIMAL\|right\|2` | exponent_generator.py |
| `SCI_OPERATION` | 4 | `SCI_OPERATION\|multiply_coefficients\|4.5\|2.3\|10.35` | exponent_generator.py |
| `SCI_SETUP` | 1 | `SCI_SETUP\|1.3 × 10^2` | exponent_generator.py |
| `SCORE_EQ` | 1 | `SCORE_EQ\|16-9*mu=0` | mle_generator.py |
| `SEARCH_BOUNDS` | 3 | `SEARCH_BOUNDS\|iter 1\|lo=0\|hi=6` | algorithm_trace_generator.py |
| `SEARCH_STATE` | 2 | `SEARCH_STATE\|lo=4\|hi=6` | algorithm_trace_generator.py |
| `SECOND_DERIV_TEST` | 2 | `SECOND_DERIV_TEST\|f'' < 0 for x < 4, f'' > 0 for x > 4\|concavity changes` | curve_analysis_generator.py, optimization_generator.py |
| `SECOND_PARTIAL` | 2 | `SECOND_PARTIAL\|f_xx\|10` | hessian_classify_generator.py |
| `SECTION_FORMULA` | 1 | `SECTION_FORMULA\|P = (x1 + m/(m+n)·(x2 - x1), y1 + m/(m+n)·(y2 - y1))` | segment_partition_generator.py |
| `SECTION_SETUP` | 2 | `SECTION_SETUP\|A(1, -6), B(-9, -21); ratio 1:4 from A\|point P` | segment_partition_generator.py |
| `SECTOR_FORMULA` | 1 | `SECTOR_FORMULA\|A = (θ/360)·πr^2` | arc_sector_generator.py |
| `SELECT_MIN` | 2 | `SELECT_MIN\|D\|0` | dijkstra_generator.py |
| `SELECT_RELEVANT` | 2 | `SELECT_RELEVANT\|base = 160, rate = 30%\|ignore 16 (irrelevant)` | percent_word_problem_generator.py, proportion_word_problem_generator.py |
| `SEPARATE` | 1 | `SEPARATE\|y^(-2) dy = dx` | ode_substitution_generator.py, separable_ode_generator.py |
| `SEQ_APPLY` | 1 | `SEQ_APPLY\|a_29 = -3 + (29 - 1)·-3` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_FORMULA` | 1 | `SEQ_FORMULA\|a_n = a_1 + (n - 1)d` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SEQ_SETUP` | 2 | `SEQ_SETUP\|-3, -6, -9, -12, ...\|sum of first 29 terms` | arithmetic_sequence_generator.py, geometric_sequence_generator.py, recursive_explicit_generator.py |
| `SERIES` | 1 | `SERIES\|G=G1*G2` | transfer_function_generator.py |
| `SERIES_ASSUME` | 2 | `SERIES_ASSUME\|y\|sum a_n x^n` | series_solution_generator.py |
| `SERIES_GROUP` | 2 | `SERIES_GROUP\|even powers\|cos(theta)I` | lie_exponential_generator.py |
| `SERIES_SETUP` | 2 | `SERIES_SETUP\|Σ -1·(-2/3)^n, n ≥ 0\|converge or diverge? find the sum if it converges` | power_series_generator.py, series_convergence_generator.py |
| `SERIES_TERM` | 3 | `SERIES_TERM\|n=0\|1\|1` | grassmann_generator.py |
| `SETUP_PERCENT_EQ` | 1 | `SETUP_PERCENT_EQ\|part = 0.5 * 50` | percent_problem_generator.py |
| `SET_SETUP` | 2, 3 | `SET_SETUP\|A = {b, e, f}\|B = {c, f}\|intersect` | set_operations_generator.py |
| `SHIFT` | 1, 2 | `SHIFT\|yi = xi - 1\|y1+...+y5 = 12` | algorithm_trace_generator.py, recurrence_generator.py, stars_and_bars_generator.py, z_transform_generator.py |
| `SHM_FORMULA` | 1 | `SHM_FORMULA\|omega^2=g/L` | shm_generator.py |
| `SHM_SETUP` | 3 | `SHM_SETUP\|pendulum_period\|g=10\|L=2/5` | shm_generator.py |
| `SIGFIG_ROUND` | 3 | `SIGFIG_ROUND\|12288\|2 significant figures\|1.2 × 10^4` | fermi_estimation_generator.py |
| `SIGMA_EXPAND` | 1 | `SIGMA_EXPAND\|4 + 6 + 8 + 10 + 12` | sigma_notation_generator.py |
| `SIGMA_SETUP` | 2 | `SIGMA_SETUP\|Σ_(k=1)^(5) (2k + 2)\|expand and evaluate` | sigma_notation_generator.py |
| `SIGMA_TERM` | 3 | `SIGMA_TERM\|k=1\|2(1) + 2\|4` | sigma_notation_generator.py |
| `SIGN` | 3 | `SIGN\|left\|-7\|negative` | bisection_generator.py |
| `SIGNAL_SETUP` | 2, 3 | `SIGNAL_SETUP\|sampling\|f_max=1706 Hz\|f_s=6869 Hz` | signal_arithmetic_generator.py |
| `SIGN_RULE` | 2 | `SIGN_RULE\|cos, quadrant I\|positive` | trig_equation_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `SIGN_TEST` | 4 | `SIGN_TEST\|(-inf, -4)\|y = -5\|f(y) = -54 (negative)\|down` | stability_generator.py |
| `SIMILAR_APPLY` | 3 | `SIMILAR_APPLY\|3\|5\|15` | scaling_generator.py |
| `SIMILAR_SCALE` | 3 | `SIMILAR_SCALE\|45\|9\|5` | scaling_generator.py |
| `SIMILAR_SETUP` | 3 | `SIMILAR_SETUP\|triangle\|9,10,3\|45 (others unknown)` | scaling_generator.py |
| `SIMPLEX_SETUP` | 3 | `SIMPLEX_SETUP\|max z=5x+4y\|x<=11\|y<=11` | simplex_generator.py |
| `SIM_SETUP` | 2 | `SIM_SETUP\|△ABC ~ △DEF; DE = 21, AB = 7, EF = 9\|find BC` | similar_triangles_generator.py |
| `SIN` | 2 | `SIN\|pi\|0` | positional_encoding_generator.py |
| `SINGULAR_VALUE` | 2 | `SINGULAR_VALUE\|sigma1\|16` | low_rank_approx_generator.py |
| `SINUSOID_SETUP` | 2 | `SINUSOID_SETUP\|y = 4sin(6(x - π/3))\|amplitude, period, phase shift, midline` | sinusoid_features_generator.py |
| `SLOPE_CALC` | 2 | *(not observed in sampling)* | equation_from_two_points_generator.py |
| `SLOPE_FORMULA` | 1 | `SLOPE_FORMULA\|m = (y2 - y1) / (x2 - x1)` | equation_from_two_points_generator.py, regression_generator.py, slope_two_points_generator.py |
| `SLOPE_INT_IDENTIFY` | 2 | `SLOPE_INT_IDENTIFY\|Slope (m)\|8` | slope_intercept_form_generator.py |
| `SLOPE_INT_MATCH` | 2 | `SLOPE_INT_MATCH\|Compare to Slope-Intercept Form\|y = mx + b` | slope_intercept_form_generator.py |
| `SLOPE_INT_SETUP` | 1 | `SLOPE_INT_SETUP\|y = 8x - 5` | slope_intercept_form_generator.py |
| `SLOPE_RESULT` | 1 | `SLOPE_RESULT\|-5` | equation_from_two_points_generator.py |
| `SLOPE_SETUP` | 2 | `SLOPE_SETUP\|(-4, 9)\|(-4, -2)` | slope_two_points_generator.py |
| `SLOPE_SUBST` | 1 | `SLOPE_SUBST\|m = (-2 - 9) / (-4 - (-4))` | equation_from_two_points_generator.py, slope_two_points_generator.py |
| `SLOPE_UNDEFINED` | 1 | `SLOPE_UNDEFINED\|Division by zero` | slope_two_points_generator.py |
| `SOFTMAX_EXP` | 2 | `SOFTMAX_EXP\|1,1\|1` | attention_generator.py, softmax_gradient_generator.py |
| `SOFTMAX_PROB` | 2 | `SOFTMAX_PROB\|1\|7/15` | softmax_gradient_generator.py |
| `SOFTMAX_SETUP` | 3 | `SOFTMAX_SETUP\|z=(2*ln(7),2*ln(5),2*ln(3))\|T=2\|target=3` | softmax_gradient_generator.py |
| `SOFTMAX_WEIGHT` | 2 | `SOFTMAX_WEIGHT\|1,1\|1/3` | attention_generator.py |
| `SOLUTIONS` | 2 | `SOLUTIONS\|tan x = -1\|135°, 315°` | trig_equation_generator.py |
| `SOLUTION_FORMULA` | 1 | `SOLUTION_FORMULA\|M1*V1=M2*V2` | solution_chem_generator.py |
| `SOLUTION_SETUP` | 3 | `SOLUTION_SETUP\|dilution_stock_volume\|M1=5\|M2=1, V2=212` | solution_chem_generator.py |
| `SOLVE_CONST` | 2 | `SOLVE_CONST\|C1 = 4\|C2 = -3` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py |
| `SOLVE_U` | 2 | `SOLVE_U\|e^(-5x)u = 3e^(-5x) + C\|u = 3 + Ce^(5x)` | ode_substitution_generator.py |
| `SOLVE_Y` | 2 | `SOLVE_Y\|e^(3x)y = 2e^(3x) + C\|y = 2 + Ce^(-3x)` | integrating_factor_generator.py, laplace_ivp_generator.py, ode_substitution_generator.py |
| `SOL_FORM` | 1, 2 | `SOL_FORM\|y = C1e^(-4x) + C2e^(2x)` | ode_system_generator.py, second_order_ode_generator.py, undetermined_coeff_generator.py, variation_parameters_generator.py |
| `SORT` | 2 | `SORT\|5,12,15,9,9\|5,9,9,12,15` | five_number_summary_generator.py, simple_stats_generator.py |
| `SORT_EDGES` | 1 | `SORT_EDGES\|AE=1, CD=5, BC=9, AB=11, AC=13, AD=19, BE=24` | mst_generator.py |
| `SPECIAL_SOLUTION` | 2 | `SPECIAL_SOLUTION\|7 = 7\|identity: true for every x` | radical_equation_generator.py, special_solution_equation_generator.py |
| `SPEED` | 2, 3 | `SPEED\|sqrt(a^2 + b^2)\|sqrt(3^2 + 4^2)\|5` | curve_geometry_generator.py |
| `SPHERICAL_BOUNDS` | 2 | `SPHERICAL_BOUNDS\|rho\|0..12` | triple_integral_generator.py |
| `SPHERICAL_CONVERT` | 2 | `SPHERICAL_CONVERT\|1 dV\|rho^2*sin(phi) drho dphi dtheta` | triple_integral_generator.py |
| `SPHERICAL_COSINES` | 1 | `SPHERICAL_COSINES\|cos(c)=sin(lat1)sin(lat2)+cos(lat1)cos(lat2)cos(dlon)` | great_circle_generator.py |
| `SPHERICAL_COSINE_LAW` | 1 | `SPHERICAL_COSINE_LAW\|cos(a)=cos(b)cos(c)+sin(b)sin(c)cos(A)` | spherical_triangle_generator.py |
| `SPHERICAL_EXCESS_SETUP` | 2 | `SPHERICAL_EXCESS_SETUP\|R=12\|angles=105,90,75` | spherical_excess_generator.py |
| `SPHERICAL_SINE_LAW` | 1 | `SPHERICAL_SINE_LAW\|sin(A)/sin(a)=sin(B)/sin(b)` | spherical_triangle_generator.py |
| `SPHERICAL_TRIANGLE_SETUP` | 2 | `SPHERICAL_TRIANGLE_SETUP\|a=150 deg, b=60 deg, A=150 deg\|find sin(B)` | spherical_triangle_generator.py |
| `SPIN_COMPONENT` | 2 | `SPIN_COMPONENT\|row=1\|-15/17` | spin_half_generator.py |
| `SPIN_SETUP` | 3 | `SPIN_SETUP\|eigenvalue\|operator=sigma_y\|psi=(ket0 - i ket1)/sqrt(2)` | spin_half_generator.py |
| `SPLIT_MIDDLE` | 2 | `SPLIT_MIDDLE\|-13x = -15x + 2x\|6x^2 - 15x + 2x - 5` | factor_trinomial_generator.py |
| `SPLIT_SETUP` | 3 | `SPLIT_SETUP\|source\|left pos=3, neg=5\|right pos=3, neg=5` | information_gain_generator.py |
| `SQRT_BOTH_SIDES` | 2 | `SQRT_BOTH_SIDES\|(x - 7)^2 = 121\|x - 7 = ±11` | completing_square_generator.py, quadratic_square_root_generator.py, rational_equation_generator.py |
| `SQRT_DIGIT` | 2 | `SQRT_DIGIT\|4\|root = 4` | manual_square_root_generator.py |
| `SQRT_NEG` | 2 | `SQRT_NEG\|√(-64)\|8i` | complex_quadratic_generator.py, polynomial_zeros_generator.py |
| `SQRT_SETUP` | 2 | `SQRT_SETUP\|N = 379\|x0 = 10` | manual_square_root_generator.py |
| `SQRT_TRIAL` | 3 | `SQRT_TRIAL\|x = 4\|(0 + 4)*4 = 16\|fits` | manual_square_root_generator.py |
| `SQUARE_BOTH_SIDES` | 2 | `SQUARE_BOTH_SIDES\|√(2x + 0) = 4\|2x + 0 = 16` | radical_equation_generator.py |
| `SQUARE_FACTOR` | 3 | `SQUARE_FACTOR\|20\|4 × 5\|4` | radical_add_sub_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py |
| `SQUARE_TEST` | 3 | `SQUARE_TEST\|72\|8^2 = 64, 9^2 = 81\|not a perfect square` | discriminant_generator.py |
| `STABILITY` | 3 | `STABILITY\|y=-4\|left down, right up\|unstable` | stability_generator.py |
| `STANDING_BOUNDARY` | 1 | `STANDING_BOUNDARY\|open-open pipe allows n=1,2,3,...` | standing_wave_generator.py |
| `STANDING_FORMULA` | 1 | `STANDING_FORMULA\|lambda=2L/n, f=v/lambda` | standing_wave_generator.py |
| `STANDING_SETUP` | 3 | `STANDING_SETUP\|open_pipe\|n=5\|L=19, v=28` | standing_wave_generator.py |
| `STATICS_FORMULA` | 1 | `STATICS_FORMULA\|sum_tau_left=0 => RB*L=W*x` | statics_generator.py |
| `STATICS_SETUP` | 3 | `STATICS_SETUP\|supported_beam\|W=136, L=13\|x=4` | statics_generator.py |
| `STAT_ABS_DEV` | 2 | `STAT_ABS_DEV\|-5\|5` | statistics_generator.py |
| `STAT_AVERAGE` | 2 | `STAT_AVERAGE\|(26 + 30) / 2\|28.0` | statistics_generator.py |
| `STAT_COUNT` | 1 | `STAT_COUNT\|5` | statistics_generator.py |
| `STAT_DEVIATION` | 3 | `STAT_DEVIATION\|24\|29\|-5` | statistics_generator.py |
| `STAT_DIVIDE` | 2 | `STAT_DIVIDE\|155 / 5\|31` | statistics_generator.py |
| `STAT_FREQUENCY` | 2 | `STAT_FREQUENCY\|40\|3` | statistics_generator.py |
| `STAT_MAD` | 3 | `STAT_MAD\|48\|6\|8` | statistics_generator.py |
| `STAT_MAX` | 1 | `STAT_MAX\|89` | statistics_generator.py |
| `STAT_MEAN` | 2 | `STAT_MEAN\|174 / 6\|29` | statistics_generator.py |
| `STAT_MIDDLE` | 2 | `STAT_MIDDLE\|position 4\|49` | statistics_generator.py |
| `STAT_MIN` | 1 | `STAT_MIN\|30` | statistics_generator.py |
| `STAT_MODE` | 2 | `STAT_MODE\|40 and 84\|3` | statistics_generator.py |
| `STAT_ORDER` | 1 | `STAT_ORDER\|24, 35, 42, 49, 51, 80, 98` | statistics_generator.py |
| `STAT_RANGE` | 2 | `STAT_RANGE\|89 - 30\|59` | statistics_generator.py |
| `STAT_SETUP` | 1 | `STAT_SETUP\|56, 25, 12, 49, 13` | statistics_generator.py |
| `STAT_SUM` | 2 | `STAT_SUM\|56 + 25 + 12 + 49 + 13\|155` | statistics_generator.py |
| `STD` | 1 | `STD\|12` | layer_norm_generator.py |
| `STEADY_EQUATION` | 2 | `STEADY_EQUATION\|pi0*pi01=pi1*pi10\|pi0+pi1=1` | markov_chain_generator.py |
| `STEPPING_STONE` | 2 | `STEPPING_STONE\|enter x21\|+x21 -x22 +x12 -x11` | transportation_generator.py |
| `STEREO_SETUP` | 3, 4 | `STEREO_SETUP\|plane_to_sphere\|u=2\|v=2` | stereographic_generator.py |
| `STOICH_RATIO` | 2 | `STOICH_RATIO\|CO->CO2\|2/2=1` | gas_stoichiometry_generator.py, stoichiometry_generator.py |
| `STOICH_SETUP` | 2, 3 | `STOICH_SETUP\|limiting_reagent\|2 CO + O2 -> 2 CO2\|given=CO=12 mol, O2=8 mol` | stoichiometry_generator.py |
| `STRUCTURE_CONSTANT` | 3 | `STRUCTURE_CONSTANT\|epsilon_zyx\|-1\|-12iJx` | structure_constant_generator.py |
| `STRUCTURE_SETUP` | 3 | `STRUCTURE_SETUP\|A=-4Jz\|B=-3Jy\|epsilon_zyx=-1` | structure_constant_generator.py |
| `SU3_SETUP` | 2 | `SU3_SETUP\|left=3bar\|right=3bar` | young_tableaux_generator.py |
| `SUBGROUP` | 2 | `SUBGROUP\|H={0, 10, 8, 6, 4, 2}\|size 6` | coset_generator.py |
| `SUBGROUP_ELEM` | 2 | `SUBGROUP_ELEM\|k=1\|5` | coset_generator.py, cyclic_group_generator.py |
| `SUBGROUP_START` | 2 | `SUBGROUP_START\|H=<10>\|identity 0` | coset_generator.py |
| `SUBSET_SIZE` | 2 | `SUBSET_SIZE\|0\|{}` | set_operations_generator.py |
| `SUBST` | 2, 3 | `SUBST\|x\|-4\|4(-4)+y-7` | arc_length_generator.py, chain_rule_generator.py, curve_analysis_generator.py, derivative_limit_def_generator.py, evaluate_expression_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_operations_generator.py, function_table_generator.py, implicit_diff_generator.py, integrating_factor_generator.py, lhopital_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, log_diff_higher_order_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, ode_substitution_generator.py, optimization_generator.py, parametric_calculus_generator.py, partial_fractions_generator.py, piecewise_evaluation_generator.py, polar_parametric_generator.py, power_series_generator.py, recursive_explicit_generator.py, related_rates_generator.py, remainder_factor_theorem_generator.py, second_order_ode_generator.py, separable_ode_generator.py, tangent_line_generator.py, taylor_series_generator.py, trig_equation_generator.py, u_substitution_generator.py, undetermined_coeff_generator.py |
| `SUBSTITUTION` | 2 | `SUBSTITUTION\|y = vx\|dy/dx = v + x dv/dx` | ode_substitution_generator.py |
| `SUB_COL` | 3 | `SUB_COL\|col_1\|5-6-borrow0\|->9 (borrow_out 1)` | multi_digit_subtraction_generator.py |
| `SUM` | 2, 3 | `SUM\|69 + 67 + 70 + 66 + 68\|340` | bayesian_update_generator.py, method_of_moments_generator.py, mle_generator.py, regression_generator.py |
| `SUPPORT` | 2 | `SUPPORT\|0<=x<=18\|0<=y<=324` | rv_transform_generator.py |
| `SUPPORT_TERM` | 2 | `SUPPORT_TERM\|1\|(15,0)` | svm_margin_generator.py |
| `SVM_SETUP` | 3 | `SVM_SETUP\|x1=(-15,0),y1=-1,alpha1=1\|x2=(0,8),y2=-1,alpha2=1\|b=-5,x=(-5,4)` | svm_margin_generator.py |
| `SWAP_VARS` | 1 | `SWAP_VARS\|x = -2y + 4` | inverse_function_generator.py |
| `SYMMETRIC_CHECK` | 3 | `SYMMETRIC_CHECK\|(1, 3)\|reverse (3, 1)\|present` | relation_check_generator.py |
| `SYMMETRY` | 2 | `SYMMETRY\|odd function\|a0=0, a_n=0` | fourier_series_generator.py |
| `SYNDIV_SETUP` | 2 | `SYNDIV_SETUP\|3x^3 + 17x^2 + 6x - 21\|r = -5` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYNDROME_CALC` | 2 | `SYNDROME_CALC\|s1=b1 xor b3 xor b5 xor b7\|0 xor 0 xor 1 xor 0=1` | hamming_code_generator.py |
| `SYNDROME_VALUE` | 2 | `SYNDROME_VALUE\|s1=1, s2=1, s4=1\|position=7` | hamming_code_generator.py |
| `SYN_DROP` | 1 | `SYN_DROP\|3` | horner_evaluation_generator.py, polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYN_ROW` | 1 | `SYN_ROW\|3, 2, -4, -1` | polynomial_zeros_generator.py, synthetic_division_generator.py |
| `SYS_ADD` | 1 | `SYS_ADD\|Add equations: 2y = 20` | systems_elimination_generator.py |
| `SYS_EQ_NEW` | 1 | `SYS_EQ_NEW\|New equation with y only` | systems_substitution_generator.py |
| `SYS_ISOLATE` | 2 | `SYS_ISOLATE\|Isolate x in Eq 1\|x = -3y - 17` | systems_substitution_generator.py |
| `SYS_MULT` | 1 | `SYS_MULT\|Eq1 * 3, Eq2 * 2` | systems_elimination_generator.py |
| `SYS_REWRITE` | 2 | `SYS_REWRITE\|12x + 12y = 180\|-12x - 10y = -160` | systems_elimination_generator.py |
| `SYS_SETUP` | 2 | `SYS_SETUP\|x = y - 4\|x + 4y = -34` | systems_elimination_generator.py, systems_substitution_generator.py |
| `SYS_SUBST` | 1 | `SYS_SUBST\|Substitute (y - 4) for x in Eq 2` | systems_substitution_generator.py |
| `SYS_SUBST_BACK` | 1 | `SYS_SUBST_BACK\|Substitute y=-6 into Eq 1` | systems_elimination_generator.py, systems_substitution_generator.py |
| `TABLEAU` | 2, 3 | `TABLEAU\|initial\|s1: x + s1 = 11\|s2: y + s2 = 11` | simplex_generator.py |
| `TABLEAU_RULE` | 3 | `TABLEAU_RULE\|3bar x 3bar\|two antiboxes split into symmetric plus antisymmetric\|6bar + 3` | young_tableaux_generator.py |
| `TABLE_ENTRY` | 2 | `TABLE_ENTRY\|h(0)\|3` | euler_method_generator.py, function_table_generator.py, taylor_series_generator.py |
| `TABLE_LOOKUP` | 2 | `TABLE_LOOKUP\|f(-4)\|17` | de_moivre_generator.py, dot_product_generator.py, euler_formula_generator.py, function_evaluation_generator.py, lie_exponential_generator.py, normal_table_generator.py, pascal_triangle_generator.py, polar_parametric_generator.py, right_triangle_trig_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, unit_circle_generator.py |
| `TANGENT_PLANE` | 2 | `TANGENT_PLANE\|z = z0 + fx(x-a) + fy(y-b)\|z = -5 + 3*(x - 2) - 5*(y - 1)` | gradient_generator.py |
| `TARGET_STATE` | 2 | `TARGET_STATE\|J=1\|M=0` | clebsch_gordan_generator.py |
| `TAYLOR_FORMULA` | 1 | `TAYLOR_FORMULA\|P_n(x) = Σ f^(k)(a)/k!·(x - a)^k` | taylor_series_generator.py |
| `TAYLOR_SETUP` | 2 | `TAYLOR_SETUP\|f(x) = e^x, center a = 0\|Maclaurin polynomial of degree 3` | taylor_series_generator.py |
| `TEMP_SCALE` | 2 | `TEMP_SCALE\|z1/T\|ln(7)` | softmax_gradient_generator.py |
| `TENSOR_ENTRY` | 2 | `TENSOR_ENTRY\|S_11\|-3` | einstein_summation_generator.py, index_raising_generator.py |
| `TENSOR_RULE` | 1 | `TENSOR_RULE\|diag(a,b) tensor diag(c,d)=diag(ac,ad,bc,bd)` | tensor_product_generator.py |
| `TENSOR_SETUP` | 3 | `TENSOR_SETUP\|A=diag(-2,-3)\|B=diag(2,2)\|u=[-4,0], v=[-3,1]` | tensor_product_generator.py |
| `TENSOR_STATE` | 2 | `TENSOR_STATE\|u tensor v\|[12,-4,0,0]` | tensor_product_generator.py |
| `TERM` | 2 | `TERM\|i=0: 1·(2/5)^0·(3/5)^3\|0.216` | binomial_probability_generator.py |
| `TERMS` | 1 | `TERMS\|x[0..3]=[40,160,640,2560]` | z_transform_generator.py |
| `TEST_CHOOSE` | 2 | `TEST_CHOOSE\|geometric series\|common ratio r = -2/3` | power_series_generator.py, series_convergence_generator.py |
| `TEST_STAT_FORMULA` | 1 | `TEST_STAT_FORMULA\|t = (x̄ - μ0)/(s/√n)` | hypothesis_test_generator.py |
| `TF_SETUP` | 3 | `TF_SETUP\|ode\|y''+9y'+8y=3x'+30x\|zero initial conditions` | transfer_function_generator.py |
| `THEOREM` | 1, 2 | `THEOREM\|factor theorem\|x + 1 is a factor iff P(-1) = 0` | angle_defect_generator.py, circle_angle_generator.py, gauss_bonnet_generator.py, geometric_mean_generator.py, logistic_growth_generator.py, mean_value_theorem_generator.py, parametric_calculus_generator.py, polar_parametric_generator.py, rational_root_generator.py, remainder_factor_theorem_generator.py, series_convergence_generator.py, special_right_triangle_generator.py, spherical_excess_generator.py, taylor_series_generator.py, triangle_solve_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py |
| `THEOREM_REWRITE` | 2 | `THEOREM_REWRITE\|outward flux\|triple integral of div F` | vector_theorem_generator.py |
| `THEOREM_SETUP` | 3 | `THEOREM_SETUP\|divergence theorem\|F=<0, -4*y, 5*z>\|box 4 by 9 by 10` | vector_theorem_generator.py |
| `THETA` | 2 | `THETA\|min(15,11)\|11` | transportation_generator.py |
| `THROUGHPUT` | 2 | `THROUGHPUT\|tokens_per_second\|100000000/39` | scaling_law_generator.py |
| `TIME_COMPONENT` | 2 | `TIME_COMPONENT\|k=1\|-i` | braket_generator.py |
| `TIME_DERIV` | 2 | `TIME_DERIV\|d/dt(m*xdot)\|m*xddot` | lagrangian_generator.py |
| `TIME_EVOLVE` | 2 | `TIME_EVOLVE\|U psi\|[-i,1-2i,2i]` | braket_generator.py |
| `TOPO_AVAILABLE` | 1 | `TOPO_AVAILABLE\|A` | graph_traversal_generator.py |
| `TOPO_READY` | 1 | `TOPO_READY\|B` | graph_traversal_generator.py |
| `TOPO_SELECT` | 2 | `TOPO_SELECT\|A\|A` | graph_traversal_generator.py |
| `TOTIENT_RESULT` | 2 | `TOTIENT_RESULT\|phi(19)\|18` | totient_generator.py |
| `TRACE` | 2 | `TRACE\|-8 + 7\|-1` | ode_system_generator.py |
| `TRACE_ADD` | 4 | `TRACE_ADD\|gamma0gamma1\|(1,1)\|0 + 0\|0` | gamma_matrix_generator.py |
| `TRACE_ENTRY` | 2 | `TRACE_ENTRY\|(1,1)\|0` | einstein_summation_generator.py, pauli_algebra_generator.py |
| `TRACE_EXPECT` | 1, 3 | `TRACE_EXPECT\|Tr(rho A)=p0*a+p1*b` | density_matrix_generator.py, gamma_matrix_generator.py |
| `TRACE_SUM` | 2 | `TRACE_SUM\|0 + 0 + 0\|0` | pauli_algebra_generator.py |
| `TRANSFER` | 1 | `TRANSFER\|H(s)=(3s+30)/(s^2+9s+8)` | transfer_function_generator.py |
| `TRANSFORM_APPLY` | 2 | `TRANSFORM_APPLY\|((-6), -(-2))\|(-6, 2)` | transformation_generator.py |
| `TRANSFORM_RULE` | 1 | `TRANSFORM_RULE\|(x, y) → (y, -x)` | transformation_generator.py |
| `TRANSFORM_SETUP` | 2, 3 | `TRANSFORM_SETUP\|P(-2, -6)\|rotation 270° counterclockwise about the origin, then translation by (-5, -4)` | rv_transform_generator.py, transformation_generator.py |
| `TRANSIENT_FORMULA` | 1 | `TRANSIENT_FORMULA\|tau=R*C` | transient_circuit_generator.py |
| `TRANSIENT_SETUP` | 3 | `TRANSIENT_SETUP\|rc_charging\|R=12, C=4\|Vs=3, t=192` | transient_circuit_generator.py |
| `TRANSITIVE_CHECK` | 3 | `TRANSITIVE_CHECK\|(1, 3) and (3, 1)\|need (1, 1)\|missing` | relation_check_generator.py |
| `TRANSPORT_SETUP` | 3 | `TRANSPORT_SETUP\|supply=(17,15)\|demand=(11,21)\|costs=(5,6;1,7)` | transportation_generator.py |
| `TRIG_RATIO` | 2 | `TRIG_RATIO\|sin\|opposite/hypotenuse` | right_triangle_trig_generator.py |
| `TRIG_SETUP` | 2 | `TRIG_SETUP\|right triangle: leg opposite A = 6, leg adjacent to A = 8, hypotenuse = 10\|sin A` | right_triangle_trig_generator.py, trig_identity_eval_generator.py, trig_six_functions_generator.py, unit_circle_generator.py |
| `TRIG_VALUE` | 2, 3 | `TRIG_VALUE\|sin(lat1)=1\|sin(lat2)=0\|cos(dlon)=-1/2` | christoffel_generator.py, great_circle_generator.py, spherical_triangle_generator.py |
| `TRIPLE_EVAL` | 3 | `TRIPLE_EVAL\|z_part * r_part * angle\|6*25/2*18*2*pi\|2700*pi` | triple_integral_generator.py |
| `TRIPLE_SETUP` | 3 | `TRIPLE_SETUP\|integrand 6*z\|cylinder radius 6, height 5\|cylindrical` | triple_integral_generator.py |
| `TRI_ANGLE_SETUP` | 3 | `TRI_ANGLE_SETUP\|3x + 2\|3x + 15\|3x - 17` | angle_relationships_generator.py |
| `TRI_ANGLE_SOLVE` | 2 | `TRI_ANGLE_SOLVE\|9x + 0 = 180\|x = 20` | angle_relationships_generator.py |
| `TRI_ANGLE_SUM` | 1 | `TRI_ANGLE_SUM\|(3x + 2) + (3x + 15) + (3x - 17) = 180` | angle_relationships_generator.py |
| `TRI_AREA_FORMULA` | 1 | `TRI_AREA_FORMULA\|Area = (1/2)·a·b·sin C` | triangle_area_sas_generator.py |
| `TRI_SETUP` | 2 | `TRI_SETUP\|45-45-90 triangle, leg = 3\|hypotenuse` | special_right_triangle_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py |
| `TRUNCATE` | 2 | `TRUNCATE\|rank=1\|discard=5` | low_rank_approx_generator.py |
| `TRUTH_ROW` | 2 | `TRUTH_ROW\|A=0, B=0, C=0\|f=0` | boolean_algebra_generator.py |
| `TRY` | 2 | `TRY\|(1, -45)\|1·(-45)=-45, 1+(-45)=-44` | factor_trinomial_generator.py, log_conversion_generator.py, log_equation_generator.py, radical_equation_generator.py, rational_equation_generator.py, rational_root_generator.py |
| `TWIDDLE` | 1, 3 | `TWIDDLE\|W2=-1` | dft_generator.py |
| `TWOS_SETUP` | 2 | `TWOS_SETUP\|8-bit two's complement\|offset = 2^8 = 256` | base_conversion_generator.py |
| `UC_GUESS` | 2 | `UC_GUESS\|constant forcing\|y_p = A` | undetermined_coeff_generator.py |
| `UC_POINT` | 2 | `UC_POINT\|180°\|(-1, 0)` | unit_circle_generator.py |
| `UNCERTAINTY_SETUP` | 3 | `UNCERTAINTY_SETUP\|particle in a box\|L=1, hbar=1\|n=60` | uncertainty_generator.py |
| `UNIT_ATTACH` | 3 | `UNIT_ATTACH\|3\|hours\|3 hours` | cross_section_generator.py, kinematics_generator.py, physics_formula_generator.py |
| `UNIT_CONVERT` | 2 | `UNIT_CONVERT\|3 minutes\|180 seconds` | physics_formula_generator.py |
| `UNIT_NORMAL` | 2 | `UNIT_NORMAL\|T'(0)/norm T'(0)\|<-1, 0>` | curve_geometry_generator.py |
| `UNIT_RATE_DIV` | 3 | `UNIT_RATE_DIV\|$72.00\|8\|$9.00` | unit_rate_generator.py |
| `UNIT_RATE_PICK` | 2 | `UNIT_RATE_PICK\|3\|75` | unit_rate_generator.py |
| `UNIT_RATE_SETUP` | 3 | `UNIT_RATE_SETUP\|8\|pounds\|$72.00` | unit_rate_generator.py |
| `UNIT_RATE_TABLE` | 2 | `UNIT_RATE_TABLE\|3,5,7\|75,125,175` | unit_rate_generator.py |
| `UNIT_RULE` | 3 | `UNIT_RULE\|hbar=1\|E=1/L\|GeV` | natural_units_generator.py |
| `UNIT_TANGENT` | 2 | `UNIT_TANGENT\|r'(0)/speed\|<0, 1>` | curve_geometry_generator.py |
| `UNLIKE_RADICALS` | 2 | `UNLIKE_RADICALS\|√3 ≠ √11\|unlike radicands — cannot combine` | radical_add_sub_generator.py |
| `UNROLL` | 2 | `UNROLL\|6, 14, 22, 30\|arithmetic, d = 8` | recursive_explicit_generator.py |
| `UPDATE` | 2 | `UPDATE\|W1_11\|-39/7` | backprop_generator.py, kernel_perceptron_generator.py |
| `U_VECTOR` | 2 | `U_VECTOR\|u1 = A*v1/σ1\|[1/√2, 1/√2]` | svd_generator.py |
| `VA` | 1 | `VA\|x = 1` | rational_function_features_generator.py |
| `VALUE_FORMULA` | 1 | `VALUE_FORMULA\|v=(ad-bc)/(a-b-c+d)` | game_theory_generator.py |
| `VARIANCE` | 1, 2 | `VARIANCE\|Delta x^2\|1/12 - 1/(7200pi^2)` | layer_norm_generator.py, uncertainty_generator.py |
| `VAR_FORMULA` | 1 | `VAR_FORMULA\|Var(X) = Σ P(x)·(x - μ)^2` | expected_value_generator.py |
| `VAR_ROW` | 3 | `VAR_ROW\|3 - 3.45 = -0.45\|(-0.45)^2 = 0.2025\|7/20·0.2025 = 0.070875` | expected_value_generator.py |
| `VECTOR_NORM` | 2 | `VECTOR_NORM\|A\|17` | embedding_similarity_generator.py |
| `VECTOR_SETUP` | 2 | `VECTOR_SETUP\|F(x,y) = <-5*x - 2*y, x + 6*y>\|divergence and scalar curl` | div_curl_generator.py |
| `VEC_SETUP` | 2 | `VEC_SETUP\|v = ⟨7, 24⟩\|unit vector` | dot_product_generator.py, vector_ops_generator.py |
| `VERIFY` | 2 | `VERIFY\|1\|ok` | error_spotting_generator.py |
| `VERTEX` | 1 | `VERTEX\|(2, -2)` | ellipse_features_generator.py, hyperbola_features_generator.py, lp_corner_generator.py, parabola_features_generator.py |
| `VERTEX_SOLVE` | 2 | `VERTEX_SOLVE\|x=0\|y=0` | lp_corner_generator.py |
| `VISIT` | 2 | `VISIT\|A\|A` | graph_traversal_generator.py |
| `VOLUME` | 1 | `VOLUME\|385` | volume_rect_prism_generator.py |
| `VOLUME_SETUP` | 2 | `VOLUME_SETUP\|region between y = 3x (outer) and y = 3x^2 (inner) on [0, 1], about the x-axis\|washer method` | solid_revolution_generator.py |
| `VOL_BASE_AREA` | 2 | `VOL_BASE_AREA\|Base Area = (1/2) × 5 × 10\|25.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_CALCULATE` | 2 | `VOL_CALCULATE\|V = 25.0 × 10\|250.0` | round_solids_generator.py, volume_3d_generator.py |
| `VOL_FORMULA` | 1 | `VOL_FORMULA\|V = Base Area × length` | round_solids_generator.py, solid_revolution_generator.py, volume_3d_generator.py |
| `VOL_SETUP` | 2 | `VOL_SETUP\|triangular_prism\|b=5, h_tri=10, length=10` | volume_3d_generator.py |
| `VOP_FORM` | 2 | `VOP_FORM\|u1' = -y2*g/W\|6/1 * e^(2x)` | variation_parameters_generator.py |
| `WALK_ENTRY` | 2 | `WALK_ENTRY\|A^2[3,2]\|1` | graph_counting_generator.py |
| `WALK_GOAL` | 2 | `WALK_GOAL\|length 2\|3 to 2` | graph_counting_generator.py |
| `WALK_TERM` | 3 | `WALK_TERM\|via 1\|A[3,1]*A[1,2]\|1` | graph_counting_generator.py |
| `WAVE_FORMULA` | 1 | `WAVE_FORMULA\|1=N^2*integral_0^L (x/L)^(2k) dx` | wavefunction_generator.py |
| `WAVE_SETUP` | 3 | `WAVE_SETUP\|power_interval\|psi=N*(x/L)^4\|0<=x<=21` | wavefunction_generator.py |
| `WEEKDAY_SCAN` | 2, 3 | `WEEKDAY_SCAN\|index 2\|Wednesday` | calendar_arithmetic_generator.py |
| `WEIGHT_VECTOR` | 2 | `WEIGHT_VECTOR\|w\|(15,-8)` | svm_margin_generator.py |
| `WIDTH_SETUP` | 3 | `WIDTH_SETUP\|lifetime\|hbar=12\|Gamma=11` | branching_ratio_generator.py |
| `WORK_DIFF` | 3 | `WORK_DIFF\|phi(end) - phi(start)\|23 + 5\|28` | line_integral_generator.py |
| `WRONSKIAN` | 2 | `WRONSKIAN\|y1*y2' - y1'*y2\|e^(3x)` | variation_parameters_generator.py |
| `XOR` | 3 | `XOR\|control=1\|target=0\|1` | quantum_gate_generator.py |
| `YOUNG_SETUP` | 3 | `YOUNG_SETUP\|partition=[5,4,1,1,1]\|n=12\|group=S_12` | young_tableaux_generator.py |
| `Z` | 1 | `Z\|63 R84` | abacus_addition_generator.py, absolute_value_equation_generator.py, absolute_value_inequality_generator.py, ac_circuit_generator.py, activation_generator.py, adam_step_generator.py, algorithm_trace_generator.py, angle_defect_generator.py, angle_measure_generator.py, angle_relationships_generator.py, annuity_generator.py, antiderivative_generator.py, arc_length_generator.py, arc_sector_generator.py, area_between_curves_generator.py, arithmetic_coding_generator.py, arithmetic_sequence_generator.py, attention_generator.py, backprop_generator.py, base_arithmetic_generator.py, base_conversion_generator.py, bayesian_update_generator.py, bch_generator.py, binomial_probability_generator.py, bisection_generator.py, bitwise_ops_generator.py, black_scholes_generator.py, blackbody_generator.py, bond_pricing_generator.py, boolean_algebra_generator.py, braket_generator.py, branching_ratio_generator.py, calendar_arithmetic_generator.py, calorimetry_generator.py, casimir_force_generator.py, casimir_generator.py, cauchy_riemann_generator.py, cayley_table_generator.py, centroid_generator.py, chain_rule_generator.py, channel_capacity_generator.py, chi_square_generator.py, christoffel_generator.py, circle_angle_generator.py, circle_equation_generator.py, circle_generator.py, classifier_metrics_generator.py, clebsch_gordan_generator.py, collision_generator.py, commutator_generator.py, completing_square_generator.py, complex_division_generator.py, complex_locus_generator.py, complex_log_generator.py, complex_number_ops_generator.py, complex_quadratic_generator.py, composite_arithmetic_generator.py, compound_inequality_generator.py, compound_probability_generator.py, conditional_probability_generator.py, confidence_interval_generator.py, conic_standard_form_generator.py, conservation_law_generator.py, continued_fraction_generator.py, continuous_distribution_generator.py, contour_integral_generator.py, convolution_generator.py, coset_generator.py, cramers_rule_generator.py, crc_generator.py, cross_section_generator.py, crt_generator.py, curve_analysis_generator.py, curve_geometry_generator.py, cyclic_group_generator.py, de_moivre_generator.py, decimal_add_sub_generator.py, decimal_div_generator.py, decimal_mult_generator.py, definite_integral_generator.py, density_matrix_generator.py, derangement_generator.py, derivative_limit_def_generator.py, derivative_power_rule_generator.py, derivative_product_quotient_generator.py, derivative_transcendental_generator.py, determinant_generator.py, dfa_simulation_generator.py, dft_generator.py, diagonalization_generator.py, diffie_hellman_generator.py, dijkstra_generator.py, dimensional_analysis_generator.py, discriminant_generator.py, distance_formula_generator.py, div_curl_generator.py, divisibility_classification_generator.py, domain_range_generator.py, doppler_generator.py, dot_product_generator.py, double_integral_generator.py, dp_table_generator.py, eigenvalue_generator.py, einstein_summation_generator.py, electrostatics_generator.py, ellipse_features_generator.py, embedding_similarity_generator.py, energy_conservation_generator.py, entropy_change_generator.py, entropy_generator.py, equation_from_two_points_generator.py, error_spotting_generator.py, euler_characteristic_generator.py, euler_circuit_generator.py, euler_formula_generator.py, euler_method_generator.py, evaluate_expression_generator.py, exact_ode_generator.py, expected_value_generator.py, exponent_generator.py, exponent_mixed_rules_generator.py, exponential_equation_generator.py, exponential_model_generator.py, extended_euclid_generator.py, factor_gcf_generator.py, factor_grouping_generator.py, factor_special_forms_generator.py, factor_trinomial_generator.py, factors_generator.py, feature_map_generator.py, fermi_estimation_generator.py, fill_in_step_generator.py, finance_generator.py, finite_difference_generator.py, finite_field_generator.py, first_law_generator.py, five_number_summary_generator.py, fixed_point_generator.py, flops_memory_generator.py, four_vector_generator.py, fourier_series_generator.py, fractal_iteration_generator.py, fraction_comparison_generator.py, fraction_decimal_percent_converter.py, fraction_op_generator.py, frequency_table_generator.py, function_composition_generator.py, function_evaluation_generator.py, function_inner_product_generator.py, function_operations_generator.py, function_table_generator.py, fundamental_form_generator.py, game_theory_generator.py, gamma_matrix_generator.py, gas_law_generator.py, gas_stoichiometry_generator.py, gauss_bonnet_generator.py, gauss_law_generator.py, gaussian_curvature_generator.py, gcf_generator.py, generating_function_generator.py, geometric_distribution_generator.py, geometric_mean_generator.py, geometric_probability_generator.py, geometric_sequence_generator.py, geometry_area_perimeter_generator.py, gradient_descent_generator.py, gradient_generator.py, gradient_step_generator.py, gram_schmidt_generator.py, graph_counting_generator.py, graph_interpret_generator.py, graph_traversal_generator.py, grassmann_generator.py, great_circle_generator.py, hamiltonian_generator.py, hamming_code_generator.py, hawking_generator.py, heat_engine_generator.py, hermitian_check_generator.py, hessian_classify_generator.py, horner_evaluation_generator.py, huffman_coding_generator.py, hydrogen_atom_generator.py, hyperbola_features_generator.py, hyperbolic_distance_generator.py, hyperbolic_function_generator.py, hypercube_counting_generator.py, hypothesis_test_generator.py, implicit_diff_generator.py, improper_integral_generator.py, inclusion_exclusion_generator.py, index_gymnastics_generator.py, index_raising_generator.py, information_gain_generator.py, integer_operations_generator.py, integrating_factor_generator.py, integration_by_parts_generator.py, interference_generator.py, interpolation_generator.py, invariant_mass_generator.py, inverse_function_generator.py, jacobian_generator.py, joint_distribution_generator.py, kernel_evaluation_generator.py, kernel_perceptron_generator.py, kernel_ridge_generator.py, kernel_validity_generator.py, kinematics_generator.py, kl_divergence_generator.py, kmeans_step_generator.py, knn_generator.py, kraft_inequality_generator.py, ladder_operator_generator.py, lagrange_multiplier_generator.py, lagrangian_generator.py, laplace_ivp_generator.py, laurent_series_generator.py, layer_norm_generator.py, lcm_generator.py, least_squares_generator.py, legendre_construction_generator.py, lhopital_generator.py, lie_exponential_generator.py, limit_evaluation_generator.py, line_integral_generator.py, linear_approx_generator.py, linear_complex_generator.py, linear_fractional_generator.py, linear_simple_generator.py, literal_equation_generator.py, log_conversion_generator.py, log_diff_higher_order_generator.py, log_equation_generator.py, log_properties_generator.py, logistic_growth_generator.py, long_division_generator.py, low_rank_approx_generator.py, lp_corner_generator.py, lr_schedule_generator.py, lu_decomposition_generator.py, magnetism_generator.py, manual_square_root_generator.py, markov_chain_generator.py, matrix_calculus_generator.py, matrix_exponential_generator.py, matrix_group_check_generator.py, matrix_inverse_generator.py, matrix_norm_generator.py, matrix_ops_generator.py, mean_value_theorem_generator.py, method_of_moments_generator.py, metric_arc_length_generator.py, mgf_generator.py, midpoint_generator.py, minkowski_interval_generator.py, mixed_number_operation_generator.py, mle_generator.py, mobius_transform_generator.py, mod_exp_generator.py, modular_arithmetic_generator.py, modular_inverse_generator.py, monomial_mult_div_generator.py, mst_generator.py, multi_digit_addition_generator.py, multi_digit_multiplication_generator.py, multi_digit_subtraction_generator.py, multi_step_unit_conversion_generator.py, multiplying_binomials_generator.py, multiplying_polynomials_generator.py, multivar_chain_rule_generator.py, mutual_information_generator.py, naive_bayes_generator.py, named_distribution_generator.py, natural_units_generator.py, nets_surface_area_generator.py, newton_raphson_generator.py, newtons_laws_generator.py, normal_table_generator.py, npv_irr_generator.py, number_comparison_generator.py, ode_substitution_generator.py, ode_system_generator.py, one_step_equation_generator.py, one_step_inequality_generator.py, optics_generator.py, optimization_generator.py, or_formula_generator.py, orbital_mechanics_generator.py, order_of_operations_generator.py, order_statistics_generator.py, parabola_features_generator.py, parallel_perpendicular_line_generator.py, param_count_generator.py, parametric_calculus_generator.py, partial_derivative_generator.py, partial_fractions_generator.py, partial_trace_generator.py, particle_in_box_generator.py, partition_function_generator.py, pascal_triangle_generator.py, pauli_algebra_generator.py, pca_generator.py, percent_problem_generator.py, percent_word_problem_generator.py, perceptron_generator.py, permutation_combination_generator.py, permutation_group_generator.py, perplexity_generator.py, ph_calculation_generator.py, physics_formula_generator.py, piecewise_evaluation_generator.py, place_value_rounding_generator.py, planck_units_generator.py, point_slope_generator.py, polar_parametric_generator.py, polygon_perimeter_generator.py, polynomial_add_sub_generator.py, polynomial_div_monomial_generator.py, polynomial_long_division_generator.py, polynomial_zeros_generator.py, portfolio_generator.py, positional_encoding_generator.py, positive_definite_generator.py, power_series_generator.py, primality_test_generator.py, prime_factorization_generator.py, probability_addition_rule_generator.py, projectile_motion_generator.py, projector_generator.py, proportion_word_problem_generator.py, proportional_relationship_generator.py, pythag_hyp_generator.py, pythag_leg_generator.py, quadratic_factoring_generator.py, quadratic_generator.py, quadratic_residue_generator.py, quadratic_square_root_generator.py, quantization_generator.py, quantum_formula_generator.py, quantum_gate_generator.py, quark_composition_generator.py, quaternion_generator.py, radical_add_sub_generator.py, radical_equation_generator.py, radical_multiply_generator.py, radical_rationalize_generator.py, radical_variable_simplify_generator.py, rate_conversion_generator.py, ratio_table_generator.py, rational_equation_generator.py, rational_exponent_generator.py, rational_expr_add_sub_generator.py, rational_expr_mult_div_generator.py, rational_expr_simplify_generator.py, rational_function_features_generator.py, rational_root_generator.py, recurrence_generator.py, recursive_explicit_generator.py, regression_generator.py, regular_polygon_area_generator.py, related_rates_generator.py, relation_check_generator.py, relativistic_energy_generator.py, remainder_factor_theorem_generator.py, repeating_decimal_generator.py, residue_generator.py, riemann_sum_generator.py, riemann_tensor_generator.py, right_triangle_trig_generator.py, rotational_dynamics_generator.py, round_solids_generator.py, routh_hurwitz_generator.py, row_reduction_generator.py, rsa_generator.py, runge_kutta_generator.py, running_coupling_generator.py, rv_transform_generator.py, scaling_generator.py, scaling_law_generator.py, schwarzschild_generator.py, second_order_ode_generator.py, segment_partition_generator.py, separable_ode_generator.py, series_convergence_generator.py, series_solution_generator.py, set_operations_generator.py, shm_generator.py, sigma_notation_generator.py, signal_arithmetic_generator.py, similar_triangles_generator.py, simple_probability_generator.py, simple_stats_generator.py, simplex_generator.py, simplify_expression_generator.py, sinusoid_features_generator.py, slope_intercept_form_generator.py, slope_two_points_generator.py, softmax_gradient_generator.py, solid_revolution_generator.py, solution_chem_generator.py, special_relativity_generator.py, special_right_triangle_generator.py, special_solution_equation_generator.py, spherical_excess_generator.py, spherical_triangle_generator.py, spin_half_generator.py, stability_generator.py, standard_deviation_generator.py, standard_form_conversion_generator.py, standing_wave_generator.py, stars_and_bars_generator.py, statics_generator.py, statistics_generator.py, stereographic_generator.py, stoichiometry_generator.py, structure_constant_generator.py, subspace_basis_generator.py, svd_generator.py, svm_margin_generator.py, synthetic_division_generator.py, systems_elimination_generator.py, systems_substitution_generator.py, tangent_line_generator.py, taxicab_geometry_generator.py, taylor_series_generator.py, temperature_conversion_generator.py, tensor_product_generator.py, tip_bill_split_generator.py, totient_generator.py, transfer_function_generator.py, transformation_generator.py, transient_circuit_generator.py, transportation_generator.py, triangle_area_sas_generator.py, triangle_solve_generator.py, trig_equation_generator.py, trig_identity_eval_generator.py, trig_identity_verify_generator.py, trig_six_functions_generator.py, triple_integral_generator.py, two_step_equation_generator.py, two_step_inequality_generator.py, u_substitution_generator.py, uncertainty_generator.py, undetermined_coeff_generator.py, unit_circle_generator.py, unit_conversion_generator.py, unit_rate_generator.py, variation_parameters_generator.py, vector_ops_generator.py, vector_theorem_generator.py, volume_3d_generator.py, volume_rect_prism_generator.py, von_neumann_entropy_generator.py, wavefunction_generator.py, young_tableaux_generator.py, z_score_generator.py, z_transform_generator.py |
| `ZERO` | 1 | `ZERO\|s=-10` | transfer_function_generator.py |
| `ZERO_PRODUCT` | 2 | `ZERO_PRODUCT\|(y + 2)(y - 5) = 0\|y + 2 = 0 or y - 5 = 0` | area_between_curves_generator.py, curve_analysis_generator.py, domain_range_generator.py, log_equation_generator.py, optimization_generator.py, polynomial_zeros_generator.py, quadratic_factoring_generator.py, radical_equation_generator.py, trig_equation_generator.py |
| `ZSCORE` | 2 | `ZSCORE\|(7 - 40)/25\|-1.32` | normal_table_generator.py, z_score_generator.py |
| `ZSCORE_FORMULA` | 1 | `ZSCORE_FORMULA\|z = (x - μ)/σ` | z_score_generator.py |
| `ZT_PAIR` | 1 | `ZT_PAIR\|Z{r^n u[n]}=1/(1-r z^-1)` | z_transform_generator.py |
| `ZT_SETUP` | 2, 3 | `ZT_SETUP\|geometric\|x[n]=40*4^n u[n]` | z_transform_generator.py |
