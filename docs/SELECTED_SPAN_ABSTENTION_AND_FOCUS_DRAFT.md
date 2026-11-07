# Four abstentions: predicate-focus draft after diagnostic v1

## Provenance
Prepared after inspecting the saved v1 diagnostic. This is an AI-assisted
development proposal, not owner-confirmed focus annotation, preregistration,
or a revised performance result. Existing rules, 37 owner decisions and all
v1 diagnostic outputs remain unchanged.

## What the implementation actually does
All four clear-reference abstentions share unresolved_action_or_responsibility.
That rule is triggered by a did-it/did-this, blame or responsible expression
without an explicit killing cue. It does not parse the selected predicate or
resolve the full statement. It is inaccurate to describe the current B1 as
having identified four different semantic causes internally; the distinctions
below are the researcher's post-hoc interpretation of that shared trigger.

| Claim ID | Execution | Evidence | Proposed predicate focus | Interpretation of limitation |
|---|---|---|---|---|
| v3-dev21-002 | 450 | I don't understand why I did it. | understand | Knowledge predicate is selected; embedded did-it trips a broad ambiguity rule. Governing negation stays in evidence. |
| v3-dev21-009 | 471 | I take the full blame for this. | take the full blame | Responsibility is explicit; precise event unresolved does not automatically require abstention for an explicit-killing-only target. |
| v3-dev21-020 | 287 | I know you think I did this | did | Selected attributed action claim is inside two attitude layers. Knowing/thinking are context, not the selected predicate. |
| v3-dev21-025 | 60 | I was responsible for the '75 and '79 cases. | was responsible | Specified cases do not supply a physical act; a generic ambiguity rule withholds an otherwise task-specific contrast decision. |

The execution 60 evidence above uses straight apostrophes only for readable
discussion; authoritative source text has curly apostrophes and is unchanged.
Any machine annotation must use exact offsets against the frozen original.

## Focus is not another semantic outcome label
Predicate focus identifies the selected predicate in an evidence span. It does
not supply claim source, actor, event class, polarity or truth/commitment.
Keep full evidence, governing negation, reporting frame and entire statement.
A focus token alone is insufficient: understand without don't loses negation,
and did without you think loses source attribution.

The same did predicate can have self or other source and affirmed or negated
polarity. Therefore source attribution cannot be inferred from focus alone.

## Experimental boundary
Do not silently add human focus to B1 while retaining the same comparison
label. Manual predicate selection is additional oracle information.
If focus is used as input, give it to all compared methods and report the
conditional task explicitly, or evaluate automatic focus extraction separately.
Focus proposals are not independent annotations and cannot establish accuracy.
For now retain this as a documentation proposal only; no new model or rule run.

## Next decision
Confirm the four focus interpretations, then define an exact span/offset
convention before extending focus annotation. Do not require re-adjudication
of already accepted five-field decisions. Do not chase zero abstentions on
these 37 known examples. Independent evaluation still needs an ID-separated
sampling plan, exposure accounting and appropriate reference annotations.
