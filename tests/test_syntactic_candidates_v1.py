"""Known development fixtures for the optional pinned syntax environment."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from syntactic_candidates_v1 import extract

class SyntaxBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import spacy
        cls.nlp=spacy.load('en_core_web_sm',disable=['ner'])
    def test_question_auxiliary(self):
        rows=extract(self.nlp('Did Roger come up here yet?'))
        come=next(r for r in rows if r['focus']['text']=='come')
        self.assertEqual([x['text'] for x in come['auxiliaries']],['Did'])
        self.assertEqual([x['text'] for x in come['subject_heads']],['Roger'])
        self.assertNotIn('Did',[r['focus']['text'] for r in rows])
    def test_two_objects_not_cross_attached(self):
        rows=extract(self.nlp('They take a life and take the power.'))
        takes=[r for r in rows if r['focus']['text']=='take']
        self.assertEqual([[o['text'] for o in r['object_or_complement_heads']] for r in takes],[['life'],['power']])
    def test_nominal_is_not_verb(self):
        self.assertEqual(extract(self.nlp("My family's murders.")),[])
    def test_layers_and_exact_offsets(self):
        text='I know you think I did this.'
        rows=extract(self.nlp(text))
        self.assertEqual([r['focus']['text'] for r in rows],['know','think','did'])
        for row in rows:
            f=row['focus'];self.assertEqual(text[f['start']:f['end']],f['text'])
    @unittest.expectedFailure
    def test_known_parser_failure_governing_layers(self):
        # Retain the desired structure as a visible known failure, not a changed
        # expected answer that would bless the parser's mistaken attachment.
        rows=extract(self.nlp('I know you think I did this.'))
        self.assertEqual([r['governing_predicate']['text'] if r['governing_predicate'] else None for r in rows],[None,'know','think'])
    def test_unparsed_input_rejected(self):
        import spacy
        with self.assertRaises(ValueError):extract(spacy.blank('en')('Hello.'))

if __name__=='__main__':unittest.main()
