# Deep-dive plan

## Research direction
Investigate when a stable lexical component supports a defensible interpretation,
and when wording, quotation, negation or religious/cultural context makes that
interpretation ambiguous. This follows the existing protocol; it does not
assume that another model or a larger k will solve the problem.

This plan is informed by all previous analyses. It is not an independent
preregistration or a claim of novelty. No psychological state or guilt inference
is intended.

## Stage 1: complete the planned uniform component review
Use notebooks/04_component_interpretation.ipynb. It reads saved numerical
references and coefficients; it does not refit models or write labels.
Review all 18 components across k=4/6/8 using the same three protocol questions:
specific linguistic pattern, documentary support, and contradictions/formulas.
Record narrow provisional descriptions, execution IDs and evidence quotations.
Leave mixed or unresolved components explicitly mixed or unresolved.

The first display uses three highest positive-coefficient documents with at
least 20 words. This is a display rule only and favors strong examples. Inspect
lower-ranked and short documents before completing a component review.
Cross-k heatmaps report lexical cosine without forcing one-to-one matching;
they cannot prove semantic equivalence or split/merge causation.

Start with k=6 components 1 and 4 to examine distinctions already raised in the
audit: apology versus harm acknowledgment, and repeated prayer versus broad
faith. Known examples remain development evidence. Complete the remaining
components and k=4/8 comparisons before recording interpretive completion.
Preparing or executing the notebook alone does not complete the human review.

Deliverable: docs/COMPONENT_REVIEW_k4_k6_k8.md with an evidence-based entry for
each component, followed by a bounded explanation of whether any k is more
useful for the stated research purpose. No unique winner is an acceptable result.

## Stage 2: formulate one semantic interpretation question
Use the review to select a concrete failure mode rather than expanding every
possible direction. Candidate distinctions include speaker versus quoted
speech, apology versus sympathy, and formulaic prayer versus broader religious
expression. Cultural context can inform a reading but is not evidence of the
speaker's private intention.

Before comparing a new method, document the intended target, textual unit,
inclusion rules, uncertainty handling and success criteria. Check existing
literature before claiming that the question is new. Do not infer prevalence
or independent performance from the 50 development records.
If revisiting past decisions, mark new rationales as retrospective rather than
inventing contemporaneous annotation history.

Deliverable: one focused research question and an evaluation design, chosen
after Stage 1. No new method is selected in this plan.

## Stage 3: decide whether new data or methods are justified
If the goal is descriptive interpretation, a documented qualitative analysis
may be sufficient. If the goal becomes generalizable prediction or comparing
semantic models, obtain suitable independent annotation and freeze an evaluation
set before tuning. Previously viewed documents cannot be called unseen evidence.
Preserve the current v2 labels and outputs; changed guidelines or features need
a separately documented version.

Do not automatically add embeddings, classifiers, bootstrap, more k values or
another 50 annotations. Each addition must answer the focused question and have
an evaluation that can support the intended claim.

## Current execution evidence
The four code-cell bodies of notebook 04 were executed in-process against the
curated inputs, with a noninteractive plotting backend, and input dimensions
and the 18-component overview were checked. This is not a separate Jupyter
kernel run. The notebook is supplied without stored outputs; the owner will
execute it in the project environment.
