# Sampled B2 smoke test v1: protocol before draw

The owner requested sampling and testing with existing rules rather than first
preparing prediction-blind manual references. Use the existing frozen 20-document
sampling procedure (seed 20261107; candidate first, nonmatch second, ten each).
Validate readiness source hashes. Do not redraw or select favorable examples.

B2 focus_rules_v1.py is unchanged. It cannot classify a document without a
selected predicate. Supply candidates through a separate, fixed literal regex
inventory in run_sampled_focus_smoke_v1.py, declared before drawing IDs. This
adapter is deliberately not a syntactic parser: auxiliary did/do and broad
say/know tokens can be returned, and unlisted paraphrases can be missed. It
does not implement the manual scope protocol, infer complete propositions, or
confirm that each focus is a lexical predicate. Its outputs are literal-focus
predictions, not document-level labels, extracted claims or reference labels.

Return every match in source order, exact character offsets, predicted class,
reason and document-level zero-match counts. Supply complete context to B2,
which uses its documented bounded windows. No target labels or document IDs
are passed to B2. Do not tune B2 or the adapter after inspecting this batch.

Keep all 20 IDs and their source hashes. Export prediction counts by stratum;
do not compute accuracy/precision/recall, infer corpus prevalence, or compare
these counts with the 32 manually selected development units as improvement.
Automatically reading these documents changes their workflow use: this is
smoke-test material, no longer the reserved prediction-blind reference batch.
Owner recognition remains unknown until explicitly reported. Future exposure
ledgers must also exclude these 20 IDs from any fresh blind sampling pool.

Provide a notebook to inspect complete prepared context alongside focus-level
predictions. This view is deliberately unblinded and creates no reference
labels. Source corpus, old labels and historical results remain unchanged.
