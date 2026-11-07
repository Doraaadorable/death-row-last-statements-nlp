"""Inspect local candidate construction on the already exposed smoke batch."""
from pathlib import Path
from collections import Counter
import json
import hashlib
import pandas as pd
from focus_candidates_v2 import candidates

def build(root):
    root=Path(root)
    corpus_path=root/'data/processed/model_corpus_v1.csv'
    smoke_path=root/'reports/sampled_focus_smoke_v1.json'
    smoke=json.loads(smoke_path.read_text())
    if hashlib.sha256(corpus_path.read_bytes()).hexdigest()!=smoke['corpus_sha256']:
        raise ValueError('Frozen corpus changed.')
    corpus=pd.read_csv(corpus_path,keep_default_na=False).set_index('execution_number')
    previous={(p['execution_number'],p['focus_start'],p['focus_end']):p for p in smoke['predictions']}
    output=[]
    for document in smoke['documents']:
        number=document['execution_number'];text=corpus.loc[number,'model_text']
        for row in candidates(text):
            key=(number,row['focus_start'],row['focus_end'])
            if key not in previous or text[row['focus_start']:row['focus_end']]!=row['predicate_focus']:
                raise ValueError('Original match inventory or exact offsets changed.')
            output.append({'execution_number':number,**row,
                'historical_B2_prediction':previous[key]['prediction'],
                'historical_B2_reason':previous[key]['reason']})
    if len(output)!=len(previous) or len(output)!=92:
        raise ValueError('All original literal matches must be retained.')
    paths=['src/focus_candidates_v2.py','src/run_candidate_structure_check_v2.py',
           'src/run_sampled_focus_smoke_v1.py','src/focus_rules_v1.py','reports/sampled_focus_smoke_v1.json']
    return {'status':'development_construction_flags_not_new_semantic_predictions',
        'counts':dict(Counter(r['disposition'] for r in output)),
        'original_abstention_dispositions':dict(Counter(r['disposition'] for r in output if r['historical_B2_prediction']=='abstain')),
        'inputs_sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},
        'rows':output,
        'limitations':['No actual dependency parsing or exhaustive predicate extraction.',
            'Linked lexical heads are proposals; some heads are outside the original lexical inventory.',
            'Flags can be wrong and are not owner-adjudicated labels.',
            'The unflagged remainder is not verified correct or in task scope.',
            'Historical predictions are copied for traceability, not recomputed or corrected.',
            'Known smoke examples informed development; no held-out improvement claimed.']}

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];result=build(root)
    output=root/'reports/candidate_structure_check_v2.json'
    payload=json.dumps(result,indent=2)+'\n'
    if output.exists() and output.read_text()!=payload:raise FileExistsError('Preserve old check; version changes.')
    if not output.exists():output.write_text(payload)
    print(json.dumps(result['counts'],indent=2))
    print('Original 30 abstentions:',json.dumps(result['original_abstention_dispositions']))
    print('92 original matches preserved. No semantic predictions changed.')
