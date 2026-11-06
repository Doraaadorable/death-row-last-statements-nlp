"""Synthetic retrieval-rule tests; not model-performance examples."""
import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from semantic_screening import screen_documents


class ScreeningTests(unittest.TestCase):
    def screen(self, texts):
        source = pd.DataFrame({'execution_number': range(len(texts)),
                               'model_text': texts, 'source_url': ['synthetic'] * len(texts)})
        original = source.copy(deep=True)
        result = screen_documents(source)
        pd.testing.assert_frame_equal(source, original)
        self.assertNotIn('claim_source', result.columns)
        return result

    def test_curly_apostrophe_and_case_are_retrieved(self):
        result = self.screen(["I didn’t KNOW.", "I DID NOT KILL anyone."])
        self.assertTrue(result.loc[0, 'negated_knowledge_cue'])
        self.assertTrue(result.loc[1, 'action_or_innocence_cue'])

    def test_reporting_alone_does_not_select_candidate(self):
        result = self.screen(['I want to say thank you.', 'My skills improved.'])
        self.assertTrue(result.loc[0, 'reporting_or_saying_cue'])
        self.assertFalse(result.candidate_document.any())

    def test_procedural_killing_is_only_a_cue(self):
        result = self.screen(['Do not kill me.'])
        self.assertTrue(result.loc[0, 'candidate_document'])
        self.assertNotIn('polarity', result.columns)


if __name__ == '__main__':
    unittest.main()
