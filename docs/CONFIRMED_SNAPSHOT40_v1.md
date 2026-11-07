# Consolidated snapshot v1: 40 owner-confirmed selected propositions

## Current entry point
Use notebooks/14_confirmed_snapshot40.ipynb. This consolidates the previously
confirmed 37 selections, two #287 mental-state additions and one #198 choice
addition. It is not a new annotation round and does not ask the owner to
repeat forty decisions. Original records, notes and IDs remain intact.

The tracked reports/semantic_confirmed_snapshot40_v1.csv is a readable snapshot.
The notebook reproducibly creates separate local snapshot CSV and manifest
under data/processed, with frozen-source checks and exact evidence/focus offsets.
Existing local outputs must match exactly; differing files are not overwritten.
Older owner worksheets are never silently read, overwritten or reconstructed.
Creation time in the manifest means actual materialization time, not a
fabricated historical decision time. Historical message times remain unrecorded.

## Two distinct confirmation states
All 40 five-field semantic tuples were confirmed after guided AI-assisted
owner discussion. No semantic values changed during consolidation.
Ten predicate focuses have explicit confirmation: seven resolved audit cases,
two #287 mental-state additions and the new #198 chose addition.
Thirty focus mappings are still AI proposals. This does not retract their
semantic decisions, but these offsets cannot be called owner-confirmed gold
focus annotations or used as independent evaluation inputs.

The two original mental-state focus spans, seven audited focus decisions,
repeated predicate occurrences and the choice addition are checked separately.
A nominal/property predicate can be a focus; a finite verb is not mandatory.
The complete evidence and context remain necessary for source and scope.

## Candidate selection backlog
reports/predicate_candidate_backlog_v1.csv retains six potential additional
predicate selections identified during guided review: made, the second shot,
feel sorry, call, the first did and the first happened in their respective
units. Their inclusion, exclusion or merging has not been adjudicated. They
are not automatically added to the forty or silently discarded. This list
is not an exhaustive inventory of every predicate in all 21 statements.
The chose candidate was resolved by the owner and is now in the snapshot.

## Version boundaries
- Notebook 11: original 37 confirmed selections.
- Notebook 12 / diagnostic v1: comparison on those 37 selected spans.
- Notebook 13 / audit v1: 39 selections, with seven historical focus questions.
- Current snapshot: 40 semantic decisions, with ten confirmed focus positions.
These are different development artifacts, not interchangeable sample sizes.
No historical result is overwritten or recomputed by the new snapshot.
The old 40-page v2 booklet has outdated status labels and pending flags;
it is historical, not the current review queue.

## Validation actually performed
Six synthetic integrity tests passed: exact counts/repeatability, local-edit
preservation, duplicate rejection, conflicting focus rejection, changed evidence
rejection and protection of earlier worksheets. Snapshot evidence is checked
against the frozen corpus. Notebook cells were directly executed in process,
not via an independent Jupyter kernel. This is structural validation, not an
independent judgment that all semantic annotations are correct.

## Next research gate
Do not keep tuning rules until these known examples are perfect. Before any
new model comparison, freeze the operational task and decide whether the unit
is supplied as a span/focus or extracted automatically. Supply comparable
inputs to methods, account for known exposure, group related material by
execution ID, and define an independent reference/evaluation procedure.
Forty selections are neither forty people nor complete annotations of their
source statements. They do not establish guilt, sincerity, prevalence,
inter-annotator agreement, generalization or publication novelty.
