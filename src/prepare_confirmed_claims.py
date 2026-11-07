"""Materialize conversation-confirmed claims without overwriting review files."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import pandas as pd
from claim_adjudication_v3 import FIELDS, read_table

CORPUS_SHA256 = 'd66a330b121ae5e59d96b58fb12d34b0c4fdbd9059d427abdc7bd182b07bcc2c'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_records(records, corpus, selected_ids):
    if len(records) != 37 or records.claim_id.duplicated().any():
        raise ValueError('Expected 37 unique selected claim IDs.')
    if not set(records.execution_number).issubset(set(selected_ids)):
        raise ValueError('A claim is outside the fixed development sample.')
    if not records.owner_decision.eq('accept').all():
        raise ValueError('Only explicitly confirmed discussion decisions belong here.')
    if not records.message_timestamp.eq('not_recorded').all():
        raise ValueError('Historical message timestamps must not be reconstructed.')
    if corpus.execution_number.duplicated().any():
        raise ValueError('Duplicate corpus execution IDs.')
    contexts = corpus.set_index('execution_number')
    for row in records.itertuples():
        text = contexts.loc[row.execution_number, 'model_text']
        start, end = int(row.span_start), int(row.span_end)
        if start < 0 or end <= start or end > len(text):
            raise ValueError(f'Invalid span range: {row.claim_id}')
        if text[start:end] != row.evidence_span or hashlib.sha256(text.encode()).hexdigest() != row.context_sha256:
            raise ValueError(f'Source evidence mismatch: {row.claim_id}')
        for field, values in FIELDS.items():
            if getattr(row, field) not in values:
                raise ValueError(f'Invalid {field}: {row.claim_id}')
        if not row.reviewer_id.strip() or row.process != 'AI_assisted_discussion_owner_confirmed_not_blind':
            raise ValueError('Missing owner/process provenance.')

def write_new_or_identical(path, data):
    path = Path(path)
    if path.exists():
        if path.read_bytes() != data:
            raise FileExistsError(f'{path.name} differs; preserve it and version changes separately.')
        return 'verified_existing'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(data)
    return 'created'

def materialize(root):
    root = Path(root)
    base = root/'data/processed'
    source = base/'model_corpus_v1.csv'
    record_path = root/'reports/semantic_owner_decisions_v3_discussion.csv'
    selection_path = root/'reports/semantic_development_sampling_v1.json'
    if sha(source) != CORPUS_SHA256:
        raise ValueError('Frozen model corpus hash mismatch.')
    ids = json.loads(selection_path.read_text())['execution_ids_in_display_order']
    if len(ids) != 21 or len(set(ids)) != 21:
        raise ValueError('Expected 21 fixed document IDs.')
    corpus = read_table(source)
    records = read_table(record_path)
    validate_records(records, corpus, ids)
    contexts = corpus.set_index('execution_number')
    prepared = records.copy()
    prepared['source_url'] = prepared.execution_number.map(contexts.source_url)
    prepared['model_text'] = prepared.execution_number.map(contexts.model_text)
    prepared['use_scope'] = 'selected_development_only_not_exhaustive_not_independent'
    dest = base/'semantic_owner_confirmed_v3_37.csv'
    payload = prepared.to_csv(index=False).encode()
    inputs = {'model_corpus':sha(source), 'owner_discussion_record':sha(record_path),
              'fixed_selection':sha(selection_path), 'preparation_script':sha(__file__),
              'field_validation_module':sha(root/'src/claim_adjudication_v3.py')}
    manifest_path = base/'semantic_owner_confirmed_v3_37_manifest.json'
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text())
        if old['inputs_sha256'] != inputs or old['output_sha256'] != hashlib.sha256(payload).hexdigest():
            raise FileExistsError('Existing manifest has different provenance; nothing overwritten.')
        if not dest.exists():
            raise FileNotFoundError('Manifest exists but output is missing; investigate before restoring.')
    status = write_new_or_identical(dest, payload)
    manifest = {'materialized_at':datetime.now(timezone.utc).isoformat(),
                'timestamp_meaning':'actual materialization time, not historical owner decision time',
                'inputs_sha256':inputs, 'output_sha256':sha(dest),
                'propositions':len(prepared),'documents_with_selected_claims':int(prepared.execution_number.nunique()),
                'scope':'AI-assisted owner-confirmed selected development claims; not an independent or exhaustive reference set'}
    if not manifest_path.exists():
        write_new_or_identical(manifest_path,(json.dumps(manifest,indent=2)+'\n').encode())
    else:
        manifest=json.loads(manifest_path.read_text())
    # This table distinguishes discussion scope from independent/exhaustive audit.
    scope_notes={141:'Religious self-evaluation retained in notes; owner agreed not to select a contrast row.',
                 414:'Apology/religious forgiveness retained in notes; no specified action attribution selected.'}
    summary=pd.DataFrame([{'execution_number':eid,
                           'confirmed_selected_propositions':int(prepared.execution_number.eq(eid).sum()),
                           'discussion_selection_status':'selected_claims_confirmed' if prepared.execution_number.eq(eid).any() else 'owner_agreed_no_selection_in_scope',
                           'scope_note':scope_notes.get(eid,'Selected claims confirmed; not a complete proposition inventory.'),
                           'exhaustive_document_review':'not_certified'} for eid in ids])
    summary_path=base/'semantic_document_scope_v3_21.csv'
    write_new_or_identical(summary_path,summary.to_csv(index=False).encode())
    summary_manifest=base/'semantic_document_scope_v3_21_manifest.json'
    write_new_or_identical(summary_manifest,(json.dumps({'inputs_sha256':inputs,'output_sha256':sha(summary_path),'scope':'discussion selection scope, not exhaustive annotation'},indent=2)+'\n').encode())
    return prepared, summary, manifest, status

if __name__ == '__main__':
    root=Path(__file__).resolve().parents[1]
    records, summary, manifest, status=materialize(root)
    print(f'Confirmed selected propositions: {len(records)}')
    print(f'Documents with selected propositions: {records.execution_number.nunique()} / 21')
    print(f'Artifact status: {status}; old worksheets were not overwritten.')
