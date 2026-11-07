"""Parse the existing exposed sample; retain outputs separately from B2."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,platform
from syntactic_candidates_v1 import extract

def save_new_or_identical(path,payload):
    if path.exists() and path.read_bytes()!=payload:
        raise FileExistsError('Changed output: preserve and version '+str(path))
    path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():path.write_bytes(payload)

def build(root):
    import spacy
    root=Path(root);nlp=spacy.load('en_core_web_sm',disable=['ner'])
    smoke_path=root/'reports/sampled_focus_smoke_v1.json'
    smoke=json.loads(smoke_path.read_text());corpus_path=root/'data/processed/model_corpus_v1.csv'
    if hashlib.sha256(corpus_path.read_bytes()).hexdigest()!=smoke['corpus_sha256']:
        raise ValueError('Frozen corpus differs.')
    with corpus_path.open(newline='',encoding='utf-8-sig') as stream:
        corpus={int(r['execution_number']):r for r in csv.DictReader(stream)}
    documents=[]
    for item in smoke['documents']:
        number=item['execution_number'];text=corpus[number]['model_text'];doc=nlp(text)
        if doc.text!=text:raise ValueError('Source text changed during parsing.')
        rows=extract(doc)
        for row in rows:
            focus=row['focus']
            if text[focus['start']:focus['end']]!=focus['text']:raise ValueError('Focus offset mismatch.')
        documents.append({'execution_number':number,'stratum':item['stratum'],
            'source_url':item['source_url'],'context_sha256':item['context_sha256'],
            'predicate_candidates':rows})
    # Model contents fingerprint includes the trained parser and tokenizer data.
    model_digest=hashlib.sha256(nlp.to_bytes()).hexdigest()
    provenance={'spacy':spacy.__version__,'model':nlp.meta['name'],'model_version':nlp.meta['version'],
        'active_pipeline':nlp.pipe_names,'loaded_pipeline_sha256':model_digest,'python':platform.python_version(),
        'inputs_sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ['src/syntactic_candidates_v1.py','src/run_syntactic_candidates_v1.py','reports/sampled_focus_smoke_v1.json']},
        'corpus_sha256':smoke['corpus_sha256']}
    full={'status':'parser_proposals_only_not_adjudicated_not_B2_predictions','provenance':provenance,'documents':documents}
    payload=(json.dumps(full,indent=2)+'\n').encode()
    fullpath=root/'data/processed/syntactic_candidates_v1.json'
    save_new_or_identical(fullpath,payload)
    kinds=Counter(p['kind'] for d in documents for p in d['predicate_candidates'])
    summary={'status':full['status'],'provenance':provenance,'local_output':'data/processed/syntactic_candidates_v1.json',
        'local_output_sha256':hashlib.sha256(payload).hexdigest(),'candidate_kind_counts':dict(kinds),
        'document_counts':[{'execution_number':d['execution_number'],'stratum':d['stratum'],'parser_candidates':len(d['predicate_candidates'])} for d in documents],
        'limitations':['Parser predictions can be wrong on transcription, religious and figurative language.',
            'No scope filtering, coreference resolution, five-field labels or classification scores.',
            'Subject/object heads are syntactic evidence, not semantic agent or source labels.',
            'No automatic expansion of relative clauses or omitted shared subjects.',
            'More candidates than a literal adapter does not establish improved extraction recall.']}
    save_new_or_identical(root/'data/processed/syntactic_candidates_summary_v1.json',(json.dumps(summary,indent=2)+'\n').encode())
    return summary

if __name__=='__main__':
    result=build(Path(__file__).resolve().parents[1])
    print('Documents:',len(result['document_counts']))
    print(json.dumps(result['candidate_kind_counts'],indent=2))
    print('Parser proposals only. Scope and semantic fields remain unassigned.')
