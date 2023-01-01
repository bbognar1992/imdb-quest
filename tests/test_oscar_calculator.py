import unittest
import pandas as pd

from src.oscar_calculator import oscar_calculator


class TestOscarCalculator(unittest.TestCase):
    def test_oscar_calculator(self):
        data = {
            'title': ['fim1', 'fim2', 'fim3', 'fim4', 'fim5'],
            'n_oscars': [3, 0, 1, 11, 6]
        }
        df = pd.DataFrame(data)
        oscar_calculator(df)
        assert 'rating_reward' in df.columns
