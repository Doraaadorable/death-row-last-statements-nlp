import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from compare_confirmed_syntax_v1 import exact_alignment,field_relation

class AlignmentChecks(unittest.TestCase):
    def test_repeated_word_does_not_match_wrong_occurrence(self):
        rows=[{'focus':{'start':10,'end':14}},{'focus':{'start':30,'end':34}}]
        self.assertIs(exact_alignment(rows,30,34),rows[1])
        self.assertIsNone(exact_alignment(rows,20,24))
    def test_contained_head_not_forced_to_multiword_focus(self):
        self.assertIsNone(exact_alignment([{'focus':{'start':5,'end':8}}],5,20))
    def test_unclear_is_not_definite_conflict(self):
        self.assertEqual(field_relation('self','unclear'),'automatic_unclear')
        self.assertEqual(field_relation('unclear','self'),'reference_unclear')
        self.assertEqual(field_relation('self','other'),'definite_value_conflict')
    def test_duplicate_focus_rejected(self):
        with self.assertRaises(ValueError):exact_alignment([{'focus':{'start':1,'end':2}}]*2,1,2)

if __name__=='__main__':unittest.main()
