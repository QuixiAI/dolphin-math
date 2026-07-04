# Dolphin Math — Curriculum Backlog

**This file is a pure backlog: it lists only what is NOT yet implemented.**
When a skill ships, **delete its line** — don't check it off. The implemented
inventory is always derivable from `ALL_GENERATORS` + `curriculum.py`
(~90 skills as of July 2026; run `python dolphin_math_datagen.py --sample` to
see them all), and checked-off history is where stale lies accumulate.

**Item format:** `- [ ] Skill — notes · ClassName · grade · d<1-5>`
The annotation is the contract: the class to create, and the `grade_level` +
`difficulty` to enter in `curriculum.CURRICULUM`. **One skill, one home** — no
topic appears twice; grade spread is handled by difficulty variants inside a
generator, never by duplicate entries.

**Definition of done** (details in AGENTS.md): generator + mirrored tests +
`ALL_GENERATORS` registration + `CURRICULUM` entry + regenerate `OPCODES.md` +
eyeball `--sample` output against the pencil-and-paper procedure.

---

## Design Principles

The scratchpad belongs to the model — it will eventually own this vocabulary.
These principles are what make the data worth training on:

1. **Every arithmetic action is explicit.** No hidden mental math; if a human
   would write it in the margin, it's a step.
2. **Human-legible cues.** Alignment, carries/borrows with source and target,
   the current expression after every rewrite.
3. **Show dead ends.** Real scratchpads contain rejected candidates. Factoring,
   rational-root search, and simplification should emit tried-and-rejected
   steps, not just the winning path.
4. **Verify before answering.** Where natural, emit check steps (substitute
   back, inverse operation, magnitude sanity) before `Z|`.
5. **No lookups the problem doesn't provide.** If a human would consult a
   table or calculator (trig values, z-tables, critical values), the problem
   text must supply those values; the scratchpad shows only the arithmetic.
6. **One op-code = one meaning.** New codes are welcome — the vocabulary is
   organic — but reusing an existing code with different field semantics is not.
7. **Hand-friendly numbers.** Choose operands so the procedure is the hard
   part, not digit grinding.
8. **Answers worth grading, spaces worth sampling.** If the answer space is
   tiny (yes/no, timelike/spacelike), make `final_answer` composite —
   "forbidden — violates lepton number" — so RL can't coin-flip it. If the
   *problem* space is tiny (Clebsch-Gordan ½⊗½ is one table, octant triangles
   are few), expect dedup to exhaust it early and weight it as garnish, not
   staple (`FactorsGenerator`'s 133-problem space taught us this).

---

## Cross-Cutting Upgrades

Not new skills — multipliers on everything. (A0-A2 and A9 shipped: see DESIGN.md "Answer Format Conventions" and "Verification & Trial-and-Error Vocabulary", and the A9 oracle rule in AGENTS.md.)


---

## Backlog

### Functions

### Sequences & Series

### Complex Numbers

### Polynomials & Rational Functions

### Exponentials & Logarithms

### Conic Sections

### Geometry & Measurement

### Trigonometry

### Vectors & Matrices

### Limits

### Calculus — Derivatives

### Calculus — Integrals & Differential Equations

### Calculus — Series (BC)

### Statistics

### Probability

### Applied & Cross-Disciplinary

### Critic & Estimation Formats
All four original items shipped (design: DESIGN.md "Derived Record
Formats"). Remaining growth path: extend `ErrorSpottingGenerator` and
`FillInStepGenerator` with more flows (long division, fractions,
factoring), and the estimate variants to more computational generators,
as the library grows.

---

## University & Graduate Backlog

Same filter as everything above: **it's in scope iff it breaks into mechanical,
human-legible scratchpad steps with an exactly checkable final answer.**
Proof-writing, sketching, and open-ended modeling stay out; the computation
that *supports* them is in. Advanced math is secretly full of tabular by-hand
procedures — simplex pivots, Gram-Schmidt, syndrome decoding, Routh arrays,
partition functions — and that's exactly what lives here. Two ground rules
bind extra hard at this level:

- **Principle 5 rules everything.** Transcendental values (ln 2, e^-1.5,
  N(d₁), critical values) are supplied in the problem, avoided by construction
  (dyadic probabilities so log₂ is exact, nice angles), or the answer stays in
  exact symbolic form per A0.
- **A8 first.** These items use the `college` and `graduate` grade levels.

### Multivariable Calculus
- [ ] Gradient, directional derivatives, tangent planes · `GradientGenerator` · college · d2
- [ ] Multivariable chain rule; total differential · `MultivarChainRuleGenerator` · college · d3
- [ ] Critical points via the second-partials (Hessian) test · `HessianClassifyGenerator` · college · d3
- [ ] Lagrange multipliers — one constraint · `LagrangeMultiplierGenerator` · college · d4
- [ ] Double integrals — iterated, order reversal, polar conversion · `DoubleIntegralGenerator` · college · d3
- [ ] Triple integrals — cylindrical and spherical · `TripleIntegralGenerator` · college · d4
- [ ] Jacobians and change of variables · `JacobianGenerator` · college · d3
- [ ] Divergence and curl of vector fields · `DivCurlGenerator` · college · d2
- [ ] Line integrals and work; potential functions for conservative fields · `LineIntegralGenerator` · college · d4
- [ ] Green's / divergence / Stokes' theorems — compute via the easier side · `VectorTheoremGenerator` · college · d5
- [ ] Curve geometry — arc length, curvature, unit tangent/normal · `CurveGeometryGenerator` · college · d3
- [ ] Centroids and moments via integration · `CentroidGenerator` · college · d4

### Linear Algebra (beyond the small-matrix K-12 items)
- [ ] LU decomposition · `LUDecompositionGenerator` · college · d3
- [ ] RREF → rank, null space and column space bases · `SubspaceBasisGenerator` · college · d3
- [ ] Eigenvalues & eigenvectors — characteristic polynomial, 2×2 and 3×3 · `EigenvalueGenerator` · college · d3
- [ ] Diagonalization; matrix powers Aᵏ via PDᵏP⁻¹ · `DiagonalizationGenerator` · college · d4
- [ ] Gram-Schmidt orthogonalization · `GramSchmidtGenerator` · college · d4
- [ ] Projections and least squares via normal equations (the linear-algebra route to `RegressionGenerator`'s formulas) · `LeastSquaresGenerator` · college · d4
- [ ] Matrix exponential e^(At) for diagonalizable 2×2 · `MatrixExponentialGenerator` · graduate · d3
- [ ] SVD of small matrices via AᵀA eigendecomposition · `SVDGenerator` · graduate · d4

### Differential Equations
- [ ] First-order linear — integrating factor · `IntegratingFactorGenerator` · college · d3
- [ ] Exactness test; solve exact equations · `ExactODEGenerator` · college · d3
- [ ] Substitutions — Bernoulli, homogeneous y = vx · `ODESubstitutionGenerator` · college · d4
- [ ] Second-order constant-coefficient — characteristic equation, all three root cases · `SecondOrderODEGenerator` · college · d3
- [ ] Undetermined coefficients · `UndeterminedCoeffGenerator` · college · d4
- [ ] Variation of parameters; Wronskian · `VariationParametersGenerator` · college · d5
- [ ] Laplace-transform IVPs — transform table provided (Principle 5), inverse via partial fractions · `LaplaceIVPGenerator` · college · d4
- [ ] Linear systems x′ = Ax via eigenvalues · `ODESystemGenerator` · college · d5
- [ ] Power-series solutions — derive the coefficient recurrence · `SeriesSolutionGenerator` · graduate · d4
- [ ] Equilibria and stability of autonomous ODEs — sign analysis of f(y) · `StabilityGenerator` · college · d3

### Discrete Math & Combinatorics
- [ ] Set algebra, power sets, Cartesian products · `SetOperationsGenerator` · college · d2
- [ ] Relation property checks on small finite sets — explicit pair-by-pair verification · `RelationCheckGenerator` · college · d2
- [ ] Inclusion-exclusion counting · `InclusionExclusionGenerator` · college · d3
- [ ] Stars and bars; multinomial coefficients · `StarsAndBarsGenerator` · college · d3
- [ ] Derangements · `DerangementGenerator` · college · d3
- [ ] Linear recurrences — characteristic-root method, homogeneous and not · `RecurrenceGenerator` · college · d4
- [ ] Generating functions — coefficient extraction for simple products · `GeneratingFunctionGenerator` · graduate · d4
- [ ] Boolean algebra — truth tables → DNF/CNF, simplification, Karnaugh maps · `BooleanAlgebraGenerator` · college · d3

### Graph Theory & Algorithms
- [ ] Degree sequences, handshake counts; adjacency-matrix powers for walk counts · `GraphCountingGenerator` · college · d3
- [ ] Dijkstra shortest path — full distance-table trace · `DijkstraGenerator` · college · d4
- [ ] Minimum spanning trees — Kruskal and Prim traces · `MSTGenerator` · college · d4
- [ ] BFS/DFS visit orders; topological sort · `GraphTraversalGenerator` · college · d3
- [ ] Euler circuits/paths — degree-parity check plus construction · `EulerCircuitGenerator` · college · d3
- [ ] DP table filling — knapsack, LCS, edit distance, coin change; the table IS the scratchpad · `DPTableGenerator` · college · d4
- [ ] Algorithm state traces — binary search, insertion/merge sort after k steps · `AlgorithmTraceGenerator` · college · d3
- [ ] DFA simulation — state sequence for a given input string · `DFASimulationGenerator` · college · d3

### Number Theory & Cryptography
- [ ] Extended Euclid — Bézout coefficients with the back-substitution table · `ExtendedEuclidGenerator` · college · d3
- [ ] Modular inverses; linear congruences · `ModularInverseGenerator` · college · d3
- [ ] Chinese Remainder Theorem · `CRTGenerator` · college · d4
- [ ] Fast modular exponentiation — square-and-multiply trace · `ModExpGenerator` · college · d3
- [ ] Euler's totient; Fermat/Euler theorem power reductions · `TotientGenerator` · college · d3
- [ ] Continued fractions and convergents · `ContinuedFractionGenerator` · college · d4
- [ ] Quadratic residues — Legendre symbol via Euler's criterion · `QuadraticResidueGenerator` · graduate · d4
- [ ] RSA with small primes — keygen, encrypt, decrypt, end to end · `RSAGenerator` · college · d4
- [ ] Diffie-Hellman small-modulus exchange · `DiffieHellmanGenerator` · college · d3
- [ ] Miller-Rabin primality steps with given witnesses · `PrimalityTestGenerator` · graduate · d4

### Abstract Algebra (computational side only)
- [ ] Cayley tables for ℤₙ, U(n), D₃; element orders · `CayleyTableGenerator` · college · d3
- [ ] Cyclic subgroups and generators · `CyclicGroupGenerator` · college · d3
- [ ] Permutations — cycle notation, composition, order, parity · `PermutationGroupGenerator` · college · d3
- [ ] Coset enumeration in small groups · `CosetGenerator` · graduate · d4
- [ ] Polynomial arithmetic over ℤₚ; GF(2) polynomial division (the algebra behind CRC) · `FiniteFieldGenerator` · graduate · d4
- [ ] Quaternion arithmetic — Hamilton's table (i² = j² = k² = ijk = −1), non-commutativity shown explicitly (ij = k but ji = −k), norms, conjugates, inverses, and rotating a 3D vector via qvq⁻¹ · `QuaternionGenerator` · graduate · d4

### Complex Analysis (computational)
- [ ] Euler's formula — rectangular ↔ polar ↔ exponential form conversions, Euler's identity as the d1 case · `EulerFormulaGenerator` · college · d3
- [ ] Polar form, De Moivre, nth roots of unity · `DeMoivreGenerator` · college · d3
- [ ] nth roots of *arbitrary* complex numbers — modulus root + argument fan (variant of `DeMoivreGenerator`) · college · d4
- [ ] Complex logarithms and complex powers — principal values, multivaluedness as explicit +2πik bookkeeping; the i^i = e^(−π/2) showstopper · `ComplexLogGenerator` · graduate · d4
- [ ] Complex loci — |z−a| = r and |z−a| = |z−b| identified as circle/line by completing the square in ℂ · `ComplexLocusGenerator` · college · d3
- [ ] Möbius transformations — images of points, fixed points via quadratic, cross-ratios · `MobiusTransformGenerator` · graduate · d4
- [ ] Mandelbrot/Julia escape iterations — trace z ← z² + c with rational c, |z| > 2 escape check; pure arithmetic, maximally mind-bending · `FractalIterationGenerator` · college · d3
- [ ] Cauchy-Riemann verification; harmonic conjugates by integration · `CauchyRiemannGenerator` · college · d3
- [ ] Residues at simple and higher-order poles · `ResidueGenerator` · graduate · d4
- [ ] Contour integrals via the residue theorem · `ContourIntegralGenerator` · graduate · d5
- [ ] Taylor/Laurent coefficients of rational functions · `LaurentSeriesGenerator` · graduate · d5

### Spherical & Non-Euclidean Geometry
Angle sums that refuse to be 180° — mind-bending results from ordinary
arithmetic. Nice angles (30°/45°/60°/90°) keep everything exact per Principle 5.
- [ ] Great-circle distance from latitude/longitude — spherical law of cosines / haversine, trig values provided · `GreatCircleGenerator` · college · d3
- [ ] Spherical excess & Girard's theorem — angle sum − 180° gives the triangle's area (octant triangle: 90°+90°+90° = 270°, area = πR²/2) · `SphericalExcessGenerator` · college · d3
- [ ] Spherical triangles — spherical laws of sines and cosines · `SphericalTriangleGenerator` · graduate · d4
- [ ] Hyperbolic functions — sinh/cosh/tanh evaluation in exact e-form; hyperbolic identities as CHECK steps (cosh² − sinh² = 1) · `HyperbolicFunctionGenerator` · college · d3
- [ ] Hyperbolic triangle area via angle defect — π − (A+B+C); the mirror image of Girard · `AngleDefectGenerator` · college · d3
- [ ] Poincaré half-plane/disk distances — metric formula with ln values provided or exact · `HyperbolicDistanceGenerator` · graduate · d4
- [ ] Stereographic projection — plane ↔ Riemann sphere point mapping both directions · `StereographicGenerator` · graduate · d4

### Differential Geometry & Topology (computational)
- [ ] First fundamental form E, F, G for parametrized surfaces (cylinder, sphere, torus); surface area via ∫∫√(EG−F²) · `FundamentalFormGenerator` · graduate · d4
- [ ] Christoffel symbols for 2D metrics (polar coordinates, the sphere) — tabular formula grinding at its purest · `ChristoffelGenerator` · graduate · d5
- [ ] Gaussian curvature — surfaces of revolution and orthogonal metrics; K = 1/R² on the sphere, K < 0 on the saddle · `GaussianCurvatureGenerator` · graduate · d5
- [ ] Gauss-Bonnet as verification — total curvature vs 2πχ on sphere and torus; the theorem *is* a CHECK step (A1) · `GaussBonnetGenerator` · graduate · d4
- [ ] Arc length under a given metric — integrate ds² = E du² + 2F du dv + G dv² along simple paths · `MetricArcLengthGenerator` · graduate · d4

### Hilbert Spaces & Quantum Information
Where linear algebra becomes physics. Everything here is finite-dimensional
matrix arithmetic or explicit integration — no functional analysis proofs.
- [ ] Function-space inner products — ⟨f,g⟩ = ∫f·g; orthogonality checks for the sin/cos family · `FunctionInnerProductGenerator` · graduate · d3
- [ ] Gram-Schmidt on {1, x, x², …} — construct the first Legendre polynomials by hand · `LegendreConstructionGenerator` · graduate · d4
- [ ] Hermitian & unitary verification — compute A†, check A = A† and U†U = I, confirm real eigenvalues (composes with `EigenvalueGenerator`) · `HermitianCheckGenerator` · college · d3
- [ ] Kronecker/tensor products — build 4×4 operators from 2×2 ⊗ 2×2; apply to product states · `TensorProductGenerator` · college · d3
- [ ] Quantum gates — apply H, X, Y, Z, CNOT to qubit states; measurement probabilities; small circuits end to end · `QuantumGateGenerator` · college · d3
- [ ] Bell states & entanglement arithmetic — separability by attempted factorization; reduced density matrix via partial trace · `PartialTraceGenerator` · graduate · d4
- [ ] Density matrices — build ρ from ensembles; expectations Tr(ρA); purity Tr(ρ²) · `DensityMatrixGenerator` · graduate · d4
- [ ] Von Neumann entropy — dyadic eigenvalues so log₂ is exact (composes with `EntropyGenerator`) · `VonNeumannEntropyGenerator` · graduate · d4
- [ ] Projectors & completeness — verify P² = P and Σ|i⟩⟨i| = I resolutions · `ProjectorGenerator` · graduate · d3
- [ ] Uncertainty products — ΔxΔp for particle-in-a-box states (extends `WavefunctionGenerator`, reusing its ⟨x⟩/⟨x²⟩ machinery) · `UncertaintyGenerator` · graduate · d5

### Lie Groups & Symmetry (computational)
The symmetry machinery of particle physics, done as explicit matrix work.
- [ ] Matrix group membership — verify RᵀR = I, det R = 1 for SO(2)/SO(3) candidates; U†U = I, det U = 1 for SU(2) · `MatrixGroupCheckGenerator` · graduate · d3
- [ ] Rotations from generators — exponentiate so(2)/so(3) elements (composes with `MatrixExponentialGenerator`) · `LieExponentialGenerator` · graduate · d4
- [ ] Structure constants — verify [Jᵢ, Jⱼ] = iεᵢⱼₖJₖ by explicit commutators of the given matrices · `StructureConstantGenerator` · graduate · d4
- [ ] Pauli & Gell-Mann algebra — products, anticommutators, trace identities Tr(σᵢσⱼ) = 2δᵢⱼ · `PauliAlgebraGenerator` · graduate · d3
- [ ] Casimir verification — J² = j(j+1)·I for given spin-1 matrices · `CasimirGenerator` · graduate · d4
- [ ] Levi-Civita index gymnastics — εᵢⱼₖεᵢₗₘ = δⱼₗδₖₘ − δⱼₘδₖₗ applied numerically and symbolically · `IndexGymnasticsGenerator` · graduate · d4
- [ ] Baker-Campbell-Hausdorff to second order — expand log(e^A e^B) for nilpotent/truncated matrices · `BCHGenerator` · graduate · d5
- [ ] Representation dimensions — Young-tableaux hook-length arithmetic; SU(3) decompositions like 3 ⊗ 3̄ = 8 ⊕ 1 by tableau rules · `YoungTableauxGenerator` · graduate · d4
- [ ] Clebsch-Gordan coefficients — ½⊗½ and 1⊗½ built by ladder operators plus orthogonality; the classic tabular grind · `ClebschGordanGenerator` · graduate · d5

### Tensors & General Relativity (computational)
- [ ] Einstein summation — numeric contractions AᵢⱼBⱼₖ, traces, symmetrization bookkeeping · `EinsteinSummationGenerator` · graduate · d3
- [ ] Raising and lowering indices with diagonal metrics (Minkowski, the sphere) · `IndexRaisingGenerator` · graduate · d3
- [ ] Riemann → Ricci → scalar curvature for the 2-sphere from its Christoffels (composes with `ChristoffelGenerator`) — tabular, long, glorious · `RiemannTensorGenerator` · graduate · d5
- [ ] 4-vector arithmetic — signature dot products; solve E² = (pc)² + (mc²)² · `FourVectorGenerator` · graduate · d3
- [ ] Schwarzschild plug-ins — rₛ = 2GM/c²; gravitational time dilation √(1 − rₛ/r); constants provided · `SchwarzschildGenerator` · graduate · d4
- [ ] Planck units — derive Planck length/time/mass from ℏ, G, c by pure dimensional analysis · `PlanckUnitsGenerator` · graduate · d4
- [ ] Black-hole thermodynamics — Hawking temperature and Bekenstein-Hawking entropy solves; quantum gravity's most famous arithmetic · `HawkingGenerator` · graduate · d4
- [ ] Casimir force between plates — F/A = −π²ℏc/(240d⁴) evaluations · `CasimirForceGenerator` · graduate · d3

### Particle Physics Arithmetic
The daily hand-computation of the field — kinematics, bookkeeping, and
algebra checks. Constants and logs provided per Principle 5.
- [ ] Natural units — GeV ↔ mass ↔ length ↔ time with ℏ = c = 1; dimensional analysis, final boss · `NaturalUnitsGenerator` · graduate · d4
- [ ] Relativistic kinematics — invariant mass of decay products, CM energy √s, threshold energies, two-body decay momenta · `InvariantMassGenerator` · graduate · d4
- [ ] Conservation bookkeeping — audit charge, lepton, and baryon number: is this reaction allowed? (n → p + e⁻ + ν̄ₑ ✓) · `ConservationLawGenerator` · college · d3
- [ ] Quark content arithmetic — hadron charges from constituents (uud → +1) · `QuarkCompositionGenerator` · college · d3
- [ ] Widths & branching ratios — partial widths → BR; lifetime τ = ℏ/Γ · `BranchingRatioGenerator` · graduate · d3
- [ ] Collider arithmetic — event rate = luminosity × cross section; barns and inverse femtobarns · `CrossSectionGenerator` · graduate · d3
- [ ] Dirac gamma algebra — verify {γᵘ, γᵛ} = 2ηᵘᵛ entries and small trace theorems by explicit 4×4 multiplication · `GammaMatrixGenerator` · graduate · d5
- [ ] Grassmann numbers — θ² = 0 makes every series terminate: expand, multiply, Berezin-integrate (∫dθ θ = 1); the algebra of fermions, utterly mechanical · `GrassmannGenerator` · graduate · d4
- [ ] Running coupling — one-loop RG evolution of α(μ) from α(μ₀) and the beta coefficient · `RunningCouplingGenerator` · graduate · d4

### Numerical Methods
- [ ] Bisection — interval-halving table with sign checks · `BisectionGenerator` · college · d2
- [ ] Newton-Raphson iterations (also serves √a and IRR) · `NewtonRaphsonGenerator` · college · d3
- [ ] Fixed-point iteration with |g′| < 1 convergence check · `FixedPointGenerator` · college · d3
- [ ] Interpolation — Lagrange form; Newton divided-difference tables · `InterpolationGenerator` · college · d4
- [ ] Finite-difference tables; forward/central difference derivatives · `FiniteDifferenceGenerator` · college · d3
- [ ] Runge-Kutta single steps — RK2/RK4 stage tables (extends `EulerMethodGenerator`) · `RungeKuttaGenerator` · college · d4

### Probability Theory & Mathematical Statistics
- [ ] Continuous distributions — normalize a pdf, then P(a<X<b), mean, variance by integration · `ContinuousDistributionGenerator` · college · d3
- [ ] Named distributions — Poisson, exponential, uniform, normal (z-values provided) · `NamedDistributionGenerator` · college · d3
- [ ] Joint distributions — marginals, conditionals, independence check, covariance/correlation · `JointDistributionGenerator` · college · d4
- [ ] Moment generating functions — derive, differentiate for moments · `MGFGenerator` · graduate · d4
- [ ] Transformations of random variables — CDF method and Jacobian · `RVTransformGenerator` · graduate · d5
- [ ] Maximum likelihood — write log-likelihood, differentiate, solve (Bernoulli, exponential, normal μ) · `MLEGenerator` · graduate · d4
- [ ] Method of moments estimators · `MethodOfMomentsGenerator` · graduate · d3
- [ ] Conjugate Bayesian updates — beta-binomial and normal-normal posterior parameters, purely mechanical · `BayesianUpdateGenerator` · graduate · d4
- [ ] Markov chains — n-step probabilities, steady state, absorption probabilities and expected hitting times via linear systems · `MarkovChainGenerator` · college · d4
- [ ] Order statistics — small n, uniform case · `OrderStatisticsGenerator` · graduate · d4

### Optimization & Operations Research
- [ ] Simplex method — tableau pivots to optimality, the classic mechanical table · `SimplexGenerator` · college · d5
- [ ] LP corner-point method — find vertices via 2×2 solves, evaluate objective · `LPCornerGenerator` · college · d3
- [ ] Gradient descent iterations on quadratic bowls · `GradientDescentGenerator` · college · d3
- [ ] Transportation problem — northwest-corner start, stepping-stone improvement · `TransportationGenerator` · graduate · d4
- [ ] 2×2 games — expected payoffs, mixed-strategy equilibrium, minimax · `GameTheoryGenerator` · college · d4
- [ ] EOQ and M/M/1 queueing metrics — formula chains with unit checks · `ORFormulaGenerator` · graduate · d3

### Signals & Systems / Control
- [ ] Discrete convolution of finite sequences — the sliding-window table · `ConvolutionGenerator` · college · d3
- [ ] DFT of length-2/4 signals — twiddle-factor arithmetic · `DFTGenerator` · college · d4
- [ ] Fourier series coefficients — square and sawtooth waves by integration · `FourierSeriesGenerator` · college · d4
- [ ] z-transforms of basic sequences; solve difference equations · `ZTransformGenerator` · graduate · d4
- [ ] Sampling/Nyquist and dB arithmetic · `SignalArithmeticGenerator` · college · d2
- [ ] Transfer functions from ODEs; block-diagram reduction; poles and zeros · `TransferFunctionGenerator` · graduate · d4
- [ ] Routh-Hurwitz stability array · `RouthHurwitzGenerator` · graduate · d4

### Physics — Mechanics
- [ ] Projectile motion — full trajectory solves with components · `ProjectileMotionGenerator` · college · d2
- [ ] Newton's laws systems — inclines, friction, Atwood machines; solve the simultaneous equations · `NewtonsLawsGenerator` · college · d3
- [ ] Momentum and collisions — elastic/inelastic, 1D and 2D components · `CollisionGenerator` · college · d3
- [ ] Work-energy theorem and energy conservation · `EnergyConservationGenerator` · college · d2
- [ ] Circular motion and gravitation; Kepler's third law · `OrbitalMechanicsGenerator` · college · d3
- [ ] Statics — force and torque balance on beams and levers · `StaticsGenerator` · college · d3
- [ ] Rotational dynamics — parallel-axis theorem, angular momentum conservation · `RotationalDynamicsGenerator` · college · d4
- [ ] Simple harmonic motion — ω, period, energy exchange · `SHMGenerator` · college · d3
- [ ] Lagrangian mechanics — write T and V, apply Euler-Lagrange (pendulum, mass-spring, Atwood) · `LagrangianGenerator` · graduate · d4
- [ ] Hamilton's equations for the same systems · `HamiltonianGenerator` · graduate · d4

### Physics — Electromagnetism & Circuits
- [ ] Coulomb superposition — fields and potentials of point-charge sets · `ElectrostaticsGenerator` · college · d3
- [ ] Gauss's law for symmetric distributions · `GaussLawGenerator` · college · d4
- [ ] RC/RL transients — time constants, exponential answers in exact form · `TransientCircuitGenerator` · college · d4
- [ ] AC circuits — complex impedance, phasors, resonance (composes with complex arithmetic) · `ACCircuitGenerator` · graduate · d4
- [ ] Magnetic forces; Biot-Savart and Ampère standard cases · `MagnetismGenerator` · college · d4

### Physics — Thermodynamics & Statistical Mechanics
- [ ] Gas laws and multi-step processes · `GasLawGenerator` · college · d2
- [ ] First-law bookkeeping — Q, W, ΔU across isothermal/adiabatic/isobaric/isochoric legs · `FirstLawGenerator` · college · d3
- [ ] Heat engines and refrigerators — efficiency, Carnot limits, COP · `HeatEngineGenerator` · college · d3
- [ ] Entropy changes for ideal-gas processes and mixing · `EntropyChangeGenerator` · college · d4
- [ ] Calorimetry with phase changes · `CalorimetryGenerator` · college · d2
- [ ] Two-level systems — Boltzmann factors, partition function, occupancies, mean energy · `PartitionFunctionGenerator` · graduate · d4
- [ ] Blackbody radiation — Wien and Stefan-Boltzmann solves · `BlackbodyGenerator` · college · d3

### Physics — Quantum Mechanics
- [ ] Photoelectric effect, de Broglie wavelength, Compton shift · `QuantumFormulaGenerator` · college · d3
- [ ] Particle in a box — energy levels, transition wavelengths · `ParticleInBoxGenerator` · college · d3
- [ ] Normalize wavefunctions; expectation values ⟨x⟩, ⟨x²⟩ by integration · `WavefunctionGenerator` · graduate · d4
- [ ] Spin-½ — apply Pauli matrices, eigenvalues, measurement probabilities · `SpinHalfGenerator` · graduate · d4
- [ ] Operator commutators — bracket algebra applied to test functions · `CommutatorGenerator` · graduate · d4
- [ ] Harmonic-oscillator ladder operators — algebraic energy computations · `LadderOperatorGenerator` · graduate · d5
- [ ] Hydrogen atom — Rydberg transitions, ionization energies · `HydrogenAtomGenerator` · college · d3
- [ ] Finite-dimensional bra-ket — inner products, time evolution under a diagonal Hamiltonian · `BraKetGenerator` · graduate · d4

### Physics — Relativity, Waves & Optics
- [ ] Lorentz transformations — time dilation, length contraction · `SpecialRelativityGenerator` · college · d3
- [ ] Relativistic energy-momentum; velocity addition; E = mc² · `RelativisticEnergyGenerator` · college · d4
- [ ] Minkowski invariant interval — s² = c²t² − x² classification (timelike/spacelike/lightlike); rapidity addition, where velocities compose by simple addition · `MinkowskiIntervalGenerator` · graduate · d4
- [ ] Doppler shift — acoustic and relativistic · `DopplerGenerator` · college · d3
- [ ] Snell's law; thin-lens and mirror equations; magnification · `OpticsGenerator` · college · d2
- [ ] Interference — double slit, diffraction gratings, thin films · `InterferenceGenerator` · college · d3
- [ ] Standing waves — harmonics on strings and pipes · `StandingWaveGenerator` · college · d2

### Chemistry Computations
- [ ] Stoichiometry — balance equations, mole-mass-volume chains, limiting reagent · `StoichiometryGenerator` · high · d4
- [ ] Molarity and dilution — M₁V₁ = M₂V₂, mixing · `SolutionChemGenerator` · high · d3
- [ ] pH/pOH — log arithmetic with provided log values or powers of ten · `PHCalculationGenerator` · high · d4
- [ ] Ideal-gas stoichiometry — PV = nRT crossovers · `GasStoichiometryGenerator` · high · d4

### Information Theory & Coding
- [ ] Entropy of discrete distributions — dyadic probabilities so log₂ is exact (Principle 5 by construction) · `EntropyGenerator` · college · d3
- [ ] Joint/conditional entropy and mutual information from a joint table · `MutualInformationGenerator` · college · d4
- [ ] KL divergence between small distributions · `KLDivergenceGenerator` · graduate · d4
- [ ] Binary symmetric channel capacity — 1 − H_b(p) · `ChannelCapacityGenerator` · graduate · d4
- [ ] Huffman coding — tree construction, expected length vs entropy, Kraft check as verification (A1) · `HuffmanCodingGenerator` · college · d4
- [ ] Arithmetic coding — interval-narrowing trace · `ArithmeticCodingGenerator` · graduate · d5
- [ ] Hamming(7,4) — encode, compute syndrome, correct single errors · `HammingCodeGenerator` · college · d4
- [ ] CRC — polynomial long division over GF(2), long division's binary cousin · `CRCGenerator` · college · d4
- [ ] Kraft inequality and code-length feasibility · `KraftInequalityGenerator` · college · d3

### Machine Learning by Hand
Poetic bonus: the model learns to compute its own building blocks on paper.
- [ ] One gradient-descent step on MSE loss — compute the gradient, update the weights (the ML-loss counterpart of `GradientDescentGenerator`; `AdamStepGenerator` extends it) · `GradientStepGenerator` · graduate · d4
- [ ] Perceptron updates over a small dataset · `PerceptronGenerator` · graduate · d3
- [ ] Tiny neural network — forward pass plus one backprop step, chain-rule bookkeeping in tables · `BackpropGenerator` · graduate · d5
- [ ] Naive Bayes classification from count tables · `NaiveBayesGenerator` · college · d4
- [ ] Decision-tree splits — information gain via entropy (composes with `EntropyGenerator`) · `InformationGainGenerator` · graduate · d4
- [ ] k-means — one full assign/update iteration · `KMeansStepGenerator` · college · d3
- [ ] k-NN classification with an explicit distance table · `KNNGenerator` · college · d2
- [ ] Confusion-matrix metrics — precision, recall, F1 · `ClassifierMetricsGenerator` · college · d2

### Matrix Calculus & ML Linear Algebra
- [ ] Matrix calculus — gradients of vector/matrix expressions: ∇ₓ(aᵀx), ∇ₓ(xᵀAx) = (A + Aᵀ)x, applied numerically and symbolically · `MatrixCalculusGenerator` · graduate · d4
- [ ] Norms — L1, L2, L∞, Frobenius; spectral norm of small matrices via eigenvalues; condition numbers · `MatrixNormGenerator` · college · d3
- [ ] Positive-definiteness checks — Sylvester's criterion via leading principal minors · `PositiveDefiniteGenerator` · college · d3
- [ ] Covariance matrix from a small dataset → 2×2 PCA — eigendecompose, project onto the principal component · `PCAGenerator` · graduate · d4
- [ ] Cosine similarity & distance matrices over small embedding sets — the geometry of embeddings, incl. king − man + woman analogy arithmetic · `EmbeddingSimilarityGenerator` · college · d3
- [ ] Low-rank approximation — truncated SVD of small matrices, reconstruction error in Frobenius norm · `LowRankApproxGenerator` · graduate · d4

### Kernel Methods
- [ ] Kernel evaluations & Gram matrices — polynomial and RBF kernels over 2-3 points (RBF exponent values exact or provided per Principle 5) · `KernelEvaluationGenerator` · graduate · d3
- [ ] Feature-map verification — expand φ(x)·φ(z) explicitly and confirm it equals K(x,z) for the polynomial kernel; the kernel trick made visible · `FeatureMapGenerator` · graduate · d4
- [ ] Kernel validity — check a small Gram matrix is PSD via Sylvester's criterion (composes with `PositiveDefiniteGenerator`) · `KernelValidityGenerator` · graduate · d4
- [ ] Kernel ridge regression on 2-3 points — solve (K + λI)α = y, predict a new point · `KernelRidgeGenerator` · graduate · d4
- [ ] SVM margin arithmetic — decision function from given support vectors and α's; margin width 2/‖w‖ · `SVMMarginGenerator` · graduate · d4
- [ ] Kernel perceptron — updates in α-space over a small dataset · `KernelPerceptronGenerator` · graduate · d4

### Transformer & LLM Arithmetic
The model hand-computes its own forward pass. Softmax stays exact by
construction: choose logits as ln of rationals (Principle 5), so the weights
come out as exact fractions.
- [ ] Scaled dot-product attention by hand — 2-3 tokens, d = 2: QKᵀ/√d, exact softmax, weighted sum of V; THE computation · `AttentionGenerator` · graduate · d5
- [ ] Softmax & cross-entropy — plain evaluation, temperature scaling, log-softmax, and the softmax+CE gradient p − y applied numerically; the single home for softmax math · `SoftmaxGradientGenerator` · graduate · d4
- [ ] LayerNorm by hand — mean, variance, normalize, scale-and-shift on small vectors (composes with `StandardDeviationGenerator`) · `LayerNormGenerator` · college · d3
- [ ] Activation functions — ReLU/GELU/sigmoid values and derivatives (e-values provided); chain them through a two-layer computation · `ActivationGenerator` · college · d3
- [ ] Sinusoidal positional encodings at nice angles · `PositionalEncodingGenerator` · college · d3
- [ ] Parameter counting — attention + MLP + embeddings per layer, the ≈12·d²·L back-of-envelope; LoRA counting r(d_in + d_out) vs full fine-tuning · `ParamCountGenerator` · college · d3
- [ ] FLOPs & memory arithmetic — matmul FLOPs 2mnk through a forward pass; KV-cache bytes = 2·L·h·d_k·seq·precision · `FLOPsMemoryGenerator` · college · d4
- [ ] Scaling-law arithmetic — C ≈ 6ND, Chinchilla-optimal tokens ≈ 20× params, tokens/s from FLOPs budgets · `ScalingLawGenerator` · college · d3
- [ ] One Adam step by hand — moment updates, bias correction, parameter update with nice numbers (extends `GradientStepGenerator`) · `AdamStepGenerator` · graduate · d4
- [ ] Learning-rate schedules — linear warmup + cosine decay evaluated at step t · `LRScheduleGenerator` · college · d2
- [ ] Perplexity — from cross-entropy with dyadic probabilities so the exponentiation is exact (composes with `EntropyGenerator`) · `PerplexityGenerator` · graduate · d3
- [ ] Quantization arithmetic — int8 scale/zero-point, quantize → dequantize a small tensor, measure round-trip error · `QuantizationGenerator` · college · d3

### Financial Mathematics
- [ ] Annuities — present/future value; amortization schedule tables · `AnnuityGenerator` · college · d4
- [ ] Bond pricing and current yield · `BondPricingGenerator` · college · d4
- [ ] NPV; IRR via Newton iterations (composes with `NewtonRaphsonGenerator`) · `NPVIRRGenerator` · college · d4
- [ ] Two-asset portfolio — expected return and variance with covariance · `PortfolioGenerator` · graduate · d4
- [ ] Black-Scholes evaluation with N(d₁), N(d₂) provided (Principle 5) · `BlackScholesGenerator` · graduate · d4

---

## Suggested Order

1. Algebra 1 core: Factoring & Quadratics → Radicals & Rationals → Functions → Sequences
4. Geometry & Trigonometry
5. Exponentials/Logs, Complex, Polynomials, Conics
6. Vectors/Matrices → Limits → Calculus AB → BC
7. Statistics & Probability (inference last; needs Principle-5 conventions)
8. Applied topics interleave anywhere — they add variety to every training mix
9. **A8**, then the college trunk everything else composes with: Multivariable Calc, Linear Algebra, ODEs, Discrete, Number Theory, Numerical Methods
10. College applied: Mechanics, E&M & Circuits, Thermo, Waves/Optics, Chemistry, Signals, OR, Finance
11. Graduate tier: Statistical Mechanics & Quantum computations, MLE/Bayesian statistics, Markov chains, Complex Analysis (through Möbius and complex logs), Spherical & Non-Euclidean Geometry, Differential Geometry & Topology, Information Theory & Coding, ML by Hand → Matrix Calculus → Kernel Methods → Transformer & LLM Arithmetic
12. The frontier tier: Hilbert Spaces & Quantum Information, Lie Groups & Symmetry, Tensors & GR, Particle Physics Arithmetic — deliberately last because it composes with everything below it: eigenvalues feed Hamiltonians, Christoffels feed Riemann, Shannon entropy feeds von Neumann, complex arithmetic feeds SU(2)

The composition pattern is deliberate: circuits reuse row reduction, AC reuses
complex arithmetic, information gain reuses entropy, IRR reuses Newton's
method, and the physics frontier reuses all of it at once. Later tracks are
cheap once their trunk skills exist — and composite problems (A5) get richer
at every tier.

---

## Removed from Curriculum

These don't fit step-by-step computational scratchpad training:

- **Conceptual/identification (no computation):** conditional statements;
  converse/inverse/contrapositive; congruence-postulate identification;
  vertical line test; conic identification from general form; even/odd
  determination; end-behavior analysis; continuity three-condition checks;
  interpreting slope/intercept.
- **Graphing/visual output:** graphing lines, inequalities, systems, rational
  functions, polar/parametric curves; slope fields; domain/range *from a
  graph*; residual plot analysis.
- **Proofs (natural-language reasoning):** two-column algebraic proofs,
  segment/angle proofs, CPCTC, coordinate proofs.
- **Translation-only (no solving):** writing expressions from word problems.
- **Multi-path/ambiguous:** SSA ambiguous case.
- **Bare table lookup:** z ↔ percentile and normal probability *as lookups* —
  but see the Stretch section: with the table excerpt provided in the problem,
  the arithmetic part is fair game.
