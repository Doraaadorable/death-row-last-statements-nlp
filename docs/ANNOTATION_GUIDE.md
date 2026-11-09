# Annotation Guide — Frozen v2

Approved and frozen: 5 November 2026.

This repository text edition preserves the definitions and boundaries of the approved English v2 guide. It does not revise the frozen labels. The eight coding categories are separate from the latent NMF topics.

## Coding values

| Value | Meaning |
|---|---|
| `1` | Sufficient textual evidence meets the definition. |
| `0` | No qualifying expression is present; this does not establish the absence of a feeling or belief. |
| `u` | Relevant evidence is present, but its meaning or classification is unresolved. |

These are non-exclusive categories, not scores to sum. Retain `u`; do not automatically convert it to `0`.

## General rules

- **Scope.** Code expressed language, not sincerity, personality, remorse, mental health or actual guilt. Values are non-exclusive categories, not scores to sum.
- **Evidence.** Use the English statement as a whole, including clear references. No fixed keyword is required. Do not fill gaps with case facts or assumed intentions.
- **Uncertainty.** Use u for a specific textual or semantic ambiguity, not simply because the speaker's inner state is unknowable or a cultural phrase is unfamiliar.
- **Speaker and quotations.** Exclude third-party replies and editorial descriptions from speaker evidence. Religious quotations can establish religious content without establishing personal experiences or motives.
- **Review.** Keep independent judgments before discussion. Review after seeing existing labels is non-blind review; agreement does not verify the speaker's intention.
- **Revision and modeling.** Recheck comparable records whenever a definition changes. Keep uncertainty rather than converting u to 0. Split data by person; these 50 records are guideline-development data, not an independent test set.
- **Approval and version control.** I approved all v2 decisions on 5 November 2026. The register is frozen for this version; u retains semantic uncertainty. Future changes require a new version and review of comparable records.

## Label definitions

### A | Relational affection

Column: `relational_affection`

Explicit love, closeness, concern within a relationship, caregiving wishes, or valuing a relationship and sustained companionship.

**Include.** Direct expressions of love or missing someone; instructions to care for loved ones. Thanks for sustained companionship may support both A and G.

**Do not infer.** Merely mentioning family, receiving love, or offering routine thanks does not automatically qualify. Kinship is not required: the addressee may be a friend, fellow believer or another person.

**Boundary.** Use the narrower relational reading: generic well-wishes or encouragement alone do not establish A. Explicit relational concern, caregiving, affection, or valuing sustained companionship is required; ambiguous support language may remain u.

### G | Gratitude

Column: `gratitude`

Explicit thanks or appreciation directed to a person, group, institution or deity.

**Include.** Thank you, I appreciate, and equivalent direct expressions qualify. Routine courtesy thanks count under this definition.

**Do not infer.** Good treatment, love, praise or support received do not independently establish gratitude. Possible sarcasm in one sentence does not automatically negate every expression of thanks in the statement.

**Boundary.** Thankfulness and affection are distinct, although both may occur together.

### F | Faith and spirituality

Column: `faith_spirituality`

Explicit religious or spiritual references, beliefs, blessings, practices or texts.

**Include.** Clear references to God, Allah, Jesus, religious prayer, scripture or an explicitly religious afterlife qualify. Religious quotations establish content, not the speaker's devotion or motive.

**Do not infer.** Home, peace, a beautiful place, golden child, and similar expressions do not independently establish religion. No religious label is inferred solely from the execution setting.

**Boundary.** Standalone pray is u when prayer and a secular wish are both plausible. Multiple contextual cues may leave an unresolved religious reading, as in #330; vague imagery alone need not be u.

### P | Apology and forgiveness

Column: `apology_forgiveness`

An explicit apology, request for forgiveness, forgiveness of others, or clear advocacy of forgiveness.

**Include.** I apologize, forgive me, and I forgive them qualify. A clear wish that others forgive can qualify even if the recipient or direction is not fully specified.

**Do not infer.** Acknowledging personal responsibility or harm is not required for P. Clear sympathy or regret alone is 0; sorry is interpreted pragmatically, not by grammatical form alone.

**Boundary.** Where apology and sympathy cannot be distinguished from context, use u. Do not require I caused before coding an apology as 1.

### H | Acknowledgment of causing harm

Column: `harm_acknowledgment`

Explicit acknowledgment that the speaker's actions or omissions caused another person or group harm, pain, trouble or loss.

**Include.** Both self-attribution and a negative consequence must be established, including through clear contextual references. The affected party may be a victim, the speaker's family or friends, or another group; the harm need not be the charged crime.

**Do not infer.** An apology, acceptance of punishment, general acceptance of responsibility, or religious sinner identity does not automatically qualify. Failure to be present is not automatically acknowledgment of harm.

**Boundary.** Uncertain causal links or possible consequences warrant u. No specific phrase such as I caused is required. Degree of understatement does not determine the label.

### I | Innocence or culpability dispute

Column: `innocence_dispute`

An explicit denial or dispute of the speaker's involvement, intent or culpability in the case.

**Include.** Complete innocence claims and narrower denials of intent or culpability qualify. Not murder, an accident can qualify even while the speaker acknowledges causation or accepts responsibility.

**Do not infer.** Opposing execution, not remembering events, or saying God knows the truth alone does not qualify. Criticism of testimony or evidence does not automatically establish a dispute about the speaker's own culpability.

**Boundary.** Use u if the link between a challenged court statement and personal culpability is unclear. Report I=1 as innocence or culpability dispute, not necessarily a claim of complete innocence.

### J | Criticism of the justice process

Column: `justice_criticism`

Explicit criticism of a trial, judicial actor, evidence or testimony in the case, legal process, judicial outcome, sentence or execution.

**Include.** Allegations of false court testimony or unfair evidence can qualify without identifying a judge or criticizing the whole system. Clear contextual reference to the current execution is allowed; the word execution is not required.

**Do not infer.** General discontent, unidentified they outside a clear judicial context, or general encouragement to struggle does not automatically qualify. A criticism label records the claim, not its truth or the speaker's innocence.

**Boundary.** Use u when the target or critical intent remains ambiguous, including unresolved sarcasm. J and I are judged independently; J=1 and I=u can coexist.

### X | Farewell, closing or procedural readiness

Column: `farewell_readiness`

An explicit farewell, closure of the statement, or indication that the execution procedure may begin.

**Include.** Goodbye, that is all, and I am ready, Warden qualify. A clear semantic farewell can qualify without those words; I will see you on the other side may function as farewell in context.

**Do not infer.** Religious belief, a general expectation of reunion, or a request for divine reception does not automatically establish a present farewell. Being fine, lacking fear, or accepting punishment does not independently qualify.

**Boundary.** An ambiguous response to the warden, unexplained abbreviation, or unresolved departure metaphor may be u. X combines distinct speech acts and must not be interpreted as psychological acceptance of death.

## Development sample and use

The sample contains 50 people, ten per decade. The v2 decisions were reviewed and approved on 5 November 2026. NMF was fitted without these labels.

The frozen CSV schema is `execution_number`, `candidate_text`, followed by the eight label columns above in their displayed order. This guide documents the coding scheme. The approved label register and curated text data are distributed in the [data-v1 Release attachment](https://github.com/Doraaadorable/death-row-last-statements-nlp/releases/tag/data-v1), rather than tracked under data/processed/. Follow the download, checksum and reproduction steps in the [README](../README.md#reproduction).
