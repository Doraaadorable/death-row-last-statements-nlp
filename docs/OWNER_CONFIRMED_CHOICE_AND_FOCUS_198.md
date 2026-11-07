# Owner-confirmed choice addition and focus boundaries

## Execution 198: two distinct propositions
After being asked to confirm both decisions, the owner responded affirmatively.
Retain the existing v3-dev21-027 record centered on did, with unchanged semantic
fields. Its larger evidence span I did this, I chose this remains available.
Add a separate choice proposition:

- claim_id: owner-added-198-choice-01
- execution_number: 198
- evidence_span: I chose this
- span_start: 633
- span_end: 645
- predicate_focus: chose
- focus_start: 635
- focus_end: 640
- context_sha256: 98322718d9dd735f9d7ae971d2316f22adf609dc2eb4e3f140300b7c4d335336
- claim_source: self
- event_type: unclear
- event_actor: self
- polarity: affirmed
- proposition_status: presented_as_true
- owner_decision: accept
- process: AI-assisted discussion, not blind annotation
- historical message timestamp: not recorded

Offsets are zero-based/end-exclusive and checked against frozen model_text.
The choice object remains unresolved. Do not infer choosing crime, waiving an
appeal, accepting execution or actual intent. The two this references must not
be assumed identical without evidence. Two proposition rows are not two people
or proof of two separate physical events.

## Focus confirmations from the same guided review
The owner explicitly accepted these offsets/conventions in notebook 13's audit:
- v3-dev21-014 (#9): first shot, speaker shooting; second shot remains context.
- v3-dev21-007 (#451): hurt, not embedded made.
- v3-added-006 (#287): murdering, not feel sorry.
- v3-dev21-027 (#198): did, with choice separated as the addition above.

These focus decisions do not automatically approve adding every contextual
predicate. Made, the second shot, and feel sorry remain candidate selections
requiring a consistent scope decision rather than silent exclusion.

## Version scope
There are now 40 confirmed selected development propositions: original 37,
two #287 know/think additions, and this choice addition. This is a conversation
record, not a silent update of the earlier decision CSV or local worksheets.
Notebook 11 and diagnostic v1 remain on 37; notebook 13 audits 39 and its
published outputs remain unchanged. A later merged release must reconcile
these additions and owner edits explicitly. No result has been rescored and no
performance estimate follows from these confirmations.
