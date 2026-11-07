"""Known-development alignment and field comparison, not held-out accuracy."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json
from syntactic_candidates_v1 import extract
from syntax_semantics_v1 import propose

FIELDS=['claim_source','event_type','event_actor','polarity','proposition_status']
INPUTS=['reports/semantic_confirmed_snapshot40_v1.csv','reports/semantic_owner_additions_9_shooting_naming.csv']

def load_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as stream:return list(csv.DictReader(stream))

def field_relation(reference,automatic):
    if reference==automatic:return 'same_value'
    if automatic=='unclear':return 'automatic_unclear'
    if reference=='unclear':return 'reference_unclear'
    return 'definite_value_conflict'

def exact_alignment(rows,start,end):
    found=[r for r in rows if r['focus']['start']==start and r['focus']['end']==end]
    if len(found)>1:raise ValueError('Duplicate parser focus intervals.')
    return found[0] if found else None

def save(path,payload):
    if path.exists() and path.read_bytes()!=payload:raise FileExistsError('Preserve old output; version changes: '+str(path))
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():path.write_bytes(payload)

def build(root):
    import spacy
    root=Path(root);refs=[r for p in INPUTS for r in load_csv(root/p)]
    if len(refs)!=42 or len({r['claim_id'] for r in refs})!=42:raise ValueError('Expected 42 unique known selections.')
    corpus={int(r['execution_number']):r for r in load_csv(root/'data/processed/model_corpus_v1.csv')}
    scope_path=root/'reports/semantic_scope_audit_v1.json'
    scope={r['claim_id']:r['scope_status'] for r in json.loads(scope_path.read_text())['decisions']}
    nlp=spacy.load('en_core_web_sm',disable=['ner']);cache={};comparisons=[]
    for ref in refs:
        number=int(ref['execution_number']);text=corpus[number]['model_text'];a,b=int(ref['focus_start']),int(ref['focus_end'])
        if text[a:b]!=ref['predicate_focus'] or hashlib.sha256(text.encode()).hexdigest()!=ref['context_sha256']:
            raise ValueError('Source/focus differs: '+ref['claim_id'])
        if ref['owner_decision']!='accept':raise ValueError('Unexpected unaccepted semantic record.')
        if number not in cache:cache[number]=extract(nlp(text))
        parser_rows=cache[number];row=exact_alignment(parser_rows,a,b)
        result={'claim_id':ref['claim_id'],'execution_number':number,'predicate_focus':ref['predicate_focus'],
            'focus_start':a,'focus_end':b,'focus_confirmation':ref.get('focus_confirmation') or 'owner_confirmed',
            'scope_status':scope[ref['claim_id']],'reference_fields':{f:ref[f] for f in FIELDS}}
        if row is None:
            nearby=[r['focus'] for r in parser_rows if a<=r['focus']['start'] and r['focus']['end']<=b]
            result.update(alignment='no_exact_predicate_alignment',contained_parser_heads=nearby,
                          comparison_status='not_compared_no_forced_alignment')
        else:
            automatic=propose(row,text,{r['focus']['start']:r for r in parser_rows})
            result.update(alignment='exact_offsets',automatic_proposal=automatic,
                          field_relations={f:field_relation(ref[f],automatic['proposed_fields'][f]) for f in FIELDS})
        comparisons.append(result)
    aligned=[r for r in comparisons if r['alignment']=='exact_offsets']
    summary={'status':'known_development_comparison_not_independent_accuracy','reference_selections':42,
        'reference_documents':len(cache),'alignment_counts':dict(Counter(r['alignment'] for r in comparisons)),
        'aligned_focus_confirmation':dict(Counter(r['focus_confirmation'] for r in aligned)),
        'aligned_scope_status':dict(Counter(r['scope_status'] for r in aligned)),
        'field_relations_all_exact':{f:dict(Counter(r['field_relations'][f] for r in aligned)) for f in FIELDS},
        'field_relations_owner_confirmed_focus':{f:dict(Counter(r['field_relations'][f] for r in aligned if r['focus_confirmation']=='owner_confirmed')) for f in FIELDS},
        'model':{'spacy':spacy.__version__,'name':nlp.meta['name'],'version':nlp.meta['version'],'loaded_pipeline_sha256':hashlib.sha256(nlp.to_bytes()).hexdigest()},
        'inputs_sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in [*INPUTS,'reports/semantic_scope_audit_v1.json','data/processed/model_corpus_v1.csv','src/compare_confirmed_syntax_v1.py','src/syntactic_candidates_v1.py','src/syntax_semantics_v1.py']},
        'limitations':['References were confirmed after AI-assisted discussion and informed method development.',
            '30 of the 42 historical focus positions remain AI-proposed, not independently confirmed.',
            'Exact alignment can fail for nominal or multiword reference foci; no forced nearest match.',
            'Field conflict does not by itself identify parser error, rule gap or genuine ambiguity.',
            'Same unclear values are counted as same_value, not successful substantive interpretation.',
            'Task-scope statuses and retired representations are retained rather than silently filtered.']}
    result={'summary':summary,'comparisons':comparisons}
    save(root/'data/processed/confirmed_syntax_comparison_v1.json',(json.dumps(result,indent=2)+'\n').encode())
    save(root/'data/processed/confirmed_syntax_comparison_summary_v1.json',(json.dumps(summary,indent=2)+'\n').encode())
    return result

if __name__=='__main__':
    result=build(Path(__file__).resolve().parents[1])
    print(json.dumps(result['summary']['alignment_counts'],indent=2))
    print(json.dumps(result['summary']['field_relations_all_exact'],indent=2))
    print('Development comparison only. No references, parser rules or historical results changed.')
