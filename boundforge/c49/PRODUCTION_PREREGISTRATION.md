# Exploratory new-family constraint search

Frozen before production execution; separate from the seven-arm held-out controller comparison.

The small-base greedy pilot stalled on F10. Change the representation of the search: CP-SAT selects a whole family over the complete nontrivial-mask universe, imposes exact Sperner constraints, and adds exact sunflower clauses found in proposed families. This is classical constraint separation, not a new algorithm.

Six bounded configurations: n10, eigenvector ratios145/100,148/100,150/100,155/100; n11, ratios160/100,170/100. Two solver threads, at most300wall seconds each, max4containers, hard420s worker timeout. Stop an individual run after six consecutive8-second solves without a feasible candidate. Preserve every status and cut count. A solver-reported infeasibility is scoped to the rational ratio criterion and is not independently certified UNSAT.

For T=[[N10,N11],[N00,N01]], u=(r,1)>0, impose T*u>=lambda*u with lambda the next millionth strictly above the rigorously enclosed incumbent rate^(n-2). Perron–Frobenius/Collatz gives rho(T)>=lambda, so an exactly valid resulting family would beat the bar. Fixed r restricts the search, not the set of all optimum families. Fixing the ordered port pair to0,1 is valid under a permutation of the ground-set coordinates. Empty and full masks cannot coexist with any other member in a Sperner family, and a four-positive-port family needs at least4members; excluding them is justified here.

Novel families must pass literal Python and separately implemented BDD C++ checks, exact transfer-rate isolation, and a fresh-process certificate check. No floating score or CP-SAT feasibility result alone accepts a record. No target pivot is authorized.
