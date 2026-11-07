# Exposure readiness and prospective sampling v1

## Completed metadata audit
The prepared corpus has 479 documents. The unchanged literal screen produces
128 cue candidates and 351 nonmatches. Prior exposure is reconstructed from
the original 50 annotations, 21 semantic development documents, three pilot
documents, 45 IDs explicitly listed in the component review, and 16 IDs from
known conversation examples. These sources overlap; counts are not additive.
The reconstructed conversation list is incomplete, not a full reading history.

| Old cue stratum | Documented prior exposure | Exposure unknown | Total |
| --- | ---: | ---: | ---: |
| Candidate | 36 | 92 | 128 |
| Nonmatch | 80 | 271 | 351 |
| Total | 116 | 363 | 479 |

The report records IDs, source hashes and exposure categories, without statement
text. One documented source ID, 82, is outside the 479 prepared documents and
therefore contributes to neither prepared stratum. All 479 were available in
the unsupervised workflow; 477 had nonzero features. Unknown reading exposure
does not mean untouched by the whole project or proven unseen by the owner.

## Frozen next-batch plan, before drawing IDs
This is a 20-document feasibility batch, not an adequate-power guarantee or a
corpus prevalence sample. Exclude all documented prior exposure. Sample ten
IDs without replacement from each remaining stratum (92 and 271 documents).
Use Python `random.Random(20261107)`, call `sample` on the ascending candidate
ID list first (k=10), then on the ascending nonmatch list (k=10), using the same
generator. Display candidate IDs then nonmatch IDs, ascending within each group.
Record the realized IDs, code/source hashes and execution environment when
drawing. Inclusion probabilities conditional on these frozen pools are 10/92
and 10/271, not probabilities for all historical executions.

If the pools change, stop and version the plan before drawing. If a selected
statement is recognized later, retain it, flag exposure and report separately;
do not replace it. No new IDs have been drawn in the readiness report.

## Reference workflow
Keep texts and blank owner fields separate from method predictions. Prepare
predicate inventories and scope decisions before assigning semantic reference
fields. The owner sees full context, but no AI-proposed labels or B2 answers.
Allow deferred/unclear decisions and explicit scope uncertainty. Do not silently
discard difficult documents. Record owner recognition at document level.
Freeze references before running B2. Owner-only annotations blind to predictions
are not independent second-annotator validation or agreement evidence.

All units from one document remain together. Unknown exposure and boilerplate
overlap remain limitations. Report counts and abstention by stratum; do not
reuse this batch for tuning and still call it a held-out evaluation.

## Reproduction
`python src/build_evaluation_exposure_v1.py` rebuilds the metadata readiness
report and refuses to overwrite a changed record. It needs the released frozen
model corpus and original annotation CSV in their project locations.
No labels, corpus files, previous methods or outputs are modified.
