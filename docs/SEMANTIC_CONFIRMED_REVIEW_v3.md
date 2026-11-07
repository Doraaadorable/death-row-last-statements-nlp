# Current semantic development review: 37 confirmed selections

## What is current
Use notebook 11_confirmed_semantic_review.ipynb for the current owner-confirmed
record. Notebooks 08, 09 and 10 are retained historical draft workflows and
must not be interpreted as the current number of pending decisions.
The owner has discussed and accepted 37 selected propositions: the original
33 plus event occurrence (#524), speech closure and permitted proceeding
(#538), and rhetorical death attribution (#335).

The final status field is proposition_status with presented_as_true /
nonasserted / unclear. Background/presupposition remains in notes.
The explicitly reconsidered #390 anticipated execution is presented_as_true.
For #335 other includes a non-speaker/nonhuman rhetorical cause; preserve the
agent note rather than inferring a particular human official.

The tracked record reports/semantic_owner_decisions_v3_discussion.csv is the
source of the discussion decisions. It records no fabricated historical time.
The preparation manifest records actual file-generation time separately.
This is AI-assisted owner development review, not blind independent annotation.
The old four pilot decisions and frozen eight-label v2 annotations remain intact.

## What notebook 11 does
Verify the frozen corpus hash, 37 unique IDs, membership in the 21 fixed IDs,
exact source spans/context hashes, allowed field values, owner confirmation
and process provenance. Join full prepared text and source URLs locally.
Create or verify identical local copies:
- data/processed/semantic_owner_confirmed_v3_37.csv
- data/processed/semantic_owner_confirmed_v3_37_manifest.json
- data/processed/semantic_document_scope_v3_21.csv
- data/processed/semantic_document_scope_v3_21_manifest.json

It reads no local owner worksheets from earlier versions, so owner edits to
those files are preserved rather than silently migrated. If an existing output
or its source/provenance differs, stop and version the change; do not overwrite.
The notebook can also inspect a selected claim together with full context.
Curated model_corpus_v1.csv is required; semantic screening need not be rerun.

## Document scope
Nineteen documents have selected propositions. #141 retains religious self-
evaluation in notes; #414 retains apology/religious forgiveness in notes.
Both nonselection decisions are owner-agreed task-scope decisions, not claims
that those statements contain no propositions or no meaningful content.
Selected rows and scope notes are not a complete predicate inventory.
No exhaustive document-review certificate is inferred from this preparation.

## Validation and remaining work
Five new synthetic integrity tests cover repeatability/old-file preservation,
local edit rejection, tampered spans, duplicate IDs/invalid values and invented
message times. They are not semantic accuracy tests. Notebook code cells were
executed directly in process, not in an independent Jupyter kernel.

Next, verify the notebook in the owner's environment, then specify a small
retrieval revision experiment before opening more documents. Preserve screen
v1; do not reuse these development decisions as an unseen test. Any subsequent
coverage/completeness audit requires explicit selection criteria and its own
record. Do not infer actual guilt, innocence, mental state, population
prevalence, agreement, novelty or generalization from the 37 decisions.
