"""Consolidation checks; no independent semantic validation."""
from pathlib import Path
import tempfile,shutil,sys,json,unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from build_confirmed_snapshot40 import build,RECORD_PATHS,FOCUS_PATH,PLAN_PATH
ROOT=Path(__file__).resolve().parents[1]
class SnapshotTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
  for rel in [*RECORD_PATHS,FOCUS_PATH,PLAN_PATH,'data/processed/model_corpus_v1.csv','reports/semantic_development_sampling_v1.json','src/claim_adjudication_v3.py','src/prepare_confirmed_claims.py','src/build_confirmed_snapshot40.py']:
   p=self.root/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,p)
 def tearDown(self):self.temp.cleanup()
 def test_exact_counts_and_repeat(self):
  a,m1,s=build(self.root);self.assertEqual(s,'created');self.assertEqual(len(a),40)
  self.assertEqual(a.focus_confirmation.value_counts().to_dict(),{'AI_proposed_not_owner_confirmed':30,'owner_confirmed':10})
  b,m2,s=build(self.root);self.assertEqual(s,'verified_existing');self.assertEqual(m1,m2);pd.testing.assert_frame_equal(a,b)
 def test_existing_local_edits_preserved(self):
  build(self.root);p=self.root/'data/processed/semantic_confirmed_snapshot40_v1.csv';p.write_text('owner edits')
  with self.assertRaises(FileExistsError):build(self.root)
  self.assertEqual(p.read_text(),'owner edits')
 def test_duplicate_addition_rejected(self):
  p=self.root/RECORD_PATHS[-1];t=pd.read_csv(p,keep_default_na=False);t.loc[0,'claim_id']='v3-dev21-001';t.to_csv(p,index=False)
  with self.assertRaises(ValueError):build(self.root)
 def test_changed_confirmed_focus_rejected(self):
  p=self.root/FOCUS_PATH;t=pd.read_csv(p,keep_default_na=False);t.loc[0,'focus_start']=0;t.to_csv(p,index=False)
  with self.assertRaises(ValueError):build(self.root)
 def test_bad_choice_evidence_rejected(self):
  p=self.root/RECORD_PATHS[-1];t=pd.read_csv(p,keep_default_na=False);t.loc[0,'span_end']=0;t.to_csv(p,index=False)
  with self.assertRaises(ValueError):build(self.root)
 def test_prior_worksheets_not_touched(self):
  p=self.root/'data/processed/semantic_development_adjudication_v2.csv';p.write_text('old owner worksheet');build(self.root)
  self.assertEqual(p.read_text(),'old owner worksheet')
if __name__=='__main__':unittest.main()
