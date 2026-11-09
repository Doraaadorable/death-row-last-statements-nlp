# Proposition status v3: owner-approved simplification, draft application

The owner agreed to remove presupposed from the exclusive status field and
retain background attribution in notes. This changes the coding scheme, not
source statements or the frozen eight-label annotations. Earlier owner decisions
remain evidence of development adjudication, not independent blind annotation.

## New field
Replace assertion_status with proposition_status:
- presented_as_true: the selected source presents the proposition as holding,
  whether as a direct claim or clearly adopted background. This records textual
  commitment at the selected source layer, not verified truth or legal guilt.
- nonasserted: hypothetical, questioned, wished or requested content that is
  not presented as holding at the selected layer.
- unclear: textual commitment cannot be resolved reliably.

A wish/request governing one proposition does not make every embedded event
nonasserted. Forgive me for taking his life requests forgiveness but presents
life-taking as background. Conversely a bare hope that an event occurs does
not establish that event as holding. Resolve each selected proposition in context.

Embedding is not automatically presupposition. Future time is not automatically
hypothetical or nonasserted. A confident future claim may be presented_as_true.
A statement attributed to others can be presented_as_true at their layer without
being endorsed by the narrator. Claim_source and proposition_status stay separate.

## Unchanged fields
claim_source: self / other / unclear.
event_type: killing_action / knowledge / wrongdoing_unspecified / other / unclear.
event_actor: self / other / unspecified / unclear.
polarity: affirmed / negated / unclear, about predicate negation, not truth.
The v2 event/reference rules otherwise apply: characterizations are distinct from
killing action, shot/injection alone does not establish death, and unresolved
this/it is not silently filled from case assumptions. Retain full-statement context.

## Mappings and review scope
Most v2 asserted and presupposed selections map to presented_as_true, but this
is a reviewed development mapping, not a universal linguistic conversion rule.
The two know-frame backgrounds (#147 murderer and #287 molestation denial)
retain their conversation-confirmed background readings in notes.
Imperatives (#383/#390) and the hypothetical killing (#542) stay nonasserted.

Only the anticipated-execution selection v2-dev21-011 (#390) is proposed to
change from nonasserted to presented_as_true: in context the speaker presents
execution as a settled expectation. This value is explicitly pending owner
confirmation, not silently finalized by the schema approval. Do not use whether
an event already happened to settle proposition status.

The four original pilot decisions remain confirmed under their earlier scheme;
this file does not migrate them or manufacture new decisions. Current 33
selections are illustrative, not exhaustive. #524's event-occurrence addition
remains outside these 33 pending a separate versioned selection decision.

## Versioned workflow
Notebook 10 and claim_adjudication_v3.py create separate v3 worksheets; v2
notebook 09 and worksheets remain intact. Prerequisites remain 05 -> 06 -> 07.
The input and mapping tables preserve stable previous_claim_id links.
New v3 local fields begin blank because the owner's actual local worksheets
are unavailable here. Blank does not retract earlier conversation confirmations.
Reconcile accepted prior decisions by ID with the tracked conversation record;
do not ask for semantic re-review of unchanged items. Record actual transfer
reviewer/time separately rather than inventing past message timestamps.

Accept / revise / defer, explicit document review, source evidence protection,
notes and hash-verified exports follow the v2 workflow with proposition_status
in place of assertion_status. The three controlled status values exclude
presupposed; its evidence remains in review_note. No model is trained or
performance measured by this change. The old 40-page v2 booklet is historical;
use the v3 field definitions for further status decisions.
