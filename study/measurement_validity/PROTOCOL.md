# Protocol: can automated methods measure apology and innocence claims in last statements?

Version 1.1. This protocol is frozen, together with the codebook, sample and method code, in `protocol_lock.json` before any human coding starts. Version 1.0 is kept in `protocol_lock_v1.0.json`. Changes made before coding are listed under "Amendments"; changes after coding starts are listed under "Deviations".

## Question

Published research codes Texas last statements by hand. Eaton & Theuer (2009) report two-coder kappas of .89–.99 and an apology rate of 32.5% for 1982–2007. Computational studies of the same kind of text often rely on keyword lists or topic models instead. I ask whether those cheaper measures agree with careful human coding on these short, formulaic, institutionally recorded texts:

> For apology and innocence claims, how closely do a keyword dictionary, an unsupervised topic model and a zero-shot large language model agree with blind two-coder human coding?

The study does not estimate how common apology or innocence claims are in the full corpus. It also does not make claims about speakers' sincerity or mental states.

**Scope.** Each result describes one specific operationalization: this keyword list, these topic-model decision rules and this prompt with this model. A poor result for the dictionary shows the limits of this simple "sorry" rule against a narrower construct, not that every dictionary method fails. The most useful output is expected to be the pattern of errors (condolence versus apology, accident versus denial, a theme being present versus dominating a statement), since these confusions change what a reported statistic means.

## Constructs

Two constructs, defined in `CODEBOOK.md` and built on the separate variables in Eaton & Theuer (2009, pp. 334–335):

- **Apology**: an apology tied to the speaker's own act or harm, or a direct apology with no object stated. Condolence that is not tied to the speaker ("sorry for your loss") does not count. This is narrower than Eaton & Theuer's "said they were sorry" (32.5% of statements), so the word "sorry" alone is not sufficient, which is a direct test of keyword methods.
- **Innocence claim**: a claim that the speaker should not stand convicted, either by denying the act (**F**, factual) or by claiming it was lawful, such as self-defense (**L**, legal). Accident and excuse accounts do not count. Eaton & Theuer report 16.4% for claims of innocence. The wording varies ("I didn't do this", "wrong man"), and claims are easy to confuse with criticism of the system or accident accounts.

The deliberate differences from Eaton & Theuer are listed at the end of `CODEBOOK.md`.

## Sample

- Pool: the 480 person-level statements in the data-v1 snapshot, minus the 50 statements in the earlier development sample, which both coders have read. 430 remain.
- Simple random sample of **150** (seed 20261109, `make_sample.py`). Each coder sees the same items in a different random order, identified only by an item code.
- 10 practice items come from the development sample. The coders discuss them together before the main coding, and they are not evaluated.

**Prior project exposure (v1.1).** Before this study, 35 of the 150 sampled statements appeared in earlier project records: the exposure ledger (`reports/evaluation_exposure_readiness_v1.json`), the earlier smoke test and the prayer-sensitivity selection. That work was largely AI-assisted. For 7 of them (S009, S025, S028, S032, S065, S078, S128), Coder A confirmed decisions on excerpts during the earlier claim review. Neither coder has otherwise read statements outside the development sample, and Coder B has read none. The 115 other statements have no documented exposure, which is not proof that they were never seen. `exposure.csv` (`build_exposure.py`) flags every item. The sample is kept unchanged and exposure is handled as a sensitivity analysis (below).

Expected positives: roughly 30–45 for apology and 10–25 for innocence. Recall for innocence will therefore have a wide interval; I report it as such rather than enlarging the sample after seeing results.

## Coding

1. Both coders read `CODEBOOK.md` and code the 10 practice items. They discuss the practice items, but **the codebook is not changed** after freezing. Unclear cases are resolved by the existing `u` rule and the note column.
2. Each coder codes all 150 items independently (`coder_A.xlsx`, `coder_B.xlsx`), without discussing them, and saves the sheet as `coder_X_completed.xlsx`.
3. `analyze.py agreement` computes agreement. Only then do the coders meet to adjudicate every disagreement and every `u`, recording the agreed value (`1`, `0`, or `u` if still undecidable) in `adjudication_completed.xlsx`.
4. The adjudicated labels are the reference standard. Items that remain `u` are excluded from method evaluation and counted.

Coder A is Dora Zhuang. Coder B is an English teacher from China who has not seen this project's labels or earlier analyses. Both coders read the English text with the English codebook. They may look up single words, but do not use machine translation.

## Automated methods (frozen in `methods.py`)

| Method | Rule |
|---|---|
| Dictionary | Apology: "sorry", "apologize/apologise", "apology/apologies", unless negated ("not sorry"). Innocence: phrases such as "I am innocent", "not guilty", "I didn't kill/do", "wrong man". |
| Topic model | The existing six-topic NMF (fitted on all 477 documents without labels). Primary rule: positive if the apology topic (topic 1) or the denial topic (topic 3) is the document's largest topic, which asks whether the theme *dominates*. Secondary rule (`nmf_top2`, v1.1): positive if the topic is one of the document's two largest topics with nonzero weight, which asks whether it is *present*. |
| LLM | `claude-opus-5-5` only, effort `low`, zero-shot, with the codebook definitions in the prompt and JSON output (`yes`/`no`/`uncertain`). Primary result: run 1, with `uncertain` counted as `no`; a sensitivity analysis counts `uncertain` as `yes`. Runs 2 and 3 measure self-consistency. There is no fallback to another model (v1.1). Refusals, technical failures and invalid output are recorded as such, excluded from the LLM's metrics rather than counted as `no`, and reported in a coverage table. |

No method is tuned on the study sample. The dictionary and the topic rule were written before sampling, and the prompt reuses the codebook wording. The automated methods are run only after both coders have finished.

## Analysis (`analyze.py`)

**Agreement.** For each construct: percent agreement and Cohen's kappa on the three values (`1`/`0`/`u`), with a 95% bootstrap interval (2,000 resamples of items). Secondary: kappa on items where neither coder used `u`. Kappa is sensitive to prevalence, so a modest kappa for the rare innocence category is not by itself evidence of poor coding. I report the raw counts next to it.

**Method performance.** For each construct and method, against the adjudicated labels: precision, recall, F1 and accuracy, with 95% bootstrap intervals. Also the paired F1 difference between each pair of methods, with a bootstrap interval. Since each item is one person's statement, items are resampled independently.

**Factual innocence (secondary).** Innocence is also evaluated with legal-justification claims (**L**) excluded, which is closer to Eaton & Theuer's variable. The type is recorded by both coders and resolved at adjudication. Agreement on F versus L is reported for items both coders coded `1`.

**Prevalence.** The share of positives in the sample, with a Wilson interval. It is descriptive only, and not comparable to Eaton & Theuer's 32.5% without qualification: the period is different (1982–2026 against 1982–2007) and so is the denominator.

**Exposure sensitivity (v1.1).** Agreement and every method's metrics are also reported separately for items with documented project exposure (35) and without it (115). Point estimates only; these subgroups are too small for useful intervals.

**Undefined estimates (v1.1).** If a statistic cannot be computed (for example kappa when both coders use one value throughout, or recall with no positives), it is reported as not estimable. A bootstrap interval is reported only if at least 95% of resamples give a defined value.

**Errors.** Every false positive and false negative is listed in `outputs/errors.csv`. I read them and group them by cause, for example: condolence versus apology, quoted prayer, accident account, system criticism, negation, recorder annotation.

## How results will be read

- A method "agrees well" with human coding if its F1 interval lies above 0.80. This is a descriptive threshold, not a significance test.
- Differences between methods are reported with their intervals. With about 45 and 12 positives, small differences will not be distinguishable, and I will say so.
- Whatever the results, I report all three methods for both constructs.

## Amendments

### Version 1.1 (9 November 2026, before any coding)

An external review of version 1.0 found problems that I corrected before coding started:

1. **Exposure claim corrected.** Version 1.0 described the sample as statements "I have not previously read or labelled". Earlier project records include 35 of them (see Sample). The sample is unchanged; exposure is now flagged and analysed as a sensitivity check.
2. **Lock enforced.** `analyze.py` and `llm_classify.py` now stop if the frozen files have changed (version 1.0 only printed a warning). `llm_classify.py`, `freeze.py` and `exposure.csv` are now also frozen.
3. **Undefined estimates.** Degenerate data (for example both coders coding every item `0`) crashed the bootstrap in version 1.0; such cases are now reported as not estimable.
4. **LLM outcomes separated.** Version 1.0 would have scored refusals and failures as `no`. They are now recorded and excluded, with coverage reported. The server-side fallback to another model is removed, so the LLM result describes one model.
5. **Topic-model scope.** The primary NMF rule tests whether a theme dominates a statement, while human coding asks whether an expression is present. The `nmf_top2` rule is added as a label-free secondary rule, and the Scope paragraph limits conclusions to the operationalizations tested.

The codebook, the sample, the dictionary rules, the primary NMF rule and the LLM prompt are unchanged.

## Deviations

None so far.
