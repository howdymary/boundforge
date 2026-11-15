# C49a: sunflower-free capacity

Independent target module. The C3c archive and protected acceptance checkers are unchanged.

This campaign tests two separate hypotheses: improve the strongest accessible C49a construction; test whether measured failure diagnoses and intervention memory outperform strong matched search controls. Neither success is presumed. See [research design and novelty table](RESEARCH_DESIGN.md), [frozen evaluation](EVALUATION_PREREGISTRATION.md), [production preregistration](PRODUCTION_PREREGISTRATION.md), [transfer follow-up](TRANSFER_FOLLOWUP.md), [port search](PORT_COMPOSITION_PREREGISTRATION.md), and [agent-memory prior art](PRIOR_ART_ADDENDUM.md).

## Results and verification

[Final assessment](FINAL_RESEARCH_REPORT.md), [actual-artifact demo](results/demo.html), [exact baseline](results/baseline.json), [certification](results/certification.json), [raw evidence](results/), [resource accounting](results/provider-usage.json). These links become available after the remote publication workflow completes.

All mathematical families are distinct integer bitmasks. A set is represented by its ground-coordinate bits. A valid finite gluing block must be Sperner and three-sunflower-free, have two distinct ports and positive four-way port counts. Its transfer matrix is [[N10,N11],[N00,N01]], with exponent n−2. A larger family is not necessarily a better asymptotic rate.

The retained frontier is Pinho PR370, pinned packet a50021b..., not a new construction by this project. Historical attribution and source hashes are preserved. No paid service is necessary to replay verification:

~~~sh
python -m pip install pytest
python -m pytest -q -p no:cacheprovider boundforge/c49/test_c49.py
python boundforge/c49/certify.py boundforge/c49/results/baseline.json boundforge/c49/results/baseline.json
~~~

Use an isolated **remote** checkout or GitHub Actions for these commands. The authoring workflow uses GitHub APIs and remote runners; no local project files are required.

The Cartesian-box and BDD implementations are algorithmically distinct and run as fresh processes during final certification. They were developed after reading primary sources, not clean-room. The algebraic comparison uses rational isolation rather than rounded floating point.

## Remote execution and controls

All C49 research workflows are manual. Their executed sources, seeds, frozen-policy hashes and outcomes are retained. Workflow names describe stageA, pilot, freeze, evaluate, model-study, production, transfer, ports, and publication. Do not rerun paid workflows against stale budgets. Reserve pending work in one serialized ledger, refresh account-wide billing boundaries, preserve unresolved holds and historical usage, and never purchase or auto-replenish credits.

Modal runs CPU-bounded workers without provider credentials or acceptance logic. Tinker proposes integer action rankings only; generated code is not executed. Training is deferred without sufficient verified diverse examples. Exa calls occur after pilot/model questions in the research loop, not just in a demo side feature. past.dev roles write and recall shared findings; exact witnesses and authoritative immutable state remain in GitHub artifacts.

The controller interface is reusable; task-specific representations, validity, scoring and several operator heuristics were human designed. No broad generalization claim follows from code reuse. Raw traces expose repeated-state, rejection and stagnation evidence; unsuccessful samples are never finite-scope impossibility certificates.

Artifacts are SHA256-indexed. Full retrieved copyrighted source text and temporary external checker source/binaries are excluded from publication. Public source links and hashes preserve provenance.
