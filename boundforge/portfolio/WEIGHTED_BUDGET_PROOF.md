# Weighted-budget pilot and mathematical scope

Registered before execution. This is a structural correction after616 ordinary masks failed to beat the reoptimized <4,5> incumbent. It is not yet a new bound or a claimed new general method.

Let M be a finite set of nonnegative integers containing0 and a positive element, B=max M, Q=2B+1. Assign rational costs w(a)>=0 with w(0)=0. Put
k_minus(d)=min{w(a)+w(b):a-b=d}, k_plus(s)=min{w(a)+w(b):a+b=s}.
Choose a symmetric integer type: n_d copies each of d and -d for positive differences, and n0 copies of0, summing to N. Choose a minimizing pair(alpha_d,beta_d) for d and its reversed pair for -d. In every type word the two reconstructed M-words have equal total cost
L=sum_{d>0} n_d*k_minus(d).
Thus its entire multinomial type lies in V−V, where V={a in M^N:sum w(a_i)<=L}.

Every sum word has sum k_plus(s_i)<=2L. For t>0, Markov's counting bound gives
|V+V| <= exp(2tL) (sum_s exp(-t*k_plus(s)))^N.
The same Q-digit argument as the cited unweighted construction is injective on sums and differences: coordinate differences of two digit words lie in[-2B,2B], strictly shorter than Q. Consequently this supplies a finite C3e bound using the log multinomial divided by the logarithm of that envelope. Costs and labels are separate; never replace digit labels by their costs in positional encoding.

With a Gibbs proposal p_d proportional to exp(u*k_minus(d)), u<0, the limiting ratio is rho/sigma with rho=log Z−u*mu and sigma=log P−v*mu. This only proposes counts. Exact acceptance needs rational costs, explicit symmetric integer counts, the exact cost minima, rigorous logarithms/exponentials and comparison beyond both the finite incumbent and the stronger open limiting claim.

Numerical pilot: four masks (<4,5> at80/160, <3,4> at80, <5,6> at100), at most36 initializations, bounded nonsmooth L-BFGS gradients, at most195 wall seconds. All objective improvements are logged; optimizer convergence is not a proof. No model, GPU or paid service is required for this first correction.

If no improvement over1.272558052 appears, do not describe beating only the old finite certificate as a new global frontier. The open PR339 also mentions1.2725580515...; that claim must be reconciled independently. If weighted moves fail, advance to the next ranked target rather than scale equivalent trials.

The baseline and two own checkers first reproduce the current finite witness. The weighted search has no exact acceptance path yet; a positive result requires extending and independently checking that path before any record claim. The underlying tools are type counting, weighted large deviations and standard optimization; novelty is not asserted.
