# C1a/C1d next-target contract

Registered before execution. Run only after C1b finishes and passes its serialized credit ledger forward. If C1b already improves by at least the Arena1e-7 threshold, skip paid work and finish its certification. Tiny improvements and unresolved stronger rounded claims do not establish an unqualified global record.

Baseline C1d: PR345 exact163840-cell signed-absolute certificate at1.45467334138563686456..., pinned cc2c67d; the exact fraction/source hash are checked in code. Arena problem4 and the QWNTL C3+1.448867... result use abs(max convolution), so those are a different constant. Do not claim to beat them under a different objective.

Baseline C1a: PR367262144-cell nonnegative certificate at1.50266483361440728..., hash b33995fe.... It is stronger than QWNTL's1.502664840776... and the live Arena's1.5027434867. Source is data only. Keep original authorship.

Two independent exact scorers: split-sign packed integer polynomial products and six-prime signed NTT/CRT, with proven coefficient bounds, primality/primitive-root checks and adversarial brute-force controls. Fresh replay of each incumbent happens before paid allocations. Numerical FFTs never accept a record.

Six bounded one-CPU420s workers, at most4 concurrent,2GB memory. Four C1d starts and two C1a starts, exactly specified in specs.json, using conventional p-norm continuation and modest kicks; one exact2:1 refinement. This is an adaptation of existing methods, not a novelty claim. Reserve2USD image plus1.50USD per worker,11USD total additional allowance, within the separately recorded60USD Modal cap. Final certification uses free GitHub Actions.

Retain all candidate data and exact results, including failures. A project record candidate needs >1e-12 strict exact improvement, not roundoff, stale decimals or precision reformatting. A live primary/leaderboard audit and fresh independent certification still precede any record claim. No external submission is authorized.
