# BoundForge

An independent computational mathematics research framework with exact acceptance, bounded remote experiments and inspectable decisions.

**C49a campaign:** independently reproduced the stronger PR370 sunflower-free capacity witness, 1.5678643845728069793620..., and tested diagnostic/memory search controllers against fixed, scheduled and adaptive controls. The first comparison found no controller advantage over the strongest controls. Bounded record search has not produced a new C49a bound. See the final assessment for the completed campaign and its limitations.

- [C49a guide and reproducible verification](boundforge/c49/README.md)
- [C49a research design, proof and novelty table](boundforge/c49/RESEARCH_DESIGN.md)
- [C49a final assessment](boundforge/c49/FINAL_RESEARCH_REPORT.md)
- [C49a exact witnesses, raw results and actual-artifact replay](boundforge/c49/results/)
- [C49a frozen comparison](boundforge/c49/EVALUATION_PREREGISTRATION.md)

**C3c archive:** two protected independent checkers certify a roughly 2.21 × 10⁻²² refinement of Jaswal's published witness. The leading 15 digits are unchanged. A later174-case campaign found no further improvement or demonstrated model advantage. This is not a substantial new mathematical advance.

- [C3c guide](boundforge/README.md)
- [C3c research assessment](boundforge/research_v2/followup/FINAL_RESEARCH_NOTE.md)
- [Comparative research review](boundforge/research_v2/COMPARATIVE_REVIEW.md)
- [C3c exact retained certificate](boundforge/results/best.json)
- [C3c recorded replay](boundforge/research_v2/output/demo.html)
- [Target-selection history](TARGET_SELECTION.md)
- [Separation provenance](MIGRATION.md)

Work on **main**. Author through GitHub and isolated remote runners. The source directory preserves archived paths; no forecasting package, dataset, deployment or volume is required. Compute Observatory is separate.

## Verify without paid services

Run **Check BoundForge sources and certificate**, **Check BoundForge research v2**, or the manual **C49 preserve results and independently certify** workflow. In an isolated remote checkout:

~~~sh
python -m pip install -r boundforge/requirements.txt
python -m pytest -q -p no:cacheprovider boundforge/test_core.py boundforge/research_v2/test_v2.py boundforge/c49/test_c49.py
python boundforge/verify.py boundforge/results/best.json --baseline boundforge/certificates/incumbent.json
python boundforge/verify_independent.py boundforge/results/best.json boundforge/certificates/incumbent.json
python boundforge/c49/certify.py boundforge/c49/results/baseline.json boundforge/c49/results/baseline.json
python boundforge/migration_check.py
~~~

All paid research workflows are manual. Refresh provider balances/billing boundaries before future paid work; preserve historical holds and unresolved reservations. Snapshots are not current balances. No purchases, plan upgrades or automatic replenishment are authorized. Required research secrets are EXA_API_KEY, PAST_API_KEY, TINKER_API_KEY, MODAL_TOKEN_ID and MODAL_TOKEN_SECRET.

The C3c construction/refinement approach is attributed to [Manvir Jaswal](https://zenodo.org/records/23289305). C49a construction data, gluing and prior bounds retain the attribution recorded in the C49 research guide, including DEGKM, IRSI, Claude F/H, Sylla, Koshta and Pinho. Verification engineering and an attractive demo do not establish a new mathematical or methodological contribution.
