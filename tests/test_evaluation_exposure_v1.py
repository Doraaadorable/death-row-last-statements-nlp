"""Ensure documentary ID extraction does not consume fit numbers or weights."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from build_evaluation_exposure_v1 import component_ids

class DocumentaryIDs(unittest.TestCase):
    def test_wrapped_list(self):
        text = 'Nine documents examined: 293, 414,\n542 and 277. Weight 0.42.'
        self.assertEqual(component_ids(text), {293,414,542,277})
    def test_fit_suffix_is_not_an_id(self):
        text = 'Documents examined under each fit: 352, 423 and 274 (different ordering at k8).'
        self.assertEqual(component_ids(text), {352,423,274})
    def test_no_silent_empty_inventory(self):
        with self.assertRaises(ValueError):
            component_ids('No documentary ID list here.')

if __name__ == '__main__':
    unittest.main()
