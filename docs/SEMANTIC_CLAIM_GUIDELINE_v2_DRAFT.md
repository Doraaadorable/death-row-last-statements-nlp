# Claim interpretation guideline v2: post-audit draft

Date: 2026-11-06. Owner authorized preparing a revision, not automatic acceptance
of its individual proposals. This draft follows AI-assisted discussion and a
third-party AI review; it is not preregistered or independent annotation.
The four original pilot decisions remain owner-confirmed under their original
scheme. No frozen eight-label annotation, v1 proposal, selection or screen changes.

## Task and scope
The narrow target is a speaker-owned proposition affirming or denying the
speaker personally taking a human life. Universal denials, particular events
and particular persons qualify. Relation to the conviction must be recorded
only when established by supplied context; it is not a requirement for inclusion.
Innocence status, other offenses, responsibility, knowledge and execution
criticism remain distinct contrast material, not automatically killing claims.
The 33 proposed rows are illustrative, not exhaustive. Their counts cannot
establish prevalence, recall or annotation agreement.

## Unit and context
A row selects one predicate in full prepared context. The evidence span can
retain an enclosing clause to preserve attribution, unique matching or negation;
its note must identify the selected predicate. Minimal surface spans alone do
not settle attribution. Multiple predicates may have separate rows if useful,
but the current selections are not a predicate-complete annotation.
Resolve references within the full statement, using relevant earlier or later
text; record the support. Never fill missing references using assumed case facts.
Nesting, requests, conditionals and transcription anomalies remain in notes.

## Controlled fields
- claim_source: self / other / unclear. Whose selected claim or attributed view
  is presented. Reporting does not establish truth or the narrator's endorsement.
- event_type: killing_action / knowledge / wrongdoing_unspecified / other / unclear.
  Killing_action requires a proposition about taking a human life, including
  execution when expressed that way. Shot or poison alone does not establish
  death. Agent nouns killer/murderer are killing-related characterizations,
  retained as other unless a particular action proposition is selected.
  Knowledge includes acquaintance; explain its object. Speech-planning formulae
  such as not knowing what to say are other, not crime-knowledge evidence.
  Wrongdoing_unspecified covers alleged crime, blame or case responsibility
  where wrongdoing is established but the act is unspecified. Innocence status
  is other. Unresolved did this without established wrongdoing is unclear.
- event_actor: self / other / unspecified / unclear. Actor or knowledge holder
  within the selected proposition. Generic anyone is unspecified. Uncertain
  individual identity does not force unclear when all candidates are other.
- polarity: affirmed / negated / unclear. Positive versus negated selected
  predicate, not factual truth. Governing negation of know/think/forgive does
  not automatically negate embedded killing. Unclear is genuine unresolved scope.
- assertion_status: asserted / presupposed / nonasserted / unclear.
  Asserted means presented as a claim at the selected attribution layer, not
  independently true or necessarily narrator-endorsed. Presupposed preserves
  self-attribution embedded in a forgiveness/reason frame. Nonasserted covers
  hypothetical, requested or anticipated event content; note which one.
  These are operational development categories, not a complete theory of factivity.

## Interpretation rules
Presupposed self-attribution can support action attribution if the action itself
is explicit or contextually resolved; it must not be called a direct assertion.
Unresolved did it is not a killing admission. Do not automatically combine
asserted and presupposed in evaluation: report separately, and freeze that
choice before prediction. Imperatives can have affirmed polarity while being
nonasserted. General judicial criticism does not establish personal denial.
No field establishes actual guilt, motive, sincerity or psychology.

## Revision and known boundaries
reports/semantic_proposal_v1_to_v2.csv records current proposal evolution, not
historical annotation decisions. V1 general-freedom row #335 is removed from
this selection, but its document remains for owner review. Added rows cover
agent nouns, presupposed did it, denied restraint/injection, another offense,
and execution-as-murder. Known omissions still include policy claims and
additional embedded predicates. No completeness claim follows from the additions.
No-selection is document-level and needs an explicit owner decision; #141,
#335, #414 and #538 currently have no selected v2 row.

## Owner workflow and files
Run notebooks 05 -> 06 -> 07 before first running 09. Notebook 08 and its v1
worksheet remain unchanged. Notebook 09 creates separate v2 proposition and
21-document decision worksheets. It matches by claim_id, allows row sorting,
requires valid exact values, notes for revise/defer, reviewer ID and an ISO
 timestamp with timezone for decisions. UTF-8 BOM is supported; other encodings
are rejected without modifying the file. Changes to immutable evidence require
new proposals rather than spreadsheet corrections.

Use accept to accept proposed fields (optional agreeing owner fields), revise
to fill all five final fields with at least one change and a note, defer for
unresolved decisions and a note. Pending fields stay blank. A document-level
defer excludes its propositions from the adjudicated export. Exports are
versioned, hashed and never overwrite an existing export. They remain
AI-assisted development outputs, not independent gold standards.

Additions: use the separate additions template, record execution ID, exact span,
selected predicate and note; additions are proposals, never automatically
merged or counted. Send that file for a new proposals version before export.
This implementation does not silently migrate v1 owner edits: the actual local
v1 worksheet was not supplied. Keep it and reconcile manually if it contains
owner decisions. Source span changes and deletions also require a new version.
