"""Literal cue retrieval for feasibility screening, never semantic labeling."""
import re
import pandas as pd

PATTERNS = {
    'action_or_innocence_cue': (
        r"\b(?:kill(?:s|ed|ing)?|murder(?:s|ed|ing)?|innocen(?:t|ce))\b|"
        r"\b(?:did\s+not|didn['’]t|never|not)\s+(?:do|commit)\b"
    ),
    'negated_knowledge_cue': (
        r"\b(?:did|do|does|could|can|was|were|is|have|has|had)\s+not\s+(?:know|understand)\b|"
        r"\b(?:didn['’]t|don['’]t|doesn['’]t|can['’]t|couldn['’]t)\s+(?:know|understand)\b|"
        r"\b(?:never|not)\s+(?:knew|known|know|understood|understand)\b|\bunaware\b"
    ),
    'reporting_or_saying_cue': (
        r"\b(?:say|says|said|saying|tell|tells|told|claim|claims|claimed|claiming|"
        r"believe|believes|believed|believing)\b|\baccording\s+to\b"
    ),
}


def screen_documents(prepared):
    required = {'execution_number', 'model_text', 'source_url'}
    if not required.issubset(prepared.columns):
        raise ValueError('Missing screening input columns')
    if not prepared.execution_number.is_unique or prepared.model_text.str.strip().eq('').any():
        raise ValueError('Duplicate IDs or empty prepared texts')
    result = prepared[['execution_number', 'source_url', 'model_text']].copy()
    for name, pattern in PATTERNS.items():
        result[name] = result.model_text.str.contains(pattern, flags=re.IGNORECASE, regex=True)
    result['candidate_document'] = result.action_or_innocence_cue | result.negated_knowledge_cue
    result['cue_combination'] = [
        f'action={int(a)};knowledge={int(k)};reporting={int(r)}'
        for a,k,r in zip(result.action_or_innocence_cue,
                         result.negated_knowledge_cue,
                         result.reporting_or_saying_cue)
    ]
    return result.sort_values('execution_number').reset_index(drop=True)
