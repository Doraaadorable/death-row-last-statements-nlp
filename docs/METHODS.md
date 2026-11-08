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

## Current contextual reading
The main narrative is [RESEARCH_DRAFT.md](RESEARCH_DRAFT.md), with detailed
memos in [OPEN_READING_WORKBOOK_v1.md](OPEN_READING_WORKBOOK_v1.md).
Reader A is the project owner. Twenty candidate documents were purposively
selected from the 50-person development sample; co-occurrence informed selection.
Memo drafting and selection were AI-assisted, with Reader A discussing and
revising interpretations. Source boundaries are listed in the draft, including
#1's media/spoken merge and #49's extracted exchange. No original recording
completeness, psychological scale or population prevalence is inferred.

Reader B subsequently read ten already selected texts: the four sparse cases
#15, #11, #32, #49 and six contrasts #508, #413, #595, #407, #1, #600. Reader A
confirmed no prior exposure to project interpretations, translation assistance
and permission for anonymous paraphrase, quotation and complete publication.
The intentionally open-ended instruction prioritized genuine feelings, without
mandatory completion of the packet questions. Original feedback and context are
in reports/reader_response_v1.txt and reports/reader_response_context_v1.json.
Permission is recorded through Reader A's written confirmation, not a separate
signed reader form. No reliability coefficient or generalized audience effect
is reported. The response does not change the frozen corpus or labels.

The NMF and predicate workflows below are earlier supporting work. Institutional
Ramirez/Murphy material is an appendix, separate from the 20-document comparison.

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

For optional syntax work follow [SYNTACTIC_CANDIDATES_v1.md](SYNTACTIC_CANDIDATES_v1.md).
Parser construction, source attribution, negation and presentation rules have
documented gaps. These supporting outputs are distinct from psychological
coding. The current research does not require further classifier development.

## Reproduction records
Input/code hashes accompany generated outputs. Version details for the original
analysis are in manifests and [TESTED_ENVIRONMENTS.md](TESTED_ENVIRONMENTS.md).
The optional syntax requirements pin spaCy and the English model. Existing
scripts preserve differing outputs rather than overwriting them; environment
metadata and runtime-pipeline fingerprints can also trigger this protection.
Keep reruns separate when investigating an environment change.
