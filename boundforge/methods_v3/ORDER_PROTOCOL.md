# Paired ordering pilot — frozen before outcomes

This is exploratory development, not the confirmatory study. The earlier scalar-probe pilot is still running when this protocol is committed; no outcomes from it select this design.

Hypothesis: when single interventions stagnate, a paired common-random-number crossover experiment A→B versus B→A can estimate order-specific enabling effects better than observational sequence credit. This is a narrow hypothesis, not proof that pair selection or noncommutativity is new.

Critical prior art: [CMCS](https://arxiv.org/html/1605.02038) already conditions sequence transitions on success/failure; [Yates/Keedwell](https://link.springer.com/article/10.1007/s10732-018-09404-7) already learns and transfers useful ordered subsequences. The candidate's only potentially material distinction is online same-state, common-random-number order contrasts with reused prefixes and explicitly charged costs. A novelty search miss is not evidence of originality. A positive result still needs comparison with existing experimental-design/portfolio methods.

Four operator-batch executions yield both single outcomes and both order outcomes by reusing the two single prefixes. Each batch is four primitive moves. Reuse is standard DAG memoization and allowed to every paired control. Retain every valid intermediate construction in every arm. Exact checks, logging and controller costs are measured. Probe comparisons are stochastic experiments, not impossibility certificates.

Development: graph(160,.14,seed9201), cap dimension4, deletion length8. Test all 30 ordered fixed pairs, seeds8101/8102, 0.15 search CPU seconds each. Select one global fixed pair by equal-task normalized gain; this is tuning, not test performance. All validation policies use this same tuned fallback.

Validation: two unseen graph instances (224,.10,seed9301;288,.06,seed9302), cap dimension5, deletion length10. Five seeds8201–8205; 2 search CPU seconds per arm. These classes were already exposed in earlier BoundForge work; this is prospective validation, not broad untouched transfer. Policies: tuned fixed pair, ordered-pair UCB, conditional transition credit (CMCS-inspired adaptation), ε-greedy single selection, paired order contrasts, shuffled contrast signs, and paired absolute sequence-reward selection. Same primitive library, initialization and core budget. Policies rotated by task/seed. Report all outcomes, actual overruns and independent verification separately.

Primary pilot questions: (1) Are enabling examples present? (2) Does measured orientation help over shuffled labels under the same probe pattern? (3) Does it beat tuned fixed, UCB and conditional sequence credit after paying for probing? A measured asymmetry alone is not a useful controller. Do not scale if controls dominate or contrasts fail to predict future order.

No claim of reproducing original CMCS's published benchmark score. Its success/failure-conditioned transition mechanism is reimplemented for this shared finite-construction interface. Training/model costs from generating this hypothesis are separate from episode CPU. Repetition counts are exploratory; no p-values or general superiority claim. Any next confirmatory campaign requires frozen code, new instances and a powered repetition plan.
