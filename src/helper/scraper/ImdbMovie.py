import re

from scrapy import Item, Field


def serialize_n_oscars(value: str) -> str:
    """
    Get the number of Oscar awards from the string.

    :param value: String containing the highest awards from a movie.
    :return: String contains the number of oscars if there is any.
    """
    try:
        found = re.search(r"Won [\d]+ Oscar", value)
        return found.group(0).replace("Won ", "").replace(" Oscar", "")
    except Exception:
        return "0"


def serializer_n_ratings(value: str) -> str:
    """
    Convert string with number like K, M, B to numbers.

    :param value: String that contains a number.
    :return: The string converted to integer.
    """
    try:
        if 'K' in value:
            if len(value) > 1:
                return str(int(float(value.replace('K', '')) * 1000))
            return str(1000)
        if 'M' in value:
            if len(value) > 1:
                return str(int(float(value.replace('M', '')) * 1000000))
            return str(1000000)
        if 'B' in value:
            return str(int(float(value.replace('B', '')) * 1000000000))
        return str(0)
    except Exception:
        return str(0)


class ImdbMovie(Item):
    """Class for defining the data model."""

    title = Field()
    rating = Field()
    n_ratings = Field(serializer=serializer_n_ratings)
    n_oscars = Field(serializer=serialize_n_oscars)
