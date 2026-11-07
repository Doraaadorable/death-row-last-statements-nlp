"""Source-checked manual focus audit; not an automatic semantic validator."""
from pathlib import Path
import hashlib,json,re,platform
import pandas as pd
from claim_adjudication_v3 import FIELDS,read_table
from prepare_confirmed_claims import CORPUS_SHA256,sha,write_new_or_identical

SEMANTIC_FIELDS=list(FIELDS)

def compile_audit(records,corpus,plan):
    if len(records)!=39 or records.claim_id.duplicated().any():
        raise ValueError('Expected 39 unique previously confirmed proposition IDs.')
    if len(plan)!=39 or len({x['claim_id'] for x in plan})!=39 or set(records.claim_id)!={x['claim_id'] for x in plan}:
        raise ValueError('Audit plan and confirmed records must match one to one.')
    contexts=corpus.set_index('execution_number');lookup={x['claim_id']:x for x in plan};rows=[]
    for row in records.to_dict('records'):
        text=contexts.loc[row['execution_number'],'model_text'];start,end=int(row['span_start']),int(row['span_end'])
        if not 0<=start<end<=len(text) or text[start:end]!=row['evidence_span']:
            raise ValueError('Evidence offsets differ: '+row['claim_id'])
        if hashlib.sha256(text.encode()).hexdigest()!=row['context_sha256']:
            raise ValueError('Context differs: '+row['claim_id'])
        for field,allowed in FIELDS.items():
            if row[field] not in allowed:raise ValueError('Invalid confirmed '+field)
        item=lookup[row['claim_id']];focus=item['predicate_focus']
        matches=[m.start() for m in re.finditer(re.escape(focus),row['evidence_span'])]
        index=item['zero_based_occurrence_in_evidence']
        if index<0 or index>=len(matches):raise ValueError('Focus occurrence missing: '+row['claim_id'])
        fs=start+matches[index];fe=fs+len(focus)
        if text[fs:fe]!=focus:raise ValueError('Focus mapping differs.')
        if item['focus_provenance']=='owner_confirmed_addition':
            if int(row['focus_start'])!=fs or int(row['focus_end'])!=fe:raise ValueError('Previously confirmed focus must be retained.')
        result={key:row[key] for key in ['claim_id','execution_number','evidence_span',*SEMANTIC_FIELDS]}
        result.update(predicate_focus=focus,focus_start=fs,focus_end=fe,focus_provenance=item['focus_provenance'],audit_priority=item['review_priority'],audit_note=item['audit_note'],label_change='none_applied',audit_scope='AI_assisted_consistency_proposal_not_independent_validation')
        rows.append(result)
    return pd.DataFrame(rows)

def run(root):
    root=Path(root);base=root/'reports'
    paths=[base/'semantic_owner_decisions_v3_discussion.csv',base/'semantic_owner_additions_287_focus.csv',base/'predicate_focus_audit_plan_v1.json',root/'data/processed/model_corpus_v1.csv']
    if sha(paths[-1])!=CORPUS_SHA256:raise ValueError('Frozen corpus hash mismatch.')
    records=pd.concat([read_table(paths[0]),read_table(paths[1])],ignore_index=True).fillna('')
    corpus=read_table(paths[-1]);plan=json.loads(paths[2].read_text())
    audit=compile_audit(records,corpus,plan)
    # Exact preservation of each already confirmed semantic field.
    original=records.set_index('claim_id');result=audit.set_index('claim_id')
    pd.testing.assert_frame_equal(original.loc[result.index,SEMANTIC_FIELDS],result[SEMANTIC_FIELDS],check_dtype=False)
    summary=audit.groupby('audit_priority').size().reset_index(name='selected_propositions')
    dest=root/'results/claim_consistency_audit_v1';dest.mkdir(parents=True,exist_ok=True)
    payloads={'consistency_audit.csv':audit.to_csv(index=False).encode(),'summary.csv':summary.to_csv(index=False).encode()}
    manifest={'inputs_sha256':{str(p.relative_to(root)):sha(p) for p in paths},'code_sha256':sha(__file__),'python':platform.python_version(),'pandas':pd.__version__,'outputs_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in payloads.items()},'scope':'39 selected records structurally verified; manual AI-proposed focus mapping; no labels changed, no completeness certification, no model evaluation'}
    mp=dest/'manifest.json'
    for name,payload in payloads.items():
        if (dest/name).exists() and (dest/name).read_bytes()!=payload:raise FileExistsError('Audit output differs; use a new version.')
    if mp.exists():
        saved=json.loads(mp.read_text())
        if any(saved[k]!=manifest[k] for k in ['inputs_sha256','code_sha256','outputs_sha256']):raise FileExistsError('Audit provenance differs; preserve existing output.')
        manifest=saved
    for name,payload in payloads.items():write_new_or_identical(dest/name,payload)
    if not mp.exists():write_new_or_identical(mp,(json.dumps(manifest,indent=2)+'\n').encode())
    return audit,summary,manifest

if __name__=='__main__':
    audit,summary,_=run(Path(__file__).resolve().parents[1]);print(summary.to_string(index=False));print('Semantic label changes applied: 0')
