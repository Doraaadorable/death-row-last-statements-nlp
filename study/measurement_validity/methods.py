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
    """Primary rule: the topic is the document's largest topic.
    weights_row maps topic_1..topic_6 -> weight. Zero-weight documents are 0."""
    values = {k: float(v) for k, v in weights_row.items() if k.startswith("topic_")}
    if not values or max(values.values()) <= 0:
        return 0
    return int(max(values, key=values.get) == NMF_TOPIC[construct])


def nmf_top2_label(weights_row, construct):
    """Secondary rule (protocol v1.1): the topic is among the document's two largest
    topics and has a nonzero weight. A looser rule than nmf_label; uses no labels."""
    values = {k: float(v) for k, v in weights_row.items() if k.startswith("topic_")}
    topic = NMF_TOPIC[construct]
    if values.get(topic, 0.0) <= 0:
        return 0
    top2 = sorted(values, key=values.get, reverse=True)[:2]
    return int(topic in top2)


# ---------------------------------------------------------------- 3. LLM classifier
LLM_MODEL = "claude-opus-5-5"
LLM_EFFORT = "low"
LLM_REPEATS = 3          # run 1 is the primary result; runs 2-3 measure self-consistency

LLM_SYSTEM = """You code the final statements of people executed in Texas for a research study.
Code only what the speaker says. Ignore recorder or editorial notes in brackets or parentheses.
Quoted prayer or scripture counts only if the speaker uses it to speak in their own voice.
Do not use outside knowledge about the case and do not judge sincerity."""

LLM_INSTRUCTIONS = """Code the statement below for two variables. For each, answer "yes", "no" or "uncertain". Use "uncertain" only when the words could reasonably be read either way.

APOLOGY: "yes" if the speaker apologizes, or says they are sorry, in a way that takes something on themselves: either the apology is tied to their own act or the harm they caused (for example "I'm sorry for what I did", "I'm sorry for the pain I caused my mother"), or it is a direct apology to someone with no object stated (for example "To the Smith family, I'm sorry"). The recipient can be anyone. "No" for: condolence that is not tied to the speaker ("I am so sorry for your loss", "I'm sorry for the pain you have been through"); sorrow about the situation ("I'm sorry it came to this"); "sorry" used as politeness; a forgiveness request without an apology; remorse or regret without an apology. If a statement has both a condolence and an apology, answer "yes".

INNOCENCE: "yes" if the speaker asserts they should not stand convicted, either by denying the act they were convicted of (for example "I am an innocent man", "I did not kill her", "I was there, but I didn't shoot anyone") or by admitting the act but claiming it was legally justified, such as self-defense. "No" for: an accident account that admits a wrongful act but disputes intent; an excuse such as intoxication; criticism of the trial, the lawyers or the death penalty without denying the act; a statement such as "God knows the truth" with no explicit denial.

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
# The number of "uncertain" answers is reported separately, and a sensitivity
# analysis scores "uncertain" as 1.
LLM_VALUE = {"yes": 1, "no": 0, "uncertain": 0}
# Protocol v1.1: these outcomes are not answers. They are excluded from LLM metrics
# (never scored as 0) and reported as a coverage table.
LLM_NON_ANSWERS = ("refused", "failed", "invalid")


# ---------------------------------------------------------------- supervised method (protocol v1.3)

# Supervised methods (bert_classify.py, tfidf_classify.py): the prediction is 1 when the
# positive-class probability, averaged over seeds for BERT, is at least this threshold.
SUPERVISED_THRESHOLD = 0.5
