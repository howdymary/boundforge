# Critical review and response (2026-11-15)

A bounded Tinker call returned a truncated, unparsed critique. It is an unverified model output, not an independent mathematical endorsement or evidence of novelty. Preserve its raw text in results/followup-research/critique.json.

Useful cautions: basis changes need not unlock a repair; repair cardinality can be large; exact finite-scope failure must not be generalized; basis exchange and explanation-guided search are standard. The pilot independently shows that enabled repairs did not yield a controller advantage.

Corrections to the model's objections:
- C is explicitly a squared Euclidean row-norm bound. Basis IDs always select original public rows, including after pivots; derived echelon vectors are not the rows to which the Hadamard bound is applied. C^d < p^2 bounds every smaller minor too because C >= 1.
- recover() constructively tries moment parameters 0..(nullity-1)*number_of_forbidden_equations. Each nonidentically-zero forbidden linear form becomes a polynomial of degree at most nullity-1. Their total possible roots bound the search. Rational denominator growth remains a practical cost, not a missing existence argument.
- Search enumerates repairs of size at most two, not unbounded minimum hitting sets. This is a basis-size quadratic enumeration times diagnostic cost. No general polynomial-time minimum-hitting-set or global optimization claim is made.
- An unpivotable obstruction would refute universal effectiveness, which we never assert; it would also be a useful scoped negative case. It would not refute an empirical claim about some other class.

Follow-up Exa found important additional prior art: Khachiyan et al., On the Complexity of Some Enumeration Problems for Matroids (https://doi.org/10.1137/S0895480103428338), and Streit/Garg, Reducing Matroid Optimization to Basis Search (https://arxiv.org/html/2408.04118v4). The latter optimizes linear weights on binary-matroid bases via cocircuit certificates; our objective is nonlinear projection entropy on rational flats excluding protected vectors. This distinguishes the optimization problem, not automatically the research mechanism.

Konyagin/Lev (https://doi.org/10.1112/S0025579300015709) already connects Freiman relations to linear algebra. A finite collision representation, modular rank implementation, or basis pivot alone is not a new general method.
