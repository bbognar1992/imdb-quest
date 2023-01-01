import os

import pandas as pd

from review_penalizer import review_penalizer
from scraper import scraper
from src.oscar_calculator import oscar_calculator

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'IMDB.csv')

    scraper(file_path)

    df = pd.read_csv(file_path).dropna()
    review_penalizer(df)
    oscar_calculator(df)

    print(df.head())

