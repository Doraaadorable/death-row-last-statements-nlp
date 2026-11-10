# Protocol: measuring apology and innocence claims in last statements

**Version 1.3: draft under review by the supervising professor.** The last frozen version is 1.2 (`protocol_lock.json`; versions 1.0 and 1.1 in `protocol_lock_v1.0.json` and `protocol_lock_v1.1.json`). Version 1.3 will be frozen with the codebook, samples and method code before coding begins, and this paragraph updated. Changes are listed under Amendments and Deviations.

## Question

Eaton & Theuer (2009) coded Texas last statements by hand, with two-coder kappas of .89–.99. Computational work on similar texts usually relies on cheaper measures: keyword lists, topic models and, more recently, language models. This study asks:

> For apology and innocence claims, how closely do a keyword dictionary, an NMF topic model and a zero-shot LLM agree with blind two-coder human coding?

Version 1.3 adds a supervised question:

> Can a BERT classifier trained on Eaton & Theuer's expert coding reproduce this study's blind human coding on statements it has not seen?

Each result applies to the specific rules tested: this keyword list, these two topic-model rules, this prompt with this model, and this fine-tuning recipe with these training labels. For apology, every method is scored on both this codebook's definition and Eaton & Theuer's broader one, so the results also show how far a model trained on the broader definition separates apology from condolence. The central output is the pattern of errors, such as condolence read as apology, accident read as denial, or a theme detected only when it dominates a statement. These confusions decide what a count of "apologies" or "innocence claims" actually measures.

This is groundwork for studying psychological expression in last statements. Before counting how often people apologize or protest their innocence at the end of their lives, the counts have to measure those acts and not their look-alikes.

## Constructs

Both constructs are defined in `CODEBOOK.md`, building on the separate variables in Eaton & Theuer (2009, pp. 334–335):

- **Apology**: an apology tied to the speaker's own act or the harm they caused, or a direct apology with no object stated. Condolence that is not tied to the speaker ("sorry for your loss") is coded `0`. This is narrower than Eaton & Theuer's rule, under which any "sorry" counts (32.5% of statements), and it is where a keyword method is most likely to fail.
- **Condolence** (added in version 1.3): "sorry" about another person's loss or pain, or about the situation, not tied to the speaker's own act. It is coded by people only. Apology or condolence (`apology_broad`) corresponds to Eaton & Theuer's apology variable.
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

## Supervised methods (version 1.3, `bert_classify.py`, `tfidf_classify.py`)

**Primary training set: Eaton & Theuer's codes.** Their two raters coded 305 statements from executions in 1982–2007, with kappas of .89–.99. Their apology variable maps to `apology` and their claims-of-innocence variable to `innocence`; present is `1`, absent `0`, unclear `u` (their unclear also holds coder disagreements, which are therefore left out of training). Statements are matched to execution numbers by name and execution date. The codes are third-party data: they stay outside version control (`coding/eaton_theuer*` is in `.gitignore`), are used only under the terms the authors set, and only statistics derived from them are published. 98 of the 150 study-sample statements fall in their period; these are removed from training and used only for the comparison of the two teams of human coders below. The two coders of this study code only the study sample.

Their definitions differ from this codebook in two ways that shape the result (codebook differences 1 and 2):

- **Apology.** They code an apology whenever the speaker said they were sorry, including sorrow for the family's loss. A model trained on their labels learns this broader definition, so its primary apology comparison is with `apology_broad` (apology or condolence). Scored against this codebook's narrower apology, it is expected to mark condolences as apologies; that score measures whether anything in their labels lets the model separate the two. Its apology predictions are expected to be close to the keyword dictionary's, which detects the same word.
- **Innocence.** Their variable probably excludes legal justification, so the model's innocence predictions are compared with factual innocence as well as with all innocence claims.

**Fallback training set: this study's codebook.** If Eaton & Theuer's codes have not arrived by 15 January 2027, or cannot be matched to the corpus, the training set is the 280 statements outside the study sample and the development sample (`training_sample.csv`, `make_training_sample.py`, seed 20261111), split at random into 140 per coder. Each coder codes their half alone with the frozen codebook (`coding/train_A.xlsx`, `coding/train_B.xlsx`), after adjudication of the study sample. If both sets exist, both models are reported, `bert` (Eaton & Theuer) and `bert_own` (this codebook).

**Model and training.** `google-bert/bert-base-uncased`, fine-tuned separately for each construct as a binary classifier. Items coded `u` are left out of training. Statements longer than 512 tokens keep their first 128 and last 382 tokens. Learning rate 2e-5, 4 epochs, batch size 16, weight decay 0.01, linear schedule with 10% warmup, cross-entropy with the positive class weighted by the negative-to-positive ratio. These settings are fixed in advance: there is no hyperparameter search and no validation split. Five seeds are trained; the prediction is `1` when the mean positive-class probability over the five seeds is at least 0.5.

**Learning curve.** The same recipe is also trained on nested random subsets of 25% and 50% of the training statements (seed 20261111), five seeds each.

The model revision, library versions, GPU and training counts are written to `outputs/bert_run_<labels>.json`.

**Supervised baseline (`tfidf_classify.py`).** TF-IDF on word unigrams and bigrams (lowercased, minimum document frequency 2, sublinear term frequency) with logistic regression (C = 1, balanced class weights, liblinear). It is trained on exactly the same statements, labels and learning-curve subsets as BERT, with settings fixed in advance. The fit is deterministic, so there is one run per training size. The comparison of `bert` with `tfidf` separates what BERT adds from what supervision on these labels alone achieves.

## Analysis (`analyze.py`)

**Agreement.** Per construct: percent agreement and Cohen's kappa on `1`/`0`/`u`, with a 95% bootstrap interval (2,000 resamples of items); secondary, kappa on items where neither coder used `u`. Kappa drops with low prevalence, so raw counts are reported next to it.

**Method performance.** Per construct and method, against the adjudicated labels: precision, recall, F1 and accuracy with 95% bootstrap intervals, and the paired F1 difference between each pair of methods. Items are resampled independently, one statement per person.

**Supervised methods.** `bert` and `tfidf` (Eaton & Theuer's codes) and, if used, `bert_own` and `tfidf_own` (this codebook) enter every table above as further methods, including the paired F1 differences. Cohen's kappa between the predictions of every pair of methods is reported (`method_agreement.csv`), so that the expected closeness of `bert` and the dictionary on apology is measured rather than assumed. Per seed and training size, F1 is reported without intervals (`supervised_run_metrics.csv`): the spread across BERT seeds shows how stable fine-tuning is at this data size, and the three training sizes form the learning curve for both models.

**Coder imprint.** Before adjudication, every method is scored against each coder's own labels (`coder_specific_f1.csv`). If the fallback training set is used, a gap between F1 against coder A and against coder B that is larger for `bert_own` than for the unsupervised methods would show the model following one coder's reading; training labels by coder are counted in `bert_run_own.json`.

**Two teams of human coders.** For study-sample statements that Eaton & Theuer coded, their codes are compared with the adjudicated labels: agreement, kappa and the counts of statements only one side marked `1` (`eaton_theuer_agreement.csv`).

**Factual innocence.** Innocence is also evaluated with legal-justification claims (**L**) set aside, which is closer to Eaton & Theuer's variable. F/L agreement is reported for items both coders coded `1`.

**Broad apology.** Every method's apology prediction is also scored against `apology_broad`, apology or condolence, which is `u` when neither is `1` and either is `u`. Agreement between the coders is reported for condolence and `apology_broad` as for the other variables, and condolence is adjudicated with them.

**Prevalence.** The share of positives in the sample, with a Wilson interval, for every target and for condolence. Eaton & Theuer cover 1982–2007, so the comparison of `apology_broad` with their 32.5% is descriptive.

**Exposure groups.** Agreement and each method's metrics are reported separately for the 35 items with documented project exposure and the 115 without, as point estimates.

**Undefined statistics.** A statistic that cannot be computed (for example kappa when both coders use a single value, or recall with no positives) is reported as not estimable. An interval is reported when at least 95% of resamples give a defined value.

**Errors.** Every false positive and false negative goes to `outputs/errors.csv`. I read each one and record its cause, such as condolence, quoted prayer, accident account, system criticism, negation or recorder annotation.

## Reading the results

- A method agrees well with human coding when its F1 interval lies above 0.80.
- Method differences are reported with their intervals; with about 45 and 12 positives, only large differences will be distinguishable.
- All methods are reported for both constructs.
- The supervised method learns from expert human coding, so its result shows whether that coding is learnable from about 200 examples and transfers to this codebook; the learning curve shows whether more coded statements would be likely to help.

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

### Version 1.3 (November 2026)

Adds the supervised method, at the suggestion of the supervising professor, before either coder started the study sample:

1. **Condolence** is added to the codebook (version 1.1) and the coding sheets, and `apology_broad` (apology or condolence) is added as a target, so that results can be set against Eaton & Theuer's apology variable without giving up the distinction between apology and condolence. No coding had started.
2. **Primary training set**: Eaton & Theuer's codes, requested from the authors on 9 November 2026, with the mapping rules above.
3. **Fallback training set**: the remaining 280 statements, 140 coded by each coder, used if the codes have not arrived by 15 January 2027 (`make_training_sample.py`, `training_sample.csv`, `coding/train_A.xlsx`, `coding/train_B.xlsx`).
4. **`bert_classify.py`** and the TF-IDF baseline **`tfidf_classify.py`**, with the settings above, and `SUPERVISED_THRESHOLD` in `methods.py`.
5. **Analysis**: the supervised method in all tables, per-seed and learning-curve results, agreement between methods, coder-specific F1 and the comparison with Eaton & Theuer's codes (`analyze.py`).
6. **Lock**: `bert_classify.py`, `tfidf_classify.py`, `make_training_sample.py` and `training_sample.csv` are added to the lock; the training sheets and supervised predictions are added to the results that block later amendments.

The study sample, the items and order of the coding sheets, the unsupervised methods and the LLM prompt are unchanged.

## Deviations

None so far.
