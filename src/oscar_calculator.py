import logging

import pandas as pd

modul_Logger = logging.getLogger('imdb_quest.oscar_calculator')


def oscar_calculator(df: pd.DataFrame):
    """
    Determine the reward value for each movie rating.

    :param df: Object containing the scraped data from IMDB 250 list
    """

    def oscar_reward_mapper(n: int):
        if 1 <= n <= 2:
            return 0.3
        elif 3 <= n <= 5:
            return 0.5
        elif 6 <= n <= 10:
            return 1
        elif 10 < n:
            return 1.5
        else:
            return 0

    modul_Logger.info("Started.")
    df['rating_reward'] = df.apply(
        lambda x: oscar_reward_mapper(x['n_oscars']),
        axis=1
    )
    modul_Logger.info("Finished.")
