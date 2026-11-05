"""Record supported inclusion evidence without reconstructing missing decisions."""
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
base = ROOT / 'data/processed'
inventory = pd.read_csv(base/'execution_inventory.csv',keep_default_na=False)
corpus = pd.read_csv(base/'person_corpus_exploratory_v1.csv',keep_default_na=False)
if not inventory.execution_number.is_unique or not corpus.execution_number.is_unique:
    raise ValueError('Duplicate execution IDs')
if not set(corpus.execution_number).issubset(set(inventory.execution_number)):
    raise ValueError('Corpus contains records outside inventory')
rows=[]
for _,r in inventory.iterrows():
    included = r.execution_number in set(corpus.execution_number)
    shared = r.link_type == 'shared_notice_page'
    rows.append({'execution_number':r.execution_number,
        'inclusion_status':'included' if included else ('excluded' if shared else 'unknown'),
        'present_in_candidate_corpus':included,
        'exclusion_reason':'' if included else ('shared_notice_link' if shared else ''),
        'reason_evidence':('data/processed/person_corpus_exploratory_v1.csv:execution_number' if included else
                           'data/processed/execution_inventory.csv:link_type' if shared else ''),
        'evidence_limit':'' if included else ('Link category only; page content was not re-audited.' if shared else
                                             'Absent from candidate corpus; upstream decision evidence unavailable in snapshot.')})
out=ROOT/'reports/inclusion_ledger_v1.csv'
out.parent.mkdir(exist_ok=True)
pd.DataFrame(rows).to_csv(out,index=False)
print(pd.DataFrame(rows).inclusion_status.value_counts().to_string())
