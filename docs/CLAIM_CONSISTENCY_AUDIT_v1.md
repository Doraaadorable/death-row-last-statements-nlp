# Consistency check after predicate-centered review: 39 selections

## Scope and actual checks
All 39 confirmed selections (37 plus the two #287 additions) were read into
one audit. Exact evidence offsets and context hashes, unique IDs and allowed
field values were checked. A manual AI-proposed focus plan was prepared for
each row. Audit code validates offsets for that plan; it is not a parser and
cannot prove the proposed focus or semantic interpretation correct.

No previous semantic values were changed. The audit table keeps them exactly,
then appends proposed focus offsets, notes and review priority. This is an
independent-of-model implementation check, NOT independent annotation.

## Findings
- 32 selections have no proposed semantic-field change and do not require a
  special boundary decision. Most new focus offsets within these rows are
  still AI proposals; the two #287 addition offsets were explicitly confirmed.
- 7 selections need an explicit focus-boundary convention. None is currently
  treated as a demonstrated semantic mislabel.
- No evidence in this audit justifies claiming exhaustive predicate selection
  across 21 statements, agreement, model accuracy or population performance.

| Claim | Focus clarification | Current label implication |
|---|---|---|
| #451 v3-dev21-007 | hurt, not embedded made | Retain harm attribution; decisions-made clause remains context. |
| #9 v3-dev21-013 | nominal cold-blooded killer, not call | Keep reported characterization. Centering call would be a different naming proposition with different source/actor roles. |
| #9 v3-dev21-014 | first shot, not relative-clause shot | Keep speaker shooting; the other man's shooting is a distinct candidate. |
| #198 v3-dev21-027 | did, with chose retained in evidence | Current span has two predicates. Proposed did focus preserves existing tuple; separately selecting chose requires a new selection decision. |
| #450 v3-added-002 | second did inside understanding/why frame | Disambiguate repeated evidence, retaining unresolved action and background note. |
| #287 v3-added-006 | murdering, not feel sorry | Keep execution accusation; sympathy remains unselected context. |
| #524 occurrence addition | matrix second happened | Keep event occurrence, not an inferred self-agent action. |

The appearance of another predicate does not automatically demand another
confirmed row. Candidate inventory, inclusion criterion and selected proposition
remain distinct. Conversely the existing five-field tuple does not establish
that every predicate inside the evidence was selected.

## Files and reproduction
reports/predicate_focus_audit_plan_v1.json is a manually prepared proposal with
explicit focus occurrence indices and provenance. It is not owner confirmation.
results/claim_consistency_audit_v1/ contains the combined audit, summary and
hash manifest. Both original decision CSVs are retained; no local owner
worksheet is read or overwritten. Run notebook 13 or src/audit_claim_consistency.py.

Five synthetic structural tests passed, including input/label preservation,
duplicate rejection, invalid focus occurrence, altered context and repeated
predicate resolution. Notebook cell bodies were executed in process, not a
separate Jupyter kernel. Diagnostic v1 remains on the original 37 selections;
this audit neither reruns nor improves those results.

## Decision before further modeling
Ask the owner about focus conventions for the seven flagged rows in small
batches. No need to repeat the five semantic fields for every row. If a focus
changes to a different proposition, do not overwrite the old row: select a new
version/row and re-adjudicate its fields. Later focus-assisted methods must
receive comparable inputs or evaluate automatic focus selection separately.
