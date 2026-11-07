# Selected-span rule diagnostic v1: development observations

## Design and result
The protocol was committed as 8073557 before this run, but was already informed
by all known examples and annotation discussions. It is not preregistration.
Both methods receive selected text and bounded preceding context, never IDs or
reference fields. The same killing lexicon is used. B0 checks lexical mention
and negators; B1 adds a bundle of agency/attribution/frame constraints and can
abstain. This is a target-class diagnostic, not automatic five-field annotation.

Inputs: 37 manually selected propositions. References: 1 personal killing
admission, 2 personal killing denials, 31 clear contrasts, 3 uncertain references.
These units are not 37 people, complete statements or independently annotated
examples. Human span selection provides an oracle advantage.

| Method | Match on clear references | Disagreement | Abstention on clear references | Uncertain reference |
|---|---:|---:|---:|---:|
| B0 lexical | 28 | 6 | 0 | 3 |
| B1 constrained | 30 | 0 | 4 | 3 |

B0's six disagreements are false personal admissions on a hypothetical killing,
a reported killer characterization, two imperatives, a self-directed execution
accusation and a rhetorical death attribution. B1 separates these examples
but abstains on four clear contrasts: #450's knowledge/embedded did-it frame,
#471 blame, #287 attributed did-this and #60 responsibility.
Zero observed disagreement among decided B1 rows is not proof of accuracy:
B1 decides fewer rows, the material is selected and seen, there are only three
clear targets, and rules were handcrafted using the observed failure types.
B1's four abstentions must remain visible rather than being counted as correct.

## Diagnostic files
results/selected_span_diagnostic_v1/claim_comparison.csv contains 74 rows:
one per method per selected proposition, with reference tuple, prediction,
rule reason, outcome, and unchanged old-screen span/document cue hits.
reference_prediction_counts.csv and outcome_counts.csv retain raw counts.
manifest.json records code, inputs, protocol and output hashes.
The manifest's original environment describes the saved run; reruns preserve
it and refuse changed code/data/results in the same result version.

## Limitations and next decision
Rules handle only a small selection of constructions. Anaphoric admissions
such as I really did it are not resolved; they may be missed or abstained on.
The bounded context window is not a validated source-attribution parser.
Nested negation, quoted material, modality, multiple predicates and transitive
voice remain potential failures. Current behavior is a development fixture,
not ready for use in a legal decision or psychological inference.

The old cue screen is left unchanged. Span cue coverage cannot establish
whole-document recall, and document cue hits do not prove correct span retrieval.
No claims outside these selected units are labeled negative. No accuracy/F1,
confidence intervals, population prevalence or statistical superiority is claimed.

Nine synthetic behavioral tests passed. Notebook 12 code cells were executed
in process, not through a separate Jupyter kernel. The diagnostic runner was
executed twice, including its repeat-preservation path. No new texts were
opened, model fitted, reference labels changed or rule tuned after these outputs.
Next inspect the four abstentions and six lexical errors with the owner,
then plan independent annotation and an ID-disjoint evaluation separately.
