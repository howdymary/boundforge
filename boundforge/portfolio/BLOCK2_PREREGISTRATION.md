# Two-coordinate masked-alphabet pilot

Registered before execution. Different construction after ordinary masks and nonsmooth cost-weight search found no improvement. Cost is linear in two coordinates; correlated membership is the new search dimension.

Take F subset of[0,B]^2 containing(0,0), cost w(a,b)=a+b, flatten labels a+(2B+1)b. Sum and difference labels are injective on their respective coordinate ranges. Use these labels as a one-digit alphabet in the weighted-budget proof; the final positional base is2*max(flat label)+1. This does not confuse weights with labels. It is an application of the existing type-counting/large-deviation method, not a new general theorem.

The product <4,5>^2 has partition histograms equal to the convolution squares of the one-coordinate histograms and reproduces the same entropy ratio. A cross generator such as(2,4) may make selected differences cheaper while introducing fewer new low-cost sum vectors than adding the one-coordinate letter2. Coordinated deletion of every representation of a low sum is another distinct neighborhood; random single-point edits rarely change sum support.

B=80. At most90 one-cross-generator,100 two-cross-generator,120 axis-replacement and160 coordinated-sum-deletion cases;175s wall-clock limit, exact C++ pair enumeration per candidate, two numerical tilt starts. Semigroup and coordinate boxes are search restrictions; no completeness claimed. Verify the product histogram identity before nonproduct cases. Keep all failures.

A score>1.272558052 triggers independent exact finite-type certification and a new frontier audit. That threshold is above the stronger open1.2725580515... limit claim as printed. No numerical candidate is accepted automatically. If no movement appears, do not repeat this library at larger scale solely because credits remain. Free public GitHub runner, no paid-provider calls.
