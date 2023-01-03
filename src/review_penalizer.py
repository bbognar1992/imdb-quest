import logging

import pandas as pd

modul_Logger = logging.getLogger('imdb_quest.review_penalizer')


def review_penalizer(df: pd.DataFrame):
    """
    Determine the penalty value for each movie rating.

    :param df: Object containing the scraped data from IMDB 250 list
    """
    modul_Logger.info("Started.")
    max_n_rating = df['n_ratings'].max()
    df['rating_deduction'] = df.apply(
        lambda x:  round(int((max_n_rating - x['n_ratings'])/100000) * 0.1, 1),
        axis=1
    )
    modul_Logger.info("Finished.")
