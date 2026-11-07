# Last Statements: Themes, Interpretation and Robustness

## Current review snapshot: 40 selected propositions

Start with [notebook 14](notebooks/14_confirmed_snapshot40.ipynb) and
[the snapshot guide](docs/CONFIRMED_SNAPSHOT40_v1.md).
All 40 semantic decisions are owner-confirmed after AI-assisted discussion.
Ten predicate-focus positions are explicitly confirmed; thirty remain proposed
mappings. The [candidate backlog](reports/predicate_candidate_backlog_v1.csv)
keeps six unresolved selection candidates separate from accepted records.
This is not independent or exhaustive annotation. Older 37-row diagnostics
and the 39-row audit remain unchanged historical artifacts.


## Historical consistency audit: 39 selected development propositions

[Notebook 13](notebooks/13_claim_consistency_audit.ipynb) checks all 39
conversation-confirmed selections (the original 37 plus the two #287 predicate
layers). [Audit notes](docs/CLAIM_CONSISTENCY_AUDIT_v1.md) distinguish
32 rows without a proposed semantic-label change from seven rows needing
focus-boundary clarification. Proposed focus offsets are manual development
annotations, not an automatic parser or independent semantic validation.
No confirmed labels were changed. The earlier 37-row rule diagnostic remains
unchanged; neither a larger selection nor a supplied focus is unseen performance.


## Original 37-selection materialization

Start with [notebook 11](notebooks/11_confirmed_semantic_review.ipynb) and
[the current review guide](docs/SEMANTIC_CONFIRMED_REVIEW_v3.md).
The owner-confirmed discussion record now contains 37 selected propositions
across 19 of the 21 fixed development documents. Two other documents retain
scope notes. These are AI-assisted development decisions, not exhaustive or
independent reference annotations.
The current field is `proposition_status`:
`presented_as_true / nonasserted / unclear`; background attribution stays in notes.
Notebooks 08-10 and the 33-row v2 booklet are historical drafts.
Notebook 11 preserves earlier local worksheets and validates exact evidence
before materializing separate current files. No new model is fitted.


An exploratory NLP project analyzing published last statements from
Texas execution records.

## Research question

What recurring expressions appear in these statements, and how sensitive
are the resulting topic structures to initialization, short texts and
selected formulaic prayers?

## Analysis

Start with
[the analysis notebook](notebooks/01_last_statements_analysis.ipynb).

The supplied snapshot contains:

- 603 execution records.
- 480 person-level candidate documents.
- 479 documents prepared for exploration.
- 477 documents with retained TF-IDF features.
- 50 manually reviewed records used for coding-guideline development.

The six-topic NMF solution is the main exploratory summary, with an
eight-topic supplement. Topics concern apology and forgiveness,
affection, case-related denial and explanation, formulaic prayer,
thanks and support, and encouragement.

## Main findings

- The six-component exploratory reading identifies recurring expressions of
  apology and forgiveness, affection, case-related denial and explanation,
  repeated prayer, thanks and support, and encouragement. These are overlapping
  linguistic patterns, not validated categories assigned to every person.
- Initialization results do not identify a unique best topic count. At k=6,
  the lower quartile of matched cosines across random-seed pairs is 0.938,
  but the weakest match is 0.054. Typical agreement can conceal a fragile component.
- In the 50-record development sample, Topic 1's median coefficient is 0.181
  for apology/forgiveness-positive records (n=22), versus 0 for negative records
  (n=26). Topic 3's corresponding medians for the innocence-dispute label are
  0.145 (n=8) and 0.033 (n=40). These are descriptive contrasts, not independent
  validation; [all prespecified contrasts](results/followup_audit_v1/topic_label_descriptive.csv),
  including uncertainty groups, are reported. Topic 4 is a weaker construct
  match for broad faith/spirituality: F=1 has median 0.013 and Q3 0.027 (n=27),
  versus median 0 for F=0 (n=20). Its narrow repeated-prayer pattern should not
  be treated as a general faith detector. Uncertain groups contain only 1-6
  records where present; their quartiles are descriptive, not stable estimates.
- Lexical stability does not guarantee semantic validity: similar words can
  express denial, uncertainty or quoted denial followed by admission. Repeated
  prayer wording also forms a component of expression style, whose substantive
  meaning requires separate judgment.
- The historical normalization comparison can be rerun with
  `src/run_nmf_v1.py` and `src/run_nmf_v2.py`; a v1/v2 comparison artifact is
  not supplied, so removal of a tokenization-driven component is not presented
  here as a self-contained published finding. Prayer removal remains a
  targeted influence check, not independent confirmation.

Topic coefficients are not probabilities. The project does not infer
actual guilt, sincerity, remorse or psychological state.

For a short project explanation, see the [project brief](docs/PROJECT_BRIEF.md).

## Results at a glance

### Six-topic exploratory summary

![Six-topic NMF results](reports/figures/notebook_topics_k6.png)

### Robustness checks

![Topic robustness](reports/figures/notebook_robustness.png)

This historical figure shows reference-based comparisons. New random-pair
comparisons are in the follow-up notebook and should be read separately.

## Methods

TF-IDF uses unigrams and bigrams. NMF models with 4, 6 and 8 components
were compared. Robustness checks examine five random initializations,
omission of modeled texts shorter than ten words, and omission of ten
records containing selected prayer phrases.

The removal experiments keep vocabulary and IDF fixed and remove entire
records. They do not isolate the effects of prayer passages alone. The ten
prayer records were selected using the observed component's content: this is
a targeted influence check, not independent confirmation. The prayer component
reflects repeated expression form; its substantive interpretation remains open.

The 50 reviewed records were used for guideline development and non-blind
adjudication, not independent evaluation. Manual labels were not used
to fit NMF.

## Annotation guide

The [frozen v2 annotation guide](docs/ANNOTATION_GUIDE.md) documents all eight
manual coding categories, values and interpretation boundaries. These
categories are separate from the NMF topics and describe expressed language,
not a speaker's internal psychological state.

## Reproduction

### 1. Set up a fresh working copy

Use a new folder so the snapshot does not overwrite existing local data.

```bash
git clone https://github.com/Doraaadorable/death-row-last-statements-nlp.git
cd death-row-last-statements-nlp
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Obtain the curated inputs

Download [data_snapshot_v1.zip](https://github.com/Doraaadorable/death-row-last-statements-nlp/releases/download/data-v1/data_snapshot_v1.zip)
from [Data snapshot v1](https://github.com/Doraaadorable/death-row-last-statements-nlp/releases/tag/data-v1)
and place it in the project root. Select the named data attachment, not
GitHub's automatically generated source-code ZIP.

Expected ZIP SHA-256:

```text
c56a4be1915cdaefd5ea1878da47d009f0cb9de8082401f7de241d42a7266168
```

On macOS, verify the downloaded bytes before extraction:

```bash
shasum -a 256 data_snapshot_v1.zip
```

After confirming the hash matches, extract into the fresh project folder:

```bash
unzip -n data_snapshot_v1.zip
```

The archive contains four curated CSV inputs under `data/processed/`,
the model-text change log, preparation metadata, a snapshot manifest
with per-file hashes, and source/use notes. Curated data remain ignored
by Git and are distributed through the Release attachment.

### 3. Read or rerun the analysis notebook

```bash
python -m notebook
```

Open `notebooks/01_last_statements_analysis.ipynb` and select
**Restart Kernel and Run All Cells**. The notebook reads the published
model outputs and verifies the model-corpus hash; it does not refit NMF.

### 4. Optional: refit the models and robustness experiments

Run these in order in a separate working copy if you want to preserve
the published result files for comparison:

```bash
python src/prepare_model_text.py
python src/run_nmf_v2.py
python src/check_nmf_stability.py
python src/check_short_text_sensitivity.py
python src/check_prayer_sensitivity.py
```

The original environment versions and parameters are recorded in
`results/nmf_v2/run_manifest.json`. The dependency list is not a lockfile.
Numerical results can vary across versions. Repaired checks use numerical
reference weights and regenerated full matrices rather than keyword ordering.
They save diagnostics in new v2 directories, preserving historical outputs.
See [the follow-up report](docs/FOLLOWUP_AUDIT.md) for tolerances and provenance.

This snapshot supports downstream reproduction from curated inputs.
Raw HTML, upstream extraction tables and every manual review decision
are not included, so it is not a complete reconstruction of source
collection and extraction. The index dates describe the supplied
snapshot, not the archive's packaging date.

## Source and assistance

Source: [Texas Department of Criminal Justice, Executed Inmates](
https://www.tdcj.texas.gov/death_row/executed_inmates.html).

The supplied index snapshot spans December 7, 1982 to October 7, 2026.
Statement-level source links are retained in the corpus.

AI assisted with code, documentation and interpretation discussions.
The project owner reviewed and approved the v2 coding decisions.
This does not constitute independent expert validation.

## Follow-up audit

Read [the follow-up notebook](notebooks/02_followup_audit.ipynb),
[the dated protocol](docs/MODEL_SELECTION_PROTOCOL.md) and
[the execution report](docs/FOLLOWUP_AUDIT.md).

The follow-up retains all 3,196 features, saves complete regenerated numerical
references, and separates random-seed pairwise comparisons from comparisons
with the NNDSVDa reference. No unique winning k is established. Reference
reconstruction captures approximately 7.3%, 8.7% and 10.0% of squared TF-IDF
Frobenius norm at k=4/6/8; this is neither semantic coverage nor regression R².

Frozen-label contrasts report n and quartiles for 0/1/u separately and are
strictly descriptive. The [current inclusion ledger](reports/inclusion_ledger_v2.csv)
records 480 included and 123 excluded records: 102 shared-notice links,
13 reports of no statement, four ambiguous short responses, and four summaries
or references. The [21-record evidence extract](reports/inclusion_evidence_21_v1.csv)
documents previously missing historical exclusion reasons. This establishes
current-version inclusion history, not that every exclusion is substantively
settled: speaker attribution remains unresolved for executions 463, 533, 539
and 567; execution 241 contains an explicit supplied translation and is flagged
for reconsideration in a future corpus version. Frozen data and models are unchanged.
Zero-feature execution IDs are 83 and 238.

To regenerate only the new follow-up tables after obtaining the data snapshot:

```bash
python src/run_followup_audit.py
python src/build_inclusion_ledger.py
```

`build_inclusion_ledger.py` regenerates the historical v1 ledger from the Release
snapshot; it does not regenerate the evidence-enriched v2 ledger. The latter
was built in [the inclusion-review notebook](notebooks/03_inclusion_review.ipynb)
using the owner's upstream cleaning table. That full table is not in the
Release; its SHA-256 is recorded in the committed evidence extract.

The supplementary notebook reads these tables. Its owner-executed outputs were
committed in `5bfe829`: three code cells numbered 1 through 3, four saved display
outputs and no stored error outputs. This verifies result loading and display,
not a new model fit or independent execution. Historical result directories
and frozen labels remain unchanged.

## Release audit status

The uniform component-by-component interpretive review planned for k=4/6/8
has not been completed. Current k comparisons are numerical diagnostics,
not a completed joint numerical-and-interpretive model-selection exercise.
See [tested environments and provenance](docs/TESTED_ENVIRONMENTS.md) for
executed checks, reviewer-reported evidence and the unresolved historical
code-hash gap. Dependencies remain unpinned; tested environments are not a lockfile.

## Semantic interpretation extension: development only

The initial [cross-k component review](docs/COMPONENT_REVIEW_k4_k6_k8.md)
now covers leading examples for all 18 components; broader boundary checks
remain limited. [Initial literature positioning](docs/LITERATURE_POSITIONING.md)
identifies substantial related work and does not establish novelty.

The next [four-span pilot](notebooks/05_claim_interpretation_pilot.ipynb)
uses previously inspected development material under a
[separate working protocol](docs/SEMANTIC_PILOT_PROTOCOL.md). It separates
claim source, event actor, event type and polarity. Labels start blank;
no new classifier, performance result or independent evaluation is claimed.
The notebook code-cell bodies and safe repeat-export behavior were checked
in-process; a separate Jupyter-kernel execution remains for the owner.

The four pilot decisions have since been confirmed by the owner after discussion;
[their recorded process](reports/semantic_pilot_decisions_v1.csv) remains non-blind
and development-only. [Notebook 06](notebooks/06_semantic_candidate_screen.ipynb)
creates a separate reviewed worksheet and screens all 479 prepared documents
under a [cue-screening protocol](docs/SEMANTIC_SCREENING_PROTOCOL.md).
The [feasibility counts](reports/semantic_screen_feasibility_v1.json) report
128 candidate documents and 351 nonmatches. These are regex hits, not confirmed
semantic classes, task accuracy or independent evaluation material.
