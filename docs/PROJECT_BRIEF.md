# Project brief

## Purpose
This project explores recurring expressions in published Texas last statements
and asks how much the resulting NMF components depend on preprocessing,
initialization and selected document exclusions.

It studies recorded language. It does not determine guilt, sincerity, remorse
or an individual's psychological state.

## Data and approach
An inventory of 603 execution records leads to 480 person-level candidate
documents, 479 prepared documents and 477 documents with retained TF-IDF
features. The current inclusion ledger documents 123 historical exclusions.
Four short-response attribution questions and one translated-utterance
inclusion boundary remain explicit.

The analysis uses contraction-aware normalization, a 3,196-feature unigram and
bigram TF-IDF representation, and NMF with 4, 6 and 8 components. It compares
random initializations both pairwise and against a reference fit. Additional
checks remove short texts or selected prayer-containing records while keeping
vocabulary and IDF fixed.

Fifty records, sampled equally across five decades, were used to develop and
adjudicate eight manual coding categories. They were not used to fit NMF.
Their topic-coefficient contrasts are descriptive because the records were
already used in guideline development and non-blind review.

## Findings
The six-component reading includes apology and forgiveness, close relationships,
case-related denial and explanation, repeated prayer, thanks and support, and
encouragement. This is an illustrative interpretation rather than a unique
optimal taxonomy.

At six components, the lower quartile of random-pair matched cosines is 0.938,
but the minimum is 0.054. High typical agreement does not remove isolated
component instability. The analyses do not establish a unique winning k.

Manual-label contrasts show higher corresponding coefficients for some
prespecified positive groups, including apology/forgiveness and innocence
disputes. Complete 0/1/u results and group sizes remain visible; this is not
independent validation or evidence of a working innocence classifier.

Close reading reveals a central failure mode: a lexically similar component
can score an explicit denial, uncertainty about what to say, and a quotation
of other people's denial followed by the speaker's own admission. Numerical
similarity alone does not establish the meaning of an utterance.

## Technical contribution
The project connects source inventory construction, traceable text preparation,
uncertainty-aware coding, numerical diagnostics and qualitative error analysis.
An audit identified brittle keyword-order checks: some unigrams and bigrams
have exactly identical TF-IDF columns. The repair retains the full feature
space, groups equivalent columns for keyword overlap only, and validates
numerical weights rather than ranked word strings. Full regenerated reference
matrices are explicitly distinguished from missing historical full matrices.

## Reproduction and limits
The Release supplies hashed curated inputs. The repository includes scripts,
saved results, executed analysis notebooks, an inclusion ledger and an
audit-informed follow-up protocol committed before the new comparisons.
Downstream reproduction is supported; collection and extraction cannot be
fully reconstructed from the Release because raw HTML and complete upstream
tables are not bundled.

Availability differs across decades. The development sample is not
representative of corpus composition. Dependencies are recorded in manifests
but not fully locked. Selected-prayer deletion is an influence check informed
by the observed component, not independent confirmation. AI assisted code,
documentation and interpretation; the owner reviewed the coding decisions.

## Short interview explanation
I built an exploratory NLP pipeline for published Texas last statements,
from a 603-record source inventory to 477 modeled documents. Beyond fitting
NMF, I examined whether the components survived initialization changes and
document exclusions, and compared them descriptively with 50 manually reviewed
records. A key finding was that numerical stability does not guarantee semantic
validity: similar words can express denial, uncertainty or an admission that
quotes someone else's denial. I also repaired tie-sensitive reproducibility
checks and documented exclusions and unresolved cases. The project demonstrates
text processing, model diagnostics and careful interpretation; it does not
claim to infer guilt or psychological state.
