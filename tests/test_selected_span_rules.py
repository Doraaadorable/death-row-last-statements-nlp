"""Synthetic behavioral checks, never held-out performance evidence."""
from pathlib import Path
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from selected_span_rules import lexical, constrained
class RuleTests(unittest.TestCase):
    def test_direct_and_passive_denial(self):
        self.assertEqual(constrained('I did not kill anyone.')[0],'denial')
        self.assertEqual(constrained('Their lives were not taken by me.')[0],'denial')
    def test_explicit_self_attribution(self):
        self.assertEqual(constrained('Forgive me for taking his life.')[0],'admission')
    def test_imperative_hypothetical_and_epithet(self):
        for t in ['Warden, murder me.','Anyone who would have killed my children','They call me a murderer']:
            self.assertEqual(constrained(t)[0],'other')
    def test_attribution_abstains(self):
        self.assertEqual(constrained('I killed someone.','They say ')[0],'abstain')
    def test_negation_does_not_transfer_from_knowledge(self):
        self.assertEqual(constrained("I don't know whether I killed him.")[0],'abstain')
    def test_curly_quotes_and_specific_nonlethal_act(self):
        self.assertEqual(constrained('I didn’t kill him.')[0],'denial')
        self.assertEqual(constrained('I shot a man.')[0],'other')
    def test_uncertain_reference_is_not_an_ordinary_negative(self):
        import pandas as pd
        from run_selected_span_diagnostic import reference
        row=pd.Series(dict(claim_source='self',event_type='unclear',event_actor='self',polarity='affirmed',proposition_status='presented_as_true'))
        self.assertEqual(reference(row),'reference_uncertain')
        row['event_type']='killing_action';self.assertEqual(reference(row),'admission')
        row['claim_source']='other';self.assertEqual(reference(row),'other')
    def test_other_person_killing_is_not_personal_admission(self):
        self.assertEqual(constrained('They killed a man.')[0],'other')
    def test_lexical_limitation_is_visible(self):
        self.assertEqual(lexical('Warden, murder me.')[0],'admission')
if __name__=='__main__':unittest.main()
