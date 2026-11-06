# Component interpretation review: k=4/6/8

## Status and evidence
Partial working record, prepared from the owner's executed notebook output and
subsequent reading discussions. Interpretations are provisional and AI-assisted;
this is not independent blind coding or a completed owner-adjudicated review.
Frozen eight-label annotations and all model outputs are unchanged.

The planned review covers 18 components. Evidence entries have been started for
four: k6 topics 1, 4, 5 and k8 topic 5. No component is declared fully reviewed.
The other 14 components remain pending this uniform review.

## Reading procedure and limits
Notebook 04 ranks positive coefficients, restricts displayed examples to at
least 20 words and breaks coefficient ties by execution number.
For k6 topic 1, displayed ranks 1-6 and 151-153 were read (offsets 0, 3 and 150).
For the other three entries, only ranks 1-3 were read. These are purposive
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
Read k8 topics 8 and 7 using the same questions, then check lower-ranked and
short examples. Continue to the other components, including every k4 component.
Do not mark the protocol's interpretation stage complete until every component
has an evidence entry and the remaining boundary checks are documented.
