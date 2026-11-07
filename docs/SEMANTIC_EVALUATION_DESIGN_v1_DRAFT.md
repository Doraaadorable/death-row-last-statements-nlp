# Next semantic evaluation: design v1 (draft, not executed)

## Status
Prepared after 42 known development selections and diagnostic v1. This is a
prospective plan for a new round, not retroactive preregistration.
No new statements, predictions or reference labels are opened by readiness work.

## Primary task and unit
Conditional proposition classification: given complete prepared context, a
selected evidence span and an exact predicate focus, classify the selected
proposition as personal killing admission, personal killing denial or other.
Retain unclear reference decisions separately. This does not evaluate automatic
predicate discovery, exhaustive extraction, actual guilt or psychological state.

Reference eligibility: killing_action + self source + self actor +
presented_as_true; polarity separates admission/denial. Preserve the five
reference fields so disagreements can be traced. Any genuinely unresolved
required field remains uncertain, not an ordinary negative.

## Reference preparation before predictions
Use a fixed, versioned predicate inventory rule in each sampled document.
Record candidates in textual order, include/exclude decisions and reasons,
auxiliaries/multiword predicates, repeated mentions and exact offsets.
Avoid importance-based selection. Complete source context remains available.
Because unit selection is human-supplied, report the oracle input explicitly.
Provide the same span/context/focus to all compared methods.

For the next feasibility annotation round propose 20 documents: ten from the
unchanged cue-candidate stratum and ten nonmatches, without replacement from
the remaining pool. Record a fixed seed, stratum sizes and selection
probabilities before opening text. If either stratum is too small, revise the
plan before sampling, not silently redraw. These 20 are a feasibility batch,
not a promise of adequate evaluation positives or a prevalence estimate.
No IDs are sampled or text opened by the current readiness script.

Exclude documented prior reading/development IDs. Remaining exposure is unknown,
not proven unseen. If the owner recognizes a sampled statement, record it and
retain it as exposed; do not replace interesting or inconvenient examples.
Prior corpus-wide NMF fitting is disclosed and supplies no target predictions.

Owner may prepare fresh references without AI suggestions and before seeing
method outputs: describe these as owner-only annotations blind to predictions,
not independent second-annotator validation. An uninvolved annotator would
strengthen reference credibility; retain separate annotations before
adjudication if a second annotator is available. Agreement cannot be inferred
from AI-assisted confirmations or a single annotator.

## Methods and leakage control
The existing B0/B1 diagnostic and its hashes remain frozen. They have no
explicit focus input and are not yet a focus-aware implementation.
Define and freeze any focus-aware baselines before new reference comparisons;
record whether a baseline ignores the supplied focus rather than concealing
unequal inputs. Do not tune on evaluation outputs.
All statements, spans, repeated mentions, edits and synthetic variants from one
execution remain in one partition. Audit near-duplicate wording across groups;
do not claim that a simple hash eliminates semantic or boilerplate overlap.
The prior 42 selections and three pilot documents are development-only.

## Reporting and stop conditions
Report raw reference/prediction counts, target counts and abstentions, separately
for both sampling strata and unresolved/exposed cases. Do not report macro
accuracy alone against many contrasts. If a class is absent, its recall is
undefined; very small target counts support descriptive cases, not a strong
generalization claim. Any weighted corpus inference requires a separate
sampling/variance analysis, not ordinary binomial intervals on weighted rows.
Do not interpret 20 documents or any arbitrary positive-count threshold as
guaranteeing statistical adequacy.

Proceed to evaluation only after reference-unit rules, method versions, exposure
accounting and prediction-blind annotation procedure are fixed. Until then
readiness artifacts are metadata, not a new test set. Automatic extraction,
model training, corpus recall and novelty claims remain separate questions.
