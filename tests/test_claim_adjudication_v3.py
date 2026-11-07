"""Regression checks for owner edit safety; not semantic accuracy tests."""
import sys
from pathlib import Path
import tempfile
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from claim_adjudication_v3 import load_or_create, validate_decisions, export_review, OWNER

class OwnerReviewTests(unittest.TestCase):
    def setUp(self):
        self.proposals=pd.DataFrame([{'claim_id':'a','proposed_claim_source':'self','proposed_event_type':'knowledge','proposed_event_actor':'self','proposed_polarity':'negated','proposed_proposition_status':'presented_as_true'}, {'claim_id':'b','proposed_claim_source':'other','proposed_event_type':'killing_action','proposed_event_actor':'self','proposed_polarity':'negated','proposed_proposition_status':'presented_as_true'}])
        self.table=self.proposals.copy()
        for f in OWNER:self.table[f]=''
    def decision(self,value):
        t=self.table.copy();t.loc[0,['owner_decision','reviewer_id','reviewed_at']]=[value,'owner','2026-11-06T12:00:00-05:00'];return t
    def test_sorted_owner_bom_edit_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'worksheet.csv';t=self.decision('accept').iloc[::-1];t.to_csv(p,index=False,encoding='utf-8-sig');before=p.read_bytes()
            out=load_or_create(self.proposals,p)
            self.assertEqual(out.iloc[0].owner_decision,'accept');self.assertEqual(before,p.read_bytes())
    def test_bad_values_rejected(self):
        for val in ['accpt',' Accept ']:
            with self.assertRaises(ValueError):validate_decisions(self.decision(val))
        t=self.decision('accept');t.loc[0,'owner_event_actor']='myself'
        with self.assertRaises(ValueError):validate_decisions(t)
    def test_revise_requires_fields_note_and_change(self):
        with self.assertRaises(ValueError):validate_decisions(self.decision('revise'))
        t=self.decision('revise');t.loc[0,'owner_note']='Correction'
        for f in ['claim_source','event_type','event_actor','polarity','proposition_status']:t.loc[0,'owner_'+f]=t.loc[0,'proposed_'+f]
        with self.assertRaises(ValueError):validate_decisions(t)
        t.loc[0,'owner_event_type']='other';validate_decisions(t)
    def test_conflict_and_missing_identity_rejected(self):
        t=self.decision('accept');t.loc[0,'owner_polarity']='affirmed'
        with self.assertRaises(ValueError):validate_decisions(t)
        t=self.decision('accept');t.loc[0,'reviewer_id']=''
        with self.assertRaises(ValueError):validate_decisions(t)
    def test_presupposed_is_note_not_status_value(self):
        t=self.decision('revise');t.loc[0,'owner_note']='Test old category'
        for f in ['claim_source','event_type','event_actor','polarity','proposition_status']:t.loc[0,'owner_'+f]=t.loc[0,'proposed_'+f]
        t.loc[0,'owner_proposition_status']='presupposed'
        with self.assertRaises(ValueError):validate_decisions(t)
    def test_pending_blocks_export_validation(self):
        with self.assertRaises(ValueError):validate_decisions(self.table,complete=True)
    def test_export_writes_once_and_hashes_payload(self):
        import json, hashlib
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for folder in ['reports','data/processed','docs']:(root/folder).mkdir(parents=True)
            q=self.proposals.copy();q['execution_number']=[1,2]
            t=q.copy()
            for f in OWNER:t[f]=''
            t['owner_decision']='accept';t['reviewer_id']='owner';t['reviewed_at']='2026-11-06T12:00:00-05:00'
            wp=root/'worksheet.csv';t.to_csv(wp,index=False)
            docs=pd.DataFrame({'execution_number':[1,2],'owner_document_decision':['reviewed_selected']*2,'owner_note':['Selected material checked']*2,'reviewer_id':['owner']*2,'reviewed_at':['2026-11-06T12:00:00-05:00']*2})
            dp=root/'documents.csv';docs.to_csv(dp,index=False)
            docs[['execution_number']].to_csv(root/'reports/semantic_development_document_coverage_v1.csv',index=False)
            (root/'data/processed/model_corpus_v1.csv').write_text('test source')
            (root/'docs/SEMANTIC_CLAIM_GUIDELINE_v3_DRAFT.md').write_text('test guideline')
            dest=export_review(root,q,wp,dp,'test')
            manifest=json.loads((dest/'manifest.json').read_text())
            for name in ['all_decisions.csv','adjudicated_propositions.csv','document_decisions.csv']:
                self.assertEqual(hashlib.sha256((dest/name).read_bytes()).hexdigest(),manifest['hashes'][name])
            with self.assertRaises(FileExistsError):export_review(root,q,wp,dp,'test')
    def test_changed_source_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'worksheet.csv';self.table.to_csv(p,index=False);before=p.read_bytes();q=self.proposals.copy();q.loc[0,'proposed_polarity']='affirmed'
            with self.assertRaises(AssertionError):load_or_create(q,p)
            self.assertEqual(before,p.read_bytes())
if __name__=='__main__':unittest.main()
