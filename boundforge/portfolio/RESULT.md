# Certified C51a lower-bound refinement

Research and verification date: 2026-11-15 UTC. This campaign found a rigorously certified but extremely small improvement of the Erdős maximum-term constant:

**C51a > 0.58507881967451359.**

The new lower bound exceeds an upper bound on the ACTUAL value of the strongest previous function located in the public-source audit by **more than 1.28 × 10^-17**. It is not merely a tighter enclosure of an unchanged function. It refines previously rounded parameters in the established He–Tang family, yielding a different exact entire function. This is conventional parameter optimization and a minor numerical refinement, not a new general research method or a meaningful-size advance.

Record status: a certified candidate new best lower bound relative to the audited public frontier. No external peer review or formal record recognition is claimed. No paper, researcher contact or leaderboard update has been made.

## Exact witness and analytic dependency

K = 3.56818544223368269553925743732750636848
alpha = 3.96154311181022808045648786109191322475

These decimals are exact rationals, not binary floats. Define
f(z) = sum_(n>=0) exp(i alpha n(n-1)/2) K^(-n(n+1)/2) z^n.
Its coefficients are all nonzero and their nth-root moduli tend to zero, so it is transcendental entire.

[He–Tang Theorem 2.8](https://arxiv.org/html/2602.12217) gives
beta(f)=1/max_theta |2 sum_(n>=0) K^(-T_n) exp(i alpha T_n) cos((2n+1)theta)|,
T_n=n(n+1)/2. The published reduction, not just the numerical checker, connects the certificate to C51a.

[Exact witness](results/2026-11-15/c51-certified/candidate.json).
[Complete report and exact comparisons](results/2026-11-15/c51-certified/report.json).
[Certification specification](C51_CERTIFICATION.md).

## Strongest relevant comparisons

The [July31 working report](https://erdosproblemaday.com/report/513) specifies
K=3.568185442233685, alpha=3.961543111810228 and certifies a lower value exceeding 0.585078819674513546608465623886.
Our independent calculations reproduce that certificate AND prove an upper bound on its actual beta, approximately 0.58507881967451357715792475348655. The new claimed lower bound beats that upper bound. Its search and equioscillation mechanism are prior art and explicitly credited.

[Röhrig PR184](https://github.com/teorth/optimizationproblems/pull/184) is weaker even after tightening its enclosure: actual beta approximately0.58507881967451347702843414544118. [Independent November7 replay](https://github.com/teorth/optimizationproblems/pull/184#issuecomment-6707059155) agrees with our high-precision value. Its headline0.5850788196744 and Tao's0.5850788 are NOT used as the record threshold.

The [final source audit](results/2026-11-15/frontier-final.json) checks every changed-file list in all95 open Tao-table PRs, not only PR titles; onlyPR184 touches51a. It also records primary paper, forum, proof-claims and working-report checks. No stronger applicable public lower witness was located. Direct HTML access to the working report returned403; Exa contents supplied its full report and exact inputs. Its original checker was unavailable; both of our whole-circle algorithms independently reproduce the witness. This is a scoped source audit, not proof that no inaccessible result exists.

## Two complete numerical certificates

Both algorithms truncate atN=12 and add the EXACT uniform tail
2 K^(-91)/(1-K^(-14)).
Odd-frequency symmetries reduce the whole circle to theta in[0,pi/2].

* [Bernstein checker](c51_bernstein.py): real cosine cross-coefficients form the polynomial Q(x), x=cos²(theta); outward interval constants become exact rational upper Bernstein coefficients. Complete rational subdivision covers[0,1]. Candidate:51nodes,26leaves,maxdepth25.
* [Taylor checker](c51_taylor.py): direct trig evaluations of Q=|P|² and Q' at dyadic midpoints plus a global Q'' bound cover theta=(pi/2)y,y in[0,1]. Candidate:487nodes,244leaves,maxdepth30.

These are independently implemented algorithms, written by the same agent. Both share mpmath's interval-arithmetic implementation at100decimal digits; this common trust dependency is explicit. This is not a clean-room human review, Lean proof or independent-team endorsement.

Both also certify the two strongest previous witnesses. Pointwise interval lower bounds on their moduli, minus infinite tails, yield rational upper bounds on their actual beta; the new lower bound strictly exceeds both. Exact fractions are retained in the report.

[Initial certification run](https://github.com/howdymary/boundforge/actions/runs/43687594780).
[Fresh replay after rejection controls](https://github.com/howdymary/boundforge/actions/runs/43687774261).
[16 passing portfolio tests and protected-verifier hashes](https://github.com/howdymary/boundforge/actions/runs/43687775839).
The controls reject a false0.6claim and invalidK=1, and compare the polynomial with the independently evaluated trig identity. C3c protected files retain their original hashes.

## Search history and contribution limits

[All120 constants ranked](TARGET_RANKING.md); lower tiers are preliminary and tied, not fabricated success probabilities. Immutable first ranking and source hashes are preserved.

Completed pilots:616ordinary masks,36weighted-budget starts,453coupled two-coordinate alphabets,6C1b continuation workers,6C1a/C1d continuation workers,3active-knot LP workers,14C59a automorphism starts, C47a fixed-geometry mass optimization, and C51a phase-period pilots.

The C1b translation result improves the reproduced Blob witness by1.8482e-12, but an unreleased rounded SimpleTES claim remains unresolved and the gain is below Arena's1e-7threshold; it is NOT called a world record.

The C51a periodic-phase pilot did NOT pass its preregistered >1e-9gate. Grid optimization initially hid between-grid peaks; using polished maxima corrected this. No periodic-phase advantage emerged. The final precision campaign is explicitly exploratory and below that gate. It does not retroactively make the structural experiment a success.

No new reusable research mechanism, memory advantage, matched-budget controller advantage or broad transfer has been demonstrated. Exa was operationally central: discovering stronger C1b and C51a witnesses changed experiments and acceptance thresholds. This is useful source-aware engineering, not proof of method novelty.

## Resources and stops

Fresh existing-credit snapshots were taken before paid work; immutable caps and older holds remain in campaign-budget.json. Paid work was serialized through a reservation ledger, checking live Modal usage before each reservation.

| Provider | This campaign reserved / unresolved | Interpretation |
|---|---:|---|
| Exa | USD2.15 | Conservative connector allowance; itemized connector receipts unavailable, not asserted actual spend |
| Modal | USD25.80 | Image and bounded-worker holds, not settled invoices; ledger retained |
| Tinker |0 | No new inference/training calls in this continuation |
| past.dev |0 | No new memory calls in this continuation |

Older unresolved holds remain separate: Exa0.31, Modal89.78, Tinker3.20, past90credits. No holds are silently released. Other projects' consumption is not attributed to this campaign. No purchases, upgrades or auto-reloads. Modal requested15one-CPU workers,12with2GiB and3with3GiB; sum of worker time limits5580CPU-seconds, noGPU. GitHub hosted runners performed the inexpensive algebra/certification pilots separately. Exact elapsed times, limits and failures are in artifacts and reports.

A strict mathematical refinement has been certified against the strongest accessible prior function found. The gain is extremely small; it is not a strong Track1 novelty story. Record-size and framework-novelty judging remain weak. Stop paid escalation here rather than spend more on failed neighborhoods.

## Replay

Run from repository root in a remote checkout with mpmath1.3.0:

python -I boundforge/portfolio/c51_bernstein.py boundforge/portfolio/results/2026-11-15/c51-certified/candidate.json
python -I boundforge/portfolio/c51_taylor.py boundforge/portfolio/results/2026-11-15/c51-certified/candidate.json

For all prior comparisons, run boundforge/portfolio/c51_certify.py. The manual portfolio-c51certify.yml and portfolio-verify.yml workflows reproduce the checks without billable providers. Source commits, artifact/member hashes and exact inputs are retained under results/2026-11-15.
