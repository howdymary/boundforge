# Exploratory pilot, frozen before outcomes

Date: 2026-11-15. No held-out or new-method claim from this pilot.

Construct independent-set tasks from random graphs, binary two-deletion conflict graphs and ternary cap-set hypergraphs. Exact membership checks are separate from local search. Start from newly generated greedy states. These are human/agent-designed mathematical adapters; cardinality is the objective, not a sunflower asymptotic rate.

Use 3 instance configurations per class, seeds 7101/7102/7103, each policy 1.0 process CPU seconds including initialization, probes, acceptance and decision overhead. Also record wall time, primitive evaluations, validation work and time to best. Rotate policy order by task/seed to reduce warmup bias. Build-time accounting separate. Every retained best is independently checked from the mathematical definition.

Common six operators: three random destroy sizes (5%,20%,50%), targeted single-anchor repair, coordinated two-anchor repair, and a fresh greedy restart. All policies get every operator. No candidate-specific privilege.

Policies: each fixed action (for development selection only), round-robin, random, UCB, ALNS roulette, measured same-state probing, and identical-cost probes with shuffled exploitation choices. The last two use the same saved state and paired seeds for short probes, retain all valid probe candidates, then spend one longer quantum continuing the selected action. Their shared probe branches must not be called a diagnosis advantage; only the action-selection difference is attributable to measurement.

Pilot purpose: identify hardness, ceiling effects, probe cost and promising scope. No p-value or generalization claim. Development-best fixed selection cannot be called a globally strongest procedure. A later evaluation must add task-appropriate published algorithms and sealed instances, and freeze repeat counts after variance estimation.

Stop scaling a direction if matched controls dominate it or useful action diversity is absent. Do not spend remaining credits repeating equivalent failures. If probing appears helpful, inspect effect mechanism and prior-art overlap before calling it new. Paired same-state effects remain conditioned on the source state.
