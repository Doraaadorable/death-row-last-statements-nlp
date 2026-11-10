# Measuring Language in Texas Last Statements

How reliably can automated text analysis measure what people say in their final words? This project builds a reproducible corpus of the last statements published by the Texas Department of Criminal Justice, then tests keyword, topic-model and LLM measures of **apology** and **innocence claims** against blind two-coder human coding.

## Current study: measurement validity

Eaton & Theuer (2009) coded these statements by hand, with two-coder kappas of .89–.99. Computational studies of similar texts usually rely on cheaper measures: keyword lists, topic models and, more recently, language models. The two constructs studied here are easy to misread. An apology can look like condolence ("sorry for your loss"), and an innocence claim can look like an accident account or criticism of the system.

- **Sample:** 150 statements drawn at random from the 430 outside the 50-statement development sample that both coders have read. 35 appear in earlier project records and are analysed as a separate group.
- **Reference standard:** two coders work independently with a codebook built on Eaton & Theuer's definitions; kappa is reported before adjudication.
- **Methods compared:** a keyword dictionary, two decision rules on the project's six-topic NMF model, and a zero-shot LLM (`claude-opus-5-5`), all frozen before coding. Results apply to these specific rules.
- **Proposed addition (draft version 1.3):** a BERT classifier trained on Eaton & Theuer's expert codes, against a TF-IDF logistic-regression baseline trained on the same labels, with condolence coded separately so that their broader apology variable can be approximated.
- **Outputs:** precision, recall and F1 with bootstrap intervals, and a categorised account of every error.

The error analysis is the main contribution: it shows which look-alikes each method counts as apology or innocence, and so what a reported count would actually measure. That is the groundwork for later work on psychological expression in last statements.

**Status:** version 1.2 frozen on 9 November 2026 (`protocol_lock.json`). Version 1.3, which adds the BERT classifier, is a draft under review by the supervising professor; Eaton & Theuer's codes have been requested. Human coding starts once version 1.3 is frozen. Details: [study/measurement_validity/](study/measurement_validity/README.md).

## Data

Source: [Texas Department of Criminal Justice, executed inmates](https://www.tdcj.texas.gov/death_row/executed_inmates.html), snapshot through 7 October 2026.

- 603 execution records; 480 person-level statements; 477 with usable text features after preparation.
- Speaker text is separated from recorder annotations, media statements and editorial insertions; see `src/prepare_model_text.py` and the inclusion ledger in `reports/`.
- A 50-statement development sample was coded with an eight-category guide ([docs/ANNOTATION_GUIDE.md](docs/ANNOTATION_GUIDE.md)). It serves for development and coder practice and is excluded from evaluation.

The processed data are in the [data-v1 release](https://github.com/Doraaadorable/death-row-last-statements-nlp/releases/tag/data-v1) (SHA-256 `c56a4be1915cdaefd5ea1878da47d009f0cb9de8082401f7de241d42a7266168`). Extract it into the repository root.

## Topic model

A six-topic NMF on TF-IDF features finds apology/forgiveness, family love, denial ("did not", "kill"), recited prayer, thanks and "stay strong" themes. Four- and eight-topic solutions, initialization stability, and sensitivity to short texts and to recited prayer are under `results/`. The model reproduces exactly from the released data (`python src/run_nmf_v2.py`). Interpretation notes: [docs/COMPONENT_REVIEW_k4_k6_k8.md](docs/COMPONENT_REVIEW_k4_k6_k8.md).

## Reproduce

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then download and extract the data-v1 snapshot as described above.

Run the tests:

```bash
python -m pytest
```

Tests that need the data snapshot are skipped until it is extracted. The syntax prototype tests also need `pip install -r requirements-syntax.txt`. Detailed workflows: [docs/METHODS.md](docs/METHODS.md).

## Ethics

These are public statements, made in an institutional setting and recorded and edited by the state. The project studies what is said: a speaker's account of a case is analysed as their account, and sincerity and guilt are outside its scope. Victims' families are among the people the statements address, and the analysis is written with that in mind.

## Repository

| Path | Contents |
|---|---|
| `study/measurement_validity/` | Current study: protocol, codebook, sample, coding sheets, methods, analysis |
| `src/`, `tests/` | Corpus construction, topic model and archived experiments, with tests ([index](src/README.md)) |
| `results/`, `reports/` | Model outputs and audit records |
| `docs/` | Methods, annotation guide, literature comparison, topic-model notes ([index](docs/README.md)) |
| `notebooks/` | Exploratory notebooks; 01 is the main entry point ([index](notebooks/README.md)) |
| `archive/` | Earlier close reading and proposition/syntax experiments ([index](archive/README.md)) |
