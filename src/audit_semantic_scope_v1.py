"""Apply an explicit, manual scope crosswalk to known development selections.

This is not an automatic predicate extractor or a predictive classifier.
Historical semantic labels and diagnostic outputs are never modified.
"""
from pathlib import Path
import hashlib
import json
import pandas as pd

INPUTS = [
    'reports/semantic_confirmed_snapshot40_v1.csv',
    'reports/semantic_owner_additions_9_shooting_naming.csv',
]
# Explicit exceptions to scope retention; unresolved relevance is not exclusion.
EXCEPTIONS = {
    'v3-dev21-001': ('scope_uncertain', 'The referent of doing this needs a documented task-relevance decision.'),
    'v3-dev21-004': ('exclude_scope', 'Uncertainty about what to say, not knowledge of a target act or responsibility claim.'),
    'v3-dev21-006': ('exclude_scope', 'Acquaintance/identity of the addressee, not knowledge of a target claim.'),
    'v3-dev21-008': ('scope_uncertain', 'Belief object is implicit; document its link to a target claim before inclusion.'),
    'v3-dev21-013': ('retire_representation', 'Historical nominal characterization is retained as context of the separate call record; no new independent predicate is supplied here.'),
    'v3-dev21-018': ('exclude_scope', 'Knowledge about witness access, outside the narrowed act/responsibility/stance task.'),
    'v3-dev21-027': ('scope_uncertain', 'Unresolved this; do not assume a criminal act or execution choice.'),
    'owner-added-198-choice-01': ('scope_uncertain', 'Unresolved choice object; do not assume an admission.'),
    'owner-added-538-speech-01': ('exclude_scope', 'Statement closure with no target claim.'),
    'owner-added-538-permission-01': ('exclude_scope', 'Procedural permission without explicit evaluative stance.'),
}

def audit(root):
    root = Path(root)
    tables = [pd.read_csv(root / p, keep_default_na=False) for p in INPUTS]
    rows = pd.concat(tables, ignore_index=True).fillna('')
    if len(rows) != 42 or rows.claim_id.duplicated().any():
        raise ValueError('Expected exactly 42 unique historical selections.')
    if not set(EXCEPTIONS).issubset(set(rows.claim_id)):
        raise ValueError('Crosswalk references an absent selection.')
    corpus_path = root / 'data/processed/model_corpus_v1.csv'
    corpus = pd.read_csv(corpus_path, keep_default_na=False).set_index('execution_number')
    if not corpus.index.is_unique:
        raise ValueError('Duplicate source document.')
    decisions = []
    for row in rows.to_dict('records'):
        context = corpus.loc[row['execution_number'], 'model_text']
        start, end = int(row['span_start']), int(row['span_end'])
        if context[start:end] != row['evidence_span'] or hashlib.sha256(context.encode()).hexdigest() != row['context_sha256']:
            raise ValueError('Source evidence changed: ' + row['claim_id'])
        status, reason = EXCEPTIONS.get(row['claim_id'], (
            'retain_scope',
            'Known selection concerns an act, responsibility, innocence, execution stance, or a directly linked mental/reporting proposition; retention is a manual crosswalk, not a semantic relabel.'
        ))
        decisions.append({'claim_id': row['claim_id'], 'execution_number': int(row['execution_number']),
                          'scope_status': status, 'reason': reason})
    counts = pd.Series([r['scope_status'] for r in decisions]).value_counts().to_dict()
    return {
        'version': 'semantic_scope_v1',
        'provenance': 'AI-applied scope crosswalk after owner requested direct testing; not individually owner-adjudicated',
        'scope': '42 known development selections only; not exhaustive predicate inventory or independent evaluation',
        'inputs_sha256': {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in INPUTS},
        'corpus_sha256': hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'counts': {k: int(v) for k, v in counts.items()}, 'decisions': decisions,
        'limitations': ['Scope retention does not confirm predicate boundaries.',
                        'Uncertain scope is separate from unclear semantic labels.',
                        'No method predictions, labels, historical files or model results were changed.'],
    }

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    result = audit(root)
    output = root / 'reports/semantic_scope_audit_v1.json'
    payload = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
    if output.exists() and output.read_text() != payload:
        raise FileExistsError('Existing audit differs; preserve it and version a new audit.')
    if not output.exists():
        output.write_text(payload)
    print(json.dumps(result['counts'], indent=2))
    print('Validated 42 source spans. Historical labels and model outputs unchanged.')
