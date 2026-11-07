"""Known-example-informed behavioral checks, not evaluation observations."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from focus_rules_v1 import predict

def selected(text, focus, occurrence=0):
    start = -1
    for _ in range(occurrence + 1):
        start = text.index(focus, start + 1)
    return predict(text, start, start + len(focus))[0]

class FocusBehavior(unittest.TestCase):
    def test_direct_denial(self):
        self.assertEqual(selected('I did not kill anyone.', 'kill'), 'denial')
    def test_other_negation_does_not_negate_action(self):
        self.assertEqual(selected('I killed him, not her.', 'killed'), 'admission')
    def test_patient_is_not_agent(self):
        self.assertEqual(selected('They killed me.', 'killed'), 'other')
    def test_two_foci_same_sentence(self):
        text = 'I know you think I killed him.'
        self.assertEqual(selected(text, 'know'), 'other')
        self.assertEqual(selected(text, 'killed'), 'abstain')
    def test_reported_denial(self):
        self.assertEqual(selected('People say I did not kill him.', 'kill'), 'abstain')
    def test_hypothesis(self):
        self.assertEqual(selected('If I killed him, I would be guilty.', 'killed'), 'abstain')
    def test_passive(self):
        self.assertEqual(selected('Their lives were not taken by me.', 'taken'), 'denial')
    def test_implicit_action(self):
        self.assertEqual(selected('I really did it.', 'did'), 'abstain')
    def test_characterization(self):
        self.assertEqual(selected('They call me a killer.', 'call'), 'other')
    def test_shooting_does_not_establish_death(self):
        self.assertEqual(selected('I shot him.', 'shot'), 'other')
    def test_forgiveness_frame(self):
        self.assertEqual(selected('Please forgive me for taking his life.', 'taking'), 'admission')
    def test_invalid_focus(self):
        with self.assertRaises(ValueError):
            predict('Hello', 3, 2)

if __name__ == '__main__':
    unittest.main()
