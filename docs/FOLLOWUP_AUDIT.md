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
follow-up manifest. The supplementary notebook is supplied without outputs;
its cells read the executed script outputs, and it has not been independently
executed as a notebook in this follow-up environment.

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
The inclusion ledger supports 480 included records and 102 exclusions based
on the inventory's shared-notice link category. For 21 additional absent
records, the upstream decision evidence is unavailable in the released
snapshot; their status remains unknown and their reason fields remain blank.
Link-category evidence does not establish the contents of a shared notice page.
Recover the upstream extraction and cleaning tables before resolving those rows.

No retrospective annotation change log has been fabricated. The v1-to-v2
history needs contemporaneous records or explicitly reconstructed provenance.
A complete dependency lock and independent fresh-environment execution of the
new notebook remain follow-up work. Existing notebook outputs describe an
older historical run. The supplementary notebook avoids personal paths and
contains no stored output.

## Interpretation corrections
The selected-prayer deletion is a targeted influence check informed by the
component's content. Losing that component after removing its supporting
records is expected, not independent confirmation. Formulaic prayer is an
NMF component driven by repeated expression form; whether it represents a
substantive research theme requires separate judgment.
