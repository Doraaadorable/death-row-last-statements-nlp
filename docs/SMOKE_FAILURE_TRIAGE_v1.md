# Smoke-output triage v1

## What was inspected
All 30 B2 abstentions from the fixed 20-document smoke batch, plus the three
zero-focus documents. This is AI qualitative inspection after seeing outputs,
not owner-confirmed reference annotation, independent validation or an error
rate. No claim is made that the other 62 predictions are correct. B2 and its
literal-focus adapter remain unchanged.

Original reason codes: 23 unresolved action/responsibility; six uncovered
agent/construction; one possible reporting frame. These codes are execution
paths, not proof of the linguistic cause or actual ambiguity.

## Proposed primary triage
| Observed mechanism | Records | Interpretation |
| --- | ---: | --- |
| Auxiliary selected separately | 7 | did/do is separated from commit, murder, know or come |
| Ellipsis | 2 | Yes I do; I know he does require reconstruction and scope checking |
| Nominal action word | 2 | more killing and family's murders are not independent verb foci |
| Nearby life token crosses predicate | 1 | take the power is contaminated by nearby take a life |
| Self-speech frame | 1 | I would like to say ... I did not murder triggers the broad reporting guard |
| Multiword expression | 2 | nothing to do with and do away with are not resolved |
| Procedural do expressions | 6 | execution/permission context requires a scope decision before target classification |
| Remaining reference, agency or mood limitation | 9 | generic acts, unspecified actions/events or exhortation need interpretation |
| Total | 30 | Primary categories assigned once per abstention |

Categories are mutually exclusive only for bookkeeping. Multiple mechanisms
can affect the same sentence. Exact ID/offset cross-references and original
reason codes are in reports/smoke_failure_triage_v1.json.

### Important examples
- Execution 372: the first I did not murder your son abstains because the
  prefix contains the speaker's own I would like to say. That framing alone
  does not attribute the denial to somebody else. A later denial in the same
  document is predicted denial. This illustrates context-window sensitivity;
  neither prediction is silently corrected in the saved output.
- Execution 211: take a life and take the power occur close together. The
  life-action window contaminates the second selected take. Argument attachment
  should be checked before using a nearby noun to establish killing content.
- Execution 378: does in I know he does is an elliptical/pro-verb use. It is
  not automatically an invalid predicate or an independent killing action.
  An earlier conversational suggestion that it was simply a bad extraction is
  too strong. Preserve the occurrence and resolve its content/scope or defer it.
- Execution 273: family's murders is nominal, while I'm innocent is missed by
  the literal predicate adapter. Absence from adapter output does not establish
  absence of relevant content. The available fields do not supply an exhaustive
  reference inventory, so this is not a measured extraction-recall result.

## Zero-focus documents
- 108: a religious message about saving innocent ones. Innocent here is not
  automatically a personal legal innocence claim.
- 216: crucified with Christ is religious/figurative language not covered by
  the literal inventory. Record the scope question; do not invent a literal
  personal killing claim.
- 409: biblical comfort and closure language. No literal focus was retrieved;
  this is not evidence of complete extraction.

## Decision for further work
The next experiment should address predicate units and argument attachment
before adding more killing keywords. Keep two stages distinct:
1. Candidate construction: identify lexical heads, attached auxiliaries,
   complements, ellipsis and nominal/copular predicates; record offsets and
   scope decisions, including missed candidates.
2. Interpretation: identify actor, attributed source, negation and presentation
   status relative to each selected predicate. Keep uncertainty visible.

Use this batch for development diagnostics only. Any revised extractor or
classifier gets a new version; do not describe an improved fit to these known
cases as held-out improvement. A complete predicate inventory is needed before
measuring extraction, and fresh references before evaluating classification.
This triage adds no new owner-review requirement and makes no semantic-label
changes.

## Reproduction
Run `python src/audit_smoke_failures_v1.py`. It validates one-to-one coverage of
the original 30 abstentions and the three zero-focus document IDs, records input
hashes and refuses to overwrite a changed report. Its manually supplied
crosswalk is explicit; it is not an automatic linguistic diagnosis engine.
