# B2 focus-aware rule baseline v1

## Status
Known-example-informed development baseline. Published before selecting or
opening the next evaluation batch. This is not a pretrained language model,
semantic parser, automatic predicate extractor or validated five-field coder.
The older B0/B1 files and results are preserved.

## Contract
`focus_rules_v1.predict(context, focus_start, focus_end)` receives complete
prepared text and a nonempty half-open character interval for a human-selected
predicate. The caller must check the selected substring against its intended
predicate. Returns `(admission|denial|other|abstain, reason)`.
Human-supplied focus is additional oracle input. B0/B1 lack that input and are
not automatically comparable under an identical-information claim.

## Rules
Only selected explicit killing predicates or explicit life-taking constructions
can produce admission or denial. Selected knowledge, naming and shooting
predicates produce other for this narrow killing task; this does not say their
statements are unimportant or out of the larger scope inventory.
Implicit did/chose/happened and responsibility expressions abstain. Bounded
prefix reporting and modal cues also trigger abstention, not a confident source
or status label. Direct first-person action and passive life-taking by me are
recognized, with negation attached to the recognized local construction.
An explicit forgive-me-for-taking-life frame has a narrow special rule.

The context is supplied in full but the method uses heuristic windows: at most
180 preceding characters since a `. ! ? ;` boundary and 100 following
characters until such a boundary. This is not reliable clause segmentation.
Reporting cues can over-abstain or be missed beyond the window. Coordination,
long-range dependencies, quoted speech, unfamiliar paraphrases and nonliteral
uses are not solved. First-person patient recognition is only a narrow pattern.
Negation has no general syntactic scope analysis. No reference labels or
execution IDs enter the prediction function.

## Checks performed
`python -m unittest discover -s tests -p test_focus_rules_v1.py`
passed 12 behavioral checks: explicit denial, unrelated trailing negation,
self-patient, different selected predicates in one sentence, reported denial,
hypothesis, passive, implicit act, characterization, shooting, forgiveness frame
and invalid interval. These fixtures are known-example-informed synthetic
checks, not held-out observations or a complete correctness proof.

A local smoke run checked exact focus substrings and executed the 32 retained
known selections from semantic_scope_audit_v1.json: 16 other, 1 admission,
2 denial and 13 abstain. These are prediction counts, not correctness counts.
Some existing focus positions remain AI-proposed. No accuracy, recall or
improvement over the differently selected 37-record diagnostic is claimed.

## Next evaluation controls
Freeze this code version before new reference comparisons. Any revision after
examining new evaluation errors must get a new version and may not be evaluated
as if it had been fixed beforehand. Keep selection/exposure accounting,
predicate inventory, scope decisions and reference annotations distinct.
No new documents were selected and no new reference labels were prepared here.
