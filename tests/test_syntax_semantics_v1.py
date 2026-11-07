"""Development behavior checks; require the optional syntax environment."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from syntactic_candidates_v1 import extract
from syntax_semantics_v1 import propose

class SemanticBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import spacy
        cls.nlp=spacy.load('en_core_web_sm',disable=['ner'])
    def selected(self,text,word):
        rows=extract(self.nlp(text));index={r['focus']['start']:r for r in rows}
        row=next(r for r in rows if r['focus']['text']==word)
        return propose(row,text,index)
    def test_direct_admission(self):
        self.assertEqual(self.selected('I took his life.','took')['target_prediction'],'admission')
    def test_direct_negation(self):
        self.assertEqual(self.selected('I did not kill him.','kill')['target_prediction'],'denial')
    def test_passive_patient_not_agent(self):
        result=self.selected('I was not paid.','paid')
        self.assertEqual(result['proposed_fields']['event_actor'],'unclear')
        self.assertEqual(result['proposed_fields']['polarity'],'negated')
    def test_explicit_passive_agent(self):
        self.assertEqual(self.selected('He was killed by me.','killed')['proposed_fields']['event_actor'],'self')
    def test_embedded_knowledge_holder(self):
        result=self.selected('I wanted you to know that I wronged your family.','know')
        self.assertEqual(result['proposed_fields']['event_actor'],'other')
        self.assertEqual(result['proposed_fields']['proposition_status'],'unclear')
    def test_ellipsis_unresolved(self):
        self.assertEqual(self.selected('I know he does, I feel it.','does')['proposed_fields']['event_type'],'unclear')
    def test_question_not_assertion(self):
        self.assertEqual(self.selected('Did I kill him?','kill')['proposed_fields']['proposition_status'],'unclear')
    def test_reporting_not_self_admission(self):
        self.assertNotEqual(self.selected('They say I killed him.','killed')['target_prediction'],'admission')

if __name__=='__main__':unittest.main()
