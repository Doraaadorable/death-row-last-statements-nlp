# Current research plan

Updated 8 November 2026.

## Research question
How do people facing execution express emotions, maintain relationships, and
make sense of death and their own situation in their final statements?

The study examines psychological expression through complete texts. Its
starting interests include emotion, relationships, responsibility, faith and
understandings of death. Religious care, perceived judicial severity and
death-penalty policy are contextual interests; they do not replace the focus
on psychological expression. The completed reading set supports contextual
comparison, while causal effects require a separate design.

## Existing materials
- 480 candidate documents, with 479 prepared texts.
- A frozen 50-person development sample, ten per decade, coded for eight
  nonexclusive forms of expression. Keep the original 1/0/u values.
- NMF results and component readings to help locate recurring language.
- Predicate/source/negation experiments as supporting methods.
- [Six-case pilot notes](../reports/psychological_expression_pilot_v1.json).

## Current progress
The [exploratory report](PSYCHOLOGICAL_EXPRESSION_REPORT.md) synthesizes the
20-case reading. The workbook now includes evidence anchors, contextual memos
and alternative readings for all 20 statements. All 20 have now been discussed
with the owner. Memos incorporate revised readings, including the withdrawn
sarcasm interpretation for 524 and unresolved referents in 138 and 433.

The [full-text literature comparison](LITERATURE_COMPARISON.md) now includes the
supplied Eaton & Theuer and Zhuo & Chun articles. It confirms substantial overlap,
including religious admonition during forgiveness and two shared source cases.
The broader check also located Smith (2019), directly concerning forgiveness
direction and religious framing; its supplied full text has now been checked, including the contextual coding
rule and relevant examples.
No additional owner annotation is needed at this point.

## Completed focused comparison
Within the overall question, ask: How do people facing execution use requests
for, and declarations of, forgiveness to express self-reproach, sustain
relationships and negotiate responsibility?

Chinese: 面对执行时，人们如何通过请求或给予宽恕，表达自责、维系关系并协商责任？

The report now compares discussed cases 413, 407, 600, 461, 595 and 508 on
worthiness, family connection, request conditions, forgiveness direction and
responsibility. These are comparison questions rather than new
labels. Retain the brief and differently oriented texts as boundary cases.

This is a literature-grounded extension; a new gap has not been established.
The focused account is complete within the existing report. Its central
interpretation is that attempting relational repair does not establish achieved
reconciliation. This exploratory version needs no new model, sample or repeat
owner review. Broader searching and a stated case-selection rationale would
precede any new empirical expansion.

## Reproducible descriptive context
The report now includes raw 1/0/u counts for all eight frozen categories in the
50-person development sample, and selected co-presence counts. All 28 label
pairs and supporting IDs are saved in
[the descriptive summary](../reports/expression_sample_descriptive_v1.json).
Run `python src/summarize_expression_sample.py` after extracting the snapshot.
These summaries describe the old development coding, not population rates or
independent confirmation of the reading comparisons.

## Institutional-context extension
The report now compares religious care and meaning, interpretations of punishment,
and policy context using the existing discussed cases. Its three levels are:

1. **Expressed experience:** what feelings, relationships and understandings the
   speaker explicitly describes. This is the current study.
2. **Institutional exposure:** the care, confinement, procedures or policy actually
   experienced. These need dated external records, not inference from prayer.
3. **Effects of change:** what would differ with another policy or support regime.
   These need comparable groups/outcomes and an identification strategy.

The current Texas execution corpus does not contain an abolition-regime control
group. Decade comparisons alone cannot estimate the effect of abolition. Retention,
suspension, commutation and procedural reform must be distinguished.

## Completed feasibility check
The report now checks two dated religious-accommodation milestones in official
court documents and counts the saved material around them. There are 450
candidate texts before 21 April 2021, two until 23 March 2022, and 28 on/after
24 March 2022. These are calendar availability groups, not verified care
exposure or psychological-outcome groups.

The prioritized extension is a contextual documentary case study of spiritual
support. It requires a dated request/decision, actual provision or an explicit
unknown, and attributable personal material. A first purposive case, John Henry Ramirez (#576), now links a legal
request, reported provision, an attributed pre-execution interview and the final
statement. It documents anticipated significance, not psychological effectiveness. Direct causal estimates of support, stays,
commutation or abolition remain deferred pending suitable evidence.

Reproduce the availability check with
`python src/check_institutional_feasibility.py`; the saved result is
[here](../reports/institutional_feasibility_v1.json).

## Next-stage decision before selecting new cases
Keep the current psychological-expression study and its focused forgiveness
comparison. The first availability check favors spiritual accommodation as a bounded
documentary context. The first case shows that documented spiritual support may be absent from the
religious vocabulary of a final statement. Next seek one contrasting arrangement
with an attributable account, rather than generalizing from this example.
Do not treat the calendar groups as a causal comparison.

Do not add a broad psychological codebook or reopen the completed 20-case
review. No new owner annotation is requested for this framework update.

## Useful distinctions
- A self-description of peace differs from wishing peace for someone else.
- Affection, gratitude and spiritual language differ from acceptance of death.
- Farewell, closing a statement and permission to begin are different speech acts.
- Accepting responsibility can coexist with criticism of execution.
- An editorial note such as crying differs from a speaker's emotional self-report.

These distinctions guide interpretation without presupposing conflict or a
particular psychological explanation. Record ambiguity in context.

## Literature comparison
| Study | Material and measurement | Reading status |
| --- | --- | --- |
| Schuck & Ward (2008) | 283 statements; sequential structure and self-presentation | Author-uploaded text located; relevant methods, analysis and appendix sections read |
| Hirschmuller & Egloff (2016) | 407 statements; LIWC emotional-word proportions | Selected full-text methods/results read |
| Goranson et al. (2017) | Actual and imagined last words, poetry, LIWC and affect ratings | Selected full-text sections read |
| Foley & Kelly (2018) | Themes including love, spirituality and forgiveness | Abstract reviewed |
| Mehra et al. (2024) | 466 statements; embedding-weighted emotion signals, category mapping, co-occurrence and notion transitions | Selected full-text methods/results read |
| Smith (2019) | Forgiveness direction and religious framing | Supplied full text read; contextual coding rule, denominator and examples checked |
| Eaton & Theuer (2009) | Apology and remorse-related content | Supplied full text read; definitions, denominators and reliability checked |
| Zhuo & Chun (2026) | 198 statements; title specifies White American inmates; emotion and moral positioning | Supplied full text read; scope, coding and close examples checked |

References:
- https://doi.org/10.1007/s13644-019-00385-y
- https://doi.org/10.1177/0957926507083687
- https://doi.org/10.3389/fpsyg.2015.01985
- https://doi.org/10.1177/0956797617701186
- https://doi.org/10.1093/qjmed/hcy062
- https://doi.org/10.3389/fcomp.2024.1463692
- https://doi.org/10.1080/07418820802245078
- https://doi.org/10.1177/00302228261437890

Compare definitions, samples, analytic units and interpretation before comparing
findings. Word proportions and dominant-emotion categories measure different
things. Co-occurrence, sequencing and self-presentation already appear in earlier work.
The full-text comparison confirms a contextual extension rather than a new
field-wide gap. The focused forgiveness comparison will remain explicit about
prior coverage and overlapping examples.

## Scope of conclusions
The documents support analysis of expressed feelings and meaning making.
They provide one public statement per person; private experience and change
over time remain outside this dataset. Availability of statements, audience,
translation and institutional context shape the material. Quantitative summaries
will use document-level denominators and retain unresolved readings.

## Institutional contrast checked: Murphy (2019)
The report now contrasts Ramirez's request for pastoral touch with counsel's
record of Murphy's preference against touch at death. Murphy's scheduled
executions were stayed; he is not an executed control without support. This
contrast supports examining the fit between arrangements and individual
preferences. It does not establish a psychological effect. A located interview
audio remains unchecked, so Murphy is an institutional boundary case rather
than a completed personal-experience case. Next check that interview if it can
be obtained; otherwise retain the experience gap. No new owner labeling round
is requested.
