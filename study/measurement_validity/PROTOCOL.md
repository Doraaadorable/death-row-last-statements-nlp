# Protocol: measuring apology and innocence claims in last statements

Version 1.2, frozen with the codebook, sample and method code in `protocol_lock.json` before coding began. Earlier versions are kept as `protocol_lock_v1.0.json` and `protocol_lock_v1.1.json`; changes are listed under Amendments and Deviations.

## Question

Eaton & Theuer (2009) coded Texas last statements by hand, with two-coder kappas of .89–.99. Computational work on similar texts usually relies on cheaper measures: keyword lists, topic models and, more recently, language models. This study asks:

> For apology and innocence claims, how closely do a keyword dictionary, an NMF topic model and a zero-shot LLM agree with blind two-coder human coding?

Each result applies to the specific rules tested: this keyword list, these two topic-model rules, and this prompt with this model. The central output is the pattern of errors, such as condolence read as apology, accident read as denial, or a theme detected only when it dominates a statement. These confusions decide what a count of "apologies" or "innocence claims" actually measures.

This is groundwork for studying psychological expression in last statements. Before counting how often people apologize or protest their innocence at the end of their lives, the counts have to measure those acts and not their look-alikes.

## Constructs

Both constructs are defined in `CODEBOOK.md`, building on the separate variables in Eaton & Theuer (2009, pp. 334–335):

- **Apology**: an apology tied to the speaker's own act or the harm they caused, or a direct apology with no object stated. Condolence that is not tied to the speaker ("sorry for your loss") is coded `0`. This is narrower than Eaton & Theuer's rule, under which any "sorry" counts (32.5% of statements), and it is where a keyword method is most likely to fail.
- **Innocence claim**: the speaker denies the act (**F**, factual) or claims it was lawful, such as self-defense (**L**, legal). Accident and excuse accounts are coded `0`. Eaton & Theuer report 16.4% for claims of innocence. The wording varies ("I didn't do this", "wrong man") and is easily confused with criticism of the system or an accident account.

The codebook lists three deliberate differences from Eaton & Theuer.

## Sample

- Pool: the 480 person-level statements in the data-v1 snapshot, minus the 50 development statements both coders have read. 430 remain.
- Simple random sample of **150** (seed 20261109, `make_sample.py`). Each coder sees the items in a different random order, identified only by an item code.
- Ten practice items come from the development sample. The coders discuss them before the main coding; they are not evaluated.
- Expected positives: about 30–45 for apology and 10–25 for innocence. Innocence recall will have a wide interval, and I report it at this sample size.

**Prior project exposure.** 35 of the 150 statements appear in earlier project records: the exposure ledger (`reports/evaluation_exposure_readiness_v1.json`), the smoke test and the prayer-sensitivity selection. Most of that work was done with AI assistance. For 7 of them (S009, S025, S028, S032, S065, S078, S128), I confirmed decisions on excerpts during the earlier claim review. Outside the development sample, neither coder has read any statement. `exposure.csv` (from `build_exposure.py`) flags every item, and the results are reported for both groups.

## Coding

1. Both coders read `CODEBOOK.md`, code the ten practice items, and discuss them. The codebook stays as frozen; unclear cases go to `u` with a note.
2. Each coder codes all 150 items alone (`coder_A.xlsx`, `coder_B.xlsx`) and saves the sheet as `coder_X_completed.xlsx`.
3. `analyze.py agreement` computes agreement. The coders then meet to adjudicate every disagreement and every `u`, recording the agreed value (`1`, `0`, or `u` if still undecidable) in `adjudication_completed.xlsx`.
4. The adjudicated labels are the reference standard. Items that remain `u` are left out of method evaluation and counted.

Coder A is Dora Zhuang. Coder B is an English teacher from China who has not seen this project's labels or analyses. Both read the English text with the English codebook, looking up single words where needed and using no machine translation.

## Automated methods (frozen in `methods.py`)

| Method | Rule |
|---|---|
| Dictionary | Apology: "sorry", "apologize/apologise", "apology/apologies", unless negated ("not sorry"). Innocence: phrases such as "I am innocent", "not guilty", "I didn't kill/do", "wrong man". |
| Topic model | The six-topic NMF, fitted on all 477 documents without labels. Primary rule: the apology topic (topic 1) or denial topic (topic 3) is the document's largest topic. Secondary rule (`nmf_top2`): the topic is among the document's two largest, with nonzero weight. |
| LLM | `claude-opus-5-5`, effort `low`, zero-shot, with the codebook definitions in the prompt and JSON output (`yes`/`no`/`uncertain`). Primary result: run 1, with `uncertain` scored as `no`; a sensitivity analysis scores it as `yes`. Runs 2 and 3 measure self-consistency. One model only. Refusals, technical failures and invalid output are recorded, left out of the LLM's metrics, and reported in a coverage table. |

No method is tuned on the study sample. The dictionary and topic rules were written before sampling, and the prompt reuses the codebook wording. The automated methods run only after both coders have finished.

## Analysis (`analyze.py`)

**Agreement.** Per construct: percent agreement and Cohen's kappa on `1`/`0`/`u`, with a 95% bootstrap interval (2,000 resamples of items); secondary, kappa on items where neither coder used `u`. Kappa drops with low prevalence, so raw counts are reported next to it.

**Method performance.** Per construct and method, against the adjudicated labels: precision, recall, F1 and accuracy with 95% bootstrap intervals, and the paired F1 difference between each pair of methods. Items are resampled independently, one statement per person.

**Factual innocence.** Innocence is also evaluated with legal-justification claims (**L**) set aside, which is closer to Eaton & Theuer's variable. F/L agreement is reported for items both coders coded `1`.

**Prevalence.** The share of positives in the sample, with a Wilson interval. Eaton & Theuer cover 1982–2007 with a different apology rule, so the comparison is descriptive.

**Exposure groups.** Agreement and each method's metrics are reported separately for the 35 items with documented project exposure and the 115 without, as point estimates.

**Undefined statistics.** A statistic that cannot be computed (for example kappa when both coders use a single value, or recall with no positives) is reported as not estimable. An interval is reported when at least 95% of resamples give a defined value.

**Errors.** Every false positive and false negative goes to `outputs/errors.csv`. I read each one and record its cause, such as condolence, quoted prayer, accident account, system criticism, negation or recorder annotation.

## Reading the results

- A method agrees well with human coding when its F1 interval lies above 0.80.
- Method differences are reported with their intervals; with about 45 and 12 positives, only large differences will be distinguishable.
- All methods are reported for both constructs.

## Amendments (all before coding)

### Version 1.1 (9 November 2026)

An external review of version 1.0 led to five changes:

1. **Exposure.** Version 1.0 described the sample as statements "I have not previously read or labelled"; 35 appear in earlier project records. The sample is unchanged, and exposure is flagged and analysed by group.
2. **Lock enforcement.** `analyze.py` and `llm_classify.py` stop if a frozen file has changed. `llm_classify.py`, `freeze.py` and `exposure.csv` are added to the lock.
3. **Undefined statistics.** All-`0` coding crashed the bootstrap in version 1.0; such cases are now reported as not estimable.
4. **LLM outcomes.** Refusals and failures are recorded separately instead of being scored `no`, and the fallback to a second model is removed.
5. **Topic-model rules.** The primary rule detects a theme only when it dominates a statement. `nmf_top2` adds a looser, label-free rule.

### Version 1.2 (9 November 2026)

Wording only: this protocol is rewritten more concisely, the purpose of the study as groundwork is stated, and the description of `nmf_top2` no longer calls it a test of presence. Every rule and analysis is unchanged, and so are the codebook, sample, coding sheets and prompt.

## Deviations

None so far.
