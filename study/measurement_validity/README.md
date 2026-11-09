# Measurement study: apology and innocence claims

**Status: design version 1.1 frozen on 9 November 2026 (`protocol_lock.json`; version 1.0 in `protocol_lock_v1.0.json`). Coding under way; no results yet.**

Can a keyword dictionary, a topic model and an LLM measure apology and innocence claims in Texas last statements as well as blind two-coder human coding? The full design is in [PROTOCOL.md](PROTOCOL.md) and the definitions are in [CODEBOOK.md](CODEBOOK.md).

## Steps

| # | Who | Step | Command or file |
|---|---|---|---|
| 1 | Dora | Check both definitions in `CODEBOOK.md` against Eaton & Theuer (2009, pp. 334–335). Edit them if needed, and fill in "Differences from Eaton & Theuer". | `CODEBOOK.md` |
| 2 | Dora | Freeze the design and commit the lock file (done: version 1.0, amended to 1.1 before coding). | `python study/measurement_validity/freeze.py` |
| 3 | Both coders | Read the codebook, code `coding/practice.xlsx` separately, then discuss the 10 practice items together. | `coding/practice.xlsx` |
| 4 | Each coder alone | Code all 150 items: `apology`, `innocence` and, when innocence is 1, `innocence_type` (F or L). Do not discuss them. Save as `coder_A_completed.xlsx` / `coder_B_completed.xlsx` in `coding/`. | `coding/coder_A.xlsx`, `coding/coder_B.xlsx` |
| 5 | Dora | Compute agreement and create the adjudication sheet. | `python study/measurement_validity/analyze.py agreement` |
| 6 | Both coders | Discuss each listed item and enter the agreed value. Save as `coding/adjudication_completed.xlsx`. | `coding/adjudication.xlsx` |
| 7 | Dora | Run the LLM classifier (needs an Anthropic API key; about 450 requests). | `python study/measurement_validity/llm_classify.py` |
| 8 | Dora | Evaluate all methods. | `python study/measurement_validity/analyze.py evaluate` |

Each coder needs about 2–3 hours for 150 statements (median 71 words each).

**Blinding.** Coders should open only their own sheet, never `sample.csv` or `exposure.csv` (they link item codes to execution records), and must not run or look at any automated method before step 6. 35 items appear in earlier project records; see "Prior project exposure" in the protocol.

## Files

| File | Purpose |
|---|---|
| `PROTOCOL.md`, `CODEBOOK.md` | Design and definitions (frozen) |
| `methods.py` | Dictionary rules, topic-model rule, LLM prompt and schema (frozen) |
| `make_sample.py` | Drew the 150-item sample and wrote the coding sheets |
| `build_exposure.py`, `exposure.csv` | Flags the 35 items that appear in earlier project records |
| `sample.csv` | Item code to execution number |
| `coding/` | Coding sheets, practice items, adjudication |
| `freeze.py` | Creates, amends and checks `protocol_lock.json` |
| `llm_classify.py` | Runs the LLM classifier |
| `analyze.py` | Agreement, adjudication sheet, method evaluation |
| `outputs/` | Results (created by the scripts) |

Tests: `python -m pytest tests/test_measurement_study.py`. They include a full simulated run of the agreement, adjudication and evaluation steps.
