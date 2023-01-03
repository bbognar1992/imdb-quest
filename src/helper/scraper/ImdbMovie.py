import logging
import re

from scrapy import Item, Field

modul_Logger = logging.getLogger('imdb_quest.scraper')


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
        return value.replace(" user ratings", '').split(" based on ")[1].replace(',', '')
    except Exception:
        modul_Logger.error(f"Cannot determine the number of oscars from: '{value}'!")
        return ""


class ImdbMovie(Item):
    """Class for defining the data model."""

    title = Field()
    imdb_rating = Field()
    n_ratings = Field(serializer=serializer_n_ratings)
    n_oscars = Field(serializer=serialize_n_oscars)
