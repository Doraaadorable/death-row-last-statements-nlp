"""Development-only comparison on human-selected spans; not retrieval evaluation."""
from pathlib import Path
import hashlib
import json
import platform
import re
import pandas as pd
from prepare_confirmed_claims import materialize,write_new_or_identical,sha
from selected_span_rules import METHODS
from semantic_screening import PATTERNS

REQUIRED=['claim_source','event_type','event_actor','polarity','proposition_status']

def reference(row):
    if any(row[f]=='unclear' for f in REQUIRED):return 'reference_uncertain'
    if (row.claim_source=='self' and row.event_type=='killing_action' and
            row.event_actor=='self' and row.proposition_status=='presented_as_true'):
        return 'denial' if row.polarity=='negated' else 'admission'
    return 'other'

def run(root):
    root=Path(root);claims,scope,_,_=materialize(root)
    rows=[]
    for claim in claims.itertuples():
        d=claim._asdict();ref=reference(pd.Series(d));prefix=claim.model_text[:int(claim.span_start)]
        for name,rule in METHODS.items():
            pred,reason=rule(claim.evidence_span,prefix)
            outcome='reference_uncertain' if ref=='reference_uncertain' else ('abstention' if pred=='abstain' else ('match' if ref==pred else 'disagreement'))
            row={key:d[key] for key in ['claim_id','execution_number','evidence_span',*REQUIRED]}
            row.update(method=name,reference_class=ref,prediction=pred,rule_reason=reason,outcome=outcome)
            for cue,pattern in PATTERNS.items():
                row['span_'+cue]=bool(re.search(pattern,claim.evidence_span,re.I))
                row['document_'+cue]=bool(re.search(pattern,claim.model_text,re.I))
            rows.append(row)
    details=pd.DataFrame(rows)
    counts=details.groupby(['method','reference_class','prediction','outcome'],dropna=False).size().reset_index(name='selected_propositions')
    outcomes=details.groupby(['method','outcome']).size().reset_index(name='selected_propositions')
    dest=root/'results/selected_span_diagnostic_v1';dest.mkdir(parents=True,exist_ok=True)
    payloads={'claim_comparison.csv':details.to_csv(index=False).encode(),
              'reference_prediction_counts.csv':counts.to_csv(index=False).encode(),
              'outcome_counts.csv':outcomes.to_csv(index=False).encode()}
    for name,content in payloads.items():
        if (dest/name).exists() and (dest/name).read_bytes()!=content:
            raise FileExistsError('Existing diagnostic differs; use a new version before changing rules.')
    inputs={'owner_decisions':sha(root/'reports/semantic_owner_decisions_v3_discussion.csv'),
            'model_corpus':sha(root/'data/processed/model_corpus_v1.csv'),
            'protocol':sha(root/'archive/claim_syntax_experiments/SELECTED_SPAN_RULE_DIAGNOSTIC_PROTOCOL_v1.md')}
    code={name:sha(root/'src'/name) for name in ['selected_span_rules.py','run_selected_span_diagnostic.py','semantic_screening.py','prepare_confirmed_claims.py','claim_adjudication_v3.py']}
    manifest={'inputs_sha256':inputs,'code_sha256':code,'output_sha256':{k:hashlib.sha256(v).hexdigest() for k,v in payloads.items()},
              'python':platform.python_version(),'pandas':pd.__version__,
              'unit':'human-selected evidence span with context; selection is an oracle advantage',
              'scope':'Known-example-informed development diagnostic, not unseen evaluation or corpus retrieval recall',
              'propositions':len(claims),'reference_counts':claims.apply(reference,axis=1).value_counts().to_dict()}
    mp=dest/'manifest.json'
    if mp.exists():
        old=json.loads(mp.read_text())
        if any(old[k]!=manifest[k] for k in ['inputs_sha256','code_sha256','output_sha256']):raise FileExistsError('Existing diagnostic provenance differs; preserve old outputs.')
        manifest=old
    for name,content in payloads.items():write_new_or_identical(dest/name,content)
    if not mp.exists():write_new_or_identical(mp,(json.dumps(manifest,indent=2)+'\n').encode())
    return details,counts,outcomes,manifest

if __name__=='__main__':
    detail,counts,outcomes,manifest=run(Path(__file__).resolve().parents[1])
    print('Selected development propositions:',manifest['propositions'])
    print('Reference counts:',manifest['reference_counts'])
    print(outcomes.to_string(index=False))
    print('No accuracy/F1 or population recall is estimated.')
