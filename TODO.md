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

### Linear Algebra (beyond the small-matrix K-12 items)

### Differential Equations

### Discrete Math & Combinatorics

### Graph Theory & Algorithms

### Number Theory & Cryptography

### Abstract Algebra (computational side only)

### Complex Analysis (computational)

### Spherical & Non-Euclidean Geometry
Angle sums that refuse to be 180° — mind-bending results from ordinary
arithmetic. Nice angles (30°/45°/60°/90°) keep everything exact per Principle 5.

### Differential Geometry & Topology (computational)

### Hilbert Spaces & Quantum Information
Where linear algebra becomes physics. Everything here is finite-dimensional
matrix arithmetic or explicit integration — no functional analysis proofs.

### Lie Groups & Symmetry (computational)
The symmetry machinery of particle physics, done as explicit matrix work.

### Tensors & General Relativity (computational)

### Particle Physics Arithmetic
The daily hand-computation of the field — kinematics, bookkeeping, and
algebra checks. Constants and logs provided per Principle 5.

### Numerical Methods

### Probability Theory & Mathematical Statistics

### Optimization & Operations Research

### Signals & Systems / Control

### Physics — Mechanics
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
