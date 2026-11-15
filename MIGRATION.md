# Standalone repository migration

Source: https://github.com/howdymary/compute-forecasting/tree/99fd43a3fab468e82e84463a2d069b34aae8baca/boundforge
Source branch at capture: compute-observatory; immutable source commit: 99fd43a3fab468e82e84463a2d069b34aae8baca.
Destination: https://github.com/howdymary/boundforge, main.

All 141 project files and 12 BoundForge workflows were captured. Certificates, verifier source, recorded research results, original source materials and logs are preserved exactly. migration-manifest.json records every imported path and source hash; modified operational files are listed explicitly.

The project directory remains boundforge/ to retain scientific artifact paths. This repository contains no Compute Observatory code, datasets, dependencies, deployed services or volumes. Exact verification and replay require no old repository or paid account.

Active publishers now write to this repository/main. Publishing and paired-follow-up workflows take explicit run IDs from this repository instead of hard-coded historical runs. Old run IDs inside immutable reports, receipts and scientific source notes remain provenance, not operational references. Git history is retained at the source link; the new repository begins with a provenance-linked snapshot, not the forecasting project's history.

Research/publishing workflows are manual. Migration does not spend provider credits or refresh archived budget snapshots. A new campaign must verify balances, account-wide consumption, billing boundaries and pending holds.

The five required GitHub secrets are migrated using GitHub's destination repository public key and sealed-box encryption inside an old-repository Actions job. Only destination-specific encrypted envelopes leave that job; plaintext keys are never printed or committed. Old secrets remain because the independent forecasting project uses them.

After standalone CI passes, the old default branch's boundforge/ directory and BoundForge-only workflows are removed in a normal commit. Forecasting code and workflows remain unchanged. Original commits and research runs are not deleted or rewritten.

## Updated operational files

- .github/workflows/boundforge-check.yml
- .github/workflows/boundforge-literature.yml
- .github/workflows/boundforge-method-replay.yml
- .github/workflows/boundforge-nondegenerate.yml
- .github/workflows/boundforge-precision.yml
- .github/workflows/boundforge-preflight.yml
- .github/workflows/boundforge-publish.yml
- .github/workflows/boundforge-structural-v2.yml
- .github/workflows/boundforge-v2-check.yml
- .github/workflows/boundforge-v2-publish.yml
- .github/workflows/boundforge.yml
- boundforge/README.md
- boundforge/finalize.py
- boundforge/research_v2/followup.py
- boundforge/research_v2/publish.py
- boundforge/research_v2/publish_followup.py
