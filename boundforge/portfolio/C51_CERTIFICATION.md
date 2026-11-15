# C51a precision certificate specification

Candidate exact rational decimals: K=3.56818544223368269553925743732750636848, alpha=3.96154311181022808045648786109191322475. Claim C51a >0.58507881967451359. This is a tiny, conventional parameter refinement, NOT success of the preregistered >1e-9 periodic-phase pilot. No new general research mechanism.

Independent arithmetic algorithms:
1. Real cosine cross-coefficients produce polynomial Q(x)=4x|sum c_n R_n(x)|², x=cos²(theta). Interval constants become exact rational upper Bernstein coefficients. Complete rational subdivision covers [0,1].
2. Direct trig evaluations of |P|² and its derivative at dyadic midpoints plus a global second-derivative bound give upper Taylor envelopes. Complete dyadic cover of theta=(pi/2)y,y in[0,1]. No polynomial/Bernstein code imported.
Both include the exact infinite tail 2 K^{-T_(N+1)}/(1-K^{-(N+2)}), N=12. Both use the same mpmath interval arithmetic library (shared trust dependency), independently implemented evaluation/remainder machinery; neither is a clean-room human review.

Analytic dependency: [He–Tang Theorem2.8](https://arxiv.org/html/2602.12217), yielding beta(f)=1/max_theta|P(theta)| for the specified transcendental entire function. Here P(theta)=2 sum K^{-Tn} exp(i alpha Tn) cos((2n+1)theta). Coefficients' nth-root moduli go to zero and are all nonzero. All frequencies odd, so evenness and pi-antiperiodicity reduce the whole circle to[0,pi/2].

Reproduce full-circle lower certificates for BOTH strongest discovered previous functions, including the unmerged [working report](https://erdosproblemaday.com/report/513). Also evaluate their modulus with intervals at0 and rational interior points, subtracting tails: beta_old <=1/(|P_N(theta)|_lower-tail). Require the NEW claimed lower bound to beat these upper bounds, thus proving a changed construction rather than extra displayed digits.

2026-11-15 final Exa audit found no stronger applicable lower construction in searches of Tao page/openPRs, He–Tang paper, official Erdős forum/proof-claims, Röhrig packet, Lystad claims and working report. It also found Tomar's new upper bound0.63005 (Zenodo23537612), a different direction that must not be confused with a stronger lower witness. This source search is scoped, not proof of global priority. No leaderboard submission/paper/contact authorized.
