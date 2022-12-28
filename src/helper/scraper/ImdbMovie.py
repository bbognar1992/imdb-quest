import scrapy


class ImdbMovie(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    n_ratings = scrapy.Field()
    n_oscars = scrapy.Field()
