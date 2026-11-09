# Known-development field comparison v1

## Scope
Run the unchanged parser and partial semantic converter on the documents
containing 42 reviewed development selections. Compare only
identical predicate character intervals. Do not use the 20-document smoke
sample as though it contained these reference selections. This run parses the
21 known reference documents separately; it draws no new documents.

Four alignment/accounting checks passed. Exact matching prevents repeated words
or contained single-word heads from silently replacing multiword reference
foci. Input/code/model fingerprints accompany the output. No reference labels,
focus positions, task-scope decisions, parser rules or converter rules changed.

## Alignment
37 exact matches; five have no identical parser interval. The five are take
the full blame (#471), cold-blooded killer (#9), am innocent (#375), was
responsible (#60), and is a murderer (#147). Most involve a difference between
reference phrase focus and parser-head representation. This is not automatically
five parsing errors. Contained heads are retained as diagnostic evidence,
without forcing comparison. The old nominal characterization is already retired
under the scope crosswalk, but remains visible in this historical comparison.

Of the 37 aligned positions, 11 have owner-confirmed focus boundaries and 26
remain proposed. Across all 42, the corresponding totals are 12 and 30.
Aligned scope statuses: 28 retain, five exclude, four uncertain. The three
different denominators must not be conflated.

## Exact-alignment field counts
| Field | Same value | Automatic unclear | Reference unclear | Definite value conflict |
| --- | ---: | ---: | ---: | ---: |
| claim_source | 21 | 16 | 0 | 0 |
| event_type | 34 | 1 | 0 | 2 |
| event_actor | 26 | 11 | 0 | 0 |
| polarity | 37 | 0 | 0 | 0 |
| proposition_status | 18 | 18 | 0 | 1 |

Same unclear values, when present, count as same_value; this is not successful
substantive interpretation. All 37 polarity values match in this known selected
material, not evidence of general negation-scope accuracy. These counts are not
held-out performance, inter-annotator agreement or corpus extraction recall.
Owner-confirmed-focus-only counts are also retained separately in the summary.

## Three definite field conflicts
1. #137 know in I don't know what to say: reference event_type=other;
   automatic=knowledge. The converter uses a broad know lemma rule and does
   not resolve the speech-planning reading. This record is outside narrowed
   task scope; retain it as a historical contrast, not a target-task error rate.
2. #375 commit in a crime I did not commit: reference=wrongdoing_unspecified;
   automatic=other. The event mapping does not cover crime/commit content.
3. #383 Warden, murder me: reference status=nonasserted;
   automatic=presented_as_true. The parser tags Warden as nsubj rather than a
   vocative. The converter's root-plus-subject heuristic then treats the command
   as declarative. This combines parser evidence failure and a weak presentation
   heuristic; it is not solved by counting a root as an assertion.

These explanations are AI diagnostic interpretations after seeing outputs,
not new owner adjudications. More generally a field difference cannot itself
establish whether a parser, rule, reference boundary or genuine ambiguity is
responsible. Unclear automatic fields remain unresolved, not silently correct.

## Reproduction and next step
In the optional parser environment:

```bash
.venv/syntax-prototype/bin/python src/compare_confirmed_syntax_v1.py
```

Or run notebooks/18_confirmed_syntax_comparison.ipynb in the original analysis
kernel; it calls the existing optional environment and displays the differences.
Its code-cell bodies were executed in-process during development, not in a
separate Jupyter kernel. No outputs are embedded in the committed notebook.
Local detailed results and local summary are written to data/processed and
refuse changed overwrites. The reports/ summary preserves this environment's run.

Prioritize a versioned phrase/head alignment policy and a presentation-status
safeguard before widening lexical mappings. Keep the current comparison frozen
so any changes can be traced. Repeated tuning on these known selections remains
development and cannot establish independent performance.
