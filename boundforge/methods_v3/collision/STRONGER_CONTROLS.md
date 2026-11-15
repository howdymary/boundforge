# Additional controls specified before opening collision-pilot outcomes

The original six-arm development pilot remains frozen at source77511b5. It is not retroactively changed. Add these controls in subsequent development/validation:

- Conditional greedy rebuild: retain the proposed new public constraint, then greedily reinsert rows from the previous collision flat while preserving target separation. This can cross a larger neighborhood than deleting two basis rows and is a strong simple alternative to basis changes. It is not a complete optimizer.
- Numerical UCB over the full common procedure library: random flat edits, direct circuit repair, random basis pivots, guided pivots, and conditional rebuild. This gives the simpler controller access to the proposed intervention rather than withholding a good operator.
- Random selection over that same full library. Separate the value of a new intervention from the policy choosing it.

All share initial constructions, exact objective, feasibility checks and CPU accounting. The development pilot cannot establish efficacy against controls not yet run. If a generic controller uses the proposed intervention equally well, scope any contribution to the intervention/representation and do not claim a superior research controller.
