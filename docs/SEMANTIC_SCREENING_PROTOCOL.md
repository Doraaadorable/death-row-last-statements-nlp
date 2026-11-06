# Candidate screening for the semantic interpretation study
Date: 2026-11-06
Status: feasibility screening informed by prior examples; not model evaluation

## Inputs and unit
Use all 479 prepared documents marked ready_for_exploration in the frozen
model_corpus_v1.csv, not only the 477 documents retained by TF-IDF.
A zero-feature document is not necessarily irrelevant to a new semantic task.
Preserve every prepared text, source URL and execution ID. Exclude only the
already recorded wholly indirect summary in this screening version.

## Approved pilot decisions
The owner confirmed all four pilot interpretations after AI-assisted discussion.
Record them separately as development decisions, not independent blind labels.
Keep the original worksheet and frozen eight-label annotations unchanged.

## Screening rules fixed before this screen's counts
Patterns operate directly on prepared text with case-insensitive matching.
Offsets, where recorded, refer to that exact text; no stopwords are removed.

- action_or_innocence_cue: kill/kills/killed/killing, murder/murders/murdered/
  murdering, innocent/innocence, or did-not/didn't/never/not followed by do/commit.
- negated_knowledge_cue: selected forms of not knowing/understanding, including
  didn't know, don't know, never knew and unaware.
- reporting_or_saying_cue: say/says/said/saying, tell/tells/told, claim variants,
  believe variants and according to.
- candidate_document: action_or_innocence_cue OR negated_knowledge_cue.
  The reporting cue stratifies candidates; by itself it does not select one.

The executable regexes are recorded in notebook 06. Generic saying cues do not
identify attribution to other people. Killing cues can refer to execution,
religion, other actors or unrelated material. No cue assigns a semantic label.

## Outputs and interpretation
Report input/exclusion counts, cue counts, intersections, mutually exclusive
cue combinations, candidates and nonmatches. Save a separate ignored screening
table and pattern/input manifest. Do not display new full texts or sample
documents in this first screen. Do not split training/test data or fit models.

Candidate counts establish retrieval workload, not numbers of authentic
denials/admissions/attributed claims, class balance or minimum sample adequacy.
Nonmatches can contain target claims (e.g. indirect references and paraphrases).
Both hits and nonhits will need a separately specified review sample before
retrieval coverage or accuracy can be assessed. Previously seen pilot cases
are included in counts but are not new evidence.

## Next decision
Use counts to choose a bounded development review across cue combinations,
including nonhits. Define its sampling rule before opening new examples.
Only after reviewing authenticity and guideline consistency decide whether a
larger annotation or task-matched model comparison is warranted.
