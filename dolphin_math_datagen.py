#!/usr/bin/env python3
# -----------------------------------------------------------
# ultra_math_dataset.py
# Main script to generate the dataset using individual generator classes.
# -----------------------------------------------------------
import json
import random
import argparse
import sys
import os

# Dynamically add the parent directory to sys.path to allow absolute imports
# when running the script directly.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

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
from generators.simple_stats_generator import SimpleStatsGenerator
from generators.number_comparison_generator import NumberComparisonGenerator
from generators.simple_probability_generator import SimpleProbabilityGenerator
from generators.graph_interpret_generator import GraphInterpretGenerator

# Middle School (6-8) Generators
from generators.integer_operations_generator import IntegerOperationsGenerator
from generators.unit_rate_generator import UnitRateGenerator, UnitRateFromTableGenerator
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
# definitive op-code legend (For reference across generator files)
# -----------------------------------------------------------
# Arithmetic  : D(ivide), M(ultiply), S(ubtract), A(dd)
#             : B(ring down: remainder_before, digit_down, new_num_to_divide)
#             : R(emainder)
#             : C(onvert fraction for LCD)
#             : L(CD calculation)
#             : I(nvert fraction: orig_frac_str, inverted_frac_str)
#             : PDEC(Place Decimal in product - old method)
#             : F(raction simplification)
# Dec Add/Sub : DEC_ALIGN(num1_aligned, num2_aligned)
#             : DEC_ADD_COL(col_name, details_str, result_str)
#             : DEC_SUB_COL(col_name, details_str, result_str)
#             : DEC_CARRY_FINAL(carry_digit)
# Dec Mult    : MUL_SETUP(int1_str, int2_str)
#             : MUL_PARTIAL(digit, top_int_str, partial_product_shifted_str)
#             : ADD_PARTIALS(sum_expression_str, result_sum_str)
#             : COUNT_DP(dp1, dp2, total_dp)
#             : PLACE_DP(sum_int_str, total_dp, final_result_str)
# Dec Div     : DEC_SHIFT(orig_expr, shifted_expr, shift_places)
#             : DIV_SETUP(integer_dividend, integer_divisor)
#             : PLACE_DP_Q(quotient_digits_str, dp_position_from_left_in_shifted_dividend)
#             : (Reuses B, D, M, S from Arithmetic)
# Percent     : PERCENT_TO_DEC, SETUP_PERCENT_EQ, REARRANGE_EQ, PERCENT_CALC_PART, DEC_TO_PERCENT
#             : (Uses division steps internally for find_percent/find_whole)
# Algebra     : G(CD - not used?), DISC(riminant calc), ROOT(square root)
#             : Q1/Q2(Quadratic formula roots)
#             : DIST(ribute term: factor, expr_in_parens, result_expr)
#             : REWRITE(expression/equation after step: new_form_string)
#             : COMB_X(Combine X terms: term1, term2, result_term)
#             : COMB_CONST(Combine Constant terms: const1, const2, result_const)
#             : SUBST(itute value: var_name, value, resulting_expr)
#             : MOVE_TERM(term_moved, target_side, resulting_equation_str)
#             : DIV_COEFF(Divide by coefficient: numerator, denominator, result_str)
# Geometry    : E(xponent/Power)
#             : (Reuses ROOT)
# Algebra+    : PROP_SETUP (Proportional relationships)
# Tools       : AB_SET AB_INFO AB_ADD_DGT AB_CARRY AB_CARRY_FINAL
# Final Answer: Z  (Contains the final formatted answer string)
# -----------------------------------------------------------

# ===========================================================================
# ALL_GENERATORS - Master list of all problem generators
# ===========================================================================
# For generators requiring args (like fractions, decimal add/sub),
# we instantiate one for each variant.
#
# Organization:
#   - Elementary (Grades 3-5): 34 generators
#   - Middle School (Grades 6-8): 39 generators
#   - High School: Algebra, Geometry (more coming)
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

    # --- Exponents & Roots ---
    ExponentEvaluationGenerator(),
    ExponentRulesGenerator(),
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
    MultiplyingBinomialsGenerator(),
    MultiplyingPolynomialsGenerator(),
    PolynomialDivMonomialGenerator(),

    # --- (More High School generators coming soon) ---
]

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

    available_map = {gen.__class__.__name__: gen for gen in ALL_GENERATORS}
    missing = requested - set(available_map.keys())
    if missing:
        available = ", ".join(sorted(available_map.keys()))
        raise ValueError(f"Unknown generator(s): {', '.join(sorted(missing))}. Available: {available}")

    return [available_map[name] for name in requested]


def write_jsonl(fp, obj):
    """Writes a JSON object to a file handle, one object per line."""
    fp.write(json.dumps(obj, ensure_ascii=False) + "\n")

def build_dataset(n=10_000, path="math_visible_dataset_refactored.jsonl", seed=None, generators=None):
    """Generates the dataset by calling the generate() method of chosen generators."""
    if seed is not None:
        random.seed(seed)
    gen_pool = generators or ALL_GENERATORS
    if not gen_pool:
        raise ValueError("No generators selected; cannot build dataset.")
    count = 0
    attempts = 0
    # Allow slightly more attempts in case some generators fail validation often
    max_attempts = int(n * 1.2) + 50

    print(f"Attempting to generate {n} examples...")
    # Explicitly set encoding='utf-8' for writing
    with open(path, "w", encoding="utf-8") as fp:
        while count < n and attempts < max_attempts:
            attempts += 1
            try:
                # Choose a generator instance randomly
                gen_instance = random.choice(gen_pool)
                example = gen_instance.generate() # Call the generate method
                if example:
                    # Basic validation before writing
                    assert 'problem_id' in example
                    assert 'operation' in example
                    assert 'problem' in example
                    assert 'steps' in example and isinstance(example['steps'], list) and len(example['steps']) > 0
                    assert 'final_answer' in example
                    assert example['steps'][-1].startswith("Z|") # Check final step format

                    write_jsonl(fp, example)
                    count += 1
                    if count % 1000 == 0 and count > 0:
                        print(f"... successfully generated {count}/{n} examples")
            except Exception as e:
                # Provide more context on which generator failed
                gen_name = gen_instance.__class__.__name__ if 'gen_instance' in locals() else "Unknown"
                print(f"ERROR: Generator {gen_name} failed during generation or validation: {e}. Skipping attempt {attempts}.")
                # Optional: Add more detailed error logging or handling here

    print(f"✔  Successfully wrote {count} lines → {path} (after {attempts} attempts)")
    if count < n:
        print(f"WARN: Target of {n} examples not reached ({count}/{n}). Consider increasing max_attempts or checking generator logic.")

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

    args = parser.parse_args()
    selected_generators = select_generators(args.generators)

    # Determine the output filename if not provided
    if args.output is None:
        args.output = f"dolphin_math_{args.num_examples}.jsonl"

    # Check if any arguments were passed (other than the script name itself)
    # OR if the --sample flag was explicitly used.
    # If no args, default to sample. If args are present but not --sample, generate dataset.
    if len(sys.argv) > 1 and not args.sample:
        # Generate dataset if arguments like -n, -o, -s are provided
        names = ", ".join(gen.__class__.__name__ for gen in selected_generators)
        print(f"Generating dataset with n={args.num_examples}, output={args.output}, seed={args.seed}...")
        print(f"Using generators: {names}")
        build_dataset(n=args.num_examples, path=args.output, seed=args.seed, generators=selected_generators)
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
                example = gen_instance.generate()
                print(json.dumps(example, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"  ERROR generating sample: {e}")
            print("-" * 50)
        print("Sample generation complete.")
