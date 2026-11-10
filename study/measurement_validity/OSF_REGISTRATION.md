# OSF registration text

Text for the OSF Preregistration template, to be submitted when version 1.3 is frozen. Each heading below is a field of the template. `PROTOCOL.md` and `CODEBOOK.md` are the authoritative documents and are attached to the registration; this text summarises them and must not differ from them. Fill the three fields marked **[at freeze]** before submitting.

## Study information

**Title.** Measuring apology and innocence claims in Texas last statements: keyword, topic-model, LLM and supervised classifiers against blind human coding

**Authors.** Dora (Ziyi) Zhuang, McGill University. [Supervisor's name, only if they agree to be listed.]

**Description.** Eaton & Theuer (2009) hand-coded the last statements of people executed in Texas, with two-coder kappas of .89–.99. Computational studies of such texts usually rely on cheaper measures. This study tests how closely five kinds of automated measure reproduce blind two-coder human coding of apology and innocence claims in 150 statements: a keyword dictionary, two rules on a six-topic NMF model, a zero-shot LLM, a BERT classifier trained on Eaton & Theuer's codes, and a TF-IDF logistic-regression baseline trained on the same codes. Condolence ("sorry for your loss") is coded separately from apology, so that both this study's narrower apology definition and Eaton & Theuer's broader one can be evaluated. The main output is the pattern of errors: which look-alikes each method counts as apology or innocence. The study measures what people said, as public final speech acts, not their inner states.

**Hypotheses.** This is a measurement study; its outputs are estimates with intervals, not tests of a null hypothesis. The following expectations are stated in advance:

1. The keyword dictionary over-detects apology under this codebook's definition, mainly by counting condolences.
2. Models trained on Eaton & Theuer's codes score higher against the broad apology definition (apology or condolence) than against the narrow one, and their apology predictions agree closely with the dictionary's.

## Design plan

**Study type.** Observational study: measurement comparison on existing public texts.

**Blinding.** The two coders work independently, each with the items in a different random order and identified only by an item code. They see no automated output, no other coder's labels and no case information until both have finished. Automated methods run only after both coders have finished.

**Study design.** Each of the 150 statements is coded by both coders for apology, condolence and innocence claims (`1`, `0` or `u`), with innocence claims marked factual (F) or legal (L). Disagreements and `u` codes are adjudicated by discussion; the adjudicated labels are the reference standard. Every automated method is scored against them.

**Randomization.** The 150 statements are a simple random sample (seed 20261109) of the 430 statements outside the 50-statement development sample.

## Sampling plan

**Existing data.** Registration prior to creation of the human coding and of all model predictions. The statements themselves are public records and already exist.

**Explanation of existing data.** The texts are the last statements published by the Texas Department of Criminal Justice (snapshot through 7 October 2026, released as data-v1 with SHA-256 `c56a4be1915cdaefd5ea1878da47d009f0cb9de8082401f7de241d42a7266168`). Both coders have read the 50 development statements, which are excluded from evaluation. 35 of the 150 sampled statements appear in earlier project records, 7 of them with decisions on excerpts; they are flagged and reported as a separate group. The topic model was fitted on all statements without labels before this study. Eaton & Theuer's codes have been requested from the authors and have not been received.

**Data collection procedures.** Coder A is the author; coder B is an English teacher who has not seen the project's labels or analyses. Both read the English text with the English codebook, using no machine translation, after coding and discussing ten practice items from the development sample.

**Sample size.** 150 statements, about 30–45 expected apologies and 10–25 innocence claims.

**Sample size rationale.** The number two coders can code carefully in a few hours each, while giving an F1 interval narrow enough to tell whether a method clears 0.80 for apology. Innocence intervals will be wide and are reported as such.

**Stopping rule.** Fixed sample; no interim analysis.

## Variables

**Manipulated variables.** None.

**Measured variables.** Human codes: apology, condolence, innocence (with F/L type). Derived: broad apology (apology or condolence) and factual innocence (innocence with legal-justification claims set aside). Automated predictions for apology and innocence from each method.

**Indices.** Per method and target: precision, recall, F1 and accuracy. Between coders: percent agreement and Cohen's kappa.

## Analysis plan

**Statistical models.** No models are fitted to the evaluation data. Supervised training: BERT (`bert-base-uncased`, learning rate 2e-5, 4 epochs, batch 16, weight decay 0.01, 10% warmup, class-weighted loss, five seeds averaged, threshold 0.5) and TF-IDF with logistic regression (unigrams and bigrams, minimum document frequency 2, C = 1, balanced weights), both on Eaton & Theuer's codes with the study-sample statements removed. Settings are fixed in advance; there is no hyperparameter search. A learning curve uses nested subsets of 25%, 50% and 100% of the training statements.

**Inference criteria.** 95% percentile bootstrap intervals over statements (2,000 resamples). A method agrees well with human coding when its F1 interval lies above 0.80. Differences between methods are paired F1 differences with bootstrap intervals.

**Data exclusion.** Statements still coded `u` after adjudication are excluded from the evaluation of that target and counted. LLM refusals, failures and invalid outputs are excluded from the LLM's metrics and reported in a coverage table.

**Missing data.** A statistic that cannot be computed is reported as not estimable; an interval is reported only when at least 95% of bootstrap resamples give a defined value.

**Exploratory analysis.** Agreement between every pair of methods; per-seed BERT results; F1 against each coder separately; comparison of Eaton & Theuer's codes with the adjudicated labels on the 98 study-sample statements they coded; results by prior-exposure group; a categorised reading of every error.

## Other

**Fallback.** If Eaton & Theuer's codes have not arrived by 15 January 2027 or cannot be matched to the corpus, the two coders each code 140 of the remaining 280 statements, and the supervised methods are trained on those labels instead.

**Frozen materials.** [at freeze] Repository commit SHA: `...`. [at freeze] SHA-256 of `protocol_lock.json`: `...`. [at freeze] Date of freeze: `...`.
