"""Metadata-only readiness accounting; never draws a new sample or prints text."""
from pathlib import Path
import hashlib
import json
import re
import pandas as pd
from semantic_screening import screen_documents

SOURCES = {
    'original_annotation_development': 'data/processed/annotation_development_v2.csv',
    'semantic_development_selection': 'reports/semantic_development_sampling_v1.json',
    'semantic_pilot': 'reports/semantic_pilot_decisions_v1.csv',
    'documented_component_reading': 'docs/COMPONENT_REVIEW_k4_k6_k8.md',
}
# Supplementary IDs with statements visibly discussed in the project conversation.
# This is an incomplete reconstructed record, not a complete browsing history.
CONVERSATION_IDS = [49, 82, 425, 192, 83, 238, 117, 391, 499, 235, 480,
                    182, 318, 487, 367, 152]

def component_ids(text):
    label = r'(?:documents examined(?: under each (?:reference )?fit)?|execution IDs were):?\s*'
    matches = re.findall(label + r'([0-9][0-9,\s]*(?:and\s+\d+)?)', text, flags=re.I)
    if not matches:
        raise ValueError('Component review ID lists were not found.')
    return {int(n) for match in matches for n in re.findall(r'\d+', match)}

def build(root):
    root = Path(root)
    corpus_path = root / 'data/processed/model_corpus_v1.csv'
    corpus = pd.read_csv(corpus_path, keep_default_na=False)
    if len(corpus) != 480 or not corpus.execution_number.is_unique:
        raise ValueError('Unexpected frozen candidate corpus.')
    prepared = corpus.loc[corpus.preparation_status.eq('ready_for_exploration')]
    if len(prepared) != 479:
        raise ValueError('Unexpected prepared corpus.')
    sources = {
        'original_annotation_development': set(pd.read_csv(root / SOURCES['original_annotation_development']).execution_number.astype(int)),
        'semantic_development_selection': set(json.loads((root / SOURCES['semantic_development_selection']).read_text())['execution_ids_in_display_order']),
        'semantic_pilot': set(pd.read_csv(root / SOURCES['semantic_pilot']).execution_number.astype(int)),
        'documented_component_reading': component_ids((root / SOURCES['documented_component_reading']).read_text()),
        'conversation_supplement_reconstructed': set(CONVERSATION_IDS),
    }
    if len(sources['original_annotation_development']) != 50 or len(sources['semantic_development_selection']) != 21 or len(sources['semantic_pilot']) != 3:
        raise ValueError('Unexpected development source counts.')
    known = set.union(*sources.values())
    if not known.issubset(set(corpus.execution_number)):
        raise ValueError('Exposure ID outside supplied corpus.')
    screen = screen_documents(prepared)
    screen['exposure'] = screen.execution_number.map(lambda n: 'documented_prior_exposure' if n in known else 'exposure_unknown')
    summary = []
    for candidate in [True, False]:
        for exposure in ['documented_prior_exposure', 'exposure_unknown']:
            group = screen.loc[screen.candidate_document.eq(candidate) & screen.exposure.eq(exposure)]
            summary.append({'cue_stratum': 'candidate' if candidate else 'nonmatch', 'exposure': exposure,
                            'documents': len(group), 'execution_ids': sorted(group.execution_number.astype(int).tolist())})
    hashes = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in [*SOURCES.values(), 'data/processed/model_corpus_v1.csv', 'src/semantic_screening.py', 'src/build_evaluation_exposure_v1.py']}
    return {'status': 'readiness_only_no_new_sample', 'prepared_documents': 479,
            'source_ids': {k: sorted(v) for k, v in sources.items()},
            'sources_sha256': hashes, 'strata': summary,
            'limitations': ['Exposure sources overlap; source counts are not additive.',
                'The conversation supplement is reconstructed and incomplete.',
                'Absence of recorded exposure is unknown, never proven unseen.',
                'Prior NMF fitting used the prepared corpus except zero-feature records; it was not target-task evaluation.',
                'No document text, new predictions, reference labels or random sample is generated.']}

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    result = build(root)
    output = root / 'reports/evaluation_exposure_readiness_v1.json'
    payload = json.dumps(result, indent=2) + '\n'
    if output.exists() and output.read_text() != payload:
        raise FileExistsError('Changed readiness record: preserve old output and version changes.')
    if not output.exists():
        output.write_text(payload)
    for group in result['strata']:
        print(group['cue_stratum'], group['exposure'], group['documents'])
    print('No new sample drawn; no statement text displayed.')
