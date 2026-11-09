# Scripts

Run scripts from the repository root, for example `python src/run_nmf_v2.py`. Most need the data-v1 snapshot; the collection scripts need network access to the TDCJ site.

## 1. Corpus construction

| Script | Purpose |
|---|---|
| `build_inventory.py` | Execution inventory from the cached TDCJ index |
| `download_all.py` | Download statement pages with caching and a manifest |
| `extract_all.py` | Extract statement candidates per execution |
| `build_segments.py` | Split labelled sections (spoken, written, media) with source offsets |
| `clean_v1.py` | Conservative cleaning; keeps source text and flags known notices |
| `prepare_model_text.py` | Modelling text, with every editorial change recorded |
| `build_inclusion_ledger.py` | Inclusion evidence per record |
| `collect_sample.py`, `prepare_sample.py`, `check_historical_sample.py` | Early pilot collection and extraction checks |
| `explore_v1.py` | Descriptive summary of the corpus |
| `run_provenance.py` | Records the exact source bytes of executed scripts |

## 2. Development annotation sample

| Script | Purpose |
|---|---|
| `create_annotation_sample.py` | The 50-statement, decade-balanced development sample |
| `summarize_expression_sample.py` | Descriptive counts for its eight labels |
| `check_institutional_feasibility.py` | Record counts around the 2022 spiritual-adviser policy change (descriptive only) |

## 3. Topic model

| Script | Purpose |
|---|---|
| `text_features.py` | Shared TF-IDF features and numerical checks |
| `run_nmf_v2.py` | Current NMF (k = 4, 6, 8); `run_nmf_v1.py` is the earlier version |
| `check_nmf_stability.py` | Initialization stability |
| `check_short_text_sensitivity.py`, `check_prayer_sensitivity.py` | Sensitivity to very short texts and recited prayer |
| `run_followup_audit.py` | Follow-up comparisons from `docs/MODEL_SELECTION_PROTOCOL.md` |

## 4. Archived proposition and syntax experiments

Earlier development work, described in [archive/claim_syntax_experiments/](../archive/claim_syntax_experiments/README.md). The scripts still run and are covered by tests.

`semantic_screening.py`, `claim_adjudication_v3.py`, `audit_claim_consistency.py`, `audit_semantic_scope_v1.py`, `prepare_confirmed_claims.py`, `build_confirmed_snapshot40.py`, `build_evaluation_exposure_v1.py`, `focus_rules_v1.py`, `focus_candidates_v2.py`, `run_sampled_focus_smoke_v1.py`, `audit_smoke_failures_v1.py`, `run_candidate_structure_check_v2.py`, `selected_span_rules.py`, `run_selected_span_diagnostic.py`, `syntactic_candidates_v1.py`, `run_syntactic_candidates_v1.py`, `syntax_semantics_v1.py`, `run_syntax_semantics_v1.py`, `compare_confirmed_syntax_v1.py`

## Current study

The measurement study's code is in [`study/measurement_validity/`](../study/measurement_validity/README.md), not here.
