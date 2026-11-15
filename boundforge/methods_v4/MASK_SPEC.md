# Exact support signatures: candidate mechanism, not established novelty

## Mathematical scope
A nonempty finite base support in Q^d and finitely many rational linear scalar maps l_j are fixed. Let S_j be each old image set. A new atom x has novelty mask n_j=1[l_j(x) not in S_j]. Enumerate every attainable mask, with a rational representative, over the entire unbounded rational domain.

## Completeness proof
For any x, take the rows l_j whose images at x belong to S_j. Choose an independent basis I of these rows. The affine flat l_i(z)=l_i(x), i in I, is among the enumerated flats, since rank is at most d and the assigned values are old. Every zero-mask projection is constant at its old value on this flat. A projection that is constant at a new value stays new; every varying projection can avoid its finite old values. Thus its generic representative has exactly x's mask.

For a k-dimensional rational flat use p+t v_1+...+t^k v_k. Every forbidden equation for a varying projection is a nonzero polynomial of degree at most k. At most k times the total number of forbidden old values are integer parameters forbidden. Trying one more distinct integer guarantees success. Constant projections are handled separately. Degenerate and zero maps are allowed.

Enumerating rank-r independent projection subsets and old values costs at most sum_{r=0}^d sum_{|I|=r} product_{i in I}|S_i| affine solves, before deduplication. There are at most 2^m masks. This is exponential in d/m, not a scalable solution to arbitrary entropy search.

## Leading-order support cone
Add total mass epsilon with normalized rational mixture weights w over new atoms, scaling the base by 1-epsilon. For each projection, the coefficient of epsilon log(1/epsilon) in its entropy change is sum_x w_x n_j(x). Collisions among newly born images do not change this leading coefficient; they do affect ordinary epsilon terms. Consequently linear entropy margins have leading matrix V_(r,n)=sum_j a_(r,j)n_j.

Maximize gamma subject to Vw >= gamma, w>=0, sum w=1. Any exact feasible w gives a rigorous lower bound min(Vw). Any exact probability vector mu over margins gives an upper bound max_n sum_r mu_r V_(r,n). The implementation uses floating LP only to propose these vectors, rationalizes, and recomputes both bounds exactly. Inexact zero reconstruction can remain unresolved.

A positive lower bound yields simultaneous positive leading logarithmic ascent. A nonpositive upper bound rules out strictly positive logarithmic ascent in this fixed-support, fixed-map, normalized infinitesimal addition class. It does not exclude ordinary-order improvement, higher-order paths, replacing base mass in another way, map changes, or a ratio improvement through inactive margins. A zero result explicitly routes to higher-order analysis.

## Prior art and claim limits
Entropy support insertion and its epsilon log epsilon asymptotics are already in BoundForge's attributed Jaswal refinement code. Linear algebra, finite hyperplane avoidance, max-min LP and rational primal-dual verification are standard. The candidate contribution is the complete geometric pricing reduction and its role in an autonomous diagnostic controller. Its distinctness from hyperplane-arrangement enumeration, entropy-support enumeration, column generation and multiobjective descent remains unestablished. A passing unit test or a tiny record is not evidence of a new research method.

## Planned rejection tests
Check masks independently against finite grids on small problems; validate representative masks directly; test dependent and zero maps, rational coordinates, d=1/2/3; compare with pair-intersection and random-box baselines including total cost; exercise positive coordinated births and negative dual certificates. Development fixtures are not untouched transfer evidence.
