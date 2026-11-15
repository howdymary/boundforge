# Competing approaches and rejection gates

| Approach | Closest prior art | Possible material difference | Smallest rejection test |
|---|---|---|---|
| Lazy certificate cache and complete neighborhood scheduling | Memoization, variable neighborhood descent | None claimed; diagnose implementation/horizon confounding | Profile saved states; if savings do not alter matched-budget outcomes, retain as engineering only |
| Failure-certificate-guided operator synthesis | Noodle2019, explanation-guided LNS, CEGIS, FunSearch | Must synthesize a reusable move outside a certified failure class, rather than rename feasible mutation | A synthesized operator must beat matched search/program-synthesis controls and transfer; otherwise reject |
| Entropy-jet support search | Entropy perturbation, symbolic asymptotics, multiobjective descent, support/column generation | Potentially compile singular and higher-order cancellations into structural experiment choices and precision predictions through one task-independent interface | Must beat first-order boundary-aware and adaptive-precision finite-search controls on natural higher-order cases; a first-order tail refinement is insufficient |
| Joint geometry/probability continuation | Numerical PMF optimization, PatternBoost, column generation | None established for ordinary joint reoptimization | Use as a strong production/baseline method, not automatic novelty |

Primary sources inspected:
- Noodle: https://arxiv.org/html/1909.08242v1 (synthesizes constraint-aware local-search operators; overlaps the generic operator-generation idea).
- Zhang et al.2024: https://www.mdpi.com/1099-4300/26/8/711 Section3 (softmax PMFs, gradient descent on entropy-vector objectives; comparison with randomized PMF search).
- Matveev/Portegies: https://arxiv.org/html/1704.00297 (large tensor-power/asymptotic equivalence, distinct from a claim that small-mass formal jets are new).
- C3c source: https://teorth.github.io/optimizationproblems/constants/3c.html and Jaswal's certificate. Published leading digits remain1.674894211307116; finer comparisons require actual certificates and open-claim audit.

Seven successful Exa connector searches requested41 leads; one fetch batch returned3 pages. Leads are not41 validated original papers. Connector cost receipts are unavailable and will remain separately unresolved. No credit balances were queried. This research does not interpret a search miss as proof of novelty.

Development begins with exact entropy-jet compilation and independently checked finite witnesses. No confirmatory outcomes have been opened. Preregister an actual mechanism and stronger baselines before scaling or claiming success.
