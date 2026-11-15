# Next hypothesis: exact shared evaluation of a family of repairs

## Why change direction
Guided neutral basis pivots lost to direct repair in the initial pilot and in the log-only stronger-control run. Their enabled moves were insufficient. A neutral pivot followed by deletion/insertion also expands into an ordinary coordinated exchange (for one pivot, at most two old rows removed and two public rows inserted). This is not by itself a new general mechanism.

Investigate a different bottleneck: evaluating many counterfactual repairs repeats linear elimination.

## Exact algebra
Let T be an independent trial basis, and for each measured linear form f_i write
f_i = u_i + sum_b c_ib b,
where u_i is its canonical residual modulo span(T). For D subset T,
f_i-f_j lies in span(T minus D) iff u_i=u_j and c_id=c_jd for every d in D.
Proof: necessity and sufficiency follow from uniqueness of coordinates in the direct sum of span(T) and the fixed elimination complement. Thus partition labels under ANY proposed deletion D can be computed from (residual_class_i, c_i restricted to D), without rebuilding the reduced basis for every D.

Use one table for all control measurements and protected target measurements. Exact protected separation and the entire nonlinear projection-entropy objective can then be evaluated for every one/two-row deletion. Recover/rebuild only the selected candidate, followed by unchanged mathematical acceptance. This interface is reusable for grouped linear measurements, not arbitrary mathematical search.

## Novelty is unresolved
Residual coordinates, batch linear algebra, dynamic rank updates, and Distinct Vectors/feature selection are existing methods. Relevant primary sources include Froese et al. (https://arxiv.org/abs/1512.01150), Pilipczuk/Sorge (https://dmtcs.episciences.org/articles/6789), and Streit/Garg (https://arxiv.org/html/2408.04118v4). The claimed potential difference is a shared exact evaluation kernel for nonlinear collision objectives over an entire repair family, enabling stronger objective-aware moves at a practical cost. A speedup alone may be useful algorithm engineering; do not call it a new general research method without a material prior-art distinction.

## Pilot and falsifiers
1. Independently compare every partition, feasibility decision and selected best repair with fresh basis rebuilds on all deletions of size at most two in small exact cases.
2. Test generic grouped linear forms in dimensions other than planar point configurations. No adaptation beyond the adapter should be required for the algebra.
3. Time identical complete candidate families. Distinguish table-setup cost, scoring cost and rebuilding.
4. Compare shared-table best repair, naive best repair, existing random circuit repair and coordinate search under equal search CPU. Include initialization and action overshoot, report certification separately. Equal candidate counts are not enough.
5. Stop scaling if setup cost cancels savings or stronger counterfactual selection fails to improve quality-cost. Do not turn known batch evaluation into a novelty claim.

All results are development until a concrete method and evaluation are frozen. No untouched confirmatory outcomes are opened by this protocol.
