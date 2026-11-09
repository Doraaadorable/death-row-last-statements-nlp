# Archived: proposition and syntax experiments (5–7 November 2026)

Before the current [measurement study](../../study/measurement_validity/README.md), I tried a finer-grained approach: break statements into propositions centred on a predicate ("I killed", "I did not kill"), code who says what about whom (admission, denial, negation, attribution), and test whether transparent rules or a dependency parser could recover those fields.

**Why it stopped.** Every evaluation in this line used development documents I had already read and discussed, so none of it is independent evidence. The rules were informed by known examples, and the parser output only partly matched the reviewed selections (37 of 42 aligned by exact character offsets). The measurement study replaces it with a simpler, pre-registered question on a fresh random sample.

**These files are kept unchanged.** Several of them are hashed in earlier reports as evidence of what each run used (for example `reports/sampled_focus_smoke_v1.json`), so editing them would break that record. They were written during an AI-assisted workflow, and "the owner" in them means me.

| File | What it records |
|---|---|
| `PREDICATE_CENTERED_REVIEW_RULE.md` | The rule for choosing the central predicate of each proposition |
| `SEMANTIC_CLAIM_GUIDELINE_v3_DRAFT.md` | The proposition coding scheme (status, actor, negation fields), draft v3 |
| `FOCUS_BASELINE_v1.md` | A rule baseline that labels a human-selected predicate |
| `SAMPLED_FOCUS_SMOKE_PROTOCOL_v1.md` | A 20-document smoke test of that baseline |
| `SELECTED_SPAN_RULE_DIAGNOSTIC_PROTOCOL_v1.md` | Whether two rules separate killing admissions from denials on selected spans |
| `SYNTACTIC_CANDIDATES_v1.md` | spaCy predicate candidates (optional; `requirements-syntax.txt`) |
| `SYNTAX_SEMANTIC_PROPOSALS_v1.md` | Partial conversion of parser output into the coding fields |
| `CONFIRMED_SYNTAX_COMPARISON_v1.md` | Parser proposals compared with the 42 reviewed selections |

The code is still in `src/` and `tests/`, and the notebooks are 05–18 in `notebooks/`; see [src/README.md](../../src/README.md) and [notebooks/README.md](../../notebooks/README.md). Generated tables are in `reports/` and `results/`.
