# Submission readiness

Prepared 2026-11-15 for Track 1. **The technical package is prepared; no competition form or leaderboard has been submitted.**

## Ready to review

- [Repository](https://github.com/howdymary/boundforge), branch main.
- [Copy-ready title, description and Q&A](SUBMISSION.md).
- [Two-minute MP4](demo/boundforge-2min.mp4): 1280 × 720, H.264, 30 fps, exactly 120 seconds; silent and captioned.
- [Required 16:9 project screenshot](demo/submission-screenshot.png).
- [Offline interactive trace viewer](demo/index.html): download and open the single HTML file; its actual recorded data is embedded. GitHub's source view does not execute HTML.
- [Narration and demo plan](DEMO_SCRIPT.md), [track evidence](TRACK1_FIT.md), [mathematical argument](MATH_VERIFICATION.md).
- [Artifact manifest](manifest.json), [final verification](verification/check-summary.json), [actual provider-assisted run](../autoresearch/results/2026-11-15/providers-model/report.json).

The video is an artifact-driven replay, not a live recording. It preserves the recorded execution and deliberately slows playback for inspection. All source references, raw events, checker outputs and controls are accessible in the viewer.

## What was verified

[Final verification run](https://github.com/howdymary/boundforge/actions/runs/43691994451): **48 tests pass** (23 archive tests and 25 portfolio/controller tests), two protected verifiers and 153 historical files pass migration checks, Docker execution succeeds, the full autonomous loop certifies the candidate, checkpoint resume checks immutable inputs/artifacts, and project sources compile.

The final verification loop takes two experiments and 8.49 seconds with paid providers disabled. The [canonical Exa/Tinker-assisted execution](https://github.com/howdymary/boundforge/actions/runs/43690811950) takes two experiments and 22.27 seconds. The latter supplies the demo data.

[Media QA](https://github.com/howdymary/boundforge/actions/runs/43692375488): video metadata validated; HTML initializes; next/back/slider work; desktop and mobile render; no horizontal overflow. Desktop/mobile screenshots and all eight video frames are preserved.

The candidate proves **C51a > 0.585078819674513593**, more than **1.58 × 10^-17** above a rigorous upper bound on the actual strongest external prior function found. All three checker implementations cover the full mathematical domain and omitted infinite tail. Executing a separately authored checker is not independent human endorsement. The gain is extremely small and conventional.

## What autonomy and novelty mean here

The executable chooses an experiment, runs an isolated worker, reads and certifies its result, retains valid partial progress, retrieves scoped evidence and chooses another intervention without human experiment-by-experiment control. The published source/model-assisted run includes an actual Exa gate and Tinker operator choice.

The initial result was found during agent-directed development. The standalone controller was engineered afterward. Its demonstration is autonomous historical replay/continuation, not a blind discovery on an untouched problem. Its library, policy and mathematical construction are informed by development.

The strongest fixed high-precision control is faster. Neither a reusable new research method nor a model/memory performance advantage is established. Track fit is supported by the runnable loop and inspectable certificates; prize eligibility and judging remain the organizers' decisions.

## Provider accounting

This submission phase consumed USD 0.015 in receipted Exa calls. Three Tinker reservations total USD 0.15 and remain held because itemized receipts are unavailable; the successful call's token-based estimate is USD 0.00286965, **not an additional settled receipt**. The first two attempts failed before sampling. No new Modal or past.dev work ran in this phase.

Historical unresolved campaign holds remain preserved separately: Exa USD 2.46, Tinker USD 3.20, Modal USD 115.58 and past.dev 90 credits. Do not add unlike units. See [provider budget](../autoresearch/provider-budget.json), [cross-run ledger](../autoresearch/provider-ledger.json) and [provider notes](../autoresearch/PROVIDERS.md). Snapshots expire: this package is not authorization to reuse stale balances for another paid run. Developer connector usage and GitHub Actions billing are not covered by those four-provider receipts.

## Final form fields and user actions

The live form was inspected read-only on 2026-11-15. It requires title, description, track and screenshot, and provides GitHub and demo URL fields. It recommends YouTube or Loom; the resources also accept Drive.

1. Supply/confirm team identity and the event's team-size and physical-presence requirements.
2. Upload the prepared MP4 to YouTube, Loom or Drive and copy its viewing URL. The public GitHub MP4 is ready for download; a video-host URL is not invented here. The connected Drive uploader requires a local file, which conflicts with the user's no-local-files instruction.
3. Use title **BoundForge**, select **Track 1**, paste the prepared description and repository URL, and upload the supplied screenshot. Exa has actual main-loop evidence; Modal has earlier negative CPU-search evidence. Do not select past.dev on the strength of this new phase alone.
4. Review and submit the form yourself, or explicitly authorize that final action separately.

The resources contain conflicting 14:00/14:30 PT deadlines on November 15; use 14:00 as the working deadline unless organizers clarify. No team facts or venue attendance are inferred. Commit-date and migration provenance are evidence, not an organizer eligibility ruling.
