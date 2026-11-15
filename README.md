# BoundForge

An independent, auditable computational mathematics research project targeting C3c, the four-slope arithmetic Kakeya sum–difference constant.

**Measured status:** two independent checkers certify a roughly 2.21 × 10⁻²² refinement of Jaswal's published witness. The leading 15 digits are unchanged. A later 174-case campaign found no further improvement or demonstrated model advantage. This is not a substantial new mathematical advance.

- [Project and reproduction guide](boundforge/README.md)
- [Latest research assessment](boundforge/research_v2/followup/FINAL_RESEARCH_NOTE.md)
- [Comparative research review](boundforge/research_v2/COMPARATIVE_REVIEW.md)
- [Exact retained certificate](boundforge/results/best.json)
- [Actual-artifact replay](boundforge/research_v2/output/demo.html)
- [Continuation prompt for Track 1](CONTINUE_RESEARCH.md)
- [Alternative constants and current frontier audit](TARGET_SELECTION.md)
- [Separation provenance and operational notes](MIGRATION.md)

Work on **main**. All source code, pinned numerical dependencies, certificates, logs and research artifacts are in this repository. The boundforge/ source directory is retained to preserve artifact paths; no forecasting package, dataset, deployment or volume is required.

## Verify without paid services

Run **Check BoundForge sources and certificate** and **Check BoundForge research v2** in Actions, or in an isolated remote checkout:

~~~sh
python -m pip install -r boundforge/requirements.txt
python -m pytest -q -p no:cacheprovider boundforge/test_core.py boundforge/research_v2/test_v2.py
python boundforge/verify.py boundforge/results/best.json --baseline boundforge/certificates/incumbent.json
python boundforge/verify_independent.py boundforge/results/best.json boundforge/certificates/incumbent.json
python boundforge/migration_check.py
~~~

Research and publishing workflows are manual; creating or editing this repository does not launch paid research. Before future paid runs, refresh provider balances/billing boundaries and preserve unresolved historical holds. Historic snapshots are not current spending authorizations. Required research secrets: EXA_API_KEY, PAST_API_KEY, TINKER_API_KEY, MODAL_TOKEN_ID and MODAL_TOKEN_SECRET.

The original construction and stationary refinement approach are attributed to [Manvir Jaswal](https://zenodo.org/records/23289305). Prior research and third-party source artifacts retain their provenance and applicable licenses.
