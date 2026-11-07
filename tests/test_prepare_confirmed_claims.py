"""Evidence/provenance regression checks, not semantic accuracy estimates."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from prepare_confirmed_claims import materialize, validate_records

ROOT=Path(__file__).resolve().parents[1]
class ConfirmedPreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        for rel in ['data/processed/model_corpus_v1.csv','reports/semantic_owner_decisions_v3_discussion.csv','reports/semantic_development_sampling_v1.json','src/claim_adjudication_v3.py']:
            dest=self.root/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dest)
    def tearDown(self):self.temp.cleanup()
    def test_repeat_is_identical_and_keeps_old_worksheet(self):
        old=self.root/'data/processed/semantic_development_adjudication_v2.csv';old.write_text('owner edits remain')
        a,scope,m1,status=materialize(self.root);self.assertEqual(status,'created');self.assertEqual(len(a),37)
        self.assertEqual(a.execution_number.nunique(),19);self.assertEqual(len(scope),21)
        b,_,m2,status=materialize(self.root);self.assertEqual(status,'verified_existing');self.assertEqual(m1,m2)
        self.assertEqual(old.read_text(),'owner edits remain')
    def test_local_changes_blocked_without_overwrite(self):
        materialize(self.root);p=self.root/'data/processed/semantic_owner_confirmed_v3_37.csv';p.write_text('local edit');before=p.read_bytes()
        with self.assertRaises(FileExistsError):materialize(self.root)
        self.assertEqual(p.read_bytes(),before)
    def test_tampered_evidence_rejected(self):
        p=self.root/'reports/semantic_owner_decisions_v3_discussion.csv';t=pd.read_csv(p,keep_default_na=False);t.loc[0,'evidence_span']='altered';t.to_csv(p,index=False)
        with self.assertRaises(ValueError):materialize(self.root)
        self.assertFalse((self.root/'data/processed/semantic_owner_confirmed_v3_37.csv').exists())
    def test_duplicate_id_and_bad_values_rejected(self):
        p=self.root/'reports/semantic_owner_decisions_v3_discussion.csv';t=pd.read_csv(p,keep_default_na=False);original=t.copy();t.loc[1,'claim_id']=t.loc[0,'claim_id'];t.to_csv(p,index=False)
        with self.assertRaises(ValueError):materialize(self.root)
        original.loc[0,'proposition_status']='presupposed';original.to_csv(p,index=False)
        with self.assertRaises(ValueError):materialize(self.root)
    def test_historical_timestamp_not_invented(self):
        p=self.root/'reports/semantic_owner_decisions_v3_discussion.csv';t=pd.read_csv(p,keep_default_na=False);t.loc[0,'message_timestamp']='2026-11-06T12:00:00-05:00';t.to_csv(p,index=False)
        with self.assertRaises(ValueError):materialize(self.root)
if __name__=='__main__':unittest.main()
