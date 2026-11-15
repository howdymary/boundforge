# Track1 requirement-to-evidence map

[Event brief](https://iterate.inc/ai-research?welcome=true&tab=resources), read 2026-11-15. No competition form or leaderboard has been submitted.

| Requirement / criterion | Evidence | Scope |
|---|---|---|
| Eligible mathematical target | Tao C51a, Erdős maximum-term constant | https://teorth.github.io/optimizationproblems/constants/51a.html |
| Beat a relevant prior bound | C51a >0.585078819674513593; three full-circle/tail checkers; actual external-function comparison | Tiny conventional parameter refinement, not a large mathematical advance |
| System chooses what to try | One-command controller selects bounded float/precision/restart experiments from measured evidence | Human/agent-designed operators and policy; not unrestricted invention of methods |
| Runs experiments itself | Docker workers, network disabled, read-only filesystem, no secrets or winning artifacts mounted | CPU-only numerical workers; parent owns acceptance |
| Reads results and chooses next | Valid float progress below continuation goal -> scoped memory retrieval -> high-precision action; model-assisted run uses Exa and Tinker | Real two-experiment trace, no human experiment-by-experiment intervention |
| Stops at goal or budget | Explicit project-bound floor, wall/step caps, strict certification and safe checkpoint resume | Valid smaller results are retained without being mislabeled failures |
| Show every decision | Hash-chained JSONL, requests/results, exact candidate data, source/image hashes, checkpoints, provider receipts/reservations | Hashes detect accidental changes and are anchored by commits; not proof against a malicious author rewriting all history |
| How far beyond record | >1.58×10^-17 above an upper bound on the strongest external prior function found | Extremely small, a weakness under record-size judging |
| How new the loop is | Distinctive source/proof/budget integration and separation of partial progress from goal acceptance | No new general algorithm, no demonstrated advantage over strongest fixed method |
| Baselines | Same input,3paired seeds, common caps; fixed float and fixed high precision included | Fixed high precision is faster; seeds are not independent tasks or held-out generalization |
| Required project screenshot | [Prepared 16:9 PNG](demo/submission-screenshot.png), copied from the actual-artifact video | Upload field required by the live form; no form was filled |
| Submission materials | Public repo, exact replay commands, trace viewer, captioned120-second video, short description and script | User still supplies team details and a final hosted video URL if required by the form |

## Autonomy chronology

The Codex research agent performed the frontier audit, selected targets, wrote and ran experiments, and found the initial C51a refinement without the user supplying its numerical answer. The standalone controller was extracted and implemented AFTER that agent-directed discovery. Its recorded runs are autonomous historical replay/continuation, not a blind held-out rediscovery. The source and saved winner are excluded from proposal containers, but the operator design was informed by the earlier development. This distinction must remain in the pitch and README.

Track1 does not require a claimed new theorem or a learned policy. The executable does run the requested loop. Its small gain and conventional method are competitive limitations; polished packaging does not remove them.

## Optional challenges

Exa: the source gate is inside the main loop, with actual API request IDs, exact witness confirmation and cost receipts. Search alone returned a rounded short excerpt; contents supplied the full pair before the controller could continue. The demo shows this consequence. An adapter that never made a real call is not counted.

Tinker: a real bounded operator-choice call is logged; explanations are hypotheses. The model rationale partially conflated numerical uncertainty with absence of verified progress, while exact records preserve the distinction. The proposed operator executed and the proof checkers decided the outcome. No fine-tuning or model-advantage claim.

Modal: earlier15bounded CPU workers and their negative results are preserved. The C51a certificate itself ran on inexpensive GitHub CPU; do not claim Modal discovered it.

past.dev: earlier C49 role-memory experiments are archived, but no new past.dev claim is made for this submission phase.

## Administrative eligibility evidence

The repository is public. Standalone root commit407ee3f811d03fa97e824cfa80a947e3f714532e is2026-11-15T04:40:37Z. The earliest imported BoundForge-directory source commit7c9c8554acb4f80292500feec0fb3b9023590cca is2026-11-15T02:50:16Z (Nov14 18:50PT), after the stated event build start Nov14 10:00PT. Migration provenance is preserved; history was not rewritten to hide prior work. This is commit-date evidence, not an organizer ruling. Team size/names and physical presence are user-confirmed fields.

The live page lists14:00 in the schedule and14:30 in the submission section. Use the earlier14:00PT on November15 as the working deadline unless organizers clarify.
