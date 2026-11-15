# C49a campaign assessment

Research date: November 14, 2026, America/Los_Angeles; runs and collection November 15 UTC.

**No new C49a lower bound and no demonstrated new general research method.** The strongest retained result is an independent reproduction of a prior open claim, not a BoundForge record. The hypotheses were tested rather than declared successful.

## Frontier and certification

The reproduced incumbent is [PR370](https://github.com/teorth/optimizationproblems/pull/370), pinned to [Pinho's certificate packet](https://github.com/rpinho/math-certificates/tree/a50021b04687719f4a2ea27609029982c980573e/c49/round1). Its rate is
(64728+sqrt(3019700660))^(1/26) = 1.567864384572806979362033445047060687289228710864066381805835...
on a 252,303-member Sperner sunflower-free family on 28 points with ports 0 and 1. Port counts are [33980,64728,64728,88867]. The weaker merged Koshta table value is 1.56785990242458988585...; beating that alone would not establish a new record.

StageA replayed both primary checkers and our BDD implementation. Final certification freshly executes our own Cartesian-box and BDD implementations, agrees on all counts, checks every required finite property and isolates the rate using exact rationals. These independently implemented algorithms were written after reading primary sources, not claimed clean-room. See [certification](results/certification.json), [exact baseline](results/baseline.json), [frontier audit](results/stage_a/frontier.json), [refresh](results/frontier-refresh.json), [source hashes](results/stage_a/sources.json), and [proof/specification](RESEARCH_DESIGN.md). The original 1997 publisher typeset proof was inaccessible; operative complete gluing proofs in Koshta/Pinho were inspected. Prior authors retain credit.

An accessible witness is not proof no newer unpublished claim exists. The frontier audit distinguishes merged entry, open claim, and independently reproduced witness. No external leaderboard was updated.

## Experiment outcomes

The development pilot used 24 saved-state/seed comparisons: a common 250 ms probe followed by six paired 250 ms interventions, 42 CPU seconds total. F10 remained flat. Uniform8 favored removal of six sets and conflict-guided repair. Two families and their deletions do not provide a broad learning distribution.

The frozen primary study used 245 episodes, seven arms, five held-out tasks and seven paired starts per task. Each arm had the same six operators and 6.25 CPU seconds per episode, including warmup. Tinker was disabled at freeze by its failed billing probe; the full arm therefore used the frozen **numerical fallback**, not a model-written policy. Archived trace wording saying "model rule" is a labeling limitation.

| Task | Fixed | Scheduled | Global UCB | No memory | Full | Numerical | Shuffled |
|---|---:|---:|---:|---:|---:|---:|---:|
|H11|1.566153938|1.566153938|1.566153938|1.566153938|1.566153938|1.566153938|1.566153938|
|uniform9|1.509916649|1.553110163|1.541239554|1.516350503|1.548707008|1.553110163|1.529646708|
|MIS64-a|16|16|16|16|16|16|16|
|MIS64-b|17|17|17|17|17|17|17|
|cap4|20|20|20|20|20|20|20|

On uniform9, full improves over the development-selected fixed procedure, but scheduled switching and numerical contextual selection both do better. Four other primary tasks have identical final results across all arms, so those ceiling results are uninformative about relative discovery quality. This does not establish diagnostic or memory superiority. Seven starts are dependent repetitions on a single family, not seven independent mathematical tasks.

A separately registered **post-hoc** harder auxiliary follow-up kept controller/engine hashes unchanged. It is a ceiling diagnostic, not a replacement of the primary study or evidence the original benchmark was adequate.

| Task | Fixed | Scheduled | Global UCB | No memory | Full | Numerical | Shuffled |
|---|---:|---:|---:|---:|---:|---:|---:|
|MIS128-a|21|21|21|21|21|21|21|
|MIS128-b|21|21|21|21|21|21|21|
|cap5|45|44.28571429|45|45|43.28571429|43.71428571|44.28571429|

On cap5, the full arm averaged 43.2857 members versus 45 for fixed search, global UCB and the no-memory arm. Both larger graph tasks again tied. This follow-up gives no support for scaling the full policy.

Raw episodes, exact checks, per-phase resource summaries and paired differences are in [primary results](results/evaluation/report.json) and [follow-up results](results/transfer/report.json). Paired bootstrap ranges resample starts only; no problem-level confidence or multiplicity-adjusted significance is claimed. Different task objectives are never pooled into one score.

Four later Tinker proposals were tested only on development data: two failed the strict integer-action schema and two were valid. Their expected rewards (0.0077916315 and 0.0075969703) were below the numerical rule (0.0083885031). No fine-tuning was justified or run. The model study neither repairs nor changes frozen held-out results.

Production switched from stalled greedy repair to classical CP-SAT whole-family search, with exact containment constraints, valid separated sunflower clauses and sufficient rational Collatz inequalities. Six bounded configurations covered n=10/n=11 and different Perron-vector ratios. No valid above-threshold candidates were found; none improved the incumbent. Solver UNKNOWN/timeouts are unsuccessful finite-budget attempts, not impossibility proofs. Any infeasible status has only its stated ratio restriction and no independently checked UNSAT certificate. Details: [production](results/production/report.json).

A separate free periodic-gluing search enumerated 956 ordered port choices, deduplicated 26 matrices, tested all matrix pairs and a width-256 beam through period 8. Exact comparison of the leading screened candidates found no record. The common-positive-vector hypothesis failed 754 matrix-wise tests: it proves no exclusion and is retained as a failed diagnostic. Neither bounded beam search nor failed sampling rules out other compositions.

## Diagnostics, memory and limits

Measured rejection counts, exact state hashes, action choices, budgets, conflict examples and observed objectives support inspectable decision chains. [Memory examples](results/memory-decision-chains.json) link aggregate archive reads to changed actions and measured consequences. They do not establish a causal memory benefit. Development paired probes are the actual same-state intervention tests. A separately labeled [post-hoc leave-state-out diagnostic check](results/posthoc-diagnostic.json) had mean normalized reward 0.007597 versus 0.007198 for unconditional action choice. All of that small difference came from one of 24 rows; only three labels appeared (19 pair, 3 repeat, 2 mismatch). This is not robust evidence that diagnoses predict intervention efficacy, and it did not alter the frozen policies. Hosted past.dev source retrieval was asymmetric; a later role retrieved a controller record. No hosted-memory performance advantage is claimed. These were sequential orchestration roles, not independently spawned agents; past.dev multi-agent sponsor eligibility is not asserted.

Limitations: small development distribution; weak differentiation on ceiling tasks; coarse heuristic diagnosis labels; mismatch labels in episode logs lack their raw counter (pilot records retain it); no complete isomorphism reduction; no literal neighborhood-exhaustion certificate; per-family port counts for all intermediate states are not retained; fixed-controller selection is development-best, not globally strongest possible search. CPU equalization does not equal end-to-end inference cost. Final task adapters and several action heuristics are human designed.

The full controller is contextual UCB with a tiny ranking bias and aggregate rewards. That is close to adaptive operator selection/ALNS, not a newly discovered general method. [Novelty table](RESEARCH_DESIGN.md) and [memory prior art](PRIOR_ART_ADDENDUM.md) identify the overlap with Ropke/Pisinger, Fialho, Kotthoff, FunSearch, AlphaEvolve, PatternBoost, Reflexion and Voyager. The comparison fails to establish the intended advantage; additional terminology would not change that result.

## Resources, credit accounting and stopping

- exa: 0.063 USD campaign actual-or-reserved; 0 unresolved; historical hold 0.31 separate.
- modal: 37.68 USD campaign actual-or-reserved; 37.68 unresolved; historical hold 52.1 separate.
- tinker: 0.8 USD campaign actual-or-reserved; 0.8 unresolved; historical hold 2.4 separate.
- past: 12.0 credits campaign actual-or-reserved; 0 unresolved; historical hold 78 separate.

These are conservative ledger amounts, **not all final charges**. Exa receipts total 0.063 USD; Tinker token estimates total 0.0185256 USD within 0.80 USD held for four calls; Modal actual metered invoice is unresolved. past usage entries are reported in credits with API estimation caveats. Old holds and external-project guards remain separate. See [provider records](results/provider-usage.json), [resource summary](results/resource-summary.json), and the initial [billing snapshot](campaign-budget.json). No GPUs or training were needed. Search 'tested' counters count single-point insertion legality checks, not full-family evaluations; CP-SAT and final certification are reported separately.

Exa used a recent manual dashboard balance snapshot and conservative guards rather than a live balance API for every query. This is a limitation of per-call freshness, and future calls need another dashboard check. Modal, Tinker and past checked available billing/usage interfaces at reservation time; provider-specific accounting assumptions and unresolved holds remain explicit.

The paid ledger was serialized across pilot, freeze, held-out evaluation, model component, production and follow-up. Unknown charges remain held; there were no purchases, auto-replenishment changes or upgrades. Final independent certification used GitHub Actions, outside paid provider experiments. No unsupported large batch is launched merely because credits remain.

The preregistered greedy direction stalled; controlled evaluation did not support scaling the full controller; bounded new-family CP-SAT and periodic compositions did not improve the record. Those tested directions stop here. This is a scoped negative campaign, not a proof the mathematical target is exhausted. A new campaign requires a materially different mathematical construction or a better discriminating benchmark, fresh budgets and a new freeze.

## Six separate contribution answers

1. **What mathematical result is new?** No improved C49a bound. The retained 1.56786438457... witness and gluing theorem are prior art. No new exclusion theorem was proved.
2. **What research mechanism is new?** None established relative to adaptive operator selection and agent-memory prior art. The concrete artifact is an adaptation with structured diagnostics and independent acceptance.
3. **What evidence shows it helps?** Full beats a weak development-selected fixed baseline on uniform9, but not scheduled/numerical controls. That does not establish the central hypothesis. The later model rules do worse on development.
4. **Where does it transfer or fail?** The same controller executes on independent sets and cap sets using human-designed adapters; raw follow-up results are above. Execution transfer does not establish a general performance benefit. C49 F/H constructions and most primary auxiliary instances stall.
5. **What remains standard engineering, adaptation or conjecture?** Exact verification, gluing/Perron analysis, CP-SAT separation, ALNS-like ruin/repair, contextual UCB, provider integrations and logging are standard methods or engineering adaptations. Reusable diagnosis-driven discovery advantage remains conjectural and unsupported here.
6. **Which Track1 criteria are met?** An autonomous bounded propose/evaluate/update loop and inspectable logs exist. **The record-beating objective is not met.** A new general research method has not been demonstrated. This is not ready to present as a winning or publishable mathematical advance.

Reproduction requires no paid service: run the remote C49 publication/check workflow or follow [the C49 guide](README.md). The [offline actual-artifact demo](results/demo.html) replays recorded outcomes; it does not run fresh inference or claim a simulated record.
