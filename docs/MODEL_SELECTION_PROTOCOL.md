# Follow-up analysis protocol
Date: 2026-11-05

## Status and scope
This is a prospective plan for new follow-up comparisons, informed by the
published v2 results and two audits. It is not a preregistration of the original
analysis. Known results include reference-based stability, short-text removal,
selected-prayer removal, and the three Topic 3 counterexamples.

Frozen annotations, curated source data, and published result directories will
remain unchanged. The first repair retains all 3,196 features. Identical columns
are grouped only for keyword display and overlap measurement, not removed from
the fitted matrix. A reduced feature space would require a separate v3 study.

## Numerical repair
Use a shared normalization/vectorization module. Save complete unit-length
topic-term matrices with an ordered vocabulary and provenance. A regenerated
reference is explicitly identified as regenerated: the original release did not
save full matrices. Validate it against the published document coefficients,
published term weights, source hash and dimensions; do not claim that historical
full matrices were recovered.

For subsequent reruns, align complete topic vectors by maximum-total-cosine
one-to-one matching and require every matched cosine to be at least 1 - 1e-8.
Also compare aligned document coefficients with explicit numerical tolerances.
Reject vocabulary or source changes. Ranked keyword strings are not a numerical
equivalence test.

Group exactly equal sparse TF-IDF columns on the full modeled corpus. Rank
groups by mean member topic weight, rounded to 10 decimal places, then by the
alphabetically first member. Report top-15 group-set Jaccard separately from
full-space cosine. This ranking convention is a display/measurement convention,
not an assertion that nearby weights are mathematically equal. Preserve group
membership across record-removal comparisons.

## Initialization comparison
Compare k = 4, 6, 8 using random seeds 0, 1, 2, 3, 4 and the existing NNDSVDa
seed-42 reference. Separate random-versus-random pairs from reference comparisons.
Primary summary: lower quartile of all matched topic cosines across random pairs.
Also report the minimum, median, full per-pair results, convergence and
reconstruction errors. These comparisons share a fixed dataset and are not
independent observations or population estimates.

Do not introduce a post-hoc pass threshold. Stability alone does not select k.
Review every component's leading groups and representative texts using the same
questions: Is there a specific linguistic pattern? Do examples support that
description? Are contradictions or formulaic repetitions disclosed? Retain
mixed components as mixed rather than forcing a semantic name. If numerical and
interpretive evidence do not distinguish candidates, report no unique winner.
Six components may remain an illustrative summary, not an established optimum.

## Topic-label descriptive contrast
Use frozen v2 labels without editing them. Predeclared mappings refer to the
published six-component reference: 1 -> P/H; 2 -> A; 3 -> I; 4 -> F; 5 -> G/X.
Do not change mappings after viewing contrasts. For each mapping, report n,
median, first and third quartiles for 0, 1 and u separately. No significance
tests, classifier performance, or independent-validity claims. Missing groups
remain visible. The sample was used for guideline development and non-blind
adjudication, and is balanced by decade rather than representative of the corpus.
Execution 117 belongs to this sample; 391 and 499 do not. All three have already
been inspected during interpretation, so none is new independent evidence.

## Evidence and deferred work
Recover inclusion decisions from upstream tables with evidence pointers. Use
unknown where reasons cannot be supported. Do not reconstruct undocumented
historical annotation edits as contemporaneous records.
Selected-prayer removal is a targeted influence check informed by the component,
not independent confirmation. Repeated prayers can define an algorithmic
component without establishing a substantive theme.
Broad k scans, bootstrap, coherence metrics and dominant-topic ARI are deferred
to keep this repair attributable and reviewable.
