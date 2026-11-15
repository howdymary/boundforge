# Mathematical verification of the C51a result

The final autonomous certificate proves C51a > 0.585078819674513593. The first project certificate proved >0.58507881967451359; the extra displayed digit is tighter certification of this project's refinement, not a second independent discovery.

## Statement and construction

For transcendental entire f(z)=sum a_n z^n, let mu(r)=max_n |a_n|r^n, M(r)=max_|z|=r |f(z)| and beta(f)=liminf_(r→infinity) mu(r)/M(r). C51a is the supremum of beta over these functions. The direction is a LOWER bound.

Take the exact rational K>1 and alpha in the saved candidate, and a_n=exp(i alpha n(n-1)/2)K^(-n(n+1)/2). Every coefficient is nonzero and |a_n|^(1/n)→0, so f is entire and non-polynomial.

The construction and reduction are prior art: [He–Tang](https://arxiv.org/html/2602.12217), extending Clunie–Hayman. The parameter/equioscillation strategy is also in the [working report](https://erdosproblemaday.com/report/513). No new reduction theorem is asserted.

## Check of the asymptotic implication

Extend the series bilaterally to k on C\{0}. Both tails converge normally on compact annuli. Coefficient comparison gives k(Kz)=z k(e^(i alpha)z). Iterating gives
k(K^m z)=K^(m(m-1)/2) exp(i alpha m(m-1)/2) z^m k(exp(i alpha m)z).
Thus M(K^m,k)=K^(m(m-1)/2) A, where A=max_|z|=1 |k(z)|.

At r=K^m, terms m-1,m tie and mu=K^(m(m-1)/2). On K^m<r<K^(m+1), the maximal index is m, because successive term ratios are r/K^(n+1). Log(mu) is affine in log(r) there. Hadamard three-circles makes log(M) convex, so log(mu/M) is concave and its minimum is at an endpoint. The defining liminf therefore reduces to these radii. The deleted negative-index tail is O(1/r), negligible relative to the endpoint maximum term. Consequently beta(f)=1/A. This is the operative He–Tang argument, not merely a numerical assumption.

Pairing bilateral indices n and -n-1 after z=exp(i alpha)exp(2i theta) yields
A=max_theta |P(theta)|,
P(theta)=2 sum_(n>=0) K^(-T_n) exp(i alpha T_n) cos((2n+1)theta),
T_n=n(n+1)/2.
Evenness and pi-antiperiodicity reduce the entire circle to theta in[0,pi/2].

## Finite verification

For truncation N, the uniform omitted tail is at most the EXACT rational
T=2 K^(-((N+1)(N+2)/2))/(1-K^(-(N+2))).
The autonomous runner selected N=8 from a numerical proof-slack estimate; the verifiers independently recompute and bound its tail. Numerical depth selection cannot accept the result.

1. The real cosine cross-coefficient checker writes |P_N|²=4x|sum c_n R_n(x)|², x=cos²(theta), R_0=1,R_1=4x-3,R_(n+1)=(4x-2)R_n-R_(n-1). Interval coefficients become exact rational upper Bernstein coefficients. Nonnegative partition-of-unity weights and exact de Casteljau subdivision give a full[0,1] cover.
2. The direct trig checker bounds Q=|P_N|² at each dyadic midpoint by Q(m)+|Q'(m)|r+Lr²/2. With S_j=sum_(n<=N)2K^(-T_n)(2n+1)^j, a valid global second-derivative bound is 2(S_1²+S_0S_2), with the (pi/2)² coordinate factor for y in[0,1]. Every cell is accepted or subdivided; no sampled list of peaks is trusted.
3. Arhan Canli's separately authored, unchanged published checker uses standard-library decimal intervals and a third-derivative/Taylor cover of[0,1.5708]. Source SHA256 bc59bfbb62d308341666bcee3dfc05b2ec533da3f55f4e433de12b4c2f22e8e8, pinned MIT-licensed source in quantavane-replays@ad5a4b17586a8c568ecc10d7fa78082830eefd95.

Each proves max|P_N|+T <1/claimed_bound. The first two share mpmath interval arithmetic at100digits; the third is an independent implementation and arithmetic dependency. This is execution of independently authored code, not independent human endorsement or formalization in Lean.

## Strict comparison, not rounded-number chasing

The strongest external witness located is K=3.568185442233685,alpha=3.961543111810228. Both of our full-circle checkers reproduce its certified lower value, and pointwise interval evaluation at0 and an exact rational interior theta gives an UPPER bound on its actual beta. This is valid because A_old >= |P_N,old(theta)|_lower - T_old. No claim that the chosen theta is an exact optimizer is needed.

The final claimed lower bound exceeds that actual-function upper bound by more than1.58×10^-17. It therefore changes the construction relative to the external witness; it is not only another digit of the unchanged prior function. A tightened version of Röhrig's witness is also weaker. The public-source audit is scoped: no stronger applicable public lower witness was found in the inspected sources.

## Limits

The gain is extremely small. Optimizers, model explanations and root equations do not establish validity, global parameter optimality or methodological novelty. The work is AI-assisted and not peer reviewed. Tests reject false enlarged claims and invalid parameters and cross-check the polynomial/trig identity. Protected C3c verifiers retain their original hashes.
