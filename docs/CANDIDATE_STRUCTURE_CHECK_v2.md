# Local candidate-construction check v2

## Implementation
focus_candidates_v2.py adds local construction flags to the unchanged v1 literal
inventory. It is a candidate-preparation prototype, not a dependency parser or
complete implementation of the human predicate inventory. Every original
match is retained. Auxiliary merges propose an exact lexical-head interval;
other flagged matches are deferred, not silently removed or semantically
relabelled. B2, the original adapter and smoke results are unchanged.

Seven behavioral tests passed. They check exact auxiliary/head offsets,
preservation of lexical did, separate take arguments, a passive-life pattern,
nominal flags, preservation of ellipsis and original offsets/case.
These fixtures were informed by known development material, not held out.

## Applied to the fixed smoke batch
All 92 source matches were cross-referenced at their original offsets:

| Disposition | Matches |
| --- | ---: |
| No local construction flag | 72 |
| Proposed auxiliary/head merge | 6 |
| Life attachment not established | 7 |
| Possible nominal use | 2 |
| Multiword interpretation needed | 2 |
| Ellipsis interpretation needed | 3 |

The 72 unflagged matches are not verified correct, independent predicates or
in-scope propositions. The seven life-attachment flags include ordinary uses
of take unrelated to life; they are not seven false positives in killing
classification. Automatic ellipsis flags can also overflag lexical do.

Among the historical 30 abstentions, six get merge proposals, one gets a life
attachment flag, two nominal flags, two multiword flags, three ellipsis flags,
and 16 no local flag. This does not mean 14 abstentions have been solved: no
new semantic predictions or reference labels were produced.

## Deliberate limits
The auxiliary-head pattern requires adjacency apart from not/really/personally.
It therefore misses questions such as Did Roger come with an intervening
subject. That explains why it flags six of the seven auxiliary observations
from qualitative triage. It does not infer long-distance syntax, pronoun
antecedents, reporting ownership, mood or complete nominal/copular inventories.
The local life-object pattern does not resolve arbitrary argument attachment.

The earlier reporting-frame issue remains in B2. A reliable improvement should
separate candidate construction from source/negation interpretation, rather
than treating these structural flags as corrected five-field labels.

## Reproduce
Run:

```bash
python -m unittest discover -s tests -p test_focus_candidates_v2.py
python src/run_candidate_structure_check_v2.py
```

The report contains original B2 predictions only for traceability and labels
them historical. Input/code hashes and all exact offsets are preserved.
Re-running refuses to overwrite a changed report. No new documents were drawn.
Next work should compare a syntactic candidate inventory against a documented
reference inventory; this local check alone cannot measure extraction recall
or demonstrate improved semantic accuracy.
