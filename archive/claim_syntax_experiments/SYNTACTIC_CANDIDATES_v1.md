# Syntactic predicate candidates v1

## Purpose and method
This optional prototype uses spaCy 3.8.18 with en_core_web_sm 3.8.0, NER
disabled. It proposes all VERB/AUX heads except dependency-labelled auxiliaries
and copulas attached to another head. It records direct auxiliaries, negation,
syntactic subject/object/complement heads, passive agent heads and the nearest
governing predicate. Copular be and unattached auxiliaries are retained rather
than silently discarded. Source character offsets are preserved.

There is no task-scope filtering or automatic five-field coding. Syntactic
subjects are not automatically semantic actors; parser ancestors do not prove
attribution or truth presentation. Ellipsis may be tagged VERB rather than AUX,
so the kind field is not a reliable ellipsis detector. Shared subjects in
coordination and relative-clause referents are not resolved.

Official references:
- https://spacy.io/usage/linguistic-features
- https://spacy.io/models/en

The English pipeline is trained for general written web text, not this corpus.
Transcription errors, religious/figurative wording and long sentences can lead
to incorrect parses. No personal statements are submitted to an external
inference service; the downloaded pipeline runs locally.

## Development checks and observed limitation
Five behavioral checks passed; one desired-structure check is retained as an
expected failure. The observed parser succeeds on these fixtures:
- Did Roger come up here yet: come is the head, Did its auxiliary, Roger subject.
- They take a life and take the power: the two object heads are life and power.
- My family's murders: no verbal candidate proposed.
- The three lexical foci in I know you think I did this and their offsets remain.

However, for the last example the parser returns think as root and attaches
know to think, rather than the desired know > think > did structure. The test
keeps the desired answer and explicitly records expectedFailure; it does not
change the expected linguistic structure to make the parser look correct.
This is an example-level limitation, not an estimated failure rate.

## Existing sample run
On the same exposed 20 documents, the prototype proposes 564 candidates:
453 lexical verbs, 110 be/copular predicates and one unattached AUX candidate.
This is a much broader inventory than the 92 literal matches. The difference
does not measure improved recall: many candidates concern affection, religion,
thanks and other out-of-scope content. No new admission/denial predictions or
independent reference labels have been produced.

The run was repeated with identical local outputs. All focus offsets matched
the frozen text. Two notebook code-cell bodies were executed in-process, not
in an independent Jupyter kernel. The committed notebook has no saved outputs.
The committed report is the development environment's summary/provenance;
reruns produce their own local summary without replacing that record.

## Run in an isolated optional environment
From the project root, create a nested environment inside the already ignored
.venv directory. This does not install parser dependencies into the original
analysis environment:

```bash
python3 -m venv .venv/syntax-prototype
.venv/syntax-prototype/bin/python -m pip install -r requirements-syntax.txt
.venv/syntax-prototype/bin/python -m unittest discover -s tests -p test_syntactic_candidates_v1.py
.venv/syntax-prototype/bin/python src/run_syntactic_candidates_v1.py
```

Expected development-test output: six tests, including one expected failure.
Model parsing can vary with dependency/platform changes; inspect unexpected
passes or failures rather than silently altering fixtures. Installed spaCy and
model versions, pipeline fingerprint, code/input hashes and Python version are
recorded for each run.

Open notebooks/16_syntactic_candidates.ipynb using the existing analysis kernel.
It reads local JSON and needs no spaCy installation in that kernel. Start with
execution 378. The syntax runner creates:
- data/processed/syntactic_candidates_v1.json
- data/processed/syntactic_candidates_summary_v1.json

It refuses to overwrite different existing outputs. Preserve earlier outputs
and version changes if a different environment or implementation is tested.
These local files are not reference annotations or training data.

## Next decision
Inspect candidate boundaries and scope before using parser proposals in a
classifier. Keep B2 and historical predictions frozen. This prototype supplies
useful syntactic evidence, but its known layer-attachment failure prevents
treating it as a dependable source-attribution engine. Further development on
this batch must remain labelled development; a fresh reference process is
still required for performance claims.
