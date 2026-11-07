"""Describe frozen development labels without changing them or estimating prevalence."""
from pathlib import Path
import argparse
import csv
import hashlib
import itertools
import json

LABELS = (
    'relational_affection', 'gratitude', 'faith_spirituality',
    'apology_forgiveness', 'harm_acknowledgment', 'innocence_dispute',
    'justice_criticism', 'farewell_readiness',
)

def summarize(source):
    payload = source.read_bytes()
    with source.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    ids = [int(row['execution_number']) for row in rows]
    if len(rows) != 50 or len(set(ids)) != 50:
        raise ValueError('Expected 50 unique frozen development records.')
    for row in rows:
        for label in LABELS:
            if row[label] not in {'0', '1', 'u'}:
                raise ValueError(f'Invalid frozen value: {label}')
    counts = {
        label: {value: sum(row[label] == value for row in rows) for value in ('1', '0', 'u')}
        for label in LABELS
    }
    pairs = []
    for left, right in itertools.combinations(LABELS, 2):
        groups = {key: [] for key in ('11', '10', '01', '00', 'unresolved')}
        for row in rows:
            a, b = row[left], row[right]
            key = 'unresolved' if 'u' in (a, b) else a + b
            groups[key].append(int(row['execution_number']))
        pairs.append({
            'left': left, 'right': right, 'denominator': len(rows),
            'counts': {key: len(value) for key, value in groups.items()},
            'execution_ids': {key: sorted(value) for key, value in groups.items()},
        })
    return {
        'analysis': 'Frozen equal-decade development sample: descriptive expression counts',
        'source': 'data/processed/annotation_development_v2.csv',
        'source_sha256': hashlib.sha256(payload).hexdigest(),
        'documents': len(rows),
        'scope': 'Development sample only; no population prevalence or inferential tests.',
        'definitions': {
            '1': 'Present in the frozen coding', '0': 'Absent in the frozen coding',
            'u': 'Unresolved in the frozen coding',
            'pair_order': 'First value is left label; second is right label.',
            'unresolved_pair': 'At least one label is u; retained in denominator.',
            'interpretation': 'Co-presence does not establish shared addressee, motive or conflict.',
        },
        'label_counts': counts, 'all_label_pairs': pairs,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    source = args.root / 'data/processed/annotation_development_v2.csv'
    result = summarize(source)
    content = (json.dumps(result, indent=2, ensure_ascii=False) + '\n').encode()
    target = args.root / 'reports/expression_sample_descriptive_v1.json'
    if target.exists() and target.read_bytes() != content:
        raise FileExistsError('Existing output differs; use a new analysis version.')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    print(f'Verified {result["documents"]} records, {len(LABELS)} labels and 28 pairs.')
    print(f'Saved: {target}')

if __name__ == '__main__':
    main()
