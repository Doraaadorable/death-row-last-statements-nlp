# Development review sample after cue screening
Date: 2026-11-06
Status: audit-informed development sampling, not an independent evaluation set

## Known information
The fixed screen has 479 documents, 128 candidates and 351 nonmatches.
The seven nonempty cue combinations and their sizes have been seen.
No newly sampled full texts have been read for this sampling step.

## Selection rule
- Use the unchanged cue-screen table and frozen corpus hash.
- Exclude executions 117, 391 and 499, which supplied the four confirmed pilot
  spans. Other previously read material may still be selected.
- Within each nonempty action/knowledge/reporting combination, sort by numeric
  execution ID and sample up to three documents without replacement.
- Use one NumPy default_rng initialized with seed 20261106, processing
  combination strings in sorted order. No redraw for interestingness.
- This should produce 21 documents: 15 cue candidates and six nonmatches,
  subject to the stated eligible group sizes. Verify rather than silently
  assuming those totals.
- Display candidate combinations before nonmatches, then combination and
  execution ID. Display order does not alter selection.
- Mark membership in the old 50-record annotation set as known prior exposure.
  All other exposure is not established, never declared unseen by default.

## Purpose and manual procedure
The goal is to assess whether the four-field claim scheme transfers beyond the
original examples and whether literal retrieval misses paraphrases.
Do not infer class counts, precision, recall or population prevalence from
the cue groups or from this small development review.

For each document, read the complete prepared context before selecting a
possible clause. Record a short exact evidence span if useful, a review note
and reviewed/pending status. Blank fields mean pending. A reviewed document
without a useful target span is a valid observation, not a reason to replace
the sample. A candidate can contain only execution-policy or religious wording;
a nonmatch can contain an indirect admission. Contextual ambiguity stays
unresolved rather than being forced into a label.

Only after reviewing the selected spans should the source/type/actor/polarity
fields be applied under a documented guideline version. These review notes
are not the frozen v2 labels and do not overwrite them.

## Source and output checks
Match every prepared text and ID to the frozen corpus, verify cue table and
module hashes against notebook 06's screening manifest, retain original
selection metadata, and never overwrite an edited worksheet.
Save an immutable selected source table separately from a working review
worksheet. Reruns must preserve existing notes and verify their source fields.

## What this cannot establish
This is not blind annotation: the sample was designed after prior analyses and
the cue rules were designed around known failures. It is not a held-out test,
and the six nonmatches cannot establish retrieval completeness. No
classifier, language-model call, synthetic augmentation or performance claim
is authorized by executing this sampling notebook alone.
