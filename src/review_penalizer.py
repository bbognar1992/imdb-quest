import pandas as pd


def review_penalizer(df: pd.DataFrame):
    """
    :param df: Object containing the scraped data from IMDB 250 list
    :return: df which has two new columns - rating reduction, penalized_rating
    """
    max_n_rating = df['n_ratings'].max()
    df['rating_deduction'] = df.apply(
        lambda x:  int((max_n_rating - x['n_ratings'])/100000) * 0.1,
        axis=1
    )
    df['penalized_rating'] = df['rating'] - df['rating_deduction']
    return df

