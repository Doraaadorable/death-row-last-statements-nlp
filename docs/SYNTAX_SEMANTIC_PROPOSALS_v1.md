# Conservative partial semantic conversion v1

## Contract and provenance
This is a development prototype informed by known examples, operating on the
saved 20-document parser output. It is neither reference annotation nor an
independent evaluation. No new sample is drawn. Corpus, owner labels, B2 and
earlier outputs remain unchanged. Source and parser hashes accompany outputs.

syntax_semantics_v1.py proposes the existing five fields with explicit unclear
values. These proposals are not individual owner-confirmed decisions. Scope
remains unassigned for every candidate: a broad parser inventory includes
affection, religion and other out-of-scope predicates.

## Narrow conversion rules
- Kill/murder/execute lemmas suggest killing_action. Take requires a directly
  attached life object, or a life passive subject. It does not use nearby words.
- Know/understand suggest knowledge. Selected responsibility constructions and
  wrong suggest wrongdoing_unspecified. Do/choose/happen remain event-unclear.
  Other predicates provisionally map to other; this is not a full ontology.
- Active actor uses the direct subject head. Passive actor uses an explicit
  by-agent head; a passive subject such as I in I was not paid is not the agent.
  Only a small pronoun set is mapped. Names, we, unresolved and missing heads
  remain unclear; no general coreference or semantic-role labelling is done.
- Direct negation children determine provisional polarity. No general negation
  scope, lexical negation or cross-clause negative interpretation is implemented.
- Root predicates with explicit subjects and no detected quotation receive a
  provisional self-source reading. A limited direct reporting-parent rule can
  identify other-owned content. All other embedded source relations are unclear.
- Subject-bearing root predicates without detected questions, quotation or the
  listed modal auxiliaries provisionally receive presented_as_true. Embedded,
  imperative, modal or otherwise unsupported presentation remains unclear.
  There is no general factivity, conditional, command, discourse or sincerity
  analysis. These root heuristics can be wrong and are not linguistic guarantees.

Target prediction derives from these partial fields. Clear non-killing events
are other; explicit other-actor/source killing is other. Only a self-source,
self-actor, presented-as-true killing can become admission/denial. Other
potential targets abstain. These target outputs are proposals on parser units,
not a substitute for the task-scope and reference preparation protocol.

## Checks and run
Eight known-example behavioral checks passed: direct life-taking, denial,
passive patient versus agent, explicit passive agent, embedded knowledge
holder, unresolved ellipsis, question presentation and reported attribution.
They do not erase the parser's separately documented governing-layer failure.

On 564 parser candidates: 533 other, 28 abstain, two denial and one admission.
The broad candidate inventory is not the old 92-match inventory. Do not compare
these counts as accuracy, improvement, precision, recall or prevalence. All
remaining cases have not been exhaustively reviewed. Run twice with unchanged
inputs reproduced output bytes.

## Run and inspect
After notebook 16's local parser output exists:

```bash
python src/run_syntax_semantics_v1.py
```

Then run notebooks/17_syntax_semantic_proposals.ipynb in the original analysis
kernel. Its first cell generates local proposals using standard-library code;
no extra spaCy installation is needed in that kernel. The notebook displays
complete context and the proposed fields, initially for execution 378.
Local files live in data/processed. A different existing result is never
overwritten; preserve it and version any changes. The reports/ summary is a
record of this development run, not an overwrite target for local reruns.

For behavioral tests use the optional syntax environment:

```bash
.venv/syntax-prototype/bin/python -m unittest discover -s tests -p test_syntax_semantics_v1.py
```

Next inspect a bounded set of proposal examples before expanding rule coverage.
Any later changes remain development on these exposed documents; independent
performance claims still require fresh references and fixed candidate units.
