# Selected-span rule diagnostic v1: development protocol

## Status and timing
Written after all 37 selections and owner discussions were seen, before running
this particular rule comparison. Audit-informed development design, not
preregistration or an independent evaluation. No unseen texts are opened.

## Question and units
Can two transparent rules separate personal killing admissions/denials from
the selected contrast propositions? Input units are the 37 human-selected
evidence spans plus complete prepared context, not automatically extracted
sentences. Manual span selection is an oracle advantage. This is NOT end-to-end
retrieval or classification performance on the 479-document corpus.

Reference target: event_type=killing_action, claim_source=self,
event_actor=self, proposition_status=presented_as_true. Polarity distinguishes
admission from denial. All clear non-target combinations are other.
Any unclear required field is reference_uncertain, retained separately,
never silently turned into other or omitted without reporting.

## Comparisons
B0 lexical: identical killing lexicon for both methods; use kill/murder/execute
word families or taking-life phrases. A first-person mention plus such a cue
produces admission or denial according to a negator anywhere in the span.
Otherwise other. This is a deliberately simple lexical baseline, not a grammar
model and not the old NMF. A first-person mention need not be an agent.

B1 constrained: same lexicon, plus direct first-person act patterns, passive
by-me life-taking, and self-attribution in forgiveness frames. Reporting and
hypothetical/imperative frames can prevent personal-action predictions.
Unresolved did-it/did-this or responsibility without a specified act abstains.
No fitted parameters, labels, claim IDs or execution IDs enter either rule.
Rules are known-example-informed and incomplete. Context handling uses a
bounded preceding sentence fragment, not a validated parser/coreference model.

Also apply the unchanged original semantic-screen regex to each selected span
and its whole document. Describe cue hits on selected material only. Those
rules were built for document screening; this is no claim of retrieval recall.

## Outputs and reporting
Record each method output, rule/reason, reference tuple and disagreement by
claim ID. Show raw reference/prediction count tables, abstentions and uncertain
reference rows separately. No headline accuracy/F1, confidence interval,
population recall or claim of generalization. Do not use 37 rows as 37 people.
Only a few target instances exist; do not claim statistical superiority.
Shared lexicon controls lexical coverage; B1 remains a bundle of several
constraints, so improvements cannot be attributed to one constraint.

## Preservation and next gate
Keep source, frozen labels, prior screens and outputs unchanged. New diagnostic
outputs are versioned with source/code/protocol hashes. Changing rules after
seeing these outputs requires a new version and an explicit change log.
Before independent evaluation: freeze the unit/target, group by execution ID,
account for previous exposure, define complete reference sampling and
independent annotation. This diagnostic does not itself supply those.
