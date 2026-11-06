# Component interpretation review: k=4/6/8

## Status and evidence
Partial working record, prepared from the owner's executed notebook output and
subsequent reading discussions. Interpretations are provisional and AI-assisted;
this is not independent blind coding or a completed owner-adjudicated review.
Frozen eight-label annotations and all model outputs are unchanged.

The planned review covers 18 components. Evidence entries have been started for
six: k6 topics 1, 4, 5 and k8 topics 5, 7, 8. No component is declared fully reviewed.
The other 12 components remain pending this uniform review.

## Reading procedure and limits
Notebook 04 ranks positive coefficients, restricts displayed examples to at
least 20 words and breaks coefficient ties by execution number.
For k6 topic 1, displayed ranks 1-6 and 151-153 were read (offsets 0, 3 and 150).
For the other five entries, only ranks 1-3 were read. These are purposive
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

## Cross-k observations
Full-vector cosine between k6 topic 4 and k8 topic 4 is about 0.983, supporting
lexical similarity of these two reference components, not semantic equivalence
or stability under every initialization.

k6 topic 5 corresponds most closely to k8 topic 8 (0.862), with additional
similarity to k8 topic 5 (0.519) and k8 topic 7 (0.407). This motivates reading
the latter components to investigate finer distinctions. It does not prove
that fitting k8 causally split a single k6 component: these are separately
fitted models, and similarities are neither probabilities nor additive shares.

## Next review actions
The initial k8 topic-7 short-text diagnostic is now recorded. Continue with
k6 topics 2 and 6, then the remaining components, including every k4 component.
Lower-ranked and short-text checks for the other entries remain pending.
Do not mark the protocol's interpretation stage complete until every component
has an evidence entry and the remaining boundary checks are documented.
