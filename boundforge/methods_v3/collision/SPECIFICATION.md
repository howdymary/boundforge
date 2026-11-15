# Search over projection collisions with exact obstruction-guided exchanges

Research hypothesis, 2026-11-15. This is the third implemented direction, after scalar probing failed and the paired-order credit rule was shown algebraically equivalent to an existing control. No novelty claim is accepted yet.

## Representation

For m labeled support points, fix x_0=y_0=0 and use d=2(m-1) variables. A public row encodes a(x_i-x_j)+b(y_i-y_j)=0 for a control projection (a,b). A protected row encodes target coincidence (x_i-y_i)-(x_j-y_j)=0. A state is an independent basis B of public rows. It is feasible iff no protected row lies in span(B).

The collision partition of a projection is determined by which of its difference rows lie in span(B). A generic rational vector in ker(B) realizes exactly those partitions and keeps all target values distinct. Conversely, the complete public-collision matrix of any m-point target-injective rational construction defines a feasible state with the same partitions. This removes coordinate-box restrictions for the uniform-mass search class; it does not cover all probability laws or all support sizes.

The embedding fact is standard linear algebra/Freiman modeling, not a new theorem. An explicit nullspace-basis moment curve avoids a finite union of forbidden hyperplanes and yields integer coordinates after clearing denominators. Every retained witness is checked from its integer coordinates, independently of the modular search.

## Exact arithmetic

Public and protected integer rows have squared Euclidean norm at most C. Hadamard bounds each k×k minor by C^(k/2), for k<=d. Choose a prime p with C^d<p². Every nonzero such integer minor then has magnitude <p, so rank over F_p equals rank over Q for every subset of original rows. Mersenne primes are verified by Lucas–Lehmer; the integer bound is checked for every task. Modular arithmetic here is exact under the stated determinant bound, not a probabilistic rank heuristic. This argument and modular elimination are standard.

## Diagnostic and repair rule

For an independent proposed public row r, B+r is independent. For each protected row newly entering span(B+r), obtain its unique coefficient support C_t on the old basis B. Removing D⊆B restores protected separation while retaining r iff D intersects EVERY C_t. Necessity and sufficiency follow from uniqueness of coordinates in the independent basis B+r. Enumerating all subsets of size <=k therefore certifies either a smallest allowed repair or that no such repair exists for this basis and proposed row. It says nothing about other bases, other proposed rows or global impossibility.

The attempted research contribution is using these exact, scoped failures to select a representation change rather than merely increase a random ruin size. A dependent public row q already in span(B) can replace any basis row with a nonzero coefficient in q's representation without changing the flat, any projection partition, or the current objective. Such a basis pivot can change which low-cardinality deletions are available in the NEXT exchange. The controller probes these objective-preserving representation changes when a small-repair certificate fails, then applies a newly enabled exchange if one is found. All rank tests and costs are logged.

This combines established circuits, hitting sets, basis pivots and entropy evaluation. A new general-method claim needs a material distinction from prior basis/representation search, useful matched-budget results and prospective transfer. The specific hypothesis is that failure-guided basis changes improve construction search beyond direct circuit repair and random pivots. Merely implementing the representation is insufficient.

## Development and comparisons

Initial development uses m=6,8,10 with three, four and five control projections drawn from (1,0),(0,1),(1,1),(1,2),(1,3), target(1,-1). Initial points are the same disclosed zigzag two-line construction for every policy. Uniform masses are a deliberate restriction. All policies use the same lexicographically sorted projection-entropy objective and occasional deterioration rule.

Controls: coordinate alignment/ruin search; random admissible-flat edits; exact circuit repair alone; circuit repair with random same-flat basis pivots; the failure-guided pivot controller; shuffled obstruction labels with exact final feasibility checks. A coordinate-box baseline is not sufficient; direct circuit repair is a required strong control. Any learned/directed pivot must beat it, and random pivots isolate representation diversity from diagnosis.

Use bounded CPU pilots to measure useful repairs, representation-only moves, new collision profiles, overrun, exact-check cost and objective gain. Freeze a later evaluation only after development variance/hardness assessment. Different slopes are related tasks within a class, not evidence of universal scientific reasoning. Preserve exposed tasks as development/validation, never untouched test.

## Sources and known overlap

[Konyagin–Lev, 2000](https://doi.org/10.1112/S0025579300015709): relation-matrix/Freiman linear algebra is prior art; full original text not yet accessible through inspected publisher page. [Tao, 2025](https://arxiv.org/html/2511.15135) supplies the projection/entropy setting. [AlphaEvolve paper](https://arxiv.org/html/2511.02864v3) and its two released arithmetic-Kakeya notebooks use coordinate probability grids/discrete Gaussians in the inspected examples; that is not proof its unreleased search never used relations. Fundamental circuits and constraint-guided repair are classical; no absence-based priority claim.
