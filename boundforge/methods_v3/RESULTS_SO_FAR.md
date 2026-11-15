# Method investigation: evidence through the first two pilots

Research date: November 15, 2026 (America/Los_Angeles). The collision-representation pilot is still in progress when this note is written. **No new general research method or new mathematical record is established by this campaign so far.** Earlier submission claims and certificates are unchanged.

## Scalar probing: stop scaling

[324 raw verified episodes](results/scalar-probes/episodes.json), [report](results/scalar-probes/report.json), [protocol](PILOT_PROTOCOL.md). Nine development configurations, three seeds, twelve policies, about 325.39 process CPU seconds. Each episode's retained construction was checked from its mathematical definition. CPU ranged from 0.9953 to 1.0291 seconds including final verification; this is bounded approximate equalization, not exact hardware-time identity.

Measured probe selection versus its same-probe/random-exploitation control gives paired differences [0,0,0] on cap4, deletion8, deletion9, deletion10 and the first graph; [-1,0,0] on cap5; [2,2,0] on cap6; [0,0,-1] on the second graph; [-1,0,1] on the third graph. The positive cap6 example is not robust cross-task support and still trails fixed small-ruin search (80 versus78.67 mean members). Cap4 and deletion8 are ceiling-limited. Three seeds are dependent repetitions, not three independent mathematical problems. No significance claim.

This fails the practical gate for scaling scalar probing or training a controller on these outcomes.

## Paired-order feedback: informative diagnoses, no useful new controller

[180 development episodes](results/paired-order/development.json), [140 validation episodes](results/paired-order/validation.json), [report](results/paired-order/report.json), [protocol](ORDER_PROTOCOL.md). Development used about27.42 CPU seconds; validation about283.30. All retained constructions pass independent definition checks. The tuned fixed sequence is anchor2 followed by ruin50; it was selected on development only.

| Validation configuration | Paired order | Same paired absolute reward | Shuffled order credit | Stronger ordinary control |
|---|---:|---:|---:|---|
| graph224,p=.10 |40.6|40.6|40.8|ε-greedy41.8|
| graph288,p=.06 |64.4|64.4|64.2|conditional65.8|
| cap5 |38.8|38.8|38.8|pair-UCB39.4|
| deletion10 |13.4|13.4|13.4|conditional13.4|

These are means of five starts on each configuration. Do not pool their different objectives or call them problem-level confidence intervals.

The paired-order arm records175 enabling observations. Of979 nonzero repeated order predictions,622 agree with the next observed contrast. These are dependent observations under adaptive state selection, not an independently validated accuracy estimate. They show why a plausible diagnostic can still fail to improve end-to-end search.

### Algebraic rejection of the claimed credit-rule distinction

Let b=f(S), and let M_AB and M_BA include every intermediate state and S itself. Then both M values are >=b. The signed contrast is D=M_AB-M_BA. Ordinary nonnegative paired rewards are g_AB=M_AB-b and g_BA=M_BA-b. Therefore D=g_AB-g_BA, and accumulating signed contrasts produces exactly the same orientation ordering as accumulating the two absolute rewards. Pair selection also uses the same absolute means in both implementations. With identical primitive counts, states and random seeds, these two policies are the same rule; differences under CPU stopping can only reflect timing. Their final objective values match on all20 paired validation starts.

This identity was noticed before opening the order report. It rejects a novelty claim for the proposed credit rule. Sequence learning itself is prior art. Stop scaling this direction; do not use the existence of enabling observations or model endorsement as evidence of a new method.

## Next hypothesis: change representation after exact failure

[Specification](collision/SPECIFICATION.md). The next experiment changes what is searched: feasible projection-collision flats, with exact protected-target separation. It uses a complete small-deletion obstruction to decide whether to change an equivalent basis before attempting another construction move. Random edits in the same representation, direct circuit repair, random basis changes and shuffled diagnostics are controls. Exact rank/circuit/embedding tests passed before any Modal experiment.

The mathematical ingredients are established. The testable potential distinction is failure-guided basis selection for future moves under an objective invariant to the current basis. A positive development result would still require prior-art assessment, prospective evaluation and transfer. A new algorithm label alone does not establish novelty.

## Sources, models and memory

[Prior-art table](PRIOR_ART.md), [model critique](HYPOTHESIS_REVIEW.md), [research decisions](decisions.jsonl), [artifact manifest](results/manifest.json). Eight initial Exa queries cost USD0.056 by receipts. Two Tinker hypothesis calls estimate USD0.0252144 with USD0.20 held, not settled. A past.dev negative-findings ingestion is pending in the first archived receipt; no successful recall is inferred. New Modal work is bounded and ongoing; final usage/holds will be reported after completion. No training or GPU use is justified yet.

The user subsequently instructed no further credit-availability checks. New operations use the last recorded provider caps and retain reservations without calling balance/usage endpoints. No purchases or billing changes occur. Single-agent hosted memory use is not a multi-agent sponsor claim.

No external submission, researcher contact or leaderboard update was made.


## Collision-flat development (2026-11-15)
Initial run43749707802:162 outputs checked by two independent arithmetic backends;195.62 worker CPU seconds. Guided pivots never exceeded direct circuit per-task means. Do not mistake an enabled one-row repair for useful search improvement.

Stronger controls: run43751582408 produced270 checked outputs but lost raw artifacts due to a workflow path error; only its log summary survives. See collision/ARTIFACT_INCIDENT.md. The corrected repeat43752081276 retained all270 outputs/traces and passed both checkers,407.02 worker CPU seconds and182.04 wall seconds. Guided pivots lost to circuit repair on four of six task means and tied on two. They were never the best procedure. The exact representation often outperformed this coordinate baseline, but that observation does not establish a new general method or superiority over all coordinate search.

Shared-library UCB and random controllers had access to the proposed guided operator. No controller advantage emerged. Stop scaling unchanged guided pivots. No confirmatory held-out evaluation is justified by these results.

past.dev completed ingestion and recalled our own source record. Its extraction also converted a scoped negative recommendation into a standing “forbidden” rule. Treat this as evidence to interpret with original scope, not authoritative instructions or a mathematical impossibility. Memory functionality is established; causal memory advantage and multi-agent sponsor compliance are not.

Next development hypothesis: share exact algebra across a whole repair family, compare every counterfactual with naive rebuilding, and separately test end-to-end benefit. Current mathematical/new-method claims remain unchanged: no new method established by this campaign.
