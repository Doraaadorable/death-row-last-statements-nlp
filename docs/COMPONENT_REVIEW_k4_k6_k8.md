# Component interpretation review: k=4/6/8

## Status and evidence
Partial working record, prepared from the owner's executed notebook output and
subsequent reading discussions. Interpretations are provisional and AI-assisted;
this is not independent blind coding or a completed owner-adjudicated review.
Frozen eight-label annotations and all model outputs are unchanged.

The planned review covers 18 components. Initial leading-example reading now
covers all four k4 topics, all six k6 topics and all eight k8 topics. Every
component has a provisional description and responses to the same three
questions. Initial coverage is complete; exhaustive boundary review,
independent validation and final owner adjudication are not.

## Reading procedure and limits
Notebook 04 ranks positive coefficients, restricts displayed examples to at
least 20 words and breaks coefficient ties by execution number.
For k6 topic 1, displayed ranks 1-6 and 151-153 were read (offsets 0, 3 and 150).
For the other seventeen entries, only ranks 1-3 were read. These are purposive
diagnostic readings, not representative samples or estimates of semantic purity.
Additional lower-ranked and short-text checks remain pending.

Eligible-document counts mean only positive coefficient plus the display word
threshold, not counts of people expressing the proposed theme. Coefficients are
not probabilities or human labels. All questions below concern textual evidence,
not sincerity, actual guilt or private psychological state.

## k6, topic 1
Provisional description: apology and requests for forgiveness, often accompanied
by wishes for peace. Nine documents examined: 293, 414, 542, 277, 433, 413,
376, 482 and 77.

1. Specific pattern: sorry, forgive, peace, pain and related language.
2. Documentary support: 293 explicitly refers to pain the speaker caused;
277, 433 and 413 likewise link the speaker to pain. 414 requests forgiveness
without a comparably specific harm acknowledgment. 542 combines repeated
apology, requests for forgiveness and wishes for closure.
3. Contradictions and mixed content: 376 combines forgiveness with family and
faith; 482 combines apology, self-explanation and opposition to execution.
77 requests prayers and invokes Jesus without an explicit apology or request
for forgiveness. Its positive coefficient is a boundary example, not a
classification error: the model did not assign a binary apology label.

Different directions of forgiveness occur: seeking forgiveness from people,
seeking it from God, and reporting divine forgiveness. The lexical component
does not distinguish these relations reliably. Do not rename this component
harm acknowledgment or remorse. Frozen F=u for 433 is unchanged; isolated pray
does not settle its religious interpretation.

## k6, topic 4
Provisional description: scripture and formulaic prayer.
Documents examined: 352, 423 and 274.

1. Specific pattern: repeated passages with thy, thou, heaven and kingdom.
2. Documentary support: the three texts contain extensive overlapping prayer
wording. 274 is almost entirely prayer; 352 and 423 also contain personal remarks.
3. Contradictions and mixed content: 352 combines apology and harm acknowledgment
with prayer; 423 combines relational language with prayer. This is a repeated
expression-form component, not a general religious-belief measure. In contrast,
77 explicitly invokes Jesus but has only a small topic-4 coefficient.

The faith/spirituality label is broader than this component. Repeated wording
does not imply shallow or deep faith. Lower-ranked and short examples remain
to be checked before review completion.

## k6, topic 5
Provisional description: thanks and support, mixed with religious and closing
language. Documents examined: 313, 569 and 558.

1. Specific pattern: thank, like thank, support alongside ready, warden, Jesus
and Lord. The like thank feature is partly a conventional expression frame,
not evidence of a separate substantive concept.
2. Documentary support: 313 thanks attendees and religious supporters, invokes
Christian language and ends ready for the warden. 569 thanks God and others,
apologizes and thanks the warden; its final thanks alone does not establish
readiness to begin the procedure. 558 thanks community and overseas supporters,
apologizes and explicitly ends the statement and permits the warden to proceed.
3. Contradictions and mixed content: 558 contains no explicit religious wording,
so religion is not common to all three. All combine gratitude with other
expressions; the top words do not justify a single pure religious or readiness
label. Keep the mixed description.

These three documents suggest co-occurrence in statement composition. They do
not establish that the same combinations recur throughout the corpus or that
NMF models clause order. Apology/harm language in 569 and 558 is not erased by
their high topic-5 coefficients.

## k8, topic 5
Provisional description: Christian praise and supplication.
Documents examined: 102, 246 and 153.

1. Specific pattern: Jesus, Lord, Christ, praise and related language.
2. Documentary support: 102 emphasizes praise, salvation and entrusting the
spirit; 246 repeats praise and invokes Jesus Christ; 153 contains extended
Christian supplication alongside personal remarks.
3. Contradictions and mixed content: 246 also criticizes justice. 153 combines
apology, affection and farewell language. This component does not cover every
religious tradition or all spiritual expression. Frozen H=u for 153 remains
unchanged.

This reference solution is interpretable, but prior random-initialization
comparison gave mean matched cosine about 0.326 for this component. Clear
reference examples do not establish reproducible component recovery.

## k8, topic 8
Provisional description: gratitude and acknowledgment of support, with
relational and closing language. Documents examined: 558, 531 and 345.

1. Specific pattern: thank, friends, family, support and conventional thanks
frames; religious vocabulary is less prominent in the leading terms than in
k6 topic 5.
2. Documentary support: 558 thanks community and overseas supporters; 531
thanks supporters and loved ones; 345 thanks family, friends and people who
continued their friendship despite disagreement.
3. Contradictions and mixed content: 558 also apologizes and explicitly permits
the procedure to continue. 531 combines thanks and affection, but thanking the
warden alone is not an explicit readiness statement. 345 ends by addressing
the warden; the ellipsis does not justify reconstructing an unreported
instruction. The unspecified decision mentioned in 345 is not identified here.

Compared with the three reviewed k6 topic-5 examples, these examples support
a narrower gratitude/support description in this reference fit. They do not
establish purity across the component or a causal split between fitted models.

## k8, topic 7
Provisional description: procedural readiness and statement-closing language,
sometimes mixed with farewell or home imagery.
Documents examined: 129, 398 and 461.

1. Specific pattern: ready, ready warden and related closing expressions.
2. Documentary support: 129 explicitly says ready to the warden; 398 explicitly
says ready to go; 461 explicitly says ready to go to the warden.
3. Contradictions and mixed content: 129 refers to a prepared media statement,
whose content cannot be inferred from this excerpt. 398 also expresses
affection and invokes eternity/home imagery. 461 combines affection and
readiness with granting forgiveness to others, not asking for forgiveness.
The referent of atrocity and the meaning of coming home dad are not resolved
by this reading. No acceptance of the justice of the sentence, calmness or
private willingness is inferred from readiness wording.

Prior numerical checks illustrate distinct stability questions: topic 7 had
mean reference-matched cosine about 0.998 across random starts, but only about
0.278 after removing modeled texts shorter than ten words. Numerical
convergence and initialization agreement do not imply robustness to document
composition. The removal refits also change the optimization problem and its
initialization, so the comparison does not isolate a causal effect of short
wording alone. Inspect short examples next: the current 20-word display rule
omits precisely some texts implicated in that sensitivity.

## k8 topic 7: short-text diagnostic extension
The owner inspected the ten highest positive topic-7 coefficients among
documents shorter than ten words. Execution IDs were 38, 525, 447, 285, 15,
133, 161, 475, 34 and 396. These IDs are execution_number values, not the
DataFrame row index. This expands the topic-7 entry; it does not complete the
other component reviews.

Ready and statement-closing expressions dominate the highest examples.
475 says no final statement without explicitly saying ready; 396 expresses
love and anticipated separation but has coefficient only about 0.0015.
The component therefore does not capture every farewell expression. No
psychological acceptance, sincerity or religious interpretation is inferred.

A full-corpus diagnostic of the frozen k8 coefficients gave:

| Length group | Documents | Positive topic-7 coefficients | Median coefficient | Coefficient sum | Share of coefficient sum |
|---|---:|---:|---:|---:|---:|
| At least 10 words | 456 | 245 | 0.0034 | 14.8663 | 81.7947% |
| Under 10 words | 21 | 10 | 0.0000 | 3.3088 | 18.2053% |

The 21 short documents are approximately 4.4% of the 477 modeled documents.
Seven of the ten highest coefficients, and seven of the twenty highest,
belong to short documents. Thus short documents are concentrated at the
extreme high end, but most coefficient mass comes from longer documents.
Do not describe this component as mostly supported by short documents on the
basis of coefficient totals, or claim that every short document receives a
high score: 11 of the 21 have zero coefficients.

These totals are descriptive coefficient-mass summaries within one fixed fit,
not theme prevalence, semantic validity or the fraction of reconstruction
causally attributable to short documents. The sums are not an exact feature-
space energy decomposition because NMF components overlap. The previous
removal fit's low matched cosine (about 0.278) describes a change in the
refitted solution; the refit also changes initialization and optimization.
It does not isolate why the component changed. A high remaining coefficient
mass does not guarantee preservation of a component after refitting.

## k6, topic 2
Provisional description: expressed affection and relational messages.
Documents examined: 201, 399 and 445.

1. Specific pattern: love, tell family, mom and associated relational words.
2. Documentary support: 201 addresses family and Kami with love and continued
presence; 399 asks for love to be conveyed to family; 445 addresses family and
named people with love and anticipated separation.
3. Contradictions and mixed content: 399 also encourages listeners to keep
their head up, while 445 also says ready. Do not treat affection, encouragement
and procedural closure as mutually exclusive person-level categories.
The source wording I live y'all in 445 is retained; no silent correction is
introduced or used as proof of a different intent.

## k6, topic 6
Provisional description: stay-strong encouragement with relational language.
Documents examined: 360, 428 and 236.

1. Specific pattern: strong, stay strong and stay dominate the leading features.
2. Documentary support: all three explicitly urge recipients to stay strong
while expressing love. 360 and 236 repeat that instruction; 428 also thanks
supporters and says at peace.
3. Contradictions and formulaic repetition: the examples contain affection
as well as encouragement; repeated stay strong may help explain lexical
concentration but has not been isolated experimentally. Their coefficients
do not measure a person's own psychological strength. The presence of an
encouragement expression is not evidence that encouragement is absent from
topic-2 examples.

Execution 399 says keep your head up, illustrating encouragement without the
exact stay-strong formula. This motivates a natural-language boundary check;
its subsequently inspected topic-6 coefficient is zero despite that
encouragement wording. This is a semantic boundary case, not a classification
error, because NMF did not produce a binary encouragement prediction. Neither component is a validated
speech-act detector. Distinguishing communicative functions and distinguishing
lexical formulas are separate interpretation questions.

## k4, topic 2
Provisional description: relational affection and care, mixed with stay-strong
encouragement and support. Documents examined: 560, 201 and 374.

1. Specific pattern: love and tell lead the terms, alongside strong, stay
strong, family and care.
2. Documentary support: 560 repeats I love you and closes with take care;
201 expresses love to family and Kami; 374 thanks family and friends and
urges them to stay strong and take care of themselves.
3. Contradictions and mixed content: 374 combines thanks, encouragement and
closing language rather than explicit I love you wording. The phrase about
five dollars in 560 is not assigned a motive or reconstructed cultural
meaning here. The component remains a lexical mixture, not a pure affection
or encouragement category.

## Affection/encouragement: cross-k and within-document check
k4 topic 2 has cosine approximately 0.904 with k6 topic 2 and 0.556 with k6
topic 6. These are overlapping vector similarities, not additive fractions or
proof that the k4 component was causally split by increasing k.

The owner inspected the following frozen k6 coefficients:

| Execution | Topic 2 | Topic 6 |
|---|---:|---:|
| 201 | 0.4334 | 0.0000 |
| 236 | 0.0000 | 0.5033 |
| 360 | 0.0000 | 0.7104 |
| 399 | 0.4189 | 0.0000 |
| 428 | 0.0319 | 0.5847 |
| 445 | 0.3865 | 0.0000 |

236 and 360 explicitly express love despite zero topic-2 coefficients. 399
says keep your head up despite a zero topic-6 coefficient. Zero coefficients
do not establish absence of the associated communicative function; nonnegative
factorization coefficients depend on the joint reconstruction across components.
The examples support sensitivity to wording and component overlap, not a
controlled causal finding that replacing one phrase with another changes
the result. Length, other words and repetition also differ across documents.

A finer lexical distinction at k6 is useful for description but does not
establish better semantic detection or justify selecting k6 by itself.

## k4, topic 1
Provisional description: apology and forgiveness requests, mixed with thanks
and religious expression. Documents examined: 277, 568 and 413.

1. Specific pattern: sorry and forgive alongside thank, family, peace, Lord,
God, Jesus and pain.
2. Documentary support: 277 combines explicit harm attribution, requests for
forgiveness, thanks to supporters and Christian expression; 568 apologizes
for grief the speaker caused, requests forgiveness, thanks others and invokes
Jesus; 413 combines explicit pain attribution with requests to families and
God for forgiveness, thanks and extended religious expression.
3. Contradictions and mixed content: all three serve multiple functions.
The component does not isolate harm acknowledgment, religion or gratitude.
The initially hesitant forgiveness language in 568 and 413 must be read
alongside their later requests, not coded from one clause alone. Mixed
language is not evidence of insincerity or private psychological state.

277 and 413 were already read under k6 topic 1. They are reused cross-model
examples, not new independent semantic validation. This demonstrates
interpretive continuity in these reference solutions, not added sample size.

k4 topic 1 has full-vector cosine approximately 0.869 with k6 topic 1 and
0.676 with k6 topic 5. The leading groups and examples support a broader
mixture at k4. These similarities are not proportions, and the relation
does not establish that fitting k6 causally split k4 topic 1. k6 topic 5
itself remains mixed. Greater granularity is not by itself better semantic
validity or a reason to declare a unique winning k.

## k4 topic 3 and k6 topic 3
Provisional description for both: denial, knowing/not-knowing and case-related
explanation language; retain the uncertainty mixture explicitly.
Documents examined under each reference fit: 367, 152 and 391. These are the
same three documents with different ordering, not six independent examples.

1. Specific pattern: not, did, know, did not, say and kill lead both sets.
2. Documentary support: 152 explicitly denies killing the listener's sister.
367 explicitly denies killing and also describes the speaker's execution as
murder; it includes separate negated predicates about walking and knowing.
391 repeatedly says the speaker does not know what to say and also says the
speaker did not know anybody was there. That latter clause may relate to
awareness of an event, but it is not an explicit denial of killing.
3. Contradictions and mixed content: similar negation/knowing vocabulary
co-occurs with different predicates, objects and communicative functions.
367 also includes affection, peace wishes and procedural readiness.
Do not infer actual innocence, a particular psychological state or absence
of case-related meaning from these readings. Neither component is an
innocence classifier.

Cross-k full-vector cosine is approximately 0.996. The same mixture and the
same three high-ranking documents recur. This supports lexical persistence
between these two reference fits, not independent semantic validation.
Increasing k from four to six did not resolve this particular observed
distinction. It does not establish that no possible k or representation can
resolve it. The previously inspected quoted-denial/admission example 499
remains supplementary development evidence, not a newly selected or unseen test.

A possible later research question is which information is lost when a
representation retains negation words but does not explicitly encode their
predicate, object, quotation attribution or scope. A new experiment and its
evaluation would require a separate plan; none is claimed by this reading.

## k4 topic 4 and k8 topic 4
Provisional description for both: scripture and formulaic prayer.
Documents examined under each fit: 352, 423 and 274 (different ordering at k8).
These were already read under k6 topic 4; they are three reused documents,
not nine independent examples.

1. Specific pattern: thy, heaven, kingdom, evil, shall and related words occur
among the leading groups across the reference fits.
2. Documentary support: all three contain overlapping extended prayer text.
352 also apologizes and acknowledges harm; 423 includes extensive affection;
274 is almost entirely prayer.
3. Contradictions and formulaic repetition: the component captures repeated
wording, while personal material in the same documents remains mixed. No
inference is made about private faith, sincerity or psychological comfort.
Positive coefficients and the eligible-document counts are not counts of
people reciting a particular prayer.

k4 topic 4 and k8 topic 4 have full-vector cosine approximately 0.989.
Combined with the earlier k6/k8 comparison (about 0.983), this supports
persistence of the lexical form across these reference fits, not all possible
initializations or independent semantic validation. Different eligibility
counts (199 at k4 and 180 at k8 under the display rule) must not be interpreted
as a change in religious prevalence; the documents have not changed.

The large k8 display group containing terms such as daily bread and bread
forgive is one group of identical full-corpus TF-IDF columns. Its members
are not independently recurring concepts. The vectorizer forms bigrams after
stopword filtering and does not enforce sentence boundaries; displayed
features such as thy earth must not automatically be quoted as literal
adjacent words in the source.

The higher coefficient for a document at k8 does not establish better fit to
its meaning or more faith: the component bases differ across fitted models.
The narrow wording-based description remains preferable to broad religion.

## k8, topic 1
Provisional description: apology and forgiveness requests with peace wishes.
Documents examined: 293, 414 and 433. All were already read under k6 topic 1.

1. Specific pattern: sorry, peace, hope, forgive, pain and caused.
2. Documentary support: 293 explicitly attributes family pain to the speaker;
433 also explicitly attributes pain to the speaker. 414 apologizes and seeks
forgiveness but does not specify comparable harm attribution. All contain
requests for forgiveness alongside other relational or religious language.
3. Contradictions and mixed content: requesting forgiveness and acknowledging
caused harm are distinct textual acts. 414's report of divine forgiveness
does not itself establish a specific harm admission. Isolated pray in 433
does not change its frozen F=u label.

The inspected k8 examples retain the earlier apology/harm distinction. This
is a boundary finding for these reused examples, not evidence that all
component documents were audited or that k8 offers no semantic improvement
anywhere.

## k8, topic 3
Provisional description: denial, knowing/not-knowing and case-related
explanation language, retaining the uncertainty mixture.
Documents examined: 152, 391 and 367; the same three were read at k4 and k6.

1. Specific pattern: not, did, did not, know, say and kill.
2. Documentary support: 152 explicitly denies killing; 367 denies killing
and separately objects to the execution; 391 repeatedly expresses not knowing
what to say and not knowing anybody was there. These are not interchangeable
propositions, despite shared vocabulary.
3. Contradictions and mixed content: 391's topic coefficient (about 0.4133)
is close to 152's (about 0.4135). This does not mean equal innocence, semantic
equivalence or an equally strong denial. The coefficient is not a calibrated
stance score. 367 also includes love, peace and closing language.

The same strong examples and semantic boundary persist across k4/6/8
reference solutions. Increased k did not resolve these particular cases.
This is not an independent test, a quantified model-wide error rate or a
claim that context-aware methods must succeed. The specific lost distinction
concerns the predicate and object of negation/knowing statements; a future
experiment would need its own target definition and evaluation design.

## k8, topic 2
Provisional description: expressed affection and relational messages.
Documents examined: 201, 399 and 445, the same three read for k6 topic 2.

1. Specific pattern: love, tell, family love, tell family and relational words.
2. Support: 201 addresses family and Kami with love and continued presence;
399 asks for love to be conveyed to family; 445 expresses love and separation.
3. Mixed content: 399 also encourages listeners to keep their head up; 445
also expresses readiness. The source's I live y'all wording is not silently
corrected. These are reused examples, not new independent validation.

## k8, topic 6
Provisional description: stay-strong encouragement with relational language.
Documents examined: 360, 428 and 236, the same three read for k6 topic 6.

1. Specific pattern: strong, stay strong and stay dominate the leading groups.
2. Support: all three explicitly urge recipients to stay strong alongside
love. 360 and 236 repeat the instruction; 428 also thanks supporters.
3. Mixed content and repetition: all contain affection. Repetition may
contribute to the lexical pattern but its causal role was not isolated.
No private psychological strength or effect on listeners is inferred.
The k6 zero-coefficient boundary cases are not assumed to have the same
coefficients at k8 without checking.

## Initial-coverage synthesis
| k | Observed descriptive structure | Limit |
|---|---|---|
| 4 | Broad apology/thanks/religious mixture; relational/encouragement mixture; case-related negation; repeated prayer | Broad lexical summaries do not isolate communicative functions |
| 6 | More explicit affection versus stay-strong distinction; apology versus mixed thanks/closing language | Zero coefficients can coexist with the named expression; mixtures remain |
| 8 | Additional reference components for Christian praise, procedural readiness and thanks/support | Finer names do not establish stable recovery or better semantic detection |

The same case-related examples remain mixed across k4/6/8; repeated prayer
persists across reference solutions; relational components retain overlap.
This supports k6 as an illustrative working summary, not a unique optimum
or validated semantic taxonomy. Numerical tradeoffs remain: k6 has the largest
random-pair lower quartile but a weak minimum; the k8 Christian component is
initialization-sensitive and readiness is short-text-removal-sensitive.

No semantic accuracy or human agreement statistic follows from this reading.
Most entries use three highest-ranked documents of at least 20 words; reused
documents are not independent samples. The planned three questions now have
provisional entries for every component. Broader interpretation remains limited
until lower-ranked/short-document coverage and owner adjudication are documented.
Frozen labels and the original protocol have not been retrospectively changed.

## Cross-k observations
Full-vector cosine between k6 topic 4 and k8 topic 4 is about 0.983, supporting
lexical similarity of these two reference components, not semantic equivalence
or stability under every initialization.

k6 topic 5 corresponds most closely to k8 topic 8 (0.862), with additional
similarity to k8 topic 5 (0.519) and k8 topic 7 (0.407). This motivates reading
the latter components to investigate finer distinctions. It does not prove
that fitting k8 causally split a single k6 component: these are separately
fitted models, and similarities are neither probabilities nor additive shares.

## Next actions
Initial leading-example coverage is complete. Preserve the bounded synthesis
rather than presenting it as exhaustive validation. Remaining boundary checks
and owner adjudication are still open.

Before adding a method, define one semantic distinction. An audit-informed
candidate is whether case-related lexical similarity distinguishes the
speaker's explicit denial or admission of killing from quoted statements and
knowing/not-knowing language. Prior examples are development material.
Check literature and define the unit, target, ambiguity policy and independent
evaluation before a comparative experiment. Novelty and improvement have not
been established.
