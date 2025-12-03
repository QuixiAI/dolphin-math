# generators/__init__.py
# This file makes the 'generators' directory a Python package.
# All generator classes are exported for convenient importing.

# Elementary (Grades 3-5) - Basic Arithmetic
from .long_division_generator import LongDivisionGenerator
from .multi_digit_addition_generator import MultiDigitAdditionGenerator
from .multi_digit_subtraction_generator import MultiDigitSubtractionGenerator
from .multi_digit_multiplication_generator import MultiDigitMultiplicationGenerator
from .abacus_addition_generator import AbacusAdditionGenerator

# Elementary - Decimals
from .decimal_add_sub_generator import DecimalAddSubGenerator
from .decimal_mult_generator import DecimalMultGenerator
from .decimal_div_generator import DecimalDivGenerator

# Elementary - Fractions
from .fraction_op_generator import FractionOpGenerator
from .fraction_comparison_generator import FractionComparisonGenerator
from .mixed_number_operation_generator import MixedNumberOperationGenerator
from .mixed_number_operations_random import MixedNumberOperationsRandom

# Elementary - Conversions
from .fraction_decimal_percent_converter import FractionDecimalPercentConverter

# Elementary - Factors & Multiples
from .factors_generator import FactorsGenerator
from .prime_factorization_generator import PrimeFactorizationGenerator
from .gcf_generator import GCFGenerator
from .lcm_generator import LCMGenerator

# Elementary - Order of Operations
from .order_of_operations_generator import OrderOfOperationsGenerator

# Elementary - Number Sense
from .place_value_rounding_generator import PlaceValueRoundingGenerator
from .number_comparison_generator import NumberComparisonGenerator
from .divisibility_classification_generator import DivisibilityClassificationGenerator

# Elementary - Geometry
from .geometry_area_perimeter_generator import GeometryAreaPerimeterGenerator
from .polygon_perimeter_generator import PolygonPerimeterGenerator
from .volume_rect_prism_generator import VolumeRectPrismGenerator

# Elementary - Units & Measurement
from .unit_conversion_generator import UnitConversionGenerator

# Elementary - Data & Statistics
from .simple_stats_generator import SimpleStatsGenerator
from .simple_probability_generator import SimpleProbabilityGenerator
from .graph_interpret_generator import GraphInterpretGenerator

# Middle School (Grades 6-8) - Integer Operations
from .integer_operations_generator import IntegerOperationsGenerator

# Middle School - Ratios & Proportions
from .unit_rate_generator import UnitRateGenerator, UnitRateFromTableGenerator
from .scaling_generator import ScalingGenerator, SimilarFiguresScaleGenerator
from .proportional_relationship_generator import ProportionalRelationshipGenerator

# Middle School - Expressions & Equations
from .one_step_equation_generator import OneStepEquationGenerator
from .two_step_equation_generator import TwoStepEquationGenerator
from .linear_simple_generator import LinearSimpleGenerator
from .linear_complex_generator import LinearComplexGenerator
from .simplify_expression_generator import SimplifyExpressionGenerator
from .evaluate_expression_generator import EvaluateExpressionGenerator

# Middle School - Inequalities
from .one_step_inequality_generator import OneStepInequalityGenerator
from .two_step_inequality_generator import TwoStepInequalityGenerator

# Middle School - Exponents & Roots
from .exponent_generator import (
    ExponentEvaluationGenerator,
    ExponentRulesGenerator,
    ScientificNotationGenerator,
    RootsAndRadicalsGenerator,
)

# Middle School - Geometry
from .angle_relationships_generator import (
    AngleRelationshipsGenerator,
    AnglesWithParallelLinesGenerator,
    TriangleAngleSumGenerator,
)
from .circle_generator import CircleAreaCircumferenceGenerator
from .volume_3d_generator import (
    VolumePrismGenerator,
    VolumeCylinderGenerator,
    SurfaceAreaPrismGenerator,
    SurfaceAreaCylinderGenerator,
)
from .pythag_hyp_generator import PythagHypGenerator
from .pythag_leg_generator import PythagoreanLegGenerator, PythagoreanWordProblemGenerator

# Middle School - Statistics
from .statistics_generator import (
    MeanGenerator,
    MedianGenerator,
    ModeGenerator,
    RangeGenerator,
    MeanAbsoluteDeviationGenerator,
)

# Middle School - Probability
from .compound_probability_generator import (
    CompoundProbabilityIndependentGenerator,
    CompoundProbabilityDependentGenerator,
)

# High School - Algebra
from .quadratic_generator import QuadraticGenerator
from .percent_problem_generator import PercentProblemGenerator

# Export all generators for easy access
__all__ = [
    # Elementary - Basic Arithmetic
    "LongDivisionGenerator",
    "MultiDigitAdditionGenerator",
    "MultiDigitSubtractionGenerator",
    "MultiDigitMultiplicationGenerator",
    "AbacusAdditionGenerator",
    # Elementary - Decimals
    "DecimalAddSubGenerator",
    "DecimalMultGenerator",
    "DecimalDivGenerator",
    # Elementary - Fractions
    "FractionOpGenerator",
    "FractionComparisonGenerator",
    "MixedNumberOperationGenerator",
    "MixedNumberOperationsRandom",
    # Elementary - Conversions
    "FractionDecimalPercentConverter",
    # Elementary - Factors & Multiples
    "FactorsGenerator",
    "PrimeFactorizationGenerator",
    "GCFGenerator",
    "LCMGenerator",
    # Elementary - Order of Operations
    "OrderOfOperationsGenerator",
    # Elementary - Number Sense
    "PlaceValueRoundingGenerator",
    "NumberComparisonGenerator",
    "DivisibilityClassificationGenerator",
    # Elementary - Geometry
    "GeometryAreaPerimeterGenerator",
    "PolygonPerimeterGenerator",
    "VolumeRectPrismGenerator",
    # Elementary - Units & Measurement
    "UnitConversionGenerator",
    # Elementary - Data & Statistics
    "SimpleStatsGenerator",
    "SimpleProbabilityGenerator",
    "GraphInterpretGenerator",
    # Middle School - Integer Operations
    "IntegerOperationsGenerator",
    # Middle School - Ratios & Proportions
    "UnitRateGenerator",
    "UnitRateFromTableGenerator",
    "ScalingGenerator",
    "SimilarFiguresScaleGenerator",
    "ProportionalRelationshipGenerator",
    # Middle School - Expressions & Equations
    "OneStepEquationGenerator",
    "TwoStepEquationGenerator",
    "LinearSimpleGenerator",
    "LinearComplexGenerator",
    "SimplifyExpressionGenerator",
    "EvaluateExpressionGenerator",
    # Middle School - Inequalities
    "OneStepInequalityGenerator",
    "TwoStepInequalityGenerator",
    # Middle School - Exponents & Roots
    "ExponentEvaluationGenerator",
    "ExponentRulesGenerator",
    "ScientificNotationGenerator",
    "RootsAndRadicalsGenerator",
    # Middle School - Geometry
    "AngleRelationshipsGenerator",
    "AnglesWithParallelLinesGenerator",
    "TriangleAngleSumGenerator",
    "CircleAreaCircumferenceGenerator",
    "VolumePrismGenerator",
    "VolumeCylinderGenerator",
    "SurfaceAreaPrismGenerator",
    "SurfaceAreaCylinderGenerator",
    "PythagHypGenerator",
    "PythagoreanLegGenerator",
    "PythagoreanWordProblemGenerator",
    # Middle School - Statistics
    "MeanGenerator",
    "MedianGenerator",
    "ModeGenerator",
    "RangeGenerator",
    "MeanAbsoluteDeviationGenerator",
    # Middle School - Probability
    "CompoundProbabilityIndependentGenerator",
    "CompoundProbabilityDependentGenerator",
    # High School - Algebra
    "QuadraticGenerator",
    "PercentProblemGenerator",
]
