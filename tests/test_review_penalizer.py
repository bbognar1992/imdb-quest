import unittest

import pandas as pd

from src.review_penalizer import review_penalizer


class TestReviewPenaluzer(unittest.TestCase):
    def test_review_penalizer(self):
        import os

        dict = {'title': ['fim1', 'fim2', 'fim3', 'fim4'],
                'rating': [9.5, 6, 7.1, 8.3],
                'n_ratings': [3021212, 1021221, 1000002, 400022],
                'n_oscars': [3, 0, 0, 11]
                }
        df = pd.DataFrame(dict)
        review_penalizer(df)
        assert 'rating_deduction' in df.columns
        assert 'penalized_rating' in df.columns



