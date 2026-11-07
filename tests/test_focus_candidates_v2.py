import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from focus_candidates_v2 import candidates

class ConstructionChecks(unittest.TestCase):
    def test_auxiliary_links_to_exact_head(self):
        text='I did not murder him.'
        rows=candidates(text);aux=rows[0]
        self.assertEqual(aux['disposition'],'merge_auxiliary_with_head')
        h=aux['linked_lexical_head'];self.assertEqual(text[h['start']:h['end']],'murder')
        self.assertEqual(rows[1]['disposition'],'retain_literal_focus')
    def test_lexical_do_is_not_merged_without_head(self):
        self.assertNotEqual(candidates('I did it.')[0]['disposition'],'merge_auxiliary_with_head')
    def test_two_take_arguments_stay_separate(self):
        rows=candidates('They take a life and take the power.')
        self.assertEqual(rows[0]['disposition'],'retain_literal_focus')
        self.assertEqual(rows[1]['disposition'],'life_attachment_not_established')
    def test_passive_life_pattern(self):
        self.assertEqual(candidates('Their lives were not taken by me.')[0]['reason'],'local_life_argument_pattern')
    def test_nominal_flag_is_preserved(self):
        row=candidates("My family's murders.")[0]
        self.assertEqual(row['predicate_focus'],'murders')
        self.assertEqual(row['disposition'],'possible_nominal_use')
    def test_ellipsis_not_silently_deleted(self):
        row=candidates('I know he does, I feel it.')[1]
        self.assertEqual(row['disposition'],'needs_ellipsis_interpretation')
    def test_all_offsets_survive(self):
        text='I DID not know what happened. I took his life.'
        for row in candidates(text):
            self.assertEqual(text[row['focus_start']:row['focus_end']],row['predicate_focus'])

if __name__=='__main__':unittest.main()
