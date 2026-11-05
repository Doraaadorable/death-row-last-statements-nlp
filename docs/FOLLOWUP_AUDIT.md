# Follow-up audit, 2026-11-05

## What changed
The protocol was committed as `2b4157c` before the new comparisons. It was
informed by the original results and audit discussions, not a preregistration
of the original project. Numerical repairs were committed separately as
`c7838f9`. The full 3,196-feature space and frozen annotations remain unchanged.

The shared feature module replaces runtime AST/exec extraction. The three
checks now write to new v2 diagnostic directories and compare numerical
weights rather than keyword order. Full regenerated unit-length topic-term
matrices and their ordered vocabulary are supplied under
`results/reference_numeric_v1/`. They were validated against the historical
term weights and document coefficients; no historical full matrix was available.
Later reruns additionally match full vectors with minimum cosine 1 - 1e-8.
Term weights use rtol=1e-8, atol=1e-12; document coefficients use rtol=1e-8,
atol=1e-10. Historical result files were not replaced.

Exactly equal columns form 90 non-singleton groups containing 275 features;
there are 3,011 groups in total. Grouping affects keyword overlap only, not
fitting. New Jaccard values measure top-15 group sets and are not interchangeable
with historical top-15 term-set Jaccard. Groups use mean member weight, rounded
to ten decimal places, then alphabetical representative as a ranking convention.

## Executed checks
In the recorded follow-up environment, all three repaired checks completed.
The follow-up script fitted 18 models: k=4/6/8, each with five random seeds and
one NNDSVDa reference. All converged. Short-text sensitivity was rerun against
the saved full matrices. Syntax compilation and a synthetic identical-column
and ranking check passed. Environment versions and input hashes are in the
follow-up manifest. The owner subsequently executed the supplementary notebook
and committed its outputs in `5bfe829`. Inspection of the committed artifact
found three code cells numbered 1 through 3, four display outputs, no stored
errors and no personal absolute paths. Its cells read saved script outputs;
this is not evidence of refitting models or independent notebook execution.

## Initialization results

| k | Minimum matched cosine | Lower quartile | Median |
|---|---:|---:|---:|
| 4 | 0.331396 | 0.916468 | 0.999991 |
| 6 | 0.054421 | 0.937597 | 0.999093 |
| 8 | 0.117624 | 0.861744 | 0.992966 |

These summarize matched components across all ten random-seed pairs per k.
They are not independent observations. Six has the largest lower quartile,
but also the weakest individual match. Four is not uniformly stable either.
The evidence does not establish a unique winning topic count. Reference-based
comparisons are kept in a separate table. Reconstruction captures approximately
7.3%, 8.7% and 10.0% of squared TF-IDF Frobenius norm for the respective reference
fits. This is not regression R-squared, semantic coverage, or topic validity.

## Descriptive contrasts with frozen labels
For the 50 development records, Topic 1 has median coefficient 0.181 for P=1
(n=22), versus 0 for P=0 (n=26); Topic 3 has median 0.145 for I=1 (n=8), versus
0.033 for I=0 (n=40). These examples describe the prespecified contrasts; the
complete table retains every specified mapping, all three coding values,
quartiles and group sizes. The data do not support an independent-validity
claim, classifier evaluation, or population inference. Execution 117 is in the
sample; previously inspected counterexamples 391 and 499 are not.

## Remaining evidence gaps
The original v1 ledger left 21 absent records unknown because upstream
cleaning evidence was missing from the Release. That evidence has now been
extracted from the owner's local cleaning table and committed in
[the 21-record evidence table](../reports/inclusion_evidence_21_v1.csv), with
the upstream file's SHA-256 and original cleaning notes. The full upstream
table and raw HTML remain outside the Release.

The [v2 ledger](../reports/inclusion_ledger_v2.csv) records 480 included and
123 historically excluded records: 102 shared-notice links, 13 reports of no
statement, four ambiguous short responses and four summaries or references.
Here excluded denotes documented exclusion from the frozen candidate corpus,
not a claim that the exclusion rule has been independently validated.
Link-category evidence alone does not establish shared-page content.

The owner's supplied cached-page text does not resolve speaker attribution
for executions 463, 533, 539 and 567 (No/None). They remain excluded with an
explicit unresolved-attribution flag. Execution 241 reports the translation
Goodbye and is a future inclusion candidate; its treatment should be reviewed
against other supplied translations. No frozen corpus, annotation or model
was changed. The historical v1 ledger remains available. The baseline ledger
script still regenerates v1; v2 construction is documented in the
[inclusion-review notebook](../notebooks/03_inclusion_review.ipynb) and requires
the upstream cleaning table, which is not bundled in the Release.

No retrospective annotation change log has been fabricated. The v1-to-v2
history needs contemporaneous records or explicitly reconstructed provenance.
A complete dependency lock and independent fresh-environment execution of the
new notebook remain follow-up work. The main analysis notebook retains its
historical outputs; the supplementary notebook now includes the owner's
executed outputs without personal paths.

## Interpretation corrections
The selected-prayer deletion is a targeted influence check informed by the
component's content. Losing that component after removing its supporting
records is expected, not independent confirmation. Formulaic prayer is an
NMF component driven by repeated expression form; whether it represents a
substantive research theme requires separate judgment.
