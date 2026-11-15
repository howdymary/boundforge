# Continue BoundForge toward Track 1

You are my computational mathematics collaborator and research engineer. Work in https://github.com/howdymary/boundforge on main. Read AGENTS.md, README.md, MIGRATION.md, and the existing research review, preregistration, final note, exact certificates, and traces before changing code. Develop through GitHub and remote execution; do not create local project files. BoundForge is independent of Compute Observatory.

## Objective and acceptance criteria

Build and execute an autonomous research system that chooses hypotheses, runs bounded experiments, interprets measured results, and chooses subsequent experiments until it produces a rigorously certified improvement over the strongest current relevant mathematical record, or reaches a genuine resource or methodological stopping condition.

C3c is the archived starting target; the user has now requested alternatives because its latest campaign stalled. Read TARGET_SELECTION.md. Prioritize a bounded feasibility pilot for C49a (3-sunflower-free capacity), with C1d (signed autoconvolution) as a backup. Recheck current primary sources and open submissions before committing to a target. You may select between these candidates based on preregistered pilot evidence; explain the decision before scaling. Ask before changing to a different mathematical problem. Track 1 welcomes improved known bounds. Judge success on (1) certified distance past the prior record, (2) demonstrated originality/value of the research loop, and (3) decision-by-decision inspectability. Do not promise a result or run indefinitely just because a record remains unbeaten.

Before claiming Track 1 success, establish:
- the exact problem definition and comparison witness, checked against current primary sources;
- a fresh run whose accepted result is reproducible from a frozen start and configuration;
- both independent interval checkers certify candidate lower endpoint > comparison upper endpoint;
- an auditable autonomous chain from initial sources and observations to the successful candidate;
- a precise disclosure of all mathematical scaffolding, hypotheses, interventions, and manual choices supplied by humans;
- the size and substance of the improvement, separately from any methodological contribution.

Never count a rounded leaderboard value as the full-precision record. Distinguish beating the published witness from beating our own best certificate. Replaying an already known improvement does not establish a new discovery.

## Starting evidence

The retained certificate refines Jaswal's published construction by about 2.21 × 10^-22, mostly removing digit-count rounding loss. The first 15 digits do not change. Two protected exact checkers validate it. This is a real certified refinement, not evidence of a substantial new construction or publication readiness.

The research-led campaign executed 174 support/start cases. Its original free-energy optimizer often collapsed to point masses, where F=0 is uninformative. An exploratory paired entropy-floor correction prevented collapse in all 87 saved support/start cases, but no positive separator or stronger certificate emerged. Six actual Tinker construction-program proposals yielded five parseable programs; no model advantage was established. No fine-tuning was justified.

Do not restart this narrow grammar at larger scale without a new reason. Use its failed cases, but do not interpret them as a proof of global impossibility. The graph restriction and entropy floor are search restrictions, not proved mathematical reductions.

## First: audit the frontier and choose a falsifiable direction

Use Exa to verify the current C3c frontier and read original papers, constructions, evaluators, and official repositories. Update the existing comparison of FunSearch, AlphaEvolve, PatternBoost, classical optimization, and direct entropy/Kakeya methods. Discover any newer relevant work. Cite primary sources and dates, distinguish author claims from our reproductions, and do not call a known method novel.

For C3c inspect representation, objective conditioning, optimizer failures, projection collisions, complementary laws, and the finite-bank LP. For C49a inspect exact sunflower/Sperner constraints, port-conditioned counts, the published gluing hypotheses and transfer-matrix rate; do not equate larger family size with a better asymptotic bound. For C1d preserve the signed absolute-convolution objective and check every lag exactly. Rank at least three genuinely different directions. Candidates include broader support geometries, coordinated structural exchanges, dual-guided law discovery, adaptive probability optimization, and model-generated bounded search procedures. Justify the representation and any symmetry/reduction mathematically. Do not assume any one direction will work.

For each direction state:
- the mathematical mechanism and why it could exceed the retained witness;
- the smallest diagnostic that could falsify it;
- exact baseline, seeds, time/evaluation budget, and success/failure thresholds;
- how promising numerical outputs become exact certificates;
- how the autonomous controller will change direction after evidence of failure.

A positive score for one numerical dual is not by itself a bound improvement; dual degeneracy can matter. A finite-bank LP dual is not a universal entropy inequality.

## Make the framework contribution testable

Choose one primary methodological hypothesis before scaling. A promising candidate is *failure-aware selection between search neighborhoods*, but validate whether it is useful and new rather than adopting it as branding.

A failure record should include the precise support/candidate hash, representation, neighborhood, optimizer, seeds, budget, termination status, numerical conditioning, projection changes, and verification outcome. Distinguish invalid candidates, numerical failures, exhausted certified finite neighborhoods, and merely unsuccessful sampled attempts. Never generalize a failed sample into an impossibility claim.

An autonomous controller should use these records to decide whether to refine, diversify, coordinate changes, change representations, or stop. Demonstrate actual read -> decision change -> measured consequence. Replaying a memory entry or adding past.dev alone is not evidence of improvement.

Compare the proposed controller against strong fixed, random, numerical-only, and no-memory/no-adaptation baselines. Use matched candidate-evaluation or compute budgets; report model inference and other overhead separately. Freeze comparisons before held-out starts, include unsuccessful runs, and avoid selection on reported evaluation outcomes. Multiple starts on one constant are not independent mathematical problems. A small number of samples does not establish generality.

Multi-objective search is optional: retain an explicit Pareto archive over certified bound, evaluation cost, support/encoding complexity, and structural novelty if those dimensions guide useful decisions. The mathematical acceptance objective stays the chosen constant. Easier verification or prettier supports cannot substitute for beating the bound. Compare any complexity objective with bound-only search.

Do not invent a novelty claim to satisfy the track. For each proposed contribution maintain: prior art, precise difference, experiment or proof, observed effect, and claim scope. Failure-aware memory, evolutionary program search, adaptive neighborhoods, and multi-objective optimization all have prior art. A new combination may be engineering; demonstrate a useful mechanism before calling it a research advance.

## Implement and run, do not stop at planning

Complete a short direction memo, freeze a bounded pilot, implement the selected approach, and run it. Checkpoint every batch remotely and keep an append-only decision trace:
source -> hypothesis -> expected observation -> experiment -> measured result -> verification -> next action.

Scale only after pilots establish useful signal. Allocate Modal to parallel deterministic evaluation/verification and Tinker to the role supported by evidence: construction/search-program generation, experiment selection, or interpretation. Generated code must run in bounded, isolated workers with no credentials and no access to protected verifiers. Exa must be used inside the main research loop when a research question changes the next experiment, not just for initial decoration. Use past.dev across distinct research roles when useful; measure benefit separately from integration.

Fine-tune only after enough diverse verified data exists, the objective is explicit, and a defensible train/evaluation separation is preregistered. Do not train to consume credits. Do not claim autonomous mathematical insight when a human supplied the decisive construction family after observing results.

After each batch explain what changed, what failed, why the next experiment is justified, and whether a meaningful contribution remains plausible. Continue through justified methodological changes. Stop repeating a stalled family; do not silently pivot targets.

## Verification and budgets

Keep the archived C3c verify.py and verify_independent.py byte-for-byte unchanged unless a separately documented correctness bug requires an independently reviewed repair. For a new constant, add target-specific checkers in a separate directory; do not repurpose or weaken the C3c verifiers. Record their hashes. Every retained improvement needs exact integer/rational data and two independently implemented target-specific checks in fresh processes. C3c additionally needs positivity, normalization, projection aggregation, valid independent-digit encoding and rigorous entropy enclosures. C49a needs exact finite-family validity and the hypotheses/proof transferring the block to the claimed asymptotic rate, with certified algebraic comparisons. C1d needs the correct signed objective, nonzero integral, all-lag exact convolution and exact rational record comparison. Keep proposal generation separate from acceptance.

Use existing provider credits only. Before paid work verify current Exa, Modal, Tinker, and past.dev balances and billing boundaries; snapshots in the archive are historical. Establish separate initial campaign caps and preserve unresolved prior holds and pending jobs. Recheck account-wide usage including other projects. Reserve worst-case simultaneous work and final certification; unknown costs remain reserved. No purchases, auto-reload, upgrades, or charges beyond credits. Disable a provider when its boundary is unknown and continue independent work. Existing credits authorize useful research, not waste.

## Deliverables and honest stopping

Deliver code, frozen configurations, all seeds and failures, full decision logs, exact witnesses, independent checks, source/provenance hashes, resource accounting, baselines/ablations, an actual-artifact demo, and a claim-by-claim novelty/evidence table.

Write a concise Track 1 assessment separating:
1. a mathematical record or certified bound refinement;
2. an experimentally demonstrated framework improvement;
3. standard methods adapted or combined;
4. engineering integrations;
5. conjectures and unproven ideas.

If we beat a record, continue enough to independently certify it, replay the discovery, quantify its magnitude, and assess the decisive mechanism. If the gain is tiny, say so. If no meaningful improvement emerges, deliver the strongest verified result and a reproducible negative study. Do not manufacture success, weaken a verifier, or guarantee publication. Do not submit a paper, contact researchers, or update a leaderboard without explicit authorization.
