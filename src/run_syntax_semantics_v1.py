"""Apply partial semantic conversion to the existing parser proposals."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json
from syntax_semantics_v1 import propose

def save(path,payload):
    if path.exists() and path.read_bytes()!=payload:raise FileExistsError('Preserve old output and version changes: '+str(path))
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():path.write_bytes(payload)

def build(root):
    root=Path(root);parser_path=root/'data/processed/syntactic_candidates_v1.json'
    parsed=json.loads(parser_path.read_text());corpus_path=root/'data/processed/model_corpus_v1.csv'
    if hashlib.sha256(corpus_path.read_bytes()).hexdigest()!=parsed['provenance']['corpus_sha256']:raise ValueError('Corpus differs.')
    with corpus_path.open(encoding='utf-8-sig',newline='') as stream:corpus={int(r['execution_number']):r['model_text'] for r in csv.DictReader(stream)}
    outputs=[]
    for document in parsed['documents']:
        rows=document['predicate_candidates'];by_start={r['focus']['start']:r for r in rows};text=corpus[document['execution_number']]
        for row in rows:
            focus=row['focus']
            if text[focus['start']:focus['end']]!=focus['text']:raise ValueError('Source offset differs.')
            outputs.append({'execution_number':document['execution_number'],'focus':focus,**propose(row,text,by_start)})
    result={'status':'partial_automatic_semantic_proposals_not_reference_labels','rows':outputs,
        'inputs_sha256':{'data/processed/syntactic_candidates_v1.json':hashlib.sha256(parser_path.read_bytes()).hexdigest(),
            **{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ['src/syntax_semantics_v1.py','src/run_syntax_semantics_v1.py']}},
        'parser_provenance':parsed['provenance']}
    payload=(json.dumps(result,indent=2)+'\n').encode();save(root/'data/processed/syntax_semantics_v1.json',payload)
    summary={'status':result['status'],'rows':len(outputs),'target_prediction_counts':dict(Counter(r['target_prediction'] for r in outputs)),
        'field_value_counts':{f:dict(Counter(r['proposed_fields'][f] for r in outputs)) for f in ['claim_source','event_type','event_actor','polarity','proposition_status']},
        'output_sha256':hashlib.sha256(payload).hexdigest(),'inputs_sha256':result['inputs_sha256'],
        'limitations':['Scope remains unassigned; broad inventory contains many out-of-scope predicates.',
            'Fields are partial heuristic proposals inherited from fallible parser output.',
            'Root predicates are heuristically treated as speaker-presented declarations when conditions allow; no discourse-level verification.',
            'No general modality, coreference, quotation, factivity, negation-scope or ellipsis resolution.',
            'Counts cannot be compared to B2 as accuracy improvement; units differ and no independent reference exists.']}
    save(root/'data/processed/syntax_semantics_summary_v1.json',(json.dumps(summary,indent=2)+'\n').encode())
    return summary

if __name__=='__main__':
    result=build(Path(__file__).resolve().parents[1]);print(json.dumps(result['target_prediction_counts'],indent=2))
    print('Partial automatic proposals only. No owner labels or B2 results changed.')
