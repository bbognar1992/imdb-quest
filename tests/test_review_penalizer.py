import unittest
import pandas as pd

from src.review_penalizer import review_penalizer


class TestReviewPenalizer(unittest.TestCase):
    def test_review_penalizer(self):
        data = {
            'title': ['fim1', 'fim2', 'fim3', 'fim4'],
            'n_ratings': [3021212, 1021221, 1000002, 400022],
        }
        df = pd.DataFrame(data)
        review_penalizer(df)
        assert 'rating_deduction' in df.columns
