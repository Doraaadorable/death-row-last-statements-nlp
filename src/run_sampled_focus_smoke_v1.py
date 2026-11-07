"""Draw the frozen 20-document batch and apply unchanged B2 to literal foci.

Automatic smoke test only: no independent references or performance estimates.
The literal focus inventory is not exhaustive predicate or scope annotation.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import platform
import random
import re
import pandas as pd
from focus_rules_v1 import predict

FOCI = re.compile(
    r'\btake\s+the\s+full\s+blame\b|\b(?:was|am|is|were|are)\s+responsible\b|'
    r'\b(?:kill|kills|killed|killing|murder|murders|murdered|murdering|'
    r'execute|executes|executed|executing|take|takes|took|taking|taken|'
    r'know|knows|knew|known|understand|understands|understood|'
    r'think|thinks|thought|believe|believes|believed|'
    r'say|says|said|tell|tells|told|call|calls|called|'
    r'shot|shoot|shoots|hurt|hurts|harmed|harm|'
    r'commit|committed|chose|choose|happened|happen|did|do|does)\b', re.I)

def literal_foci(text):
    # Deliberately lexical. Auxiliaries and out-of-scope mentions can be returned;
    # this does not implement the human predicate-inventory protocol.
    return [(m.start(), m.end(), m.group()) for m in FOCI.finditer(text)]

def build(root):
    root = Path(root)
    readiness_path = root / 'reports/evaluation_exposure_readiness_v1.json'
    readiness = json.loads(readiness_path.read_text())
    for path, digest in readiness['sources_sha256'].items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != digest:
            raise ValueError('Readiness source changed: ' + path)
    pools = {g['cue_stratum']: g['execution_ids'] for g in readiness['strata'] if g['exposure'] == 'exposure_unknown'}
    if len(pools['candidate']) != 92 or len(pools['nonmatch']) != 271:
        raise ValueError('Frozen sampling pools changed.')
    rng = random.Random(20261107)
    sample = {s: sorted(rng.sample(sorted(pools[s]), 10)) for s in ['candidate', 'nonmatch']}
    corpus_path = root / 'data/processed/model_corpus_v1.csv'
    corpus = pd.read_csv(corpus_path, keep_default_na=False).set_index('execution_number')
    documents, predictions = [], []
    for stratum, ids in sample.items():
        for number in ids:
            text = corpus.loc[number, 'model_text']
            foci = literal_foci(text)
            documents.append({'execution_number': number, 'stratum': stratum,
                              'source_url': corpus.loc[number, 'source_url'],
                              'literal_focus_count': len(foci),
                              'context_sha256': hashlib.sha256(text.encode()).hexdigest(),
                              'exposure_before_run': 'unknown',
                              'exposure_after_run': 'automated_focus_smoke_material_not_reserved_blind_batch'})
            for start, end, focus in foci:
                label, reason = predict(text, start, end)
                predictions.append({'execution_number': number, 'stratum': stratum,
                    'focus_start': start, 'focus_end': end, 'predicate_focus': focus,
                    'prediction': label, 'reason': reason})
    assert len(documents) == 20 and len({d['execution_number'] for d in documents}) == 20
    summary = {}
    for stratum in sample:
        subset = [p for p in predictions if p['stratum'] == stratum]
        summary[stratum] = {'documents': 10, 'literal_foci': len(subset),
            'zero_focus_documents': sum(d['literal_focus_count'] == 0 for d in documents if d['stratum'] == stratum),
            'prediction_counts': dict(Counter(p['prediction'] for p in subset))}
    paths = ['src/focus_rules_v1.py', 'src/run_sampled_focus_smoke_v1.py',
             'reports/evaluation_exposure_readiness_v1.json', 'docs/SAMPLED_FOCUS_SMOKE_PROTOCOL_v1.md']
    return {'status': 'automatic_smoke_only_no_reference_labels', 'seed': 20261107,
            'sampling': sample, 'pool_sizes': {'candidate':92,'nonmatch':271},
            'conditional_inclusion_probabilities': {'candidate':10/92,'nonmatch':10/271},
            'python': platform.python_version(), 'pandas': pd.__version__,
            'inputs_sha256': {p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},
            'corpus_sha256': hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
            'documents': documents, 'predictions': predictions, 'summary': summary,
            'limitations': ['No accuracy, precision, recall or semantic ground truth.',
                'Literal foci are not exhaustive, owner-confirmed or scope-filtered predicates.',
                'B2 is unchanged; automatic focus supply differs from its intended human-focus task.',
                'This batch replaces the planned blind-reference use at owner request; reserve fresh documents for any later blind evaluation.',
                'Zero retrieved foci do not imply no eligible proposition.']}

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    result = build(root)
    output = root / 'reports/sampled_focus_smoke_v1.json'
    payload = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
    if output.exists() and output.read_text() != payload:
        raise FileExistsError('Preserve the previous run; version changed outputs.')
    if not output.exists():
        output.write_text(payload)
    print(json.dumps(result['sampling'], indent=2))
    print(json.dumps(result['summary'], indent=2))
    print('Automatic smoke test only. No performance metric computed.')
