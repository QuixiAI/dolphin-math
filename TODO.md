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

### Physics — Electromagnetism & Circuits

### Physics — Thermodynamics & Statistical Mechanics

### Physics — Quantum Mechanics

### Physics — Relativity, Waves & Optics

### Chemistry Computations

### Information Theory & Coding

### Machine Learning by Hand
Poetic bonus: the model learns to compute its own building blocks on paper.

### Matrix Calculus & ML Linear Algebra

### Kernel Methods

### Transformer & LLM Arithmetic
The model hand-computes its own forward pass. Softmax stays exact by
construction: choose logits as ln of rationals (Principle 5), so the weights
come out as exact fractions.
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
