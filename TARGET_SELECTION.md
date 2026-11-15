# Target reassessment after C3c

Research date: November 14, 2026, America/Los_Angeles (receipts extend into November 15 UTC).
This is a source audit and proposed experiment agenda, not a claim of new records or an executed alternative-target campaign.

## Recommendation

Run a bounded feasibility pilot for **C49a, 3-sunflower-free capacity**, before allocating a large new campaign.
Keep **C1d, signed third autoconvolution**, as a backup. C89a is a third option with a more expensive exact evaluator.
This prioritization is our analysis, not a measured probability of success. A large gap between known bounds does not imply easy computational headroom.

The last C3c campaign found no further improvement. Its earlier roughly 2.21e-22 certified refinement remains valid; it is not a substantial mathematical advance. Preserve that archive and its attribution.

## Frontier audit: merged pages are insufficient

The current table warns that inclusion does not certify correctness. Open submissions can contain stronger witnesses than either the summary table or the detailed page.
The following are the strongest claims found in the inspected pages and relevant open PRs; they are not an exhaustive proof that no other result exists. None of these alternative-target witnesses has been independently replayed by BoundForge yet.

| Target | Merged-page construction | Stronger open claim found | Preliminary assessment |
|---|---|---|---|
| C49a, lower bound: higher is better | (64728+sqrt(3018723123))^(1/26) ≈1.5678599024 | [PR370](https://github.com/teorth/optimizationproblems/pull/370): (64728+sqrt(3019700660))^(1/26) ≈1.567864384572806979 | First pilot: discrete constraints and structural alternatives; exact family plus valid chain theorem needed. |
| C1d, upper bound: lower is better | 1.457854884921989, a restricted-access 800-cell artifact | [PR345](https://github.com/teorth/optimizationproblems/pull/345): exact fraction 838861227937471890002426104328885370880 / 576666392427609677715360509915372739121 ≈1.45467334138563686456 | Clean exact objective and parallel optimization, but latest witness has163840 cells and recent gains are tiny local refinements. |
| C89a, upper bound: lower is better | 0.030138879313256… from a3840-class step graphon | [PR270](https://github.com/teorth/optimizationproblems/pull/270): claims0.0301388585 | Rich structural search, but exact density certification and large graphon handling raise implementation cost. |

Primary pages: [49a](https://teorth.github.io/optimizationproblems/constants/49a.html), [1d](https://teorth.github.io/optimizationproblems/constants/1d.html), [89a](https://teorth.github.io/optimizationproblems/constants/89a.html).
[Main table and verification caveat](https://teorth.github.io/optimizationproblems/).

C49a PR370 was updated November14. It replaces21 additional sets in Koshta's252292-set block with32 seven-element sets, producing252303 sets; its claim is roughly4.48e-6 above the merged construction. That result is prior art, not ours.
It explicitly labels its AI referee as not an independent second party. The certificate and proof must be replayed and assessed before using it as an established comparison.
Primary packet: [rpinho/math-certificates at a50021b](https://github.com/rpinho/math-certificates/tree/a50021b04687719f4a2ea27609029982c980573e/c49/round1).

C1d PR345 describes p-norm continuation/L-BFGS restarts on Modal and two exact convolution checks; those techniques are established prior art for this target. Beating a weaker600-cell or300-cell witness would not beat the known frontier.
The restricted older artifact is [Zenodo23541324](https://zenodo.org/records/23541324); the stronger open witness is [quantavane-replays at cc2c67d](https://github.com/arhancanli/quantavane-replays/tree/cc2c67deb49fb09bcdc1947d0ad0b6ee2b9106b5/improvements/c1d).

## Why C49a is the first pilot

A3-sunflower consists of three distinct sets whose pairwise intersections are equal.
The search objects are finite bitmask families. Exact validity is discrete, and structural operators can add/remove coordinated sets, alter base families, select ports, and test compatible gluing patterns.
The published constructions certify an asymptotic rate using a transfer matrix and a gluing theorem, not just raw set count.

Use port-conditioned counts and the transfer-matrix growth rate as the actual objective. More sets can have the wrong distribution or require more ground-set points, so maximizing cardinality alone can mislead.

Proposed bounded diagnostic:
1. Pin and replay the newest candidate and the previous Koshta block; assess the proof transferring finite validity to the infinite chain.
2. Build an independently written checker from the mathematical specification.
3. Measure performance of fixed numerical/combinatorial baselines on small base families and validated structural operators.
4. Test genuinely different families or coordinated exchanges, beyond repeating the already-published21-to32 augmentation.
5. Retain exact witnesses and certify any claimed rate against the strongest reproduced relevant construction.
6. Continue only if the pilot finds legal nontrivial structural diversity, useful objective movement, or a falsifiable new mechanism. Do not invent a success-rate claim before these experiments.

[Prior certificate, proof and checkers](https://github.com/DennisKoshta/sunflower3-49a-certificate) disclose a fast proof-based Python check and slower exhaustive C/independent checks. These runtimes are author-reported; BoundForge has not timed them. The gluing lemma, exact chain count, small base families, pendant construction and augmentation all have explicit prior authors; credit them.

## Other screened directions

- [C1a Sidon autocorrelation](https://teorth.github.io/optimizationproblems/constants/1a.html): simple exact step-function formulation but highly competitive, large refined witnesses. [PR367](https://github.com/teorth/optimizationproblems/pull/367) claims1.5026648336, stronger than the detailed merged page; do not use its older1.5027434868 as the target.
- [C3a masked-digit sum–difference](https://teorth.github.io/optimizationproblems/constants/3a.html): transfers some C3c experience, but controlled carries and asymptotic/finite comparisons complicate acceptance. Existing sophisticated families make naive digit extension a weak default.
- [C3e unnormalized single-set sum–difference](https://teorth.github.io/optimizationproblems/constants/3e.html): exact finite counts are appealing, but the literature's simplex construction remains ahead of AlphaEvolve's reported blind search. A large known-bound gap is not evidence of tractability.
- [C42a Turán power sums](https://teorth.github.io/optimizationproblems/constants/42a.html): analytic asymptotic reductions and validated multi-dimensional integrals add proof risk. [PR302](https://github.com/teorth/optimizationproblems/pull/302) claims0.68637, ahead of the merged0.6873358063.
- [C51a maximum-term constant](https://teorth.github.io/optimizationproblems/constants/51a.html): certified complex analysis is possible, but optimizing the known two-parameter family alone may again yield only marginal gains.

## What is and is not new in BoundForge

Actual accomplishments: a tiny exact C3c witness refinement, a separately implemented verification chain, an inspectable remote research system, and a174-case study that identifies point-mass collapse and tests an optimizer correction.
These are certified/empirical artifacts. They do not establish a new general search algorithm, a new mathematical theorem, an advantage from language models or memory, or publication readiness.

Possible future contribution: a controller that identifies *why* a search failed, selects a meaningfully different intervention, and outperforms strong fixed/no-memory/numerical-only baselines under matched budgets. Failure-aware memory, adaptive neighborhoods, program evolution and multi-objective search have prior art; neither using these terms nor adding APIs establishes novelty. Compare the exact mechanism with prior work and test it.

Do not conflate target choice, a record improvement, and framework novelty. A successful C49a campaign could produce a new construction while using a conventional loop, or a useful framework result without beating a record; report the two separately.

No alternative-target paid search has been launched as part of this audit.
