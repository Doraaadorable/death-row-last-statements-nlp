"""Versioned 40-selection snapshot: semantic confirmation != focus confirmation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,platform
import pandas as pd
from claim_adjudication_v3 import FIELDS,read_table
from prepare_confirmed_claims import CORPUS_SHA256,sha,write_new_or_identical

RECORD_PATHS=['reports/semantic_owner_decisions_v3_discussion.csv','reports/semantic_owner_additions_287_focus.csv','reports/semantic_owner_addition_198_choice.csv']
FOCUS_PATH='reports/owner_confirmed_focus_boundaries_v1.csv'
PLAN_PATH='reports/predicate_focus_audit_plan_v1.json'
CORE=['claim_source','event_type','event_actor','polarity','proposition_status']

def combine(records_list,focus_decisions,plan,corpus,selection_ids):
    records=pd.concat(records_list,ignore_index=True).fillna('')
    if len(records)!=40 or records.claim_id.duplicated().any():raise ValueError('Expected 40 unique claim IDs.')
    if not set(records.execution_number).issubset(selection_ids):raise ValueError('Outside fixed development selection.')
    if not records.owner_decision.eq('accept').all():raise ValueError('Not all proposition decisions are confirmed.')
    if not records.message_timestamp.eq('not_recorded').all():raise ValueError('Do not fabricate decision times.')
    contexts=corpus.set_index('execution_number')
    if contexts.index.duplicated().any():raise ValueError('Duplicate source execution ID.')
    plans={x['claim_id']:x for x in plan}
    if len(plans)!=39 or not set(plans)<set(records.claim_id):raise ValueError('Unexpected 39-row manual audit plan.')
    if len(focus_decisions)!=7 or focus_decisions.claim_id.duplicated().any():raise ValueError('Expected seven unique focus confirmations.')
    if not set(focus_decisions.claim_id).issubset(set(records.claim_id)):raise ValueError('Unknown focus confirmation ID.')
    if not focus_decisions.focus_decision.eq('owner_confirmed').all():raise ValueError('Unconfirmed focus decisions.')
    confirmed=focus_decisions.set_index('claim_id');out=[]
    for row in records.to_dict('records'):
        text=contexts.loc[row['execution_number'],'model_text'];a,b=int(row['span_start']),int(row['span_end'])
        if not 0<=a<b<=len(text) or text[a:b]!=row['evidence_span'] or hashlib.sha256(text.encode()).hexdigest()!=row['context_sha256']:
            raise ValueError('Evidence differs: '+row['claim_id'])
        for field,allowed in FIELDS.items():
            if row[field] not in allowed:raise ValueError('Invalid confirmed '+field)
        if row['claim_id'] in plans:
            item=plans[row['claim_id']];focus=item['predicate_focus'];offsets=[m.start() for m in re.finditer(re.escape(focus),row['evidence_span'])];occ=item['zero_based_occurrence_in_evidence']
            if not 0<=occ<len(offsets):raise ValueError('Proposed focus not found.')
            fs=a+offsets[occ];fe=fs+len(focus)
            focus_status='AI_proposed_not_owner_confirmed'
            if row['claim_id'] in confirmed.index:
                d=confirmed.loc[row['claim_id']]
                if int(d.execution_number)!=int(row['execution_number']) or d.predicate_focus!=focus or int(d.focus_start)!=fs or int(d.focus_end)!=fe:
                    raise ValueError('Focus proposal conflicts with owner confirmation.')
                focus_status='owner_confirmed'
        else:
            focus=row['predicate_focus'];fs=int(row['focus_start']);fe=int(row['focus_end']);focus_status='owner_confirmed'
        # The two mental-state addition rows already have explicit focus evidence.
        if row['claim_id'].startswith('owner-added-287-'):
            if row['predicate_focus']!=focus or int(row['focus_start'])!=fs or int(row['focus_end'])!=fe:raise ValueError('Confirmed addition focus changed.')
            focus_status='owner_confirmed'
        if not a<=fs<fe<=b or text[fs:fe]!=focus:raise ValueError('Focus is not exact within evidence.')
        row.update(predicate_focus=focus,focus_start=fs,focus_end=fe,focus_confirmation=focus_status,
                   semantic_confirmation='owner_confirmed_after_AI_discussion',source_url=contexts.loc[row['execution_number'],'source_url'],
                   snapshot_use='selected_development_not_independent_not_exhaustive')
        out.append(row)
    table=pd.DataFrame(out)
    # No established semantic value may change during consolidation.
    original=records.set_index('claim_id');new=table.set_index('claim_id')
    pd.testing.assert_frame_equal(original.loc[new.index,CORE],new[CORE],check_dtype=False)
    if table.focus_confirmation.eq('owner_confirmed').sum()!=10:raise ValueError('Expected 10 owner-confirmed focus positions.')
    cols=['claim_id','execution_number','evidence_span','span_start','span_end','context_sha256','predicate_focus','focus_start','focus_end','focus_confirmation',*CORE,'owner_decision','semantic_confirmation','review_note','reviewer_id','process','message_timestamp','source_url','snapshot_use']
    return table[cols]

def build(root):
    root=Path(root);corpus_path=root/'data/processed/model_corpus_v1.csv'
    if sha(corpus_path)!=CORPUS_SHA256:raise ValueError('Frozen corpus differs.')
    selection_path=root/'reports/semantic_development_sampling_v1.json'
    ids=json.loads(selection_path.read_text())['execution_ids_in_display_order']
    records=[read_table(root/p) for p in RECORD_PATHS]
    table=combine(records,read_table(root/FOCUS_PATH),json.loads((root/PLAN_PATH).read_text()),read_table(corpus_path),ids)
    snapshots=root/'data/processed/semantic_confirmed_snapshot40_v1.csv'
    manifest_path=root/'data/processed/semantic_confirmed_snapshot40_v1_manifest.json'
    payload=table.to_csv(index=False).encode()
    inputs=[*RECORD_PATHS,FOCUS_PATH,PLAN_PATH,str(corpus_path.relative_to(root)),str(selection_path.relative_to(root))]
    provenance={p:sha(root/p) for p in inputs}
    codes={p:sha(root/'src'/p) for p in ['build_confirmed_snapshot40.py','claim_adjudication_v3.py','prepare_confirmed_claims.py']}
    manifest={'materialized_at':datetime.now(timezone.utc).isoformat(),'timestamp_meaning':'actual snapshot creation time, not historical decision time',
              'inputs_sha256':provenance,'code_sha256':codes,'output_sha256':hashlib.sha256(payload).hexdigest(),'rows':len(table),
              'semantic_confirmed':40,'focus_confirmed':10,'focus_proposed':30,'python':platform.python_version(),'pandas':pd.__version__,
              'scope':'AI-assisted selected development record; no exhaustive annotation or independent validation'}
    if manifest_path.exists():
        saved=json.loads(manifest_path.read_text())
        if any(saved[k]!=manifest[k] for k in ['inputs_sha256','code_sha256','output_sha256']):raise FileExistsError('Snapshot provenance changed; keep old file and version the change.')
        if not snapshots.exists():raise FileNotFoundError('Manifest exists without snapshot; investigate.')
        manifest=saved
    state=write_new_or_identical(snapshots,payload)
    if not manifest_path.exists():write_new_or_identical(manifest_path,(json.dumps(manifest,indent=2)+'\n').encode())
    return table,manifest,state

if __name__=='__main__':
    table,manifest,state=build(Path(__file__).resolve().parents[1])
    print('Semantic decisions confirmed:',len(table))
    print('Focus confirmation:',table.focus_confirmation.value_counts().to_dict())
    print('Artifact status:',state,'; previous files untouched.')
