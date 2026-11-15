# BoundForge

An autonomous research loop with sourced frontiers, isolated experiments, scoped memory and mathematical acceptance outside the search worker.

**Latest research cycle (2026-11-15):** [failure diagnosis, stronger controls and method assessment](boundforge/methods_v4/RESEARCH_STATUS.md). Running the existing conventional solver produced a further tiny certified C3c refinement; the new representation experiments did not establish a new general method or performance advantage. [Exact witness and checks](boundforge/methods_v4/README.md) · [decision log](boundforge/methods_v4/decisions.jsonl). Earlier reports below remain historical.

**C51a > 0.585078819674513593.** Three checker implementations certify this very small He–Tang-family parameter refinement, including the whole circle and infinite tail. It beats an upper bound on the strongest external prior function located by more than 1.58×10^-17. This is not a substantial mathematical advance or a new general algorithm.

The Codex research agent found the initial refinement during development. The portable runner was built afterward; its recorded executions are autonomous historical replay/continuation, not a blind held-out discovery. It does choose, run, inspect and change experiments without human experiment-by-experiment control. A strong fixed high-precision method is faster, so no controller-advantage claim is made.

- [Readiness, verification and final form checklist](boundforge/submission/READINESS.md)
- [Submission draft and short description](boundforge/submission/SUBMISSION.md)
- [Track1 requirement-to-evidence map](boundforge/submission/TRACK1_FIT.md)
- [Mathematics, strict comparison and trust boundary](boundforge/submission/MATH_VERIFICATION.md)
- [Two-minute captioned demo](boundforge/submission/demo/boundforge-2min.mp4)
- [Downloadable offline trace viewer](boundforge/submission/demo/index.html)
- [Actual source/model-assisted decision trace](boundforge/autoresearch/results/2026-11-15/providers-model/decisions.jsonl)
- [Corrected fixed-search comparisons](boundforge/autoresearch/results/2026-11-15/controls-continuation/summary.json)

## Run the loop without paid providers

From a remote checkout of this repository:

~~~sh
python -m pip install -r boundforge/autoresearch/requirements.txt
docker build -t boundforge-research-worker boundforge/autoresearch
python -m boundforge.autoresearch.run \
  --out boundforge/autoresearch/runs/example \
  --sandbox docker --upstream
~~~

Or run the manual [autonomous research workflow](.github/workflows/autoresearch-loop.yml). The optional published-verifier download is pinned by source hash; omit --upstream for the two own checkers alone. Numerical workers have no network, secrets, repository mount or saved answer. Candidate generation and protected acceptance run in separate processes.

The controller first tests a cheap numerical method. It can retain a valid improvement below the current continuation goal, retrieve that evidence and choose higher precision. It generates exact rational parameters and a proof budget, runs independent full-domain checkers, and stops only at the declared goal or resource limit. Hash-chained decisions, requests, results and checkpoints are saved. Completed runs can be resumed with --resume; altered inputs or artifacts are refused.

## Optional source and model path

The manual [Exa/Tinker workflow](.github/workflows/autoresearch-providers.yml) calls Exa inside the next-experiment branch. Search returned only a rounded excerpt; contents confirmed the full exact witness before research could continue. A real Tinker call proposed a bounded operator; its explanation remains unverified model text. [Provider semantics and failures](boundforge/autoresearch/PROVIDERS.md) and the [shared cross-run ledger](boundforge/autoresearch/provider-ledger.json) are explicit.

Fresh credit snapshots and immutable per-provider caps are required before paid runs. Unknown charges stay reserved; no purchases, upgrades or automatic replenishment. Default execution needs no paid provider. Model training and a memory/model performance advantage are not claimed.

## Verification and history

[Autonomous execution contract](boundforge/autoresearch/CONTRACT.md) · [Comparison contract and corrections](boundforge/autoresearch/EVALUATION.md) · [All 120 constants ranked](boundforge/portfolio/TARGET_RANKING.md) · [Original portfolio result](boundforge/portfolio/RESULT.md) · [Attribution](boundforge/submission/THIRD_PARTY_NOTICES.md)

The existing C3c and C49a archives remain intact:

- [C49a guide](boundforge/c49/README.md) and [final assessment](boundforge/c49/FINAL_RESEARCH_REPORT.md): strongest relevant witness reproduced, no new C49a bound or controller advantage.
- [C3c guide](boundforge/README.md) and [final assessment](boundforge/research_v2/followup/FINAL_RESEARCH_NOTE.md): roughly 2.21×10^-22 conventional refinement; later 174 cases no further gain.
- [Standalone migration provenance](MIGRATION.md) and [earlier root guide](boundforge/submission/README-before-submission.md).

Work on main through GitHub and remote execution. Protected verifiers retain their original hashes. No paper, researcher contact or leaderboard submission has been made.
