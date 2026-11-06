"""Focused regression checks for duplicate-column keyword diagnostics."""
import sys
import unittest
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from text_features import identical_column_groups, top_groups, group_jaccard


class FeatureGroupingTests(unittest.TestCase):
    def test_near_equal_columns_are_not_collapsed(self):
        X = csr_matrix([[1., 1., 1. + 1e-12], [0., 0., 0.]])
        self.assertEqual(identical_column_groups(X), [[0, 1], [2]])

    def test_cutoff_uses_alphabetical_group_representative(self):
        terms = np.array(['z', 'a', 'b'])
        groups = [[0, 1], [2]]
        self.assertEqual(top_groups(np.array([.5, .5, .5]), terms, groups, n=1), {0})

    def test_member_weight_swap_does_not_change_group_overlap(self):
        terms = np.array([f'term_{i:02}' for i in range(18)])
        groups = [[0, 1]] + [[i] for i in range(2, 18)]
        left = np.linspace(1., .1, 18)
        right = left.copy()
        right[0], right[1] = left[1], left[0]
        self.assertEqual(group_jaccard(left, right, terms, groups), 1.)


if __name__ == '__main__':
    unittest.main()
