"""Central grade/difficulty metadata for every registered generator class.

Each class in ``ALL_GENERATORS`` (dolphin_math_datagen.py) must have an entry
here — the pipeline stamps ``grade_level`` and ``difficulty`` onto every
generated example after ``generate()`` returns. A generator may instead emit
either key itself (e.g. computed per-instance from its operands); generator-
provided values always win over the table.

grade_level: "elementary" (grades 3-5), "middle" (6-8), "high" (high school),
             "college" (undergraduate), "graduate".
difficulty:  coarse 1-5 tier, read *relative to the grade band* — a
             "college · d2" item is routine for that level, not
             middle-school hard. Within a band:
             1 = single-read/lookup, 2 = standard algorithm,
             3 = multi-stage, 4 = multi-step / single-topic advanced,
             5 = the band's hardest skills.
"""

ELEMENTARY = "elementary"
MIDDLE = "middle"
HIGH = "high"
COLLEGE = "college"
GRADUATE = "graduate"

GRADE_LEVELS = (ELEMENTARY, MIDDLE, HIGH, COLLEGE, GRADUATE)

CURRICULUM = {
    # ===== ELEMENTARY (Grades 3-5) =====
    "LongDivisionGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "MultiDigitAdditionGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "MultiDigitSubtractionGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "MultiDigitMultiplicationGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "AbacusAdditionGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "DecimalAddSubGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "DecimalMultGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "DecimalDivGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "FractionOpGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "FractionComparisonGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "MixedNumberOperationsRandom": {"grade_level": ELEMENTARY, "difficulty": 3},
    "MixedNumberOperationGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "FractionDecimalPercentConverter": {"grade_level": ELEMENTARY, "difficulty": 3},
    "FactorsGenerator": {"grade_level": ELEMENTARY, "difficulty": 1},
    "PrimeFactorizationGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "GCFGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "LCMGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "OrderOfOperationsGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "PlaceValueRoundingGenerator": {"grade_level": ELEMENTARY, "difficulty": 1},
    "NumberComparisonGenerator": {"grade_level": ELEMENTARY, "difficulty": 1},
    "DivisibilityClassificationGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "GeometryAreaPerimeterGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "PolygonPerimeterGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "VolumeRectPrismGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "UnitConversionGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "MultiStepUnitConversionGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "RateConversionGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "TemperatureConversionGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "DimensionalAnalysisGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "PercentWordProblemGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "RepeatingDecimalGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "ProportionWordProblemGenerator": {"grade_level": ELEMENTARY, "difficulty": 3},
    "SimpleStatsGenerator": {"grade_level": ELEMENTARY, "difficulty": 2},
    "SimpleProbabilityGenerator": {"grade_level": ELEMENTARY, "difficulty": 1},
    "GraphInterpretGenerator": {"grade_level": ELEMENTARY, "difficulty": 1},

    # ===== MIDDLE SCHOOL (Grades 6-8) =====
    "IntegerOperationsGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "UnitRateGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "RatioTableGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "TipBillSplitGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "LinearFractionalGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "SpecialSolutionEquationGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "ExponentMixedRulesGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "RoundSolidsGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "FactorGCFGenerator": {"grade_level": HIGH, "difficulty": 4},
    "FactorTrinomialGenerator": {"grade_level": HIGH, "difficulty": 4},
    "ErrorSpottingGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "FactorSpecialFormsGenerator": {"grade_level": HIGH, "difficulty": 4},
    "FactorGroupingGenerator": {"grade_level": HIGH, "difficulty": 5},
    "QuadraticFactoringGenerator": {"grade_level": HIGH, "difficulty": 5},
    "QuadraticSquareRootGenerator": {"grade_level": HIGH, "difficulty": 4},
    "CompletingSquareGenerator": {"grade_level": HIGH, "difficulty": 5},
    "DiscriminantGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RadicalVariableSimplifyGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RadicalAddSubGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RadicalMultiplyGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RadicalRationalizeGenerator": {"grade_level": HIGH, "difficulty": 5},
    "RationalExponentGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RadicalEquationGenerator": {"grade_level": HIGH, "difficulty": 5},
    "RationalExprSimplifyGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RationalExprMultDivGenerator": {"grade_level": HIGH, "difficulty": 5},
    "RationalExprAddSubGenerator": {"grade_level": HIGH, "difficulty": 5},
    "RationalEquationGenerator": {"grade_level": HIGH, "difficulty": 5},
    "FunctionEvaluationGenerator": {"grade_level": HIGH, "difficulty": 3},
    "FunctionTableGenerator": {"grade_level": HIGH, "difficulty": 3},
    "PiecewiseEvaluationGenerator": {"grade_level": HIGH, "difficulty": 4},
    "FunctionOperationsGenerator": {"grade_level": HIGH, "difficulty": 4},
    "FunctionCompositionGenerator": {"grade_level": HIGH, "difficulty": 4},
    "DomainRangeGenerator": {"grade_level": HIGH, "difficulty": 4},
    "InverseFunctionGenerator": {"grade_level": HIGH, "difficulty": 4},
    "ArithmeticSequenceGenerator": {"grade_level": HIGH, "difficulty": 4},
    "GeometricSequenceGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RecursiveExplicitGenerator": {"grade_level": HIGH, "difficulty": 4},
    "SigmaNotationGenerator": {"grade_level": HIGH, "difficulty": 4},
    "PascalTriangleGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "ComplexNumberOpsGenerator": {"grade_level": HIGH, "difficulty": 4},
    "ComplexDivisionGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ComplexQuadraticGenerator": {"grade_level": HIGH, "difficulty": 5},
    "PolynomialLongDivisionGenerator": {"grade_level": HIGH, "difficulty": 5},
    "SyntheticDivisionGenerator": {"grade_level": HIGH, "difficulty": 4},
    "HornerEvaluationGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RemainderFactorTheoremGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RationalRootGenerator": {"grade_level": HIGH, "difficulty": 5},
    "PolynomialZerosGenerator": {"grade_level": HIGH, "difficulty": 5},
    "RationalFunctionFeaturesGenerator": {"grade_level": HIGH, "difficulty": 4},
    "ExponentialModelGenerator": {"grade_level": HIGH, "difficulty": 4},
    "LogConversionGenerator": {"grade_level": HIGH, "difficulty": 4},
    "LogPropertiesGenerator": {"grade_level": HIGH, "difficulty": 4},
    "ExponentialEquationGenerator": {"grade_level": HIGH, "difficulty": 5},
    "LogEquationGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ParabolaFeaturesGenerator": {"grade_level": HIGH, "difficulty": 5},
    "EllipseFeaturesGenerator": {"grade_level": HIGH, "difficulty": 5},
    "HyperbolaFeaturesGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ConicStandardFormGenerator": {"grade_level": HIGH, "difficulty": 5},
    "NetsSurfaceAreaGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "RegularPolygonAreaGenerator": {"grade_level": HIGH, "difficulty": 4},
    "SimilarTrianglesGenerator": {"grade_level": HIGH, "difficulty": 4},
    "GeometricMeanGenerator": {"grade_level": HIGH, "difficulty": 4},
    "DistanceFormulaGenerator": {"grade_level": HIGH, "difficulty": 3},
    "MidpointGenerator": {"grade_level": HIGH, "difficulty": 3},
    "SegmentPartitionGenerator": {"grade_level": HIGH, "difficulty": 4},
    "TransformationGenerator": {"grade_level": HIGH, "difficulty": 3},
    "ArcSectorGenerator": {"grade_level": HIGH, "difficulty": 4},
    "CircleAngleGenerator": {"grade_level": HIGH, "difficulty": 4},
    "CircleEquationGenerator": {"grade_level": HIGH, "difficulty": 5},
    "TaxicabGeometryGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "EulerCharacteristicGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "HypercubeCountingGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RightTriangleTrigGenerator": {"grade_level": HIGH, "difficulty": 4},
    "SpecialRightTriangleGenerator": {"grade_level": HIGH, "difficulty": 4},
    "AngleMeasureGenerator": {"grade_level": HIGH, "difficulty": 4},
    "UnitCircleGenerator": {"grade_level": HIGH, "difficulty": 4},
    "SinusoidFeaturesGenerator": {"grade_level": HIGH, "difficulty": 4},
    "TrigSixFunctionsGenerator": {"grade_level": HIGH, "difficulty": 4},
    "TrigIdentityEvalGenerator": {"grade_level": HIGH, "difficulty": 5},
    "TrigIdentityVerifyGenerator": {"grade_level": HIGH, "difficulty": 5},
    "TrigEquationGenerator": {"grade_level": HIGH, "difficulty": 5},
    "TriangleSolveGenerator": {"grade_level": HIGH, "difficulty": 5},
    "TriangleAreaSASGenerator": {"grade_level": HIGH, "difficulty": 4},
    "PolarParametricGenerator": {"grade_level": HIGH, "difficulty": 5},
    "VectorOpsGenerator": {"grade_level": HIGH, "difficulty": 4},
    "DotProductGenerator": {"grade_level": HIGH, "difficulty": 4},
    "MatrixOpsGenerator": {"grade_level": HIGH, "difficulty": 4},
    "DeterminantGenerator": {"grade_level": HIGH, "difficulty": 4},
    "MatrixInverseGenerator": {"grade_level": HIGH, "difficulty": 4},
    "CramersRuleGenerator": {"grade_level": HIGH, "difficulty": 5},
    "RowReductionGenerator": {"grade_level": HIGH, "difficulty": 5},
    "LimitEvaluationGenerator": {"grade_level": HIGH, "difficulty": 4},
    "DerivativeLimitDefGenerator": {"grade_level": HIGH, "difficulty": 5},
    "DerivativePowerRuleGenerator": {"grade_level": HIGH, "difficulty": 4},
    "DerivativeProductQuotientGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ChainRuleGenerator": {"grade_level": HIGH, "difficulty": 5},
    "DerivativeTranscendentalGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ImplicitDiffGenerator": {"grade_level": HIGH, "difficulty": 5},
    "LogDiffHigherOrderGenerator": {"grade_level": HIGH, "difficulty": 5},
    "TangentLineGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RelatedRatesGenerator": {"grade_level": HIGH, "difficulty": 5},
    "LinearApproxGenerator": {"grade_level": HIGH, "difficulty": 4},
    "LHopitalGenerator": {"grade_level": HIGH, "difficulty": 5},
    "CurveAnalysisGenerator": {"grade_level": HIGH, "difficulty": 5},
    "OptimizationGenerator": {"grade_level": HIGH, "difficulty": 5},
    "MeanValueTheoremGenerator": {"grade_level": HIGH, "difficulty": 4},
    "AntiderivativeGenerator": {"grade_level": HIGH, "difficulty": 4},
    "USubstitutionGenerator": {"grade_level": HIGH, "difficulty": 5},
    "DefiniteIntegralGenerator": {"grade_level": HIGH, "difficulty": 4},
    "RiemannSumGenerator": {"grade_level": HIGH, "difficulty": 4},
    "AreaBetweenCurvesGenerator": {"grade_level": HIGH, "difficulty": 5},
    "SolidRevolutionGenerator": {"grade_level": HIGH, "difficulty": 5},
    "SeparableODEGenerator": {"grade_level": HIGH, "difficulty": 5},
    "IntegrationByPartsGenerator": {"grade_level": HIGH, "difficulty": 5},
    "PartialFractionsGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ImproperIntegralGenerator": {"grade_level": HIGH, "difficulty": 5},
    "EulerMethodGenerator": {"grade_level": HIGH, "difficulty": 5},
    "LogisticGrowthGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ParametricCalculusGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ArcLengthGenerator": {"grade_level": HIGH, "difficulty": 5},
    "SeriesConvergenceGenerator": {"grade_level": HIGH, "difficulty": 5},
    "PowerSeriesGenerator": {"grade_level": HIGH, "difficulty": 5},
    "TaylorSeriesGenerator": {"grade_level": HIGH, "difficulty": 5},
    "FiveNumberSummaryGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "StandardDeviationGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "CompositeArithmeticGenerator": {"grade_level": ELEMENTARY, "difficulty": 4},
    "ZScoreGenerator": {"grade_level": HIGH, "difficulty": 4},
    "FrequencyTableGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "RegressionGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ExpectedValueGenerator": {"grade_level": HIGH, "difficulty": 4},
    "ConfidenceIntervalGenerator": {"grade_level": HIGH, "difficulty": 5},
    "HypothesisTestGenerator": {"grade_level": HIGH, "difficulty": 5},
    "ChiSquareGenerator": {"grade_level": HIGH, "difficulty": 5},
    "PermutationCombinationGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "BinomialProbabilityGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "ProbabilityAdditionRuleGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "ConditionalProbabilityGenerator": {"grade_level": HIGH, "difficulty": 5},
    "FillInStepGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "NormalTableGenerator": {"grade_level": HIGH, "difficulty": 4},
    "UnitRateFromTableGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "ScalingGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "SimilarFiguresScaleGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "ProportionalRelationshipGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "OneStepEquationGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "TwoStepEquationGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "LinearSimpleGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "LinearComplexGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "SimplifyExpressionGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "EvaluateExpressionGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "OneStepInequalityGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "TwoStepInequalityGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "ExponentEvaluationGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "ExponentRulesGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "ScientificNotationGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "RootsAndRadicalsGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "AngleRelationshipsGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "AnglesWithParallelLinesGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "TriangleAngleSumGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "CircleAreaCircumferenceGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "VolumePrismGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "VolumeCylinderGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "SurfaceAreaPrismGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "SurfaceAreaCylinderGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "PythagHypGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "PythagoreanLegGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "PythagoreanWordProblemGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "MeanGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "MedianGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "ModeGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "RangeGenerator": {"grade_level": MIDDLE, "difficulty": 3},
    "MeanAbsoluteDeviationGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "CompoundProbabilityIndependentGenerator": {"grade_level": MIDDLE, "difficulty": 4},
    "CompoundProbabilityDependentGenerator": {"grade_level": MIDDLE, "difficulty": 4},

    # ===== HIGH SCHOOL =====
    "QuadraticGenerator": {"grade_level": HIGH, "difficulty": 5},
    "PercentProblemGenerator": {"grade_level": HIGH, "difficulty": 4},
    "LiteralEquationGenerator": {"grade_level": HIGH, "difficulty": 4},
    "AbsoluteValueEquationGenerator": {"grade_level": HIGH, "difficulty": 5},
    "AbsoluteValueInequalityGenerator": {"grade_level": HIGH, "difficulty": 5},
    "CompoundInequalityGenerator": {"grade_level": HIGH, "difficulty": 4},
    "SlopeTwoPointsGenerator": {"grade_level": HIGH, "difficulty": 4},
    "SlopeInterceptFormGenerator": {"grade_level": HIGH, "difficulty": 4},
    "EquationFromTwoPointsGenerator": {"grade_level": HIGH, "difficulty": 5},
    "PointSlopeGenerator": {"grade_level": HIGH, "difficulty": 4},
    "StandardFormConversionGenerator": {"grade_level": HIGH, "difficulty": 4},
    "ParallelPerpendicularLineGenerator": {"grade_level": HIGH, "difficulty": 5},
    "SystemsSubstitutionGenerator": {"grade_level": HIGH, "difficulty": 5},
    "SystemsEliminationGenerator": {"grade_level": HIGH, "difficulty": 5},
    "PolynomialAddSubGenerator": {"grade_level": HIGH, "difficulty": 4},
    "MonomialMultDivGenerator": {"grade_level": HIGH, "difficulty": 4},
    "MultiplyingBinomialsGenerator": {"grade_level": HIGH, "difficulty": 5},
    "MultiplyingPolynomialsGenerator": {"grade_level": HIGH, "difficulty": 5},
    "PolynomialDivMonomialGenerator": {"grade_level": HIGH, "difficulty": 5},
}


def clamp_difficulty(value):
    """Clamp a computed per-instance difficulty to the 1-5 scale.

    Generators that compute difficulty from their actual operands
    (digit counts, carries, signs, step count) emit
    ``result["difficulty"] = clamp_difficulty(...)``; the emitted
    value wins over the static table entry (setdefault semantics in
    stamp_metadata).
    """
    return max(1, min(5, value))


def metadata_for(gen_instance):
    """Returns the CURRICULUM entry for a generator instance, or None."""
    return CURRICULUM.get(gen_instance.__class__.__name__)


def stamp_metadata(example, gen_instance):
    """Fills grade_level/difficulty on an example (generator-provided values win).

    Raises ValueError if the generator's class has no CURRICULUM entry and the
    example does not carry the keys itself.
    """
    meta = metadata_for(gen_instance)
    if meta is not None:
        example.setdefault("grade_level", meta["grade_level"])
        example.setdefault("difficulty", meta["difficulty"])
    if "grade_level" not in example or "difficulty" not in example:
        cls = gen_instance.__class__.__name__
        raise ValueError(
            f"No metadata for {cls}: add it to curriculum.CURRICULUM or emit "
            f"grade_level/difficulty from its generate()."
        )
    return example
