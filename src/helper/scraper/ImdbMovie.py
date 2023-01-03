from scrapy import Item, Field


class ImdbMovie(Item):
    """Class for defining the data model."""

    title = Field()
    rating = Field()
    n_ratings = Field()
    n_oscars = Field()
