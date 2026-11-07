# Owner-confirmed predicate layers: execution 287

## New confirmed selections
The owner separately accepted the know and think propositions after a guided
explanation. See reports/semantic_owner_additions_287_focus.csv for exact
evidence/focus offsets and context hashes. Both rows retain the full frame
I know you think I did this. Exact historical message times are not recorded.

| Focus | Selected proposition | Source | Type | Actor | Polarity | Status |
|---|---|---|---|---|---|---|
| know | Speaker knows the listener's belief | self | knowledge | self | affirmed | presented_as_true |
| think | Listener holds the embedded belief, as described by speaker | self | other | other | affirmed | presented_as_true |
| did | Speaker did this, attributed to listener | other | wrongdoing_unspecified | self | affirmed | presented_as_true |

The did row was already confirmed as v3-dev21-020. It is not duplicated as
a new addition. Think is a belief-state contrast under the existing operational
event types, not silently redefined as epistemic knowledge.

Different source values reflect different selected propositions. The narrator
claims knowledge or attributes a belief state; the embedded action content is
attributed to the listener. Neither the listener's actual belief nor the
narrator's actual knowledge is independently verified.

## Version boundaries
There are now 39 confirmed selected development propositions: the preserved
37-record discussion file plus two additions. This does not establish complete
predicate annotation of all 21 statements. Manual focus itself is not an
independent reference or automatically extracted feature.

Notebook 11 and the published diagnostic v1 still intentionally use 37 rows.
Their result counts are historical, not silently recalculated on 39 rows.
Existing local owner worksheets and source files have not been overwritten.
A later versioned integration must preserve IDs and distinguish evidence spans
from focus spans. The fact that two rows share evidence does not make their
selected propositions identical. All layers from one execution must remain in
the same future development/evaluation partition.

## Next implementation requirement
Before any focus-assisted comparison, declare whether focus is supplied by a
human or identified automatically, give methods comparable inputs and retain
full negation/reporting context. Do not infer an action source simply from the
focus token. The original four-example focus inventory remains a draft outside
these two explicitly confirmed additions.
