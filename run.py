import logging
import os
import argparse

import pandas as pd

from src.scraper import scraper
from src.oscar_calculator import oscar_calculator
from src.review_penalizer import review_penalizer


def remove_file_if_exists(path: str):
    if os.path.exists(path):
        os.remove(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='The Big IMDB quest',
        description='The application scrapes data from IMDB and adjusts IMDB ratings based on defined rules.'
    )
    parser.add_argument('-l', '--limit', dest='limit', default=0, type=int, required=False,
                        help='Limit the number of movies to parse.')

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    original_file_path = os.path.join(dir_path, 'scraped_data.csv')
    remove_file_if_exists(original_file_path)

    scraper(original_file_path, limit=args.limit)

    df = pd.read_csv(original_file_path)
    review_penalizer(df)
    oscar_calculator(df)

    df['new_rating'] = df.apply(
        lambda x: round(x['rating'] - x['rating_deduction'] + x['rating_reward'], 1),
        axis=1
    )
    df.sort_values(by='new_rating', ascending=False, inplace=True)
    corrected_file_path = os.path.join(dir_path, 'ratings.csv')
    remove_file_if_exists(corrected_file_path)
    df.to_csv(corrected_file_path, index=False)
    remove_file_if_exists(original_file_path)
