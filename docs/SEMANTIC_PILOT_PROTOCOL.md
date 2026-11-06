# Semantic interpretation pilot: development protocol
Date: 2026-11-06
Status: working pilot, informed by observed examples; no independent test

## Focused question
Can a method distinguish a speaker's own explicit denial of personally
performing a killing from an externally attributed denial, a negated statement
about knowledge, and an explicit admission?

The target is an expressed proposition in context, never actual guilt,
innocence, sincerity or a psychological diagnosis. This is a narrower target
than the frozen innocence_dispute label, which includes other disputes.
Do not reuse the eight frozen labels as gold labels for this task.

## Why start small
Four selected spans from previously read executions 117, 391 and 499 provide a
feasibility check. They were chosen because they exposed the current lexical
boundary, not sampled randomly. They are development material, not an unseen
test set. No method performance estimate can be obtained from four cases.

## Unit and context
The review unit is a selected claim span together with the complete prepared
statement and source URL. Keep punctuation, quotation/reporting cues and
negation; do not use stopword-filtered text as human evidence.
A span may be a clause rather than a complete sentence. Preserve zero-based,
end-exclusive source offsets and a hash of the prepared context.

The two spans selected from execution 499 need the surrounding reporting cue
and antecedent to interpret who said what and what it refers to.
Selecting a small phrase does not authorize ignoring its context. No automatic
coreference resolution is assumed.

## Pilot fields
Leave every annotation blank until reviewed. Blank means not yet reviewed,
whereas unclear means reviewed but unresolved.

| Field | Allowed values | Meaning |
|---|---|---|
| claim_source | self / other / unclear | Whose claim is presented in context? Grammatical I alone does not settle this when others are being reported. |
| event_type | killing_action / knowledge / other / unclear | What proposition is affirmed or negated? A crime-intent dispute is not automatically a denial of personally performing the act. |
| event_actor | self / other / unspecified / unclear | Who performs the action or holds the knowledge inside the proposition? This is separate from the source of the claim. |
| polarity | affirmed / negated / unclear | Is that proposition affirmed or negated? Do not transfer negation across verbs or outside reported content. |
| review_note | free text | Evidence, referring expressions and remaining ambiguity. |

These categories describe the selected spans and do not label an entire person
or statement. A statement can contain both reported denial and the speaker's
own admission without logical contradiction between those two attributed claims.

Religious/metaphorical killing, wishes about future death, execution-policy
criticism, descriptions of another actor and unresolved references must not be
silently converted into the target claim. In a larger dataset, absence of a
target denial requires reviewing the defined context; absence of an extracted
keyword hit does not establish absence of such a claim.

## Procedure
1. Run notebook 05 and read the definitions before filling any fields.
2. Review the four spans with full context; keep unresolved cases unclear.
3. Discuss guideline problems and revise this pilot protocol transparently.
   Do not edit frozen v2 labels or create a retrospective historical log.
4. Only after the target is workable, plan candidate retrieval and evaluation.
   No classifier, embedding model or prompt comparison is selected here.

## Later evaluation requirements
If a comparative experiment is justified:
- Record a dated protocol version and sampling plan before new predictions.
- Separate corpus coverage from a deliberately difficult challenge set.
- Freeze a development/evaluation partition by execution ID. Keep all spans,
  edited variants and paraphrases of one source in the same partition.
- Known examples, previously read documents and uncertain exposure histories
  cannot be called independently unseen owner evidence.
- Seek independently prepared reference annotations where feasible; a second
  AI reviewing labels it has seen is not blind human agreement.
- Publish raw confusion counts and bucket sizes for the defined target;
  report precision/recall only when supported by labeled denominators.
  Report uncertain/reference-excluded cases and abstentions separately.
- Compare task-matched baselines. Existing NMF coefficients are not class
  predictions, so their apparent classification failure is not a fair
  benchmark against a trained classifier.
- Keep synthetic contrast examples separate from authentic statements and
  explicitly label their provenance. Diagnostic success is not population
  performance, and publication novelty remains to be checked.

## Stop conditions
If source attribution cannot be resolved consistently, narrow the target or
remain with a descriptive audit. If too few authentic cases support evaluation,
report that limitation instead of training on four examples or manufacturing
a claim of generalization.
