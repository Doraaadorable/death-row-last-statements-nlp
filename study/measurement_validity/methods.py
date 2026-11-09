"""Automated measures compared with blind human coding.

Everything in this file is frozen by protocol_lock.json before human labels exist.
Do not tune these rules on the study sample.
"""
import re

CONSTRUCTS = ("apology", "innocence")

# ---------------------------------------------------------------- 1. Dictionary rules
# Deliberately simple keyword rules of the kind used in many text-analysis studies.

_APOSTROPHES = str.maketrans({"’": "'", "‘": "'", "ʼ": "'"})

APOLOGY_PATTERNS = [
    r"\bsorry\b",
    r"\bapologi[sz](?:e|ed|es|ing)\b",
    r"\bapolog(?:y|ies)\b",
]
APOLOGY_NEGATIONS = [
    r"\b(?:not|never|ain't|isn't|am not|'m not)\s+(?:\w+\s+){0,2}sorry\b",
    r"\bno\s+apolog(?:y|ies)\b",
]

INNOCENCE_PATTERNS = [
    r"\b(?:i am|i'm|im)\s+(?:an?\s+)?innocent\b",
    r"\binnocent\s+(?:man|person|woman|men)\b",
    r"\bnot\s+guilty\b",
    r"\bi\s+(?:did\s+not|didn't|didnt|never)\s+(?:do|kill|killed|commit|murder|murdered|shoot|shot|hurt|harm|rape|stab|stabbed)\b",
    r"\b(?:did\s+not|didn't|didnt)\s+do\s+(?:it|this|that)\b",
    r"\bwrong\s+(?:man|person|guy)\b",
]

_COMPILED = {
    "apology": [re.compile(p) for p in APOLOGY_PATTERNS],
    "apology_neg": [re.compile(p) for p in APOLOGY_NEGATIONS],
    "innocence": [re.compile(p) for p in INNOCENCE_PATTERNS],
}


def normalise(text):
    return " ".join(str(text).translate(_APOSTROPHES).lower().split())


def dictionary_label(text, construct):
    """Return 1 if any pattern for the construct matches, else 0."""
    t = normalise(text)
    if construct == "apology":
        hits = [m.span() for p in _COMPILED["apology"] for m in p.finditer(t)]
        negated = [m.span() for p in _COMPILED["apology_neg"] for m in p.finditer(t)]
        # A hit counts unless it lies inside a negated phrase ("not sorry").
        kept = [h for h in hits if not any(n[0] <= h[0] and h[1] <= n[1] for n in negated)]
        return int(bool(kept))
    if construct == "innocence":
        return int(any(p.search(t) for p in _COMPILED["innocence"]))
    raise KeyError(construct)


# ---------------------------------------------------------------- 2. Topic-model rule
# Uses the existing six-topic NMF (results/nmf_v2/document_weights_k6.csv), fitted on
# all 477 documents without labels. Topic numbers are fixed from that run:
#   topic_1: sorry, peace, forgive, hope, pain, god   -> apology
#   topic_3: not, did, know, did not, say, want       -> innocence
# A document is positive when the topic is its largest weight.
NMF_TOPIC = {"apology": "topic_1", "innocence": "topic_3"}


def nmf_label(weights_row, construct):
    """weights_row: mapping topic_1..topic_6 -> weight. Zero-weight documents are 0."""
    values = {k: float(v) for k, v in weights_row.items() if k.startswith("topic_")}
    if not values or max(values.values()) <= 0:
        return 0
    return int(max(values, key=values.get) == NMF_TOPIC[construct])


# ---------------------------------------------------------------- 3. LLM classifier
LLM_MODEL = "claude-opus-5-5"
LLM_EFFORT = "low"
LLM_REPEATS = 3          # run 1 is the primary result; runs 2-3 measure self-consistency

LLM_SYSTEM = """You code the final statements of people executed in Texas for a research study.
Code only what the speaker says. Ignore recorder or editorial notes in brackets or parentheses.
Quoted prayer or scripture counts only if the speaker uses it to speak in their own voice.
Do not use outside knowledge about the case and do not judge sincerity."""

LLM_INSTRUCTIONS = """Code the statement below for two variables. For each, answer "yes", "no" or "uncertain".

APOLOGY: "yes" if the speaker explicitly apologizes, or says they are sorry, to someone, about something they did or a harm or loss connected to them. The recipient can be anyone. "Sorry" used as politeness is "no". A forgiveness request without apology or sorrow is "no". Remorse without apology words is "no". Sorrow about the situation with no harm or act tied to the speaker is "uncertain".

INNOCENCE: "yes" if the speaker asserts they did not commit the crime they are being executed for, or that they are innocent or wrongly convicted, including denying the killing while admitting being present. An accident or self-defense account that admits the act is "no". Criticism of the trial or the death penalty without denying the act is "no". A bare statement such as "God knows the truth" is "uncertain".

Statement:
<statement>
{text}
</statement>"""

LLM_SCHEMA = {
    "type": "object",
    "properties": {
        "apology": {"type": "string", "enum": ["yes", "no", "uncertain"]},
        "innocence": {"type": "string", "enum": ["yes", "no", "uncertain"]},
    },
    "required": ["apology", "innocence"],
    "additionalProperties": False,
}

# Primary scoring of the LLM: "yes" -> 1; "no" and "uncertain" -> 0.
# The number of "uncertain" answers is reported separately.
LLM_VALUE = {"yes": 1, "no": 0, "uncertain": 0}
