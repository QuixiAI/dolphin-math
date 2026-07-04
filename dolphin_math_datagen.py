#!/usr/bin/env python3
# -----------------------------------------------------------
# dolphin_math_datagen.py
# Main script to generate the dataset using individual generator classes.
# -----------------------------------------------------------
import json
import random
import argparse
import sys
import os

from curriculum import GRADE_LEVELS, stamp_metadata
from helpers import DELIM

# Import Generator Classes (from generators subdirectory)
from generators.long_division_generator import LongDivisionGenerator
from generators.decimal_mult_generator import DecimalMultGenerator
from generators.decimal_add_sub_generator import DecimalAddSubGenerator
from generators.decimal_div_generator import DecimalDivGenerator
from generators.fraction_op_generator import FractionOpGenerator
from generators.linear_simple_generator import LinearSimpleGenerator
from generators.quadratic_generator import QuadraticGenerator
from generators.simplify_expression_generator import SimplifyExpressionGenerator
from generators.evaluate_expression_generator import EvaluateExpressionGenerator
from generators.linear_complex_generator import LinearComplexGenerator
from generators.pythag_hyp_generator import PythagHypGenerator
from generators.abacus_addition_generator import AbacusAdditionGenerator
from generators.proportional_relationship_generator import ProportionalRelationshipGenerator
from generators.percent_problem_generator import PercentProblemGenerator
from generators.multi_digit_addition_generator import MultiDigitAdditionGenerator
from generators.multi_digit_subtraction_generator import MultiDigitSubtractionGenerator
from generators.multi_digit_multiplication_generator import MultiDigitMultiplicationGenerator
from generators.mixed_number_operation_generator import MixedNumberOperationGenerator
from generators.mixed_number_operations_random import MixedNumberOperationsRandom
from generators.fraction_comparison_generator import FractionComparisonGenerator
from generators.fraction_decimal_percent_converter import FractionDecimalPercentConverter
from generators.factors_generator import FactorsGenerator
from generators.prime_factorization_generator import PrimeFactorizationGenerator
from generators.gcf_generator import GCFGenerator
from generators.lcm_generator import LCMGenerator
from generators.order_of_operations_generator import OrderOfOperationsGenerator
from generators.geometry_area_perimeter_generator import GeometryAreaPerimeterGenerator
from generators.polygon_perimeter_generator import PolygonPerimeterGenerator
from generators.volume_rect_prism_generator import VolumeRectPrismGenerator
from generators.place_value_rounding_generator import PlaceValueRoundingGenerator
from generators.divisibility_classification_generator import DivisibilityClassificationGenerator
from generators.unit_conversion_generator import UnitConversionGenerator
from generators.multi_step_unit_conversion_generator import MultiStepUnitConversionGenerator
from generators.rate_conversion_generator import RateConversionGenerator
from generators.temperature_conversion_generator import TemperatureConversionGenerator
from generators.dimensional_analysis_generator import DimensionalAnalysisGenerator
from generators.percent_word_problem_generator import PercentWordProblemGenerator
from generators.repeating_decimal_generator import RepeatingDecimalGenerator
from generators.proportion_word_problem_generator import ProportionWordProblemGenerator
from generators.simple_stats_generator import SimpleStatsGenerator
from generators.number_comparison_generator import NumberComparisonGenerator
from generators.simple_probability_generator import SimpleProbabilityGenerator
from generators.graph_interpret_generator import GraphInterpretGenerator

# Middle School (6-8) Generators
from generators.integer_operations_generator import IntegerOperationsGenerator
from generators.unit_rate_generator import UnitRateGenerator, UnitRateFromTableGenerator
from generators.ratio_table_generator import RatioTableGenerator
from generators.tip_bill_split_generator import TipBillSplitGenerator
from generators.linear_fractional_generator import LinearFractionalGenerator
from generators.special_solution_equation_generator import SpecialSolutionEquationGenerator
from generators.exponent_mixed_rules_generator import ExponentMixedRulesGenerator
from generators.round_solids_generator import RoundSolidsGenerator
from generators.factor_gcf_generator import FactorGCFGenerator
from generators.factor_trinomial_generator import FactorTrinomialGenerator
from generators.factor_special_forms_generator import FactorSpecialFormsGenerator
from generators.factor_grouping_generator import FactorGroupingGenerator
from generators.quadratic_factoring_generator import QuadraticFactoringGenerator
from generators.quadratic_square_root_generator import QuadraticSquareRootGenerator
from generators.completing_square_generator import CompletingSquareGenerator
from generators.discriminant_generator import DiscriminantGenerator
from generators.radical_variable_simplify_generator import RadicalVariableSimplifyGenerator
from generators.radical_add_sub_generator import RadicalAddSubGenerator
from generators.radical_multiply_generator import RadicalMultiplyGenerator
from generators.radical_rationalize_generator import RadicalRationalizeGenerator
from generators.rational_exponent_generator import RationalExponentGenerator
from generators.radical_equation_generator import RadicalEquationGenerator
from generators.rational_expr_simplify_generator import RationalExprSimplifyGenerator
from generators.rational_expr_mult_div_generator import RationalExprMultDivGenerator
from generators.rational_expr_add_sub_generator import RationalExprAddSubGenerator
from generators.rational_equation_generator import RationalEquationGenerator
from generators.function_evaluation_generator import FunctionEvaluationGenerator
from generators.function_table_generator import FunctionTableGenerator
from generators.piecewise_evaluation_generator import PiecewiseEvaluationGenerator
from generators.function_operations_generator import FunctionOperationsGenerator
from generators.function_composition_generator import FunctionCompositionGenerator
from generators.domain_range_generator import DomainRangeGenerator
from generators.inverse_function_generator import InverseFunctionGenerator
from generators.arithmetic_sequence_generator import ArithmeticSequenceGenerator
from generators.geometric_sequence_generator import GeometricSequenceGenerator
from generators.recursive_explicit_generator import RecursiveExplicitGenerator
from generators.sigma_notation_generator import SigmaNotationGenerator
from generators.pascal_triangle_generator import PascalTriangleGenerator
from generators.complex_number_ops_generator import ComplexNumberOpsGenerator
from generators.complex_division_generator import ComplexDivisionGenerator
from generators.complex_quadratic_generator import ComplexQuadraticGenerator
from generators.polynomial_long_division_generator import PolynomialLongDivisionGenerator
from generators.synthetic_division_generator import SyntheticDivisionGenerator
from generators.horner_evaluation_generator import HornerEvaluationGenerator
from generators.remainder_factor_theorem_generator import RemainderFactorTheoremGenerator
from generators.rational_root_generator import RationalRootGenerator
from generators.polynomial_zeros_generator import PolynomialZerosGenerator
from generators.rational_function_features_generator import RationalFunctionFeaturesGenerator
from generators.exponential_model_generator import ExponentialModelGenerator
from generators.log_conversion_generator import LogConversionGenerator
from generators.log_properties_generator import LogPropertiesGenerator
from generators.exponential_equation_generator import ExponentialEquationGenerator
from generators.log_equation_generator import LogEquationGenerator
from generators.parabola_features_generator import ParabolaFeaturesGenerator
from generators.ellipse_features_generator import EllipseFeaturesGenerator
from generators.hyperbola_features_generator import HyperbolaFeaturesGenerator
from generators.conic_standard_form_generator import ConicStandardFormGenerator
from generators.nets_surface_area_generator import NetsSurfaceAreaGenerator
from generators.regular_polygon_area_generator import RegularPolygonAreaGenerator
from generators.similar_triangles_generator import SimilarTrianglesGenerator
from generators.geometric_mean_generator import GeometricMeanGenerator
from generators.distance_formula_generator import DistanceFormulaGenerator
from generators.midpoint_generator import MidpointGenerator
from generators.segment_partition_generator import SegmentPartitionGenerator
from generators.transformation_generator import TransformationGenerator
from generators.arc_sector_generator import ArcSectorGenerator
from generators.circle_angle_generator import CircleAngleGenerator
from generators.circle_equation_generator import CircleEquationGenerator
from generators.taxicab_geometry_generator import TaxicabGeometryGenerator
from generators.euler_characteristic_generator import EulerCharacteristicGenerator
from generators.hypercube_counting_generator import HypercubeCountingGenerator
from generators.right_triangle_trig_generator import RightTriangleTrigGenerator
from generators.special_right_triangle_generator import SpecialRightTriangleGenerator
from generators.angle_measure_generator import AngleMeasureGenerator
from generators.unit_circle_generator import UnitCircleGenerator
from generators.sinusoid_features_generator import SinusoidFeaturesGenerator
from generators.trig_six_functions_generator import TrigSixFunctionsGenerator
from generators.trig_identity_eval_generator import TrigIdentityEvalGenerator
from generators.trig_identity_verify_generator import TrigIdentityVerifyGenerator
from generators.trig_equation_generator import TrigEquationGenerator
from generators.triangle_solve_generator import TriangleSolveGenerator
from generators.triangle_area_sas_generator import TriangleAreaSASGenerator
from generators.polar_parametric_generator import PolarParametricGenerator
from generators.vector_ops_generator import VectorOpsGenerator
from generators.dot_product_generator import DotProductGenerator
from generators.matrix_ops_generator import MatrixOpsGenerator
from generators.determinant_generator import DeterminantGenerator
from generators.matrix_inverse_generator import MatrixInverseGenerator
from generators.cramers_rule_generator import CramersRuleGenerator
from generators.row_reduction_generator import RowReductionGenerator
from generators.limit_evaluation_generator import LimitEvaluationGenerator
from generators.derivative_limit_def_generator import DerivativeLimitDefGenerator
from generators.derivative_power_rule_generator import DerivativePowerRuleGenerator
from generators.derivative_product_quotient_generator import DerivativeProductQuotientGenerator
from generators.chain_rule_generator import ChainRuleGenerator
from generators.derivative_transcendental_generator import DerivativeTranscendentalGenerator
from generators.implicit_diff_generator import ImplicitDiffGenerator
from generators.log_diff_higher_order_generator import LogDiffHigherOrderGenerator
from generators.tangent_line_generator import TangentLineGenerator
from generators.related_rates_generator import RelatedRatesGenerator
from generators.linear_approx_generator import LinearApproxGenerator
from generators.lhopital_generator import LHopitalGenerator
from generators.curve_analysis_generator import CurveAnalysisGenerator
from generators.optimization_generator import OptimizationGenerator
from generators.mean_value_theorem_generator import MeanValueTheoremGenerator
from generators.antiderivative_generator import AntiderivativeGenerator
from generators.u_substitution_generator import USubstitutionGenerator
from generators.definite_integral_generator import DefiniteIntegralGenerator
from generators.riemann_sum_generator import RiemannSumGenerator
from generators.area_between_curves_generator import AreaBetweenCurvesGenerator
from generators.solid_revolution_generator import SolidRevolutionGenerator
from generators.separable_ode_generator import SeparableODEGenerator
from generators.integration_by_parts_generator import IntegrationByPartsGenerator
from generators.partial_fractions_generator import PartialFractionsGenerator
from generators.improper_integral_generator import ImproperIntegralGenerator
from generators.euler_method_generator import EulerMethodGenerator
from generators.logistic_growth_generator import LogisticGrowthGenerator
from generators.parametric_calculus_generator import ParametricCalculusGenerator
from generators.arc_length_generator import ArcLengthGenerator
from generators.series_convergence_generator import SeriesConvergenceGenerator
from generators.power_series_generator import PowerSeriesGenerator
from generators.taylor_series_generator import TaylorSeriesGenerator
from generators.five_number_summary_generator import FiveNumberSummaryGenerator
from generators.standard_deviation_generator import StandardDeviationGenerator
from generators.composite_arithmetic_generator import CompositeArithmeticGenerator
from generators.z_score_generator import ZScoreGenerator
from generators.frequency_table_generator import FrequencyTableGenerator
from generators.regression_generator import RegressionGenerator
from generators.expected_value_generator import ExpectedValueGenerator
from generators.confidence_interval_generator import ConfidenceIntervalGenerator
from generators.hypothesis_test_generator import HypothesisTestGenerator
from generators.chi_square_generator import ChiSquareGenerator
from generators.permutation_combination_generator import PermutationCombinationGenerator
from generators.binomial_probability_generator import BinomialProbabilityGenerator
from generators.probability_addition_rule_generator import ProbabilityAdditionRuleGenerator
from generators.conditional_probability_generator import ConditionalProbabilityGenerator
from generators.geometric_probability_generator import GeometricProbabilityGenerator
from generators.geometric_distribution_generator import GeometricDistributionGenerator
from generators.finance_generator import FinanceGenerator
from generators.kinematics_generator import KinematicsGenerator
from generators.physics_formula_generator import PhysicsFormulaGenerator
from generators.base_conversion_generator import BaseConversionGenerator
from generators.base_arithmetic_generator import BaseArithmeticGenerator
from generators.bitwise_ops_generator import BitwiseOpsGenerator
from generators.modular_arithmetic_generator import ModularArithmeticGenerator
from generators.manual_square_root_generator import ManualSquareRootGenerator
from generators.calendar_arithmetic_generator import CalendarArithmeticGenerator
from generators.fermi_estimation_generator import FermiEstimationGenerator
from generators.partial_derivative_generator import PartialDerivativeGenerator
from generators.gradient_generator import GradientGenerator
from generators.multivar_chain_rule_generator import MultivarChainRuleGenerator
from generators.hessian_classify_generator import HessianClassifyGenerator
from generators.lagrange_multiplier_generator import LagrangeMultiplierGenerator
from generators.double_integral_generator import DoubleIntegralGenerator
from generators.triple_integral_generator import TripleIntegralGenerator
from generators.jacobian_generator import JacobianGenerator
from generators.div_curl_generator import DivCurlGenerator
from generators.line_integral_generator import LineIntegralGenerator
from generators.vector_theorem_generator import VectorTheoremGenerator
from generators.curve_geometry_generator import CurveGeometryGenerator
from generators.centroid_generator import CentroidGenerator
from generators.lu_decomposition_generator import LUDecompositionGenerator
from generators.subspace_basis_generator import SubspaceBasisGenerator
from generators.eigenvalue_generator import EigenvalueGenerator
from generators.diagonalization_generator import DiagonalizationGenerator
from generators.gram_schmidt_generator import GramSchmidtGenerator
from generators.least_squares_generator import LeastSquaresGenerator
from generators.matrix_exponential_generator import MatrixExponentialGenerator
from generators.svd_generator import SVDGenerator
from generators.integrating_factor_generator import IntegratingFactorGenerator
from generators.exact_ode_generator import ExactODEGenerator
from generators.ode_substitution_generator import ODESubstitutionGenerator
from generators.second_order_ode_generator import SecondOrderODEGenerator
from generators.undetermined_coeff_generator import UndeterminedCoeffGenerator
from generators.variation_parameters_generator import VariationParametersGenerator
from generators.laplace_ivp_generator import LaplaceIVPGenerator
from generators.ode_system_generator import ODESystemGenerator
from generators.series_solution_generator import SeriesSolutionGenerator
from generators.stability_generator import StabilityGenerator
from generators.set_operations_generator import SetOperationsGenerator
from generators.relation_check_generator import RelationCheckGenerator
from generators.inclusion_exclusion_generator import InclusionExclusionGenerator
from generators.stars_and_bars_generator import StarsAndBarsGenerator
from generators.derangement_generator import DerangementGenerator
from generators.recurrence_generator import RecurrenceGenerator
from generators.generating_function_generator import GeneratingFunctionGenerator
from generators.boolean_algebra_generator import BooleanAlgebraGenerator
from generators.graph_counting_generator import GraphCountingGenerator
from generators.dijkstra_generator import DijkstraGenerator
from generators.mst_generator import MSTGenerator
from generators.graph_traversal_generator import GraphTraversalGenerator
from generators.euler_circuit_generator import EulerCircuitGenerator
from generators.dp_table_generator import DPTableGenerator
from generators.algorithm_trace_generator import AlgorithmTraceGenerator
from generators.dfa_simulation_generator import DFASimulationGenerator
from generators.extended_euclid_generator import ExtendedEuclidGenerator
from generators.modular_inverse_generator import ModularInverseGenerator
from generators.crt_generator import CRTGenerator
from generators.mod_exp_generator import ModExpGenerator
from generators.totient_generator import TotientGenerator
from generators.continued_fraction_generator import ContinuedFractionGenerator
from generators.quadratic_residue_generator import QuadraticResidueGenerator
from generators.rsa_generator import RSAGenerator
from generators.diffie_hellman_generator import DiffieHellmanGenerator
from generators.primality_test_generator import PrimalityTestGenerator
from generators.cayley_table_generator import CayleyTableGenerator
from generators.cyclic_group_generator import CyclicGroupGenerator
from generators.permutation_group_generator import PermutationGroupGenerator
from generators.coset_generator import CosetGenerator
from generators.finite_field_generator import FiniteFieldGenerator
from generators.quaternion_generator import QuaternionGenerator
from generators.euler_formula_generator import EulerFormulaGenerator
from generators.de_moivre_generator import DeMoivreGenerator
from generators.complex_log_generator import ComplexLogGenerator
from generators.complex_locus_generator import ComplexLocusGenerator
from generators.mobius_transform_generator import MobiusTransformGenerator
from generators.fractal_iteration_generator import FractalIterationGenerator
from generators.cauchy_riemann_generator import CauchyRiemannGenerator
from generators.residue_generator import ResidueGenerator
from generators.contour_integral_generator import ContourIntegralGenerator
from generators.laurent_series_generator import LaurentSeriesGenerator
from generators.great_circle_generator import GreatCircleGenerator
from generators.spherical_excess_generator import SphericalExcessGenerator
from generators.spherical_triangle_generator import SphericalTriangleGenerator
from generators.hyperbolic_function_generator import HyperbolicFunctionGenerator
from generators.angle_defect_generator import AngleDefectGenerator
from generators.hyperbolic_distance_generator import HyperbolicDistanceGenerator
from generators.stereographic_generator import StereographicGenerator
from generators.fundamental_form_generator import FundamentalFormGenerator
from generators.christoffel_generator import ChristoffelGenerator
from generators.gaussian_curvature_generator import GaussianCurvatureGenerator
from generators.gauss_bonnet_generator import GaussBonnetGenerator
from generators.metric_arc_length_generator import MetricArcLengthGenerator
from generators.function_inner_product_generator import FunctionInnerProductGenerator
from generators.legendre_construction_generator import LegendreConstructionGenerator
from generators.hermitian_check_generator import HermitianCheckGenerator
from generators.tensor_product_generator import TensorProductGenerator
from generators.quantum_gate_generator import QuantumGateGenerator
from generators.partial_trace_generator import PartialTraceGenerator
from generators.density_matrix_generator import DensityMatrixGenerator
from generators.von_neumann_entropy_generator import VonNeumannEntropyGenerator
from generators.projector_generator import ProjectorGenerator
from generators.uncertainty_generator import UncertaintyGenerator
from generators.matrix_group_check_generator import MatrixGroupCheckGenerator
from generators.lie_exponential_generator import LieExponentialGenerator
from generators.structure_constant_generator import StructureConstantGenerator
from generators.pauli_algebra_generator import PauliAlgebraGenerator
from generators.casimir_generator import CasimirGenerator
from generators.index_gymnastics_generator import IndexGymnasticsGenerator
from generators.bch_generator import BCHGenerator
from generators.young_tableaux_generator import YoungTableauxGenerator
from generators.error_spotting_generator import ErrorSpottingGenerator
from generators.fill_in_step_generator import FillInStepGenerator
from generators.normal_table_generator import NormalTableGenerator
from generators.scaling_generator import ScalingGenerator, SimilarFiguresScaleGenerator
from generators.one_step_equation_generator import OneStepEquationGenerator
from generators.two_step_equation_generator import TwoStepEquationGenerator
from generators.one_step_inequality_generator import OneStepInequalityGenerator
from generators.two_step_inequality_generator import TwoStepInequalityGenerator
from generators.literal_equation_generator import LiteralEquationGenerator
from generators.absolute_value_equation_generator import AbsoluteValueEquationGenerator
from generators.absolute_value_inequality_generator import AbsoluteValueInequalityGenerator
from generators.compound_inequality_generator import CompoundInequalityGenerator
from generators.slope_two_points_generator import SlopeTwoPointsGenerator
from generators.slope_intercept_form_generator import SlopeInterceptFormGenerator
from generators.equation_from_two_points_generator import EquationFromTwoPointsGenerator
from generators.point_slope_generator import PointSlopeGenerator
from generators.standard_form_conversion_generator import StandardFormConversionGenerator
from generators.parallel_perpendicular_line_generator import ParallelPerpendicularLineGenerator
from generators.systems_substitution_generator import SystemsSubstitutionGenerator
from generators.systems_elimination_generator import SystemsEliminationGenerator
from generators.polynomial_add_sub_generator import PolynomialAddSubGenerator
from generators.monomial_mult_div_generator import MonomialMultDivGenerator
from generators.multiplying_binomials_generator import MultiplyingBinomialsGenerator
from generators.multiplying_polynomials_generator import MultiplyingPolynomialsGenerator
from generators.polynomial_div_monomial_generator import PolynomialDivMonomialGenerator
from generators.exponent_generator import (
    ExponentEvaluationGenerator,
    ExponentRulesGenerator,
    ScientificNotationGenerator,
    RootsAndRadicalsGenerator,
)
from generators.angle_relationships_generator import (
    AngleRelationshipsGenerator,
    AnglesWithParallelLinesGenerator,
    TriangleAngleSumGenerator,
)
from generators.circle_generator import CircleAreaCircumferenceGenerator
from generators.volume_3d_generator import (
    VolumePrismGenerator,
    VolumeCylinderGenerator,
    SurfaceAreaPrismGenerator,
    SurfaceAreaCylinderGenerator,
)
from generators.pythag_leg_generator import PythagoreanLegGenerator, PythagoreanWordProblemGenerator
from generators.statistics_generator import (
    MeanGenerator,
    MedianGenerator,
    ModeGenerator,
    RangeGenerator,
    MeanAbsoluteDeviationGenerator,
)
from generators.compound_probability_generator import (
    CompoundProbabilityIndependentGenerator,
    CompoundProbabilityDependentGenerator,
)

# Import Helpers if needed (jid is used in generate methods, step/DELIM are used internally)
# from helpers import jid, step, DELIM # Not strictly needed here anymore

# -----------------------------------------------------------
# Op-code legend: see OPCODES.md (generated; regenerate with
# `python tools/gen_opcode_legend.py`). The vocabulary is descriptive and
# evolves organically — generators may introduce new op-codes freely.
# -----------------------------------------------------------

# ===========================================================================
# ALL_GENERATORS - Master list of all problem generators
# ===========================================================================
# For generators requiring args (like fractions, decimal add/sub),
# we instantiate one for each variant.
#
# The grade-band banners below are the source of truth for grade_level;
# per-class grade/difficulty metadata lives in curriculum.py and every class
# listed here must have a CURRICULUM entry (enforced by tests).
# ===========================================================================

ALL_GENERATORS = [
    # ===== ELEMENTARY (Grades 3-5) =====

    # --- Basic Arithmetic ---
    LongDivisionGenerator(),
    MultiDigitAdditionGenerator(),
    MultiDigitSubtractionGenerator(),
    MultiDigitMultiplicationGenerator(),
    AbacusAdditionGenerator(),

    # --- Decimals ---
    DecimalAddSubGenerator('+'),
    DecimalAddSubGenerator('-'),
    DecimalMultGenerator(),
    DecimalDivGenerator(),

    # --- Fractions ---
    FractionOpGenerator('+'),
    FractionOpGenerator('-'),
    FractionOpGenerator('*'),
    FractionOpGenerator('/'),
    FractionComparisonGenerator(),
    MixedNumberOperationsRandom(),  # Random operation picker
    MixedNumberOperationGenerator('+'),
    MixedNumberOperationGenerator('-'),
    MixedNumberOperationGenerator('*'),
    MixedNumberOperationGenerator('/'),

    # --- Conversions ---
    FractionDecimalPercentConverter(),

    # --- Factors & Multiples ---
    FactorsGenerator(),
    PrimeFactorizationGenerator(),
    GCFGenerator(),
    LCMGenerator(),

    # --- Order of Operations ---
    OrderOfOperationsGenerator(),
    OrderOfOperationsGenerator("decimals"),
    OrderOfOperationsGenerator("mixed_numbers"),

    # --- Number Sense ---
    PlaceValueRoundingGenerator(),
    NumberComparisonGenerator(),
    DivisibilityClassificationGenerator(),

    # --- Geometry (Elementary) ---
    GeometryAreaPerimeterGenerator(),
    PolygonPerimeterGenerator(),
    VolumeRectPrismGenerator(),

    # --- Units & Measurement ---
    UnitConversionGenerator(),
    MultiStepUnitConversionGenerator(),
    RateConversionGenerator(),
    TemperatureConversionGenerator(),
    DimensionalAnalysisGenerator(),
    PercentWordProblemGenerator(),
    PercentWordProblemGenerator(distractor=True),
    RepeatingDecimalGenerator(),
    ProportionWordProblemGenerator(),
    ProportionWordProblemGenerator(distractor=True),

    # --- Data & Statistics (Elementary) ---
    SimpleStatsGenerator(),
    SimpleProbabilityGenerator(),
    GraphInterpretGenerator(),

    # ===== MIDDLE SCHOOL (Grades 6-8) =====

    # --- Integer Operations ---
    IntegerOperationsGenerator(),

    # --- Ratios & Proportions ---
    UnitRateGenerator(),
    UnitRateFromTableGenerator(),
    RatioTableGenerator(),
    TipBillSplitGenerator(),
    ScalingGenerator(),
    SimilarFiguresScaleGenerator(),
    ProportionalRelationshipGenerator(),

    # --- Expressions & Equations ---
    OneStepEquationGenerator(),
    TwoStepEquationGenerator(),
    LinearSimpleGenerator(),
    LinearComplexGenerator(),
    SimplifyExpressionGenerator(),
    EvaluateExpressionGenerator(),

    # --- Inequalities ---
    OneStepInequalityGenerator(),
    TwoStepInequalityGenerator(),
    LinearFractionalGenerator(),
    SpecialSolutionEquationGenerator(),

    # --- Exponents & Roots ---
    ExponentEvaluationGenerator(),
    ExponentRulesGenerator(),
    ExponentRulesGenerator(base_style="decimal"),
    ExponentRulesGenerator(base_style="fraction"),
    ExponentMixedRulesGenerator(),
    ScientificNotationGenerator(),
    RootsAndRadicalsGenerator(),

    # --- Geometry (Middle School) ---
    AngleRelationshipsGenerator(),
    AnglesWithParallelLinesGenerator(),
    TriangleAngleSumGenerator(),
    CircleAreaCircumferenceGenerator(),
    VolumePrismGenerator(),
    VolumeCylinderGenerator(),
    SurfaceAreaPrismGenerator(),
    SurfaceAreaCylinderGenerator(),
    RoundSolidsGenerator(),
    PythagHypGenerator(),
    PythagoreanLegGenerator(),
    PythagoreanWordProblemGenerator(),

    # --- Statistics (Middle School) ---
    MeanGenerator(),
    MedianGenerator(),
    ModeGenerator(),
    RangeGenerator(),
    MeanAbsoluteDeviationGenerator(),

    # --- Probability (Middle School) ---
    CompoundProbabilityIndependentGenerator(),
    CompoundProbabilityDependentGenerator(),
    GeometricProbabilityGenerator(),
    FinanceGenerator(),
    KinematicsGenerator(),
    PhysicsFormulaGenerator(),
    BaseConversionGenerator(),
    BaseArithmeticGenerator(),
    BitwiseOpsGenerator(),
    ModularArithmeticGenerator(),
    ManualSquareRootGenerator(),
    CalendarArithmeticGenerator(),

    # ===== HIGH SCHOOL =====

    # --- Algebra ---
    QuadraticGenerator(),
    PercentProblemGenerator(),
    LiteralEquationGenerator(),
    AbsoluteValueEquationGenerator(),
    AbsoluteValueInequalityGenerator(),
    CompoundInequalityGenerator(),
    SlopeTwoPointsGenerator(),
    SlopeInterceptFormGenerator(),
    EquationFromTwoPointsGenerator(),
    PointSlopeGenerator(),
    StandardFormConversionGenerator(),
    ParallelPerpendicularLineGenerator(),
    SystemsSubstitutionGenerator(),
    SystemsEliminationGenerator(),
    PolynomialAddSubGenerator(),
    MonomialMultDivGenerator(),
    FactorGCFGenerator(),
    FactorTrinomialGenerator(),
    FactorTrinomialGenerator("general"),
    FactorSpecialFormsGenerator(),
    FactorGroupingGenerator(),
    QuadraticFactoringGenerator(),
    QuadraticSquareRootGenerator(),
    CompletingSquareGenerator(),
    DiscriminantGenerator(),
    RadicalVariableSimplifyGenerator(),
    RadicalAddSubGenerator(),
    RadicalMultiplyGenerator(),
    RadicalRationalizeGenerator(),
    RationalExponentGenerator(),
    RadicalEquationGenerator(),
    RationalExprSimplifyGenerator(),
    RationalExprMultDivGenerator(),
    RationalExprAddSubGenerator(),
    RationalEquationGenerator(),
    FunctionEvaluationGenerator(),
    FunctionTableGenerator(),
    PiecewiseEvaluationGenerator(),
    FunctionOperationsGenerator(),
    FunctionCompositionGenerator(),
    DomainRangeGenerator(),
    InverseFunctionGenerator(),
    ArithmeticSequenceGenerator(),
    GeometricSequenceGenerator(),
    RecursiveExplicitGenerator(),
    SigmaNotationGenerator(),
    PascalTriangleGenerator(),
    ComplexNumberOpsGenerator(),
    ComplexDivisionGenerator(),
    ComplexQuadraticGenerator(),
    PolynomialLongDivisionGenerator(),
    SyntheticDivisionGenerator(),
    HornerEvaluationGenerator(),
    RemainderFactorTheoremGenerator(),
    RationalRootGenerator(),
    PolynomialZerosGenerator(),
    RationalFunctionFeaturesGenerator(),
    ExponentialModelGenerator(),
    LogConversionGenerator(),
    LogPropertiesGenerator(),
    ExponentialEquationGenerator(),
    LogEquationGenerator(),
    ParabolaFeaturesGenerator(),
    EllipseFeaturesGenerator(),
    HyperbolaFeaturesGenerator(),
    ConicStandardFormGenerator(),
    NetsSurfaceAreaGenerator(),
    RegularPolygonAreaGenerator(),
    SimilarTrianglesGenerator(),
    GeometricMeanGenerator(),
    DistanceFormulaGenerator(),
    MidpointGenerator(),
    SegmentPartitionGenerator(),
    TransformationGenerator(),
    ArcSectorGenerator(),
    CircleAngleGenerator(),
    CircleEquationGenerator(),
    TaxicabGeometryGenerator(),
    EulerCharacteristicGenerator(),
    HypercubeCountingGenerator(),
    RightTriangleTrigGenerator(),
    SpecialRightTriangleGenerator(),
    AngleMeasureGenerator(),
    UnitCircleGenerator(),
    SinusoidFeaturesGenerator(),
    TrigSixFunctionsGenerator(),
    TrigIdentityEvalGenerator(),
    TrigIdentityVerifyGenerator(),
    TrigEquationGenerator(),
    TriangleSolveGenerator(),
    TriangleAreaSASGenerator(),
    PolarParametricGenerator(),
    VectorOpsGenerator(),
    DotProductGenerator(),
    MatrixOpsGenerator(),
    DeterminantGenerator(),
    MatrixInverseGenerator(),
    CramersRuleGenerator(),
    RowReductionGenerator(),
    LimitEvaluationGenerator(),
    DerivativeLimitDefGenerator(),
    DerivativePowerRuleGenerator(),
    DerivativeProductQuotientGenerator(),
    ChainRuleGenerator(),
    DerivativeTranscendentalGenerator(),
    ImplicitDiffGenerator(),
    LogDiffHigherOrderGenerator(),
    TangentLineGenerator(),
    RelatedRatesGenerator(),
    LinearApproxGenerator(),
    LHopitalGenerator(),
    CurveAnalysisGenerator(),
    OptimizationGenerator(),
    MeanValueTheoremGenerator(),
    AntiderivativeGenerator(),
    USubstitutionGenerator(),
    DefiniteIntegralGenerator(),
    RiemannSumGenerator(),
    AreaBetweenCurvesGenerator(),
    SolidRevolutionGenerator(),
    SeparableODEGenerator(),
    IntegrationByPartsGenerator(),
    PartialFractionsGenerator(),
    ImproperIntegralGenerator(),
    EulerMethodGenerator(),
    LogisticGrowthGenerator(),
    ParametricCalculusGenerator(),
    ArcLengthGenerator(),
    SeriesConvergenceGenerator(),
    PowerSeriesGenerator(),
    TaylorSeriesGenerator(),
    FiveNumberSummaryGenerator(),
    StandardDeviationGenerator(),
    CompositeArithmeticGenerator(),
    ZScoreGenerator(),
    FrequencyTableGenerator(),
    RegressionGenerator(),
    ExpectedValueGenerator(),
    ConfidenceIntervalGenerator(),
    HypothesisTestGenerator(),
    ChiSquareGenerator(),
    PermutationCombinationGenerator(),
    BinomialProbabilityGenerator(),
    ProbabilityAdditionRuleGenerator(),
    ConditionalProbabilityGenerator(),
    GeometricDistributionGenerator(),
    FermiEstimationGenerator(),

    # --- Critic formats (see DESIGN.md "Derived Record Formats") ---
    ErrorSpottingGenerator(),
    FillInStepGenerator(),
    MultiDigitMultiplicationGenerator(estimate=True),
    LongDivisionGenerator(estimate=True),
    NormalTableGenerator(),
    MultiplyingBinomialsGenerator(),
    MultiplyingPolynomialsGenerator(),
    PolynomialDivMonomialGenerator(),
    PartialDerivativeGenerator(),
    GradientGenerator(),
    MultivarChainRuleGenerator(),
    HessianClassifyGenerator(),
    LagrangeMultiplierGenerator(),
    DoubleIntegralGenerator(),
    TripleIntegralGenerator(),
    JacobianGenerator(),
    DivCurlGenerator(),
    LineIntegralGenerator(),
    VectorTheoremGenerator(),
    CurveGeometryGenerator(),
    CentroidGenerator(),
    LUDecompositionGenerator(),
    SubspaceBasisGenerator(),
    EigenvalueGenerator(),
    DiagonalizationGenerator(),
    GramSchmidtGenerator(),
    LeastSquaresGenerator(),
    MatrixExponentialGenerator(),
    SVDGenerator(),
    IntegratingFactorGenerator(),
    ExactODEGenerator(),
    ODESubstitutionGenerator(),
    SecondOrderODEGenerator(),
    UndeterminedCoeffGenerator(),
    VariationParametersGenerator(),
    LaplaceIVPGenerator(),
    ODESystemGenerator(),
    SeriesSolutionGenerator(),
    StabilityGenerator(),
    SetOperationsGenerator(),
    RelationCheckGenerator(),
    InclusionExclusionGenerator(),
    StarsAndBarsGenerator(),
    DerangementGenerator(),
    RecurrenceGenerator(),
    GeneratingFunctionGenerator(),
    BooleanAlgebraGenerator(),
    GraphCountingGenerator(),
    DijkstraGenerator(),
    MSTGenerator(),
    GraphTraversalGenerator(),
    EulerCircuitGenerator(),
    DPTableGenerator(),
    AlgorithmTraceGenerator(),
    DFASimulationGenerator(),
    ExtendedEuclidGenerator(),
    ModularInverseGenerator(),
    CRTGenerator(),
    ModExpGenerator(),
    TotientGenerator(),
    ContinuedFractionGenerator(),
    QuadraticResidueGenerator(),
    RSAGenerator(),
    DiffieHellmanGenerator(),
    PrimalityTestGenerator(),
    CayleyTableGenerator(),
    CyclicGroupGenerator(),
    PermutationGroupGenerator(),
    CosetGenerator(),
    FiniteFieldGenerator(),
    QuaternionGenerator(),
    EulerFormulaGenerator(),
    DeMoivreGenerator(),
    ComplexLogGenerator(),
    ComplexLocusGenerator(),
    MobiusTransformGenerator(),
    FractalIterationGenerator(),
    CauchyRiemannGenerator(),
    ResidueGenerator(),
    ContourIntegralGenerator(),
    LaurentSeriesGenerator(),
    GreatCircleGenerator(),
    SphericalExcessGenerator(),
    SphericalTriangleGenerator(),
    HyperbolicFunctionGenerator(),
    AngleDefectGenerator(),
    HyperbolicDistanceGenerator(),
    StereographicGenerator(),
    FundamentalFormGenerator(),
    ChristoffelGenerator(),
    GaussianCurvatureGenerator(),
    GaussBonnetGenerator(),
    MetricArcLengthGenerator(),
    FunctionInnerProductGenerator(),
    LegendreConstructionGenerator(),
    HermitianCheckGenerator(),
    TensorProductGenerator(),
    QuantumGateGenerator(),
    PartialTraceGenerator(),
    DensityMatrixGenerator(),
    VonNeumannEntropyGenerator(),
    ProjectorGenerator(),
    UncertaintyGenerator(),
    MatrixGroupCheckGenerator(),
    LieExponentialGenerator(),
    StructureConstantGenerator(),
    PauliAlgebraGenerator(),
    CasimirGenerator(),
    IndexGymnasticsGenerator(),
    BCHGenerator(),
    YoungTableauxGenerator(),

    # --- (More High School generators coming soon) ---
]

# Instances excluded from the DEFAULT pool: MixedNumberOperationsRandom is a
# pure wrapper that re-rolls the four MixedNumberOperationGenerator variants,
# so including both would double-count the mixed-number skill. It stays
# registered and can still be requested explicitly via --generators.
DEFAULT_POOL_EXCLUDED = {"MixedNumberOperationsRandom"}


def resolve_pool(generators=None):
    """Returns the working generator pool.

    An explicit selection is honored as-is; the default pool is
    ALL_GENERATORS minus DEFAULT_POOL_EXCLUDED wrapper duplicates.
    """
    if generators is not None:
        pool = list(generators)
        if not pool:
            raise ValueError("No generators selected; cannot build dataset.")
        return pool
    return [g for g in ALL_GENERATORS
            if g.__class__.__name__ not in DEFAULT_POOL_EXCLUDED]


def group_into_skills(gen_pool):
    """Groups generator instances into skills keyed by class name.

    Variant instances of one class (e.g. the four FractionOpGenerator ops)
    form a single skill so each skill gets equal sampling probability by
    default, regardless of how many instances implement it.
    """
    skills = {}
    for gen in gen_pool:
        skills.setdefault(gen.__class__.__name__, []).append(gen)
    return skills


def parse_weights(spec, available):
    """Parses a --weights spec into {skill_name: positive float}.

    Accepts inline "SkillA=2.5,SkillB=0.5" or a path to a JSON file holding
    an object of skill: weight. Unknown skills, non-numeric or non-positive
    weights raise ValueError.
    """
    if isinstance(spec, dict):
        raw = dict(spec)
    elif os.path.isfile(spec) or spec.endswith(".json"):
        try:
            with open(spec, encoding="utf-8") as fp:
                raw = json.load(fp)
        except (OSError, json.JSONDecodeError) as e:
            raise ValueError(f"Could not read weights file {spec!r}: {e}")
        if not isinstance(raw, dict):
            raise ValueError(
                f"Weights file {spec!r} must contain a JSON object of "
                f"{{\"SkillName\": weight}}.")
    else:
        raw = {}
        for part in spec.split(","):
            part = part.strip()
            if not part:
                continue
            name, sep, val = part.partition("=")
            if not sep:
                raise ValueError(
                    f"Bad weight entry {part!r}; expected SkillName=NUMBER")
            raw[name.strip()] = val.strip()

    weights = {}
    for name, val in raw.items():
        try:
            num = float(val)
        except (TypeError, ValueError):
            raise ValueError(f"Weight for {name!r} must be a number, got {val!r}")
        if num <= 0:
            raise ValueError(f"Weight for {name!r} must be positive, got {num}")
        weights[name] = num

    unknown = set(weights) - set(available)
    if unknown:
        raise ValueError(
            f"Unknown skill(s) in --weights: {', '.join(sorted(unknown))}. "
            f"Available: {', '.join(sorted(available))}")
    return weights


def select_generators(generator_arg: str):
    """
    Returns a filtered list of generators based on a comma-separated list of
    class names. If no argument is provided, returns all generators.
    """
    if not generator_arg:
        return ALL_GENERATORS

    requested = {name.strip() for name in generator_arg.split(",") if name.strip()}
    if not requested:
        return ALL_GENERATORS

    available = {gen.__class__.__name__ for gen in ALL_GENERATORS}
    missing = requested - available
    if missing:
        raise ValueError(f"Unknown generator(s): {', '.join(sorted(missing))}. "
                         f"Available: {', '.join(sorted(available))}")

    # All instances of each requested class (variant instances included).
    return [gen for gen in ALL_GENERATORS
            if gen.__class__.__name__ in requested]


def validate_example(example):
    """Structural validation of a generated example; raises ValueError.

    Deliberately vocabulary-agnostic: op-codes are not checked against any
    fixed list (the scratchpad vocabulary evolves organically), only the
    step *shape* and the required record fields are enforced.
    """
    if not isinstance(example, dict):
        raise ValueError(f"example must be a dict, got {type(example).__name__}")
    for key in ("problem_id", "operation", "problem", "steps", "final_answer",
                "grade_level", "difficulty"):
        if key not in example:
            raise ValueError(f"missing required key: {key}")
    steps = example["steps"]
    if not isinstance(steps, list) or not steps:
        raise ValueError("steps must be a non-empty list")
    for i, s in enumerate(steps):
        if not isinstance(s, str) or not s:
            raise ValueError(f"step {i} must be a non-empty string, got {s!r}")
        fields = s.split(DELIM)
        if not fields[0]:
            raise ValueError(f"step {i} has an empty op-code: {s!r}")
        # The final Z step is exempt from the field-count check: it is
        # constrained by exact equality with final_answer below, and critic
        # formats put a pipe-format step inside the answer itself.
        if len(fields) > 5 and i != len(steps) - 1:
            raise ValueError(f"step {i} has more than 4 payload fields: {s!r}")
    expected_final = f"Z{DELIM}{example['final_answer']}"
    if steps[-1] != expected_final:
        raise ValueError(
            f"last step must be {expected_final!r}, got {steps[-1]!r}")
    if example["grade_level"] not in GRADE_LEVELS:
        raise ValueError(f"invalid grade_level: {example['grade_level']!r}")
    difficulty = example["difficulty"]
    if not isinstance(difficulty, int) or isinstance(difficulty, bool) \
            or not 1 <= difficulty <= 5:
        raise ValueError(f"difficulty must be an int in 1..5, got {difficulty!r}")


def write_jsonl(fp, obj):
    """Writes a JSON object to a file handle, one object per line."""
    fp.write(json.dumps(obj, ensure_ascii=False) + "\n")

def _instance_label(gen_instance):
    """Display label for stats: class name plus variant symbol if present."""
    name = gen_instance.__class__.__name__
    if hasattr(gen_instance, "op_symbol"):
        name += f"({gen_instance.op_symbol})"
    return name


def build_dataset(n=10_000, path="math_visible_dataset_refactored.jsonl", seed=None,
                  generators=None, weights=None, allow_duplicates=False):
    """Generates the dataset by calling the generate() method of chosen generators.

    Sampling is balanced per skill (generator class): each skill gets equal
    probability by default, and a skill's variant instances are chosen
    uniformly within it. `weights` (a {skill_name: float} dict or --weights
    spec string) overrides individual skill weights; unlisted skills keep
    weight 1.0.

    Exact repeats of (operation, problem) are skipped unless
    allow_duplicates is set. Returns a summary dict with per-instance stats.
    """
    if seed is not None:
        random.seed(seed)
    gen_pool = resolve_pool(generators)
    skills = group_into_skills(gen_pool)
    skill_names = list(skills)
    if weights:
        weights = parse_weights(weights, skill_names)
        skill_weights = [weights.get(name, 1.0) for name in skill_names]
    else:
        skill_weights = None

    count = 0
    attempts = 0
    seen = set()
    stats = {}
    # Generous budget: dedup can reject heavily when a skill's problem space
    # is small, so allow many more attempts than examples...
    max_attempts = n * 10 + 1000
    # ...but stop early if nothing new has been accepted for a long stretch
    # (likely an exhausted problem space).
    consecutive_rejects = 0
    max_consecutive_rejects = max(2000, n)

    print(f"Attempting to generate {n} examples...")
    # Explicitly set encoding='utf-8' for writing
    with open(path, "w", encoding="utf-8") as fp:
        while count < n and attempts < max_attempts:
            if consecutive_rejects >= max_consecutive_rejects:
                print(f"WARN: no new examples accepted in the last "
                      f"{consecutive_rejects} attempts; the problem space of the "
                      f"selected skills is likely exhausted. Stopping early.")
                break
            attempts += 1
            # Choose a skill (optionally weighted), then an instance within it
            skill = random.choices(skill_names, weights=skill_weights)[0]
            gen_instance = random.choice(skills[skill])
            entry = stats.setdefault(
                _instance_label(gen_instance),
                {"emitted": 0, "duplicates_skipped": 0, "errors": 0})
            try:
                example = gen_instance.generate()
                if not example:
                    raise ValueError("generate() returned an empty example")
                example = stamp_metadata(example, gen_instance)
                validate_example(example)
            except Exception as e:
                entry["errors"] += 1
                consecutive_rejects += 1
                if entry["errors"] <= 5:
                    print(f"ERROR: Generator {gen_instance.__class__.__name__} failed "
                          f"during generation or validation: {e}. Skipping attempt {attempts}.")
                elif entry["errors"] == 6:
                    print(f"ERROR: suppressing further errors from "
                          f"{gen_instance.__class__.__name__} (see stats table).")
                continue

            key = (example["operation"], example["problem"])
            if not allow_duplicates:
                if key in seen:
                    entry["duplicates_skipped"] += 1
                    consecutive_rejects += 1
                    continue
                seen.add(key)

            write_jsonl(fp, example)
            entry["emitted"] += 1
            count += 1
            consecutive_rejects = 0
            if count % 1000 == 0:
                print(f"... successfully generated {count}/{n} examples")

    print(f"✔  Successfully wrote {count} lines → {path} (after {attempts} attempts)")
    if stats:
        width = max(len(name) for name in stats)
        totals = {"emitted": 0, "duplicates_skipped": 0, "errors": 0}
        print(f"{'Generator'.ljust(width)}  {'emitted':>8}  {'dup_skip':>8}  {'errors':>6}")
        for name in sorted(stats):
            s = stats[name]
            for k in totals:
                totals[k] += s[k]
            print(f"{name.ljust(width)}  {s['emitted']:>8}  "
                  f"{s['duplicates_skipped']:>8}  {s['errors']:>6}")
        print(f"{'TOTAL'.ljust(width)}  {totals['emitted']:>8}  "
              f"{totals['duplicates_skipped']:>8}  {totals['errors']:>6}")
    if count < n:
        print(f"WARN: Target of {n} examples not reached ({count}/{n}). Consider increasing max_attempts or checking generator logic.")
    return {"count": count, "attempts": attempts, "stats": stats}

# ---------- Main Execution Block ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Dolphin Math Dataset")
    parser.add_argument(
        "-n", "--num_examples",
        type=int,
        default=10000,
        help="Number of examples to generate."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None, # Default will be generated based on num_examples
        help="Output file path for the generated dataset. Defaults to dolphin_math_<num_examples>.jsonl"
    )
    parser.add_argument(
        "-s", "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility. Omit to use system randomness."
    )
    # Removed --generate_dataset flag, sample is now default if no args given
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Explicitly generate one sample from each generator type (this is also the default if no other args are given)."
    )
    parser.add_argument(
        "--generators",
        type=str,
        default=None,
        help="Comma-separated list of generator class names to include (e.g., 'MultiDigitAdditionGenerator,LongDivisionGenerator')."
    )
    parser.add_argument(
        "--weights",
        type=str,
        default=None,
        help="Skill weight overrides for dataset builds: inline 'SkillA=2.5,SkillB=0.5' "
             "or a path to a JSON file of {\"SkillName\": weight}. Unlisted skills "
             "keep weight 1.0. Ignored with --sample."
    )
    parser.add_argument(
        "--allow-duplicates",
        action="store_true",
        help="Keep exact repeats of (operation, problem) instead of skipping them."
    )

    args = parser.parse_args()
    selected_generators = select_generators(args.generators)

    # Determine the output filename if not provided
    if args.output is None:
        args.output = f"dolphin_math_{args.num_examples}.jsonl"

    # Check if any arguments were passed (other than the script name itself)
    # OR if the --sample flag was explicitly used.
    # If no args, default to sample. If args are present but not --sample, generate dataset.
    if len(sys.argv) > 1 and not args.sample:
        # Generate dataset if arguments like -n, -o, -s are provided.
        # Only an explicit --generators selection overrides the default pool
        # (which excludes wrapper duplicates, see DEFAULT_POOL_EXCLUDED).
        explicit_selection = selected_generators if args.generators else None
        pool = resolve_pool(explicit_selection)
        names = ", ".join(gen.__class__.__name__ for gen in pool)
        print(f"Generating dataset with n={args.num_examples}, output={args.output}, seed={args.seed}...")
        print(f"Using generators: {names}")
        try:
            build_dataset(n=args.num_examples, path=args.output, seed=args.seed,
                          generators=explicit_selection, weights=args.weights,
                          allow_duplicates=args.allow_duplicates)
        except ValueError as e:
            print(f"ERROR: {e}")
            sys.exit(2)
        print("Dataset generation finished.")
    else:
        # Default action (no args) or explicit --sample: print samples
        action_reason = "Default Action" if len(sys.argv) == 1 else "--sample specified"
        print(f"Generating one sample from each generator type ({action_reason}):")
        print("(Use -n, -o, or -s arguments to generate the full dataset file)")
        if args.generators:
            names = ", ".join(gen.__class__.__name__ for gen in selected_generators)
            print(f"Limiting to generators: {names}")
        print("-" * 50)
        if args.seed is not None:
            random.seed(args.seed) # Use specified seed for samples

        for gen_instance in selected_generators:
            generator_name = gen_instance.__class__.__name__
            # Handle generators that take arguments in __init__
            if hasattr(gen_instance, 'op_symbol'):
                 generator_name += f" (op='{gen_instance.op_symbol}')"

            print(f"Generator: {generator_name}")
            try:
                example = stamp_metadata(gen_instance.generate(), gen_instance)
                print(json.dumps(example, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"  ERROR generating sample: {e}")
            print("-" * 50)
        print("Sample generation complete.")
