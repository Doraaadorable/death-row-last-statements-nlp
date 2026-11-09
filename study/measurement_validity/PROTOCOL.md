# Protocol: can automated methods measure apology and innocence claims in last statements?

Version 1.0. This protocol is frozen, together with the codebook, sample and method code, in `protocol_lock.json` before any human coding starts. Changes after freezing are listed under "Deviations".

## Question

Published research codes Texas last statements by hand. Eaton & Theuer (2009) report two-coder kappas of .89–.99 and an apology rate of 32.5% for 1982–2007. Computational studies of the same kind of text often rely on keyword lists or topic models instead. I ask whether those cheaper measures agree with careful human coding on these short, formulaic, institutionally recorded texts:

> For apology and innocence claims, how closely do a keyword dictionary, an unsupervised topic model and a zero-shot large language model agree with blind two-coder human coding?

The study does not estimate how common apology or innocence claims are in the full corpus. It also does not make claims about speakers' sincerity or mental states.

## Constructs

Two constructs, defined in `CODEBOOK.md` and built on the separate variables in Eaton & Theuer (2009, pp. 334–335):

- **Apology**: an apology tied to the speaker's own act or harm, or a direct apology with no object stated. Condolence that is not tied to the speaker ("sorry for your loss") does not count. This is narrower than Eaton & Theuer's "said they were sorry" (32.5% of statements), so the word "sorry" alone is not sufficient, which is a direct test of keyword methods.
- **Innocence claim**: a claim that the speaker should not stand convicted, either by denying the act (**F**, factual) or by claiming it was lawful, such as self-defense (**L**, legal). Accident and excuse accounts do not count. Eaton & Theuer report 16.4% for claims of innocence. The wording varies ("I didn't do this", "wrong man"), and claims are easy to confuse with criticism of the system or accident accounts.

The deliberate differences from Eaton & Theuer are listed at the end of `CODEBOOK.md`.

## Sample

- Pool: the 480 person-level statements in the data-v1 snapshot, minus the 50 statements in the earlier development sample, which I had already read and labelled. 430 remain.
- Simple random sample of **150** (seed 20261109, `make_sample.py`). Each coder sees the same items in a different random order, identified only by an item code.
- 10 practice items come from the development sample. The coders discuss them together before the main coding, and they are not evaluated.

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
| Topic model | The existing six-topic NMF (fitted on all 477 documents without labels). Positive if the apology topic (topic 1) or the denial topic (topic 3) is the document's largest topic. |
| LLM | `claude-opus-5-5`, effort `low`, zero-shot, with the codebook definitions in the prompt and JSON output (`yes`/`no`/`uncertain`). Primary result: run 1, with `uncertain` counted as `no`. Runs 2 and 3 measure self-consistency. If the model declines a request, the API falls back to another model; the served model is recorded for every item. |

No method is tuned on the study sample. The dictionary and the topic rule were written before sampling, and the prompt reuses the codebook wording. The automated methods are run only after both coders have finished.

## Analysis (`analyze.py`)

**Agreement.** For each construct: percent agreement and Cohen's kappa on the three values (`1`/`0`/`u`), with a 95% bootstrap interval (2,000 resamples of items). Secondary: kappa on items where neither coder used `u`. Kappa is sensitive to prevalence, so a modest kappa for the rare innocence category is not by itself evidence of poor coding. I report the raw counts next to it.

**Method performance.** For each construct and method, against the adjudicated labels: precision, recall, F1 and accuracy, with 95% bootstrap intervals. Also the paired F1 difference between each pair of methods, with a bootstrap interval. Since each item is one person's statement, items are resampled independently.

**Factual innocence (secondary).** Innocence is also evaluated with legal-justification claims (**L**) excluded, which is closer to Eaton & Theuer's variable. The type is recorded by both coders and resolved at adjudication. Agreement on F versus L is reported for items both coders coded `1`.

**Prevalence.** The share of positives in the sample, with a Wilson interval. It is descriptive only, and not comparable to Eaton & Theuer's 32.5% without qualification: the period is different (1982–2026 against 1982–2007) and so is the denominator.

**Errors.** Every false positive and false negative is listed in `outputs/errors.csv`. I read them and group them by cause, for example: condolence versus apology, quoted prayer, accident account, system criticism, negation, recorder annotation.

## How results will be read

- A method "agrees well" with human coding if its F1 interval lies above 0.80. This is a descriptive threshold, not a significance test.
- Differences between methods are reported with their intervals. With about 45 and 12 positives, small differences will not be distinguishable, and I will say so.
- Whatever the results, I report all three methods for both constructs.

## Deviations

None so far.
