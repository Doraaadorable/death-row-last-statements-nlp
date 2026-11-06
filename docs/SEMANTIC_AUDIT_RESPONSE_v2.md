# Semantic audit response and implementation status

Date: 2026-11-06. Post-audit development revision, not independent validation.

## Implemented
- Preserved v1 proposals, notebook 08, existing source files and frozen labels.
- Added a v2 draft guideline: polarity separate from assertion status, with
  presupposed kept distinct; explicit action versus characterization and
  unspecified wrongdoing versus unresolved event distinguished.
- Added 33 exact-span draft proposals (26 revised original selections plus
  seven additions). Removed only the out-of-scope general-freedom selection;
  its document remains. Mapping is a present-day proposal revision log.
- Notebook 09 uses shared decision validation, matches sorted owner rows by ID,
  supports UTF-8 BOM, validates IDs/evidence/source prerequisites, creates
  separate claim/document/addition sheets, and provides an explicit export.
- Export preserves all decisions, excludes deferred documents/claims from the
  adjudicated subset, records hashes and refuses overwriting existing exports.
- Correct first-time notebook prerequisite order: 05 -> 06 -> 07 -> 09.
  The previous package START_HERE instruction to begin at 06 was incorrect.

## Checks actually performed
Seven synthetic regression tests in tests/test_claim_adjudication.py passed:
owner-edit preservation with BOM and sorted rows, invalid values, revision
requirements, accept conflicts/missing reviewer identity, pending-export block,
changed-source preservation and hashed export/no-overwrite.
Notebook 09 cell bodies were executed directly in process, then rerun with
existing blank worksheets. This was not a separate Jupyter-kernel execution.
All 33 spans were checked against model_corpus_v1.csv, with positions/hashes.
No model refitting, new evaluation or independent annotation was performed.

## Remaining limitations and decisions
V2 is draft; owner approval to prepare it does not confirm individual rows.
Source/actor referents and assertion status still need semantic review.
Selections remain illustrative. Additional knowledge layers and policy claims
are not exhaustively annotated. A complete-reference task would need a
separate annotation pass with a fixed unit definition.
Owner additions have a template and an explicit export gate; incorporation,
source corrections and deletions require a new proposals version, not silent
merging. The actual owner-edited v1 CSV was not supplied, so no owner decisions
were migrated or reconstructed. Spreadsheet changes to immutable punctuation
are rejected to protect evidence, not repaired automatically.
Document worksheets are finalized at export rather than on every inspection.
Final artifacts are created locally; the user must explicitly stage intended
exports/manifests in Git to version them. There is no automatic Git commit of
private/local owner decisions. Worksheet hashes support later provenance only
when the generated exports are preserved. Neither Git hashes nor execution
success establish annotation validity or publication novelty.

## Audit interpretations not adopted automatically
Unused category values are not defects by themselves. An arbitrary preceding-
sentence-only reference window is not imposed. Agent nouns remain distinct
from action predicates. Presupposition is retained, not silently collapsed
into direct assertion. No fixed count such as 20 or 40 cases guarantees a
valid evaluation; sampling and uncertainty analysis require a later protocol.
