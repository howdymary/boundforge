# Critical review of two model suggestions

Run [43747146303](https://github.com/howdymary/boundforge/actions/runs/43747146303), Qwen/Qwen3.5-397B-A17B. Two calls, 2,836 input and 2,738 output tokens combined; estimated USD 0.0252144, with USD 0.20 still held pending receipts. No training or generated-code execution.

## Suggestion 0: obstruction contrast

Rejected as specified. A bounded depth-2 failure trace is not an exact obstruction or unsatisfiability certificate. The suggested avoidance score and action choice are undefined. Its novelty claim overlooks no-good learning, explanation-guided LNS and subproblem dominance. Its quantitative speed/pruning predictions have no evidence.

The suggested independent-set target of size 50 in G(100,1/2) is also a poor performance test: the expected number of such sets is C(100,50)2^-1225 < 2^-1125. A union bound gives the same upper bound on existence probability. A random graph almost certainly lacks the requested object. This is not proof about any specific generated graph, but it invalidates the model's unqualified proposed target.

No experiments were scaled on the strength of these statements.

## Suggestion 1: paired order feedback

Accepted only as an exploratory, precisely implemented hypothesis. The second output hit its 1,500-token cap and is truncated; it is retained as unverified text, not counted as a schema-valid program.

Corrected unsupported claims before implementation:
- Ordered-pair methods do not need exponentially many sequences to compare all length-2 pairs: six actions have 30 ordered distinct pairs. Ordered-pair UCB is an explicit control.
- Learning useful enabling sequences and conditioning on success/failure are prior art, including CMCS and subsequence hyperheuristics.
- The same initial state alone does not remove stochastic effects. The implementation couples each action's random seed across both orders. Common random numbers can reduce variance but are not guaranteed to do so.
- One observed order difference is not a statistically established cause or a proof of future usefulness. Prediction logs count repeated nonzero contrasts and disclose sample counts.
- Retaining a better probe construction is extra search, not evidence that the orientation estimator helps. Paired controls retain the same available intermediate constructions and pay all four batch executions.

The tested distinction is a narrow online crossover estimator versus observational sequence credit, absolute pair rewards and shuffled contrast signs. Whether it helps, transfers, or is materially new remains unresolved before results. The frozen protocol is [ORDER_PROTOCOL.md](ORDER_PROTOCOL.md).

The code is implemented by the research agent from this corrected specification; model-generated Python is not executed. No description in this file licenses a novelty or performance claim.


## Further source-informed proposal call (run43751783535)
The response is not an executable or accepted mechanism. Parsing failed due to trailing special-token text; the raw JSON also repeats an id key and combines two proposed hypotheses in one object. Preserve the raw output rather than silently repairing it into a valid proposal.

Substantive rejection:
- H1 proposes a minimum hitting-set repair that the existing exact circuit baseline already performs within size two. Minimal repairs are not necessarily unique, and deleting multiple rows is not a single pivot.
- H2 confuses increasing a projection's entropy with our objective, which minimizes maximum control entropy. Neutral basis rewrites preserve every collision partition, so their intermediate objective cannot differ. The stated equal-operation comparison ignores scoring overhead.
- H3 proposes ordinary incremental linear algebra. Exact finite-field computation has no floating-point numerical instability; any rank mismatch would indicate a software/proof error. No new general method is established.
- Some named references in the model answer lack supplied source URLs; treat them as unverified leads, not citations.

The useful next question comes from direct mathematical analysis of repeated elimination, not accepting these proposals: can shared residual/coordinate tables evaluate all repairs exactly at lower cost? See collision/BATCH_REPAIR_PROTOCOL.md. The Distinct Vectors and dynamic/batch linear-algebra literature substantially limits any novelty claim.
