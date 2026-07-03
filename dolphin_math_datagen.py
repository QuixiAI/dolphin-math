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
    RepeatingDecimalGenerator(),
    ProportionWordProblemGenerator(),

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

    available_map = {gen.__class__.__name__: gen for gen in ALL_GENERATORS}
    missing = requested - set(available_map.keys())
    if missing:
        available = ", ".join(sorted(available_map.keys()))
        raise ValueError(f"Unknown generator(s): {', '.join(sorted(missing))}. Available: {available}")

    return [available_map[name] for name in requested]


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
        if len(fields) > 5:
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
