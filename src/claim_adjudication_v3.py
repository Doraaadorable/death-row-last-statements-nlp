"""Validate development owner decisions without changing source proposals."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
import pandas as pd

FIELDS = {
    'claim_source': {'self', 'other', 'unclear'},
    'event_type': {'killing_action', 'knowledge', 'wrongdoing_unspecified', 'other', 'unclear'},
    'event_actor': {'self', 'other', 'unspecified', 'unclear'},
    'polarity': {'affirmed', 'negated', 'unclear'},
    'proposition_status': {'presented_as_true', 'nonasserted', 'unclear'},
}
OWNER = ['owner_decision', *['owner_'+f for f in FIELDS], 'owner_note', 'reviewer_id', 'reviewed_at']

def read_table(path):
    try:
        return pd.read_csv(path, keep_default_na=False, encoding='utf-8-sig')
    except UnicodeDecodeError as exc:
        raise ValueError('Save CSV as UTF-8. Original file has not been modified.') from exc

def validate_proposals(proposals, corpus):
    if proposals.claim_id.duplicated().any():
        raise ValueError('Duplicate claim_id.')
    corpus = corpus.set_index('execution_number')
    for row in proposals.itertuples():
        text = corpus.loc[row.execution_number, 'model_text']
        if (hashlib.sha256(text.encode()).hexdigest() != row.context_sha256
                or text[int(row.span_start):int(row.span_end)] != row.evidence_span):
            raise ValueError(f'Evidence differs: {row.claim_id}')
        for field, allowed in FIELDS.items():
            if getattr(row, 'proposed_'+field) not in allowed:
                raise ValueError(f'Invalid proposed {field}: {row.claim_id}')

def load_or_create(proposals, path):
    path = Path(path)
    if not path.exists():
        table = proposals.copy()
        for field in OWNER:
            table[field] = ''
        with path.open('x', encoding='utf-8', newline='') as handle:
            table.to_csv(handle, index=False)
    table = read_table(path)
    if set(table.columns) != set(proposals.columns) | set(OWNER):
        raise ValueError('Worksheet columns differ. Nothing overwritten.')
    if table.claim_id.duplicated().any() or set(table.claim_id) != set(proposals.claim_id):
        raise ValueError('Worksheet IDs differ. Use the additions file for new claims.')
    ordered = table.set_index('claim_id').loc[proposals.claim_id].reset_index()
    pd.testing.assert_frame_equal(ordered[proposals.columns], proposals, check_dtype=False)
    validate_decisions(ordered)
    return ordered

def validate_decisions(table, complete=False):
    for row in table.to_dict('records'):
        decision = row['owner_decision']
        if decision not in {'', 'accept', 'revise', 'defer'}:
            raise ValueError(f"Invalid owner_decision: {row['claim_id']}")
        for field, allowed in FIELDS.items():
            value = row['owner_'+field]
            if value and value not in allowed:
                raise ValueError(f"Invalid owner {field}: {row['claim_id']}")
            if decision in {'', 'defer'} and value:
                raise ValueError('Pending/deferred rows must not carry final field overrides.')
            if decision == 'accept' and value and value != row['proposed_'+field]:
                raise ValueError('Accept conflicts with owner field; use revise.')
        if decision in {'revise', 'defer'} and not row['owner_note'].strip():
            raise ValueError('Revise/defer requires a note.')
        if decision == 'revise':
            if not all(row['owner_'+f] for f in FIELDS):
                raise ValueError('Revise requires all five owner fields.')
            if not any(row['owner_'+f] != row['proposed_'+f] for f in FIELDS):
                raise ValueError('Revise must change at least one field; use accept with a note.')
        if decision:
            if not row['reviewer_id'].strip() or not row['reviewed_at'].strip():
                raise ValueError('Decision requires reviewer_id and timezone-aware reviewed_at.')
            try:
                dt = datetime.fromisoformat(row['reviewed_at'])
                if dt.tzinfo is None:
                    raise ValueError()
            except ValueError as exc:
                raise ValueError('Use ISO time with timezone, e.g. 2026-11-06T12:00:00-05:00.') from exc
        if complete and not decision:
            raise ValueError('Export blocked: pending proposition decisions remain.')

def export_review(root, proposals, worksheet_path, documents_path, tag):
    """Export only explicitly adjudicated rows plus separate deferred records."""
    root = Path(root)
    table = load_or_create(proposals, worksheet_path)
    validate_decisions(table, complete=True)
    documents = read_table(documents_path)
    coverage = read_table(root/'reports/semantic_development_document_coverage_v1.csv')
    if documents.execution_number.duplicated().any() or set(documents.execution_number) != set(coverage.execution_number):
        raise ValueError('Document decisions must cover all 21 fixed IDs once.')
    if not documents.owner_document_decision.isin(['reviewed_selected', 'reviewed_no_selection', 'defer']).all():
        raise ValueError('Complete document decisions first.')
    for row in documents.to_dict('records'):
        if not row['owner_note'].strip() or not row['reviewer_id'].strip():
            raise ValueError('Document decision requires note and reviewer ID.')
        try:
            if datetime.fromisoformat(row['reviewed_at']).tzinfo is None:
                raise ValueError()
        except ValueError as exc:
            raise ValueError('Document decision requires timezone-aware ISO timestamp.') from exc
        has_selected = row['execution_number'] in set(table.execution_number)
        if row['owner_document_decision']=='reviewed_no_selection' and has_selected:
            raise ValueError('Selected claims exist; resolve selection in a new proposals version first.')
        if row['owner_document_decision']=='reviewed_selected' and not has_selected:
            raise ValueError('No selected claims; add and version proposals first.')
    if not tag or any(ch not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for ch in tag):
        raise ValueError('Use a simple unique export tag.')
    dest = root/'results'/('semantic_adjudication_'+tag)
    if dest.exists():
        raise FileExistsError('Export exists; choose another tag.')
    accepted = table.loc[table.owner_decision.isin(['accept','revise'])].copy()
    deferred_documents = set(documents.loc[documents.owner_document_decision.eq('defer'),'execution_number'])
    accepted = accepted.loc[~accepted.execution_number.isin(deferred_documents)]
    for f in FIELDS:
        accepted['final_'+f] = [x['owner_'+f] if x['owner_decision']=='revise' else x['proposed_'+f] for x in accepted.to_dict('records')]
    dest.mkdir(parents=True)
    table.to_csv(dest/'all_decisions.csv',index=False)
    accepted.to_csv(dest/'adjudicated_propositions.csv',index=False)
    documents.to_csv(dest/'document_decisions.csv',index=False)
    hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir()}
    hashes['proposals_dataframe_csv'] = hashlib.sha256(proposals.to_csv(index=False).encode()).hexdigest()
    hashes['owner_worksheet_input'] = hashlib.sha256(Path(worksheet_path).read_bytes()).hexdigest()
    hashes['owner_documents_input'] = hashlib.sha256(Path(documents_path).read_bytes()).hexdigest()
    hashes['frozen_corpus_input'] = hashlib.sha256((root/'data/processed/model_corpus_v1.csv').read_bytes()).hexdigest()
    hashes['guideline_input'] = hashlib.sha256((root/'docs/SEMANTIC_CLAIM_GUIDELINE_v3_DRAFT.md').read_bytes()).hexdigest()
    manifest = {'created_at':datetime.now(timezone.utc).isoformat(),'scope':'AI-assisted development; not independent validation; illustrative selections only', 'hashes':hashes, 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return dest
