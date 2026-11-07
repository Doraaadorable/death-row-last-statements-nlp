"""Structural audit regression tests, not semantic agreement tests."""
from pathlib import Path
import sys,json,unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from audit_claim_consistency import compile_audit,SEMANTIC_FIELDS
from claim_adjudication_v3 import read_table
ROOT=Path(__file__).resolve().parents[1]
class AuditTests(unittest.TestCase):
    def setUp(self):
        self.rows=pd.concat([read_table(ROOT/'reports/semantic_owner_decisions_v3_discussion.csv'),read_table(ROOT/'reports/semantic_owner_additions_287_focus.csv')],ignore_index=True).fillna('')
        self.corpus=read_table(ROOT/'data/processed/model_corpus_v1.csv')
        self.plan=json.loads((ROOT/'reports/predicate_focus_audit_plan_v1.json').read_text())
    def test_labels_and_inputs_preserved(self):
        before=self.rows.copy(deep=True);out=compile_audit(self.rows,self.corpus,self.plan)
        self.assertEqual(len(out),39);self.assertTrue(out.label_change.eq('none_applied').all())
        pd.testing.assert_frame_equal(self.rows,before)
        for f in SEMANTIC_FIELDS:self.assertEqual(out[f].tolist(),before[f].tolist())
    def test_duplicate_id_rejected(self):
        self.rows.loc[1,'claim_id']=self.rows.loc[0,'claim_id']
        with self.assertRaises(ValueError):compile_audit(self.rows,self.corpus,self.plan)
    def test_bad_focus_occurrence_rejected(self):
        self.plan[0]['zero_based_occurrence_in_evidence']=99
        with self.assertRaises(ValueError):compile_audit(self.rows,self.corpus,self.plan)
    def test_altered_context_rejected(self):
        self.corpus.loc[self.corpus.execution_number.eq(147),'model_text']='altered'
        with self.assertRaises(ValueError):compile_audit(self.rows,self.corpus,self.plan)
    def test_repeated_focus_uses_declared_occurrence(self):
        out=compile_audit(self.rows,self.corpus,self.plan).set_index('claim_id')
        row=out.loc['v3-added-002'];original=self.rows.set_index('claim_id').loc['v3-added-002']
        self.assertEqual(row.focus_start,int(original.span_start)+original.evidence_span.rindex('did'))
        row=out.loc['v3-dev21-014'];original=self.rows.set_index('claim_id').loc['v3-dev21-014']
        self.assertEqual(row.focus_start,int(original.span_start)+original.evidence_span.index('shot'))
if __name__=='__main__':unittest.main()
