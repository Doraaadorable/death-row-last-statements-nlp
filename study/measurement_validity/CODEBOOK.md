# Codebook: apology, condolence and innocence claims

Version 1.1 (protocol version 1.3; version 1.0 had no condolence variable), frozen in `protocol_lock.json`. Do not edit after coding starts. Any later change needs a new version and a note in the protocol.

These definitions build on Eaton & Theuer (2009, pp. 334–335), who code apology, remorse, forgiveness requests, empathy, responsibility, admission of guilt, innocence, accident and excuse as separate variables. Where this codebook deliberately differs, the difference is listed at the end.

## What to read

- Read the English text as shown. You may look up single words, but do not use machine translation.
- Code **only the speaker's own words**.
- Ignore recorder or editorial material, such as `(crying)`, `[inaudible]` or `[have]`.
- Quoted prayer or scripture counts only if the speaker uses it to say something in their own voice. Reciting "forgive us our trespasses" in the Lord's Prayer is **not** an apology.
- Judge each statement as a whole, but code only what is said. Do not use case facts, outside knowledge or guesses about sincerity.

## Values

| Value | Use when |
|---|---|
| `1` | The text clearly meets the definition. |
| `0` | It does not. Silence is `0`: a statement that never mentions the crime is `0` for all three. |
| `u` | There is relevant text, but you cannot decide between `1` and `0` from the words alone. Use sparingly, and say why in the note. |

## A. Apology

**`1`:** the speaker apologizes, or says they are sorry, in a way that takes something on themselves: either the apology is tied to their own act or the harm they caused, or it is a direct apology to someone with no object stated.

| Example | Code |
|---|---|
| "I'm sorry for what I did." / "I apologize for taking your son's life." | `1` |
| "I'm sorry for the pain I caused my mother." (any recipient, including the speaker's own family) | `1` |
| "To the Smith family, I'm sorry." / "I want to apologize to the family." (direct apology, no object stated) | `1` |
| "To the victim's family, I am so sorry for your loss." (sorrow about the family's loss, not tied to the speaker) | `0`; condolence `1` |
| "I'm sorry for the pain you have been through." (sorrow for the other person's pain, not tied to the speaker) | `0`; condolence `1` |
| "I'm sorry it came to this." (sorrow about the situation) | `0`, unless the context ties it to the speaker's act; condolence `1` |
| "Sorry, I forgot what I wanted to say." (politeness) | `0` |
| "Please forgive me." (forgiveness request, no apology) | `0`; note "forgiveness request" |
| "I regret what I did every day." (remorse, no apology) | `0`; note "remorse" |

If a statement contains both a condolence and an apology ("I'm sorry for your loss. I'm sorry for what I did."), code apology `1` and condolence `1`.

## C. Condolence

**`1`:** the speaker says they are sorry, or apologizes, about another person's loss or pain, or about the situation, without tying it to their own act. This is the "sorry" that section A codes `0`.

| Example | Code |
|---|---|
| "I am so sorry for your loss." / "I'm sorry for the pain you have been through." | `1` |
| "I'm sorry it came to this." / "I'm sorry we all had to be here." | `1` |
| "I'm sorry for what I did." (tied to the speaker's act: apology, not condolence) | `0` |
| "My heart goes out to you." / "I know you are hurting." (sympathy without "sorry" or "apologize") | `0` |
| "Sorry, I forgot what I wanted to say." (politeness) | `0` |

Condolence is coded independently of apology: a statement can be `1` for both. Together the two give Eaton & Theuer's broader apology variable, which counts any "sorry" (see the differences below).

## B. Innocence claim

**`1`:** the speaker asserts that they should not stand convicted, either by denying the act or by claiming the act was lawful. In the note, write **F** or **L**:

- **F (factual):** denies doing what they were convicted of.
- **L (legal):** admits the act but claims it was legally justified, for example self-defense or defense of another person.

| Example | Code |
|---|---|
| "I am an innocent man." / "I did not kill her." / "You are executing the wrong person." | `1`, F |
| "I was there, but I didn't shoot anyone." (denies the killing) | `1`, F |
| "I killed him, but it was self-defense." | `1`, L |
| "It was an accident; I never meant to kill him." (admits a wrongful act, disputes intent) | `0`; note "accident" |
| "I was on drugs, I wasn't myself." (excuse) | `0`; note "excuse" |
| Criticism of the trial, the lawyers or the death penalty, without denying the act | `0` |
| "God knows the truth." / "One day the truth will come out." (no explicit denial) | `0` |

Use `u` only when the words could reasonably be read either way, for example "I didn't do what they say I did" when it is unclear whether the speaker denies the act or only the prosecution's version of it.

## Note column

Write anything that helps adjudication: F or L for innocence claims, "forgiveness request", "remorse", "accident", "excuse", the reason for a `u`, or a transcription problem.

## Differences from Eaton & Theuer

1. **Apology is narrower.** Eaton & Theuer code an apology whenever the speaker "specifically said they were sorry". Here, sorrow about the other person's loss or pain that is not tied to the speaker ("sorry for your loss") is `0` for apology and `1` for condolence, which is close to their separate *empathy* variable. Apology or condolence (`apology_broad` in the analysis) corresponds to their apology variable, and its prevalence is the one to set beside their 32.5%.
2. **Innocence includes legal justification.** Eaton & Theuer code claims of innocence separately from accident and excuse accounts; a self-defense account would probably fall outside their innocence variable. Here, self-defense and similar justification claims are `1` and marked **L**, so results can be reported both with and without them. Accident and excuse accounts are `0`, as in their scheme.
3. **No uncertain-by-default rule.** Eaton & Theuer code every coder disagreement as "unclear" (their value 3). Here, disagreements are resolved by adjudication, and `u` is kept only for genuinely undecidable text.
