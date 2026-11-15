# BoundForge methods-v4
Start with [research status and failure diagnosis](RESEARCH_STATUS.md). The new general-method objective remains unmet.

- [Leading support-cone specification](MASK_SPEC.md)
- [Full finite support-geometry specification](PARTITION_SPEC.md)
- [Independent validation protocol](VALIDATION_PROTOCOL.md)
- [Conventional solver certificate](results/legacy/candidate.json)
- [Two original checker results](results/legacy/certification.json)
- [Legacy shortlist audit](results/oracle/legacy-counterfactual.json)
- [Corrected finite-versus-jets control](results/jets-corrected/report.json)
- [Full geometry development cases](results/partitions/tasks.json)
- [Unverified model critique](results/critique/critique.json)

All workflows are manual. Remote Actions/Modal runs only; no local project files. Protected verifiers and prior archives are unchanged. No external submission.

From a remote source checkout:
~~~sh
python -m pip install pytest==8.3.5 python-flint==0.8.0 mpmath==1.3.0 scipy==1.15.2 z3-solver==4.13.4.0
python -m pytest -q -p no:cacheprovider boundforge/methods_v4/test_jets.py boundforge/methods_v4/test_adaptive_log.py boundforge/methods_v4/test_masks.py boundforge/methods_v4/test_partitions.py
python -m boundforge.verify boundforge/methods_v4/results/legacy/candidate.json --baseline boundforge/results/best.json
python -m boundforge.verify_independent boundforge/methods_v4/results/legacy/candidate.json boundforge/results/best.json
~~~

The finite compiler is exact only when complete=true. A nonpositive logarithmic cone upper bound excludes positive *leading* simultaneous ascent within its specified class, not all improvements. Numerical LP proposals are re-evaluated rationally. Every retained mathematical claim uses independent finite acceptance.
