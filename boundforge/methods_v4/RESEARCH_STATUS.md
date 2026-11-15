# Research diagnosis and next-method assessment
Research date: 2026-11-15 UTC. This is a new development cycle; historical v2/v3 reports are preserved. No general-method success is declared.

## What actually failed
The campaign had conflated valid experiments, informative diagnostics, and better discovery. Kernel/cache completeness and memory hits were real, but did not establish that an intervention was useful. Cache lookup occurred after the expensive kernel calculation and also forced a particular escape move. Short, closely related task instances and uncharged serialization overhead could not support broad claims.

Most importantly, the later production campaign held support size and masses fixed and screened changes at 1e-9. That left out support insertion plus weight reoptimization. But insertion itself was **not a new discovery**: existing precision.py already implemented attributed Jaswal-style asymptotic support proposals and Newton refinement.

A direct counterfactual audit found the newly tested atom (11,-9) in law1 was already ranked **first** by the existing proposer. Its predicted log mass was about -79.17, well within the old -210 cutoff. Do not claim that cutoff or the old radius excluded this atom. The missing step was execution and certification of an available strong conventional baseline.

## New mathematical artifacts, separate from methods
1. The standalone support loop enumerated five zero-new-control-image candidates, chose its own atom and scale, and certified a strict gain over the archived C3c witness of about **4.4642179006e-59**. It selected epsilon=2^-197. This is prospective development after a human diagnostic had already exposed the existence of holes, not a blind generalization test.
2. A matched conventional counterfactual ran existing Newton refinement on the same archived witness, with and without its top-ranked support addition. Fixed-support Newton gave no strict gain. The support-addition arm converged in four iterations and produced a gain of about **2.2235523921224084943e-35**. Total worker CPU was12.72sec across both arms. Thus the existing solver's gain is about5e23 times larger than the conservative support loop's gain.
3. Both unchanged original checkers certify the larger candidate and strict comparison. Their hashes remain:
   - verify.py: 3c5cd73bf3d50eea098d3253e46e9e5ea9812ec3c2fa2711ea16b349f586ef30
   - verify_independent.py: 49e1cbbc9d287a227d8f790b2f7a678972a88f53d3c2e88592f6c1424dda0774

The candidate's exact claimed floor is in [results/legacy/candidate.json](results/legacy/candidate.json); the ratio begins **1.67489421130711622876456517316280156114334396378991130137...**. This is a tiny conventional refinement, not a substantial mathematical advance and not evidence of a new method.

The [current Tao page](https://teorth.github.io/optimizationproblems/constants/3c.html) still lists Jaswal's two-law construction as strongest merged entry, independently replayed at1.67489421130711622876434373706.... A fresh audit checked titles/bodies and first100 changed-file entries for each of96 open PRs and found no C3c file. That is a stated audit scope, not proof of absence of all unpublished or unindexed claims. No leaderboard or paper submission is authorized or made. The improvement cited above is against the project's independently reproduced archived witness, not merely the rounded table number.

## Hypotheses tested

| Mechanism | Closest prior work | Measured evidence | Assessment |
|---|---|---|---|
| Formal entropy jets select perturbation scales and precision | Existing support asymptotics; symbolic Taylor/automatic differentiation and rigorous evaluation | All9 predicted positive cases independently finite-verified. Corrected pilot: jet+verification .0431CPU sec, oracle-epsilon finite .0247sec, blind-scale finite .0293sec | Correctness useful; no speed advantage on these development cases. One pass is not a statistical speed claim. Do not scale on speed narrative. |
| Complete novelty-mask oracle over Q^d | Affine arrangement flats, multiobjective max-min LP, support insertion | Exact rational primal/dual bounds; d1/d2/d3 grid checks; coordinated example certified gamma=1/4; negative example upper=-1 | A scoped exact diagnostic, not a new generic controller. Independent symbolic control added. |
| Full equality-stratum compiler for k support additions | Arrangement intersection enumeration; canonical entropy-support enumeration | Four tasks fully enumerated (50/50/10/393 partitions); three finite improvements independently verified, one known negative control. About1.07CPU sec total | Preserves more objective information than masks. Exact finite geometry does not certify global probability optimization. |
| Model critique discovers missing mechanism | Model-assisted hypothesis generation | Tinker claimed dependent equations break mask completeness; explicit deterministic test disproves this claim. Suggested entropy splitting identity is standard | Sampling a critique is not peer review or a novelty endorsement. Reject its mathematical error. |

The initial finite baseline had two flaws: it received the jet's proposed epsilon and unnecessarily escalated precision on already resolved mixed signs. Both were corrected before interpreting a speed advantage. The corrected raw run is retained, as is the earlier run's provenance.

## What the richer representation establishes
Masks record whether an image is new, but not which old image it meets or whether two newly born images collide. We constructed two pairs with identical per-atom masks but different target entropy, independently checked at a finite epsilon. The full compiler enumerates all old-new and new-new equality strata for fixed k, maps and old support. It represents every attainable entropy vector for every common assignment of atom weights. See [mathematical scope](PARTITION_SPEC.md).

This is a useful exact reduction of an unbounded coordinate domain to finite candidate structure. Its implementation is explicitly standard arrangement traversal. It is **not** established as a new general research method.

## Closest primary sources and unresolved novelty objections
- [Liu and Walsh, arxiv1512.03324, sectionsIII-IV](https://arxiv.org/html/1512.03324): enumerate canonical k-atom support classes via partitions/group actions, then optimize probabilities. Our arithmetic-realizability/fixed-incumbent restriction is a difference in scope, not automatically a new method.
- [Zhang etal., Entropy26(8)711, section3](https://www.mdpi.com/1099-4300/26/8/711): parameterize probability distributions using generative networks and gradient-based entropy optimization. A learned parameterization alone would not be new.
- [Singular arrLattice](https://www.singular.uni-kl.de/web/cmd/arr/arrlattice-11552fa8.html), [Macaulay2 intersectionLattice](https://www.macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Posets/html/_intersection__Lattice.html): exact affine intersection enumeration is established.
- [Noodle, arxiv1909.08242](https://arxiv.org/html/1909.08242v1): synthesis of constraint-aware neighborhood operators. Automatically inventing operators alone is not new.
- [FPTaylor](https://dl.acm.org/doi/10.1145/3230733), [Daisy](https://link.springer.com/chapter/10.1007/978-3-319-89960-2_15): symbolic/error-aware rigorous numerical optimization is established.
- [Z3Py primary tutorial](https://ericpony.github.io/z3py-tutorial/advanced-examples.htm): an independent QF_LRA mask enumerator supplies a stronger simple symbolic baseline.

This is a targeted literature review, not an exhaustive novelty clearance. Exa searches returned many irrelevant leads; no mechanism is novel merely because a focused query failed to locate it.

## Independent validation and a stronger control
Run43760186238 resolved all Boolean masks on18 tasks, including both archived C3c laws, with complete agreement between the independent Z3 and geometry implementations. Exact witnesses were directly rechecked. Geometry CPU was .6791sec; SMT CPU was .3607sec. On the actual C3c laws geometry took .3206/.2302sec versus SMT .1361/.1078sec. Individual tiny d2 fixtures favor geometry, so the result is not uniform dominance. This is one timed pass, not a statistical superiority claim.

Nevertheless it rejects a simple efficiency narrative for our custom oracle on the actual target: a standard symbolic solver is a strong, cheaper control here. The new code is useful verification/representation work, not evidence that we invented a better generic solver. [Raw report](results/mask-validation/report.json), [all inputs, statuses and timings](results/mask-validation/validation.json).

## The most promising remaining research question
Can an autonomous system derive **certified, objective-sufficient search representations** from a target's verifier, and refine them only when a checkable counterexample shows they discard useful distinctions?

A genuine contribution would need more than the hand-written projection compiler here. It must differ materially from CEGAR, symbolic expression canonicalization, program synthesis and arrangement enumeration; automatically derive nontrivial target interfaces or reductions; and beat strong exact/symbolic baselines under equal total cost on prospectively chosen task families. The current system does **not** do that. Do not relabel today's implementation as that method.

Before scaling, test the strongest simple alternative and reject the method if advantages disappear when both methods receive the same exact representation. The independent SMT validation is a correctness and strong-control experiment, not yet a test of that future hypothesis.

## Current honest claim
We diagnosed a weak baseline and representation/evaluation blind spots, reproduced a stronger conventional C3c refinement, implemented exact boundary and support-geometry diagnostics, and rejected unsupported novelty/speed claims. We have **not** demonstrated a new general research method, a memory advantage, model-training advantage, or broad transfer. That objective remains open.
