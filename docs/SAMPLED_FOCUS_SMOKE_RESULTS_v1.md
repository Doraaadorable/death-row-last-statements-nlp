# Sampled focus smoke test v1: results

The owner requested a draw followed by immediate existing-rule testing. Protocol
and adapter were committed at 35824af8df54bd64a3f7428f9029ac4b6d58dcaf before
the draw. B2 is unchanged. No independent references were collected.

| Old cue stratum | Documents | Literal foci | Other | Abstain | Denial | Admission | Documents with zero foci |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Candidate | 10 | 64 | 39 | 23 | 2 | 0 | 1 |
| Nonmatch | 10 | 28 | 20 | 7 | 0 | 1 | 2 |
| Total | 20 | 92 | 59 | 30 | 2 | 1 | 3 |

All counts are automated predictions on literal matches, not adjudicated claims.
Broad know/say/did matches include out-of-scope and auxiliary uses. Zero matches
do not mean no eligible proposition. Results cannot establish precision, recall,
accuracy, semantic coverage or corpus prevalence.

The two denial predictions are at execution 229's kill and execution 372's
murder. The admission prediction is execution 378's took, in I took his life.
Execution 378 came from the old screen's nonmatch pool: explicit life-taking
wording can escape its limited kill/murder/innocence/negated-knowledge cues.
This is a retrieval limitation illustrated by one observed case, not a recall
estimate or a reason to retune the screen on this batch.

All 92 focus intervals were checked against source substrings. Running the
script twice reproduced the saved result. Notebook 15's three code-cell bodies
were executed in-process; this is not evidence of a separate Jupyter-kernel run.
The committed notebook has no saved outputs and reads the local frozen corpus.

Use notebooks/15_sampled_focus_smoke.ipynb to inspect full context and outputs;
the initial view displays execution 378. This is deliberately unblinded. The
sample is now smoke/development material, not the reserved blind-reference
batch. Add all 20 IDs to future exposure exclusions. Historical corpus, labels,
B0/B1/B2 code and earlier diagnostic results were not changed by this run.
