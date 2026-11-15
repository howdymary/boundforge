# Exploratory port-composition diagnostic

Before execution: use the reproduced PR370 family and the published F10/H11 families. Enumerate every ordered port pair; count exact positive transfer matrices. Search all pairs and a width256 beam through period8, then isolate candidate rates rigorously. This is existing periodic gluing and positive matrix optimization, not a new theorem or global optimum claim.

Also test whether the PR370 Perron eigenvector u=(sqrt(88867/33980),1) bounds every port matrix of that exact family componentwise by rho0*u. If every exact inequality holds, arbitrary products of those port matrices satisfy the same upper rate and port-only periodic search can be stopped with a scoped certificate. The check reduces each A*sqrt(88867/33980)+B<=0 to signed integer-square comparisons. A failed inequality is not evidence of an improvement.

This is a separate mathematical headroom diagnostic, not retuning the frozen controller evaluation. No provider calls or paid resources; bounded GitHub Actions execution. The two base families and the large family retain their original authorship.
