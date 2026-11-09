# Methods and reproduction

## Data

The data-v1 release contains the execution inventory, the person-level corpus, the prepared modelling corpus and the 50-statement development sample, coded with the eight-category [annotation guide](ANNOTATION_GUIDE.md). The preparation script keeps source texts intact and records every editorial change separately. Execution 82 is an indirect recorder summary; 83 and 238 have no retained TF-IDF features. The current inclusion ledger is `reports/inclusion_ledger_v2.csv`.

## Measurement study

The [measurement study](../study/measurement_validity/README.md) compares a keyword dictionary, two rules on the topic model below and an LLM with blind two-coder coding of apology and innocence claims in a random sample of 150 statements outside the development sample. Related work is summarised in [LITERATURE.md](LITERATURE.md).

## Topic model

`python src/run_nmf_v2.py` fits the four-, six- and eight-topic NMF on the prepared corpus; shared features and topic matching are in `src/text_features.py`, and reference numbers in `results/reference_numeric_v1/`. Stability and sensitivity checks are in `results/nmf_stability_v2/`, `results/short_text_sensitivity_v2/` and `results/prayer_sensitivity_v2/`; follow-up comparisons (initialization pairs, reconstruction, topic–label contrasts) in `results/followup_audit_v1/`. Notebooks 01–04 cover exploration, follow-up tables, inclusion evidence and topic interpretation. Rebuilding extraction and inclusion from scratch needs the raw HTML, which is outside data-v1.

## Earlier work

- **Close reading** of 20 development statements, with a second reader's response to ten: [archive/close_reading/](../archive/close_reading/).
- **Proposition and syntax experiments** (notebooks 05–18): 42 propositions selected in 19 development documents, rule baselines and spaCy parser proposals, which matched 37 of the 42 selections by exact character offsets. Protocols and notes: [archive/claim_syntax_experiments/](../archive/claim_syntax_experiments/README.md); the optional syntax environment is in `requirements-syntax.txt`.

## Reproduction records

Generated outputs carry the hashes of their inputs and code. Software versions for each set of results are in [TESTED_ENVIRONMENTS.md](TESTED_ENVIRONMENTS.md). Scripts write to new folders instead of overwriting earlier outputs, so reruns in a different environment stay separate.
