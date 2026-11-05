# Last Statements: Themes, Interpretation and Robustness

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

- Contraction normalization removed a tokenization-driven topic.
- Topic sensitivity differs across initialization and record-removal
  experiments.
- Lexical stability does not guarantee semantic validity: similar words
  can express denial, uncertainty or quoted denial followed by admission.

Topic coefficients are not probabilities. The project does not infer
actual guilt, sincerity, remorse or psychological state.

## Methods

TF-IDF uses unigrams and bigrams. NMF models with 4, 6 and 8 components
were compared. Robustness checks examine five random initializations,
omission of modeled texts shorter than ten words, and omission of ten
records containing selected prayer phrases.

The removal experiments keep vocabulary and IDF fixed and remove entire
records. They do not isolate the effects of prayer passages alone.

The 50 reviewed records were used for guideline development and non-blind
adjudication, not independent evaluation. Manual labels were not used
to fit NMF.

## Reproduction

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

The notebook reads saved model outputs. Model fitting and robustness
procedures are in `src/`.

Curated data under `data/processed/` are currently excluded from Git.
A clone therefore requires the original data snapshots before the
notebook can be rerun. A public snapshot distribution route is not yet
provided.

## Source and assistance

Source: [Texas Department of Criminal Justice, Executed Inmates](
https://www.tdcj.texas.gov/death_row/executed_inmates.html).

The supplied index snapshot spans December 7, 1982 to October 7, 2026.
Statement-level source links are retained in the corpus.

AI assisted with code, documentation and interpretation discussions.
The project owner reviewed and approved the v2 coding decisions.
This does not constitute independent expert validation.
