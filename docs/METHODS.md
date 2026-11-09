# Methods and reproduction

## Data and coding
The data-v1 release supplies the inventory, candidate corpus, prepared model
corpus and frozen 50-person eight-category annotation sample. Annotation
definitions are in [ANNOTATION_GUIDE.md](ANNOTATION_GUIDE.md). The development
records were reviewed through discussion after proposed readings were available.
Use them for framework development and contextual examples.

The corpus preparation script preserves source texts and records editorial
changes separately. Execution 82 is an indirect recorder summary; 83 and 238
have no retained TF-IDF features. The current inclusion ledger is
reports/inclusion_ledger_v2.csv.

## Current study
The [measurement study](../study/measurement_validity/README.md) compares a keyword dictionary, the NMF topic model below and an LLM with blind two-coder human coding of apology and innocence claims in a random sample of 150 statements. The 50 development records are excluded from that sample.

## Archived close reading
An earlier qualitative reading of 20 purposively selected development records, with a second reader's open-ended response to ten of them, is in [archive/close_reading/](../archive/close_reading/). I drafted the memos and selection with AI assistance and revised the interpretations myself. It is kept as a record and is not part of the current study.

The NMF and predicate workflows below are earlier supporting work.

## Exploratory NMF
Run python src/run_nmf_v2.py after preparing the released corpus. Numeric
references are in results/reference_numeric_v1/. Shared features and topic
matching are implemented in src/text_features.py. The current diagnostic
directories are nmf_stability_v2, short_text_sensitivity_v2 and
prayer_sensitivity_v2. Older result directories retain their original metrics.

Initialization pairs, reconstruction summaries and topic/label descriptive
contrasts are in results/followup_audit_v1/. The equal-decade 50-person sample
has a different composition from the corpus. Results describe this sample and
the specified feature/model settings.

Entry notebooks: 01 for exploratory analysis, 02 for follow-up tables, 03 for
inclusion evidence, and 04 for component interpretation. Some extraction and
inclusion rebuilding steps need raw HTML or upstream tables outside data-v1.

## Supporting predicate experiments
The historical predicate discussion records contain 42 selected propositions in 19 documents:
12 focus boundaries are confirmed and 30 are proposed. Raw decision CSVs and
historical numerical outputs remain under reports/ and results/.

| Entry | Purpose |
| --- | --- |
| notebooks 05–07 | Pilot, cue screening and development selection |
| notebook 11 | Materialize the 37-selection discussion record |
| notebook 12 | Selected-span rule diagnostic |
| notebook 15 | Fixed 20-document literal-focus smoke test |
| notebook 16 | Parser predicate proposals |
| notebook 17 | Partial syntax-to-semantics conversion |
| notebook 18 | Exact-focus development comparison |

The 20 smoke-test documents are already used development material. The
comparison in notebook 18 aligns 37 of 42 selections by exact offsets. Its
remaining five use different phrase/head representations. Case provenance,
reference values and proposed values are stored separately.

The protocols and notes for these experiments are archived, unchanged, in
[archive/claim_syntax_experiments/](../archive/claim_syntax_experiments/README.md);
start with [SYNTACTIC_CANDIDATES_v1.md](../archive/claim_syntax_experiments/SYNTACTIC_CANDIDATES_v1.md)
for the optional syntax work. Parser construction, source attribution, negation
and presentation rules have documented gaps. This work is not part of the
current measurement study.

## Reproduction records
Input/code hashes accompany generated outputs. Version details for the original
analysis are in manifests and [TESTED_ENVIRONMENTS.md](TESTED_ENVIRONMENTS.md).
The optional syntax requirements pin spaCy and the English model. Existing
scripts preserve differing outputs rather than overwriting them; environment
metadata and runtime-pipeline fingerprints can also trigger this protection.
Keep reruns separate when investigating an environment change.
