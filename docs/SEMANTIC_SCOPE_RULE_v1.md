# Predicate inventory and task scope v1

## Status and provenance
Operational scope follows the owner's request to test the new rule directly,
after guided review of known examples. The accompanying 42-selection crosswalk
is AI-applied, not 42 new owner adjudications, independent validation or a
complete predicate inventory. Existing five-field labels remain historical.

## Task scope
Include propositions about acts causing or potentially causing harm, attribution
of acts, responsibility, innocence, and explicit evaluations of conviction or
execution. Include mental-state and reporting predicates when their content is
directly linked to those propositions. Preserve hypothetical and other-person
acts as contrasts: inclusion does not mean personal admission.

Exclude standalone affection, thanks, religious praise, wishes, forgiveness,
speech planning/closure, and procedural permission when they make no target
proposition. Preserve them as context. A request for forgiveness may contain a
separately eligible act: taking his life remains eligible even though hope and
forgive do not independently enter this narrowed task. Explicit causal harm
claims in an apology remain eligible. Names or religious language alone do not
determine scope.

An unresolved referent is not automatically a negative. Distinguish uncertain
task relevance (scope_uncertain) from uncertainty in a semantic field of an
otherwise eligible proposition. Both must remain visible in reporting.

## Unit procedure
1. Inventory predicates in source order, including matrix, embedded and relative
   clauses. Keep this inventory separate from target records.
2. Attach auxiliaries, negation and modals to the lexical predicate. Use a
   copular complement or conventional multiword predicate when appropriate.
3. Select independently expressed eligible predicates, not whichever verb seems
   important. A noun such as killer under call is a complement, not an invented
   independent killed or am predicate. An explicit he is a murderer is a
   different construction and remains eligible as an identity claim.
4. Record exact source offsets, inclusion/exclusion reason, arguments, governing
   frames and complete document context. Repeated occurrences retain positions;
   any linking of repetitions must be explicit, not silent deletion.
5. Assign the five semantic fields to the selected predicate only. Inclusion,
   polarity and truth presentation are different decisions. Requests and
   hypotheses can contain eligible predicates without asserting their events.

## Direct trial on known examples
| Example | Predicate | Result |
| --- | --- | --- |
| I take the full blame for this | take the full blame | Include responsibility, not a specified killing |
| They call me a cold-blooded killer | call | Include attributed characterization; retain killer as complement |
| I don't have anything to say | have ... to say | Exclude statement closure |
| You can proceed | proceed | Exclude procedural permission in this context |
| I don't understand why I did it | understand; did | Include linked knowledge and action separately; act identity unresolved |
| I hope he will forgive me for taking his life | taking his life | Include act; keep hope/forgive as context and inventory exclusions |

## Applied crosswalk
Run `python src/audit_semantic_scope_v1.py` from an environment with project
dependencies and the frozen model corpus. It validates 42 exact source spans
and applies an explicit manual crosswalk; it does not infer scope from raw text.
The script refuses to overwrite a different existing audit.

Results: 32 retain_scope; 5 exclude_scope; 4 scope_uncertain;
1 retire_representation. The retired historical characterization in execution 9
is preserved in the old record and as context of the existing call selection.
It is not a semantic correction to that old record.

Uncertain relevance: execution 147's doing this, execution 471's implicit belief
object, and execution 198's did this/chose this. These are not four new required
owner review tasks. Keep them out of any definite-scope denominator until a
versioned resolution exists. Report the exclusions; do not conceal them to
improve performance.

The 32 retained selections are not a test set, an exhaustive inventory, or 32
fully confirmed focus boundaries. The older diagnostic used 37 differently
selected units and cannot be compared to a score on these 32 as an improvement.

## Next stage
Freeze a method with an explicit focus input, using known development material
only. Then account for documented prior exposure and fix sampling before
opening the proposed new feasibility batch. Fresh owner references must be
prepared before predictions or AI label suggestions. This remains an owner-only
prediction-blind check unless a separate annotator contributes independently.
Do not add a model score or draw new evaluation text in this scope audit.
