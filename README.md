# Measuring Language in Texas Last Statements

Can automated text analysis measure what people say in their final statements as reliably as careful human coding? This project builds a reproducible corpus of the last statements published by the Texas Department of Criminal Justice, then tests keyword, topic-model and LLM measures of **apology** and **innocence claims** against blind two-coder human coding.

## Current study: measurement validity

Published studies of these statements code them by hand: Eaton & Theuer (2009) report two-coder kappas of .89–.99. Computational work often uses cheaper measures such as keyword lists or topic models. Whether those measures work on short, formulaic, institutionally recorded text has not been tested. This study tests it:

- **Sample:** 150 statements drawn at random from 430 that I have not previously read or labelled.
- **Reference standard:** two coders work independently with a codebook based on Eaton & Theuer's definitions, with three documented differences; kappa is reported before adjudication.
- **Methods compared:** a keyword dictionary, the project's six-topic NMF model and a zero-shot LLM (`claude-opus-5-5`), all frozen before coding starts.
- **Outputs:** precision, recall and F1 with bootstrap intervals, plus a categorised error analysis.

**Status:** the design, codebook, sample, method code and analysis code were frozen on 9 November 2026 (`protocol_lock.json`). Human coding is under way; there are no results yet. Details: [study/measurement_validity/](study/measurement_validity/README.md).

## Data

Source: [Texas Department of Criminal Justice, executed inmates](https://www.tdcj.texas.gov/death_row/executed_inmates.html), snapshot through 7 October 2026.

- 603 execution records; 480 person-level statements; 477 with usable text features after preparation.
- Speaker text is separated from recorder annotations, media statements and editorial insertions; see `src/prepare_model_text.py` and the inclusion ledger in `reports/`.
- A 50-statement development sample was coded with an eight-category guide ([docs/ANNOTATION_GUIDE.md](docs/ANNOTATION_GUIDE.md)). It is used only for development and practice, never for evaluation.

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

Without the data snapshot, tests that need it are skipped. The syntax prototype tests also need `pip install -r requirements-syntax.txt`. Detailed workflows: [docs/METHODS.md](docs/METHODS.md).

## Scope and ethics

These are public statements made in an institutional setting, recorded and edited by the state. The project measures what is said. It does not judge sincerity, guilt or mental state. Victims' families are among the people addressed, and the analysis does not present a speaker's claims about a case as established fact.

## Repository

| Path | Contents |
|---|---|
| `study/measurement_validity/` | Current study: protocol, codebook, sample, coding sheets, methods, analysis |
| `src/`, `tests/` | Corpus construction, topic model and archived experiments, with tests ([index](src/README.md)) |
| `results/`, `reports/` | Model outputs and audit records |
| `docs/` | Methods, annotation guide, literature comparison, topic-model notes ([index](docs/README.md)) |
| `notebooks/` | Exploratory notebooks; 01 is the main entry point ([index](notebooks/README.md)) |
| `archive/` | Earlier close reading and proposition/syntax experiments, kept as records ([index](archive/README.md)) |
