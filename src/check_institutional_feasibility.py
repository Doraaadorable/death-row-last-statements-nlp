"""Count saved records around documented milestones; do not assign care exposure."""
from pathlib import Path
import argparse
import csv
from datetime import date
import hashlib
import json

MILESTONES = {
    'protocol_reference': '2021-04-21',
    'ramirez_decision': '2022-03-24',
}
SOURCES = [
    'https://www.govinfo.gov/content/pkg/USCOURTS-ca5-21-70004/pdf/USCOURTS-ca5-21-70004-0.pdf',
    'https://www.supremecourt.gov/opinions/21pdf/21-5592_feah.pdf',
]

def read_records(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    records = [(int(r['execution_number']), date.fromisoformat(r['index_date'])) for r in rows]
    if len({eid for eid, _ in records}) != len(records):
        raise ValueError(f'Duplicate execution IDs: {path.name}')
    return records

def period(day):
    if day < date.fromisoformat(MILESTONES['protocol_reference']):
        return 'before_2021_04_21'
    if day < date.fromisoformat(MILESTONES['ramirez_decision']):
        return '2021_04_21_through_2022_03_23'
    return 'on_or_after_2022_03_24'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    files = {'inventory': 'execution_inventory.csv', 'candidate': 'person_corpus_exploratory_v1.csv'}
    records, hashes = {}, {}
    for kind, filename in files.items():
        path = args.root / 'data/processed' / filename
        records[kind] = read_records(path)
        hashes[filename] = hashlib.sha256(path.read_bytes()).hexdigest()
    inv = dict(records['inventory'])
    if any(inv.get(eid) != day for eid, day in records['candidate']):
        raise ValueError('Candidate IDs/dates do not match inventory.')
    if len(inv) != 603 or len(records['candidate']) != 480:
        raise ValueError('Expected saved snapshot sizes: 603 inventory and 480 candidate records.')
    names = ['before_2021_04_21','2021_04_21_through_2022_03_23','on_or_after_2022_03_24']
    groups = []
    for name in names:
        ids = {kind: sorted(eid for eid, day in rows if period(day) == name) for kind, rows in records.items()}
        groups.append({'calendar_period': name, 'counts': {k: len(v) for k,v in ids.items()}, 'execution_ids': ids})
    result = {
        'purpose': 'Calendar-based source availability for an institutional-context feasibility check',
        'source_sha256': hashes, 'milestones': MILESTONES, 'milestone_sources': SOURCES,
        'snapshot_end': max(inv.values()).isoformat(),
        'interpretation': 'Dates are calendar milestones, not verified individual spiritual-care exposure.',
        'causal_status': 'No treatment/control assignment, psychological outcome or policy effect estimated.',
        'calendar_groups': groups,
    }
    content = (json.dumps(result, indent=2) + '\n').encode()
    target = args.root / 'reports/institutional_feasibility_v1.json'
    if target.exists() and target.read_bytes() != content:
        raise FileExistsError('Existing result differs; create a new version.')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    for group in groups:
        print(group['calendar_period'], group['counts'])
    print('Saved:', target)

if __name__ == '__main__':
    main()
