# C49a research design and novelty assessment

Research date: November14,2026 America/Los_Angeles. Baseline replay run43678845982 passed three exact finite checks and independent rational isolation. Exact baseline rate (64728+sqrt(3019700660))^(1/26), not the weaker merged table value. This is prior art: R.Pinho and collaborators, [PR370](https://github.com/teorth/optimizationproblems/pull/370). The source packet claims no improving exchange through seven deletions of this witness. We do not treat unexecuted exclusion claims as our own proof.

## Mathematical specification and proof used

A finite family is represented by distinct integer bitmasks. Sperner means no strict containment. A sunflower means three distinct masks with equal pairwise AND. The capacity definition does not require Sperner; our chain construction does.

For disjoint valid Sperner sunflower-free families A,B and ports a,b, glue only pairs with opposite port membership, delete both ports, and take the disjoint union of the remaining sets. Equal membership in a containment restores inclusions in both original families. Unequal membership restores a strict inclusion in one of them. Thus Sperner gives injectivity and no proper containment. For an equal-intersection triple, if exactly one a-bit is1, restoration preserves equal intersections in A, forcing three identical A members with unequal bits, a contradiction; with two1s use the complementary b-bits. If all bits agree, restore both factors, whose equal-intersection triples must be constant. Therefore no distinct glued sunflower exists.

This restates the DEGKM1997 Lemma4.4 mechanism, not a new theorem. We read the complete operative argument in the pinned [Koshta proof](https://github.com/DennisKoshta/sunflower3-49a-certificate/blob/c4ee81737f9f6a4ae9793586a27004553a12d5c0/PROOF.md) and [Pinho proof](https://github.com/rpinho/math-certificates/blob/a50021b04687719f4a2ea27609029982c980573e/c49/round1/PROOF.md). The original1997 typeset paper was not accessible in this audit (publisher403); no claim of directly inspecting that typeset lemma.

With two distinct surviving ports, counts N00,N01,N10,N11 give T=[[N10,N11],[N00,N01]]. For positive counts, gluing repeats multiply the positive row vector by T. A positive Perron eigenvector gives family size >=c*rho(T)^k on k(n-2)+2 points. Hence capacity>=rho(T)^(1/(n-2)). Products of compatible blocks use the product matrix and summed exponents. Rational isolation compares algebraic rates; raw family size and float ranking do not certify an improvement.

The exact BDD checker counts all ordered containments P and all equal-intersection triples Q allowing repetitions. A valid M-member Sperner sunflower-free family has P=Q=M. Conversely these equalities rule out every proper containment and distinct sunflower. Tuple counts fit uint64 for M<=300000. Literal enumeration and adversarial controls test the implementation separately.

## Prior art and proposed difference

| Mechanism | Closest primary prior art | Precise difference tested here | Required evidence |
|---|---|---|---|
| Multiple ruin/recreate moves and historic reward adaptation | [Ropke–Pisinger2006](https://pubsonline.informs.org/doi/10.1287/trsc.1050.0135) | None claimed for ALNS itself | Strong fixed and adaptive baselines |
| UCB operator allocation and fitness/diversity feedback | [Fialho thesis](https://groups.csail.mit.edu/EVO-DesignOpt/pb/uploads/Site/FialhoThesisDraft.pdf), dynamic MAB/AOS | Context is an explicitly measured failure diagnosis; this is still within contextual algorithm selection prior art | Global-UCB versus contextual-memory ablation |
| Instance-conditioned algorithm selection | [Kotthoff2014](https://doi.org/10.1609/aimag.v35i3.2460) | Paired saved-state interventions as an auditable action-effect archive for exact construction search | Held-out prediction usefulness, not just correlations |
| Local/global training and generated seeds | [PatternBoost](https://arxiv.org/html/2411.00566v1) | No new training algorithm; training deferred | Diverse data gate; no decorative SFT |
| Model-generated programs and deterministic evaluators | [FunSearch](https://www.nature.com/articles/s41586-023-06924-6), [AlphaEvolve](https://arxiv.org/html/2511.02864v3) | Restricted model-written diagnosis/action rankings, not unrestricted program evolution | Model-prior versus numerical-only contextual controller |
| Exact rejection-witness memory | Constraint/nogood learning; CP/SAT and adaptive search | Evidence scopes retained; no sampled failure labeled impossible | Actual memory-read -> choice change -> outcome trace |
| New C49a construction | DEGKM, IRSI, Claude F/H, Sylla, Koshta, Pinho | Search new small base families and coordinated exchanges, not replay21-to32 augmentation | New exactly checked family and rigorous rate above latest baseline |

**Novelty assessment:** No new general algorithm is established at design time. The central hypothesis is already closely related to ALNS, contextual selection and experience-based search. Candidate contribution is a carefully evaluated adaptation and diagnostic benchmark; a general-method claim requires a concrete performance/transfer mechanism that survives ablations. A successful implementation or API integration alone does not establish novelty.

Exa performed six discovery queries (actual costUSD0.042); full primary texts are transient, URL/hash metadata retained. Some searches yielded irrelevant results; no absence-of-prior-art claim follows.

## Architecture

Task adapter -> bounded worker -> measured diagnostics -> contextual action archive -> controller -> next worker.
Exact verifier and algebraic comparison remain outside this proposal path. Worker receives no provider keys or verifier access.

The pilot uses six common actions: remove2, remove6, large ruin, restart, rejection-conflict-guided ruin, and objective/structure-targeted ruin. Greedy repair is shared. C49 scores the best positive-count port pair by transfer rate; this is a proposal score until exact certification. Auxiliary independent-set and cap-set tasks use cardinality and independent exact validity checks. The same controller consumes task-independent diagnosis labels, with all task-specific validity/score adapters disclosed.

Diagnostics: measured constraint rejection, objective/cardinality mismatch, exact repeated state, sampled stagnation, progress, timeout. A failed sampled neighborhood is never called exhausted. We do not claim isomorphism merely from a repeated invariant.

## Bounded pilot, frozen before implementation

Development C49 tasks: published75-set F on10 points and a seeded uniform-family construction on8 points. Development uses paired saved states; all six actions get the same seed and CPU allowance. Pilot8 paired states, three repeated seeds,250ms processCPU/action. Use variation in paired results to choose evaluation repetition count before held-out results.

Candidate ranking rules: up to four Tinker proposals, each a bounded JSON ordering of the same six actions for each diagnosis. No generated Python executes. Select using development outcomes only, then freeze. Model outputs are hypotheses, not proofs. No fine-tuning: no sufficient diverse archive.

Planned comparison arms: best fixed action selected on development, scheduled switching, global numerical UCB, diagnosis rules without persistent memory, full contextual memory, numerical contextual memory without model rules, and shuffled-context memory. Equal workerCPU quanta, identical libraries and initial states. Model inference and archive-building overhead reported separately; additionally report end-to-end costs. A pilot may justify dropping unsupported components, with amendment committed before held-out outcomes.

Held-out C49 family H on11 points and a seeded9-point family differ from development starts. Transfer tasks: cap sets in F3^4 and independent sets on two separately seeded64-vertex graphs. They test out-of-domain use of a controller trained only on C49. They do not establish generality beyond these adapters. No record claim on auxiliary tasks.

Production record search is separate from held-out evaluation. Use larger bounded batches only if new structural diversity or objective movement justifies them. Stop if none appears after the preregistered pilots and one justified methodological correction.

## Budget and resource controls

Fresh snapshot in campaign-budget.json. Initial caps are immutable; no purchases, upgrades, reloads. Preserve old holds and a conservative external-project guard. Campaign maxima: Exa5USD, Modal40USD, Tinker10USD, past200credits. These are caps, not spending targets. Pilot uses a small fraction. All dispatch is manual. Reserve pending jobs before spawn, recheck account-wide usage, retain unknown charges, and reserve independent certification on GitHub Actions. Disable unknown provider boundaries rather than guessing.

Pilot clarification committed before any successful pilot: each saved state first receives a common250ms action0 probe. The measured diagnosis comes from that probe; all six paired interventions then start from the identical post-probe state with a common seed. This avoids labeling an already observed intervention as a prospective prediction. Probe CPU is reported and charged equally. Failure labels distinguish measured pair-constraint from triple-constraint rejection, alongside mismatch/repetition/stagnation/progress. All earlier failed integration runs remain visible; an initial failed image retains a conservativeUSD2 hold.
