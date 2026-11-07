# Last Statements: Psychological Expression and Meaning

An exploratory study of emotional expression, relational concerns and meaning
making in published last statements from Texas execution records.

## Research question
How do people facing execution express emotions, maintain relationships, and
make sense of death and their own situation in their final statements?

## Start here
- [Exploratory report](docs/PSYCHOLOGICAL_EXPRESSION_REPORT.md): case comparisons, literature and conclusions.
- [Literature comparison](docs/LITERATURE_COMPARISON.md): prior coverage, access status and the next research decision.
- [Current research plan](docs/CURRENT_RESEARCH_PLAN.md): question, literature and next steps.
- [Open reading workbook](docs/OPEN_READING_WORKBOOK_v1.md): 20 complete statements with evidence-linked reading memos.
- [Eight-category annotation guide](docs/ANNOTATION_GUIDE.md): definitions for the existing development sample.
- [Methods and reproduction](docs/METHODS.md): data preparation, exploratory models and supporting experiments.

## Data
The saved inventory contains 603 execution records. The candidate corpus has
480 person-level documents; 479 are prepared for exploration and 477 have
nonzero TF-IDF features. The coding-development sample contains 50 people,
ten per decade.

The eight nonexclusive categories cover affection, gratitude, faith/spirituality,
apology/forgiveness, acknowledgment of harm, culpability disputes, justice
criticism, and farewell/closure/readiness. Values are 1, 0 and u (unresolved).
These describe textual expression; they are not a psychological scale.

## Current work
The 20-case workbook now contains contextual reading memos and alternative
interpretations. All 20 cases have been discussed with the project owner; the memos now
record refinements, reading responses and unresolved interpretations. The accompanying report examines
responsibility and judgment, family connection, spiritual meaning and readiness.

The case comparisons show why readiness should be separated from endorsement
of punishment, and why harm acknowledgment, intent and involvement need
separate interpretation. These are exploratory observations from purposively
selected texts, not corpus prevalence estimates. Close precedents include
Schuck & Ward (2008) and Zhuo & Chun (2026); a new literature gap is not established.

## Completed exploratory analysis
The six-component NMF reading identifies apology/forgiveness, affection,
case-related explanation, repeated prayer, thanks/support, and encouragement.
Four- and eight-component solutions, initialization comparisons and text-removal
checks are retained under results/. The repeated-prayer removal is a targeted
influence check. Component interpretations are in the
[review notes](docs/COMPONENT_REVIEW_k4_k6_k8.md).

The later predicate and syntax experiments provide supporting tools for source,
negation and actor distinctions. Their code, tests and result tables remain
available; current research focuses on contextual psychological expression.

## Reproduction
Install the core dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Download data_snapshot_v1.zip from the [data-v1 release](https://github.com/Doraaadorable/death-row-last-statements-nlp/releases/tag/data-v1),
verify SHA-256 `c56a4be1915cdaefd5ea1878da47d009f0cb9de8082401f7de241d42a7266168`,
and extract it into the project root. Then open
[notebook 01](notebooks/01_last_statements_analysis.ipynb).
Additional workflows and the optional syntax environment are documented in
[METHODS.md](docs/METHODS.md).

## Interpretation and scope
The material records public statements in an institutional setting. Conclusions
concern expressed language and contextual interpretations, rather than private
mental states, sincerity or actual guilt. The equal-decade development sample
supports framework development; corpus-frequency estimates require a separate
sampling and coding design. References and access status are recorded in the
current research plan.

## Source
[Texas Department of Criminal Justice](https://www.tdcj.texas.gov/death_row/executed_inmates.html).
Individual source links are retained in the corpus. The snapshot covers records
through October 7, 2026. Raw data and local generated artifacts are excluded
from Git; source statements and original coding values are preserved.
