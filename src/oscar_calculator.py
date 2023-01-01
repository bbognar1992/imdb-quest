import pandas as pd


def oscar_calculator(df: pd.DataFrame):
    """
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

    df['rating_reward'] = df.apply(
        lambda x: oscar_reward_mapper(x['n_oscars']),
        axis=1
    )


