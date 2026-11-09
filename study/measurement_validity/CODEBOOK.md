# Codebook: apology and innocence claims

Version 1.0 (draft; frozen when `protocol_lock.json` is created). Do not edit after coding starts. Any later change needs a new version and a note in the protocol.

These definitions follow the separation used by Eaton & Theuer (2009, pp. 334–335), who code apology, forgiveness requests, responsibility, admission of guilt, innocence, accident accounts and excuses as distinct variables.

> **Before freezing:** compare both definitions below with the article's wording on pp. 334–335 and adjust them so they match. Record any intentional difference in the "Differences from Eaton & Theuer" section at the end.

## What to read

- Code **only the speaker's own words** in the text shown.
- Ignore recorder or editorial material, such as `(crying)`, `[inaudible]` or `[have]`.
- Quoted prayer or scripture counts only if the speaker uses it to say something in their own voice. Reciting "forgive us our trespasses" in the Lord's Prayer is **not** an apology.
- Judge each statement as a whole, but code only what is said. Do not use case facts, outside knowledge or guesses about sincerity.

## Values

| Value | Use when |
|---|---|
| `1` | The text clearly meets the definition. |
| `0` | It does not. Silence is `0`: a statement that never mentions the crime is `0` for both. |
| `u` | There is relevant text, but you cannot decide between `1` and `0` from the words alone. Use sparingly, and say why in the note. |

## A. Apology

**`1`:** the speaker explicitly apologizes, or says they are sorry, to someone, about something they did or a harm or loss connected to them.

- "I'm sorry for what I did." / "I apologize to the Smith family." → `1`
- "I'm sorry for the pain I caused my mother." → `1` (the recipient does not have to be the victim's family)
- "To the victim's family, I am so sorry for your loss." → `1`
- "Sorry" as politeness ("Sorry, I forgot what I wanted to say") → `0`
- A forgiveness request with no apology or sorrow ("Please forgive me") → `0`; mention it in the note
- Sorrow about the situation with no harm or act tied to the speaker ("I'm sorry it came to this") → `u`, unless the context makes the reference clear
- Remorse expressed without apology words ("I regret what I did every day") → `0`. Remorse is a separate concept; mention it in the note.

## B. Innocence claim

**`1`:** the speaker asserts that they did not commit the crime they are being executed for, or that they are innocent or wrongly convicted.

- "I am an innocent man." / "I did not kill her." / "You are executing the wrong person." → `1`
- Denying the killing while admitting being present ("I was there, but I didn't shoot anyone") → `1`
- An accident or self-defense account that admits the act ("It was an accident; I never meant to hurt him") → `0`; mention it in the note
- Criticism of the trial, the death penalty or the system without denying the act → `0`
- "God knows the truth" or "One day the truth will come out" with nothing else → `u`

## Note column

Use the note for anything that helps adjudication: a forgiveness request, remorse without apology, an accident account, the reason for a `u`, or a transcription problem.

## Differences from Eaton & Theuer

_To be filled in before freezing._
