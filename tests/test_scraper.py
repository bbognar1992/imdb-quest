import unittest

from src.scraper import scraper


class TestScraper(unittest.TestCase):
    def test_scraper(self):
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'IMDB.csv')
        scraper(file_path, limit=10)
        assert os.path.exists(file_path)
        import pandas as pd
        df = pd.read_csv(file_path).dropna()
        assert df.size > 0
        os.remove(file_path)




