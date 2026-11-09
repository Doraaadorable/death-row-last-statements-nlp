# Notebooks

Start with **01**. Run notebooks from this folder after extracting the data-v1 snapshot into the repository root.

## Corpus and topic model

| Notebook | Contents |
|---|---|
| `01_last_statements_analysis.ipynb` | Corpus overview, NMF themes and robustness checks (main entry point) |
| `02_followup_audit.ipynb` | Follow-up audit tables and descriptive contrasts |
| `03_inclusion_review.ipynb` | Evidence for which records are included |
| `04_component_interpretation.ipynb` | Reading the k = 4, 6 and 8 topic solutions |

## Archived proposition and syntax experiments

Development work on documents I had already read, described in [archive/claim_syntax_experiments/](../archive/claim_syntax_experiments/README.md).

| Notebook | Contents |
|---|---|
| `05_claim_interpretation_pilot.ipynb` | Four-span pilot of "who said what" coding |
| `06_semantic_candidate_screen.ipynb` | Keyword screen for candidate claims |
| `07_semantic_development_review.ipynb` | Fixed development sample for claim coding |
| `11_confirmed_semantic_review.ipynb` | The 37 reviewed propositions |
| `12_selected_span_rule_diagnostic.ipynb` | Rule diagnostic on selected spans |
| `15_sampled_focus_smoke.ipynb` | 20-document smoke test of the focus rules |
| `16_syntactic_candidates.ipynb` | spaCy predicate proposals |
| `17_syntax_semantic_proposals.ipynb` | Partial conversion of parser output to coding fields |
| `18_confirmed_syntax_comparison.ipynb` | Parser proposals compared with reviewed selections |

Notebooks 08–10, 13 and 14 were removed in commit `d2efaa1` (redundant review notebooks); the numbering is kept so that existing references stay valid.
